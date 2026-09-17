# Home dashboard visual redesign (Module 14) — v1

A visual/UX overhaul of the Home screen only, per the user's reference
image (a dark-navy/cyan HUD with an orange/gold holographic AI core).
Scoped deliberately: no backend, auth, API, or other-section changes —
`ultron-dashboard.html` is the only file this touched.

## Audit correction, up front

The request described "the current bright blue/green digital visual."
That's never existed in this project. Before this pass, the hero
centerpiece was Module 13's dark-chrome robotic head with a red visor
(built the same night), and before that, an orange/amber particle
sphere. There is also no WebSocket anywhere in this codebase — every
live value on the dashboard comes from REST polling
(`setInterval` + `fetchStatus()`/`fetchContainers()`/etc.). Both
corrected before any code changed, not silently assumed.

## AI core: Three.js/glTF retired, Canvas2D particle system in its place

Module 13's real, working robotic-head pipeline (Blender → `.glb` →
Three.js/GLTFLoader) was replaced, not recolored — the reference image's
brain is fundamentally a particle/filament effect, not solid lit
geometry, and a dependency-free 2D canvas gets closer to that look while
being far cheaper on a Raspberry Pi 400 (no WebGL context, no model
fetch, ~46 small draw calls a frame instead of a shaded mesh).

- **Nodes**: generated once (not per frame), biased toward the center
  via `sqrt(random())` so the shape reads as a dense energy mass, not a
  hollow ring. Each connects to 2–3 nearest neighbors, computed once, to
  form the filament mesh.
- **Traveling pulses**: small bright dots occasionally animate along a
  random edge — more often in `thinking`/`responding` states.
- **State machine** (`idle` / `listening` / `thinking` / `responding` /
  `alert`): drives pulse speed, particle activity, and color, via
  `window.__heroSetState(name)`. Wired to real events, not decorative:
  - `listening` — the existing `SpeechRecognition` `onstart`/`onend`.
  - `thinking` → `responding` → `idle` — the existing `sendChatMessage()`
    flow, around the same `postChat()` call that already drove the
    "thinking…" chat bubble.
  - `alert` — `refreshAll()`'s catch block, specifically a connection
    lost *after* having been connected (not "never configured yet,"
    which the pre-existing `.offline` CSS class already communicates
    neutrally without implying a fault).
- **Reduced Visual Mode**: a real Settings toggle (`localStorage`-backed,
  reloads to rebuild the particle graph at half the node count), on top
  of the existing `prefers-reduced-motion` handling (one static frame,
  zero animation loop) inherited from Module 13.
- **The same resize-forces-redraw fix Module 13 had to add is carried
  forward as-is** — `sizeToContainer()` calls `renderFrame()` directly,
  since a paused RAF loop (tab hidden, or a one-shot reduced-motion
  render) would otherwise leave a resized canvas blank until something
  else forced a repaint. Re-verified live this time, not just copied
  blind: the `alert` state's red color was confirmed via this exact
  mechanism (`document.hidden` was `true` in the test environment,
  pausing the RAF loop — a forced `resize` event was what actually
  revealed the color change).

`three-pipeline/hero_head.glb`, `build_hero_head.py`, and the loader
files are left in place, unreferenced by the dashboard now — Three.js +
GLTFLoader stay useful for the future graph viewer (Module 6), and
deleting them wasn't this pass's call to make unprompted.

## Color system

New tokens (`:root`): `--core-gold`, `--core-amber`, `--core-glow-a/b` —
gold/amber, reserved for the AI core specifically. `--oxide` (the
site's existing orange) is untouched and still drives the nav, buttons,
and mode pills everywhere, including on Home — this pass recolors the
*AI core and its immediate HUD* to cyan/gold, not the whole page, per
explicit scope agreement before implementation.

New `.hud-card`/`.hud-label`/`.hud-row` classes (cyan-accented) sit
alongside the existing `.card`/`.panel-label` (orange-accented) —
deliberately separate classes, not a redefinition, so every other
section's styling is provably untouched (verified live: Security,
Systems, etc. render pixel-identical to before this pass).

## Real data audit — the actual point of this pass

Several Home rows were hardcoded fake values with no backend behind
them at all: "Raspberry Pi 400: online", "Home lab servers: online",
"Network security: enforced", "Backups: current", a fake VM count, five
fake named services (Pi-hole/Nextcloud/Jellyfin/Grafana/Home Assistant,
none of which this backend has ever queried), and a fake BTC/ETH price
ticker. All removed from Home rather than left in or "illustratively"
labeled — user's explicit call.

**What replaced them is real, verified against the actual backend:**

