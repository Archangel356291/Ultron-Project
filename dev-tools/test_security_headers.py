"""Self-check for response security headers (owner-requested 2026-09-16).

Proves the real headers land on actual responses (not just that the
function exists), and specifically that the CSP still allows what the
dashboard genuinely needs -- inline scripts/styles (no nonce/hash setup
in the HTML), Google Fonts, and connecting to an arbitrary backend origin
(the Settings -> Connection LAN/Tailscale address feature) -- so this
hardening pass didn't quietly break real functionality.

Run standalone from anywhere:
    python dev-tools/test_security_headers.py
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

client = app.app.test_client()


def demo():
    # Headers land on a real response, including an unauthenticated one --
    # security headers should apply regardless of auth outcome.
    res = client.get("/api/health")
    assert res.status_code == 200, res.get_json()
    assert res.headers["X-Content-Type-Options"] == "nosniff", dict(res.headers)
    assert res.headers["X-Frame-Options"] == "DENY", dict(res.headers)
    assert res.headers["Referrer-Policy"] == "no-referrer", dict(res.headers)
    assert "microphone=(self)" in res.headers["Permissions-Policy"], res.headers["Permissions-Policy"]
    assert "camera=()" in res.headers["Permissions-Policy"], res.headers["Permissions-Policy"]

    csp = res.headers["Content-Security-Policy"]
    # The real things the dashboard needs still work under this CSP.
    assert "script-src 'self' 'unsafe-inline'" in csp, csp  # inline <script> blocks, no nonce setup
    assert "style-src 'self' 'unsafe-inline'" in csp, csp
    # Fonts are self-hosted now (fonts/ + the /fonts/ route) -- no Google
    # Fonts origin may be allowed, or the "no third-party request" property
    # the self-hosting bought is silently gone.
    assert "font-src 'self'" in csp, csp
    assert "googleapis" not in csp and "gstatic" not in csp, csp
    assert "connect-src *" in csp, csp  # Settings -> Connection points at an arbitrary backend origin

    # The self-hosted fonts actually serve (a real woff2, not a 404), and
    # path traversal out of fonts/ is refused.
    res = client.get("/fonts/orbitron.woff2")
    assert res.status_code == 200 and res.data[:4] == b"wOF2", (res.status_code, res.data[:8])
    assert client.get("/fonts/../ultron-backend/app.py").status_code == 404
    # The real things it should still block.
    assert "object-src 'none'" in csp, csp
    assert "frame-ancestors 'none'" in csp, csp
    assert "base-uri 'self'" in csp, csp

    # Headers also apply to a 401, not just 200s -- an attacker probing
    # auth failures shouldn't get an unhardened response.
    res = client.get("/api/whoami")
    assert res.status_code == 401
    assert res.headers["X-Frame-Options"] == "DENY", dict(res.headers)

    print("OK: security headers (nosniff, frame-deny, no-referrer, a scoped Permissions-Policy, "
          "and a CSP that blocks third-party scripts/framing/base-hijack while still allowing "
          "the dashboard's real inline scripts, self-hosted fonts, and arbitrary-backend connections) "
          "land on real responses, including unauthenticated and 401 ones.")


if __name__ == "__main__":
    demo()
