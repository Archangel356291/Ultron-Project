"""Self-check for GET /api/brain-graph -- the Brain vault drawn under Odin's
corner ("What Odin knows", owner-requested 2026-09-16).

Proves the things the panel depends on: a memory note's page and heading fold
into one node named by the note's own words (not "note-7.md"), conversations
are counted per exchange and dated from the log's file name, the counts stay
whole when the picture is thinned past the node cap, a missing graph is an
honest empty state rather than an error, and only the admin can read it --
these headings carry the owner's words.

Run standalone from anywhere:
    python dev-tools/test_brain_graph.py
"""
import json
import os
import sys
import tempfile

BACKEND_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "odin-backend")
FAKE_PKGS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fake_pkgs")
sys.path.insert(0, FAKE_PKGS_DIR)
sys.path.insert(0, BACKEND_DIR)

DATA_DIR = tempfile.mkdtemp()
os.environ["ODIN_API_TOKEN"] = "admin-test-token"
os.environ["ODIN_BETA_TOKENS"] = "tester:beta-test-token"
os.environ["ODIN_DB_PATH"] = os.path.join(DATA_DIR, "test_odin.db")
os.environ["ODIN_DISABLE_MEMORY_TRENDS"] = "1"
os.environ["ODIN_DISABLE_METRICS_HISTORY"] = "1"

import app  # noqa: E402

client = app.app.test_client()
ADMIN = {"Authorization": "Bearer admin-test-token"}
BETA = {"Authorization": "Bearer beta-test-token"}


def write_graph(nodes, links):
    os.makedirs(os.path.dirname(app.BRAIN_GRAPH_PATH), exist_ok=True)
    with open(app.BRAIN_GRAPH_PATH, "w", encoding="utf-8") as f:
        json.dump({"nodes": nodes, "links": links}, f)
    app._brain_graph_cache.update(mtime=None)   # same-second rewrites share an mtime


def page(i, src):
    return {"id": i, "label": src.rsplit("/", 1)[-1], "node_kind": "page", "source_file": src}


def heading(i, label, src):
    return {"id": i, "label": label, "node_kind": "heading", "source_file": src}


def demo():
    # No graph yet: an empty picture with a hint, not a 500.
    res = client.get("/api/brain-graph", headers=ADMIN)
    assert res.status_code == 200, res.status_code
    body = res.get_json()
    assert body["available"] is False and body["nodes"] == [] and "hint" in body, body

    # Admin only.
    assert client.get("/api/brain-graph").status_code == 401
    assert client.get("/api/brain-graph", headers=BETA).status_code == 403

    chat = "chat logs/dashboard/2026-09-16.md"
    write_graph(
        [page("note7", "knowledge/notes/note-7.md"), heading("note7_h", "Jellyfin lives on the D drive", "knowledge/notes/note-7.md"),
         page("note8", "knowledge/notes/note-8.md"), heading("note8_h", "Prefers short answers", "knowledge/notes/note-8.md"),
         page("chat", chat), heading("chat_1", "how hot is the GPU", chat), heading("chat_2", "restart pihole", chat),
         page("home", "Home.md")],
        [{"source": "note7", "target": "note7_h", "relation": "contains"},
         {"source": "note8", "target": "note8_h", "relation": "contains"},
         {"source": "note7", "target": "note8", "relation": "references"},
         {"source": "chat", "target": "chat_1", "relation": "contains"},
         {"source": "chat", "target": "chat_2", "relation": "contains"},
         {"source": "home", "target": "note7", "relation": "references"}],
    )
    body = client.get("/api/brain-graph", headers=ADMIN).get_json()
    by_id = {n["id"]: n for n in body["nodes"]}
    assert body["available"] is True
    assert "note7_h" not in by_id and "note8_h" not in by_id, "memory headings fold into their page"
    assert by_id["note7"]["label"] == "Jellyfin lives on the D drive" and by_id["note7"]["kind"] == "memory", by_id["note7"]
    assert by_id["chat"]["label"] == "Dashboard chat, 2026-09-16", by_id["chat"]
    assert by_id["chat_1"]["kind"] == "conversation" and by_id["chat_1"]["page"] is False
    assert by_id["home"]["label"] == "Home" and by_id["home"]["kind"] == "knowledge"
    ids = set(by_id)
    assert all(e["source"] in ids and e["target"] in ids and e["source"] != e["target"] for e in body["links"]), body["links"]
    s = body["stats"]
    assert (s["conversations"], s["memories"], s["knowledge"], s["nodes"], s["shown"], s["links"]) == (2, 2, 1, 6, 6, 4), s
    assert body["by_day"] == [{"date": "2026-09-16", "conversations": 2, "memories": 0}], body["by_day"]

    # A remembered note shows up in the per-day count from the DB.
    assert "error" not in app.remember_note(note="test memory for the by-day strip")
    today = [d for d in client.get("/api/brain-graph", headers=ADMIN).get_json()["by_day"] if d["memories"]]
    assert len(today) == 1 and today[0]["memories"] == 1, today

    # Past the cap the picture is thinned -- pages first, then the best
    # connected -- but the counts still describe the whole vault.
    cap = app.BRAIN_GRAPH_MAX_NODES
    nodes = [page("chat", chat)] + [heading(f"h{i}", f"exchange {i}", chat) for i in range(cap + 50)]
    write_graph(nodes, [{"source": "chat", "target": f"h{i}", "relation": "contains"} for i in range(cap + 50)])
    body = client.get("/api/brain-graph", headers=ADMIN).get_json()
    assert len(body["nodes"]) == cap and body["stats"]["shown"] == cap, len(body["nodes"])
    assert body["stats"]["nodes"] == cap + 51 and body["stats"]["conversations"] == cap + 50, body["stats"]
    assert any(n["id"] == "chat" for n in body["nodes"]), "pages survive the thinning"
    kept = {n["id"] for n in body["nodes"]}
    assert all(e["source"] in kept and e["target"] in kept for e in body["links"])

    print("OK: /api/brain-graph is admin-only, empty-but-honest with no graph, folds each memory note into one "
          "node named by its own words, names chat logs by where and when, counts and dates what was learned, "
          "and thins the picture past %d nodes without shrinking the counts." % cap)


if __name__ == "__main__":
    demo()
