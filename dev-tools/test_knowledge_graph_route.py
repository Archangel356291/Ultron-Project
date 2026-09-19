"""Self-check for the Home-tab knowledge graph endpoint (get_knowledge_graph
/ GET /api/knowledge-graph).

Proves the real mechanism, not just that the route exists: it actually
reads graphify-out/graph.json (real vault data, not a fabricated demo
set), merges in Odin's own runtime memory graph via the exact same
_notes_as_graph() helper recall_related_notes already uses, the size
limit keeps the highest-degree nodes (not an arbitrary prefix), and the
route stays admin-only.

Run standalone from anywhere:
    python dev-tools/test_knowledge_graph_route.py
"""
import json
import os
import sys
import tempfile

BACKEND_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "odin-backend")
FAKE_PKGS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fake_pkgs")
sys.path.insert(0, FAKE_PKGS_DIR)
sys.path.insert(0, BACKEND_DIR)

os.environ["ODIN_API_TOKEN"] = "admin-test-token"
os.environ["ODIN_DB_PATH"] = os.path.join(tempfile.mkdtemp(), "test_odin.db")
os.environ["ODIN_DISABLE_MEMORY_TRENDS"] = "1"

import app  # noqa: E402


def demo_real_vault_data():
    result = app.get_knowledge_graph()
    assert "error" not in result, result
    assert result["stats"]["node_count"] > 0, "expected real nodes from graphify-out/graph.json"
    assert result["stats"]["link_count"] > 0, result["stats"]
    # Every node came from the real file or real memory -- no node whose id
    # doesn't trace to one of those two sources.
    real_graph = json.load(open(app.GRAPH_PATH, encoding="utf-8"))
    real_ids = {n["id"] for n in real_graph["nodes"]}
    for n in result["nodes"]:
        is_memory = str(n["id"]).startswith("mem:")
        assert is_memory or n["id"] in real_ids, f"node {n['id']!r} traces to neither the vault graph nor memory"
    print(f"OK: get_knowledge_graph() returns {result['stats']['node_count']} real nodes "
          f"({result['stats']['link_count']} links, {result['stats']['clusters']} clusters) -- "
          f"every id traces to graphify-out/graph.json or Odin's own memory graph, none fabricated.")


def demo_memory_merge():
    app.remember_note(note="plex server runs on pi5 in closet")
    app.remember_note(note="update plex server monthly")
    result = app.get_knowledge_graph()
    mem_nodes = [n for n in result["nodes"] if n["category"] == "memory"]
    assert len(mem_nodes) >= 2, mem_nodes
    mem_links = [e for e in result["links"] if str(e["source"]).startswith("mem:") and str(e["target"]).startswith("mem:")]
    assert len(mem_links) >= 1, "expected the real memory_edges auto-link (Module 10) to carry through as a link"
    print(f"OK: remember_note()'d notes show up as real category:memory nodes ({len(mem_nodes)}) "
          f"with their real memory_edges relationship carried through ({len(mem_links)} link(s)).")


def demo_limit_keeps_highest_degree():
    full = app.get_knowledge_graph()
    total = full["stats"]["node_count"]
    assert total > 30, "test assumes the real vault graph has more than 30 nodes"

    # Real degree, computed independently of the function under test.
    degree = {}
    for e in full["links"]:
        degree[e["source"]] = degree.get(e["source"], 0) + 1
        degree[e["target"]] = degree.get(e["target"], 0) + 1
    top_ids_by_real_degree = {n_id for n_id, _ in sorted(degree.items(), key=lambda kv: kv[1], reverse=True)[:20]}

    limited = app.get_knowledge_graph(limit=20)
    assert limited["stats"]["node_count"] == 20, limited["stats"]
    limited_ids = {n["id"] for n in limited["nodes"]}
    # Real check: the kept set is (close to) the actual highest-degree
    # nodes, not just "the first 20 in file order" -- catches a regression
    # to a naive nodes[:limit] slice, which would silently pass a "returns
    # 20 nodes" assertion alone.
    overlap = len(limited_ids & top_ids_by_real_degree)
    assert overlap >= 15, f"expected the limited graph to keep mostly the real highest-degree nodes, overlap was {overlap}/20"

    # Every surviving link's both ends must be in the kept node set -- no
    # dangling edges pointing at a trimmed-away node.
    for e in limited["links"]:
        assert e["source"] in limited_ids and e["target"] in limited_ids, e
    print(f"OK: limit=20 keeps the real highest-degree nodes ({overlap}/20 match an independent degree "
          f"computation), and no link dangles at a trimmed node.")


def demo_admin_only():
    client = app.app.test_client()
    res = client.get("/api/knowledge-graph")
    assert res.status_code == 401, res.status_code

    res2 = client.get("/api/knowledge-graph", headers={"Authorization": "Bearer admin-test-token"})
    assert res2.status_code == 200, res2.get_json()
    body = res2.get_json()
    assert "nodes" in body and "stats" in body, body
    print("OK: GET /api/knowledge-graph refuses no token (401) and serves real data with a token.")


if __name__ == "__main__":
    demo_real_vault_data()
    demo_memory_merge()
    demo_limit_keeps_highest_degree()
    demo_admin_only()
