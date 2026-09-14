"""Module 7's write path: drafts a session-summary graph node from real
git history -- never appends directly. Step 29 is explicit that, for at
least the first 10-20 uses, a human has to review the draft before it
enters the graph, since an unreviewed, possibly-hallucinated summary
would quietly mislead every future session that reads it back. This
script only ever writes session-write/pending-review.json; nothing
touches graphify-out/graph.json until approve_session_summary.py runs,
which is a separate, deliberate step.

"Capture what changed, decisions made, why" (step 28) is read straight
from git commit messages, not regenerated/guessed -- this project's own
commit messages already carry that detail (every commit tonight
explains what changed and why, not just what), so compressing them is
literal text processing, not an LLM re-summarizing from scratch and
risking drift from what actually happened.

Usage:
    python session-write/summarize_session.py                  # since the last approved summary
    python session-write/summarize_session.py --since <ref>     # since a specific commit/tag
    python session-write/summarize_session.py --since <ref> --label "Custom label"
"""
import argparse
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "graph-schema"))
from enrich_visibility import classify_visibility, derive_tags  # noqa: E402

STATE_PATH = ROOT / "session-write" / ".last_summarized_commit"
PENDING_PATH = ROOT / "session-write" / "pending-review.json"
GRAPH_PATH = ROOT / "graphify-out" / "graph.json"

# Commits that are pure mechanical byproducts of other commits in the
# same range (graphify's own auto-refresh, merge commits) -- compressing
# these out is compressing redundancy, not substance: their content is
# fully covered by the real commit they follow.
_NOISE_PATTERNS = (
    re.compile(r"^Refresh graphify", re.I),
    re.compile(r"^Merge module-", re.I),
)


def _run_git(*args, cwd=ROOT):
    result = subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True, check=True)
    return result.stdout


def _is_noise(subject):
    return any(p.match(subject) for p in _NOISE_PATTERNS)


def collect_commits(since_ref, cwd=ROOT):
    log = _run_git("log", "--no-merges", f"{since_ref}..HEAD", "--pretty=format:%H%x1f%s%x1f%b%x1e", cwd=cwd)
    commits = []
    for entry in filter(None, log.split("\x1e")):
        parts = entry.strip("\n").split("\x1f")
        if len(parts) < 2:
            continue
        commit_hash, subject = parts[0].strip(), parts[1]
        body = parts[2] if len(parts) > 2 else ""
        if _is_noise(subject):
            continue
        files = _run_git("diff-tree", "--no-commit-id", "--name-only", "-r", commit_hash, cwd=cwd).splitlines()
        commits.append({"hash": commit_hash, "subject": subject, "body": body.strip(), "files": files})
    return commits


def find_related_nodes(commits, graph_nodes):
    """Real, factual edges (EXTRACTED, not INFERRED) -- 'this session's
    commits touched this file' is read directly from git diff output,
    not guessed."""
    by_source_file = {}
    for n in graph_nodes:
        sf = n.get("source_file")
        if sf:
            by_source_file.setdefault(sf, n["id"])
    touched = {f for c in commits for f in c["files"]}
    return sorted({by_source_file[f] for f in touched if f in by_source_file})


def compress(commits):
    """Compress redundancy, never substance (step 28) -- keeps every
    commit's own subject + body verbatim (that IS the substance: what
    changed and why, already written by whoever/whatever made the
    commit), just strips the mechanical noise commits and formats it as
    one readable block instead of N separate ones."""
    lines = []
    for c in commits:
        lines.append(f"- {c['subject']}")
        if c["body"]:
            indented = "\n".join("  " + line for line in c["body"].splitlines() if line.strip())
            lines.append(indented)
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--since", help="Git ref to summarize from (default: last approved summary, or asks if none recorded)")
    parser.add_argument("--label", help="Short label for the session node (default: derived from the date + commit count)")
    args = parser.parse_args()

    since_ref = args.since
    if not since_ref:
        if STATE_PATH.exists():
            since_ref = STATE_PATH.read_text(encoding="utf-8").strip()
        else:
            print("[summarize_session] no prior summary recorded and no --since given -- "
                  "pass --since <commit-or-tag> for the first run.", file=sys.stderr)
            sys.exit(1)

    commits = collect_commits(since_ref)
    if not commits:
        print(f"[summarize_session] no substantive commits since {since_ref[:12]} -- nothing to draft.")
        return

    graph = json.loads(GRAPH_PATH.read_text(encoding="utf-8"))
    related = find_related_nodes(commits, graph["nodes"])
    summary_text = compress(commits)

    now = datetime.now(timezone.utc)
    date_str = now.strftime("%Y_%m_%d")
    node_id = f"session_{date_str}_{commits[-1]['hash'][:8]}"
    label = args.label or f"Session {now.strftime('%Y-%m-%d')} ({len(commits)} commit(s))"

    draft_node = {
        "id": node_id,
        "label": label,
        "file_type": "rationale",
        "category": "rationale",
        "source_commits": [c["hash"] for c in commits],
        "summary": summary_text,
        "date_created": now.isoformat(),
        "date_updated": now.isoformat(),
    }
    visibility = classify_visibility(draft_node)
    tags = derive_tags(draft_node, visibility) + ["session-summary"]
    draft_node["visibility"] = visibility
    draft_node["tags"] = tags

    draft_edges = [
        {
            "source": node_id, "target": target_id, "relation": "documents",
            "confidence": "EXTRACTED", "confidence_score": 1.0,
            "source_file": None, "source_location": None, "weight": 1.0,
        }
        for target_id in related
    ]

    pending = {
        "node": draft_node,
        "edges": draft_edges,
        "since_ref": since_ref,
        "end_ref": commits[0]["hash"],
        "drafted_at": now.isoformat(),
    }
    PENDING_PATH.write_text(json.dumps(pending, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"[summarize_session] drafted '{label}' from {len(commits)} commit(s) "
          f"({visibility}, {len(related)} linked node(s)) -> {PENDING_PATH}")
    print(f"[summarize_session] review it, then run: python session-write/approve_session_summary.py")


if __name__ == "__main__":
    main()
