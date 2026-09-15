# session-read (Module 8)

The read path — given a task/topic, pull a bounded, relevant slice of
the graph instead of feeding the whole thing into context. Step 31
calls this "the real token-savings mechanism."

## `graphify query` already exists — why build this too

Confirmed in Module 2's gap spec: `graphify query "<question>"` is real,
working retrieval (BFS, vocabulary-expanded, token-budgeted) — not a
gap. This tool is deliberately **narrower** than that, because step 30
names something specific `graphify query` doesn't do: match against
**Module 4's own `tag-index.json`** (not graphify's internal
vocabulary-expansion) and pull "matching nodes plus directly linked
ones only" — one hop, not `graphify query`'s default two. Use
`graphify query` when a broader answer is genuinely wanted; use this
when the point is specifically not feeding the whole graph.

## Usage

```
python session-read/retrieve_context.py "TTS streaming fix"
python session-read/measure_savings.py
```

Output is compact prose (`[seed]`/`[linked]`, label, category,
`PRIVATE` flag), not a JSON dump — the format itself is part of the
token-savings mechanism, not just which nodes get included.

## A real bug this caught, not just a design note

First version matched query words against **every word in every tag**,
including the tag's structural key. Every node carries a
`visibility:public` or `visibility:private` tag by construction
(Module 4's schema) — so the bare word "visibility" matched the literal
string in both tags, on **all 543 nodes**. Query
`"private node encryption visibility"` returned the entire graph: a
reported "95.7% reduction" that was actually 0% useful reduction, since
the slice *was* the graph. Caught by `measure_savings.py` actually
printing the numbers rather than assuming the mechanism worked, fixed
by tokenizing only a tag's **value** (`_tag_words()`, splits on `:` and
ignores the key) — `"visibility:public"` now contributes only
`"public"` as a matchable word, not `"visibility"` too.

## Measured (step 32), real numbers against the real graph

```
Full graph.json: 543 nodes, ~139,970 tokens (estimated, chars/4)

query                                        nodes   ~tokens  reduction
------------------------------------------------------------------------
TTS streaming fix                               18       212      99.8%
private node encryption visibility             322     3,409      97.6%
gitleaks secret scan pre-commit                 15       204      99.9%
three.js Blender pipeline                       16       196      99.9%
trade FIFO engine tax lots                      27       268      99.8%
```

Token counts are `chars/4` — a standard rough estimate, not a real
tokenizer for Claude's own models (none installed here). Stated
plainly: the *ratio* between full-graph and slice is what this number
is for, not a precise absolute count.

The second row (322 nodes, 97.6%) is real OR-based broadening, not a
remaining bug: `"private node encryption visibility"` is four distinct
concepts, matched with OR semantics (any query word matching any tag/
label word seeds a node) rather than AND — a genuinely ambiguous,
multi-concept query legitimately pulls in more. Deliberately not
tightened to AND-matching, which would risk under-feeding a real
question — step 31 explicitly prefers "pull in enough to answer well"
over minimizing tokens when a task is broad.

## "Confirm accuracy hasn't dropped" (step 32) — how this was actually checked

Not a live LLM eval (out of scope, costs real API spend for what Module
8 is really about — the mechanism, not proving downstream answer
quality). Instead: hand-verified recall checks in
`test_retrieve.py` — node ids chosen by inspecting the real graph
*before* running the tool, then asserting the retrieval actually
includes them. Checking a tool's output against ids the same tool
produced would prove nothing; these ids were picked independently.

## Known limitations — not solved tonight

- **OR-matching, not ranked/AND-matching.** A broad query pulls in a
  broad slice by design (see above) — no relevance ranking or "top N
  best matches" trimming exists. Reasonable next step if 97%-ish
  reduction on ambiguous queries ever isn't good enough in practice.
- **`three-pipeline/`'s Python files aren't in the graph yet** —
  noticed while picking recall-check node ids, not something this
  module fixes. graphify's rebuild hook hasn't picked that directory up
  since Module 5/6 were committed; a manual `graphify update .` would
  close this, but it's tangential to Module 8's own deliverable.
- **Not wired into any actual "new session start" trigger** — same
  reality as Module 7's missing hook. This is a callable tool, not
  something that runs itself yet.
