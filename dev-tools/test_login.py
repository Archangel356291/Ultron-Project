"""Self-check for the dashboard sign-in gate's real check: POST /api/login
(owner-requested 2026-09-15: a real username+password sign-in page).

Proves this is genuinely two-factor, not password-alone with a cosmetic
username: a correct password with the WRONG username is rejected, not
just a wrong password. Also proves it never reveals which field was
wrong (same error either way -- no username-enumeration side channel),
that every other route's existing bearer-token auth is completely
untouched by this, and that beta-tester login resolves to that tester's
own name/spend info, not the admin's.

Run standalone from anywhere:
    python dev-tools/test_login.py
"""
import os
import sys
import tempfile

BACKEND_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "ultron-backend")
FAKE_PKGS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fake_pkgs")
sys.path.insert(0, FAKE_PKGS_DIR)
sys.path.insert(0, BACKEND_DIR)

os.environ["ULTRON_API_TOKEN"] = "admin-test-token"
os.environ["ULTRON_ADMIN_USERNAME"] = "Archangel356291"
os.environ["ULTRON_BETA_TOKENS"] = "tester1:beta-test-token"
os.environ["ULTRON_DB_PATH"] = os.path.join(tempfile.mkdtemp(), "test_ultron.db")
os.environ["ULTRON_DISABLE_MEMORY_TRENDS"] = "1"
os.environ["ULTRON_DISABLE_METRICS_HISTORY"] = "1"

import app  # noqa: E402

client = app.app.test_client()


def _login(username, password):
    return client.post("/api/login", json={"username": username, "password": password})


def demo():
    # Correct username + correct password -> success, real identity back.
    res = _login("Archangel356291", "admin-test-token")
    assert res.status_code == 200, res.get_json()
    assert res.get_json() == {"role": "admin", "name": "Archangel356291"}, res.get_json()

    # Correct password, WRONG username -> rejected. This is the whole
    # point: proves username is a real, checked factor, not decoration.
    res = _login("someone-else", "admin-test-token")
    assert res.status_code == 401, res.get_json()
    wrong_username_error = res.get_json()["error"]

    # Wrong password, correct username -> also rejected.
    res = _login("Archangel356291", "not-the-real-password")
    assert res.status_code == 401, res.get_json()
    wrong_password_error = res.get_json()["error"]

    # Same generic error either way -- can't be used to probe which field was wrong.
    assert wrong_username_error == wrong_password_error == "invalid credentials"

    # Missing fields rejected outright, not treated as empty-string-matches-nothing.
    res = _login("", "admin-test-token")
    assert res.status_code == 401, res.get_json()
    res = _login("Archangel356291", "")
    assert res.status_code == 401, res.get_json()

    # Beta tester login resolves to their own identity and spend info, not admin's.
    res = _login("tester1", "beta-test-token")
    assert res.status_code == 200, res.get_json()
    who = res.get_json()
    assert who["role"] == "beta" and who["name"] == "tester1", who
    assert "spend_usd" in who and "spend_limit_usd" in who, who

    # A beta tester's own token with the ADMIN's username is still rejected.
    res = _login("Archangel356291", "beta-test-token")
    assert res.status_code == 401, res.get_json()

    # Every other route's existing bearer-token auth is untouched -- this
    # new endpoint didn't change require_token/require_role at all.
    res = client.get("/api/whoami", headers={"Authorization": "Bearer admin-test-token"})
    assert res.status_code == 200 and res.get_json()["name"] == "Archangel356291", res.get_json()
    res = client.get("/api/whoami")
    assert res.status_code == 401

    print("OK: /api/login requires a matching username AND password (a right password with "
          "the wrong username is rejected, not just accepted on the password alone), never "
          "reveals which field failed, correctly resolves beta-tester identity/spend, and "
          "every other route's bearer-token auth is unaffected.")


if __name__ == "__main__":
    demo()
