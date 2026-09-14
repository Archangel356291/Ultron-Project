"""Generates a self-contained, fully offline HTML knowledge-graph viewer
(Module 6) from graphify's own graphify-out/graph.json -- not a live
Flask page (step 27 explicitly skips that), a regenerated static
artifact, same pattern graphify's own graph.html already uses.

Reads whatever graph.json currently contains, including Module 4's
visibility redaction -- a private node's stub (label: "[private]", no
source_file) is all this script ever sees, so there's no separate
privacy logic needed here: this viewer literally cannot leak anything
that isn't already in the plaintext graph.json.

The 3d-force-graph library bundles its own internal copy of three.js
(self-contained UMD build) -- separate from three-pipeline's vendored
three.module.js/three.core.js, which is for Module 9's hero head. Both
vendored per Module 5's "downloaded once, no CDN" requirement; not the
same file because 3d-force-graph doesn't support bringing your own
three.js instance in its UMD build.

Usage:
    python graph-viewer/generate_viewer.py
    -> writes graphify-out/graph-3d-viewer.html

Regenerate any time graph.json changes (after a graphify rebuild, after
Module 4's enrich_visibility.py/safe_report.py, or -- once it exists --
after Module 7's write step, per step 26).
"""
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GRAPH_PATH = ROOT / "graphify-out" / "graph.json"
LIBRARY_PATH = ROOT / "three-pipeline" / "vendor" / "3d-force-graph.min.js"
OUT_PATH = ROOT / "graphify-out" / "graph-3d-viewer.html"

CATEGORY_COLORS = {
    "code": "#3DD6FF",
    "document": "#FFC24B",
    "concept": "#33D17A",
    "rationale": "#B084F0",
    "paper": "#FF8A1E",
    "image": "#5B6B8C",
}
PRIVATE_COLOR = "#4C5A78"
DEFAULT_COLOR = "#8D9BBD"

