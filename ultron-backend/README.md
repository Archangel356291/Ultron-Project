# Ultron home lab backend

A small Flask API that reports real CPU/memory/temperature, Docker container
status, disk usage, and pending updates — the data the dashboard's Home,
Home Lab, and Systems panels currently mock.

Primary target: **Windows 11**, on the Cyberpower PC. It also runs unmodified
on Linux (e.g. the Raspberry Pi 400) — the platform-specific checks (temp
sensors, update checks) detect the OS automatically.

## Setup (Windows 11, PowerShell)

Requires Python 3.10+ ([python.org](https://www.python.org/downloads/) — check
"Add python.exe to PATH" during install) and Docker Desktop if you want the
Home Lab / container panel to work. This isn't just a suggestion: the
Anthropic SDK (v1.0+, needed for `/api/chat`) requires 3.10+ and `pip
install` will simply fail to find a compatible version on anything older,
so check `python --version` first if you're not sure what's installed.

```powershell
cd ultron-backend
python -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

If `Activate.ps1` is blocked by PowerShell's execution policy, run once as
admin: `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`.

Set an API token (required — the app won't start without one) and run it:

```powershell
$env:ULTRON_API_TOKEN = -join ((48..57)+(97..102)|Get-Random -Count 32|%{[char]$_})
python app.py
```

The token above is only set for the current PowerShell session. Save it
somewhere (password manager) so you can reuse it — you'll need it in every
`Authorization: Bearer <token>` request, including from the dashboard.

**Beta testers each get their own, weaker token** — never your real
`ULTRON_API_TOKEN`, and never one token shared between people. Set
`ULTRON_BETA_TOKENS` to a comma-separated list of `name:token` pairs
(generate each token the same way as above, run once per person):

```powershell
$env:ULTRON_BETA_TOKENS = "alice:$(-join ((48..57)+(97..102)|Get-Random -Count 32|%{[char]$_})),bob:$(-join ((48..57)+(97..102)|Get-Random -Count 32|%{[char]$_}))"
```

Any of those tokens authenticates as the `beta_tester` role: chat (full)
plus view-only trading data (`/api/trades`, `/api/trades/summary`,
`/api/trades/tax-lots`) — everything else 403s, including via chat's own
tool use, not just the raw HTTP routes. Because each person has their own
token, removing one entry revokes just that person, and `/api/whoami`
reports back which tester is connected (`{"role": "beta", "name": "alice"}`)
so requests aren't anonymous within the role. Leave `ULTRON_BETA_TOKENS`
unset and the role doesn't exist at all — see `BETA-TESTERS.md` for the
full add/remove process and the credits roster. The dashboard hides
admin-only nav/controls automatically once it detects this role via
`/api/whoami`, but that's convenience — the 403s are what actually
enforce it.

Optionally, to enable the AI Assistant chat panel, also set an Anthropic API
key before starting the server:

```powershell
$env:ANTHROPIC_API_KEY = "sk-ant-..."
```

Without it, every other endpoint works fine — `/api/chat` just returns 503
until you set this and restart.

The server listens on `0.0.0.0:5000`.

### Allow it through Windows Firewall

To reach it from another device on your network (phone, laptop viewing the
dashboard), open port 5000 for inbound traffic:

```powershell
New-NetFirewallRule -DisplayName "Ultron Backend" -Direction Inbound -Protocol TCP -LocalPort 5000 -Action Allow
```

## Endpoints

| Route            | Returns                                           |
|-------------------|----------------------------------------------------|
| `GET /api/health`  | `{"ok": true}` — no auth, for uptime checks        |
| `GET /api/status`    | CPU %, memory %, temp, uptime, container counts     |
| `GET /api/containers` | Per-container name, image, status, cpu, mem        |
| `GET /api/storage`      | Disk usage for the drives listed in `STORAGE_MOUNTS` |
| `GET /api/systems`       | Pending updates, temp, uptime, load average        |
| `GET /api/activity`       | Persistent log of real events — backups, deploys, CVE scans |
| `GET /api/memory`         | Ultron's saved memory notes (most recent first, or `?query=` to search) |
| `GET /api/brain-graph`    | The Brain vault's graph for the dashboard's "What Ultron knows" panel: nodes by kind, links, counts, learned-per-day (admin only) |
| `GET /api/crypto/market`  | Oracle: read-only crypto spot prices + 24h change (CoinGecko free API) for ledger coins plus BTC/DOGE. Reference only, never a trade (admin only) |
| `GET /api/stats/rollup`   | Tally: daily efficiency rollup — LLM spend/tokens, agent task load, activity mix, containers running (admin only) |
| `GET /api/dev/repos`       | Git status (branch, dirty/clean, last commit) for configured repos |
| `GET /api/dev/repos/<repo>/diff` | Uncommitted diff for one configured repo             |
| `GET/POST /api/trades`     | Your manually-recorded trade ledger — list or add    |
| `DELETE /api/trades/<id>`   | Remove one trade record                            |
| `GET /api/trades/summary`    | Realized gain/loss per asset (FIFO) — see below     |
| `GET /api/trades/tax-lots`    | Per-disposal FIFO detail (acquisition date, holding period, term) |
| `GET /api/trades/export`       | CSV download — transactions or tax-lots format      |
| `GET /api/security/auth-log` | Recent login attempts (fast)                    |
| `GET /api/security/cve-scan` | CVE scan of running containers' images (slow — see below) |
| `GET /api/security/threats` | **Admin-only.** Sentinel's live watchdog view — active findings, last check — see below |
| `GET /api/briefing` | **Admin-only.** Ultron's deterministic read of the host (the Home "Ultron's read" card) |
| `GET /api/agents` | **Admin-only.** Every agent's role, permissions, health, current task, spend vs cap — see `AGENT_CAPABILITIES_AND_GOVERNANCE.md` |
| `GET/POST /api/agents/tasks`, `PATCH /api/agents/tasks/<uid>` | **Admin-only.** The agent task ledger and its lifecycle (evidence required to complete, approval required for high-risk) |
| `GET /manifest.webmanifest`, `GET /sw.js` | Installable-app manifest and service worker (no auth; the worker never caches `/api/*`) |
| `GET /fonts/<file>`, `GET /pixel-assets/<file>` | Static dashboard assets (no auth; self-hosted typefaces, sprites, app icons) |
| `POST /api/actions/backup` | **Mutates the host.** Two-step confirm — see below    |
| `POST /api/actions/deploy-container` | **Mutates the host.** Two-step confirm — see below |
| `POST /api/chat`          | Chat with Ultron — see below                       |
| `GET /api/chat/usage`      | Today's real token usage and budget status, plus per-beta-tester spend — see Cost controls |
| `GET /api/whoami`           | Your own role/name; a beta tester also gets their spend vs. the cap |
| `GET /api/connections`       | **Admin-only.** Who's connected right now — name, role, device count, last seen |
| `GET /api/mcp/servers`      | Configured external tool servers and their tools — see External tools |

Storage paths come from `ULTRON_STORAGE_MOUNTS` as `label=path,label=path`
(default `C:=C:\` on Windows). **In Docker this is required**: the
container cannot see the host's drives except where `docker-compose.yml`
bind-mounts them read-only (`C:\ → /host/c`, `D:\ → /host/d`), and compose
sets `ULTRON_STORAGE_MOUNTS=C:=/host/c,D:=/host/d` accordingly. Without it
the container reported its own 1 TB virtual disk as "root" — which is what
the Storage panel, `get_storage_usage` and the briefing showed until
2026-09-16.

By default the API allows requests from any origin (`ULTRON_ALLOWED_ORIGIN`
defaults to `*`), which is fine while you're testing on your own network.
Once the dashboard has a fixed address, set
`$env:ULTRON_ALLOWED_ORIGIN = "http://your-dashboard-host:port"` to restrict it.

## Trade records (`/api/trades*`) — this is not tax advice

> **This is a personal record-keeping tool. It is not tax, legal, or
> financial advice, and it is not connected to any exchange.** You type in
> what you traded; nothing here fetches prices, suggests a trade, or knows
> anything about the market beyond what you've entered.

What it does:

- **You enter trades manually** — asset, buy/sell, quantity, price, an
  optional fee and exchange name, and the trade date. `POST /api/trades`
  validates everything (numeric fields, a real `buy`/`sell`, a parseable
  date) before saving.
- **`GET /api/trades/summary` computes realized gain/loss using simplified
  FIFO** (first-in-first-out) accounting: each sell is matched against your
  oldest recorded buys first. Fees are folded into the effective per-unit
  cost (on buys) or proceeds (on sells) at the time of that trade — a
  deliberate simplification, not a precise tax-lot allocation.
- **If you record a sell that exceeds what you've recorded buying**, the
  summary still computes gain/loss for whatever it *could* match, and adds
  a plain-language warning noting the discrepancy — it never silently
  produces a number that doesn't add up.
- **`GET /api/trades/tax-lots` breaks that same FIFO matching down to
  per-disposal detail** — one row per sell matched against one consumed
  buy lot, with the acquisition date, holding period in days, and a
  short/long-term classification (>365 days held = long-term, the US
  convention). This is what real tax reporting (e.g. a Form 8949-style
  worksheet) actually needs — the aggregated summary intentionally doesn't
  carry this much detail, most callers just want the totals. Both come
  from the exact same FIFO computation internally (`_fifo_engine()`), so
  they can never disagree with each other.
- **`GET /api/trades/export?format=transactions` or `?format=tax-lots`**
  downloads either view as a CSV file — the disclaimer is written into the
  file itself as a header comment, not just shown in the UI around it, so
  it survives being opened in Excel or handed to someone else. The
  dashboard's Crypto tab has "Export CSV" and "Export tax report" buttons
  that trigger these downloads directly (via `fetch` + a blob URL, since a
  plain download link can't carry the `Authorization` header this needs).
- Every response from `/api/trades*` includes the disclaimer text above
  verbatim, so it can't get lost between the API and whatever's displaying
  it — the dashboard shows it directly under the trade history table,
  pulled from the real API response rather than hardcoded.

What it deliberately doesn't do:

- **No exchange integration.** No API keys for Coinbase/Binance/etc., no
  automatic import — that's a meaningfully bigger scope (credential
  storage, rate limits, exchange-specific formats) than this project has
  taken on.
- **No chat tool for adding a trade.** Ultron can read and report on your
  recorded trades (`get_trades`, `get_trade_summary`, `get_trade_tax_lots`)
  — real numbers, never invented — but adding a financial record is
  something you do directly, the same reasoning that keeps
  `/api/actions/backup` and `/api/actions/deploy-container` out of chat's
  own initiative. There's no chat tool for the CSV export either, for the
  same reason a file download doesn't map cleanly onto a chat reply.
- **No trading advice, ever, even about your own data.** Ultron can tell
  you your realized BTC gain is $X; it will not tell you whether to buy,
  sell, or hold anything — that boundary is enforced in the system prompt,
  not just documented here.

## Development (`/api/dev/*`)

Read-only git status for the repos you point it at — this is what backs the
dashboard's Development tab (which used to be entirely mock data) and gives
Ultron something real to check when you ask it about your code.

```powershell
$env:ULTRON_CODE_REPOS = "C:\Users\you\ultron-core;C:\Users\you\lab-infra"
```

(Semicolon-separated on Windows, colon-separated on Linux — same convention
as `ULTRON_BACKUP_SOURCES`.)

- `GET /api/dev/repos` — for each configured repo: current branch, whether
  there are uncommitted changes, and the most recent commit (hash, message,
  author, relative time).
- `GET /api/dev/repos/<repo>/diff` — the uncommitted diff for one repo,
  capped at 8,000 characters. `<repo>` is matched only against the
  configured repos' folder names — there's no way to point this at an
  arbitrary path on the host, from the URL or from a chat tool call.
- Both are **read-only**. Nothing here stages, commits, or pushes anything
  — this reports on code, it doesn't touch it. If you want Ultron to
  actually change files or commit on your behalf, that's a different,
  much more carefully-scoped feature this project doesn't have yet.
- Both are available to Ultron's chat (`get_repo_status`, `get_repo_diff`)
  — fast enough, and safe enough being read-only, that there's no reason
  to keep them out the way the CVE scan is kept out.

## Activity log (`/api/activity`)

A persistent record of real events, backed by a SQLite file (`ultron.db` in
the backend folder by default; override with `ULTRON_DB_PATH`). Unlike
everything else in this backend, this survives a restart — it's the actual
history the dashboard's "Latest Activity" panel used to fake.

What it logs, and — just as deliberately — what it doesn't:

- **Backups, container deployments, and CVE scans** — every real outcome,
  success or failure, with enough detail to know what happened without
  digging through terminal output.
- **Not chat.** Conversations with Ultron are never written here. This is a
  log of actions the system took, not a transcript of what you asked it.
- **Not routine polling.** A CVE scan that returns from cache (see below)
  doesn't get a new log entry — only an actual fresh scan does. Otherwise
  every dashboard poll would flood this with noise.

`GET /api/activity?limit=N` returns the most recent `N` events (default 20,
capped at 100). It's also available to Ultron's chat as a read-only tool
(`get_recent_activity`) — fast enough that, unlike the CVE scan, there's no
reason to keep it out of chat.

## Action endpoints (`/api/actions/*`) — read this before using either one

These are the only two endpoints in this backend that change anything on
the host. Both use the same **preview, then confirm** pattern:

1. `POST` with no `confirm_token` — validates the request and returns a
   `preview` of exactly what would happen, plus a `confirm_token` that
   expires in 5 minutes (`ACTION_TOKEN_TTL_SECONDS`).
2. `POST` again with `{"confirm_token": "..."}` — actually does it.

A stray request, a browser retry, or a replayed request can't trigger
either action by itself — nothing runs without that second explicit call
with a token the backend itself issued. Tokens are single-use.

**Neither action is available to Ultron's chat.** `/api/chat`'s tools are
all read-only; an LLM deciding to call a tool is not the same thing as a
human clicking "confirm," and these are exactly the two actions where that
distinction matters. If you ask Ultron via chat to deploy something or run
a backup, it'll tell you to use the dashboard instead — that's intentional.

### `POST /api/actions/backup`

Archives the directories in `ULTRON_BACKUP_SOURCES` into
`ULTRON_BACKUP_DEST` as timestamped zip files. Both are unset by default —
without them, this returns a clear "not configured" error rather than
guessing what you want backed up:

```powershell
$env:ULTRON_BACKUP_SOURCES = "C:\Users\you\docker-volumes;C:\Users\you\configs"
$env:ULTRON_BACKUP_DEST = "D:\Backups"
```

(On Windows, separate multiple sources with `;`; on Linux, with `:`.)

Checks free disk space at the destination before archiving and refuses if
there isn't enough room, rather than filling the disk mid-backup.

### `POST /api/actions/deploy-container`

Runs `docker run -d` with a **deliberately small surface**: image, container
name, port mappings, and environment variables — nothing else. No volumes,
no `--privileged`, no host networking, no custom entrypoint. Request body:

```json
{"image": "nginx:latest", "name": "my-nginx", "ports": {"80": "8080"}, "env": {"FOO": "bar"}}
```

`ports` maps container port → host port. Rejects: image references that
look malformed, container names with anything other than letters/digits/
`.`/`_`/`-`, ports outside 1–65535, invalid environment variable names, and
container names that already exist (checked both at preview time and again
right before execution, since time passes between the two).

## Security monitoring (`/api/security/*`)

Both endpoints are **read-only** — recognition and reporting, not action.
There's no auto-blocking, no firewall changes, nothing that touches the
system beyond reading logs and querying public vulnerability data.

### `/api/security/auth-log`

Recent login attempts (successes and failures), platform-aware:

- **Windows**: reads the Security event log (event IDs 4624/4625) via
  PowerShell. **This normally requires administrator privileges.** If the
  backend isn't running elevated, this returns a clear error saying so
  rather than a cryptic failure — it won't crash the rest of the API.
- **Linux**: reads the systemd journal for `sshd` success/failure lines via
  `journalctl`. No special privileges needed for this one.

Fast (a few hundred ms), safe to call whenever you want — but the dashboard
still only calls it on a manual "Refresh" click, not on the 15-second
auto-poll cycle, since there's no need to hit it that often.

### `/api/security/cve-scan`

Scans the images of currently running containers for known CVEs, via
`docker scout cves`. A few things to know before you rely on this:

- **Requires a one-time, free Docker Hub login.** Docker Scout ships with
  Docker Desktop but won't do anything until you run `docker login` once
  in a terminal. Without it, this endpoint returns a clear message telling
  you exactly that, instead of a cryptic failure.
- **This is genuinely slow** — tens of seconds per image is normal.
  Results are cached in memory for `CVE_SCAN_CACHE_SECONDS` (1 hour by
  default) so repeated requests don't re-scan every time; pass
  `?force=true` to bypass the cache and scan fresh.
- Capped at `CVE_SCAN_MAX_IMAGES` (8) images per request and scans only
  currently *running* containers — a stopped container's image isn't
  scanned.
- **This endpoint is deliberately not part of Ultron's chat tools.** A slow
  scan inside a chat turn would blow well past reasonable response times,
  so `/api/chat` can check auth-log but not trigger a CVE scan — that stays
  a manual dashboard/API action.
- The SARIF parsing here is defensive by design: Docker Scout's exact
  output schema isn't something that could be verified against a live scan
  while building this, so parsing failures degrade to an honest "couldn't
  parse" result rather than guessing.

### `/api/security/threats` — Sentinel, the watchdog subagent

Sentinel is a background thread (every `ULTRON_SENTINEL_INTERVAL_SECONDS`,
default 300; `0` disables it) that re-reads what this backend can already
see and **uses no LLM tokens at all**: active sign-in lockouts and
repeated failed sign-ins, containers that aren't running, and critical
CVEs in the last scan's cache (it never starts a scan itself — that stays
the manual "Scan now"). It writes to the activity log **only on a
change** — a finding appearing (`warning`, or `error` for lockouts and
critical CVEs, which classify as CRITICAL) or clearing (`success`) — so
the Home feed, the Security tab's Sentinel card, and the pixel room's
Sentinel desk react to real events, never to polling. This endpoint
returns the current view: `enabled`, `interval_seconds`, `last_run`,
`active_findings` (`key`/`status`/`summary`), `active_count`, and the
list of `checks`. Admin-only. The same view is Ultron's `get_threat_summary`
chat tool, so "anything wrong right now?" is a cheap, honest answer.

## Ultron's brain (`/api/chat`)

`POST /api/chat` is the AI Assistant panel's backend — a Claude API chat loop
that's grounded in this backend's own data rather than guessing:

- Request body: `{"message": "...", "history": [...]}`. `history` is
  whatever this endpoint returned last time (an opaque list of Claude
  message objects) — the server itself is stateless, so the browser is
  responsible for resending it each turn. Omit it (or send `[]`) to start a
  fresh conversation.
- Response body: `{"reply": "...", "history": [...], "tools_used": [...]}`.
  Store the returned `history` and send it back on the next call.
- Ultron can call fifteen built-in tools — `get_system_status`,
  `list_containers`, `get_storage_usage`, `get_pending_updates`,
  `get_auth_log`, `get_recent_activity`, `remember_note`, `recall_notes`,
  `get_repo_status`, `get_repo_diff`, `get_trades`, `get_trade_summary`,
  `get_trade_tax_lots`, `get_llm_usage`, and `get_mcp_servers` — which
  (aside from the memory pair below) are the exact same functions the GET
  routes above use, so its answers reflect real numbers, not invented
  ones. CVE scanning is deliberately not one of these tools — see
  "Security monitoring" above for why. Adding a trade record is
  deliberately not one either — see "Trade records" above, and neither is
  the CSV export, since a file download doesn't map onto a chat reply.
  `get_repo_diff` is the first tool that takes a real parameter (`repo`)
  — the tool-calling loop passes whatever arguments the model supplies
  straight through as keyword arguments, so a handler function's own
  signature is what defines what it will accept. On top of these fifteen,
  any approved external tools from `ULTRON_MCP_CONFIG` are added
  dynamically, namespaced `mcp__<server>__<tool>` — see "External tools
  (MCP)" above for what "approved" means and why there's no way around it
  from inside a conversation.
- `remember_note` / `recall_notes` are a small persistent notebook — a
  short distilled fact or preference Ultron chooses to save so it can
  recall it in a later conversation, not a transcript log (chat content
  is still never logged anywhere). Capped at 500 characters per note and
  200 notes total (oldest trimmed first); admin-only, like `get_mcp_servers`.
- Other than `remember_note`, Ultron has **no ability to take actions
  through chat**, even though the backup and deploy-container actions now
  exist on the dashboard. If asked to deploy something or run a backup via
  chat, it says so and points to the dashboard action instead of
  pretending to comply — see "Action endpoints" above for why that's a
  deliberate line, not a gap.
- It refuses to write exploit code or attack tooling, and won't give
  specific trading/investment advice — this is enforced in the system
  prompt, not just a suggestion.
- Each turn is capped at 5 tool calls (`MAX_TOOL_ITERATIONS` in `app.py`)
  and conversation history is capped at 40 messages
  (`MAX_HISTORY_MESSAGES`) — see "Cost controls" below for the full set of
  real, enforced spending safeguards this backend applies, not just this
  turn-level cap.
- Model defaults to `claude-sonnet-5`; override with `ULTRON_LLM_MODEL` if
  you want to point it at a different model.
- **Economy mode** — a per-request `"lite": true` in the `/api/chat` body
  (the dashboard's Settings → "Economy mode" switch sends it) answers with
  `ULTRON_LITE_MODEL` (default `claude-haiku-4-5`, about half the price),
  `max_tokens` capped at 400, at most 2 tool rounds, and only the six
  basic read tools (status, containers, storage, updates, recall notes,
  recent activity). It never widens a role's tool set — a beta tester in
  economy mode gets the intersection of both allowlists — and every other
  safeguard is unchanged. The response carries `"lite": true/false` so the
  caller can label the reply. Usage is priced at the lite model's rate, so
  the saving shows as real dollars in `/api/chat/usage`.
- **Deep thought mode** — `"deep": true` (Settings → "Deep thought")
  answers with `ULTRON_DEEP_MODEL` (default `claude-opus-5`, about 2.5×
  Sonnet per token), `max_tokens` at least 2048, and up to 8 tool rounds.
  Admin-only — a beta tester's `deep` is ignored — and it wins over `lite`
  if both are sent. The response echoes `"deep"`.
- **Learn from our conversations** — `"learn": true` (Settings switch,
  opt-in, admin-only): after the reply, one small call to the lite model
  asks whether the exchange held *one* fact or preference worth
  remembering next month; if so and it isn't already in the notebook, it
  is saved through `remember_note` and an activity entry ("Ultron
  remembered: …") is logged. Runs in a background thread so the reply is
  never delayed (`ULTRON_LEARN_INLINE=1` makes it synchronous, for tests).
  Live numbers, greetings and web-search content are excluded by the
  learner's instructions.
- **Where his knowledge lives** — the directory holding `ultron.db`
  (`ULTRON_DATA_DIR`, `D:\ultron's Brain&Knowledge` on the owner's host)
  also gets `chat logs\dashboard\YYYY-MM-DD.txt` and
  `chat logs\discord\YYYY-MM-DD.txt` (web and Discord conversations kept
  apart, decided by the `speaker` label in one place) and
  `knowledge\memory-notes.md`, the whole memory notebook rewritten on
  every save so it can be read — or opened in Obsidian — without a SQLite
  client. `dev-tools/test_deep_learn_brain.py` covers all three.
- **Ultron's Brain — an Obsidian vault and a graphify root.** That same
  folder is registered in Obsidian as its own vault (deliberately separate
  from the *Ultron Project* vault: the project is where he is developed,
  the Brain is what he knows). Chat logs are Markdown with one heading per
  exchange carrying the person's words; every memory note is its own page
  under `knowledge\notes\` with `[[wikilinks]]` for each `memory_edges`
  row, so Obsidian's graph view *is* his memory graph (gold = notes,
  blue = dashboard talks, violet = Discord). `dev-tools/brain-graph-refresh.ps1`
  runs `graphify update` over the vault hourly (scheduled task "Ultron
  Brain Graph"; AST-only, no API key, no tokens); the backend reads
  `graphify-out\graph.json` from it for the `recall_from_brain` tool and
  adds matching past conversations to the situational context — so "what
  did we say about X" is answered from the vault before any model call.
- Requests to the Anthropic API time out after 60s by default (override with
  `ULTRON_LLM_TIMEOUT_SECONDS`), and errors are mapped to distinct, useful
  responses instead of one generic failure: a bad/rejected key comes back
  as a 502 that says so explicitly, rate limiting comes back as 429 (so a
  client could reasonably back off and retry), network issues are
  distinguished from API-side errors, and anything truly unexpected is a
  500 rather than crashing the process.
- The server runs with `threaded=True` specifically because of this
  endpoint — a chat call can take several real seconds waiting on the LLM,
  and without it every other request (the dashboard's status polling,
  for instance) would queue up behind it instead of being served
  concurrently. Verified with an actual concurrent-request test, not just
  assumed.

**Before the beta key goes in:** the only thing this needs from you is
`ANTHROPIC_API_KEY` set to a real key — everything above (validation, error
mapping, timeouts, concurrency) is already in place and doesn't change when
the key does. If you hit an error once it's live, the response's `error`
field should already tell you which of the above it is rather than a bare
stack trace.

### Ultron's read of the room (`/api/briefing`, `get_briefing`, situational context)

Before every admin turn, `run_ultron_chat` adds a second system block —
after the cached static prompt, small and uncached — assembled by this
backend from its own data: the live briefing (CPU/memory/containers/
uptime, storage headroom, anything running well above its 24-hour
baseline, Sentinel's active findings, warning/error events in the last
day, memory size, ideas awaiting review) plus the memory notes related to
what was just said (`recall_related_notes`). The block states that it is
information, never instruction. The result: Ultron opens already knowing
the numbers and already remembering you, usually without a tool round —
cheaper, and it reads as someone who has already looked. Beta testers
never receive it (host state and memory are admin-only). The same
briefing is the Home tab's "Ultron's read" card, the admin-only
`GET /api/briefing`, and the `get_briefing` tool (also in Economy mode).
No LLM call anywhere in it. `dev-tools/test_situational_context.py`.

## External tools (MCP) — read this before connecting anything

Ultron can use tools from external servers over the
[Model Context Protocol](https://modelcontextprotocol.io) — the same
mechanism Claude Desktop and Claude Code use to connect things like
Notion, GitHub, or a filesystem server. Unconfigured by default; nothing
about this changes how the backend behaves until you opt in.

### The security model, stated plainly

**Connecting a server does nothing by itself.** Ultron discovers every
tool a connected server offers, but none of them are *callable* — not by
the model, not at all — unless you name that exact tool in the server's
`auto_approve` list in the config file. An unapproved tool isn't "offered
and refused" — it's simply never included in what the model can see or
call. This is deliberate and worth understanding:

- **There is no in-conversation approval path.** The model can't ask "can
  I call this?" and get a "yes" from the user that unlocks it for that
  turn. The only way a tool becomes callable is the operator adding its
  name to the static config and restarting the backend.
- **Why not conversational approval, which would be more convenient?**
  Because a tool result — from any already-approved tool — is untrusted
  external data by definition, and it gets fed straight back into the
  model's context on the next turn. A conversational "yes, go ahead"
  mechanism is exactly the kind of thing a prompt injection can forge:
  hide an instruction in a tool result that makes the model believe the
  user consented to something they never said. Removing that path
  entirely removes that entire class of attack, not just makes it harder.
- **Every call is logged.** Success, failure, or a tool-level error — all
  three show up in the activity log (`event_type: mcp_tool_call`), so
  there's a real audit trail of what Ultron actually asked an external
  service to do.
- **Results are capped and treated as data, not instructions.** Response
  content is capped at 4,000 characters before it reaches the model. The
  system prompt explicitly instructs Ultron that tool results — especially
  from `mcp__`-prefixed tools — are data to report on, never commands to
  follow, regardless of what they claim.
- **What this can't protect you from:** the tools *you* approve. If you
  approve a tool that genuinely mutates something (sends an email, posts
  a message, deletes a file) on the *external* service, Ultron will call
  it the same way it calls a read-only one — there's no internal way to
  tell a "safe" MCP tool from a "risky" one by name or description alone.
  Only approve tools from servers you trust, and read what a tool
  actually does before adding it to `auto_approve`.

### Configuration

```powershell
$env:ULTRON_MCP_CONFIG = "C:\Users\you\mcp-config.json"
```

The file itself:

```json
{
  "servers": [
    {
      "name": "my-server",
      "url": "https://example.com/mcp",
      "auth_token": "optional-bearer-token",
      "auto_approve": ["search_docs", "get_weather"]
    }
  ]
}
```

- `name` must be alphanumeric/dash/underscore — it becomes part of every
  tool's qualified name (`mcp__my-server__search_docs`), which is how MCP
  tools are namespaced away from Ultron's own internal tools and from each
  other. There's no way for an external tool to collide with or shadow an
  internal one.
- `url` must be `http://` or `https://` — only the Streamable HTTP
  transport is supported. There's no stdio (local subprocess) transport
  here on purpose: spawning an arbitrary local process based on config is
  a meaningfully bigger risk than talking to a server over HTTP, and this
  project doesn't take that on.
- `auth_token`, if the server needs one, is sent as `Authorization: Bearer
  <token>` — the same convention most MCP servers expect.
- `auto_approve` is the list described above — an empty list (or omitting
  it) means the server's tools are discoverable but none are callable.

A malformed entry (bad name, bad URL, a duplicate server name) is skipped
with a warning printed to stderr at startup — one bad entry doesn't stop
the rest of the config from loading.

### How discovery works

The backend doesn't connect to any configured server at startup — it
connects lazily, the first time a chat request actually needs to know
what external tools are available, and caches the result for the rest of
that process's life. This is deliberate: MCP discovery is a real network
call with a real timeout (10s per server), and doing that at startup
would block the whole backend — health checks included — behind however
many servers are configured and however slow or unreachable they are. The
tradeoff is that the *first* chat request after a restart pays that cost
once; every request after is instant. If a server was unreachable at that
first attempt, restart the backend to retry — there's no automatic
background retry within a running process.

`GET /api/mcp/servers` shows every configured server, whether it's
currently reachable, and every tool it offers — approved and not — so you
can see what's available before deciding what to add to `auto_approve`.
Ultron can also answer questions about this directly via the
`get_mcp_servers` chat tool, which is the same read the endpoint uses.

## Scout — web search through your own engine (`web_search` chat tool)

The owner's web-research subagent, built to cost as close to nothing as
possible: `docker-compose.yml` runs a private **SearXNG** instance
(`ultron-searxng`, free, no account, no per-query fee) that is **not
published on any host port** — only `ultron-backend` can reach it, over
the compose network. The `web_search` chat tool queries it and returns up
to 5 titles, URLs and 300-character snippets, so a lookup costs a short
question plus a few hundred tokens of results, and zero when nobody asks.

Setup is two lines in `.env` (already added on this host):

```
SEARXNG_SECRET=<any long random string>
ULTRON_SEARXNG_URL=http://searxng:8080
```

Without `ULTRON_SEARXNG_URL` the tool is inert and says so. `searxng/
settings.yml` enables the JSON format the tool needs and turns SearXNG's
rate limiter off (one internal caller; the limiter would otherwise want a
Valkey container).

Safety, deliberately: results reach the model inside the same
`<untrusted_external_data>` wrapper MCP results get, so a web page can
never instruct Ultron; the tool is admin-only (not in the beta
allowlist) and not part of Economy mode's cheap set; and **nothing found
on the web is stored unless you explicitly ask Ultron to remember it**
(`remember_note`), never by automatic ingestion. `dev-tools/test_web_search.py`
covers the request shape, trimming, every failure mode, the wrapper, and
the scope.

## Cost controls — real safeguards, not just documentation

Every one of these is enforced in code, verified with tests that check the
actual mechanism (an API call not happening, a request getting refused,
real token counts landing in the database) — not just settings that exist
on paper.

**Prompt caching.** The system prompt and the tool schema list — over
1,000 tokens of static content that used to get sent fresh on *every*
single API call, including every intermediate step of a multi-tool turn —
now carry a `cache_control` breakpoint. After the first call in a session,
Anthropic serves that prefix from cache at a fraction of normal input-token
cost. A second breakpoint sits at the end of each conversation's history,
so an ongoing back-and-forth increasingly benefits from caching as it
grows, turn over turn. Nothing to configure — this is always on.

**Daily token budget, with an actual hard stop.**

```powershell
$env:ULTRON_LLM_DAILY_TOKEN_BUDGET = "100000"
```

Unset by default — no limit unless you opt in. Tracked against *real*
token counts from the API's own response, not an estimate. Once the day's
total (input + output tokens, summed across every call, resets at
midnight local time) reaches the budget, `/api/chat` returns a 429 with a
clear message — and, critically, **the Anthropic API is never called** for
that request. This isn't a warning after the fact; it's a wall.

**Beta-tester spend cap, in real dollars, with an actual hard stop.**

```powershell
$env:ULTRON_BETA_MAX_SPEND_USD = "1.00"    # this is the default — set only to change it
```

Every beta token is capped at **$1.00 of real spend for the whole beta,
not a daily allowance** — it never resets on its own. Each call's real
cost is computed from its actual token usage against `LLM_PRICING_PER_MTOK`
(the live per-model USD/MTok rates for the models this project uses) and
stored on that row in `llm_usage` at write time, so a later pricing edit
can't retroactively change what a past call actually cost. Once a
tester's lifetime total reaches the cap, `/api/chat` returns a 429 and —
same as the daily token budget above — **the Anthropic API is never
called** for that request. Admin chat (the real `ULTRON_API_TOKEN`) is
never subject to this; it's a beta-tester-only restriction, enforced
alongside the beta role's existing tool restrictions
(`BETA_ALLOWED_TOOLS`). A tester can see their own running total via
`/api/whoami` and the dashboard's beta-only "Your spend" card in
Settings; the admin sees every tester's spend via `/api/chat/usage`'s
`beta_testers` field and the dashboard's Settings → Usage & cost controls
card.

The cap covers more than `/api/chat` itself, closing three gaps a
2026-09-14 pre-launch review found (full detail in `CODE-AUDIT.md`):
`/api/tts` (voice replies) checks the same cap before calling Fish
Audio, since that's real cost too, not just chat tokens; each history
entry is capped at `MAX_HISTORY_MESSAGE_CHARS` (20,000 chars) on top of
the existing 40-entry count cap, so one oversized entry can't blow past
the whole budget in a single request; and `BETA_SPEND_LOCKS` (one lock
per beta tester) serializes that tester's own check-then-act sequence,
so two genuinely concurrent requests from the same identity can't both
read "under cap" before either logs its usage. Verified in
`dev-tools/test_beta_spend_cap.py` — drives real `/api/chat` and
`/api/tts` calls through a scripted fake Anthropic client until a
tester's computed spend crosses the cap, asserts the next call on either
endpoint is genuinely refused, fires two truly concurrent same-tester
requests to prove the lock serializes them (and confirms this by
temporarily removing the lock and watching the same test fail), and
confirms an admin token is unaffected throughout.

**Connection/device tracking.** `/api/connections` (admin-only) reports
every identity (admin, or a beta tester by name) that has made an
authenticated request since this backend process started, how many
distinct devices (IPs) each has connected from, and whether they're
active in the last 5 minutes. Read-only — this is visibility, not a
limit. ponytail-simple: in-memory and single-process, so it resets on
restart and wouldn't share state across `gunicorn -w N` workers; move it
into SQLite like `llm_usage` if this backend ever runs multi-process.
Surfaced on the dashboard (Settings → Connections) and via the Discord
bot's `/connections` command.

**Rate limiting.**

```powershell
$env:ULTRON_CHAT_RATE_LIMIT_PER_MINUTE = "20"
```

Defaults to 20 requests/minute. A backstop against a runaway or
misbehaving client hammering `/api/chat` — independent of the token
budget, since a burst of tiny requests could otherwise slip under a token
limit while still being clearly abnormal. In-memory sliding window,
resets naturally; a refused request doesn't itself count against the
window, so retrying after a 429 doesn't dig you in deeper.

**Response length cap.**

```powershell
$env:ULTRON_LLM_MAX_TOKENS = "1024"
```

Caps how long a single reply can be. Lower it for tighter cost control;
raise it if 1024 tokens is cutting off real answers.

**Usage visibility.** Every API call — including each intermediate step of
a multi-tool turn, not just the final one — logs its real input/output/
cache token counts to a `llm_usage` table.

- `GET /api/chat/usage` returns today's totals: request count, input/output
  tokens, cache read/write activity, and (if a budget is set) how much is
  left.
- Ultron can report on this itself via chat — ask something like "how much
  have you used today" and it calls `get_llm_usage`, the same function the
  endpoint uses, so the numbers always match.

**Already in place from earlier in this project, still relevant here:** a
tool-use loop capped at 5 calls per turn (`MAX_TOOL_ITERATIONS`) and
conversation history capped at 40 messages (`MAX_HISTORY_MESSAGES`) — both
bound the worst case for a single confused turn, independent of the
budget/rate-limit backstops above.

## Windows-specific behavior (read this)

- **CPU temperature** is read via WMI (`MSAcpi_ThermalZoneTemperature`).
  On a lot of consumer motherboards, Windows simply never gets this data
  from the firmware — if `/api/status` returns `"cpu_temp_c": null`, that's
  very likely your hardware, not a bug here. If you need reliable temps,
  a vendor tool (HWiNFO, etc.) is the more reliable source; this endpoint
  is a best-effort convenience, not a guarantee.
- **Pending updates** queries the real Windows Update Agent via COM
  (`Microsoft.Update.Session`), which requires `pywin32` (in
  `requirements.txt`) and can take several seconds per call since it's
  actually contacting Windows Update — expect `/api/systems` to be
  noticeably slower than the other endpoints.
- **Docker** here means Docker Desktop. Make sure it's running before
  hitting `/api/containers` — if it's not, you'll get a clean error in the
  response rather than a crash, but the panel will be empty.

## Running it permanently at startup

**With Docker Compose (how the owner's install runs):** `docker compose up -d`
from the repo root. In the container the backend is served by gunicorn
(`gunicorn.conf.py`: one worker with 16 threads, because lockouts, rate
limits and presence live in the process's memory), as the non-root user
`ultron`, with a `HEALTHCHECK` (`healthcheck.py`). The Discord bot and
SearXNG are health-checked too, and all three carry the `autoheal` label so
an autoheal container, if one is running on the host, restarts any that go
unhealthy. `docker compose ps` shows each one's health.

**Without Docker**, `python app.py` runs Flask's own development server --
fine for working on it, not for leaving it running. The simplest reliable
option on Windows is Task Scheduler:

1. Create `start-ultron.bat` in the `ultron-backend` folder:
   ```bat
   @echo off
   cd /d "%~dp0"
   call venv\Scripts\activate.bat
   set ULTRON_API_TOKEN=paste-your-generated-token-here
   python app.py
   ```
2. Open Task Scheduler → Create Task (not "Basic Task", so you get the
   "Run whether user is logged on or not" option).
3. Triggers → New → "At startup" (or "At log on" if you'd rather it only
   run when you're signed in).
4. Actions → New → Program/script: the full path to `start-ultron.bat`.
5. On the General tab, tick "Run with highest privileges" if Docker Desktop
   needs it.

For something closer to a real Windows service (auto-restart on crash,
proper service semantics), [NSSM](https://nssm.cc/) is the standard tool —
point it at `venv\Scripts\python.exe app.py` with the working directory set
to the project folder and `ULTRON_API_TOKEN` set as a service environment
variable.

## Installable app (PWA)

The dashboard can be added to a phone's home screen or a desktop and
opened full-screen. `app.py` serves `/manifest.webmanifest` and a
service worker at `/sw.js` (source: `sw.js` at the repo root) whose cache
name carries a version hashed from the dashboard's own content at
startup, so a redeploy invalidates old caches on the next visit. The
worker caches only the page shell, `/fonts/*` and `/pixel-assets/*`;
**it never intercepts `/api/*`** — live data and anything behind the
token always go to the network. Settings → "Install as an app" appears
only when the browser can offer the prompt; iOS users get the Share →
"Add to Home Screen" pointer. `dev-tools/test_pwa.py` covers all of it.

## Exposing it beyond your LAN

The backend serves the dashboard itself at `/` — open
`http://<backend-address>:5000/` on any device and you get the real
dashboard, not the static file. (`ultron-dashboard.html` still exists and
still works if you double-click it locally, but for any *other* device,
use the URL instead of copying the file around — see the note below on
why.) It has a **Settings → Connection** panel where you enter this
backend's URL and your `ULTRON_API_TOKEN` (or one of the
`ULTRON_BETA_TOKENS` entries, see the beta_tester section above) — once
connected it polls
`/api/status`, `/api/containers`, `/api/storage`, and `/api/systems`
every 15 seconds and replaces the mock numbers with real ones. On the
same Wi-Fi, use the LAN address (e.g. `http://192.168.1.50:5000`, found
via `ipconfig`); from a phone off that network, use a Tailscale address
instead.

**Why the URL, not the file:** mobile browsers (Chrome on Android,
confirmed) restrict `fetch()` calls made from a page opened via
`file://`, which silently breaks the Connect button with a generic
"could not reach backend" error even though the backend is reachable —
this cost real debugging time on 2026-09-13's beta test before the fix
above went in. Opening the dashboard from the backend's own `/` route
avoids it entirely, since the page and the API it calls share an origin.

This runs Flask's built-in dev server, which is fine on your own network but
isn't meant to be exposed to the internet directly. For remote access from
your phone or laptop, put it behind Tailscale rather than forwarding a port
on your router — see **[REMOTE-ACCESS.md](REMOTE-ACCESS.md)** for the full
setup walkthrough (install steps, the Windows Firewall interaction that
trips people up, and a helper script to print the address to paste into
the dashboard). Unlike the rest of this project, that's a setup guide
rather than tested code — Tailscale itself isn't something that can be
installed or verified from the environment this backend was built in.

## Running on Linux instead (Raspberry Pi 400, etc.)

The same `app.py` works there — it detects the OS and switches to
`/sys/class/thermal` / `vcgencmd` for temperature and `apt` for pending
updates, with `STORAGE_MOUNTS` defaulting to `{"ssd": "/mnt/ssd", "root": "/"}`.
Setup is the same, with the obvious substitutions (`export` instead of
`$env:`, `source venv/bin/activate`, a systemd unit instead of Task
Scheduler — ask if you want that written out again for this variant).

## Not included here

Read-only monitoring plus two deliberately narrow, confirmed actions
(backup, deploy-container) — that's the whole surface. Specifically still
not here: no update-installation action, no container stop/restart/remove,
no arbitrary command execution, and no ethical-hacking or exploit-scanning
functionality of any kind. If you want more actions later, give each one
the same treatment as the two here: real validation, a preview step, and a
token-based confirm — not a shortcut bolted onto the monitoring API.
