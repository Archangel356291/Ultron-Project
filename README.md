# Ultron

A personal AI-powered home lab system: a Flask backend with an LLM chat
brain (Claude), a single-file HTML/JS dashboard, and a Discord bot — all
three talking to the same backend so there's exactly one implementation
of every piece of logic, not three that can drift apart.

## Structure

```
ultron-backend/       Flask backend — all the real logic lives here
ultron-discord-bot/   Thin remote-control layer; every command is an
                       HTTP call to the backend, no duplicated logic
ultron-dashboard.html Single-file dashboard, opens directly in a browser
dev-tools/            Testing infrastructure (fake SDKs, a real local
                       MCP test server) — not part of the shipped product
```

## Where to start reading

- **Setting this up for the first time?** →
  `ultron-backend/BETA-LAUNCH-CHECKLIST.md` — the consolidated,
  step-by-step path from files to a running, verified system.
- **Are you a beta tester, not the developer?** →
  `ultron-backend/BETA-TESTER-GUIDE.md` — written for you directly, no
  dev background assumed. This is the one to actually send someone.
- **Onboarding a beta tester, or want to see who's helped test this?** →
  `ultron-backend/BETA-TESTERS.md` — the add/remove process and the
  credits roster.
- **Backend API reference, every endpoint and env var?** →
  `ultron-backend/README.md`
- **Discord bot commands and setup?** →
  `ultron-discord-bot/README.md`
- **Remote access (Tailscale)?** →
  `ultron-backend/REMOTE-ACCESS.md`
- **Connecting a Raspberry Pi for home-lab actions?** →
  `ultron-backend/PI-SETUP.md` — phase 1 (network/SSH/Docker) only; the
  backend doesn't talk to a Pi yet
- **Continuing development / writing tests?** →
  `dev-tools/README.md`
- **Dashboard's visual design, pixel-sampled against the reference
  image?** → `ULTRON-DASHBOARD-DESIGN-SPEC.md` (mostly historical — see
  its status note at the top)

## Design principles this codebase has held to throughout

These aren't incidental — they were deliberate, repeated decisions across
many features, and code added going forward should keep holding to them
unless there's a real reason not to:

**Read-only by default, everywhere.** Every chat tool Ultron has is a
read function — no chat tool writes a trade, deploys a container, runs a
backup, or approves an MCP tool. Adding a new *read* tool is low-stakes;
adding anything that writes needs the reasoning below, not just a
function reference in `TOOL_DISPATCH`.

**Destructive host actions require a human-confirmed token, not a
conversational "yes."** `/api/actions/backup` and
`/api/actions/deploy-container` both use a preview-then-confirm flow: the
first call returns a server-issued token and a description of exactly
what would happen; nothing runs until that exact token comes back in a
second call. There is no way to skip this from chat — Ultron will tell
you to use the dashboard instead of pretending it can act. If a new
action ever needs building, this is the pattern to extend, not route
around.

**External/third-party capability (MCP) is opt-in at the tool level, not
the server level.** Connecting an MCP server discovers its tools but
grants nothing — only tools the operator names in that server's
`auto_approve` config become callable, and there is deliberately no
in-conversation approval path (a forged "yes" via prompt injection would
defeat one). See `ultron-backend/README.md`'s "External tools (MCP)"
section for the full reasoning before changing this.

**Real safeguards, not just docs.** Rate limiting, a daily token budget,
a $1.00-lifetime beta-tester spend cap (in real computed dollars, not
tokens), and prompt caching are enforced in code and were each verified
with a test that checks the actual mechanism (a request genuinely
refused, an API call that genuinely never happens) — not just that a
setting exists. Any new cost or safety control added later should meet
the same bar: prove it does the thing, don't just document the intent.

**One source of truth per piece of logic.** The dashboard, the bot, and
Ultron's own chat tools all call the same backend functions — there's no
separate "bot version" of the status check or "dashboard version" of the
trade summary. When adding a feature, the backend function is the
implementation; the dashboard and bot are thin callers of it.

**Financial and legal boundaries are explicit, not implied.** The trade
ledger computes FIFO gain/loss as a factual record-keeping aid — the
disclaimer that it isn't tax advice is embedded in the API responses
themselves (and in exported CSV files as a header comment), not just
shown once in a UI. The system prompt separately and explicitly forbids
Ultron from turning that data into trading or tax advice. Both layers
exist on purpose; don't remove either while trying to simplify things.

**Nothing works until explicitly configured.** Backups, git repo status,
MCP servers, cost budgets — every optional feature is inert by default
(empty env var, empty config) and fails gracefully with a clear "not
configured" message rather than guessing or erroring unpredictably.

## Testing approach

Nothing in this project was accepted as "should work" — everything was
tested against something that behaves like the real dependency:

- Real SQLite for all persistence (activity log, trades, LLM usage).
- Real local git repositories for the Development tab.
- A real, protocol-strict local MCP server (`dev-tools/test_mcp_server.py`)
  for the MCP client — this caught two real protocol-handling bugs that a
  lenient mock likely would have hidden.
- Scriptable fakes for `anthropic`, `discord`, and `aiohttp`
  (`dev-tools/fake_pkgs/`) where the real service genuinely can't be
  reached in a dev/test environment (no real API key, no real Discord
  gateway) — built to match the real SDKs' shape closely enough that code
  written against them works unmodified against the real thing.
- End-to-end passes wiring the real dashboard JS (via a Node `vm` harness)
  against a real running backend process wherever feasible, not just
  backend unit tests in isolation.

If you're extending this in Claude Code: keep testing this way. A change
that "looks right" and a change that's been run against something real
are different bars, and this codebase has consistently held to the
second one.

## Current status

Fully functional beta: backend (24 endpoints, 13 built-in chat tools plus
dynamic MCP tools), dashboard (10 sections, all live-wired), Discord bot
(16 commands). See `ultron-backend/BETA-LAUNCH-CHECKLIST.md` for what's
been verified and what to expect. Known, deliberate gaps — not
oversights — are called out in each README's own "Not included here" or
equivalent section (e.g. no stdio/local-subprocess MCP transport, no
exchange API integration for trades, no CI integration for the
Development tab).

## Contributors

### Core

| Name | Role |
|---|---|
| [@Archangel356291](https://github.com/Archangel356291) | Project owner |
| Claude Code (Anthropic) | AI pair-programming assistant — built, tested, and documented alongside the owner throughout development |

### Beta testers

Credited here as they join — not required, but real work deserves it.
Full process (how someone gets added, each tester's own independently-
revocable token, what to send them) lives in
`ultron-backend/BETA-TESTERS.md`; this table mirrors that file's
roster — update both when it changes.

| Name | Started | Notes |
|---|---|---|
| _none yet_ | | |

No third-party testers yet — beta test #1 (2026-09-13) verified the
`beta_tester` role itself using the owner's own second device over
Tailscale, not an outside tester.

**Inviting someone?** `ultron-backend/BETA-INVITE-MESSAGE.md` has a
ready-to-send, copy/paste invite — the first ask, sent before
`ultron-backend/BETA-TESTER-GUIDE.md` and their token. Once they say
yes, add their name to the roster both here and in `BETA-TESTERS.md`.

### Other contributors

Room for anyone else who pitches in beyond beta testing — code, docs,
bug reports that led to a real fix, whatever the actual contribution
was.

| Name | Contribution |
|---|---|
| ShawneeMacDabs | Set up the messaging platform (Slack) used for easy project information transfer |
| LyraWolf | Funding |
