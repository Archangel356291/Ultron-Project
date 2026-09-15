"""Restores a graph-data backup produced by backup_graph_data.py.

Usage:
    python backup/restore_graph_data.py                  # restores the latest backup into the real repo
    python backup/restore_graph_data.py --zip <path>      # restores a specific backup
    python backup/restore_graph_data.py --to <dir>        # restores into a different directory (used by the test suite)
    python backup/restore_graph_data.py --yes              # skip the interactive confirm

Refuses to overwrite existing files without --yes when restoring into
the real repo -- a restore is exactly the kind of action that should
require a deliberate confirmation, the same reasoning as every other
"are you sure" gate in this project.
"""
import argparse
import zipfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
BACKUP_DIR = REPO_ROOT.parent / "_backups" / "graph-data"


def latest_backup(backup_dir=BACKUP_DIR):
    backups = sorted(backup_dir.glob("graph-data-*.zip"), key=lambda p: p.name)
    return backups[-1] if backups else None


def restore(zip_path, target_dir, yes=False):
    with zipfile.ZipFile(zip_path, "r") as zf:
        names = zf.namelist()
        existing = [n for n in names if (target_dir / n).exists()]
        if existing and not yes:
            answer = input(
                f"Restoring will overwrite {len(existing)} existing file(s): "
                f"{', '.join(existing)}\nProceed? [y/N] "
            ).strip().lower()
            if answer != "y":
                print("[restore] cancelled.")
                return []
        zf.extractall(target_dir)
    return names


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--zip", type=Path, help="Specific backup zip (default: latest)")
    parser.add_argument("--to", type=Path, default=REPO_ROOT, help="Restore target directory (default: this repo)")
    parser.add_argument("--yes", action="store_true")
    args = parser.parse_args()

    zip_path = args.zip or latest_backup()
    if not zip_path or not zip_path.exists():
        print("[restore] no backup found.")
        return

    restored = restore(zip_path, args.to, yes=args.yes)
    if restored:
        print(f"[restore] restored {len(restored)} file(s) from {zip_path.name} into {args.to}: "
              f"{', '.join(restored)}")


if __name__ == "__main__":
    main()
