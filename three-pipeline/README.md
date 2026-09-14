# three-pipeline (Module 5)

Shared setup for the two things that both use Three.js but are
otherwise separate deliverables — the knowledge-graph viewer (Module 6,
`3d-force-graph` on plain node/edge data) and the dashboard's hero
robotic head (Module 9/13, a Blender-built `.glb` asset). This directory
is the "set up Three.js as a project dependency once" step; it doesn't
build either feature itself.

## What's here

- **`three.module.js` + `three.core.js`** — three.js **r186** (npm
  `0.186.0`), vendored (downloaded once from `unpkg`, not loaded from a
  CDN at runtime — Module 6 asked for this to stay fully offline).
  `three.module.js` is a thin re-export wrapper; the actual
  implementation lives in `three.core.js`, which it imports via a
  relative path. **Both files are required together** — this took a
  failed smoke test to find: unpkg's own `build/` listing doesn't make
  the split obvious, and vendoring only `three.module.js` fails with a
  generic "Failed to fetch dynamically imported module" error that
  doesn't mention the missing file by name.
- **`smoke_test.html`** — proves the vendored files actually work:
  creates a real `THREE.Scene`/`WebGLRenderer`/`Mesh`, renders one
  frame. Verified live in Chrome, served over a local HTTP server (ES
  module imports are blocked under `file://` by CORS — needs an actual
  origin, `http://localhost:<port>` here). Not part of any real
  feature; delete or ignore once Module 6/9 have their own pages using
  these files for real.
- **`blender_smoke_test.py`** — proves the OTHER half of Module 5:
  Blender installed, and its headless CLI can run a `bpy` script that
  constructs geometry and exports a real, valid `.glb` (verified by
  checking the output's magic bytes, not just that a file exists). Run
  it with:
  ```
  "<blender.exe>" --background --python three-pipeline/blender_smoke_test.py
  ```
  Module 9's real script will follow this exact shape with actual head
  geometry instead of a cube.

## Prerequisites this confirmed are in place

- **Blender 5.2.1 LTS**, installed via
  `winget install --id BlenderFoundation.Blender -e`. Not on `PATH` by
  default — invoke via its full install path,
  `C:\Program Files\Blender Foundation\Blender 5.2\blender.exe`.
- **The dashboard is not React-based** (confirmed: `ultron-dashboard.html`
  is a single vanilla HTML/CSS/JS file, no build step) — so the
  roadmap's "via React Three Fiber if the project is React-based"
  clause doesn't apply. Plain Three.js, loaded as a native ES module
  (`<script type="module">`), matches the existing codebase.

## Deliberately not done here

- **Not wired into `ultron-dashboard.html`.** Module 5 is
  infrastructure setup; actually building the graph viewer (Module 6)
  or the hero head (Module 9/13) is out of scope here. Whoever picks up
  either module imports from these vendored files rather than
  re-downloading three.js.
- **No placeholder Sketchfab/Poly Haven model downloaded.** The
  roadmap's step 20 fallback is for if the Blender pipeline hits real
  trouble — it didn't; the smoke test above proves the pipeline works,
  so there's nothing to fall back from yet. If Module 9's actual head
  geometry turns out to be a bigger lift than expected, revisit this.
- **No actual robotic head or graph geometry built.** That's Module 9
  and Module 6's own work, respectively.
