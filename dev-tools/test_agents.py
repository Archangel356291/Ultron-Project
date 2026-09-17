"""Self-check for agent governance: the registry/status view, the task
lifecycle, deny-by-default tool dispatch, per-agent spend caps, Sentinel's
posture review, and the monitoring allowlist's private-host rule.

Run standalone from anywhere:
    python dev-tools/test_agents.py
"""
import json
import os
import sys
import tempfile
import urllib.error

BACKEND_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "ultron-backend")
FAKE_PKGS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fake_pkgs")
sys.path.insert(0, FAKE_PKGS_DIR)
sys.path.insert(0, BACKEND_DIR)

DATA_DIR = tempfile.mkdtemp()
os.environ["ULTRON_API_TOKEN"] = "admin-test-token-with-32-characters!!"
os.environ["ULTRON_BETA_TOKENS"] = "tester:beta-test-token"
os.environ["ANTHROPIC_API_KEY"] = "fake-key-for-test"
os.environ["ULTRON_DB_PATH"] = os.path.join(DATA_DIR, "ultron.db")
os.environ["ULTRON_DISABLE_MEMORY_TRENDS"] = "1"
os.environ["ULTRON_DISABLE_METRICS_HISTORY"] = "1"
os.environ["ULTRON_SENTINEL_INTERVAL_SECONDS"] = "0"
os.environ["ULTRON_LEARN_INLINE"] = "1"
os.environ["ULTRON_AGENT_DAILY_USD"] = "learner=0.000001,ultron=100"
os.environ["ULTRON_ALLOWED_ORIGIN"] = "*"
os.environ.pop("ULTRON_TLS_CERT", None)
os.environ.pop("ULTRON_TLS_KEY", None)
os.environ["ULTRON_MONITOR_TARGETS"] = os.path.join(DATA_DIR, "monitoring-targets.json")
os.environ["ULTRON_TAILNET_SUFFIX"] = "tailc5bde9.ts.net"
json.dump({"targets": [
    {"name": "local ok", "type": "http", "target": "http://host.docker.internal:8096/health"},
    {"name": "local down", "type": "http", "target": "http://127.0.0.1:9/nothing"},
    {"name": "public", "type": "http", "target": "https://example.com/"},
    {"name": "tailnet ok", "type": "http", "target": "https://jellyfin.tailc5bde9.ts.net/health"},
    {"name": "lookalike", "type": "http", "target": "https://evil.tailc5bde9.ts.net.attacker.com/"},
]}, open(os.environ["ULTRON_MONITOR_TARGETS"], "w"))

import anthropic  # noqa: E402
import app  # noqa: E402

client = app.app.test_client()
ADMIN = {"Authorization": "Bearer admin-test-token-with-32-characters!!"}
BETA = {"Authorization": "Bearer beta-test-token"}
calls = app.anthropic_client.messages.calls
script = app.anthropic_client.messages.script


def _text(text="ok", out=5):
    return anthropic.Message(content=[anthropic.ContentBlock(type="text", text=text)],
                             stop_reason="end_turn", usage=anthropic.Usage(input_tokens=5, output_tokens=out))


