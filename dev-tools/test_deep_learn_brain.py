"""Self-check for Deep thought mode, Learn-from-conversations, and the
Brain & Knowledge folder layout (split chat logs + the memory mirror).

Against the fake Anthropic client: a deep request really goes out on the
deep model with the larger caps and wins over lite; a beta tester's deep
flag is ignored; learning runs one lite-model call after an admin turn,
saves exactly one new note (with an activity entry), skips NONE and
duplicates, and never runs for beta. On disk: dashboard and Discord turns
land in separate dated files under "chat logs/", and knowledge/
memory-notes.md mirrors the notebook.

Run standalone from anywhere:
    python dev-tools/test_deep_learn_brain.py
"""
import os
import sys
import tempfile
import time

BACKEND_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "odin-backend")
FAKE_PKGS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fake_pkgs")
sys.path.insert(0, FAKE_PKGS_DIR)
sys.path.insert(0, BACKEND_DIR)

DATA_DIR = tempfile.mkdtemp()
os.environ["ODIN_API_TOKEN"] = "admin-test-token"
os.environ["ODIN_BETA_TOKENS"] = "tester:beta-test-token"
os.environ["ANTHROPIC_API_KEY"] = "fake-key-for-test"
os.environ["ODIN_DB_PATH"] = os.path.join(DATA_DIR, "odin.db")
os.environ["ODIN_DISABLE_MEMORY_TRENDS"] = "1"
os.environ["ODIN_DISABLE_METRICS_HISTORY"] = "1"
os.environ["ODIN_SENTINEL_INTERVAL_SECONDS"] = "0"
os.environ["ODIN_LEARN_INLINE"] = "1"

import anthropic  # noqa: E402
import app  # noqa: E402

client = app.app.test_client()
ADMIN = {"Authorization": "Bearer admin-test-token"}
BETA = {"Authorization": "Bearer beta-test-token"}
calls = app.anthropic_client.messages.calls
script = app.anthropic_client.messages.script


def _text(text="ok"):
    return anthropic.Message(content=[anthropic.ContentBlock(type="text", text=text)],
                             stop_reason="end_turn", usage=anthropic.Usage(input_tokens=5, output_tokens=5))


def _notes():
    return [n["note"] for n in app.recall_notes(limit=200)["notes"]]


