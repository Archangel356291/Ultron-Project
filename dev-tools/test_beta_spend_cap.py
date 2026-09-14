"""Self-check for the beta-tester $1 spend cap (ULTRON_BETA_MAX_SPEND_USD)
and the concurrency/scope gaps found in the 2026-09-14 pre-launch review.

Proves the actual enforcement mechanism, not just that the setting exists:
drives real /api/chat (and /api/tts) requests through Flask's test client
against a fake Anthropic client (fake_pkgs/anthropic) that returns
expensive canned usage, and asserts each request is genuinely refused
(429) once the tester's real computed spend reaches the cap — while an
admin token making the same request never gets capped.

Also covers, each tied to a specific review finding:
- The oversized-history-message cap (one huge history entry can no longer
  blow past the whole $1 budget in a single request).
- The per-tester lock closing the check-then-act race (two genuinely
  concurrent requests from the same beta identity can't both slip through
  before either logs its usage).
- /api/tts being subject to the same cap as /api/chat (voice replies
  were previously unbounded cost for a beta tester, outside the cap
  entirely).

Run standalone from anywhere:
    python dev-tools/test_beta_spend_cap.py
"""
import os
import sys
import tempfile
import threading

BACKEND_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "ultron-backend")
FAKE_PKGS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fake_pkgs")
sys.path.insert(0, FAKE_PKGS_DIR)   # 'import anthropic' below resolves to the fake
sys.path.insert(0, BACKEND_DIR)

os.environ["ULTRON_API_TOKEN"] = "admin-test-token"
os.environ["ULTRON_BETA_TOKENS"] = "tester:beta-test-token,racer:beta-test-token-racer"
os.environ["ANTHROPIC_API_KEY"] = "fake-key-for-test"
os.environ["ULTRON_BETA_MAX_SPEND_USD"] = "1.00"
os.environ["ULTRON_DB_PATH"] = os.path.join(tempfile.mkdtemp(), "test_ultron.db")
os.environ["ULTRON_FISH_AUDIO_API_KEY"] = "fake-fish-key"
os.environ["ULTRON_FISH_VOICE_ID"] = "fake-voice-id"
os.environ["ULTRON_DISABLE_MEMORY_TRENDS"] = "1"  # keep the spend-cap assertions deterministic

import anthropic  # noqa: E402  (the fake, via sys.path above)
import app  # noqa: E402

app._fish_audio_tts = lambda text: ([b"fake-mp3-bytes"], "audio/mpeg", None)  # matches the streaming (chunk-iterable) contract

client = app.app.test_client()
ADMIN_HEADERS = {"Authorization": "Bearer admin-test-token"}
BETA_HEADERS = {"Authorization": "Bearer beta-test-token"}
RACER_HEADERS = {"Authorization": "Bearer beta-test-token-racer"}

# claude-sonnet-5 pricing in app.LLM_PRICING_PER_MTOK: $10/MTok output.
# 60,000 output tokens -> $0.60 per call, so two calls cross the $1.00 cap.
EXPENSIVE_USAGE = anthropic.Usage(input_tokens=100, output_tokens=60_000)
# 90,000 output tokens -> exactly $0.90, used to seed "racer" close to the
# cap without already being over it, for the concurrency-race check below.
NINETY_CENT_USAGE = anthropic.Usage(input_tokens=100, output_tokens=90_000)


def _queue_reply(usage=EXPENSIVE_USAGE):
    app.anthropic_client.messages.script.append(
        anthropic.Message(
            content=[anthropic.ContentBlock(type="text", text="ok")],
            stop_reason="end_turn",
            usage=usage,
        )
    )


