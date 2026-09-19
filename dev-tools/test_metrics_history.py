"""Self-check for Odin's metrics-history sampler (master prompt section 9
-- real time-series history behind /api/systems, /api/storage,
/api/containers, which are otherwise point-in-time only).

Proves: an empty table reports "collection begins now" honestly rather
than fabricating a trend, a real sample round-trips through get_metrics_history
with the right shape, the period/hours lookback window actually filters,
and age-based retention prunes old rows. The background scheduler is
disabled (ODIN_DISABLE_METRICS_HISTORY=1) so this stays deterministic --
_sample_metrics() is called directly instead.

Run standalone from anywhere:
    python dev-tools/test_metrics_history.py
"""
import os
import sys
import tempfile
import time

BACKEND_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "odin-backend")
FAKE_PKGS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fake_pkgs")
sys.path.insert(0, FAKE_PKGS_DIR)
sys.path.insert(0, BACKEND_DIR)

os.environ["ODIN_API_TOKEN"] = "admin-test-token"
os.environ["ODIN_DB_PATH"] = os.path.join(tempfile.mkdtemp(), "test_odin.db")
os.environ["ODIN_DISABLE_MEMORY_TRENDS"] = "1"
os.environ["ODIN_DISABLE_METRICS_HISTORY"] = "1"  # drive _sample_metrics() by hand below

import app  # noqa: E402


def demo():
    # Empty table -> honest "collection begins now", not a fabricated trend.
    r = app.get_metrics_history()
    assert r["samples"] == [] and r["collection_started_at"] is None, r
    assert "begins now" in r["note"], r

    # A real sample round-trips with the expected shape.
    app._sample_metrics()
    r = app.get_metrics_history()
    assert len(r["samples"]) == 1, r
    sample = r["samples"][0]
    for field in ("timestamp", "cpu_percent", "mem_percent", "cpu_temp_c",
                  "containers_running", "containers_total", "storage"):
        assert field in sample, (field, sample)
    assert isinstance(sample["storage"], dict), sample
    assert r["collection_started_at"] == sample["timestamp"], r

    # Both admin chat tool and REST route serve it, admin-only.
    assert "get_metrics_history" in app.TOOL_DISPATCH
    assert "get_metrics_history" not in app.BETA_ALLOWED_TOOLS
    client = app.app.test_client()
    res = client.get("/api/metrics-history")
    assert res.status_code == 401, res.get_json()
    res = client.get("/api/metrics-history", headers={"Authorization": "Bearer admin-test-token"})
    assert res.status_code == 200 and len(res.get_json()["samples"]) == 1, res.get_json()

    # period/hours lookback actually filters -- a sample manually backdated
    # outside the window must not appear in a narrow query.
    conn = app._get_db_connection()
    old_ts = time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime(time.time() - 10 * 3600))
    conn.execute(
        "INSERT INTO metrics_history (timestamp, cpu_percent, mem_percent, cpu_temp_c, "
        "containers_running, containers_total, storage_json) VALUES (?, 1, 1, 1, 1, 1, '{}')",
        (old_ts,),
    )
    conn.commit()
    conn.close()
    hour_window = app.get_metrics_history(hours=1)["samples"]
    assert len(hour_window) == 1, hour_window  # only the fresh sample, not the 10h-old one
    day_window = app.get_metrics_history(period="day")["samples"]
    assert len(day_window) == 2, day_window  # both fall inside 24h

    # Retention: a row older than METRICS_HISTORY_RETENTION_DAYS is pruned
    # the next time a sample is written.
    conn = app._get_db_connection()
    ancient_ts = time.strftime(
        "%Y-%m-%dT%H:%M:%S",
        time.localtime(time.time() - (app.METRICS_HISTORY_RETENTION_DAYS + 1) * 86400),
    )
    conn.execute(
        "INSERT INTO metrics_history (timestamp, cpu_percent, mem_percent, cpu_temp_c, "
        "containers_running, containers_total, storage_json) VALUES (?, 1, 1, 1, 1, 1, '{}')",
        (ancient_ts,),
    )
    conn.commit()
    conn.close()
    app._sample_metrics()  # every write also prunes past-retention rows
    all_rows = app.get_metrics_history(hours=24 * 365)["samples"]
    assert ancient_ts not in [s["timestamp"] for s in all_rows], all_rows

    print("OK: empty history reports 'collection begins now' honestly, a real sample round-trips "
          "with the right shape, period/hours actually filter the lookback window, retention "
          "prunes rows past METRICS_HISTORY_RETENTION_DAYS, and the tool/route stay admin-only.")


if __name__ == "__main__":
    demo()
