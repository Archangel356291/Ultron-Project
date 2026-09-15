"""Self-check for the Data & analytics tab stat cards (evolution idea #2):
get_llm_usage's cost_usd_today and get_recent_activity's count_today, the
two fields that replaced the dashboard's previously-hardcoded, unwired
"Tokens this session / Session cost estimate / Commands routed today /
30-day uptime" placeholder numbers.

Proves both aggregates are real sums over today's rows, not copies of
some other field, and that a day-boundary is actually respected (a
backdated row from yesterday must not count).

Run standalone from anywhere:
    python dev-tools/test_data_analytics_stats.py
"""
import os
import sys
import tempfile
import time

BACKEND_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "ultron-backend")
FAKE_PKGS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fake_pkgs")
sys.path.insert(0, FAKE_PKGS_DIR)
sys.path.insert(0, BACKEND_DIR)

os.environ["ULTRON_API_TOKEN"] = "admin-test-token"
os.environ["ULTRON_DB_PATH"] = os.path.join(tempfile.mkdtemp(), "test_ultron.db")
os.environ["ULTRON_DISABLE_MEMORY_TRENDS"] = "1"
os.environ["ULTRON_DISABLE_METRICS_HISTORY"] = "1"

import app  # noqa: E402


def demo():
    # cost_usd_today: sums real cost_usd across today's rows (admin + beta).
    r = app.get_llm_usage()
    assert r["cost_usd_today"] == 0.0, r

    conn = app._get_db_connection()
    now = time.strftime("%Y-%m-%dT%H:%M:%S")
    conn.execute(
        "INSERT INTO llm_usage (timestamp, input_tokens, output_tokens, "
        "cache_read_input_tokens, cache_creation_input_tokens, beta_name, cost_usd) "
        "VALUES (?, 100, 50, 0, 0, NULL, 0.0123)", (now,),
    )
    conn.execute(
        "INSERT INTO llm_usage (timestamp, input_tokens, output_tokens, "
        "cache_read_input_tokens, cache_creation_input_tokens, beta_name, cost_usd) "
        "VALUES (?, 10, 5, 0, 0, 'someone', 0.0007)", (now,),
    )
    # A row from yesterday must not count toward "today".
    yesterday = time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime(time.time() - 86400))
    conn.execute(
        "INSERT INTO llm_usage (timestamp, input_tokens, output_tokens, "
        "cache_read_input_tokens, cache_creation_input_tokens, beta_name, cost_usd) "
        "VALUES (?, 999, 999, 0, 0, NULL, 5.0)", (yesterday,),
    )
    conn.commit()
    conn.close()

    r = app.get_llm_usage()
    assert r["cost_usd_today"] == 0.013, r  # 0.0123 + 0.0007, admin+beta combined, yesterday excluded
    assert r["total_tokens"] == 165, r  # 150 + 15, not the 1998 from yesterday's row

    # count_today: real COUNT(*) over today's activity_log rows, day-boundary respected.
    r = app.get_recent_activity()
    assert r["count_today"] == 0, r
    app.log_activity("backup", "backup ran")
    app.log_activity("cve_scan", "scan ran")
    conn = app._get_db_connection()
    conn.execute(
        "INSERT INTO activity_log (timestamp, event_type, summary, status) VALUES (?, 'old', 'yesterday event', 'success')",
        (yesterday,),
    )
    conn.commit()
    conn.close()
    r = app.get_recent_activity()
    assert r["count_today"] == 2, r  # not 3 -- yesterday's row excluded
    assert len(r["events"]) == 3, r  # but the events list itself is unbounded by day, unchanged behavior

    print("OK: get_llm_usage.cost_usd_today and get_recent_activity.count_today are real sums/counts "
          "over today's rows (admin+beta combined for cost), and both respect the day boundary "
          "rather than including yesterday's rows.")


if __name__ == "__main__":
    demo()
