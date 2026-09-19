# Odin's runtime knowledge graph (Module 10) — v1

The roadmap's own instruction for this module: *"Build Odin's runtime
knowledge graph, reusing Module 4/7/8. Do not design this from scratch.
Reuse the same schema, labeled-edge convention, public/private tagging,
indexing, and retrieval logic built for the vault graph, applied to
Odin's own runtime memory."* This is that — applied to `memory_notes`,
the SQLite table `remember_note`/`recall_notes` already used, not a new
store.

## The reuse problem, and how it's actually solved

The functions the roadmap says to reuse (`classify_visibility`,
`derive_tags`, `retrieve`) were built in `graph-schema/` (Module 4) and
`session-read/` (Module 8) — both **outside** `odin-backend/`. But the
Docker image (`odin-backend/Dockerfile`) only `COPY`s `odin-backend/`
and `odin-dashboard.html`; nothing else in the repo root ships inside
the container. Module 10's actual runtime code lives in `app.py`, which
does ship — so the functions had to move somewhere `app.py` can import
directly at build time, not just at dev time.

Fix: `odin-backend/graph_schema_shared.py` is now the one canonical
implementation of `classify_visibility`, `derive_tags`, `_tag_words`, and
`retrieve`. `graph-schema/enrich_visibility.py` and
`session-read/retrieve_context.py` were both refactored to import FROM
this module (`sys.path.insert(0, .../odin-backend)`) instead of keeping
their own copies — so there is exactly one implementation, not three that
could quietly drift apart. `app.py` imports it directly (same directory,
no path hack needed — it's the only one of the three consumers that
actually ships inside the image).

Both existing test suites (`graph-schema/test_enrich.py`,
`session-read/test_retrieve.py`) were re-run after this refactor and
still pass unchanged — proof the shared module is a pure extraction, not
a rewrite.

## Schema (per note, in `memory_notes`)

Three new columns, added the same way `llm_usage` gained `beta_name`/
`cost_usd` (`ALTER TABLE ... ADD COLUMN`, gated on `PRAGMA table_info`, so
an existing `odin.db` keeps its history):

```
category    TEXT   -- always "concept" for notes today (no file_type/
                    -- community_name concept applies to a chat-saved note)
tags        TEXT   -- JSON-encoded list, from derive_tags() — currently
                    -- just ["visibility:public"] or ["visibility:private"]
visibility  TEXT   -- "public" or "private", from classify_visibility()
```

A new `memory_edges` table gives notes the **same labeled-edge
convention** the vault graph uses (`source`/`target`/`relation`):

```sql
CREATE TABLE memory_edges (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source_note_id INTEGER NOT NULL,
    target_note_id INTEGER NOT NULL,
    relation TEXT NOT NULL,       -- always "relates_to" today
    confidence REAL NOT NULL DEFAULT 1.0,
    created_at TEXT NOT NULL
)
```

## Classification and tagging: literally the same functions

`remember_note()` now runs the note text through
`classify_visibility({"label": note})` and `derive_tags(node, visibility)`
— the exact functions Module 4 built for graphify nodes, unmodified,
treating the note as a one-field node dict. A note mentioning a private
keyword (`wireguard`, `api key`, `trade record`, an IP address, etc.) gets
`visibility: "private"` the same way a vault document would. **Enforcement
is lighter than Module 4's**, deliberately: a private *note* is never
shown to the beta role (memory tools are already admin-only, excluded
from `BETA_ALLOWED_TOOLS`) but isn't separately encrypted-at-rest the way
`private-nodes.enc.json` is — `odin.db` itself isn't published anywhere
graphify's graph.json is, so the threat model (public git history) that
justified Module 4's encryption doesn't apply here. If `odin.db` is
ever backed up somewhere less trusted, this would need revisiting.

## Edges: reusing `retrieve()` itself to find them, not new overlap logic

The roadmap says reuse "the same ... indexing, and retrieval logic" — so
edge discovery doesn't get its own bespoke keyword-overlap function. When
`remember_note()` saves a new note, it builds the graph/tag_index shape
`retrieve()` expects from the *existing* notes (via `_notes_as_graph()`),
then calls `retrieve(new_note_text, graph, tag_index, min_nodes=3)` —
the new note's own text is the query. Whatever comes back as `seed_ids`
(genuinely related existing notes, by tag or shared label words) becomes
`relates_to` edges from the new note, capped at `MEMORY_EDGE_MAX_LINKS =
10` per save so two very generic notes can't create a fan-out explosion.