HTML_TEMPLATE = r"""<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Ultron knowledge graph</title>
<style>
  :root{
    --void:#050810; --panel:#0A1120; --panel-raised:#0F1830; --line:#03294A;
    --text:#E9EDF7; --text-dim:#8D9BBD; --text-faint:#4C5A78; --oxide:#FF8A1E;
  }
  *{box-sizing:border-box;}
  body{ margin:0; background:var(--void); color:var(--text); font-family:'Inter',system-ui,sans-serif; overflow:hidden; }
  #graph{ position:fixed; inset:0; }
  #ui{
    position:fixed; top:0; left:0; right:0; z-index:10;
    display:flex; align-items:center; gap:14px; flex-wrap:wrap;
    padding:12px 18px; background:linear-gradient(180deg, rgba(10,17,32,0.95), rgba(10,17,32,0.75));
    border-bottom:1px solid var(--line); font-size:13px;
  }
  #ui h1{ font-size:15px; margin:0; font-weight:700; letter-spacing:0.02em; }
  #ui h1 span{ color:var(--oxide); }
  .tabs{ display:flex; gap:4px; background:var(--panel); border-radius:6px; padding:3px; }
  .tab{ padding:6px 14px; border-radius:4px; cursor:pointer; color:var(--text-dim); user-select:none; }
  .tab.active{ background:var(--oxide); color:var(--void); font-weight:600; }
  #search{
    background:var(--panel); border:1px solid var(--line); color:var(--text);
    border-radius:6px; padding:7px 12px; font-size:13px; min-width:200px;
  }
  #search:focus{ outline:none; border-color:var(--oxide); }
  #stats{ color:var(--text-faint); font-size:12px; margin-left:auto; }
  .legend{ display:flex; gap:10px; flex-wrap:wrap; font-size:11px; color:var(--text-faint); }
  .legend span{ display:inline-flex; align-items:center; gap:5px; }
  .legend i{ width:9px; height:9px; border-radius:50%; display:inline-block; }
  #list-view{
    position:fixed; inset:56px 0 0 0; overflow-y:auto; background:var(--void);
    padding:10px 24px; display:none;
  }
  #list-view table{ width:100%; border-collapse:collapse; font-size:12.5px; }
  #list-view th{ text-align:left; padding:8px 10px; color:var(--text-faint); border-bottom:1px solid var(--line); position:sticky; top:0; background:var(--void); }
  #list-view td{ padding:7px 10px; border-bottom:1px solid var(--line); }
  #list-view tr:hover{ background:var(--panel); }
  .pill{ display:inline-block; padding:2px 8px; border-radius:10px; font-size:10.5px; color:var(--void); font-weight:600; }
  .node-tooltip{ font-family:'JetBrains Mono',monospace; font-size:11.5px; line-height:1.5; }
</style>
</head>
<body>
<div id="ui">
  <h1>ULTRON<span>·</span>Knowledge Graph</h1>
  <div class="tabs">
    <div class="tab active" data-mode="clean">Clean</div>
    <div class="tab" data-mode="explore">Explore 3D</div>
    <div class="tab" data-mode="list">List</div>
  </div>
  <input id="search" type="text" placeholder="Search label or tag...">
  <div class="legend" id="legend"></div>
  <div id="stats"></div>
</div>
<div id="graph"></div>
<div id="list-view"><table><thead><tr><th>Label</th><th>Category</th><th>Community</th><th>Visibility</th><th>Updated</th></tr></thead><tbody id="list-body"></tbody></table></div>

<script>__LIBRARY_JS__</script>
<script>
const GRAPH_DATA = __GRAPH_DATA_JSON__;
const CATEGORY_COLORS = __CATEGORY_COLORS_JSON__;
const PRIVATE_COLOR = __PRIVATE_COLOR_JSON__;
const DEFAULT_COLOR = __DEFAULT_COLOR_JSON__;
const GENERATED_AT = __GENERATED_AT_JSON__;

// Degree (connection count) per node, for node size (step 25: "scale
// node size by connection count") -- computed once from the edge list.
const degree = {};
GRAPH_DATA.links.forEach(l => {
  const s = typeof l.source === 'object' ? l.source.id : l.source;
  const t = typeof l.target === 'object' ? l.target.id : l.target;
  degree[s] = (degree[s] || 0) + 1;
  degree[t] = (degree[t] || 0) + 1;
});

function colorFor(node) {
  if (node.visibility === 'private') return PRIVATE_COLOR;
  return CATEGORY_COLORS[node.category] || DEFAULT_COLOR;
}

function tooltipFor(node) {
  const cat = node.category || 'unknown';
  const vis = node.visibility === 'private' ? 'PRIVATE' : 'public';
  const tags = (node.tags || []).join(', ');
  return `<div class="node-tooltip"><b>${escapeHtml(node.label)}</b><br>`
    + `category: ${escapeHtml(cat)} &middot; ${vis}<br>`
    + (node.community_name ? `community: ${escapeHtml(node.community_name)}<br>` : '')
    + (tags ? `tags: ${escapeHtml(tags)}<br>` : '')
    + (node.date_created ? `created: ${escapeHtml(node.date_created.slice(0,10))}<br>` : '')
    + (node.date_updated ? `updated: ${escapeHtml(node.date_updated.slice(0,10))}` : '')
    + `</div>`;
}

function escapeHtml(s) {
  return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
}

const graphEl = document.getElementById('graph');
const Graph = ForceGraph3D()(graphEl)
  .graphData(GRAPH_DATA)
  .backgroundColor('#050810')
  .nodeColor(colorFor)
  .nodeVal(n => 1 + Math.sqrt(degree[n.id] || 0))
  .nodeLabel(tooltipFor)
  .linkColor(() => 'rgba(140,160,200,0.25)')
  .linkWidth(0.4)
  .numDimensions(2)
  .onNodeClick(n => { Graph.centerAt(n.x, n.y, n.z, 800); });

window.addEventListener('resize', () => Graph.width(window.innerWidth).height(window.innerHeight));
Graph.width(window.innerWidth).height(window.innerHeight - 56);

// --- mode tabs: Clean (2D, settled, no auto-rotate) / Explore (full 3D,
// slow auto-rotate, free orbit) / List (plain sortable table) -- step 24
// explicitly asks that the animated 3D view never be the ONLY way to
// read the graph, since dense clusters can occlude. ---
let rotateTimer = null;
function stopRotate() { if (rotateTimer) { clearInterval(rotateTimer); rotateTimer = null; } }
function startRotate() {
  stopRotate();
  let angle = 0;
  rotateTimer = setInterval(() => {
    angle += 0.0025;
    const distance = 400;
    Graph.cameraPosition({ x: distance * Math.sin(angle), z: distance * Math.cos(angle) });
  }, 30);
}

function setMode(mode) {
  document.querySelectorAll('.tab').forEach(t => t.classList.toggle('active', t.dataset.mode === mode));
  const listView = document.getElementById('list-view');
  if (mode === 'list') {
    graphEl.style.display = 'none';
    listView.style.display = 'block';
    stopRotate();
    return;
  }
  graphEl.style.display = 'block';
  listView.style.display = 'none';
  if (mode === 'clean') {
    stopRotate();
    Graph.numDimensions(2);
  } else {
    Graph.numDimensions(3);
    startRotate();
  }
}
document.querySelectorAll('.tab').forEach(t => t.addEventListener('click', () => setMode(t.dataset.mode)));

// --- search/filter: dims non-matching nodes rather than hiding them
// outright, so the overall shape of the graph stays visible while
// searching (step 25: search/filter by keyword or tag). ---
document.getElementById('search').addEventListener('input', (e) => {
  const q = e.target.value.trim().toLowerCase();
  Graph.nodeColor(n => {
    if (!q) return colorFor(n);
    const hay = (n.label + ' ' + (n.tags || []).join(' ')).toLowerCase();
    return hay.includes(q) ? colorFor(n) : 'rgba(80,90,110,0.15)';
  });
});

// --- list view ---
const listBody = document.getElementById('list-body');
const sortedNodes = [...GRAPH_DATA.nodes].sort((a, b) => (a.label || '').localeCompare(b.label || ''));
listBody.innerHTML = sortedNodes.map(n => {
  const color = colorFor(n);
  return `<tr><td>${escapeHtml(n.label)}</td>`
    + `<td><span class="pill" style="background:${color}">${escapeHtml(n.category || '?')}</span></td>`
    + `<td>${escapeHtml(n.community_name || '')}</td>`
    + `<td>${n.visibility === 'private' ? 'private' : 'public'}</td>`
    + `<td>${escapeHtml((n.date_updated || '').slice(0,10))}</td></tr>`;
}).join('');

// --- legend + stats ---
const legendEl = document.getElementById('legend');
legendEl.innerHTML = Object.entries(CATEGORY_COLORS).map(([cat, color]) =>
  `<span><i style="background:${color}"></i>${cat}</span>`
).join('') + `<span><i style="background:${PRIVATE_COLOR}"></i>private</span>`;

const privateCount = GRAPH_DATA.nodes.filter(n => n.visibility === 'private').length;
document.getElementById('stats').textContent =
  `${GRAPH_DATA.nodes.length} nodes · ${GRAPH_DATA.links.length} edges · ${privateCount} private · generated ${GENERATED_AT}`;
</script>
</body>
</html>
"""


