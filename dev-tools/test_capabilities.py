"""Self-check for Ultron's capability registry (get_capabilities --
master prompt sections 27-28).

Proves it's actually introspecting the live tables, not a hand-maintained
list that can drift: adding a fake tool to TOOL_DISPATCH/TOOLS at runtime
must show up in get_capabilities()'s output, and admin_only must track
BETA_ALLOWED_TOOLS exactly. Also proves the endpoint is admin-only (it
embeds MCP server info, same reasoning as /api/mcp/servers).

Run standalone from anywhere:
    python dev-tools/test_capabilities.py
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

import app  # noqa: E402


def demo():
    caps = app.get_capabilities()

    # Every real chat tool is present, with the right admin_only flag.
    names = {t["name"] for t in caps["chat_tools"]}
    assert names == set(app.TOOL_DISPATCH), names ^ set(app.TOOL_DISPATCH)
    for t in caps["chat_tools"]:
        expected_admin_only = t["name"] not in app.BETA_ALLOWED_TOOLS
        assert t["admin_only"] == expected_admin_only, t
    beta_visible = {t["name"] for t in caps["chat_tools"] if not t["admin_only"]}
    assert beta_visible == app.BETA_ALLOWED_TOOLS, beta_visible

    # It's genuinely live, not a frozen snapshot -- a tool added to TOOLS/
    # TOOL_DISPATCH after import shows up without touching get_capabilities.
    app.TOOLS.append({"name": "fake_tool_for_test", "description": "x", "input_schema": {}})
    app.TOOL_DISPATCH["fake_tool_for_test"] = lambda **_: {}
    try:
        caps2 = app.get_capabilities()
        assert any(t["name"] == "fake_tool_for_test" for t in caps2["chat_tools"])
    finally:
        app.TOOLS.pop()
        del app.TOOL_DISPATCH["fake_tool_for_test"]

    # MCP servers are embedded verbatim (same shape get_mcp_servers returns).
    assert caps["mcp"] == app.get_mcp_servers()

    # Senses/devices are present and honestly marked -- no home-lab device
    # beyond the PC claims to be connected, since none has been verified.
    assert any(s["name"] == "Infrastructure" and s["connected"] for s in caps["senses"])
    assert any(s["name"] == "Network" and not s["connected"] for s in caps["senses"])
    pc = next(d for d in caps["devices"] if d["device"] == "CyberPower PC")
    assert pc["status"] == "connected", pc
    for d in caps["devices"]:
        if d["device"] != "CyberPower PC" and d["device"] != "Pixel 7":
            assert d["status"] == "not_connected", d

    # Admin-only, not offered to beta chat.
    assert "get_capabilities" not in app.BETA_ALLOWED_TOOLS

    # REST route requires a token.
    client = app.app.test_client()
    res = client.get("/api/capabilities")
    assert res.status_code == 401, res.get_json()
    res = client.get("/api/capabilities", headers={"Authorization": "Bearer admin-test-token"})
    assert res.status_code == 200
    assert res.get_json()["chat_tools"], res.get_json()

    print("OK: get_capabilities tracks live TOOL_DISPATCH/BETA_ALLOWED_TOOLS (not a frozen list), "
          "embeds real get_mcp_servers() output, marks only the PC as connected, and "
          "GET /api/capabilities is admin-only.")


if __name__ == "__main__":
    demo()
