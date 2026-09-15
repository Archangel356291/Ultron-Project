"""Module 9: automated periodic backup of the graph data that ISN'T
already safe in git -- graphify-out/graph.json is fine, it's public and
already committed/pushed. What actually needs a separate backup is
exactly what Module 4 deliberately kept OUT of git: the encrypted
private-node store and the key that decrypts it. Losing both together
means losing every private node's content permanently (Module 4's own
docs already say so) -- this is the "separate from the GitHub repo"
step 33 asks for.

Never reads or prints the .env file's contents -- copies it as a file
(shutil.copy2), the same way a real backup tool would, without this
script (or me) ever needing to see what's inside it.

Backs up to a directory OUTSIDE the git repo (C:\\Ultron Project\\_backups\\,
a sibling of the git repo root -- same pattern _archive/ already uses),
timestamped, rotated to keep only the most recent N backups so this
doesn't grow unbounded.

Usage:
    python backup/backup_graph_data.py
"""
import shutil
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
BACKUP_DIR = REPO_ROOT.parent / "_backups" / "graph-data"
KEEP_LAST_N = 10

# What actually needs backing up -- everything here is either gitignored
# (private-nodes.enc.json, .env) or small enough that including it costs
# nothing and guarantees one zip is a fully consistent restore point
# (.node_history.json is git-tracked already, but a restore that also
# recovers it in one step is simpler than "recover 2 of 3 files from here,
# 1 from git").
SOURCES = [
    REPO_ROOT / "graphify-out" / "private-nodes.enc.json",
    REPO_ROOT / ".env",
    REPO_ROOT / "graph-schema" / ".node_history.json",
]


def backup(backup_dir=BACKUP_DIR, sources=SOURCES, keep_last_n=KEEP_LAST_N):
    backup_dir.mkdir(parents=True, exist_ok=True)
    # Microsecond precision, not just seconds -- two backups fired within
    # the same second (a manual run right after a scheduled one, or this
    # test's own rotation check) would otherwise collide on the same
    # filename and silently overwrite each other with no warning.
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    archive_path = backup_dir / f"graph-data-{timestamp}.zip"

    included = []
    with zipfile.ZipFile(archive_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for src in sources:
            if not src.exists():
                continue
            # Relative arcname (e.g. "graphify-out/private-nodes.enc.json")
            # so restore knows exactly where each file belongs.
            arcname = str(src.relative_to(REPO_ROOT))
            zf.write(src, arcname)
            included.append(arcname)

    if not included:
        archive_path.unlink()
        print("[backup] nothing to back up -- no source files exist yet.", file=sys.stderr)
        return None

    _rotate(backup_dir, keep_last_n)
    print(f"[backup] wrote {archive_path} ({len(included)} file(s): {', '.join(included)})")
    return archive_path


def _rotate(backup_dir, keep_last_n):
    backups = sorted(backup_dir.glob("graph-data-*.zip"), key=lambda p: p.name)
    for old in backups[:-keep_last_n] if keep_last_n > 0 else []:
        old.unlink()


if __name__ == "__main__":
    backup()
