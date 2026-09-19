"""Module 8's read path: given a task/topic, pull a bounded, relevant
slice of the knowledge graph instead of feeding a whole graph/vault/git
log into context (step 31 -- "this is the real token-savings
mechanism").

Deliberately narrower than `graphify query`, which already exists and
works well (BFS depth=2, vocabulary-expanded, token-budgeted -- see
KNOWLEDGE-GRAPH-GAP-SPEC.md's Module 2 finding that real retrieval
already exists). This tool is the literal, narrower thing step 30
names: match against Module 4's tag-index.json specifically, and pull
"matching nodes plus directly linked ones only" (one hop, not two).
Use `graphify query` instead when a broader answer is actually wanted --
this one is for the specific "don't feed the whole graph" case.

Privacy inherited, not reimplemented (same property Module 6/7 already
have): reads whatever's currently in graph.json, so a Module-4-redacted
private node's stub is all this can ever return.

Usage:
    python session-read/retrieve_context.py "TTS streaming fix"
    python session-read/retrieve_context.py "trade FIFO engine" --min-nodes 10
"""
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "odin-backend"))
from graph_schema_shared import retrieve  # noqa: E402 -- Module 10 made this the shared home

GRAPH_PATH = ROOT / "graphify-out" / "graph.json"
TAG_INDEX_PATH = ROOT / "graphify-out" / "tag-index.json"


def format_for_context(query, result, total_node_count):
    """Compact, LLM-readable text -- NOT a JSON dump. This is what
    actually gets fed into a future session's context, so the format
    itself is part of the token-savings mechanism, not just the
    node-count reduction."""
    lines = [f'## Graph context for: "{query}"']
    lines.append(f"({len(result['nodes'])} of {total_node_count} total nodes"
                 + (", widened for a sparse initial match" if result["widened"] else "") + ")")
    seed_set = set(result["seed_ids"])
    for n in sorted(result["nodes"], key=lambda n: n["id"] not in seed_set):
        role = "seed" if n["id"] in seed_set else "linked"
        priv = ", PRIVATE" if n.get("visibility") == "private" else ""
        lines.append(f"- [{role}] {n.get('label')} ({n.get('category', '?')}{priv})")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("query")
    parser.add_argument("--min-nodes", type=int, default=6)
    args = parser.parse_args()

    graph = json.loads(GRAPH_PATH.read_text(encoding="utf-8"))
    tag_index = json.loads(TAG_INDEX_PATH.read_text(encoding="utf-8"))

    result = retrieve(args.query, graph, tag_index, min_nodes=args.min_nodes)
    print(format_for_context(args.query, result, len(graph["nodes"])))


if __name__ == "__main__":
    main()
