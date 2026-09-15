# Home-tab knowledge graph integration

Adds "ULTRON'S KNOWLEDGE" as a second, distinct visualization on Home,
per a user-supplied reference image (a dense, clustered force-directed
graph). Placed below the existing System Telemetry/Home Lab
Overview/Security grid, matching the requested visual hierarchy (brain =
intelligence, graph = knowledge, both secondary to the brain).

## Audit finding that shaped the whole approach

This project already had almost everything needed, built across earlier
tonight's modules:

- **The real data**: `graphify-out/graph.json` (Module 4) — 543 real
  nodes, 859 real edges, 62 real clusters, extracted from this actual
  codebase (code/document/rationale/concept), already privacy-redacted
  (85 nodes stubbed to `"[private]"`). Plus Ultron's own runtime memory
  graph (Module 10's `memory_notes`/`memory_edges`, via the exact same
  `_notes_as_graph()` helper `recall_related_notes` already uses).
- **The rendering library**: `three-pipeline/vendor/3d-force-graph.min.js`
  — vendored in Module 5, already proven working in
  `graph-viewer/generate_viewer.py`'s standalone viewer (Module 6),
  including the exact color-by-category / size-by-degree / hover-tooltip
  / search-and-dim techniques this integration reuses directly.

So this wasn't really "build a knowledge graph" — it was "finish wiring
Module 6's already-built pieces into the Home tab," which is why the
implementation is a few hundred lines, not a new subsystem.

## Backend: `GET /api/knowledge-graph`

`get_knowledge_graph()` in `app.py` reads `graphify-out/graph.json`
server-side (not served as a raw static file — this is a REST endpoint,
consistent with the rest of the app's `/api/*` convention) and merges in
the memory graph, tagging memory nodes with a real `category: "memory"`
rather than inventing home-lab/security/finance categories the actual
tagging scheme doesn't have. Admin-only (`@require_token`, same as
`/api/memory`) — this exposes real project internals, not something the
beta role's narrow scope should reach.

`limit=N` keeps the **highest-degree** nodes, not an arbitrary prefix —
verified against an independently-computed degree map in
`dev-tools/test_knowledge_graph_route.py`, specifically to catch a
regression to a naive `nodes[:limit]` slice. Used for mobile/narrow
viewports and Reduced Visual Mode (step 17's LOD requirement).

`graphify-out/graph.json` alone (not the rest of `graphify-out/` —
caches, the Obsidian export, the never-committed
`private-nodes.enc.json`) is now shipped in the Docker image via one
narrow `COPY` line and one narrow `.dockerignore` allowlist entry.

## Frontend: real 3d-force-graph, forced to 2D

Same library Module 6 already vendored, `numDimensions(2)` (matches the
reference image's flat layout, and avoids the cost of a lit 3D scene on
a Raspberry Pi 400), `cooldownTicks` set finite (not infinite — the
layout settles once and the physics simulation stops, shorter under
`prefers-reduced-motion`/Reduced Visual Mode). Node color by category,
node size by connection count (`nodeVal`), hover highlights direct
neighbors and dims the rest, click opens an Ultron-styled inspector
panel (never a browser alert/modal) with real fields — type,
visibility, cluster, relationship count, last updated. Search dims
non-matching nodes rather than hiding them, same technique the
standalone viewer uses. Filter pills are built from whatever categories
are actually present in the response, with real counts — never a fixed
list of categories that may not exist in the data.

The AI-core connection (step 13) is a plain CSS gradient line between
the hero panel and this section — deliberately not "highlight nodes
when Ultron is thinking," since that would imply specific memory access
that isn't real. A thematic connector, not a fabricated data-driven
effect.

## Real bugs found live, not assumed away

**The graph never rendered on a normal page load — twice, for two
different reasons**, both caught by testing on an actual fresh load,
not just checking the code:

1. First fix attempt: added a "catch up if already connected" check at
   this script's own load time, reasoning that the connection hook
   inside `refreshAll()` fires too early (before this script, loaded
   last, has defined `window.__kgRefresh`). This was real but
   insufficient.
2. **The actual root cause**: the initial auto-connect
   (`loadRememberedConnection()` → `connectBackend()`) sets
   `state.connected = true` directly and calls `refreshAll()` itself —
   so by the time `refreshAll()`'s own internal `if (!state.connected)`
   check runs, the condition is already false, and that hook (correct
   for the separate case of recovering from a mid-session drop) never
   fires for the initial connect at all. Fixed by calling
   `window.__kgRefresh()` directly from `connectBackend()`'s own success
   path — the actual single source of truth for "we just connected."
   Confirmed via a real page load (not a manual console call) after the
   fix, twice, both fully populating: 544 nodes, 859 links, 62 clusters,
   real per-category filter counts.

**`.nodeVal()` was silently missing.** The `degree` map was built and
used for tooltips/the inspector panel, but never actually wired to
node sizing — "different node sizes" from the spec silently wasn't
happening. Caught by re-reading the `initGraph()` call chain against
the spec, not by a visual glance.

**Links were present but effectively invisible** at the original
opacity/width (0.18 alpha, 0.4px). Not a functional bug — the data was
there — but a real readability problem given "connecting lines" is
explicit in the brief. Increased to 0.35 alpha / 0.6px / `linkOpacity(0.6)`.

## Verified live in Chrome

Fresh page load (not a manual re-trigger) correctly populates real
stats (544 nodes / 859 links / 62 clusters / synchronized), the
category filter pills, and the graph itself; console clean throughout.
Filter-by-category confirmed working (clicking "Memory (1)" correctly
dimmed all 543 non-memory nodes, leaving the one real memory node
visible). Node inspector confirmed populating real fields for a real
node (`app.py` — type `code`, cluster `Private/Mixed Community 6`).
Close button confirmed working. Section-switch away from and back to
Home confirmed clean (no errors from the pause/resume hook). Other
sections (Security) confirmed unaffected.

## Known limitations — not solved this round

- **Pixel-precise click-testing wasn't done via simulated mouse
  clicks** — screenshot-based coordinate clicking on a dense
  force-graph's small nodes proved unreliable in this test harness; the
  inspector's data-population logic was verified directly (the same
  code path `onNodeClick` calls) instead of via an actual simulated
  click landing on a specific node.
- **No automated visual-density tuning.** 543 nodes at the default
  zoom read as a dense cluster with edges visible mainly at the
  periphery — usable via the library's built-in zoom/pan, not
  independently verified as optimal.
- **Camera rotation control is still present** even in 2D mode (a
  3d-force-graph characteristic already present in Module 6's
  standalone viewer's own "Clean" mode) — left as-is, matching existing
  precedent, not a regression introduced here.
- **Mobile/Pi-400 LOD (the `limit` query param) implemented and unit
  tested, not verified live** — same automation-environment limitation
  noted in Module 13/14 (can't trigger a genuine narrow-viewport reflow
  here).
- **Memory category currently has exactly one real node.** Honest, not
  a bug — Module 10's memory system is real infrastructure that simply
  hasn't accumulated much content yet in normal use.