| New Home element | Backed by |
|---|---|
| Core Status (online/mode/AI/CPU/memory) | `/api/status`, same poll that already drove the old CPU badge |
| System Telemetry (containers/updates/power/storage) | `/api/status`, `/api/systems`, `/api/storage` — storage is a new hook into the *existing* `fetchStorage()`, not a new endpoint |
| Home lab overview (container ring, Pi host + uptime) | Same `/api/status` + `/api/systems` data the old fake-augmented version partially already used |
| Security (auth method, audit trail, link to real scan) | Structural facts (Bearer-token auth is how every route already works) + a link to the Security section's real, already-existing auth log/CVE scan — no new claims |
| Human Oversight / Approval System | The existing preview-then-confirm confirm-token mechanism (`/api/actions/backup`, `/api/actions/deploy-container`) — a permanent architectural property, not a live-polled value, so static "armed" text is honest, not fabricated |

**What the request asked for that still doesn't exist anywhere in this
backend, so wasn't added**: network download/upload/latency, and
per-device online/offline counts. No endpoint in `ultron-backend/app.py`
produces either. Adding real ones would mean new backend monitoring
code — out of scope for a visual redesign pass, flagged rather than
faked or silently dropped.

**A related, pre-existing issue found but NOT touched** (out of
tonight's agreed scope — Home only): the Crypto & Markets section
(`#sec-crypto`) has the *same* hardcoded fake BTC/ETH/SOL/SPY ticker
this pass just removed from Home. Worth a follow-up pass.

## Verified live in Chrome

Console clean across Home and after switching sections and back; other
sections (Security checked directly) render identically to before —
nav still orange, `.card` untouched; real data confirmed rendering
(containers, updates, storage percentage, Pi host/uptime, real activity
feed entries); `thinking` and `alert` states confirmed visually (the
`alert` red color required the forced-resize workaround above to
actually observe, since this test environment reports `document.hidden`
as permanently `true`); responsive breakpoints for the home grids and
`.sphere-wrap` sizing were not touched and were not re-verified beyond
confirming the CSS rules are still present unmodified.

## Addendum: density refinement against the actual reference image

The reference image (`ultron brain referance pic.jpg`, project root —
confirmed present, inspected directly, not assumed) is a dense
gold/orange particle-filament wheel/hub with radiating spokes, a bright
ring-structured core, and scattered sparks. The original v1 particle
system (46 nodes, 2-3 edges each, a single glowing core dot) was
noticeably sparser and flatter than this by comparison. Refined,
without changing the underlying architecture:

- **Fine dust layer** (~190 particles desktop / 70 reduced) — flat
  `fillStyle`, no per-particle gradient or shadow, kept deliberately
  cheap since this is the actual density lift, not the structural node
  graph.
- **Radiating filament spokes** (~14 desktop / 7 reduced) — fixed
  organic curves (one random-offset control point each) from near the
  core outward, generated once, only their flicker animates per frame.
  This is the specific "wheel/hub" structure the reference's silhouette
  is built from, distinct from the node-to-node edges.
- **Depth**: each structural node gets a random `depth` (0-1) set at
  generation, used to modulate size/opacity (back nodes dimmer and
  smaller) — a cheap parallax fake, not an actual canvas blur filter
  per node (which would be real cost at this count).
- **Core**: two thin concentric ring strokes added around the glow,
  reading as a tight hub rather than a single dot; the far SVG
  `.core-rings` ellipses are unchanged and separate.
- Structural node count raised 46→64 (30 reduced), edge fan-out 2-3→2-4.

Verified live: the `alert` state's color shift (confirmed via the same
forced-resize technique noted above) correctly recolors every new layer
together, not just the original elements; console clean; Reduced Visual
Mode's lower counts confirmed present in the same code path.

## Known limitations — not solved this round

- **Mobile layout not independently re-verified this pass** — same
  automation-environment limitation Module 13 hit (`resize_window`
  doesn't change the actual rendered viewport here). The existing
  `@media(max-width:1050px)` grid-collapse and `.sphere-wrap` size
  overrides were left untouched, not re-tested at a real narrow
  viewport.
- **`prefers-reduced-motion` inherited from Module 13, not re-verified
  live** — same reasoning as before: the OS-level media feature can't
  be toggled in this environment. Code-reviewed only.
- **The Crypto & Markets ticker's identical fake-data problem**, noted
  above, is unresolved — deliberately out of scope tonight.
- **No component-file split.** The request's suggested
  `UltronHome/AiCore/SystemTelemetry/...` hierarchy assumes a framework
  this project doesn't have (plain HTML/CSS/JS, no build step, by
  design — see `README.md`). The equivalent here is clearly-labeled CSS
  blocks and named JS functions within the single file, not physically
  separate component files.
