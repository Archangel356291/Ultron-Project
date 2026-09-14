# Knowledge graph schema design (Module 4) — v1

Builds on `KNOWLEDGE-GRAPH-GAP-SPEC.md` (Module 2), which found graphify's
real `graph.json` already has stable IDs, labels, and **labeled** edges
(`relation`), but no per-node timestamps, no real `tags` field, no
public/private flag, and obviously no encryption. This is the design for
closing exactly that gap — implemented in `graph-schema/enrich_visibility.py`,
run as a post-processing pass over graphify's own output, never a fork of
graphify's graph store.

## Schema additions (per node)

```json
{
  "...every field graphify already writes, unchanged...": "...",
  "category": "code",
  "tags": ["type:code", "community:backend_rest_routes", "visibility:public"],
  "visibility": "public",
  "date_created": "2026-09-14T04:17:16+00:00",
  "date_updated": "2026-09-14T22:38:00+00:00"
}
```

- **`category`** — aliases graphify's existing `file_type` rather than
  inventing a second, competing taxonomy (`code`/`document`/`paper`/
  `image`/`rationale`/`concept`). One axis, not two.
- **`tags`** — derived deterministically from `file_type`, `community_name`,
  and `visibility`. Also written to a standalone `graphify-out/tag-index.json`
  (`{tag: [node_id, ...]}`) so retrieval code can look up "everything
  tagged X" in O(1) without scanning the whole graph — this is the
  actual "keyword/tag index the retrieval code can query directly" the
  roadmap asked for.
- **`date_created` / `date_updated`** — `date_updated` is the node's
  *source file's* mtime, read from graphify's own `manifest.json` (real
  content-change time, not "whenever this script happened to run").
  `date_created` is the first time this node id was ever observed,
  tracked in `graph-schema/.node_history.json` (a small id→timestamp
  sidecar this script owns, since graphify's manifest only keeps the
  current run's state, not history). This file is safe to commit — it
  holds no node content, only ids and timestamps.
- **`visibility`** — `"public"` or `"private"`. See below.

## Visibility: classification and enforcement

**Classification** (`classify_visibility()`): keyword + IP-address-pattern
match against the node's own label/source_file/community text, covering
the roadmap's explicit hard-private list (API keys, credentials, tokens,
VPN/network config, home lab layout, IPs, trading/financial data) plus
Tailscale/beta-spend-specific terms relevant to this project. **Defaults
private on any doubt** — this is a deliberately broad, conservative list;
false positives (a doc merely *about* Tailscale, not containing an actual
credential) are treated as an acceptable cost, per the roadmap's own
instruction to default unclear/new types private rather than the reverse.

**Enforcement is not just the label.** A node classified private has its
*entire original content* removed from the plaintext `graph.json` — the
public graph keeps only an opaque stub (`id`, `label: "[private]"`,
`visibility`, `category`, `community`, timestamps) so graph topology
(edges, community clustering) still works, but the real label, source
file, and any descriptive text are gone from the file that gets committed
and pushed. The full original node is AES-backed-authenticated-encrypted
(Fernet, from the `cryptography` package — Python's stdlib has no safe
built-in AEAD primitive, and hand-rolling encryption for genuinely
sensitive data is exactly the kind of thing not to DIY) and stored,
keyed by node id, in `graphify-out/private-nodes.enc.json`.

**Key management:** `ULTRON_GRAPH_ENCRYPTION_KEY` in `.env` — generated
once on first run if absent, reused after that. `.env` is already
gitignored (see `.gitignore`), the same place every other secret this
project holds lives. **There is no recovery path if this key is lost** —
back it up the same way you'd back up any other credential in `.env`.

**Sticky once private:** a node already redacted by a prior run stays
private on every subsequent run, even if its (now-hidden) content would
no longer match the keyword list — re-deriving from an already-scrubbed
stub would misread "no more telltale keywords" as "safe to make public,"
which is backwards. (This was a real bug caught by
`graph-schema/test_enrich.py` during development — a naive first version
reclassified redacted nodes as public on the second run, because the
redaction itself removed the words that triggered private classification
in the first place. Fixed by recovering the decrypted original before
re-classifying/re-tagging on every run, not working off the stub.)

