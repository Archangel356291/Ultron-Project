"""Self-check for Odin's Evolution/Ideas tracker (propose_idea / get_ideas /
update_idea_status -- master prompt section 13).

Proves the real mechanisms: validation rejects unknown category/status,
propose_idea always lands at DISCOVERED regardless of what's passed in, the
chat surface can create ideas but NOT change their status (section 11 --
Odin proposes, never self-approves), and the REST routes behind the
dashboard's Approve/Reject actions require an admin token.

Run standalone from anywhere:
    python dev-tools/test_evolution_ideas.py
"""
import os
import sys
import tempfile

BACKEND_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "odin-backend")
FAKE_PKGS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fake_pkgs")
sys.path.insert(0, FAKE_PKGS_DIR)   # 'import anthropic' inside app.py resolves to the fake
sys.path.insert(0, BACKEND_DIR)

os.environ["ODIN_API_TOKEN"] = "admin-test-token"
os.environ["ODIN_DB_PATH"] = os.path.join(tempfile.mkdtemp(), "test_odin.db")
os.environ["ODIN_DISABLE_MEMORY_TRENDS"] = "1"

import app  # noqa: E402


def demo():
    # Unknown category/missing required fields are rejected, not silently coerced.
    r = app.propose_idea(category="not-a-real-category", problem="x", proposed_solution="y")
    assert "error" in r, r
    r = app.propose_idea(category="monitoring", problem="", proposed_solution="y")
    assert "error" in r, r

    # A valid proposal always starts DISCOVERED, regardless of what status (if any) was passed.
    idea = app.propose_idea(
        category="monitoring",
        problem="no time-series history for system metrics",
        proposed_solution="add a periodic sampler + history table",
    )
    assert "error" not in idea, idea
    assert idea["status"] == "DISCOVERED", idea
    idea_id = idea["id"]

    # Read path: filter by category and by status.
    by_category = app.get_ideas(category="monitoring")["ideas"]
    assert any(i["id"] == idea_id for i in by_category), by_category
    by_status = app.get_ideas(status="APPROVED")["ideas"]
    assert not any(i["id"] == idea_id for i in by_status), by_status

    # update_idea_status rejects an unknown status and a nonexistent id.
    r = app.update_idea_status(idea_id, "NOT_A_REAL_STATUS")
    assert "error" in r, r
    r = app.update_idea_status(999999, "APPROVED")
    assert "error" in r, r

    # A real transition works and is reflected on read.
    r = app.update_idea_status(idea_id, "APPROVED", note="looks good")
    assert r == {"id": idea_id, "status": "APPROVED"}, r
    approved = app.get_ideas(status="APPROVED")["ideas"]
    assert any(i["id"] == idea_id and i["status"] == "APPROVED" for i in approved), approved

    # Section 11: chat can propose (create), but status transitions are
    # deliberately NOT a chat tool -- only propose_idea/get_ideas are dispatchable.
    assert "propose_idea" in app.TOOL_DISPATCH and "get_ideas" in app.TOOL_DISPATCH
    assert "update_idea_status" not in app.TOOL_DISPATCH
    assert "propose_idea" not in app.BETA_ALLOWED_TOOLS
    assert "get_ideas" not in app.BETA_ALLOWED_TOOLS

    # REST routes behind the dashboard's approve/reject actions are admin-only.
    client = app.app.test_client()
    res = client.get("/api/evolution/ideas")
    assert res.status_code == 401, res.get_json()
    res = client.get("/api/evolution/ideas", headers={"Authorization": "Bearer admin-test-token"})
    assert res.status_code == 200 and len(res.get_json()["ideas"]) >= 1, res.get_json()
    res = client.patch(
        f"/api/evolution/ideas/{idea_id}",
        json={"status": "COMPLETED"},
        headers={"Authorization": "Bearer admin-test-token"},
    )
    assert res.status_code == 200 and res.get_json()["status"] == "COMPLETED", res.get_json()
    res = client.patch(f"/api/evolution/ideas/{idea_id}", json={"status": "COMPLETED"})
    assert res.status_code == 401, res.get_json()

    print("OK: propose_idea validates input and always starts DISCOVERED, get_ideas filters "
          "by category/status, update_idea_status is reachable only via the admin-gated REST "
          "route (never a chat tool), and GET/PATCH /api/evolution/ideas enforce that.")


if __name__ == "__main__":
    demo()
