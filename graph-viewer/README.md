# graph-viewer (Module 6)

A dual-mode, fully offline HTML knowledge-graph viewer, generated from
graphify's own `graphify-out/graph.json` — not a live Flask page (step
27 explicitly skips that for now), a regenerated static artifact, the
same pattern graphify's own `graph.html` already uses.

## Step 22 — does graphify already output Obsidian-native markdown/links?

Yes, confirmed already during Module 2's audit (`KNOWLEDGE-GRAPH-GAP-SPEC.md`):
`graphify-out/obsidian/` — one `.md` file per node with wikilinks and
frontmatter tags, regenerated via `graphify export obsidian`. Noted for
reference per the roadmap's own instruction, but this doesn't replace
the dedicated viewer below — Obsidian's built-in graph view has no 3D
or physics-driven layout mode, which is specifically what step 23 asks
for.

## What this generates

`python graph-viewer/generate_viewer.py` reads the current
`graphify-out/graph.json` and writes
`graphify-out/graph-3d-viewer.html` — one self-contained file (~1.85 MB
on the current graph: 542 nodes, 844 edges, the vendored
`3d-force-graph` library, and the graph data itself, all inlined).
**No fetch(), no ES module imports, no CDN** — opens directly, data and
all, exactly like `odin-dashboard.html`'s own single-file philosophy.
(Verified served over a local HTTP server, since the browser automation
available couldn't navigate to `file://` URLs directly to test that
path specifically — but the page uses only classic `<script>` tags and
inlined data, neither of which file:// restricts, so it's expected to
work opened directly too.)

**Privacy is inherited, not reimplemented.** This viewer only ever sees
whatever's currently in `graph.json` — a Module-4-redacted private node
is already just `{id, label: "[private]", category, community,
timestamps}` by the time this script reads it, so there's no separate
privacy logic here at all. It literally cannot leak what isn't already
in the plaintext file.

## The three modes (step 24 — animated 3D is never the only way to read it)

- **Clean** — `numDimensions(2)`, no camera motion. Default. For fast,
  practical lookup without the disorientation of full 3D.
- **Explore 3D** — `numDimensions(3)`, slow auto-rotating camera, full
  orbit/pan/zoom via the library's built-in controls.
- **List** — a plain sortable-by-label table (category, community,
  visibility, last-updated columns). No graph rendering at all — for
  when a dense cluster in either graph mode is genuinely hard to parse.

## Human-facing features (step 25) — verified live in Chrome, not just written

- Color-coded by `category` (Module 4's field) — six colors + a
  distinct muted grey for anything `visibility: "private"`, overriding
  its category color so private nodes are visually obvious at a glance
  in every mode, list included.
- Node size scales with connection count (computed from the edge list
  at generation time, not stored on the node).
- Hover tooltip shows label, category, visibility, community, tags, and
  both `date_created`/`date_updated` from Module 4's schema — labels
  otherwise stay hidden until hovered, so a dense cluster isn't a wall
  of overlapping text.
- Search box dims (doesn't hide) nodes that don't match label/tags —
  keeps the overall graph shape visible while searching, verified
  visually: matching nodes stay bright, everything else fades to
  near-invisible without disappearing outright.

## Vendoring (Module 5's shared setup, used here)

`three-pipeline/vendor/3d-force-graph.min.js` — `3d-force-graph`
v1.80.0, vendored from unpkg (downloaded once, not a runtime CDN load).
Bundles its **own internal copy of three.js** — a self-contained UMD
build, separate from `three-pipeline/three.module.js`/`three.core.js`
(which Module 9's hero head will use instead). Not the same file
because 3d-force-graph's UMD build doesn't support bringing your own
three.js instance — two vendored copies for two separate consumers is
correct here, not duplication to clean up.

## Regenerating (step 26)

Re-run `python graph-viewer/generate_viewer.py` any time
`graph.json` changes — after a graphify rebuild + Module 4's
`enrich_visibility.py`/`safe_report.py` pass, or (once it exists) after
Module 7's write step. Not wired into any hook automatically — same
manual-step reality as `graph-schema/run.ps1`, not solved here either.
