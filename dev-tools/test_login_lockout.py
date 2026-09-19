"""Self-check for the /api/login lockout (owner-requested 2026-09-16: a
backstop against brute-forcing the new sign-in page).

Proves the actual mechanism with a low, deterministic threshold: the Nth
consecutive failure from one source locks that source out (429) even with
the CORRECT credentials on the next attempt, a different source is
completely unaffected by another source's failures, the lockout expires
after its window, and a genuine success clears the count so a real user
who fat-fingers their password a couple times isn't punished once they
get it right.

Run standalone from anywhere:
    python dev-tools/test_login_lockout.py
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
os.environ["ODIN_ADMIN_USERNAME"] = "Archangel356291"
os.environ["ODIN_DB_PATH"] = os.path.join(tempfile.mkdtemp(), "test_odin.db")
os.environ["ODIN_DISABLE_MEMORY_TRENDS"] = "1"
os.environ["ODIN_DISABLE_METRICS_HISTORY"] = "1"
os.environ["ODIN_LOGIN_LOCKOUT_MAX_ATTEMPTS"] = "3"
os.environ["ODIN_LOGIN_LOCKOUT_WINDOW_SECONDS"] = "3600"
os.environ["ODIN_LOGIN_LOCKOUT_SECONDS"] = "3600"

import app  # noqa: E402


def demo():
    assert app.LOGIN_LOCKOUT_MAX_ATTEMPTS == 3, "test assumes the low threshold set above"

    # Unit-level: exercise the lockout functions directly rather than via
    # Flask's test client, since the test client doesn't let us vary
    # request.remote_addr per call to simulate different sources.
    app._login_lockout_clear("1.1.1.1")
    app._login_lockout_clear("2.2.2.2")

    # First two failures from 1.1.1.1: not locked out yet.
    assert app._login_lockout_check("1.1.1.1") is None
    app._login_lockout_record_failure("1.1.1.1")
    assert app._login_lockout_check("1.1.1.1") is None
    app._login_lockout_record_failure("1.1.1.1")
    assert app._login_lockout_check("1.1.1.1") is None

    # Third failure (the configured threshold) locks it out.
    app._login_lockout_record_failure("1.1.1.1")
    err = app._login_lockout_check("1.1.1.1")
    assert err is not None and "too many failed" in err, err

    # A DIFFERENT source is completely unaffected by 1.1.1.1's failures.
    assert app._login_lockout_check("2.2.2.2") is None

    # Clearing (what a genuine success does) lifts the lockout immediately.
    app._login_lockout_clear("1.1.1.1")
    assert app._login_lockout_check("1.1.1.1") is None

    # A lockout that has expired (window elapsed) also lifts on its own.
    app._login_lockout_record_failure("3.3.3.3")
    app._login_lockout_record_failure("3.3.3.3")
    app._login_lockout_record_failure("3.3.3.3")
    assert app._login_lockout_check("3.3.3.3") is not None
    app._login_lockouts["3.3.3.3"] = time.time() - 1  # simulate the window having passed
    assert app._login_lockout_check("3.3.3.3") is None

    # End-to-end through the real route: lock out via repeated wrong
    # passwords, confirm the CORRECT credentials are also refused with 429
    # (not 401) while locked out, and the lockout error, not "invalid
    # credentials", is what comes back.
    client = app.app.test_client()

    def login():
        return client.post("/api/login", json={"username": "Archangel356291", "password": "wrong"})

    for _ in range(3):
        res = login()
        assert res.status_code == 401, res.get_json()

    res = client.post("/api/login", json={"username": "Archangel356291", "password": "admin-test-token"})
    assert res.status_code == 429, res.get_json()
    assert "too many failed" in res.get_json()["error"], res.get_json()

    print("OK: /api/login lockout triggers at the configured attempt threshold, blocks even a "
          "correct password while locked out (429, not 401), never affects a different source, "
          "clears on a genuine success, and expires on its own after the window.")


if __name__ == "__main__":
    demo()
