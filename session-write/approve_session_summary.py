"""Second half of Module 7's write path: appends a REVIEWED draft
(session-write/pending-review.json, produced by summarize_session.py)
into graphify-out/graph.json. Deliberately a separate script/step from
drafting -- per step 29, nothing reaches the graph without a human
having looked at the draft first, for at least the first 10-20 uses.

Run graph-schema/run.ps1 afterward -- this writes a node that's already
schema-complete (category/tags/visibility/timestamps set by
summarize_session.py, reusing Module 4's own classifier), but the
community/report/tag-index artifacts still need graphify's own
clustering pass to actually include the new node.

Usage:
    python session-write/approve_session_summary.py           # review it yourself first!
    python session-write/approve_session_summary.py --yes     # skip the interactive confirm (for scripting only)
"""
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PENDING_PATH = ROOT / "session-write" / "pending-review.json"
STATE_PATH = ROOT / "session-write" / ".last_summarized_commit"
GRAPH_PATH = ROOT / "graphify-out" / "graph.json"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--yes", action="store_true", help="skip the interactive confirmation")
    args = parser.parse_args()

    if not PENDING_PATH.exists():
        print(f"[approve] no pending draft at {PENDING_PATH} -- run summarize_session.py first.", file=sys.stderr)
        sys.exit(1)

    pending = json.loads(PENDING_PATH.read_text(encoding="utf-8"))
    node = pending["node"]

    print(f"--- Draft session node: {node['id']} ---")
    print(f"label: {node['label']}")
    print(f"visibility: {node['visibility']}  tags: {node['tags']}")
    print(f"linked nodes: {len(pending['edges'])}")
    print(f"summary:\n{node.get('summary', '(none)')}")
    print("---")

    if not args.yes:
        answer = input("Append this to graphify-out/graph.json? [y/N] ").strip().lower()
        if answer != "y":
            print("[approve] not appended. Edit session-write/pending-review.json and re-run, "
                  "or delete it to discard the draft.")
            return

    graph = json.loads(GRAPH_PATH.read_text(encoding="utf-8"))
    existing_ids = {n["id"] for n in graph["nodes"]}
    if node["id"] in existing_ids:
        print(f"[approve] a node with id {node['id']} already exists -- refusing to duplicate it. "
              "Delete the existing one first if this is meant to replace it.", file=sys.stderr)
        sys.exit(1)

    graph["nodes"].append(node)
    graph["links"].extend(pending["edges"])
    GRAPH_PATH.write_text(json.dumps(graph, indent=2, ensure_ascii=False), encoding="utf-8")

    STATE_PATH.write_text(pending["end_ref"], encoding="utf-8")
    PENDING_PATH.unlink()

    print(f"[approve] appended {node['id']} + {len(pending['edges'])} edge(s) to graph.json.")
    print("[approve] next: run graph-schema\\run.ps1 to refresh clustering/report/tag-index, "
          "then graph-viewer\\generate_viewer.py to refresh the viewer.")


if __name__ == "__main__":
    main()
