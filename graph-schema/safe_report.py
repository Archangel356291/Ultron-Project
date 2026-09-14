"""Regenerates graph.json's community_name field, GRAPH_REPORT.md, and
graph.html with privacy-safe community labels -- closes a real leak
found while building Module 4: `graphify cluster-only` derives a
community's auto-name from its most-connected node, and node IDs
necessarily still contain the real name (they can't be redacted without
breaking every edge reference), so a private node's real identity was
leaking back in through its community's name even though the node's own
`label` field was correctly "[private]".

Must run under graphify's OWN interpreter (needs the graphify package;
enrich_visibility.py deliberately runs under a plain system Python with
`cryptography` instead, so this is a separate script, not folded into
that one). Run this AFTER enrich_visibility.py, using whichever
interpreter graphify itself uses:

    <graphify-python> graph-schema/safe_report.py

Any community containing at least one private node gets its name forced
to "Private/Mixed Community N" -- conservative on purpose: a community
that's mostly public but touches one private node still doesn't get a
name derived from that private node.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GRAPH_PATH = ROOT / "graphify-out" / "graph.json"


def make_safe_labels(G, communities):
    safe = {}
    for cid, members in communities.items():
        if any(G.nodes[m].get("visibility") == "private" for m in members if m in G.nodes):
            safe[cid] = f"Private/Mixed Community {cid}"
        else:
            safe[cid] = G.nodes[members[0]].get("community_name") if members else f"Community {cid}"
    return safe


def main():
    from graphify.build import build_from_json
    from graphify.cluster import cluster, score_all
    from graphify.analyze import god_nodes, surprising_connections, suggest_questions
    from graphify.report import generate
    from graphify.export import to_json

    extraction = json.loads(GRAPH_PATH.read_text(encoding="utf-8"))
    G = build_from_json(extraction, root=str(ROOT), directed=extraction.get("directed", False))
    communities = cluster(G)
    cohesion = score_all(G, communities)

    labels = make_safe_labels(G, communities)
    private_communities = sum(1 for v in labels.values() if v.startswith("Private/Mixed"))

    gods = god_nodes(G)
    surprises = surprising_connections(G, communities)
    # A private node's label is already "[private]" -- god-nodes/surprising-connections
    # report by label, so nothing further to scrub there; the leak was only ever the
    # community name itself.
    questions = suggest_questions(G, communities, labels)
    tokens = {"input": 0, "output": 0}
    detection = {"total_files": G.number_of_nodes(), "total_words": 0, "files": {}}

    report = generate(G, communities, cohesion, labels, gods, surprises, detection, tokens,
                       str(ROOT), suggested_questions=questions)
    (ROOT / "graphify-out" / "GRAPH_REPORT.md").write_text(report, encoding="utf-8")

    wrote = to_json(G, communities, str(GRAPH_PATH), community_labels=labels, force=True)

    print(f"[safe_report] {len(communities)} communities, {private_communities} forced to a "
          f"generic name for touching a private node. graph.json written: {wrote}")

    try:
        from graphify.export import to_html
        to_html(G, communities, str(ROOT / "graphify-out" / "graph.html"), community_labels=labels)
        print("[safe_report] graph.html regenerated with safe labels.")
    except ImportError:
        print("[safe_report] graphify.export.to_html not available in this version -- "
              "run `graphify export html` manually to refresh it.", file=sys.stderr)


if __name__ == "__main__":
    main()
