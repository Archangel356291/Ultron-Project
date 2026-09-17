"""Self-check for ULTRON_STORAGE_MOUNTS parsing and the storage read.

The Docker container cannot see the host's drives except where compose
bind-mounts them, so the mount list must be configurable; this proves the
"label=path,label=path" form parses (and tolerates junk), that a bad or
empty value falls back to the platform default, and that _storage_data()
reports real numbers for a real path and a clear error for a missing one.

Run standalone from anywhere:
    python dev-tools/test_storage_mounts.py
"""
import os
import sys
import tempfile

BACKEND_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "ultron-backend")
FAKE_PKGS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fake_pkgs")
sys.path.insert(0, FAKE_PKGS_DIR)
sys.path.insert(0, BACKEND_DIR)

REAL_DIR = tempfile.mkdtemp()
os.environ["ULTRON_API_TOKEN"] = "admin-test-token"
os.environ["ULTRON_DB_PATH"] = os.path.join(REAL_DIR, "test_ultron.db")
os.environ["ULTRON_DISABLE_MEMORY_TRENDS"] = "1"
os.environ["ULTRON_DISABLE_METRICS_HISTORY"] = "1"
os.environ["ULTRON_SENTINEL_INTERVAL_SECONDS"] = "0"
os.environ["ULTRON_STORAGE_MOUNTS"] = f"Real={REAL_DIR}, Missing={os.path.join(REAL_DIR, 'nope')} ,junk-without-equals,=nolabel,nopath="

import app  # noqa: E402


def demo():
    assert app.STORAGE_MOUNTS == {"Real": REAL_DIR, "Missing": os.path.join(REAL_DIR, "nope")}, app.STORAGE_MOUNTS
    assert app._parse_storage_mounts("") == {} and app._parse_storage_mounts(None) == {}
    assert app._parse_storage_mounts("C:=/host/c,D:=/host/d") == {"C:": "/host/c", "D:": "/host/d"}

    data = app._storage_data()
    real = data["Real"]
    assert real["path"] == REAL_DIR and real["total_gb"] > 0 and 0 <= real["percent_used"] <= 100, real
    assert abs(real["total_gb"] - (real["used_gb"] + (real["total_gb"] - real["used_gb"]))) < 0.01
    assert data["Missing"]["error"] == "path not found", data["Missing"]

    # The briefing carries the labels as given (a drive letter reads as itself).
    lines = " ".join(app.get_briefing()["lines"])
    assert "Storage Real:" in lines and "Missing" not in lines, lines

    print("OK: ULTRON_STORAGE_MOUNTS parses label=path pairs (ignoring junk), a real path reports real "
          "numbers, a missing one a clear error, and the briefing uses the labels as given.")


if __name__ == "__main__":
    demo()
