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

**Beta testers get a second, weaker token** — set `ULTRON_BETA_TOKEN` to a
*different* random value (same command as above, run again) and hand that
one out instead of your real `ULTRON_API_TOKEN`. It authenticates as the
`beta_tester` role: chat (full) plus view-only trading data
(`/api/trades`, `/api/trades/summary`, `/api/trades/tax-lots`) — everything
else 403s, including via chat's own tool use, not just the raw HTTP routes.
Leave `ULTRON_BETA_TOKEN` unset and the role doesn't exist at all. The
dashboard hides admin-only nav/controls automatically once it detects this
role via `/api/whoami`, but that's convenience — the 403s are what actually
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
| `GET /api/dev/repos`       | Git status (branch, dirty/clean, last commit) for configured repos |
| `GET /api/dev/repos/<repo>/diff` | Uncommitted diff for one configured repo             |
| `GET/POST /api/trades`     | Your manually-recorded trade ledger — list or add    |
| `DELETE /api/trades/<id>`   | Remove one trade record                            |
| `GET /api/trades/summary`    | Realized gain/loss per asset (FIFO) — see below     |
| `GET /api/trades/tax-lots`    | Per-disposal FIFO detail (acquisition date, holding period, term) |
| `GET /api/trades/export`       | CSV download — transactions or tax-lots format      |
| `GET /api/security/auth-log` | Recent login attempts (fast)                    |
| `GET /api/security/cve-scan` | CVE scan of running containers' images (slow — see below) |
| `POST /api/actions/backup` | **Mutates the host.** Two-step confirm — see below    |
| `POST /api/actions/deploy-container` | **Mutates the host.** Two-step confirm — see below |
| `POST /api/chat`          | Chat with Ultron — see below                       |
| `GET /api/chat/usage`      | Today's real token usage and budget status — see Cost controls |
| `GET /api/mcp/servers`      | Configured external tool servers and their tools — see External tools |

`STORAGE_MOUNTS` defaults to `{"c_drive": "C:\\"}` on Windows. Add other
drive letters at the top of `app.py`, e.g.:

```python
STORAGE_MOUNTS = {"c_drive": "C:\\", "d_drive": "D:\\"}
```

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
- Ultron can call thirteen built-in read-only tools — `get_system_status`,
  `list_containers`, `get_storage_usage`, `get_pending_updates`,
  `get_auth_log`, `get_recent_activity`, `get_repo_status`, `get_repo_diff`,
  `get_trades`, `get_trade_summary`, `get_trade_tax_lots`, `get_llm_usage`,
  and `get_mcp_servers` — which are the exact same functions the GET routes
  above use, so its answers reflect real numbers, not invented ones. CVE
  scanning is deliberately not one of these tools — see "Security
  monitoring" above for why. Adding a trade record is deliberately not one
  either — see "Trade records" above, and neither is the CSV export, since
  a file download doesn't map onto a chat reply. `get_repo_diff` is the
  first tool that takes a real parameter (`repo`) — the tool-calling loop
  passes whatever arguments the model supplies straight through as keyword
  arguments, so a handler function's own signature is what defines what it
  will accept. On top of these thirteen, any approved external tools from
  `ULTRON_MCP_CONFIG` are added dynamically, namespaced `mcp__<server>__
  <tool>` — see "External tools (MCP)" above for what "approved" means and
  why there's no way around it from inside a conversation.
- It has **no ability to take actions through chat**, even though the
  backup and deploy-container actions now exist on the dashboard. Ultron's
  own tools are all read-only; if asked to deploy something or run a
  backup via chat, it says so and points to the dashboard action instead of
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

The simplest reliable option on Windows is Task Scheduler:

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

## Exposing it beyond your LAN

The dashboard (`ultron-dashboard.html`) now has a **Settings → Connection**
panel where you enter this backend's URL and your `ULTRON_API_TOKEN` — once
connected it polls `/api/status`, `/api/containers`, `/api/storage`, and
`/api/systems` every 15 seconds and replaces the mock numbers with real
ones. On the same Wi-Fi, use the LAN address (e.g. `http://192.168.1.50:5000`,
found via `ipconfig`); from a phone off that network, use a Tailscale
address instead.

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
