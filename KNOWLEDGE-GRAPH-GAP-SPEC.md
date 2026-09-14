# Knowledge graph gap spec (Module 2 deliverable)

Written before any Module 4 schema work, per the roadmap's own gate
("do not proceed until this spec exists"). Everything below was verified
against the actual files on disk tonight (2026-09-14), not assumed from
graphify's documentation.

## 1. Beta test results already recorded — pulled in as ground truth

Checked `ultron-backend/BETA-TESTERS.md`, `CODE-AUDIT.md`,
`BETA-LAUNCH-CHECKLIST.md`, and queried the graphify graph itself
(`graphify query "beta test results and verification"`) for anything not
already in those docs. Nothing was found outside them — the graph
surfaces exactly the same facts the docs already state, which is itself
a useful confirmation nothing is buried or lost:

- **Roster is empty.** No third-party beta tester has been onboarded yet
  (`BETA-TESTERS.md`: "_none yet_").
- **One self-test exists:** 2026-09-13, the `beta_tester` role verified
  end-to-end using the owner's own second device (phone) over Tailscale
  — explicitly not counted as a third-party tester in the roster.
- **Real bugs found during that verification pass** (already logged in
  `CODE-AUDIT.md` / `PROJECT-SUMMARY-FOR-CLAUDE-CODE.md`, not re-stated
  here): the spend-cap read-then-act race, `/api/tts` missing from the
  spend cap, `_PRESENCE` dict-changed-size race, beta testers unable to
  see their own spend, and a `file://` origin `fetch()` bug hit live on
  mobile Chrome's Connect button.

Conclusion: there is no separate "lost" beta-results source to recover.
The existing docs are already the ground truth Module 4 needs to index.

## 2. Graphify's actual output format, verified from the real files

`graphify-out/` on disk right now:

| Path | What it is |
|---|---|
| `graph.json` | The graph itself. Top-level: `{directed, multigraph, graph, nodes, links, hyperedges, built_at_commit}`. |
| `manifest.json` | **Per-source-file** bookkeeping for `--update` (not per-node): `{mtime, seen, ast_hash, semantic_hash}` keyed by file path. |
| `cost.json` | Per-run token cost log (`{runs: [{date, input_tokens, output_tokens, files}], total_input_tokens, total_output_tokens}`). |
| `GRAPH_REPORT.md` | Human-readable audit: god nodes, surprising connections, communities, suggested questions. |
| `graph.html` | Self-contained interactive viz (already exists — relevant context for Module 6). |
| `obsidian/` | One `.md` file per node, YAML frontmatter + wikilinks, regenerated on `graphify export obsidian`. |
| `cache/ast/`, `cache/semantic/` | Content-hash-keyed extraction cache, avoids re-extracting unchanged files. |
| `2026-09-13/`, `2026-09-14/` | Dated backup snapshots graphify takes automatically before an export that would shrink the graph. |

**Node schema** (real sample, `graph.json`):
```json
{
  "id": "dev_tools_fake_pkgs_discord_init_interaction",
  "label": "Interaction",
  "file_type": "code",
  "source_file": "dev-tools/fake_pkgs/discord/__init__.py",
  "source_location": "L89",
  "community": 0,
  "community_name": "bot.py",
  "norm_label": "interaction",
  "_origin": "ast",
  "_callable": true
}
```

**Edge schema** (real sample):
```json
{
  "source": "...", "target": "...",
  "relation": "calls",
  "confidence": "EXTRACTED", "confidence_score": 1.0,
  "context": "call", "weight": 1.0,
  "source_file": "...", "source_location": "L53"
}
```

**Load-bearing finding: edges are already labeled.** `relation` (calls,
references, shares_data_with, conceptually_related_to, etc.) already
exists on every edge. Module 4 step 10 called labeled edges "the single
biggest lever for AI accuracy" as if it were new work — it isn't; it's
already the format. Nothing to build there.

**Obsidian export already has tags**, but only as an export-time
side-effect, not a first-class graph.json field — generated from
`file_type` + `community` + `confidence` at export time
(`tags: [graphify/concept, graphify/EXTRACTED, community/...]`), not
stored on the underlying node itself, and not independently settable.

**Retrieval already exists**: `graphify query "<question>"` does
vocabulary-expanded BFS/DFS traversal with a token budget today — this
is real, working retrieval, not a gap. See §3 for what it doesn't do yet.

**Extensibility, confirmed rather than assumed:** nodes already carry
extra fields beyond a fixed core schema (`_origin`, `_callable` above are
AST-only, not present on doc-derived nodes) and `build_from_json`/
`to_json` round-trip them without complaint. Adding new fields to the
existing node dict is additive and already how the format behaves in
practice — Module 4 does not need to fork graphify's graph store to add
fields; it needs to add fields to the same one.

## 3. Ponytail — what it actually limits/strips

Checked the installed plugin (`~/.claude/plugins/cache/ponytail/ponytail/4.9.0/`)
directly rather than assuming from its one-line description.

**It is a prompt-injection plugin, not a mechanical token/context
filter.** A `SessionStart` hook (`.claude-plugin/plugin.json` →
`hooks/claude-codex-hooks.json`) injects a system-prompt block (the
"lazy senior dev" ladder: YAGNI → reuse → stdlib → native → existing dep
→ one-liner → minimum code) that governs how *I* write code — shorter
diffs, no speculative abstraction, stdlib/native before a new
dependency. `~/.claude/.ponytail-active` just stores the current
intensity level (currently `full`).

**What this means for Module 8 specifically:** Ponytail's "token
efficiency" is about the size of code I write, not the size of context
fed into a conversation. It has no mechanism for trimming what goes into
context, retrieval, or the graph — that's an entirely separate concern
Module 8's read-path design has to solve on its own. Don't conflate the
two when measuring Module 8's before/after token counts.

## 4. The gap — what Module 4 actually needs to add

Given §2's real schema, here's what genuinely doesn't exist yet, scoped
down from the roadmap's step-by-step list to just the real deltas:

| Roadmap ask (Module 4) | Status |
|---|---|
| Labeled edges | **Already exists.** No work needed. |
| Fixed node schema (id, name, category, tags) | `id`/`label`/`file_type`/`community` already exist and are consistent. `category` beyond `file_type`'s 6 fixed values, and a real `tags` array, do not. |
| Created/updated timestamps **per node** | Does not exist. `manifest.json` has `mtime`/`seen` per *file*, not per node, and it's not merged onto the node itself. |
| Keyword/tag index queryable by code | Does not exist as a standalone artifact. `graphify query` is real retrieval today, but there's no separate index file a non-graphify script could query directly. |
| Public/private flag, defaulted at creation | Does not exist in any form. |
| Encryption at rest for the private partition | Does not exist — nothing in this pipeline encrypts anything; it's all plaintext JSON/Markdown. |

Everything in the left column that isn't in this table (edges,
extensibility, retrieval) is already provided and out of scope for new
build work — Module 4 should extend, not rebuild.