def demo():
    assert app.LLM_MODEL == "claude-sonnet-5", "test assumes default pricing; update EXPENSIVE_USAGE if this changes"

    # Call 1: under the cap, should succeed.
    _queue_reply()
    r1 = client.post("/api/chat", json={"message": "hi", "history": []}, headers=BETA_HEADERS)
    assert r1.status_code == 200, r1.get_json()
    spend_after_1 = app._beta_tester_spend_usd("tester")
    assert 0.55 < spend_after_1 < 0.65, f"expected ~$0.60, got {spend_after_1}"

    # Call 2: pushes cumulative spend over $1.00 — but this call itself is
    # allowed (the cap is checked *before* the call, using spend-so-far).
    _queue_reply()
    r2 = client.post("/api/chat", json={"message": "hi again", "history": []}, headers=BETA_HEADERS)
    assert r2.status_code == 200, r2.get_json()
    spend_after_2 = app._beta_tester_spend_usd("tester")
    assert spend_after_2 >= app.BETA_MAX_SPEND_USD, f"expected >= $1.00 cap, got {spend_after_2}"

    # Call 3: now genuinely refused — this is the real mechanism, not a
    # displayed number. No fake reply queued, so if this call is NOT
    # refused before reaching anthropic_client.messages.create(), the fake's
    # "script exhausted" RuntimeError would surface instead and fail loudly.
    r3 = client.post("/api/chat", json={"message": "one more"}, headers=BETA_HEADERS)
    assert r3.status_code == 429, r3.get_json()
    assert "spend limit" in r3.get_json()["error"]

    # Admin is never subject to this cap, even after a tester maxed out.
    _queue_reply()
    r4 = client.post("/api/chat", json={"message": "admin chat", "history": []}, headers=ADMIN_HEADERS)
    assert r4.status_code == 200, r4.get_json()

    # Presence tracking: both identities should now show up as connected.
    conn = client.get("/api/connections", headers=ADMIN_HEADERS).get_json()
    names = {p["name"] for p in conn["people"]}
    assert "tester" in names and "admin" in names, conn

    # /api/tts is subject to the same cap -- "tester" is already over it.
    r5 = client.post("/api/tts", json={"text": "hello"}, headers=BETA_HEADERS)
    assert r5.status_code == 429, r5.get_json()
    assert "spend limit" in r5.get_json()["error"]

    # Oversized single history entry: MAX_HISTORY_MESSAGES only caps entry
    # *count* (40) -- without a per-entry size cap, one huge entry could
    # blow past the whole $1 budget in a single request. "racer" is still
    # at $0.00, so this must be rejected on shape, not the spend cap.
    huge_history = [{"role": "user", "content": "x" * (app.MAX_HISTORY_MESSAGE_CHARS + 1)}]
    r6 = client.post("/api/chat", json={"message": "hi", "history": huge_history}, headers=RACER_HEADERS)
    assert r6.status_code == 400, r6.get_json()
    assert "exceeds" in r6.get_json()["error"]

    # Concurrency race: seed "racer" to exactly $0.90 (under the $1.00 cap),
    # then fire two genuinely concurrent /api/chat calls. Both threads read
    # spend, call the LLM, and log usage inside BETA_SPEND_LOCKS["racer"] --
    # if that lock didn't serialize this, both could read "$0.90 < cap"
    # before either logged its $0.60, letting combined spend reach $2.10
    # from two calls the cap was supposed to allow only one of. With the
    # lock, exactly one call succeeds (-> ~$1.50 total) and the other is
    # refused, deterministically regardless of thread scheduling, because
    # the second thread can't even start its check until the first
    # releases the lock.
    app._log_llm_usage(NINETY_CENT_USAGE, beta_name="racer")
    seeded = app._beta_tester_spend_usd("racer")
    assert 0.85 < seeded < 0.95, f"expected ~$0.90 seed, got {seeded}"

    _queue_reply()
    _queue_reply()
    results = [None, None]

    def _fire(idx):
        results[idx] = client.post(
            "/api/chat", json={"message": "race", "history": []}, headers=RACER_HEADERS
        )

    threads = [threading.Thread(target=_fire, args=(i,)) for i in range(2)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    codes = sorted(r.status_code for r in results)
    assert codes == [200, 429], f"expected exactly one 200 and one 429, got {codes}"
    racer_final = app._beta_tester_spend_usd("racer")
    assert 1.45 < racer_final < 1.55, f"expected ~$1.50 (one call landed, one refused), got {racer_final}"

    print("OK: beta spend cap refuses /api/chat and /api/tts once >= $%.2f, "
          "admin unaffected, oversized history rejected, concurrent same-tester "
          "requests serialized correctly, presence tracked." % app.BETA_MAX_SPEND_USD)


if __name__ == "__main__":
    demo()
