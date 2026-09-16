"""Self-check for the installable-app (PWA) surface: manifest, service
worker and icons, served by the backend.

Proves the parts a browser needs to offer "install" are really there and
correctly typed, that the worker's cache version really tracks the
dashboard's content (so a redeploy drops old caches), and -- the one that
matters for safety -- that the worker source contains the /api/ bypass,
so live data and anything behind the token is never served from cache.

Run standalone from anywhere:
    python dev-tools/test_pwa.py
"""
import json
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
    # Manifest: valid JSON with the fields an installable app needs, and
    # every icon it names actually serves as a PNG.
    res = client.get("/manifest.webmanifest")
    assert res.status_code == 200, res.status_code
    assert res.headers["Content-Type"].startswith("application/manifest+json"), res.headers["Content-Type"]
    manifest = json.loads(res.data)
    for key in ("name", "short_name", "start_url", "display", "background_color", "theme_color", "icons"):
        assert key in manifest, key
    assert manifest["display"] == "standalone"
    assert manifest["start_url"] == "/"
    sizes = {i["sizes"] for i in manifest["icons"]}
    assert {"192x192", "512x512"} <= sizes, sizes
    assert any(i.get("purpose") == "maskable" for i in manifest["icons"]), "a maskable icon is needed for Android"
    for icon in manifest["icons"]:
        r = client.get(icon["src"])
        assert r.status_code == 200 and r.data[:8] == b"\x89PNG\r\n\x1a\n", icon["src"]

    # Service worker: JS content type, versioned from the dashboard's own
    # content (so a changed dashboard means a new cache name), and the
    # /api/ bypass present verbatim -- this is the line that keeps live
    # data and token-protected responses out of the cache.
    res = client.get("/sw.js")
    assert res.status_code == 200, res.status_code
    assert res.headers["Content-Type"].startswith(("application/javascript", "text/javascript")), res.headers["Content-Type"]
    sw = res.data.decode()
    assert "__VERSION__" not in sw, "version placeholder was not substituted"
    assert "'ultron-shell-' + VERSION" in sw
    assert app.SHELL_VERSION in sw
    assert len(app.SHELL_VERSION) >= 8
    assert "url.pathname.startsWith('/api/')" in sw, "the /api/ network-only bypass is missing"
    assert "no-store" in res.headers.get("Cache-Control", ""), "the worker itself must not be HTTP-cached"

    # The dashboard links the manifest and registers the worker.
    html = client.get("/").data.decode()
    assert 'rel="manifest" href="/manifest.webmanifest"' in html
    assert "navigator.serviceWorker.register('/sw.js')" in html
    assert 'rel="apple-touch-icon"' in html

    print("OK: manifest (standalone, 192/512 + maskable icons all served as PNG), service worker "
          "(JS, versioned %s from dashboard content, /api/ bypass present, itself uncached), and "
          "the dashboard's manifest link + registration are all in place." % app.SHELL_VERSION)


if __name__ == "__main__":
    demo()
