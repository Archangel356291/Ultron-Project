"""Self-check for the beta-tester $1 spend cap (ULTRON_BETA_MAX_SPEND_USD).

Proves the actual enforcement mechanism, not just that the setting exists:
drives real /api/chat requests through Flask's test client against a fake
Anthropic client (fake_pkgs/anthropic) that returns expensive canned usage,
and asserts the request is genuinely refused (429) once the tester's real
computed spend reaches the cap — while an admin token making the same
request never gets capped.

Run standalone from anywhere:
    python dev-tools/test_beta_spend_cap.py
"""
import os
import sys
import tempfile

BACKEND_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "ultron-backend")
FAKE_PKGS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fake_pkgs")
sys.path.insert(0, FAKE_PKGS_DIR)   # 'import anthropic' below resolves to the fake
sys.path.insert(0, BACKEND_DIR)

os.environ["ULTRON_API_TOKEN"] = "admin-test-token"
os.environ["ULTRON_BETA_TOKENS"] = "tester:beta-test-token"
os.environ["ANTHROPIC_API_KEY"] = "fake-key-for-test"
os.environ["ULTRON_BETA_MAX_SPEND_USD"] = "1.00"
os.environ["ULTRON_DB_PATH"] = os.path.join(tempfile.mkdtemp(), "test_ultron.db")

import anthropic  # noqa: E402  (the fake, via sys.path above)
import app  # noqa: E402

client = app.app.test_client()
ADMIN_HEADERS = {"Authorization": "Bearer admin-test-token"}
BETA_HEADERS = {"Authorization": "Bearer beta-test-token"}

# claude-sonnet-5 pricing in app.LLM_PRICING_PER_MTOK: $10/MTok output.
# 60,000 output tokens -> $0.60 per call, so two calls cross the $1.00 cap.
EXPENSIVE_USAGE = anthropic.Usage(input_tokens=100, output_tokens=60_000)


def _queue_reply():
    app.anthropic_client.messages.script.append(
        anthropic.Message(
            content=[anthropic.ContentBlock(type="text", text="ok")],
            stop_reason="end_turn",
            usage=EXPENSIVE_USAGE,
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

    print("OK: beta spend cap refuses chat once >= $%.2f, admin unaffected, presence tracked." % app.BETA_MAX_SPEND_USD)


if __name__ == "__main__":
    demo()