def demo():
    # Registry + status: every agent has a role, tools and forbidden list; admin-only.
    res = client.get("/api/agents", headers=ADMIN)
    assert res.status_code == 200, res.get_json()
    agents = {a["agent"]: a for a in res.get_json()["agents"]}
    assert {"ultron", "sentinel", "scout", "learner", "engineering", "docker_orchestrator", "tailscale_topology",
            "pihole_guard", "test_automation", "security_auditor", "log_coordinator", "context_manager",
            "knowledge_synthesizer", "slack_communicator", "discord_gateway", "developer", "research",
            "frontend_designer", "market_analyst", "stats_tracker", "ethical_hacking"} == set(agents), set(agents)
    for a in agents.values():
        assert a["role"] and a["tools"] and a["forbidden"] and a["scope"], a
    assert agents["test_automation"]["health"].startswith("standby (Claude Code")
    # Every Claude Code specialist has a definition file the session can invoke.
    agents_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".claude", "agents")
    for name, meta in app.AGENT_REGISTRY.items():
        if meta["kind"] == "claude-code":
            path = os.path.join(agents_dir, name.replace("_", "-") + ".md")
            assert os.path.isfile(path), path
            head = open(path, encoding="utf-8").read(2000)
            assert head.startswith("---\nname: " + name.replace("_", "-")) and "\ntools:" in head, path

    # Scribe's runtime half: redacted, capped, only real container names.
    app.docker_ps = lambda: ([{"name": "ultron-searxng", "image": "x", "status": "Up", "running_for": "", "state": "running"}], None)
    r = app.get_container_logs(container="not-a-container")
    assert "no container named" in r["error"] and r["containers"] == ["ultron-searxng"], r
    assert app.get_container_logs()["error"].startswith("container is required")
    # Built from parts so no realistic-looking secret sits in this file
    # (the repo's gitleaks pre-commit hook rightly refuses those).
    fake_key = "sk-" + "fake" + "0" * 16
    fake = ("INFO Authorization: Bearer abcdefghijklmnop123\nWARN api_key=" + fake_key + "\n"
            "password: hunter2secret\ntskey-auth-XXXXXXXXXXXX ok\nnormal line\n")
    class _Res:
        stdout, stderr = fake, ""
    app.subprocess.run = lambda *a, **k: _Res()
    r = app.get_container_logs(container="ultron-searxng", lines=999)
    assert r["lines_requested"] == app.LOG_TAIL_MAX_LINES
    assert "abcdefghijklmnop123" not in r["log"] and fake_key not in r["log"] and "hunter2secret" not in r["log"] and "XXXXXXXXXXXX" not in r["log"], r["log"]
    assert "[redacted]" in r["log"] and "normal line" in r["log"], r["log"]
    assert app._redact("x" * 10) == "x" * 10
    assert "get_container_logs" in app.TOOL_DISPATCH and "get_container_logs" not in app.LITE_ALLOWED_TOOLS

    # read_page: https-only, public hosts only, readable text out of HTML,
    # capped, and every failure a plain error.
    assert "read_page" in app.TOOL_DISPATCH and "read_page" not in app.LITE_ALLOWED_TOOLS
    for bad in ("http://example.org/", "https://user:pw@example.org/", "https://192.168.0.5/", "https://pihole.tailc5bde9.ts.net/admin/",
                "https://localhost/", "https://host.docker.internal/", ""):
        assert "error" in app.read_page(url=bad), bad
    html = ("<html><head><title> Docs &amp; Guide </title><script>evil()</script><style>x{}</style></head>"
            "<body><nav>Menu Menu</nav><h1>Install</h1><p>Run <code>pip install x</code> first.</p>"
            "<h2>Config</h2><ul><li>one</li><li>two</li></ul><footer>foot</footer></body></html>")
    class _R:
        status = 200
        headers = {"Content-Type": "text/html; charset=utf-8"}
        def read(self, n=None): return html.encode()
        def __enter__(self): return self
        def __exit__(self, *a): return False
    real_urlopen = app.urllib.request.urlopen
    app.urllib.request.urlopen = lambda req, timeout=None: _R()
    try:
        r = app.read_page(url="https://docs.example.org/guide")
        assert r["title"] == "Docs & Guide", r
        assert "# Install" in r["text"] and "## Config" in r["text"] and "pip install x" in r["text"], r["text"]
        assert "evil()" not in r["text"] and "Menu" not in r["text"] and "foot" not in r["text"], r["text"]
        assert r["truncated"] is False and "unverified" in r["note"]
        r = app.read_page(url="https://docs.example.org/guide", max_chars=500)
        assert r["chars"] <= 500
        class _Bin(_R):
            headers = {"Content-Type": "application/pdf"}
        app.urllib.request.urlopen = lambda req, timeout=None: _Bin()
        assert "not a readable page" in app.read_page(url="https://docs.example.org/x.pdf")["error"]
    finally:
        app.urllib.request.urlopen = real_urlopen
    assert agents["sentinel"]["health"] == "disabled"  # interval 0 in tests
    assert agents["learner"]["daily_cap_usd"] == 0.000001
    assert client.get("/api/agents", headers=BETA).status_code == 403
    assert "get_agent_status" in app.TOOL_DISPATCH

    # Task lifecycle.
    r = client.post("/api/agents/tasks", json={"agent": "nobody", "objective": "x"}, headers=ADMIN)
    assert r.status_code == 400
    r = client.post("/api/agents/tasks", json={
        "agent": "engineering", "objective": "Add a test for the agents card", "risk_level": "low",
        "acceptance_criteria": "test passes", "authorized_scope": "this repo", "allowed_tools": ["dev-tools tests"],
    }, headers=ADMIN)
    assert r.status_code == 201, r.get_json()
    task = r.get_json()
    uid = task["task_uid"]
    assert task["status"] == "created" and task["approval_status"] == "not_required" and task["allowed_tools"] == ["dev-tools tests"]
    # Duplicate open objective -> 409.
    r = client.post("/api/agents/tasks", json={"agent": "engineering", "objective": "Add a test for the agents card"}, headers=ADMIN)
    assert r.status_code == 409 and r.get_json()["duplicate_of"] == uid, r.get_json()
    # Illegal jump.
    r = client.patch(f"/api/agents/tasks/{uid}", json={"status": "completed", "evidence": "x"}, headers=ADMIN)
    assert r.status_code == 400 and "cannot move" in r.get_json()["error"]
    for s in ("assigned", "acknowledged", "in_progress"):
        assert client.patch(f"/api/agents/tasks/{uid}", json={"status": s}, headers=ADMIN).status_code == 200, s
    # Completion needs evidence.
    r = client.patch(f"/api/agents/tasks/{uid}", json={"status": "completed"}, headers=ADMIN)
    assert r.status_code == 400 and "evidence" in r.get_json()["error"]
    r = client.patch(f"/api/agents/tasks/{uid}", json={"status": "completed", "evidence": "test_agents.py OK; 1 file"}, headers=ADMIN)
    assert r.status_code == 200 and r.get_json()["status"] == "completed"
    # Terminal state is terminal.
    assert client.patch(f"/api/agents/tasks/{uid}", json={"status": "in_progress"}, headers=ADMIN).status_code == 400
    # High risk needs approval before it starts.
    r = client.post("/api/agents/tasks", json={"agent": "sentinel", "objective": "probe a new host", "risk_level": "high"}, headers=ADMIN)
    hi = r.get_json()["task_uid"]
    assert r.get_json()["approval_status"] == "pending"
    for s in ("assigned", "acknowledged"):
        client.patch(f"/api/agents/tasks/{hi}", json={"status": s}, headers=ADMIN)
    r = client.patch(f"/api/agents/tasks/{hi}", json={"status": "in_progress"}, headers=ADMIN)
    assert r.status_code == 400 and "approval" in r.get_json()["error"]
    r = client.patch(f"/api/agents/tasks/{hi}", json={"status": "in_progress", "approval_status": "approved"}, headers=ADMIN)
    assert r.status_code == 200 and r.get_json()["status"] == "in_progress"
    # Current task shows on the agent, and beta can't touch tasks.
    sent = {a["agent"]: a for a in client.get("/api/agents", headers=ADMIN).get_json()["agents"]}["sentinel"]
    assert sent["current_task"]["task_uid"] == hi
    assert client.get("/api/agents/tasks", headers=BETA).status_code == 403
    audit = [e for e in app.get_recent_activity(limit=50)["events"] if e["event_type"] == "agent_task"]
    assert len(audit) >= 7, len(audit)

    # Deny by default at dispatch: a normal admin call is offered every tool,
    # but a model naming a tool it was NOT offered (here: Economy mode asks
    # for get_repo_diff) is refused and logged as a permission event.
    script.append(anthropic.Message(
        content=[anthropic.ContentBlock(type="tool_use", id="t1", name="get_repo_diff", input={"repo": "x"})],
        stop_reason="tool_use", usage=anthropic.Usage(input_tokens=5, output_tokens=5)))
    script.append(_text())
    r = client.post("/api/chat", json={"message": "diff", "history": [], "lite": True}, headers=ADMIN)
    assert r.status_code == 200
    assert "forbidden" in calls[-1]["messages"][-1]["content"][0]["content"]
    assert any(e["event_type"] == "agent_permission" for e in app.get_recent_activity(limit=20)["events"])

    # Per-agent cap: the learner's cap is microscopic, so one logged call
    # trips it and the next learn is refused with a budget event, while chat
    # (cap $100) still works.
    script.append(_text()); script.append(_text("The owner likes tests.", out=1000))
    client.post("/api/chat", json={"message": "I like tests", "history": [], "learn": True}, headers=ADMIN)
    assert app._agent_spend_today("learner") > 0
    before = len(calls)
    script.append(_text())
    client.post("/api/chat", json={"message": "again", "history": [], "learn": True}, headers=ADMIN)
    assert len(calls) - before == 1, "learner must not be called once over its cap"
    assert any(e["event_type"] == "agent_budget" for e in app.get_recent_activity(limit=20)["events"])
    by_agent = {r["agent"]: r for r in app.get_llm_usage()["by_agent"]}
    assert "learner" in by_agent and "ultron" in by_agent, by_agent

    # Sentinel posture + monitoring allowlist. Probes are faked: the
    # "local ok" target answers, "local down" refuses, "public" must be
    # refused BEFORE any request is made.
    probed = []

    def fake_urlopen(req, timeout=None):
        probed.append(req.full_url)
        if "8096" in req.full_url or "jellyfin.tailc5bde9" in req.full_url:
            class R:
                status = 200
                def __enter__(self): return self
                def __exit__(self, *a): return False
            return R()
        raise urllib.error.URLError("connection refused")
    real = app.urllib.request.urlopen
    app.urllib.request.urlopen = fake_urlopen
    try:
        findings = app._sentinel_checks()
    finally:
        app.urllib.request.urlopen = real
    assert "posture:cors_any_origin" in findings and "posture:no_tls" in findings, findings.keys()
    assert "posture:weak_admin_token" not in findings
    assert "monitor_down:local down" in findings and findings["monitor_down:local down"][0] == "error"
    assert "monitor_refused:public" in findings, findings.keys()
    assert not any("example.com" in u for u in probed), "a public host must never be probed: " + str(probed)
    assert "monitor_down:local ok" not in findings
    # The owner's tailnet names count as private; a look-alike with the
    # suffix in the middle does not, and is never contacted.
    assert "monitor_down:tailnet ok" not in findings and "monitor_refused:tailnet ok" not in findings, findings.keys()
    assert "monitor_refused:lookalike" in findings, findings.keys()
    assert not any("attacker.com" in u for u in probed), probed
    assert app._is_private_host("pihole.tailc5bde9.ts.net") and not app._is_private_host("tailc5bde9.ts.net")
    assert not app._is_private_host("a.b.tailc5bde9.ts.net")

    print("OK: agent registry/status (admin-only), task lifecycle (transitions, evidence, high-risk approval, "
          "dedup, audit), deny-by-default tool dispatch with a permission event, per-agent daily caps with a "
          "budget event, Sentinel posture findings, and a monitoring allowlist that never probes a public host.")


if __name__ == "__main__":
    demo()
