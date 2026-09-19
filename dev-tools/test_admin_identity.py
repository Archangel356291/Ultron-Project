"""Self-check for ODIN_ADMIN_USERNAME (owner-requested 2026-09-15: mark the
admin's identity as "Archangel356291" instead of the generic literal
"admin" in whoami, presence, and chat_log).

Proves the override actually takes effect end-to-end -- not just that the
constant exists -- and that it's a pure display label: the real security
boundary (the token itself, via hmac.compare_digest) is untouched, and a
wrong token is still rejected regardless of what ADMIN_USERNAME is set to.

Run standalone from anywhere:
    python dev-tools/test_admin_identity.py
"""
import os
import sys
import tempfile

BACKEND_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "odin-backend")
FAKE_PKGS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fake_pkgs")
sys.path.insert(0, FAKE_PKGS_DIR)
sys.path.insert(0, BACKEND_DIR)

os.environ["ODIN_API_TOKEN"] = "admin-test-token"
os.environ["ODIN_ADMIN_USERNAME"] = "Archangel356291"
os.environ["ANTHROPIC_API_KEY"] = "fake-key-for-test"
os.environ["ODIN_DB_PATH"] = os.path.join(tempfile.mkdtemp(), "test_odin.db")
os.environ["ODIN_DISABLE_MEMORY_TRENDS"] = "1"
os.environ["ODIN_DISABLE_METRICS_HISTORY"] = "1"

import anthropic  # noqa: E402  (the fake, via sys.path above)
import app  # noqa: E402

client = app.app.test_client()


def demo():
    assert app.ADMIN_USERNAME == "Archangel356291", app.ADMIN_USERNAME

    # /api/whoami reports the real configured name, not the literal "admin".
    res = client.get("/api/whoami", headers={"Authorization": "Bearer admin-test-token"})
    assert res.status_code == 200
    who = res.get_json()
    assert who == {"role": "admin", "name": "Archangel356291"}, who

    # A wrong token is still rejected outright -- the name is cosmetic,
    # never part of the actual credential check.
    res = client.get("/api/whoami", headers={"Authorization": "Bearer not-the-real-token"})
    assert res.status_code == 401, res.get_json()

    # chat_log picks it up too (via _log_chat_turn's identity), not "admin".
    app.anthropic_client.messages.script.append(
        anthropic.Message(
            content=[anthropic.ContentBlock(type="text", text="acknowledged")],
            stop_reason="end_turn",
            usage=anthropic.Usage(input_tokens=10, output_tokens=5),
        )
    )
    res = client.post(
        "/api/chat", json={"message": "hello", "history": []},
        headers={"Authorization": "Bearer admin-test-token"},
    )
    assert res.status_code == 200, res.get_json()
    turns = app.get_chat_history()["turns"]
    assert all(t["identity"] == "Archangel356291" for t in turns), turns

    print("OK: ODIN_ADMIN_USERNAME overrides the admin identity in /api/whoami and chat_log, "
          "while the actual token check is untouched -- a wrong token is still 401'd "
          "regardless of the configured name.")


if __name__ == "__main__":
    demo()
