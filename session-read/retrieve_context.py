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
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GRAPH_PATH = ROOT / "graphify-out" / "graph.json"
TAG_INDEX_PATH = ROOT / "graphify-out" / "tag-index.json"

_WORD_RE = re.compile(r"[a-z0-9]+")


def _words(text):
    return [w for w in _WORD_RE.findall((text or "").lower()) if len(w) > 2]


def _tag_words(tag):
    """Tokenizes only a tag's VALUE, not its structural key. Every node
    carries a visibility:public or visibility:private tag and a
    type:<category> tag by construction (Module 4's schema) -- if
    "visibility" or "type" themselves were matchable words, a query
    containing either would match the entire graph, not a relevant
    slice (this was a real bug: "private node encryption visibility"
    matched all 543 nodes via the universal "visibility" word before
    this fix, caught by measure_savings.py showing 0% real reduction
    despite reporting 95.7%)."""
    value = tag.split(":", 1)[1] if ":" in tag else tag
    return _words(value)


def retrieve(query, graph, tag_index, min_nodes=6):
    """Returns a dict: seed_ids, neighbor_ids, nodes, edges, widened.
    Never touches more of the graph than what's returned."""
    query_words = set(_words(query))
    if not query_words:
        return {"seed_ids": [], "neighbor_ids": [], "nodes": [], "edges": [], "widened": False}

    # Primary match: Module 4's tag-index.json -- this is the specific
    # artifact step 30 names, and it's cheap (a dict lookup by substring),
    # not a re-scan of every node's full content.
    seed_ids = set()
    for tag, ids in tag_index.items():
        if query_words & set(_tag_words(tag)):
            seed_ids.update(ids)

    # Secondary: node label match -- catches queries whose words don't
    # happen to appear in any tag (e.g. a specific function name).
    by_id = {n["id"]: n for n in graph["nodes"]}
    for node in graph["nodes"]:
        if query_words & set(_words(node.get("label"))):
            seed_ids.add(node["id"])

    # Step 31: "if a task is ambiguous or broad, pull in enough context
    # to answer well rather than under-feeding." Widen to summary/
    # community text only when the tight match genuinely came up short --
    # never used to shrink an already-adequate match.
    widened = False
    if len(seed_ids) < min_nodes:
        widened = True
        for node in graph["nodes"]:
            hay = " ".join(str(node.get(k, "")) for k in ("summary", "community_name"))
            if query_words & set(_words(hay)):
                seed_ids.add(node["id"])

    # One hop only ("directly linked ones only", step 30) -- this is the
    # deliberate difference from graphify query's default 2-hop BFS.
    neighbor_ids = set()
    for edge in graph["links"]:
        s, t = edge.get("source"), edge.get("target")
        if s in seed_ids and t not in seed_ids:
            neighbor_ids.add(t)
        elif t in seed_ids and s not in seed_ids:
            neighbor_ids.add(s)

    result_ids = seed_ids | neighbor_ids
    nodes = [by_id[i] for i in result_ids if i in by_id]
    edges = [e for e in graph["links"] if e.get("source") in result_ids and e.get("target") in result_ids]

    return {
        "seed_ids": sorted(seed_ids),
        "neighbor_ids": sorted(neighbor_ids),
        "nodes": nodes,
        "edges": edges,
        "widened": widened,
    }


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
