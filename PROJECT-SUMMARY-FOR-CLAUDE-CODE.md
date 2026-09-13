# Ultron — Project & Conversation Summary (for Claude Code handoff)

This document captures the full arc of a long-running collaborative build —
not just what exists, but why it exists, what was tried, what broke, and
what was deliberately left out. The codebase's own `README.md` (top level)
covers architecture and design principles for working with the code today;
this document is the history behind it, useful for judgment calls on
anything not explicitly covered elsewhere.

## What Ultron is

A personal AI-powered home lab management system for a Windows 11 PC,
built around three pieces that all talk to one Flask backend: a
single-file HTML/JS dashboard, a Discord bot, and the backend's own LLM
chat brain (Claude). The throughline across the whole build: exactly one
implementation of any given piece of logic, with the dashboard and bot as
thin callers of the same backend functions Ultron's own chat tools use.

## Where this started

The original spec proposed four sub-agents:

1. **Ethical hacking agent** (vulnerability analysis, exploit scripting) —
   **refused outright, held firm throughout.** Never built, and the system
   prompt has a standing hard rule against writing exploit code or attack
   tooling "for my own home lab" framings included.
2. **Investment/financial predictive agent** (trade proposals) —
   **refused as specified**, but reinterpreted into something legitimate:
   a personal trade *record-keeping* agent (see below). Specific trading
   advice remains a hard-refused category in the system prompt, including
   about the user's own recorded trades.
3. **Crypto/trade record & tax agent** — built, as FIFO-based
   record-keeping, explicitly not advice.
4. **Home lab monitor & command router** — built first, as the backend's
   core monitoring layer.

A fifth thing that wasn't in the original spec but emerged naturally: a
"coding sub-agent," which became real git status/diff data backing the
dashboard's previously-mock Development tab.

## Build order (chronological, roughly)

1. Dashboard redesigned to match a reference image (navy/amber/orange
   sci-fi aesthetic), all ten nav sections built out, initially with mock
   data throughout.
2. Backend (`app.py`) built: Windows-primary with Linux/Pi fallback,
   system status/containers/storage/systems monitoring, security
   monitoring (auth log, CVE scanning via Docker Scout), and the chat
   brain wired to Claude with a tool-use loop.
3. Discord bot built as a thin HTTP client of the same backend — no
   duplicated logic, ever.
4. **Real action endpoints** (backup, deploy-container) — the first
   things that mutate the host. Built with a two-step preview-then-confirm
   flow using a server-issued token; deliberately excluded from chat's own
   initiative (Ultron will tell you to use the dashboard, never fake
   compliance).
5. **Real activity log** — SQLite-backed, replacing a mock "recent
   activity" feed, logging real backups/deploys/CVE scans with success/
   failure detail.
6. **Development tab wired to real git data** — status and diffs for
   configured repos, with the first *parameterized* chat tool
   (`get_repo_diff` takes a `repo` argument), which required changing the
   core tool-dispatch mechanism to pass through arbitrary kwargs.
7. **Trade record-keeping** — manual entry, SQLite-backed, FIFO realized
   gain/loss calculation. Heavy emphasis on the "not tax advice" boundary:
   disclaimer text embedded in every API response and in exported CSV
   files as a header comment, not just shown once in a UI. Later extended
   with per-disposal tax-lot detail (acquisition date, holding period,
   short/long-term classification) via a refactor into a single shared
   `_fifo_engine()` — verified against the *exact* same hand-computed
   scenarios as before the refactor to prove zero behavioral drift.
8. **CSV export** for trades (transactions + tax-lots formats), wired into
   both the dashboard (via fetch+Blob, since a plain download link can't
   carry an auth header) and the Discord bot (as a real file attachment).
9. **Remote access documentation** (`REMOTE-ACCESS.md`) — Tailscale setup,
   researched fresh rather than assumed, including a genuinely useful find
   (Windows Firewall rules apply to all profiles by default when
   `-Profile` is omitted, which the project's existing firewall rule
   already was) and later extended with Tailscale ACL/tags/grants
   guidance, including a real nuance (`autogroup:self` doesn't cover
   tagged devices) that would've been easy to get subtly wrong.