def main():
    graph = json.loads(GRAPH_PATH.read_text(encoding="utf-8"))
    library_js = LIBRARY_PATH.read_text(encoding="utf-8")

    # 3d-force-graph wants {nodes, links} -- graphify's graph.json already
    # uses exactly that shape (id/source/target line up natively), so this
    # is just a straight pass-through, not a transformation.
    graph_data = {"nodes": graph["nodes"], "links": graph["links"]}

    from datetime import datetime, timezone
    generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    html = (
        HTML_TEMPLATE
        .replace("__LIBRARY_JS__", library_js)
        .replace("__GRAPH_DATA_JSON__", json.dumps(graph_data, ensure_ascii=False))
        .replace("__CATEGORY_COLORS_JSON__", json.dumps(CATEGORY_COLORS))
        .replace("__PRIVATE_COLOR_JSON__", json.dumps(PRIVATE_COLOR))
        .replace("__DEFAULT_COLOR_JSON__", json.dumps(DEFAULT_COLOR))
        .replace("__GENERATED_AT_JSON__", json.dumps(generated_at))
    )
    OUT_PATH.write_text(html, encoding="utf-8")

    node_count = len(graph_data["nodes"])
    private_count = sum(1 for n in graph_data["nodes"] if n.get("visibility") == "private")
    print(f"[graph-viewer] wrote {OUT_PATH} ({len(html):,} bytes) -- "
          f"{node_count} nodes ({private_count} private), {len(graph_data['links'])} edges")


if __name__ == "__main__":
    main()
