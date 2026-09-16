"""Self-check for _resolve_ssl_context (owner-requested 2026-09-16: real
HTTPS via a Tailscale-issued cert, with a plain-HTTP fallback for local/
non-Docker dev that has no cert configured).

Proves both cert and key must be present to enable TLS -- a half-
configured state (only one of the two set) falls back to plain HTTP
rather than crashing or silently running without the other file.

Run standalone from anywhere:
    python dev-tools/test_tls_fallback.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "ultron-backend"))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "fake_pkgs"))

os.environ["ULTRON_API_TOKEN"] = "admin-test-token"

import app  # noqa: E402


def demo():
    # Neither set -> plain HTTP.
    assert app._resolve_ssl_context(None, None) is None
    assert app._resolve_ssl_context("", "") is None

    # Only one set -> still plain HTTP, not a broken half-state.
    assert app._resolve_ssl_context("/app/tls/ultron.crt", None) is None
    assert app._resolve_ssl_context(None, "/app/tls/ultron.key") is None
    assert app._resolve_ssl_context("/app/tls/ultron.crt", "") is None

    # Both set -> the (cert, key) tuple Flask's ssl_context expects, whitespace stripped.
    assert app._resolve_ssl_context("/app/tls/ultron.crt", "/app/tls/ultron.key") == (
        "/app/tls/ultron.crt", "/app/tls/ultron.key",
    )
    assert app._resolve_ssl_context("  /app/tls/ultron.crt  ", "  /app/tls/ultron.key  ") == (
        "/app/tls/ultron.crt", "/app/tls/ultron.key",
    )

    print("OK: _resolve_ssl_context only enables TLS when both cert and key are configured, "
          "falls back to plain HTTP for any other combination, and strips whitespace.")


if __name__ == "__main__":
    demo()
