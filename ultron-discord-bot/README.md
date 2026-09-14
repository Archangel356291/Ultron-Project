# Ultron Discord bot

A remote-control surface for the Ultron backend, from Discord. This bot has
no logic of its own beyond formatting — every command is an HTTP call to the
same backend (`app.py`) the dashboard uses, so there's exactly one
implementation of "what the system status is," not two that can drift apart.

## What it can do

| Command | What it does | Cost |
|---|---|---|
| `/status` | CPU, memory, temp, uptime, container count | free (direct API call) |
| `/containers` | List Docker containers and their state | free |
| `/storage` | Disk usage per configured drive | free |
| `/systems` | Pending updates, temp, uptime | free |
| `/repos` | Git status (branch, dirty/clean, last commit) for configured repos | free |
| `/diff <repo>` | Uncommitted diff for one repo | free |
| `/trades [asset]` | Your recorded trades — read-only, optionally filtered by asset | free |
| `/portfolio` | Realized gain/loss per asset (FIFO) — not tax advice | free |
| `/usage` | Today's real Claude API token usage, cache activity, and budget status | free |
| `/connections` | Who's connected right now — people, role, device count, last seen | free |
| `/mcp` | External tool servers, reachability, and which tools are approved | free |
| `/export` | Download trades as a CSV file — transactions or tax-lots | free |
| `/backup` | **Mutates the host.** Preview a backup, confirm with a button | free |
| `/deploy` | **Mutates the host.** Preview a container deploy, confirm with a button | free |
| `/ask <message>` | Ask Ultron anything — routes through the LLM, which can check real data via tools | costs Anthropic API tokens |
| `/forget` | Clear your conversation history with Ultron | free |

`/backup` and `/deploy` use the exact same preview-then-confirm flow as the
backend and dashboard — see "Action commands" below before using either.

`/trades` and `/portfolio` are read-only, same boundary as the backend's
own chat tools: there's no `/addtrade` command. Recording a financial
transaction happens on the dashboard, deliberately, not as a bot command —
`/portfolio`'s realized gain/loss is FIFO-simplified record-keeping, not
tax advice, and the disclaimer shows up in the embed's footer every time.
`/export` sends the same CSV the dashboard's export buttons download, as
a real file attachment in Discord — the disclaimer is written into the
file itself (as a header comment), the same way it is in the dashboard
download, so it travels with the file wherever it ends up.

`/usage` shows the same real numbers as the dashboard's Usage & Cost
Controls card and the backend's `GET /api/chat/usage` — same source, so
they never disagree. The embed turns red once you're at 90%+ of a
configured daily budget, same threshold the dashboard uses.

