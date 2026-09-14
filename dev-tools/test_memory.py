"""Self-check for Ultron's memory-notes feature (remember_note / recall_notes).

Proves the actual mechanisms, not just that the functions exist: real SQLite
via a temp DB, the per-note length cap, the row-count cap (oldest trimmed
first), substring search, and that the memory tools are admin-only (absent
from BETA_ALLOWED_TOOLS, the same gate every other admin-only tool uses).

Run standalone from anywhere:
    python dev-tools/test_memory.py
"""
import os
import sys
import tempfile

BACKEND_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "ultron-backend")
FAKE_PKGS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fake_pkgs")
sys.path.insert(0, FAKE_PKGS_DIR)   # 'import anthropic' inside app.py resolves to the fake
sys.path.insert(0, BACKEND_DIR)

os.environ["ULTRON_API_TOKEN"] = "admin-test-token"
os.environ["ULTRON_DB_PATH"] = os.path.join(tempfile.mkdtemp(), "test_ultron.db")
os.environ["ULTRON_DISABLE_MEMORY_TRENDS"] = "1"  # deterministic note counts below

import app  # noqa: E402


def demo():
    # Basic save + recall.
    r = app.remember_note(note="owner prefers FIFO trade summaries")
    assert r == {"saved": "owner prefers FIFO trade summaries", "truncated": False}, r
    notes = app.recall_notes()["notes"]
    assert len(notes) == 1 and notes[0]["note"] == "owner prefers FIFO trade summaries", notes

    # Empty note is rejected.
    r = app.remember_note(note="   ")
    assert "error" in r, r

    # Per-note length cap truncates rather than silently accepting megabytes.
    long_note = "x" * (app.MEMORY_NOTE_MAX_CHARS + 50)
    r = app.remember_note(note=long_note)
    assert r["truncated"] is True and len(r["saved"]) == app.MEMORY_NOTE_MAX_CHARS, r

    # Search filters by substring.
    app.remember_note(note="the Pi lives at ultron-pi on the tailnet")
    hits = app.recall_notes(query="tailnet")["notes"]
    assert len(hits) == 1 and "tailnet" in hits[0]["note"], hits

    # Row-count cap: fill past MEMORY_NOTES_MAX_ROWS and confirm only the
    # most recent rows survive (oldest trimmed first).
    for i in range(app.MEMORY_NOTES_MAX_ROWS + 10):
        app.remember_note(note=f"filler note {i}")
    all_notes = app.recall_notes(limit=app.MEMORY_NOTES_MAX_ROWS)["notes"]
    assert len(all_notes) == app.MEMORY_NOTES_MAX_ROWS, len(all_notes)
    assert "filler note 0" not in [n["note"] for n in all_notes]  # oldest, trimmed
    newest = f"filler note {app.MEMORY_NOTES_MAX_ROWS + 9}"
    assert all_notes[0]["note"] == newest, all_notes[0]

    # Admin-only: memory tools must not be reachable by the beta role.
    assert "remember_note" not in app.BETA_ALLOWED_TOOLS
    assert "recall_notes" not in app.BETA_ALLOWED_TOOLS
    assert "remember_note" in app.TOOL_DISPATCH and "recall_notes" in app.TOOL_DISPATCH

    # The dashboard's brain panel reads memory through the REST endpoint,
    # not the chat tool directly — prove that route actually works too.
    client = app.app.test_client()
    res = client.get("/api/memory?limit=3", headers={"Authorization": "Bearer admin-test-token"})
    assert res.status_code == 200, res.get_json()
    body = res.get_json()
    assert len(body["notes"]) == 3, body
    assert body["notes"][0]["note"] == newest, body

    # No token at all -> unauthorized, same as every other admin-only route.
    res = client.get("/api/memory")
    assert res.status_code == 401, res.get_json()

    print("OK: remember_note/recall_notes save, truncate, search, cap row count, "
          "stay admin-only, and GET /api/memory serves the same data.")


def demo_trend_distillation():
    # Start from a clean slate — demo() above already saturated memory_notes
    # to MEMORY_NOTES_MAX_ROWS, and count-based assertions below need real
    # headroom rather than a table permanently pinned at the cap.
    conn = app._get_db_connection()
    conn.execute("DELETE FROM memory_notes")
    conn.execute("DELETE FROM activity_log")
    conn.commit()
    conn.close()

    # A one-off event (below MEMORY_TREND_MIN_COUNT) shouldn't produce a note.
    app.log_activity("backup", "backup ran")
    app.log_activity("backup", "backup ran")
    before = len(app.recall_notes(limit=app.MEMORY_NOTES_MAX_ROWS)["notes"])
    app.distill_activity_trends()
    after = len(app.recall_notes(limit=app.MEMORY_NOTES_MAX_ROWS)["notes"])
    assert after == before, "a below-threshold event type must not produce a memory note"

    # Push "backup" over MEMORY_TREND_MIN_COUNT — now it's a real pattern.
    for _ in range(app.MEMORY_TREND_MIN_COUNT):
        app.log_activity("backup", "backup ran")
    app.distill_activity_trends()
    notes = app.recall_notes(limit=1)["notes"]
    assert notes and "backup" in notes[0]["note"] and "Recurring activity" in notes[0]["note"], notes

    # A second call with no new activity_log rows must NOT duplicate the
    # note — this runs on every process start, not just once a day, and a
    # container restarted repeatedly shouldn't spam identical notes.
    count_before = len(app.recall_notes(limit=app.MEMORY_NOTES_MAX_ROWS)["notes"])
    app.distill_activity_trends()
    count_after = len(app.recall_notes(limit=app.MEMORY_NOTES_MAX_ROWS)["notes"])
    assert count_after == count_before, "identical consecutive distillations must be deduped"

    # But once the picture actually changes (a new event type crosses the
    # threshold too), a fresh note IS saved — dedup isn't a one-note-ever cap.
    for _ in range(app.MEMORY_TREND_MIN_COUNT):
        app.log_activity("cve_scan", "scan ran")
    app.distill_activity_trends()
    count_final = len(app.recall_notes(limit=app.MEMORY_NOTES_MAX_ROWS)["notes"])
    assert count_final == count_before + 1, "a genuinely changed summary must still get saved"
    newest_note = app.recall_notes(limit=1)["notes"][0]["note"]
    assert "cve_scan" in newest_note and "backup" in newest_note, newest_note

    print("OK: distill_activity_trends ignores one-offs, summarizes real recurrence, dedups "
          "identical reruns, still saves genuine changes, and its background scheduler stayed "
          "off (ULTRON_DISABLE_MEMORY_TRENDS=1).")


if __name__ == "__main__":
    demo()
    demo_trend_distillation()
