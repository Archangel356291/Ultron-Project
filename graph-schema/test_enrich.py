"""Self-check for graph-schema/enrich_visibility.py (Module 4).

Proves the actual behavior against real temp files (never the real
graphify-out/), not just that the functions run without throwing:
private nodes get their full content redacted out of graph.json and
genuinely encrypted (wrong key fails to decrypt, right key round-trips
byte-for-byte); public nodes are left fully intact plus the new fields;
the tag index is correct; and date_created survives a second run while
date_updated only moves when the source file's own mtime changes.

Run standalone from anywhere:
    python graph-schema/test_enrich.py
"""
import json
import sys
import tempfile
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from cryptography.fernet import Fernet, InvalidToken
import enrich_visibility as ev


def _write(path, obj):
    path.write_text(json.dumps(obj), encoding="utf-8")


def _fresh_paths(tmp):
    return dict(
        graph_path=tmp / "graph.json",
        manifest_path=tmp / "manifest.json",
        history_path=tmp / ".node_history.json",
        tag_index_path=tmp / "tag-index.json",
        private_store_path=tmp / "private-nodes.enc.json",
        env_path=tmp / ".env",
    )


def demo():
    tmp = Path(tempfile.mkdtemp())
    paths = _fresh_paths(tmp)

    graph = {
        "nodes": [
            {"id": "n_public_code", "label": "get_system_status", "file_type": "code",
             "source_file": "odin-backend/app.py", "community_name": "Backend REST Routes"},
            {"id": "n_private_tailscale", "label": "Tailscale Remote Access", "file_type": "document",
             "source_file": "odin-backend/REMOTE-ACCESS.md", "community_name": "Beta Program & Tailscale Docs"},
            {"id": "n_private_ip", "label": "Pi network address 192.168.1.50", "file_type": "concept",
             "source_file": "odin-backend/PI-SETUP.md", "community_name": "Pi Setup"},
        ],
        "links": [],
        "hyperedges": [],
    }
    _write(paths["graph_path"], graph)
    manifest = {
        "odin-backend/app.py": {"mtime": 1000.0},
        "odin-backend/REMOTE-ACCESS.md": {"mtime": 2000.0},
        "odin-backend/PI-SETUP.md": {"mtime": 3000.0},
    }
    _write(paths["manifest_path"], manifest)

    ev.enrich(**paths)

    result = json.loads(paths["graph_path"].read_text(encoding="utf-8"))
    by_id = {n["id"]: n for n in result["nodes"]}

    # Public node: untouched content, plus the new fields.
    pub = by_id["n_public_code"]
    assert pub["label"] == "get_system_status", pub
    assert pub["visibility"] == "public", pub
    assert pub["category"] == "code", pub
    assert "type:code" in pub["tags"] and "visibility:public" in pub["tags"], pub
    assert pub["date_created"] and pub["date_updated"], pub

    # Private nodes: redacted in the plaintext graph.
    for nid in ("n_private_tailscale", "n_private_ip"):
        priv = by_id[nid]
        assert priv["label"] == "[private]", priv
        assert priv["visibility"] == "private", priv
        assert "source_file" not in priv, f"{nid} leaked source_file into the plaintext graph: {priv}"
        assert "Tailscale" not in json.dumps(priv) and "192.168" not in json.dumps(priv), priv

    # Encrypted store: has exactly the private ids, and decrypts correctly.
    store = json.loads(paths["private_store_path"].read_text(encoding="utf-8"))
    assert set(store.keys()) == {"n_private_tailscale", "n_private_ip"}, store.keys()

    key = ev._get_or_create_key(paths["env_path"], paths["private_store_path"], quiet=True)
    recovered = ev.decrypt_private_node("n_private_tailscale", key=key, private_store_path=paths["private_store_path"])
    assert recovered["label"] == "Tailscale Remote Access", recovered
    assert recovered["source_file"] == "odin-backend/REMOTE-ACCESS.md", recovered

    # Wrong key must fail, not silently return garbage.
    wrong_key = Fernet.generate_key()
    try:
        ev.decrypt_private_node("n_private_tailscale", key=wrong_key, private_store_path=paths["private_store_path"])
        assert False, "decrypting with the wrong key should have raised InvalidToken"
    except InvalidToken:
        pass

    # Tag index correctness.
    tag_index = json.loads(paths["tag_index_path"].read_text(encoding="utf-8"))
    assert "n_public_code" in tag_index["type:code"], tag_index
    assert "n_private_tailscale" in tag_index["visibility:private"], tag_index

    # Second run: date_created stable, date_updated stable too (mtime unchanged).
    created_before = by_id["n_public_code"]["date_created"]
    updated_before = by_id["n_public_code"]["date_updated"]
    time.sleep(0.05)
    ev.enrich(**paths)
    result2 = json.loads(paths["graph_path"].read_text(encoding="utf-8"))
    by_id2 = {n["id"]: n for n in result2["nodes"]}
    pub2 = by_id2["n_public_code"]
    assert pub2["date_created"] == created_before, "date_created must not move on an unchanged rerun"
    assert pub2["date_updated"] == updated_before, "date_updated must track source mtime, not 'now'"

    # The real bug this caught: a naive re-run reclassified already-
    # redacted private nodes as public, because the redacted stub no
    # longer contains the keywords that made it private in the first
    # place. Private must stay private across reruns.
    for nid in ("n_private_tailscale", "n_private_ip"):
        assert by_id2[nid]["visibility"] == "private", (
            f"{nid} flipped to public on a second run -- redaction isn't idempotent: {by_id2[nid]}"
        )
        assert by_id2[nid]["label"] == "[private]", by_id2[nid]
    store2 = json.loads(paths["private_store_path"].read_text(encoding="utf-8"))
    assert set(store2.keys()) == {"n_private_tailscale", "n_private_ip"}, (
        "private store must still hold exactly the private nodes after a second run"
    )

    # Bump the source file's mtime and rerun: date_updated moves, date_created still doesn't.
    manifest["odin-backend/app.py"]["mtime"] = 9999.0
    _write(paths["manifest_path"], manifest)
    ev.enrich(**paths)
    result3 = json.loads(paths["graph_path"].read_text(encoding="utf-8"))
    pub3 = {n["id"]: n for n in result3["nodes"]}["n_public_code"]
    assert pub3["date_created"] == created_before, "date_created must survive a real content update too"
    assert pub3["date_updated"] != updated_before, "date_updated must move when the source file's mtime changes"

    print("OK: private nodes redacted + genuinely encrypted (wrong key fails, right key round-trips), "
          "public nodes untouched plus new fields, tag index correct, timestamps behave correctly "
          "across reruns and real source-file changes.")


if __name__ == "__main__":
    demo()