`/connections` reads the same `/api/connections` the dashboard's Settings →
Connections card does — it's presence visibility only, no way to disconnect
or block anyone from here. Beta testers each show up under their own name
(never a shared identity), which is also what makes the $1.00 lifetime
beta spend cap (see the backend README's Cost controls) attributable to a
real person rather than an anonymous token.

`/mcp` is read-only visibility, nothing more — it shows every configured
external tool server, whether it's reachable, and every tool it offers
with a clear ✓ approved / not approved marker. There is no command here
(and no way, from Discord or anywhere else in a conversation) to approve
a tool — that only happens in the backend's own config file. See the
backend README's "External tools (MCP)" section for why that's a hard
line, not a missing feature.

## Security — read this before inviting the bot anywhere

Every command checks the calling user's Discord ID against
`ULTRON_DISCORD_ALLOWED_USERS` before doing anything. **The bot refuses to
start without this set.** Without it, anyone who can see and message the bot
in a server — not just you — could query your home lab's status or spend
your Anthropic API budget via `/ask`. This is a remote-control surface for
personal infrastructure; keep the allowlist tight, and keep the bot out of
servers you don't fully control.

Unauthorized users get a plain "Not authorized" reply. Nothing about the
attempt is logged or reported back to you right now — if you want that,
it's a small addition to `require_auth` in `bot.py`.

## Setup

### 1. Create the Discord application and bot

1. Go to the [Discord Developer Portal](https://discord.com/developers/applications) → **New Application**.
2. Under **Bot**, click **Reset Token** to get your bot token (save it — you won't see it again without resetting).
3. Under **Bot**, you do *not* need to enable any Privileged Gateway Intents — this bot only uses slash commands, not message content.
4. Under **OAuth2 → URL Generator**, check scopes `bot` and `applications.commands`, and under Bot Permissions check `Send Messages` and `Embed Links`. Copy the generated URL and open it to invite the bot to your server.

### 2. Get your Discord user ID for the allowlist

In Discord, enable Developer Mode (User Settings → Advanced → Developer
Mode), then right-click your own name and **Copy User ID**. Repeat for
anyone else who should be allowed to use the bot.

### 3. Install and run (Windows 11, PowerShell)

```powershell
cd ultron-discord-bot
python -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt

$env:DISCORD_BOT_TOKEN = "paste your bot token here"
$env:ULTRON_BACKEND_URL = "http://127.0.0.1:5000"
$env:ULTRON_API_TOKEN = "the same token the backend was started with"
$env:ULTRON_DISCORD_ALLOWED_USERS = "your discord user id, and anyone else's, comma separated"

python bot.py
```

The bot needs the backend (`app.py`) already running and reachable at
`ULTRON_BACKEND_URL`. If the backend is on a different machine (e.g. the
Raspberry Pi, or the Cyberpower PC reachable over Tailscale), point this at
that address instead of `127.0.0.1`.

Global slash commands can take up to an hour to show up in Discord the
first time. For instant testing, set `ULTRON_DISCORD_DEV_GUILD_ID` to a
server ID (right-click a server icon with Developer Mode on → Copy Server
ID) and commands sync to that one server immediately.

## Running it permanently at startup

Same pattern as the backend — Task Scheduler:

1. Create `start-bot.bat` in the `ultron-discord-bot` folder:
   ```bat
   @echo off
   cd /d "%~dp0"
   call venv\Scripts\activate.bat
   set DISCORD_BOT_TOKEN=paste-your-token-here
   set ULTRON_BACKEND_URL=http://127.0.0.1:5000
   set ULTRON_API_TOKEN=paste-your-backend-token-here
   set ULTRON_DISCORD_ALLOWED_USERS=your-id,other-id
   python bot.py
   ```
2. Task Scheduler → Create Task → Triggers → "At startup" (or "At log on").
3. Actions → Program/script: the full path to `start-bot.bat`.

If both the backend and this bot run on the same machine, set the backend's
Task Scheduler entry to run first, or add a short `timeout /t 10` at the
top of `start-bot.bat` so the backend has time to come up first.

## Action commands (`/backup`, `/deploy`) — read this before using either

Both use the same preview-then-confirm flow as the backend and dashboard:
running the command doesn't do anything by itself. It shows you an embed —
what would be backed up, or what image/name/ports/env a container would run
with — plus **Confirm** and **Cancel** buttons. Nothing happens on the host
until you click Confirm.

A few things worth knowing:

- **Only you can click your own Confirm/Cancel.** If someone else on the
  allowlist (or anyone else, for that matter) clicks the buttons on your
  preview, they get told plainly that only the person who ran the command
  can confirm it — the click is rejected, not just visually ignored.
- **The buttons expire in about 4.5 minutes**, just under the backend's own
  5-minute confirmation-token lifetime, so a stale "Confirm" button can't
  linger and then fail confusingly later. After that, the message updates
  itself to say so and the buttons stop working — run the command again.
- **This bot doesn't grant itself anything the backend doesn't already
  gate.** The confirm token comes from the backend on preview and gets
  echoed straight back on confirm — same mechanism the dashboard uses. If
  you inspect the backend's own docs for `/api/actions/*`, you're reading
  the real security model, not something bot-specific.
- **`/deploy`'s `port` and `env` parameters take one mapping/variable each**
  (`port: 8080:80`, `env: FOO=bar`) — for anything more complex, use the
  dashboard, which supports multiple of each.

## How `/ask` conversation history works

Same design as the dashboard's chat: the backend is stateless, so this bot
keeps each Discord user's conversation history in its own memory, keyed by
their Discord user ID. Restarting the bot clears everyone's history — there's
no database here. Use `/forget` to clear your own history without waiting
for a restart.

## Not included here

- No voice support, no message-content-based commands (slash commands only
  — simpler, more secure, and doesn't need the privileged message content
  intent).
- No per-server configuration — the allowlist is global across every server
  the bot is in.
- No rate limiting beyond what Discord itself enforces. If you're worried
  about `/ask` costs, the backend's own `ULTRON_LLM_TIMEOUT_SECONDS` and
  tool-call cap still apply, but nothing here stops an allowlisted user
  from asking a lot of questions.
