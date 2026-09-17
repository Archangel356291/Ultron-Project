"""Self-check for Sentinel, the zero-token security watchdog.

Drives _sentinel_run_once() directly (the thread is disabled with
ULTRON_SENTINEL_INTERVAL_SECONDS=0) against controlled inputs and proves
the mechanism: a stopped container and an active lockout each produce
exactly one activity-log entry at the right status, a second pass with
nothing changed logs nothing, a cleared finding logs once as success,
lockouts classify as CRITICAL, and the summary is reachable as both the
admin-only route and the chat tool.

Run standalone from anywhere:
    python dev-tools/test_sentinel.py
"""
import os
import sys
import tempfile
import time

BACKEND_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "ultron-backend")
FAKE_PKGS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fake_pkgs")
sys.path.insert(0, FAKE_PKGS_DIR)
sys.path.insert(0, BACKEND_DIR)

os.environ["ULTRON_API_TOKEN"] = "admin-test-token-with-32-characters!!"
os.environ["ULTRON_BETA_TOKENS"] = "tester:beta-test-token"
os.environ["ULTRON_DB_PATH"] = os.path.join(tempfile.mkdtemp(), "test_ultron.db")
os.environ["ULTRON_DISABLE_MEMORY_TRENDS"] = "1"
os.environ["ULTRON_DISABLE_METRICS_HISTORY"] = "1"
os.environ["ULTRON_SENTINEL_INTERVAL_SECONDS"] = "0"
# A clean posture, so this test's finding sets stay about lockouts,
# containers and CVEs (posture itself is covered by test_agents.py).
os.environ["ULTRON_ALLOWED_ORIGIN"] = "https://dashboard.test"
os.environ["ULTRON_TLS_CERT"] = "/tmp/fake.crt"
os.environ["ULTRON_TLS_KEY"] = "/tmp/fake.key"

import app  # noqa: E402

client = app.app.test_client()
ADMIN = {"Authorization": "Bearer admin-test-token-with-32-characters!!"}
BETA = {"Authorization": "Bearer beta-test-token"}


def _sentinel_events():
    return [e for e in app.get_recent_activity(limit=50)["events"] if e["event_type"] == "sentinel"]


def demo():
    assert app.SENTINEL_INTERVAL_SECONDS == 0, "test must run with the thread disabled"
    assert "get_threat_summary" in app.TOOL_DISPATCH
    assert any(t["name"] == "get_threat_summary" for t in app.TOOLS)

    # Controlled world: one stopped container, no lockouts, empty CVE cache.
    world = {"containers": [
        {"name": "ultron-backend", "image": "x", "status": "Up 2 hours", "running_for": "2 hours ago", "state": "running"},
        {"name": "jellyfin", "image": "y", "status": "Exited (137) 3 minutes ago", "running_for": "", "state": "stopped"},
    ]}
    app.docker_ps = lambda: (world["containers"], None)
    app._cve_scan_cache.clear()
    app._login_lockouts.clear()
    app._login_failures.clear()

    # Pass 1: the stopped container is a new finding -> one warning logged.
    findings = app._sentinel_run_once()
    assert set(findings) == {"container_down:jellyfin"}, findings
    events = _sentinel_events()
    assert len(events) == 1 and events[0]["status"] == "warning" and "jellyfin" in events[0]["summary"], events

    # Pass 2: nothing changed -> nothing new logged (no polling noise).
    app._sentinel_run_once()
    assert len(_sentinel_events()) == 1, _sentinel_events()

    # A lockout appears -> one error-level finding, classified CRITICAL.
    app._login_lockouts["203.0.113.9"] = time.time() + 900
    findings = app._sentinel_run_once()
    assert "lockout:203.0.113.9" in findings and findings["lockout:203.0.113.9"][0] == "error", findings
    events = _sentinel_events()
    assert len(events) == 2 and events[0]["status"] == "error", events
    assert app.classify_event_severity("sentinel", "error") == "CRITICAL"
    assert app.classify_event_severity("sentinel", "warning") == "IMPORTANT"

    # Route: admin sees the live summary; a beta tester is refused with a
    # 403 (a real identity, wrong scope -- require_token's own convention),
    # no token at all with a 401.
    res = client.get("/api/security/threats", headers=ADMIN)
    assert res.status_code == 200, res.get_json()
    summary = res.get_json()
    assert summary["enabled"] is False and summary["active_count"] == 2, summary
    assert {f["key"] for f in summary["active_findings"]} == {"container_down:jellyfin", "lockout:203.0.113.9"}
    assert summary["last_run"] and summary["runs"] == 3, summary
    assert client.get("/api/security/threats", headers=BETA).status_code == 403
    assert client.get("/api/security/threats").status_code == 401

    # Both problems clear -> each cleared once, as success, and the
    # summary is empty again.
    world["containers"][1]["state"] = "running"
    app._login_lockouts.clear()
    findings = app._sentinel_run_once()
    assert findings == {}, findings
    events = _sentinel_events()
    assert len(events) == 4, events
    assert all(e["status"] == "success" for e in events[:2]) and all("cleared" in e["summary"] for e in events[:2]), events
    assert app.get_threat_summary()["active_count"] == 0

    # Critical CVEs from a cached scan surface too; high-only does not.
    app._cve_scan_cache["img:1"] = {"data": {"by_severity": {"critical": 2, "high": 5}}, "scanned_at": time.time()}
    app._cve_scan_cache["img:2"] = {"data": {"by_severity": {"critical": 0, "high": 5}}, "scanned_at": time.time()}
    findings = app._sentinel_run_once()
    assert set(findings) == {"cve_critical:img:1"} and findings["cve_critical:img:1"][0] == "error", findings
    app._cve_scan_cache.clear()
    app._sentinel_run_once()

    print("OK: Sentinel logs each new finding once at its status (stopped container -> warning, "
          "lockout -> error/CRITICAL, critical CVEs -> error), logs nothing when nothing changed, "
          "logs a cleared finding once as success, and exposes the live summary admin-only and as a chat tool.")


if __name__ == "__main__":
    demo()
