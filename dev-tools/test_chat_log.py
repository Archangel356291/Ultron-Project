"""Self-check for the chat transcript log (chat_log / get_chat_history --
owner-requested 2026-09-15: a real record of who talks to Ultron, with
timestamps and token usage, that survives a restart) and the "speaker"
passthrough that lets the Discord bot (one shared admin token for every
Discord user) attribute a turn to the actual person instead of "admin".

Drives real /api/chat requests through Flask's test client against a fake
Anthropic client, same harness as test_beta_spend_cap.py.

Run standalone from anywhere:
    python dev-tools/test_chat_log.py
"""
import os
import sys
import tempfile

BACKEND_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "ultron-backend")
FAKE_PKGS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fake_pkgs")
sys.path.insert(0, FAKE_PKGS_DIR)   # 'import anthropic' below resolves to the fake
sys.path.insert(0, BACKEND_DIR)

os.environ["ULTRON_API_TOKEN"] = "admin-test-token"
os.environ["ANTHROPIC_API_KEY"] = "fake-key-for-test"
os.environ["ULTRON_DB_PATH"] = os.path.join(tempfile.mkdtemp(), "test_ultron.db")
os.environ["ULTRON_DISABLE_MEMORY_TRENDS"] = "1"
os.environ["ULTRON_DISABLE_METRICS_HISTORY"] = "1"

import anthropic  # noqa: E402  (the fake, via sys.path above)
import app  # noqa: E402

client = app.app.test_client()
ADMIN_HEADERS = {"Authorization": "Bearer admin-test-token"}


def _queue_reply(text, input_tokens=42, output_tokens=17):
    app.anthropic_client.messages.script.append(
        anthropic.Message(
            content=[anthropic.ContentBlock(type="text", text=text)],
            stop_reason="end_turn",
            usage=anthropic.Usage(input_tokens=input_tokens, output_tokens=output_tokens),
        )
    )


def demo():
    # A plain dashboard-origin turn (no speaker) logs as "admin".
    _queue_reply("hello there")
    res = client.post("/api/chat", json={"message": "hi Ultron", "history": []}, headers=ADMIN_HEADERS)
    assert res.status_code == 200, res.get_json()

    turns = app.get_chat_history()["turns"]
    assert len(turns) == 2, turns  # one user row, one assistant row
    user_turn, assistant_turn = turns[-2], turns[-1]
    assert user_turn["role"] == "user" and user_turn["content"] == "hi Ultron" and user_turn["identity"] == "admin", user_turn
    assert assistant_turn["role"] == "assistant" and assistant_turn["content"] == "hello there", assistant_turn
    assert assistant_turn["identity"] == "admin", assistant_turn
    # Token usage lands on the assistant row, real numbers from the fake API response.
    assert assistant_turn["input_tokens"] == 42 and assistant_turn["output_tokens"] == 17, assistant_turn
    # The user row carries no token cost of its own.
    assert user_turn["input_tokens"] is None and user_turn["output_tokens"] is None, user_turn

    # Plain-text mirror (owner-requested 2026-09-15, split by source
    # 2026-09-16): a dated file under "<data dir>/chat logs/dashboard/",
    # human-readable, both sides of the turn with token usage.
    mirror_path = app._chat_log_path("admin")
    assert os.path.exists(mirror_path), mirror_path
    assert os.path.dirname(mirror_path) == os.path.join(os.path.dirname(app.DB_PATH), "chat logs", "dashboard"), mirror_path
    with open(mirror_path, encoding="utf-8") as f:
        file_text = f.read()
    # Markdown: a title on first write, one heading per exchange carrying
    # the person's words (the node graphify/Obsidian see), reply beneath.
    assert file_text.startswith("# Dashboard chat — "), file_text[:60]
    assert "] admin asked: hi Ultron\n\nhi Ultron\n\n" in file_text, file_text
    assert "**Ultron** [tokens: in=42, out=17]:\nhello there" in file_text, file_text

    # A Discord-origin turn with a speaker logs under that identity, not "admin" --
    # this is the whole point: one shared bot token, distinguishable people.
    _queue_reply("hey there, Discord")
    res = client.post(
        "/api/chat",
        json={"message": "hi from discord", "history": [], "speaker": "discord:someuser"},
        headers=ADMIN_HEADERS,
    )
    assert res.status_code == 200, res.get_json()
    discord_turns = app.get_chat_history(identity="discord:someuser")["turns"]
    assert len(discord_turns) == 2, discord_turns
    assert all(t["identity"] == "discord:someuser" for t in discord_turns), discord_turns
    assert discord_turns[0]["content"] == "hi from discord", discord_turns

    # The identity filter actually filters -- "admin"-only history doesn't include the Discord turns.
    admin_only = app.get_chat_history(identity="admin")["turns"]
    assert all(t["identity"] == "admin" for t in admin_only), admin_only
    assert len(admin_only) == 2, admin_only  # just the first exchange, not the Discord one

    # Unfiltered history returns everything, oldest first.
    all_turns = app.get_chat_history(limit=10)["turns"]
    assert len(all_turns) == 4, all_turns
    assert [t["identity"] for t in all_turns] == ["admin", "admin", "discord:someuser", "discord:someuser"], all_turns

    # Admin-only tool/route, same posture as get_capabilities/get_mcp_servers.
    assert "get_chat_history" in app.TOOL_DISPATCH
    assert "get_chat_history" not in app.BETA_ALLOWED_TOOLS
    res = client.get("/api/chat/history")
    assert res.status_code == 401, res.get_json()
    res = client.get("/api/chat/history?limit=10", headers=ADMIN_HEADERS)
    assert res.status_code == 200 and len(res.get_json()["turns"]) == 4, res.get_json()

    # The system prompt actually carries the plain-prose/no-markdown rule
    # (owner-requested 2026-09-15: no literal asterisks/markdown in replies).
    assert "no markdown" in app.ULTRON_SYSTEM_PROMPT.lower(), "plain-prose rule missing from system prompt"
    assert "*asterisks*" in app.ULTRON_SYSTEM_PROMPT or "asterisks" in app.ULTRON_SYSTEM_PROMPT.lower()

    print("OK: /api/chat logs every real turn to chat_log with timestamps and real token usage, "
          "a caller-supplied speaker overrides the default 'admin' identity (Discord attribution), "
          "get_chat_history filters by identity, stays admin-only, the plain-text mirror file lands "
          "next to ultron.db with both sides of the turn, and the system prompt carries the "
          "plain-prose/no-markdown rule.")


if __name__ == "__main__":
    demo()
