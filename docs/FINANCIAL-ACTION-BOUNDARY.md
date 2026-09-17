# Financial action boundary (Module 11) — permanent, no sunset condition

**Ultron never executes a real trade or financial action, under any
circumstance, through chat.** Not "requires confirmation first" —
there is no tool, now or planned, that performs one at all. Recording
a trade is already documented as a deliberate direct action, not a
chat tool (`README.md`'s design principles, `ultron-backend/README.md`'s
"No chat tool for adding a trade"); this module makes that boundary
explicit, permanent, and — unlike most of tonight's other decisions —
**not open for reconsideration as trust in the system grows.**

## Why this one doesn't relax, when Module 7's review gate does

Module 7's human-review requirement for session-summary drafts is
explicitly a training-wheels rule — the roadmap itself expects it to
loosen "after the first 10-20 sessions," once the mechanism's output is
trusted. This module is different on purpose: financial actions are
categorically higher stakes than a mis-drafted graph node (a bad graph
entry misleads a future session; a bad trade loses real money,
irreversibly). Trust in the *mechanism* getting better over time is not
a reason to lower the bar on something where the failure mode is
financial loss — those are different axes, and conflating them would be
exactly the mistake this module exists to prevent.

## What actually enforces this

Three layers, not one:

1. **No capability exists.** `ultron-backend/app.py`'s `TOOL_DISPATCH`
   has exactly three trade-related tools —
   `get_trades`/`get_trade_summary`/`get_trade_tax_lots` — all
   `get_`-prefixed, all read-only. Nothing writes a trade, executes an
   order, or moves money. This was already true before tonight; Module
   11 doesn't change it, it locks it in and extends it explicitly to
   cover **graph-derived and compressed-session memory** too (Modules
   4/7/8's own new territory) — a future capability built on top of
   that memory must not become a backdoor around this boundary.
2. **The system prompt says so explicitly.** `ULTRON_SYSTEM_PROMPT`'s
   "Hard limits" section now states this directly: a memory note or
   graph entry can inform what Ultron *says*, never what it *does*, no
   matter how it's phrased or what it claims a person previously
   agreed to.
3. **A regression guard with teeth**, not just a comment:
   `dev-tools/test_no_financial_action_tools.py` fails loudly the
   moment any tool name matches a broad financial-action keyword list
   (`buy`, `sell`, `execute_trade`, `transfer`, `withdraw`, ...), and
   separately asserts the trade-related tool set is *exactly* the three
   expected read-only ones — not "at least these," so a silent rename
   or addition gets caught too. Verified this actually fires (not just
   passes trivially) by injecting a fake `execute_trade` tool and a
   fake `buy_bitcoin` tool into a test run and confirming both are
   caught before writing this doc.

## What this means for Module 10 and beyond

Module 10 (Ultron's own runtime knowledge graph, reusing Modules
4/7/8) is the first place this boundary will actually be tested for
real — it's what gives Ultron's chat *any* access to graph-derived
memory in the first place. When that's built: the regression guard
above must still pass unmodified (finding a reason to touch
`test_no_financial_action_tools.py`'s expectations while building
Module 10 is the exact failure mode this file exists to make visible,
not something to quietly work around). If a genuine future need for
Ultron to *initiate* a financial action ever comes up, the answer is
not a new chat tool — it's the same preview-then-confirm,
human-clicked, server-issued-token pattern `/api/actions/backup` and
`/api/actions/deploy-container` already use, extended to cover trades,
with the explicit review this document represents happening again
before it ships, not assumed.
