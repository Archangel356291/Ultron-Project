"""Self-check for Economy mode ("lite": true on /api/chat).

Proves the mechanism against the fake Anthropic client, not just that the
constants exist: a lite request really goes out with the lite model, the
capped max_tokens and only the six basic tools; a normal request is
untouched; the lite tool-round cap really stops the loop; and usage is
priced at the lite model's rate, so the saving on the Data & analytics
tab is real dollars, not a label.

Run standalone from anywhere:
    python dev-tools/test_economy_mode.py
"""
import os
import sys
import tempfile

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

import anthropic  # noqa: E402
import app  # noqa: E402

client = app.app.test_client()
ADMIN = {"Authorization": "Bearer admin-test-token"}
BETA = {"Authorization": "Bearer beta-test-token"}
calls = app.anthropic_client.messages.calls
script = app.anthropic_client.messages.script


def _text_reply(usage=None):
    return anthropic.Message(
        content=[anthropic.ContentBlock(type="text", text="ok")],
        stop_reason="end_turn",
        usage=usage or anthropic.Usage(input_tokens=10, output_tokens=10),
    )


def _tool_call(name):
    return anthropic.Message(
        content=[anthropic.ContentBlock(type="tool_use", id="toolu_1", name=name, input={})],
        stop_reason="tool_use",
        usage=anthropic.Usage(input_tokens=10, output_tokens=10),
    )


def demo():
    assert app.LITE_MODEL != app.LLM_MODEL, "lite must actually be a different (cheaper) model"
    assert app.LITE_MODEL in app.LLM_PRICING_PER_MTOK, "lite model needs a pricing row or usage logs at $0"
    assert app.LITE_ALLOWED_TOOLS <= set(app.TOOL_DISPATCH), "every lite tool must be a real tool"

    # 1. Lite request: lite model, capped tokens, only the six basic tools.
    script.append(_text_reply())
    r = client.post("/api/chat", json={"message": "status?", "history": [], "lite": True}, headers=ADMIN)
    assert r.status_code == 200, r.get_json()
    assert r.get_json()["lite"] is True, r.get_json()
    sent = calls[-1]
    assert sent["model"] == app.LITE_MODEL, sent["model"]
    assert sent["max_tokens"] == app.LITE_MAX_TOKENS, sent["max_tokens"]
    assert {t["name"] for t in sent["tools"]} == app.LITE_ALLOWED_TOOLS, sorted(t["name"] for t in sent["tools"])

    # 2. Normal request: untouched -- default model, full tool list, full cap.
    script.append(_text_reply())
    r = client.post("/api/chat", json={"message": "status?", "history": []}, headers=ADMIN)
    assert r.status_code == 200, r.get_json()
    assert r.get_json()["lite"] is False
    sent = calls[-1]
    assert sent["model"] == app.LLM_MODEL
    assert sent["max_tokens"] == app.LLM_MAX_TOKENS
    assert len(sent["tools"]) == len(app.TOOLS), (len(sent["tools"]), len(app.TOOLS))

    # 3. Lite never widens a role: a beta tester in lite gets the beta
    #    allowlist intersected with the lite set (here: nothing).
    script.append(_text_reply())
    r = client.post("/api/chat", json={"message": "hi", "history": [], "lite": True}, headers=BETA)
    assert r.status_code == 200, r.get_json()
    assert {t["name"] for t in calls[-1]["tools"]} == (app.BETA_ALLOWED_TOOLS & app.LITE_ALLOWED_TOOLS)

    # 4. Lite tool-round cap really stops the loop: the model keeps asking
    #    for tools, only LITE_MAX_TOOL_ITERATIONS calls go out, and the
    #    reply is the honest "hit my limit" text, not a silent extra round.
    before = len(calls)
    for _ in range(app.LITE_MAX_TOOL_ITERATIONS):
        script.append(_tool_call("get_system_status"))
    script.append(_text_reply())  # would be consumed by a third round if the cap failed
    r = client.post("/api/chat", json={"message": "dig deep", "history": [], "lite": True}, headers=ADMIN)
    assert r.status_code == 200, r.get_json()
    assert len(calls) - before == app.LITE_MAX_TOOL_ITERATIONS, len(calls) - before
    assert "tool-call limit" in r.get_json()["reply"], r.get_json()["reply"]
    assert r.get_json()["tools_used"] == ["get_system_status"] * app.LITE_MAX_TOOL_ITERATIONS
    script.pop()  # the unused spare reply

    # 5. A lite tool call outside the lite set is refused server-side even
    #    if the model somehow asks for it (the same "forbidden" as beta).
    script.append(_tool_call("get_repo_diff"))
    script.append(_text_reply())
    r = client.post("/api/chat", json={"message": "diff?", "history": [], "lite": True}, headers=ADMIN)
    assert r.status_code == 200, r.get_json()
    tool_result = calls[-1]["messages"][-1]["content"][0]["content"]
    assert "forbidden" in tool_result, tool_result

    # 6. Usage is priced at the lite model's rate. 1,000,000 output tokens:
    #    $5 on claude-haiku-4-5 vs $10 on claude-sonnet-5.
    million_out = anthropic.Usage(input_tokens=0, output_tokens=1_000_000)
    script.append(_text_reply(usage=million_out))
    client.post("/api/chat", json={"message": "hi", "history": [], "lite": True}, headers=BETA)
    lite_cost = app._beta_tester_spend_usd("tester")
    expected = app.LLM_PRICING_PER_MTOK[app.LITE_MODEL]["output"]
    assert abs(lite_cost - expected) < 0.01, (lite_cost, expected)
    assert lite_cost < app.LLM_PRICING_PER_MTOK[app.LLM_MODEL]["output"], "lite must be cheaper than default"

    print("OK: Economy mode sends %s with max_tokens=%d and only %d tools, leaves normal chat "
          "untouched, never widens a role, stops after %d tool rounds, refuses non-lite tools, "
          "and logs usage at the lite model's price." % (
              app.LITE_MODEL, app.LITE_MAX_TOKENS, len(app.LITE_ALLOWED_TOOLS), app.LITE_MAX_TOOL_ITERATIONS))


if __name__ == "__main__":
    demo()
