"""Self-check for the prompt-cache breakpoint on conversation history.

Reproduces the intermittent 400 the owner saw ("messages.N.content.0.
thinking.cache_control: Extra inputs are not permitted"): the breakpoint
used to land on whatever block came last, including a thinking block,
which the API rejects. Also covers the quieter half of the same code:
history returned to the client carries last turn's breakpoint, so without
stripping, markers accumulate turn over turn toward the API's limit.

Run standalone from anywhere:
    python dev-tools/test_cache_breakpoint.py
"""
import os
import sys
import tempfile

BACKEND_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "ultron-backend")
FAKE_PKGS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fake_pkgs")
sys.path.insert(0, FAKE_PKGS_DIR)
sys.path.insert(0, BACKEND_DIR)

os.environ["ULTRON_API_TOKEN"] = "admin-test-token-with-32-characters!!"
os.environ["ANTHROPIC_API_KEY"] = "fake-key-for-test"
os.environ["ULTRON_DB_PATH"] = os.path.join(tempfile.mkdtemp(), "test_ultron.db")
os.environ["ULTRON_DISABLE_MEMORY_TRENDS"] = "1"
os.environ["ULTRON_DISABLE_METRICS_HISTORY"] = "1"
os.environ["ULTRON_SENTINEL_INTERVAL_SECONDS"] = "0"

import anthropic  # noqa: E402
import app  # noqa: E402

client = app.app.test_client()
ADMIN = {"Authorization": "Bearer admin-test-token-with-32-characters!!"}
CC = {"type": "ephemeral"}


def _cc_blocks(messages):
    """(message index, block index, block type) for every cache_control marker."""
    out = []
    for mi, m in enumerate(messages):
        c = m.get("content")
        if isinstance(c, list):
            for bi, b in enumerate(c):
                if isinstance(b, dict) and "cache_control" in b:
                    out.append((mi, bi, b.get("type")))
    return out


def demo():
    # A thinking block last: the marker must land on the last cacheable
    # block instead, never on the thinking block.
    msg = {"role": "assistant", "content": [
        {"type": "text", "text": "answer"},
        {"type": "thinking", "thinking": "hmm", "signature": "sig"},
    ]}
    out = app._add_cache_breakpoint(msg)
    assert out["content"][0].get("cache_control") == CC and "cache_control" not in out["content"][1], out
    assert "cache_control" not in msg["content"][0], "must not mutate the caller's message"

    # Only thinking blocks: leave the message alone.
    only = {"role": "assistant", "content": [{"type": "thinking", "thinking": "x", "signature": "s"}]}
    assert app._add_cache_breakpoint(only) == only

    # The exact failing shape: content.0 is thinking, then a tool_use.
    shaped = {"role": "assistant", "content": [
        {"type": "thinking", "thinking": "x", "signature": "s"},
        {"type": "tool_use", "id": "t1", "name": "get_system_status", "input": {}},
    ]}
    out = app._add_cache_breakpoint(shaped)
    assert "cache_control" not in out["content"][0] and out["content"][1]["cache_control"] == CC, out

    # Plain string content still becomes one tagged text block.
    out = app._add_cache_breakpoint({"role": "user", "content": "hi"})
    assert out["content"] == [{"type": "text", "text": "hi", "cache_control": CC}], out

    # Stale markers coming back from the client are stripped.
    stale = [
        {"role": "user", "content": [{"type": "text", "text": "a", "cache_control": CC}]},
        {"role": "assistant", "content": [{"type": "text", "text": "b", "cache_control": CC}]},
        {"role": "user", "content": "c"},
    ]
    assert _cc_blocks(app._strip_cache_control(stale)) == []
    assert _cc_blocks(stale) == [(0, 0, "text"), (1, 0, "text")], "must not mutate the caller's history"

    # End to end through /api/chat: a 12-message history full of stale
    # markers and a thinking-last final assistant turn goes out with exactly
    # ONE marker in messages, on a cacheable block of the last history
    # message -- so the request the owner's dashboard makes on turn 12 is
    # valid, where it used to 400.
    history = []
    for i in range(5):
        history.append({"role": "user", "content": [{"type": "text", "text": f"q{i}", "cache_control": CC}]})
        history.append({"role": "assistant", "content": [{"type": "text", "text": f"a{i}", "cache_control": CC}]})
    history.append({"role": "user", "content": "q5"})
    history.append({"role": "assistant", "content": [
        {"type": "text", "text": "a5"},
        {"type": "thinking", "thinking": "deep", "signature": "sig"},
    ]})
    app.anthropic_client.messages.script.append(anthropic.Message(
        content=[anthropic.ContentBlock(type="text", text="ok")], stop_reason="end_turn",
        usage=anthropic.Usage(input_tokens=5, output_tokens=5)))
    r = client.post("/api/chat", json={"message": "q6", "history": history}, headers=ADMIN)
    assert r.status_code == 200, r.get_json()
    sent = app.anthropic_client.messages.calls[-1]["messages"]
    markers = _cc_blocks(sent)
    assert markers == [(11, 0, "text")], markers
    assert sent[11]["content"][1]["type"] == "thinking" and "cache_control" not in sent[11]["content"][1]
    # And the history handed back still carries that one marker -- which
    # the NEXT turn's strip removes again, so the count never grows.
    assert len(_cc_blocks(r.get_json()["history"])) == 1

    print("OK: the cache breakpoint skips thinking blocks (lands on the last cacheable block, or nowhere), "
          "stale markers from returned history are stripped, and a 12-message thinking-last history goes out "
          "with exactly one marker.")


if __name__ == "__main__":
    demo()