**Second real leak, found and fixed the same night:** redacting a node's
own `label`/`source_file` isn't sufficient — `graphify cluster-only`
derives a community's auto-name from its most-connected node, and since
a node's `id` necessarily still contains its real name (ids can't be
redacted without breaking every edge that references them), a private
node's identity was leaking back in through its *community's* name even
though the node's own `label` correctly read `"[private]"`. Fixed by
`graph-schema/safe_report.py`, which forces any community containing at
least one private node to a generic name (`"Private/Mixed Community N"`)
before regenerating `GRAPH_REPORT.md`/`graph.html`/`community_name`.
Verified by grepping the regenerated report/html for real private labels
after the fix — zero hits (the node `id` itself, e.g.
`ultron_backend_app_fifo_engine`, still appears in `graph.html`'s raw
node list next to `"label": "[private]"` — that's the accepted,
documented tradeoff above, not a re-opened leak of content).

## Full workflow after a graphify rebuild

```
graphify update .   (or a full rebuild)               # graphify's own step
python graph-schema/enrich_visibility.py               # redact + encrypt + tag (system Python, needs `cryptography`)
<graphify's own interpreter> graph-schema/safe_report.py   # regenerate report/html without leaking via community names
```

Two different interpreters on purpose: `enrich_visibility.py` needs
`cryptography`, which graphify's own isolated tool environment doesn't
have; `safe_report.py` needs the `graphify` package itself, which a
plain system Python doesn't have. Not auto-chained into one command
tonight — see "not solved tonight" below.

## What's committed to git vs. what never is

| File | Committed? | Why |
|---|---|---|
| `graphify-out/graph.json` (post-enrichment, private nodes redacted) | Yes | Same as always — now with private content actually stripped out, not just labeled. |
| `graphify-out/tag-index.json` | Yes | No node content, just id lists per tag. |
| `graph-schema/.node_history.json` | Yes | No node content, just ids + timestamps. |
| `graphify-out/private-nodes.enc.json` | **No** — gitignored | Encrypted, but per Module 9's own explicit rule ("private nodes should never enter public repo history"), encryption is not treated as a license to commit it anyway. Defense in depth against a future key compromise. |
| `.env` (holds the encryption key) | **No** — already gitignored | Same as every other secret in this project. |

## Known limitations — not solved tonight

- **This does not retroactively scrub git history.** Everything that was
  committed to `graphify-out/graph.json` and the Obsidian vault *before*
  this script existed is still sitting in past commits in plaintext —
  running this script only protects the working tree and every commit
  from now on. Actually removing it from history is Module 3's job
  (`git filter-repo`), not this one — don't treat Module 4 as having
  already done Module 3's work.
- **No automatic wiring into graphify's own post-commit/post-checkout
  hook, and the two-script, two-interpreter workflow above isn't chained
  into one command.** That hook is generated and managed by
  `graphify hook install`; hand-editing it risks it being silently
  overwritten by a future `graphify` upgrade or re-install. For now, run
  both scripts manually after a `graphify update`/rebuild, in the order
  above (enrich, then safe_report — reversing the order regenerates the
  report from pre-redaction content, reopening both leaks). Wiring this
  into the hook, or at least a single wrapper script, is a reasonable
  follow-up, not done here.
- **No manual override to un-flag a false-positive private node.** Given
  the "sticky once private" design above, a node wrongly caught by the
  broad keyword list stays private until a reclassification tool exists.
  None does yet — this is what the roadmap's own ongoing-maintenance
  item ("periodically re-audit the public/private tagging convention")
  is for; it's an acknowledged gap, not an oversight.
- **The Obsidian export (`graphify export obsidian`) is not yet
  private-aware.** It reads the same `graph.json`, so a private node's
  redacted stub will still generate a `[private].md` file with no real
  content — better than leaking content, but not yet a clean UX. Left
  for whoever next touches the Obsidian export path.
