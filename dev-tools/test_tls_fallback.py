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

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "odin-backend"))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "fake_pkgs"))

os.environ["ODIN_API_TOKEN"] = "admin-test-token"

import app  # noqa: E402


def demo():
    # Neither set -> plain HTTP.
    assert app._resolve_ssl_context(None, None) is None
    assert app._resolve_ssl_context("", "") is None

    # Only one set -> still plain HTTP, not a broken half-state.
    assert app._resolve_ssl_context("/app/tls/odin.crt", None) is None
    assert app._resolve_ssl_context(None, "/app/tls/odin.key") is None
    assert app._resolve_ssl_context("/app/tls/odin.crt", "") is None

    # Both set -> the (cert, key) tuple Flask's ssl_context expects, whitespace stripped.
    assert app._resolve_ssl_context("/app/tls/odin.crt", "/app/tls/odin.key") == (
        "/app/tls/odin.crt", "/app/tls/odin.key",
    )
    assert app._resolve_ssl_context("  /app/tls/odin.crt  ", "  /app/tls/odin.key  ") == (
        "/app/tls/odin.crt", "/app/tls/odin.key",
    )

    # The container is served by gunicorn, whose config file restates the
    # rule (it cannot import app without starting the background schedulers
    # in gunicorn's master process). Hold the two to the same answer, and to
    # the one-worker setting the in-memory lockouts and rate limits rely on.
    import runpy
    conf_path = os.path.join(os.path.dirname(os.path.abspath(app.__file__)), "gunicorn.conf.py")
    for cert, key in ((None, None), ("/c.crt", None), (None, "/k.key"), ("/c.crt", ""), ("  /c.crt ", " /k.key  ")):
        for name, value in (("ODIN_TLS_CERT", cert), ("ODIN_TLS_KEY", key)):
            if value is None:
                os.environ.pop(name, None)
            else:
                os.environ[name] = value
        conf = runpy.run_path(conf_path)
        expected = app._resolve_ssl_context(cert, key)
        got = (conf["certfile"], conf["keyfile"]) if "certfile" in conf else None
        assert got == expected, (cert, key, got, expected)
        assert conf["workers"] == 1 and conf["worker_class"] == "gthread" and conf["threads"] >= 8, conf["workers"]
    os.environ.pop("ODIN_TLS_CERT", None)
    os.environ.pop("ODIN_TLS_KEY", None)

    print("OK: _resolve_ssl_context only enables TLS when both cert and key are configured, "
          "falls back to plain HTTP for any other combination, and strips whitespace; "
          "gunicorn.conf.py gives the same answer and stays one threaded worker.")


if __name__ == "__main__":
    demo()