10. **Discord bot parity** — every feature above got a matching bot
    command as it was built (`/repos`, `/diff`, `/trades`, `/portfolio`,
    `/export`, `/backup`, `/deploy` with Confirm/Cancel buttons).
11. **Cost controls** — prompt caching (system prompt + tools + growing
    conversation history all get cache breakpoints), a real daily token
    budget with an actual hard stop (verified: zero API calls happen once
    over budget, not just a warning), a request rate limiter, configurable
    response length, and full usage visibility (`/api/chat/usage`, a
    `get_llm_usage` chat tool, a dashboard card, a `/usage` bot command).
12. **MCP (external tool/plugin) support** — the most security-sensitive
    feature built. Full writeup below.
13. **Full project audit** — re-verified everything fresh (not from
    memory): all 20 backend routes hit on a live server, dashboard
    structural checks, bot command registration, documentation-vs-code
    drift across every README, and a holistic safety re-review (no write
    function present in the chat tool dispatch table, action endpoints
    still token-gated, MCP approval gate still enforced, every Discord
    command still has its auth check).
14. **Beta launch checklist + startup scripts** — consolidating 13+
    scattered environment variables into one step-by-step path, plus
    fill-in-the-blank PowerShell scripts with placeholder-detection guards
    (which themselves caught a real UX trap — see bugs list below).
15. **Full project packaged for Claude Code** — this handoff.

## MCP support, in more depth (the highest-stakes feature built)

The user asked for the AI to be able to "use other plugins and tools from
other sources, safe and secure." The design landed on:

- **Discovery and execution are separate.** Connecting a server discovers
  its tools but grants nothing. Only tools an operator names in that
  server's `auto_approve` list in a config file become callable — not
  "offered and refused," genuinely absent from what the model can see.
- **No in-conversation approval path, on purpose.** A tool result from an
  already-approved tool is untrusted external data by definition, and
  it's fed straight back into the model's context. Letting the model act
  on a conversational "yes" would let a prompt injection forge that
  consent. The only path to execution is the operator's static config —
  full stop, deliberately with no clever workaround.
- **Protocol details were researched, not assumed** — JSON-RPC shapes,
  the `initialize` → `notifications/initialized` handshake, the
  `Mcp-Session-Id` header convention — verified against current spec
  documentation before writing code.
- **Tested against a real local MCP server**, not a mock — this is
  `dev-tools/test_mcp_server.py`, a real Flask app implementing the real
  protocol with strict `assert`s on request shape. This caught two real
  bugs (see below) that a lenient mock would likely have hidden.

## Real bugs found during development (worth knowing about)

These are the interesting ones — caught by testing against realistic
behavior rather than assuming code was correct because it looked right:

