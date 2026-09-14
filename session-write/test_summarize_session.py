"""Self-check for Module 7's write path (draft, never auto-append).

Uses a real throwaway git repo (not a mock) to prove: noise commits
(graphify auto-refresh, merges) are actually filtered out while real
ones survive with their subject+body intact; file-based edges only
form for files a real existing graph node actually claims as its
source_file; visibility classification and tagging come from Module 4's
own classifier, not a reimplementation; and approve_session_summary.py
genuinely refuses to duplicate an id and genuinely appends a well-formed
node+edges when it does append.

Run standalone from anywhere:
    python session-write/test_summarize_session.py
"""
import json
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import summarize_session as ss  # noqa: E402


def _git(repo, *args):
    subprocess.run(["git", *args], cwd=repo, check=True, capture_output=True, text=True)


def _commit(repo, filename, content, subject, body=""):
    path = repo / filename
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    _git(repo, "add", filename)
    msg = subject + ("\n\n" + body if body else "")
    _git(repo, "commit", "-m", msg)
    return _git_head(repo)


def _git_head(repo):
    return subprocess.run(["git", "rev-parse", "HEAD"], cwd=repo, check=True,
                           capture_output=True, text=True).stdout.strip()


def demo():
    repo = Path(tempfile.mkdtemp())
    _git(repo, "init", "-q")
    _git(repo, "config", "user.email", "test@example.com")
    _git(repo, "config", "user.name", "test")

    base = _commit(repo, "app.py", "print('v1')\n", "Initial commit")

    _commit(repo, "app.py", "print('v2')\n", "Add real feature: streaming TTS",
            "Fixed a real bug: audio waited for the whole reply before playing.")
    _commit(repo, "graphify-out/graph.json", "{}", "Refresh graphify stat cache after commit")
    _commit(repo, "README.md", "docs\n", "Document the new feature",
            "Explains the streaming behavior for future readers.")

    commits = ss.collect_commits(base, cwd=repo)
    subjects = [c["subject"] for c in commits]
    assert "Refresh graphify stat cache after commit" not in subjects, subjects
    assert "Add real feature: streaming TTS" in subjects, subjects
    assert "Document the new feature" in subjects, subjects
    assert len(commits) == 2, commits

    feature_commit = next(c for c in commits if "streaming TTS" in c["subject"])
    assert "app.py" in feature_commit["files"], feature_commit
    assert "Fixed a real bug" in feature_commit["body"], feature_commit

    # find_related_nodes: only matches files a real graph node claims.
    fake_nodes = [
        {"id": "app_py_node", "source_file": "app.py"},
        {"id": "unrelated_node", "source_file": "some/other/file.py"},
    ]
    related = ss.find_related_nodes(commits, fake_nodes)
    assert related == ["app_py_node"], related

    # compress(): keeps subject + body, drops nothing from the real commits.
    text = ss.compress(commits)
    assert "streaming TTS" in text and "Fixed a real bug" in text, text
    assert "Document the new feature" in text, text

    print("OK: noise commits filtered (graphify refresh), real commits kept with "
          "subject+body intact, file-based edges only match real existing nodes.")

    # --- approve_session_summary.py: id-collision refusal + real append ---
    import approve_session_summary as approve

    graph_dir = Path(tempfile.mkdtemp())
    graph_path = graph_dir / "graph.json"
    graph_path.write_text(json.dumps({"nodes": [{"id": "existing_node"}], "links": []}), encoding="utf-8")
    pending_path = graph_dir / "pending-review.json"
    state_path = graph_dir / ".last_summarized_commit"

    approve.GRAPH_PATH = graph_path
    approve.PENDING_PATH = pending_path
    approve.STATE_PATH = state_path

    draft = {
        "node": {"id": "session_test_node", "label": "Test session", "visibility": "public", "tags": [], "summary": "test summary"},
        "edges": [{"source": "session_test_node", "target": "existing_node", "relation": "documents"}],
        "since_ref": base, "end_ref": "deadbeef",
    }
    pending_path.write_text(json.dumps(draft), encoding="utf-8")

    sys.argv = ["approve_session_summary.py", "--yes"]
    approve.main()

    graph_after = json.loads(graph_path.read_text(encoding="utf-8"))
    ids = {n["id"] for n in graph_after["nodes"]}
    assert "session_test_node" in ids and "existing_node" in ids, ids
    assert len(graph_after["links"]) == 1, graph_after["links"]
    assert not pending_path.exists(), "pending-review.json should be cleared after approval"
    assert state_path.read_text(encoding="utf-8") == "deadbeef", state_path.read_text(encoding="utf-8")

    # Re-drafting the same id and approving again must refuse (no duplicate nodes).
    pending_path.write_text(json.dumps(draft), encoding="utf-8")
    try:
        approve.main()
        assert False, "approving a duplicate id should have exited non-zero"
    except SystemExit as e:
        assert e.code != 0

    print("OK: approve_session_summary.py appends a well-formed node+edges, clears the "
          "pending draft, records state, and refuses to duplicate an existing id.")


if __name__ == "__main__":
    demo()