This means the exact same retrieval mechanism serves two different jobs —
write-time linking and read-time recall — which is the literal reuse the
roadmap asked for, not two implementations of "are these related."

## Retrieval: `recall_related_notes`, a new tool alongside `recall_notes`

`recall_notes` (existing, substring `LIKE` search) is untouched — it's a
different, already-tested use case (skim recent notes / exact-phrase
lookup) and nothing about Module 10 required changing its behavior.

`recall_related_notes(query, min_nodes=6)` is new: it shapes
`memory_notes` + `memory_edges` into `{"nodes": [...], "links": [...]}` +
`tag_index` (via `_notes_as_graph()`, the same helper `remember_note` uses)
and calls `retrieve()` — tag/label seed match, widened on a sparse result,
expanded exactly one hop via `memory_edges`. This is the piece that
actually earns the word "graph": it can surface a note that shares *no*
literal words with the query, reached only by walking one `relates_to`
edge from a note that does. Verified in
`dev-tools/test_runtime_graph.py` with a real (not synthetic-only) case:
querying `"reminder"` returns a note containing "reminder" as the seed,
and pulls in a linked note containing "monthly" (not "reminder") purely
via the edge between them — and correctly stops at one hop, not two.

Registered as a new chat tool, admin-only (absent from
`BETA_ALLOWED_TOOLS`, same gate every other memory tool uses).

## What was actually verified (not just "should work")

`dev-tools/test_runtime_graph.py` proves, against real SQLite:

- A note containing a private keyword gets `visibility: "private"`; an
  ordinary note gets `"public"` and the matching tag — reusing Module 4's
  classifier unmodified.
- Saving a related note creates a real `relates_to` edge to the note(s)
  it's actually related to (shared words) — and a genuine negative case
  (an unrelated note about car insurance) creates **no** edge to anything,
  proving this isn't a rubber-stamp "always link" mechanism.
- `recall_related_notes` reaches a note via a one-hop edge with zero
  literal word overlap with the query, and does **not** reach a
  two-hops-away note — proving the one-hop boundary is real, not
  accidental.
- `recall_related_notes` rejects an empty/missing query rather than
  returning something misleading.
- `memory_edges` has zero dangling rows after `memory_notes` trims past
  `MEMORY_NOTES_MAX_ROWS` — SQLite has no `FOREIGN KEY` cascade here, so
  `remember_note()` explicitly deletes edges pointing at trimmed notes on
  every save. (A real bug class this test exists specifically to catch:
  without the explicit cleanup, `memory_edges` would accumulate rows
  referencing note ids that no longer exist.)

Full existing checkpoint (`test_enrich`, `test_retrieve`,
`test_summarize_session`, `test_backup_restore`, `test_memory`,
`test_beta_spend_cap`, `test_mcp_untrusted_wrap`, `test_tts_streaming`)
re-run after these changes — all still pass unchanged.

**Per Module 11's own stated warning** that Module 10 is the first real
test of the permanent financial-action boundary:
`dev-tools/test_no_financial_action_tools.py` was re-run after Module 10's
changes and still passes — 16 tools in `TOOL_DISPATCH` now (up from 15),
the new one (`recall_related_notes`) is read-only and not
trade/financial-action-shaped, and the trade-tool set is still exactly
`{get_trades, get_trade_summary, get_trade_tax_lots}`.

## Known limitations — not solved this round

- **No backfill for notes saved before this migration.** Existing rows
  keep `category`/`tags`/`visibility` as `NULL` until they're re-saved
  (which never happens automatically — notes aren't edited in place).
  `_notes_as_graph()` treats a `NULL` visibility as `"public"` and a
  `NULL` category as `"concept"` so old rows don't crash retrieval, but
  they also never got auto-linked to anything at save time, so they'll
  have no outgoing edges until something new relates to them going
  forward. Not a correctness bug — just means the graph is denser for
  notes saved after tonight than before it.
- **Edge relations are all `"relates_to"`.** The vault graph has richer
  relation types (`calls`, `imports`, etc.) because graphify extracts them
  structurally from code/docs. A saved note has no structural relation to
  extract — `"relates_to"` is the only relation this mechanism can
  honestly claim. A future pass could ask the model itself to label the
  relation (e.g. "clarifies", "contradicts", "follows up on") when saving
  a note that clearly connects to an existing one, but that's a
  qualitatively different (LLM-judgment-based) mechanism, not a small
  addition to this one.
- **No manual edge/tag correction tool**, same gap Module 4 already has
  for the vault graph (no un-flag for a false-positive private
  classification) — same acknowledged gap, not solved here either.