- **MCP: empty notification response mishandled.** A `202 Accepted` with
  no body is the *correct* response to `notifications/initialized`
  (JSON-RPC notifications don't get a response payload), but the client
  unconditionally tried to JSON-parse every response body, raising a
  false error on the empty one. Fixed by treating an empty body as `{}`
  rather than a parse failure.
- **MCP: response-size cap applied at the wrong layer.** The safety cap
  meant to limit what reaches the model was being applied to the *raw
  HTTP bytes read*, truncating mid-JSON for any real-sized response and
  corrupting the structure entirely. Fixed by separating a generous raw
  read ceiling (2MB, a backstop against a truly malicious response) from
  the actual user-facing content cap (4,000 chars), which is now applied
  *after* successful JSON parsing, to the extracted text only.
- **Discord bot: `backend_get` showed raw response text on errors**
  instead of parsing the JSON `error` field, unlike `backend_post` and
  `backend_get_csv` which already did this correctly — meaning nearly
  every read-only command (`/status`, `/repos`, `/trades`, etc.) was
  showing uglier error messages than necessary. Found while building
  `/usage` and testing its error path; fixed to match the established
  correct pattern, verified the fix improved (not broke) every command
  that uses it.
- **Discord bot: field-truncation off-by-N.** `value[:1000] + suffix`
  where the suffix itself was 33 characters — total 1033, over Discord's
  hard 1024-character field limit. Fixed to compute the truncation point
  including the suffix length.
- **Backend: tool-registration ordering bug.** `get_llm_usage` was
  initially defined *after* `TOOL_DISPATCH` referenced it — would have
  raised `NameError` at import time. Caught by the routine post-edit
  syntax check, before it ever ran.
- **Startup script UX trap:** `ANTHROPIC_API_KEY` was initially left
  *active* in the fill-in-the-blanks startup script with a placeholder
  value, unlike every other optional line (which are commented out by
  default). An unedited placeholder there would cause a confusing
  authentication error at runtime instead of the clean "not configured"
  message the app gives when the variable is genuinely unset. Fixed to
  match the commented-out-by-default pattern used everywhere else.
- **Config value hardening:** `ULTRON_LLM_MAX_TOKENS` and
  `ULTRON_CHAT_RATE_LIMIT_PER_MINUTE` originally had no floor — a
  misconfigured `0` or negative value would have silently broken chat
  entirely (zero-length responses, or a rate limit blocking everything).
  Both now clamp to a minimum of 1.

None of these were hypothetical "could theoretically happen" issues —
each was actually reproduced, root-caused, and fixed, with a test added
or updated to catch a regression.

## Testing philosophy applied throughout

Not "looks right" — "verified against something that behaves like the
real thing":

- Real SQLite for all persistence, real local git repos for the
  Development tab, a real protocol-compliant local MCP server for the MCP
  client.
- Scriptable fakes (`dev-tools/fake_pkgs/`) for `anthropic`, `discord`,
  and `aiohttp` where the real service genuinely isn't reachable in a dev
  environment — built to match real SDK shapes closely enough that code
  written against them needs no changes for the real thing.
- End-to-end passes running the actual dashboard JavaScript (via a Node
  `vm` sandbox) against an actual running backend process, not just
  backend unit tests in isolation.
- Regression suites re-run after every change that touched shared/core
  code (the tool-dispatch mechanism, the FIFO engine, `backend_get`) to
  prove old behavior didn't silently change.

## Explicit boundaries maintained across the whole project

- No exploit code or attack tooling, any framing.
- No specific trading/investment advice, including about the user's own
  recorded trades — factual reporting only.
- No chat-initiated host mutation, ever — backup and deploy-container are
  dashboard-only actions requiring a human-confirmed token.
- No trade-record writing via chat — recording a financial transaction is
  a deliberate direct action, same reasoning as the action-endpoint
  boundary.
- No conversational bypass for MCP tool approval — the operator's static
  config is the only path to execution.
- Every optional feature is inert until explicitly configured, and fails
  with a clear message rather than guessing.

## Known, deliberate gaps (not oversights)

- No stdio/local-subprocess MCP transport — only HTTP-based MCP servers,
  since spawning an arbitrary local process from config is a meaningfully
  bigger risk than an HTTP call.
- No exchange API integration for trades — manual entry only; adding real
  exchange credentials and rate-limit handling was judged out of scope.
- No CI integration for the Development tab — git status/diff only, no
  build/test status.
- No raw WireGuard setup guide — Tailscale only, since it's built on
  WireGuard and meaningfully easier to set up correctly.
- No automatic background retry for unreachable MCP servers within a
  running process — discovery happens once, lazily, on first chat use;
  a restart retries.

## Current state

Fully functional beta, audited clean as of the last pass: 20 backend
routes, 13 built-in chat tools (plus dynamic MCP tools when configured),
a fully live-wired dashboard across all 10 sections, and a 15-command
Discord bot. Every deliverable file was confirmed byte-identical between
what was tested and what's in the final package. `ultron-backend/
BETA-LAUNCH-CHECKLIST.md` is the current source of truth for what's been
verified end-to-end and what a first real run should expect.

## Suggested entry points for continuing work

- Read the top-level `README.md` first (architecture + design principles
  — written for exactly this handoff).
- `dev-tools/README.md` for how to keep testing without real credentials.
- Each component's own README for the endpoint/command-level reference.
- If extending anything touching money (trades), actions (backup/deploy),
  or external tools (MCP), re-read that feature's "why" in this document
  before changing the boundary — these were the most deliberated parts of
  the whole build, not incidental design.