def demo():
    today = time.strftime("%Y-%m-%d")

    # Folder layout exists from startup.
    for sub in (("chat logs", "dashboard"), ("chat logs", "discord"), ("knowledge",)):
        assert os.path.isdir(os.path.join(DATA_DIR, *sub)), sub
    mirror = os.path.join(DATA_DIR, "knowledge", "memory-notes.md")
    assert os.path.isfile(mirror) and "0 note(s)" in open(mirror, encoding="utf-8").read()

    # Deep: deep model, bigger caps, full tools, wins over lite, echoed back.
    assert app.DEEP_MODEL in app.LLM_PRICING_PER_MTOK and app.DEEP_MODEL != app.LLM_MODEL
    script.append(_text())
    r = client.post("/api/chat", json={"message": "think hard", "history": [], "deep": True, "lite": True}, headers=ADMIN)
    assert r.status_code == 200, r.get_json()
    assert r.get_json()["deep"] is True and r.get_json()["lite"] is False, r.get_json()
    sent = calls[-1]
    assert sent["model"] == app.DEEP_MODEL and sent["max_tokens"] == app.DEEP_MAX_TOKENS, (sent["model"], sent["max_tokens"])
    assert len(sent["tools"]) == len(app.TOOLS)

    # Beta: the deep flag is ignored -- normal model, and no learning either.
    before = len(calls)
    script.append(_text())
    r = client.post("/api/chat", json={"message": "hi", "history": [], "deep": True, "learn": True}, headers=BETA)
    assert r.status_code == 200 and r.get_json()["deep"] is False and r.get_json()["learning"] is False, r.get_json()
    assert calls[-1]["model"] == app.LLM_MODEL
    assert len(calls) - before == 1, "beta must not trigger the learner call"

    # Learn: main reply, then ONE learner call on the lite model; the fact is saved once.
    script.append(_text("Noted — the Jellyfin box is on the D drive."))
    script.append(_text("The owner keeps the Jellyfin media library on the D drive."))
    before = len(calls)
    r = client.post("/api/chat", json={"message": "fyi my jellyfin media lives on the D drive", "history": [], "learn": True}, headers=ADMIN)
    assert r.status_code == 200 and r.get_json()["learning"] is True, r.get_json()
    assert len(calls) - before == 2, len(calls) - before
    learner = calls[-1]
    assert learner["model"] == app.LEARN_MODEL and learner["max_tokens"] == app.LEARN_MAX_TOKENS
    assert learner["system"][0]["text"] == app.LEARN_PROMPT and "tools" not in learner
    assert "D drive" in learner["messages"][0]["content"]
    assert _notes() == ["The owner keeps the Jellyfin media library on the D drive."], _notes()
    learned_events = [e for e in app.get_recent_activity(limit=20)["events"] if e["event_type"] == "learned"]
    assert len(learned_events) == 1 and "Jellyfin" in learned_events[0]["summary"]

    # NONE -> nothing saved; duplicate -> nothing saved.
    script.append(_text()); script.append(_text("NONE"))
    client.post("/api/chat", json={"message": "thanks", "history": [], "learn": True}, headers=ADMIN)
    assert len(_notes()) == 1
    script.append(_text()); script.append(_text("The owner keeps the Jellyfin media library on the D drive."))
    client.post("/api/chat", json={"message": "again: jellyfin is on D", "history": [], "learn": True}, headers=ADMIN)
    assert len(_notes()) == 1, _notes()

    # Learn off -> no learner call at all.
    before = len(calls)
    script.append(_text())
    client.post("/api/chat", json={"message": "plain", "history": []}, headers=ADMIN)
    assert len(calls) - before == 1

    # Odin remembered something himself this turn -> the learner stays
    # quiet (it would only paraphrase what he just saved).
    script.append(anthropic.Message(
        content=[anthropic.ContentBlock(type="tool_use", id="toolu_rm", name="remember_note",
                                        input={"note": "The owner's router is a UniFi Dream Machine."})],
        stop_reason="tool_use", usage=anthropic.Usage(input_tokens=5, output_tokens=5)))
    script.append(_text("Filed."))
    before = len(calls)
    r = client.post("/api/chat", json={"message": "my router is a UniFi Dream Machine", "history": [], "learn": True}, headers=ADMIN)
    assert r.get_json()["tools_used"] == ["remember_note"], r.get_json()
    assert len(calls) - before == 2, "main call + tool round only; no learner call"
    assert len(_notes()) == 2 and any("UniFi" in n for n in _notes()), _notes()

    # Knowledge mirror reflects the notebook: the one-page view, one linked
    # page per note (with a wikilink where the DB has an edge), an index.
    body = open(mirror, encoding="utf-8").read()
    assert "2 note(s)" in body and "Jellyfin media library" in body and "UniFi" in body, body
    app.remember_note(note="The Jellyfin media library backup also goes to the D drive weekly")  # shares words -> edge
    notes_dir = os.path.join(DATA_DIR, "knowledge", "notes")
    files = sorted(f for f in os.listdir(notes_dir) if f.startswith("note-"))
    assert len(files) == 3, files
    pages = {f: open(os.path.join(notes_dir, f), encoding="utf-8").read() for f in files}
    newest = pages[files[-1]]
    assert newest.startswith("---\ncreated: ") and "\n# The Jellyfin media library backup" in newest, newest[:200]
    assert "[[note-" in newest, "the related note should appear as a wikilink:\n" + newest
    index = open(os.path.join(DATA_DIR, "knowledge", "Memory index.md"), encoding="utf-8").read()
    assert "3 note(s)" in index and "[[notes/note-" in index, index
    # Trimmed notes lose their page: fake a trim by deleting a row.
    conn = app._get_db_connection()
    conn.execute("DELETE FROM memory_notes WHERE note LIKE 'The owner''s router%'"); conn.commit(); conn.close()
    app._write_knowledge_mirror()
    assert not any("UniFi" in open(os.path.join(notes_dir, f), encoding="utf-8").read()
                   for f in os.listdir(notes_dir) if f.startswith("note-")), "page for a trimmed note must be removed"

    # Chat logs split by source, as Markdown with one heading per exchange.
    dash = os.path.join(DATA_DIR, "chat logs", "dashboard", today + ".md")
    disc = os.path.join(DATA_DIR, "chat logs", "discord", today + ".md")
    d_text = open(dash, encoding="utf-8").read()
    assert d_text.startswith("# Dashboard chat — " + today), d_text[:60]
    assert "] admin asked: fyi my jellyfin media lives on the D drive" in d_text, d_text
    assert not os.path.exists(disc)
    script.append(_text("hello from the bot"))
    client.post("/api/chat", json={"message": "ping from discord", "history": [], "speaker": "discord:somebody"}, headers=ADMIN)
    assert os.path.isfile(disc), "a discord:* speaker must land in chat logs/discord"
    d_body = open(disc, encoding="utf-8").read()
    assert d_body.startswith("# Discord chat — ") and "] discord:somebody asked: ping from discord" in d_body, d_body
    assert "ping from discord" not in open(dash, encoding="utf-8").read(), "discord turns must not leak into the dashboard log"

    # Brain graph: absent -> honest "not yet"; present -> conversations
    # retrieved by the words in their headings, and surfaced in the
    # situational context as past conversations.
    r = app.recall_from_brain(query="jellyfin drive")
    assert r["available"] is False and r["hits"] == [] and "graphify" in r["error"], r
    gdir = os.path.join(DATA_DIR, "graphify-out")
    os.makedirs(gdir, exist_ok=True)
    import json as _json
    _json.dump({"nodes": [
        {"id": "f1", "label": today + ".md", "node_kind": "file", "source_file": "chat logs/dashboard/" + today + ".md"},
        {"id": "h1", "label": "[16:58] admin asked: fyi my jellyfin media lives on the D drive", "node_kind": "heading",
         "source_file": "chat logs/dashboard/" + today + ".md", "community_name": "Dashboard chat"},
        {"id": "k1", "label": "The owner keeps the Jellyfin media library on the D drive", "node_kind": "heading",
         "source_file": "knowledge/notes/note-1.md", "tags": ["visibility:public"]},
        {"id": "h9", "label": "[09:00] admin asked: how hot is the cpu", "node_kind": "heading",
         "source_file": "chat logs/dashboard/2026-09-10.md"},
    ], "links": [{"source": "f1", "target": "h1", "relation": "contains"}]},
        open(os.path.join(gdir, "graph.json"), "w", encoding="utf-8"))
    r = app.recall_from_brain(query="where does my jellyfin media live?")
    assert r["available"] and r["hit_count"] >= 2, r
    kinds = {h["source"]: h["kind"] for h in r["hits"]}
    assert kinds["chat logs/dashboard/" + today + ".md"] == "conversation" and kinds["knowledge/notes/note-1.md"] == "knowledge", kinds
    assert not any(h["label"] == today + ".md" for h in r["hits"]), "bare file nodes must be filtered out"
    assert not any("cpu" in h["label"] for h in r["hits"]), "unrelated conversation must not match"
    ctx = app._situational_context("where does my jellyfin media live?")
    assert "From your own past conversations" in ctx and "jellyfin media lives on the D drive" in ctx, ctx
    assert "recall_from_brain" in app.TOOL_DISPATCH and "recall_from_brain" in app.LITE_ALLOWED_TOOLS

    print("OK: deep mode uses %s with max_tokens=%d and wins over lite, beta gets neither deep nor learning; "
          "learning runs one %s call, saves a new fact once (activity logged), skips NONE/duplicates; "
          "chat logs split into dashboard/ and discord/ dated files; knowledge/memory-notes.md mirrors the notebook."
          % (app.DEEP_MODEL, app.DEEP_MAX_TOKENS, app.LEARN_MODEL))


if __name__ == "__main__":
    demo()
