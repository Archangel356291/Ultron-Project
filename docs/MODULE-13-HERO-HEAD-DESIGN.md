# Dashboard hero visual redesign (Module 13) — v1

Replaces the dashboard's central orange particle sphere with an original,
procedurally-built robotic AI head, rendered live via Three.js on top of
Module 5's vendored pipeline. Per the roadmap's own IP requirement: this
is an original design built from primitive geometric forms (beveled
boxes, a low-poly faceted sphere), not a trace or reproduction of the
reference image or any existing character. No copyrighted asset was used
or referenced during construction.

## What changed, and what didn't

**Touched:** only the hero centerpiece (`.sphere-wrap`'s contents) and
its immediate glow. `odin-backend/app.py` gained one new static-asset
route; `odin-backend/Dockerfile` and `.dockerignore` gained one new
allowlisted directory.

**Explicitly untouched, per the roadmap's own preservation list:**
ULTRON AI branding, "ULTRON STANDING BY"/"ULTRON ONLINE", the tagline,
"LEARN ADAPT SOLVE EVOLVE", hero layout, chat interface, mode pills,
system status panel, CPU/network monitoring, every backend/API/auth
route, all other page sections. `--oxide` (the site's orange accent)
is untouched everywhere outside the hero centerpiece itself — the nav
logo, active states, buttons, and mode pills are still orange. Only
`.sphere-glow`'s two color stops moved from orange to red.

## Pipeline: reusing Module 5, not rebuilding it

Module 5 vendored `three.module.js` + `three.core.js` (r186) and proved
the Blender → `.glb` → Three.js mechanism with placeholder geometry.
Module 13 is that mechanism, for real:

- **`three-pipeline/build_hero_head.py`** — the actual Blender bpy
  script (`blender_smoke_test.py`'s real successor), run headlessly:
  `"<blender.exe>" --background --python three-pipeline/build_hero_head.py`.
  Outputs `hero_head.glb` (the deliverable) and `hero_head_preview.png`
  (a rendered preview — see "Real bugs" below for why this mattered).
- **`three-pipeline/loaders/GLTFLoader.js`** + its two transitive
  dependencies (`utils/BufferGeometryUtils.js`, `utils/SkeletonUtils.js`)
  — newly vendored at the exact same r186 version, in the nested layout
  they ship in upstream (so their own relative imports between each
  other resolve unmodified). Not previously needed — Module 5 vendored
  the core renderer, not a model loader.
- **An import map** (`odin-dashboard.html`'s `<head>`) resolves
  GLTFLoader's own `import ... from 'three'` (a bare specifier) to the
  vendored `three.module.js`, so none of the three downloaded files
  needed hand-patching — verified working via
  `three-pipeline/gltf_smoke_test.html` before touching the live
  dashboard at all, same "prove the mechanism first" discipline as
  Module 5's own smoke tests.

## New: a static-asset route, because the dashboard wasn't just one file anymore

The Docker image only ever shipped `odin-backend/` +
`odin-dashboard.html` (see the Dockerfile's own comment). Module 13
needs Three.js + a `.glb` served over HTTP too — an ES module import
needs a real origin, the same reason the dashboard itself moved off
`file://` earlier in this project. New route:

```python
@app.route("/three-pipeline/<path:filename>")
def three_pipeline_asset(filename):
    return send_from_directory(THREE_PIPELINE_DIR, filename)
```

Unauthenticated, like `/` itself — nothing served here is a secret, and
`send_from_directory` already refuses path traversal (verified in
`dev-tools/test_hero_assets_route.py`, both a plain `../` and a
percent-encoded one). `Dockerfile` gained `COPY three-pipeline/
three-pipeline/`; `.dockerignore`'s allowlist gained `!three-pipeline/`
plus explicit blocks for everything under it that isn't actually fetched
at runtime (the Blender script, smoke-test HTML pages, the render
preview) — verified by building the image and listing its contents:
only `hero_head.glb`, `three.module.js`, `three.core.js`,
`loaders/GLTFLoader.js`, and the two `utils/*.js` files made it in.

## The geometry: three failed renders before one that reads as a head

Not assumed to look right from the code alone — each version was
actually rendered (via `build_hero_head.py`'s Eevee preview pass) and
visually inspected before moving on:

1. **First pass**: beveled boxes for every part (skull, forehead, cheek,
   jaw, visor), positioned by hand-computed offsets. Rendered as
   scattered, disconnected floating primitives — nothing overlapped.
   Root cause, found by re-deriving the math: `primitive_cube_add(size=1.0)`
   already creates a unit-extent cube, so `obj.scale = size/2` (my first
   version) rendered every single part at **half** its intended
   dimensions while every position offset assumed full size.
2. **Second pass**: fixed the scale bug — parts connected, but the whole
   thing read as a server tower / mini-fridge, not a head. A beveled box
   stays box-shaped in silhouette no matter how much bevel is added;
   bevel adds seam detail, not roundness.
3. **Third pass**: replaced the skull's base primitive with a **low-poly
   faceted UV sphere** (`segments=9, ring_count=6`) instead of a beveled
   box. This is the actual fix — a sphere gives the tapering, rounded
   silhouette a head needs, while the low vertex count keeps it faceted
   and angular rather than smooth/organic, satisfying "clearly
   artificial" without needing a box's straight edges to do it. Jaw
   still floated below with a visible gap (an overlap math error,
   fixed by moving it up and increasing its size).

The working design: a faceted sphere skull (narrow, tall — "narrow
mechanical face," not a wide panel), three stepped forehead plates
overlapping its upper-front, two mirrored cheek plates overlapping its
sides, a narrower jaw overlapping its lower-front (the skull→jaw taper
is what makes it read as a head rather than a box-on-a-box), and one
narrow emissive visor strip. Every part is deliberately sized to overlap
its neighbor's volume, not merely touch it — that overlap is what reads
as "one armored object" instead of "assembled parts."

**Materials**: three dark neutral metals (Gunmetal, DarkChrome, Graphite
— roughness 0.25–0.55, metallic 1.0, all "avoid full gloss") plus one
emissive crimson (`(1.0, 0.06, 0.09)`, strength ~3) on the visor alone —
"majority of the head stays black/graphite/dark chrome, not red."

## Runtime: what the Three.js side actually does

- **Real scene lights** (ambient + a white key + a dim red-tinted rim) —
  the glTF-exported plate materials are PBR (`MeshStandardMaterial`),
  unlit without them; only the visor is self-lit via its own emission.
- **Auto-rotation**, slow (`0.008 rad/frame`), skipped entirely under
  `prefers-reduced-motion`.
- **Visor pulse**: `emissiveIntensity` driven by a slow sine wave via
  `THREE.Timer` (not the deprecated `THREE.Clock` — caught as a console
  deprecation warning during live testing and fixed before merging, not
  left in).
- **CPU-driven intensity** (step 48, optional): `window.__heroSetCpu(pct)`,
  called from the existing `fetchStatus()` right where it already writes
  `#core-pct`. `>90%` and `>70%` nudge the visor's intensity multiplier
  up slightly. No existing shared "system state" machine to reuse was
  found (`.val.warn` elsewhere is specific to the updates-pending row),
  so this stays a small, local threshold rather than inventing one.
- **Cursor parallax** (step 53): mouse-only, capped small (±0.14/±0.08
  rad), skipped under reduced-motion, never attached to anything that
  could intercept chat/button/keyboard events.
- **Offline dimming**: reuses the *exact* existing mechanism — `setTopbar()`
  already toggled `.offline` on `#sphere-wrap`; a new CSS rule
  (`.sphere-wrap.offline #hero-canvas{ filter:grayscale(0.6) brightness(0.7); }`)
  targets the canvas the same way the old rule targeted the SVG core.
  Zero new JS needed for this.
- **`prefers-reduced-motion`**: renders exactly one static frame, no RAF
  loop scheduled at all — not just a slower loop. Head and CPU badge
  stay visible; rotation, pulse, and parallax are all skipped.
- **Page Visibility**: the RAF loop cancels when `document.hidden` and
  resumes on `visibilitychange` — found genuinely necessary during live
  testing, not theoretical (see bugs below).
- **Failure modes**: no WebGL, a failed `.glb` fetch, or any renderer
  construction error all fail silently — the CSS glow stays as the only
  hero visual, nothing else on the page is affected. A hero-visual
  problem must never break the rest of the dashboard.

## Real bugs found live — not assumed to work

All of these were caught by actually loading the live dashboard in
Chrome and checking console/network/pixels, not by reading the code and
deciding it looked right:

1. **`ResizeObserver` didn't fire reliably.** Directly tested (a fresh
   observer on `#sphere-wrap`, resized via script) — zero callbacks
   over 500ms. Whether that's specific to the test harness or a real
   gap, the dashboard's actual responsive breakpoints are viewport-width
   media queries anyway, so a `window.addEventListener('resize', ...)`
   was added as a **guaranteed** fallback, not an else-branch — both are
   now always attached.
2. **A resize while the render loop was paused left the canvas blank.**
   `renderer.setSize()` clears the canvas's drawing buffer; if nothing
   is actively re-rendering (loop paused for `document.hidden`, or the
   reduced-motion one-shot render already happened), nothing repaints
   it. Fixed: `sizeToContainer()` now calls `renderFrame()` directly,
   so a resize always redraws immediately regardless of loop state.
3. **A temporal-dead-zone crash, shipped for one build.** Fixing bug #2
   made `sizeToContainer()` call `renderFrame()`, which reads `cpuBoost`/
   `timer`/`parallaxX`/`parallaxY` — all declared with `let`/`const`
   *further down* the same function, after `sizeToContainer()`'s first
   (immediate) call. That's a `ReferenceError: Cannot access '...'
   before initialization` on every single page load, silently aborting
   the rest of `initHero()` (no resize listeners, no render loop, blank
   canvas) with the error caught by the outer `try/catch` pattern only
   in the sense that it didn't crash the *page* — it just meant nothing
   rendered. Caught via `read_console_messages`, not assumed absent.
   Fixed by moving every piece of render-loop state above every function
   that reads it, before any of those functions are first called.
4. **`THREE.Clock` is deprecated in r186** (a real console warning, not
   an error) — swapped for `THREE.Timer` (`.update()` + `.getElapsed()`)
   before merging, rather than shipping a warning.

## Testing (step 56)

- **Visual**: the Blender preview render caught two genuinely bad
  geometry iterations before the third one shipped (see above) — not
  claimed to look right without looking.
- **Functional, live in Chrome**: head renders and rotates; visor pulses
  red; CPU badge keeps updating from the same live `/api/status` poll it
  always used; section navigation (Home → AI Assistant → Home) survives
  without breaking the WebGL context or the separate brain-canvas
  feature; offline dimming verified by toggling the class directly.
- **Responsive**: verified by resizing `#sphere-wrap` itself and
  confirming the canvas's drawing buffer tracks it (the window-level
  resize path, since the browser automation environment used for testing
  couldn't itself trigger a true viewport resize).
- **Technical**: console clean after fixes (checked after a hard reload,
  not a stale buffer — the TDZ crash bug above was initially *missed*
  by checking a console buffer that still held pre-fix messages; caught
  properly once the buffer was cleared and the page reloaded fresh).
  Full existing Python test checkpoint re-run clean, plus the new
  `dev-tools/test_hero_assets_route.py`.
- **Accessibility**: `prefers-reduced-motion` handling verified by code
  review (the automation environment couldn't toggle the OS-level media
  feature to test live) — every animation branch (parallax listener,
  rotation, pulse, RAF scheduling) is gated on the same `reducedMotion`
  constant, read once at module load.

## Known limitations — not solved this round

- **`prefers-reduced-motion` wasn't verified live**, only by code
  review, for the reason above. The logic is straightforward enough
  (one boolean, checked consistently) that this is a reasonable but not
  absolute confidence level.
- **No manual visual regression test.** The Blender preview render is a
  one-time visual sanity check at build time, not an automated
  "does the head still look right" gate — a future geometry change could
  still silently regress the look. Matches this project's existing bar
  for anything purely visual (the dashboard's CSS has no visual
  regression suite either).
- **No LOD or mobile-specific geometry simplification.** The head is
  low-poly by design (7 mesh objects, faceted primitives), so this
  hasn't been a measured problem, but it also hasn't been measured on
  an actual low-end device.
- **The optional HUD ring (step 46) wasn't built.** Explicitly optional
  in the brief; the visor's pulse alone was judged sufficient accent for
  v1 given effort already spent getting the base geometry right.
