"""Step 32: measure context size before/after retrieval, for real
queries against the real graph -- not a claimed percentage, a computed
one. Token counts are an estimate (chars/4, the standard rough rule of
thumb for English text) since no real tokenizer for Claude's own models
is installed here -- stated plainly rather than implying more precision
than a heuristic has. The ratio between full-graph and slice is what
matters for this comparison, and chars/4 applied consistently to both
sides is fair for that, even if the absolute numbers are approximate.

Usage:
    python session-read/measure_savings.py
"""
import json
from pathlib import Path

from retrieve_context import retrieve, format_for_context

ROOT = Path(__file__).resolve().parent.parent
GRAPH_PATH = ROOT / "graphify-out" / "graph.json"
TAG_INDEX_PATH = ROOT / "graphify-out" / "tag-index.json"

SAMPLE_QUERIES = [
    "TTS streaming fix",
    "private node encryption visibility",
    "gitleaks secret scan pre-commit",
    "three.js Blender pipeline",
    "trade FIFO engine tax lots",
]


def est_tokens(text):
    return len(text) // 4


def main():
    graph = json.loads(GRAPH_PATH.read_text(encoding="utf-8"))
    tag_index = json.loads(TAG_INDEX_PATH.read_text(encoding="utf-8"))

    full_text = json.dumps(graph, ensure_ascii=False)
    full_tokens = est_tokens(full_text)

    print(f"Full graph.json: {len(graph['nodes'])} nodes, ~{full_tokens:,} tokens (estimated, chars/4)\n")
    print(f"{'query':<42} {'nodes':>7} {'~tokens':>9} {'reduction':>10}")
    print("-" * 72)

    for query in SAMPLE_QUERIES:
        result = retrieve(query, graph, tag_index)
        text = format_for_context(query, result, len(graph["nodes"]))
        tokens = est_tokens(text)
        reduction = 100 * (1 - tokens / full_tokens) if full_tokens else 0
        print(f"{query:<42} {len(result['nodes']):>7} {tokens:>9,} {reduction:>9.1f}%")


if __name__ == "__main__":
    main()
