"""Self-check for Module 9 (step 33: "confirm restore actually works,
don't just assume it").

The strong proof, not the weak one: a weak test would just check that
restored files exist on disk. This test backs up the REAL project's
private-nodes.enc.json + .env, restores them into an isolated temp
directory, and then actually DECRYPTS a real private node using ONLY
the restored copies (never touching the real .env's key directly --
reads it back out of the restored file the same way any real disaster
recovery would) and asserts the decrypted content matches decrypting
the same node from the live files. If the backup or restore silently
corrupted or truncated anything, this fails; a file-existence check
would not have caught that.

Also tests rotation (old backups actually get deleted past the keep
count) in a fully isolated temp backup directory, never touching the
real backup history.

Run standalone from anywhere:
    python backup/test_backup_restore.py
"""
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "graph-schema"))
import backup_graph_data as bk  # noqa: E402
import restore_graph_data as rs  # noqa: E402
import enrich_visibility as ev  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parent.parent


def demo_real_round_trip():
    """Backs up and restores the REAL project's private-node store and
    key, proving restore actually recovers working, decryptable data --
    not just that files with the right names reappear."""
    real_store = REPO_ROOT / "graphify-out" / "private-nodes.enc.json"
    real_env = REPO_ROOT / ".env"
    if not real_store.exists() or not real_env.exists():
        print("[test_backup_restore] SKIP real round-trip: no real private-nodes.enc.json/.env "
              "in this checkout yet.")
        return

    import json
    store = json.loads(real_store.read_text(encoding="utf-8"))
    if not store:
        print("[test_backup_restore] SKIP real round-trip: private-nodes.enc.json is empty.")
        return
    sample_node_id = next(iter(store))

    # Decrypt from the REAL files first, as the ground truth to compare against.
    expected = ev.decrypt_private_node(sample_node_id)

    tmp_backup_dir = Path(tempfile.mkdtemp()) / "backups"
    zip_path = bk.backup(backup_dir=tmp_backup_dir)
    assert zip_path is not None and zip_path.exists(), "backup produced no archive"

    restore_target = Path(tempfile.mkdtemp())
    restored_names = rs.restore(zip_path, restore_target, yes=True)
    assert "graphify-out/private-nodes.enc.json" in restored_names, restored_names
    assert ".env" in restored_names, restored_names

    restored_store_path = restore_target / "graphify-out" / "private-nodes.enc.json"
    restored_env_path = restore_target / ".env"
    assert restored_store_path.exists() and restored_env_path.exists()

    # The actual proof: decrypt using ONLY the restored copies.
    restored_key = ev._get_or_create_key(env_path=restored_env_path,
                                          private_store_path=restored_store_path, quiet=True)
    recovered = ev.decrypt_private_node(sample_node_id, key=restored_key,
                                         private_store_path=restored_store_path)

    assert recovered == expected, (
        "restored data decrypts to something DIFFERENT from the live data -- "
        "backup/restore silently corrupted something"
    )

    print(f"[test_backup_restore] OK: backed up + restored into an isolated temp dir, "
          f"decrypted node {sample_node_id!r} from ONLY the restored files, "
          f"byte-for-byte identical to decrypting it from the live files.")


def demo_rotation():
    # backup()'s arcname is always relative to REPO_ROOT (a reasonable
    # assumption -- every real source in SOURCES lives under the repo) --
    # so the fake source for this test needs to live there too, not in an
    # unrelated temp dir, or relative_to() raises exactly as it should.
    scratch_dir = REPO_ROOT / "backup" / ".test_scratch"
    scratch_dir.mkdir(exist_ok=True)
    fake_source = scratch_dir / "fake.txt"
    fake_source.write_text("fake content", encoding="utf-8")

    backup_dir = Path(tempfile.mkdtemp()) / "backups"
    try:
        for _ in range(5):
            bk.backup(backup_dir=backup_dir, sources=[fake_source], keep_last_n=3)

        remaining = sorted(backup_dir.glob("graph-data-*.zip"))
        assert len(remaining) == 3, f"expected rotation to keep exactly 3, found {len(remaining)}: {remaining}"
        print("[test_backup_restore] OK: rotation keeps only the most recent N backups.")
    finally:
        fake_source.unlink()
        scratch_dir.rmdir()


if __name__ == "__main__":
    demo_real_round_trip()
    demo_rotation()
