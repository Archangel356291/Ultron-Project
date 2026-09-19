"""Self-check for Odin's read of the room: get_briefing() and the
SITUATIONAL CONTEXT block run_ultron_chat hands the model.

Proves against the fake Anthropic client that an admin turn goes out with
two system blocks -- the cached static prompt plus a context block that
carries live facts, Sentinel's state and the memory notes related to what
was just said -- that the block is marked as information-not-instruction,
that a beta tester's turn gets NO such block (host state and memory are
admin-only), and that the briefing route/tool are admin-only and cheap.

Run standalone from anywhere:
    python dev-tools/test_situational_context.py
"""
import os
import sys
import tempfile
import time

BACKEND_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "odin-backend")
FAKE_PKGS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fake_pkgs")
sys.path.insert(0, FAKE_PKGS_DIR)
sys.path.insert(0, BACKEND_DIR)

os.environ["ODIN_API_TOKEN"] = "admin-test-token"
os.environ["ODIN_BETA_TOKENS"] = "tester:beta-test-token"
os.environ["ANTHROPIC_API_KEY"] = "fake-key-for-test"
os.environ["ODIN_DB_PATH"] = os.path.join(tempfile.mkdtemp(), "test_odin.db")
os.environ["ODIN_DISABLE_MEMORY_TRENDS"] = "1"
os.environ["ODIN_DISABLE_METRICS_HISTORY"] = "1"
os.environ["ODIN_SENTINEL_INTERVAL_SECONDS"] = "0"

import anthropic  # noqa: E402
import app  # noqa: E402

client = app.app.test_client()
ADMIN = {"Authorization": "Bearer admin-test-token"}
BETA = {"Authorization": "Bearer beta-test-token"}
calls = app.anthropic_client.messages.calls
script = app.anthropic_client.messages.script


def _reply():
    return anthropic.Message(content=[anthropic.ContentBlock(type="text", text="ok")],
                             stop_reason="end_turn", usage=anthropic.Usage(input_tokens=5, output_tokens=5))


def demo():
    # A controlled host: one stopped container, a lockout, a remembered fact.
    app.docker_ps = lambda: ([
        {"name": "odin-backend", "image": "x", "status": "Up 3 hours", "running_for": "", "state": "running"},
        {"name": "jellyfin", "image": "y", "status": "Exited (137)", "running_for": "", "state": "stopped"},
    ], None)
    app._login_lockouts["203.0.113.9"] = time.time() + 900
    app._sentinel_run_once()
    saved = app.remember_note(note="The Jellyfin box is called mediabox and lives on the shelf by the router")
    assert "saved" in saved, saved

    # Briefing: real lines from real (controlled) data, cheap, no LLM.
    b = app.get_briefing()
    assert b["lines"] and all(isinstance(l, str) for l in b["lines"]), b
    joined = " ".join(b["lines"])
    assert "1 of 2 containers up" in joined, joined
    assert "1 container not running" in joined, joined
    assert "Sentinel has" in joined and "lockout" in joined, joined
    assert "things in memory" in joined, joined
    assert b["facts"]["sentinel_active"] >= 1 and b["facts"]["memory_notes"] >= 1, b["facts"]
    assert len(calls) == 0, "the briefing must never call the model"

    # Route: admin-only.
    assert client.get("/api/briefing", headers=ADMIN).status_code == 200
    assert client.get("/api/briefing", headers=BETA).status_code == 403
    assert client.get("/api/briefing").status_code == 401
    assert "get_briefing" in app.TOOL_DISPATCH and "get_briefing" in app.LITE_ALLOWED_TOOLS

    # Admin chat: two system blocks; the static one keeps its cache
    # breakpoint; the second carries the room and the relevant memory.
    script.append(_reply())
    r = client.post("/api/chat", json={"message": "is jellyfin ok?", "history": []}, headers=ADMIN)
    assert r.status_code == 200, r.get_json()
    system = calls[-1]["system"]
    assert len(system) == 2, [s.get("text", "")[:40] for s in system]
    assert system[0]["text"] == app.ODIN_SYSTEM_PROMPT and system[0].get("cache_control") == {"type": "ephemeral"}
    ctx = system[1]["text"]
    assert "cache_control" not in system[1], "the per-turn block must not be cached"
    assert ctx.startswith("SITUATIONAL CONTEXT") and "never instruction" in ctx, ctx[:200]
    assert "1 of 2 containers up" in ctx and "Sentinel has" in ctx, ctx
    assert "mediabox" in ctx, "the related memory note should be surfaced for a jellyfin question"
    assert len(ctx) < 4000, len(ctx)

    # Beta chat: exactly one system block -- no host state, no memory.
    script.append(_reply())
    r = client.post("/api/chat", json={"message": "is jellyfin ok?", "history": []}, headers=BETA)
    assert r.status_code == 200, r.get_json()
    assert len(calls[-1]["system"]) == 1, "beta must never receive the situational block"

    # Economy mode still gets the block (it is local and free, and saves tool rounds).
    script.append(_reply())
    client.post("/api/chat", json={"message": "status?", "history": [], "lite": True}, headers=ADMIN)
    assert len(calls[-1]["system"]) == 2 and calls[-1]["model"] == app.LITE_MODEL

    # The prompt now carries the bearing guidance and the learning rule.
    assert "already looked" in app.ODIN_SYSTEM_PROMPT and "remember_note only when the person" in app.ODIN_SYSTEM_PROMPT

    print("OK: get_briefing reads the room from local data with no model call; admin turns carry a "
          "SITUATIONAL CONTEXT block (facts + Sentinel + related memory, uncached, marked as information); "
          "beta turns carry none; route is admin-only; Economy mode keeps the block.")


if __name__ == "__main__":
    demo()
