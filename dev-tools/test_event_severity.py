"""Self-check for event severity classification (master prompt sections
21-26 -- "proactive but not interruptive" needs a way to tell CRITICAL
from routine).

Proves classify_event_severity's real mapping rules, that get_recent_activity
actually attaches a severity to every real logged event (not a hardcoded
value), that the severity filter only returns matching events, and that
an unknown severity value is rejected rather than silently ignored.

Run standalone from anywhere:
    python dev-tools/test_event_severity.py
"""
import os
import sys
import tempfile

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
    # The real classification rules, not just "it returns something".
    assert app.classify_event_severity("backup", "error") == "CRITICAL"
    assert app.classify_event_severity("deploy_container", "error") == "CRITICAL"
    assert app.classify_event_severity("cve_scan", "error") == "IMPORTANT"  # scan didn't run -- real, but not data-loss-critical
    assert app.classify_event_severity("mcp_tool_call", "error") == "IMPORTANT"
    assert app.classify_event_severity("backup", "warning") == "IMPORTANT"
    assert app.classify_event_severity("anything", "warning") == "IMPORTANT"
    assert app.classify_event_severity("backup", "success") == "INFORMATIONAL"
    assert app.classify_event_severity("deploy_container", "success") == "INFORMATIONAL"
    assert app.classify_event_severity("evolution_status_change", "success") == "INFORMATIONAL"
    assert app.classify_event_severity("cve_scan", "success") == "BACKGROUND"
    assert app.classify_event_severity("mcp_tool_call", "success") == "BACKGROUND"
    assert app.classify_event_severity("some_new_event_type", "success") == "BACKGROUND"  # unknown types default sane, not CRITICAL

    # get_recent_activity attaches a real severity per event, derived from
    # what was actually logged -- not a copy of status, not hardcoded.
    app.log_activity("backup", "backup failed", status="error")
    app.log_activity("mcp_tool_call", "tool call ok", status="success")
    app.log_activity("cve_scan", "scan could not run", status="error")
    events = app.get_recent_activity(limit=10)["events"]
    by_summary = {e["summary"]: e["severity"] for e in events}
    assert by_summary["backup failed"] == "CRITICAL", by_summary
    assert by_summary["tool call ok"] == "BACKGROUND", by_summary
    assert by_summary["scan could not run"] == "IMPORTANT", by_summary

    # The severity filter only returns matching events.
    critical_only = app.get_recent_activity(severity="CRITICAL")["events"]
    assert len(critical_only) == 1 and critical_only[0]["summary"] == "backup failed", critical_only
    assert all(e["severity"] == "CRITICAL" for e in critical_only)

    background_only = app.get_recent_activity(severity="background")["events"]  # case-insensitive
    assert len(background_only) == 1 and background_only[0]["summary"] == "tool call ok", background_only

    # An unrecognized severity is rejected, not silently ignored/returning everything.
    r = app.get_recent_activity(severity="NOT_A_REAL_SEVERITY")
    assert "error" in r, r

    # Both chat tool and REST route serve it.
    assert "get_recent_activity" in app.TOOL_DISPATCH
    client = app.app.test_client()
    res = client.get("/api/activity", headers={"Authorization": "Bearer admin-test-token"})
    assert res.status_code == 200
    body = res.get_json()
    assert all("severity" in e for e in body["events"]), body
    res = client.get("/api/activity?severity=CRITICAL", headers={"Authorization": "Bearer admin-test-token"})
    assert res.status_code == 200
    assert len(res.get_json()["events"]) == 1

    print("OK: classify_event_severity follows its real (event_type, status) rules, "
          "get_recent_activity attaches a real per-event severity and honors the severity "
          "filter (case-insensitive, rejects an unknown value), and both the chat tool and "
          "GET /api/activity serve it.")


if __name__ == "__main__":
    demo()
