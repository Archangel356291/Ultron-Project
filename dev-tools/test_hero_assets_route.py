"""Self-check for Module 13's /three-pipeline/<file> route -- the piece of
the hero-head feature that's actually unit-testable without a browser
(the Three.js/WebGL rendering itself is verified live in Chrome, the same
way Module 5/6's smoke tests are -- see three-pipeline/README.md).

Proves the real thing a route like this needs to get right: serves an
existing vendored file, 404s cleanly for one that doesn't exist, and
Werkzeug's own path-traversal guard actually refuses a "../" escape rather
than assuming send_from_directory is safe just because it's a stdlib-ish
helper.

Run standalone from anywhere:
    python dev-tools/test_hero_assets_route.py
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

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def demo():
    client = app.app.test_client()

    # A real vendored file the dashboard actually loads must be reachable,
    # unauthenticated -- same reasoning as the "/" dashboard route itself.
    res = client.get("/three-pipeline/three.module.js")
    assert res.status_code == 200, res.status_code
    assert res.data.startswith(b"/**") or b"THREE" in res.data[:2000], \
        "response doesn't look like three.module.js"

    res2 = client.get("/three-pipeline/loaders/GLTFLoader.js")
    assert res2.status_code == 200, res2.status_code

    res3 = client.get("/three-pipeline/hero_head.glb")
    assert res3.status_code == 200, res3.status_code
    assert res3.data[:4] == b"glTF", "hero_head.glb doesn't start with the glTF magic bytes"

    # A file that genuinely doesn't exist 404s, not a 500 or a silent
    # empty-body 200.
    res4 = client.get("/three-pipeline/does-not-exist.js")
    assert res4.status_code == 404, res4.status_code

    # Path traversal: a "../" must not escape three-pipeline/ to serve an
    # arbitrary repo file (e.g. app.py itself, or worse, something outside
    # the repo entirely). Flask/Werkzeug's own routing normalizes this
    # before send_from_directory ever sees it -- assert the real behavior,
    # not just trust that it's "supposed to" be safe.
    res5 = client.get("/three-pipeline/../ultron-backend/app.py")
    assert res5.status_code in (403, 404), \
        f"path traversal should be refused, got {res5.status_code}"
    res6 = client.get("/three-pipeline/..%2f..%2fultron-backend%2fapp.py")
    assert res6.status_code in (403, 404), \
        f"encoded path traversal should be refused, got {res6.status_code}"

    print("OK: /three-pipeline/<file> serves the real vendored Three.js + hero_head.glb, "
          "404s for a missing file, and refuses path traversal (plain and percent-encoded).")


if __name__ == "__main__":
    demo()
