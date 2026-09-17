"""Canonical implementation of the schema/tagging/retrieval logic Module
4 (graph-schema/enrich_visibility.py) and Module 8
(session-read/retrieve_context.py) built for the vault knowledge graph.
Lives here, inside ultron-backend/, specifically so Module 10 can
import it directly at runtime (this is the only one of the three
consumers that actually ships inside a Docker image -- see the
Dockerfile's COPY list) -- the other two now import FROM this module
instead of keeping their own copies, so there's exactly one
implementation, not three that could quietly drift apart. Per the
roadmap's own instruction for Module 10: "do not design this from
scratch, reuse the same schema/tagging/indexing/retrieval logic."

No dependency on anything graph.json-specific or vault-specific --
every function here operates on plain dicts/lists (nodes, edges, a
tag-index mapping), so the exact same code works whether those came
from graphify-out/graph.json (the vault) or Ultron's own memory_notes/
memory_edges SQLite tables (this module).
"""
import re

_PRIVATE_KEYWORDS = (
    "api key", "api_key", "apikey", "credential", "password", "secret",
    "token", "bearer", "auth token",
    "vpn", "wireguard", "tailscale", "network config", "firewall",
    "home lab", "raspberry pi", "pi-setup",
    "trading position", "account balance", "portfolio", "trade record",
    "financial", "realized gain", "tax lot", "fifo",
    "ssn", "passport", "beta spend", "spend cap",
)
_IP_RE = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")
_WORD_RE = re.compile(r"[a-z0-9]+")


def classify_visibility(node):
    """Private by default on any doubt (the roadmap's own instruction).
    Sticky once private -- see docs/GRAPH-SCHEMA-DESIGN.md for
    why re-deriving from already-redacted content would misread "no
    more telltale keywords" as "safe to make public," which is
    backwards."""
    if node.get("visibility") == "private":
        return "private"
    haystack = " ".join(
        str(node.get(k, "")) for k in ("label", "source_file", "community_name", "norm_label")
    ).lower()
    if _IP_RE.search(haystack):
        return "private"
    for kw in _PRIVATE_KEYWORDS:
        if kw in haystack:
            return "private"
    return "public"


def _slug(text):
    return re.sub(r"[^a-z0-9]+", "_", str(text).lower()).strip("_")


def derive_tags(node, visibility):
    tags = []
    if node.get("file_type"):
        tags.append(f"type:{node['file_type']}")
    if node.get("community_name"):
        tags.append(f"community:{_slug(node['community_name'])}")
    tags.append(f"visibility:{visibility}")
    return tags


def _words(text):
    return [w for w in _WORD_RE.findall((text or "").lower()) if len(w) > 2]


def _tag_words(tag):
    """Tokenizes only a tag's VALUE, not its structural key -- see
    session-read/README.md's real-bug writeup: every node/note carries
    a visibility:public or visibility:private tag by construction, so
    if "visibility" itself were a matchable word, any query containing
    it would match everything, not a relevant slice."""
    value = tag.split(":", 1)[1] if ":" in tag else tag
    return _words(value)


def retrieve(query, graph, tag_index, min_nodes=6):
    """Given a query and a graph shaped as {"nodes": [...], "links":
    [...]} (source/target on links), returns a bounded, relevant slice:
    seed nodes matched via tag_index + labels, expanded exactly one hop.
    Widens to summary/community text only when the tight match came up
    short (step 31: pull in enough to answer well rather than
    under-feeding an ambiguous task)."""
    query_words = set(_words(query))
    if not query_words:
        return {"seed_ids": [], "neighbor_ids": [], "nodes": [], "edges": [], "widened": False}

    seed_ids = set()
    for tag, ids in tag_index.items():
        if query_words & set(_tag_words(tag)):
            seed_ids.update(ids)

    by_id = {n["id"]: n for n in graph["nodes"]}
    for node in graph["nodes"]:
        if query_words & set(_words(node.get("label"))):
            seed_ids.add(node["id"])

    widened = False
    if len(seed_ids) < min_nodes:
        widened = True
        for node in graph["nodes"]:
            hay = " ".join(str(node.get(k, "")) for k in ("summary", "community_name"))
            if query_words & set(_words(hay)):
                seed_ids.add(node["id"])

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
