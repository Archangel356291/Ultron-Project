"""Module 10 self-check: runtime knowledge graph on top of memory_notes.

Proves the actual reused mechanisms behave correctly against real SQLite,
not just that the functions exist:
- classify_visibility/derive_tags (reused from Module 4) correctly tag a
  saved note private/public and stamp its category/tags/visibility columns.
- retrieve() (reused from Module 8) is used BOTH to auto-link a new note to
  existing related notes (memory_edges) AND to answer recall_related_notes
  queries, including a real one-hop case: a note reached only via an edge,
  not via any literal word it shares with the query.
- memory_edges never accumulates dangling rows after memory_notes trims old
  rows (no FK cascade in SQLite -- this must be explicit).

Run standalone from anywhere:
    python dev-tools/test_runtime_graph.py
"""
import json
import os
import sys
import tempfile

BACKEND_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "ultron-backend")
FAKE_PKGS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fake_pkgs")
sys.path.insert(0, FAKE_PKGS_DIR)   # 'import anthropic' inside app.py resolves to the fake
sys.path.insert(0, BACKEND_DIR)

os.environ["ULTRON_API_TOKEN"] = "admin-test-token"
os.environ["ULTRON_DB_PATH"] = os.path.join(tempfile.mkdtemp(), "test_ultron.db")
os.environ["ULTRON_DISABLE_MEMORY_TRENDS"] = "1"

import app  # noqa: E402


def _note_row(note_text):
    conn = app._get_db_connection()
    try:
        row = conn.execute(
            "SELECT id, category, tags, visibility FROM memory_notes WHERE note = ?",
            (note_text,),
        ).fetchone()
    finally:
        conn.close()
    return dict(row) if row else None


def demo_classification():
    app.remember_note(note="wireguard config lives in etc wireguard")
    row = _note_row("wireguard config lives in etc wireguard")
    assert row["visibility"] == "private", row
    assert row["category"] == "concept", row
    assert "visibility:private" in json.loads(row["tags"]), row

    app.remember_note(note="prefers dark mode on dashboard")
    row2 = _note_row("prefers dark mode on dashboard")
    assert row2["visibility"] == "public", row2
    assert "visibility:public" in json.loads(row2["tags"]), row2

    print("OK: remember_note reuses Module 4's classify_visibility/derive_tags -- a private "
          "keyword triggers visibility:private, an ordinary note stays visibility:public.")


def demo_edge_creation_and_one_hop_recall():
    app.remember_note(note="plex server runs on pi5 in closet")
    app.remember_note(note="update plex server monthly")
    app.remember_note(note="renewed car insurance today")  # unrelated -- must NOT get an edge
    app.remember_note(note="monthly maintenance reminder")

    n1 = _note_row("plex server runs on pi5 in closet")
    n2 = _note_row("update plex server monthly")
    n3 = _note_row("renewed car insurance today")
    n4 = _note_row("monthly maintenance reminder")

    conn = app._get_db_connection()
    try:
        edges = conn.execute(
            "SELECT source_note_id, target_note_id, relation FROM memory_edges"
        ).fetchall()
    finally:
        conn.close()
    edge_pairs = {(e["source_note_id"], e["target_note_id"]) for e in edges}

    # Real match: note2 shares "plex"/"server" with note1.
    assert (n2["id"], n1["id"]) in edge_pairs, edge_pairs
    # Real match: note4 shares "monthly" with note2.
    assert (n4["id"], n2["id"]) in edge_pairs, edge_pairs
    # Real negative: note3 shares nothing with anything -- must not appear as
    # either side of any edge.
    assert not any(n3["id"] in pair for pair in edge_pairs), edge_pairs
    assert all(e["relation"] == "relates_to" for e in edges), edges

    # One-hop proof: "reminder" appears only in note4's text, not note2's
    # ("remember" != "reminder") -- note2 must still surface, reached only
    # via the note4->note2 edge, not via any literal shared word with the
    # query. note1 is two hops away and must NOT appear (one hop only).
    result = app.recall_related_notes(query="reminder", min_nodes=1)
    notes_by_text = {n["note"]: n["relation"] for n in result["notes"]}
    assert notes_by_text.get("monthly maintenance reminder") == "seed", notes_by_text
    assert notes_by_text.get("update plex server monthly") == "linked", notes_by_text
    assert "plex server runs on pi5 in closet" not in notes_by_text, notes_by_text

    print("OK: saving a note auto-links it to genuinely related existing notes (and NOT to an "
          "unrelated one), and recall_related_notes surfaces a note reached only via that edge, "
          "not just via shared words with the query -- while staying one hop, not two.")


def demo_recall_related_notes_validation():
    r = app.recall_related_notes(query="")
    assert "error" in r, r
    r2 = app.recall_related_notes()
    assert "error" in r2, r2
    print("OK: recall_related_notes rejects an empty/missing query instead of returning garbage.")


def demo_admin_only_and_no_dangling_edges():
    assert "recall_related_notes" not in app.BETA_ALLOWED_TOOLS
    assert "recall_related_notes" in app.TOOL_DISPATCH

    # Push memory_notes past its row cap and confirm memory_edges was
    # trimmed alongside it -- SQLite has no FK cascade, this must be
    # explicit (see remember_note's cleanup DELETE).
    for i in range(app.MEMORY_NOTES_MAX_ROWS + 20):
        app.remember_note(note=f"filler note about topic {i}")
    conn = app._get_db_connection()
    try:
        live_ids = {r["id"] for r in conn.execute("SELECT id FROM memory_notes")}
        edge_rows = conn.execute(
            "SELECT source_note_id, target_note_id FROM memory_edges"
        ).fetchall()
    finally:
        conn.close()
    for e in edge_rows:
        assert e["source_note_id"] in live_ids, (e["source_note_id"], "dangling edge source")
        assert e["target_note_id"] in live_ids, (e["target_note_id"], "dangling edge target")

    print("OK: recall_related_notes stays admin-only, and memory_edges has zero dangling rows "
          "after memory_notes trims past its row cap.")


if __name__ == "__main__":
    demo_classification()
    demo_edge_creation_and_one_hop_recall()
    demo_recall_related_notes_validation()
    demo_admin_only_and_no_dangling_edges()
    print("All Module 10 checks passed.")
