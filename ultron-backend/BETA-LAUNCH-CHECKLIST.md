# Beta launch checklist

## Phase 1 status: complete (2026-09-13)

Core backend + dashboard + chat + voice, verified against a real running
instance (not just "should work"):

- Backend boots clean via `start-ultron.ps1`, secrets auto-loaded from
  `.env`, real `ULTRON_API_TOKEN` + `ANTHROPIC_API_KEY` in place
- Auth gating confirmed (401 with no/wrong token, 200 with the right one)
- Dashboard connects and shows real data, not mock — CPU/memory/status
- AI Assistant chat verified end-to-end: real tool calls
  (`get_system_status`), real answers, not guesses
- Usage/cost tracking confirmed accurate against actual API responses;
  daily token budget (50k) enforced by default
- Voice added and verified: `/api/tts` (Fish Audio) returns real,
  playable MP3 through the actual backend route; mic input wired to the
  browser's native speech recognition
- Security pass: gitignore hardened (a real gap — `*.db` had been
  dropped), a hardcoded bearer token found and scrubbed from git history
  before it was ever pushed, a SAST pass (bandit) came back clean, no
  secrets confirmed anywhere in git history or GitHub

**Not yet tested this phase** — still open for Phase 2: backup
preview/confirm flow, trade record entry + FIFO calc, Discord bot (never
started), MCP servers (none configured), CVE scanning, actual human
confirmation that TTS audio is audible (network-level success confirmed,
not ear-confirmed).

## Beta tester role — built, not yet deployed (2026-09-13)

Added a `beta_tester` role, separate from your admin login: chat (full
input) plus view-only trading data (`/api/trades`, `/api/trades/summary`,
`/api/trades/tax-lots` — no create/delete/export). Everything else 403s,
enforced at the Flask route level *and* inside chat's own tool-use loop
(the tool schemas offered to the model are filtered by role, so chat can't
be used to route around the same boundary). See `README.md`'s auth section
and `start-ultron.ps1`'s `ULTRON_BETA_TOKENS` block (originally a single
shared token; see `BETA-TESTERS.md` for the per-tester version this
became on 2026-09-13).

Not yet done / not tested against a real instance:
- No hard login screen before the dashboard loads — Settings → Connection
  is the only gate today. Fine for LAN/dev use; needed before anything is
  exposed publicly (see Funnel note below).
- Raspberry Pi deployment, Tailscale Funnel, and Pi resource monitoring —
  postponed (no Pi access yet as of this write-up). `REMOTE-ACCESS.md`
  covers personal Tailscale access only, not Funnel.

## Beta test #1: launched locally (2026-09-13)

First real beta_tester run, on this Windows machine (no Pi, no networking
— same device, `http://127.0.0.1:5000`), superseding the "not verified
end-to-end" gap above:

- Real `ULTRON_BETA_TOKEN` generated and added to `.env`.
- Backend launched via `start-ultron.ps1` with real secrets (not test
  tokens) — real `ANTHROPIC_API_KEY`, real `ultron.db`.
- Chat verified end-to-end with the beta token: real Claude reply, real
  `get_trades` tool call, and — asked directly for system/CPU info, which
  is out of beta scope — it correctly reported that tool isn't available
  to it rather than guessing or leaking data.
- Walked the actual dashboard UI (not just curl) connected as beta_tester:
  nav correctly shows only AI Assistant, Crypto & Markets, and Settings;
  Crypto & Markets shows prices/alerts/FIFO summary/trade history with no
  add-trade form and no export buttons; Settings shows Connection and
  Preferences only, Usage & Cost Controls and External Tools (MCP) both
  hidden.
- `run-beta.ps1` added alongside `start-ultron.ps1` — same startup, but
  activates the venv itself first, for launching from a non-interactive
  context.

Still open before this goes beyond "same device": the login-screen and
Pi/Funnel items above.

## Beta test #1 part 2: real remote device over Tailscale (2026-09-13)

Extended beta test #1 beyond one device, using Tailscale instead of
waiting on the Pi/Funnel:

- Tailscale switched to a fresh account with both devices on it: this
  PC (`pc-device-name`) and a phone (`phone-device-name`).
- Windows Firewall rule scoped to the Tailscale range only, not the LAN:
  `-RemoteAddress 100.64.0.0/10` (narrower than the plain port-5000 rule
  in step 4 of the deployment plan above).
- Tailnet grants locked to `autogroup:member` → `autogroup:self` (own
  devices only) — see `REMOTE-ACCESS.md` for the syntax fix this needed
  (`autogroup:self` isn't valid as a source, only a destination).
- Verified from the phone itself, cellular only (Wi-Fi off, genuinely
  off-LAN): `http://pc-device-name.tailXXXX.ts.net:5000/api/health`
  returned `{"ok":true}`. Confirmed from this machine that `/api/whoami`
  also resolves correctly over the same address with the beta token.

**Real limitation, not yet closed:** this only reaches devices on *this*
Tailscale account. A genuine third-party tester (different person,
different account) still isn't covered by `autogroup:self` — they'd need
an explicit invite/share, or the original public-URL-via-Funnel plan,
which is still waiting on the Pi.

Not yet done: actually opening `ultron-dashboard.html` on the phone
itself and connecting through the UI (only the raw API was hit from the
phone; the full dashboard-as-beta_tester walkthrough was verified locally
on this PC, not yet repeated on a second device).

## Beta test #1 closed out: full success (2026-09-13)

Finished what "not yet done" above left open — the dashboard itself,
through the UI, on the actual phone. Two real bugs surfaced doing this,
both fixed:

- **`file://` silently broke the Connect button.** The dashboard was
  Taildropped to the phone and opened as a local file; mobile Chrome
  restricts `fetch()` from `file://` origins, so the health check failed
  with no useful error beyond "could not reach backend" even though the
  backend was reachable (confirmed by navigating the same URL directly).
  Fixed by adding an unauthenticated `GET /` route to `app.py` that
  serves `ultron-dashboard.html` from the backend itself — same origin as
  the API, no CORS/file-origin issues, and no more transferring the file
  to every device that wants to use it. Safe to serve unauthenticated:
  the file has no secrets baked in, same as handing someone the file
  directly.
- **Both tokens rotated** (`ULTRON_API_TOKEN` and `ULTRON_BETA_TOKEN`)
  after having been typed into chat multiple times during setup —
  current values live only in `.env`, never in this file or git history.

**Verified on the phone itself, through the actual dashboard UI, over
Tailscale (cellular, Wi-Fi off):**
- Beta token: nav restricted to AI Assistant + Crypto & Markets +
  Settings, chat working end-to-end.
- Admin token: full nav (all 9 sections + Settings), confirming the same
  URL correctly serves either role depending only on which token is used.
- Voice: `/api/tts` fires and returns real audio once "Speak replies
  aloud" is toggled on in Settings (off by default, doesn't persist
  between sessions — expected, not a bug).

Backend stopped after this test (not left running). To relaunch:
`run-beta.ps1` from `ultron-backend/`, same as documented above.

## Discord bot: set up, invited, and verified live (2026-09-13)

Closes the "Discord bot (never started)" gap from Phase 1. Real bug found
and fixed along the way — see `CODE-AUDIT.md`'s later 2026-09-13 entry
for the full detail: `start-bot.ps1` never loaded `.env`, and the real
bot token that had been sitting in `.env` was under the wrong key name.

- Fixed both, confirmed the existing bot token is real and valid
  (successfully authenticated with Discord's gateway).
- Invited the bot to a real Discord server via an OAuth link built from
  its own application ID (fetched live via the Discord API, not typed by
  hand) with the permissions it actually needs: view channels, send
  messages, embed links, attach files (for `/export`), read history.
- Set `ULTRON_DISCORD_DEV_GUILD_ID` to that server so all 15 slash
  commands sync instantly instead of waiting up to an hour for global
  sync — confirmed synced via the Discord API.
- A human ran `/status` and `/ask` for real in Discord; cross-checked
  against the backend's own request log to confirm the full round trip
  (Discord → bot → backend → Claude → back), not just "Discord showed a
  reply."

Not yet tested live: `/backup` and `/deploy`'s preview-confirm flow (the
per-user Confirm/Cancel buttons), `/export`'s file attachment, and the
rest of the read-only commands (`/containers`, `/storage`, `/systems`,
`/repos`, `/diff`, `/trades`, `/portfolio`, `/usage`, `/mcp`, `/forget`).
Their code paths are the same ones already exercised via the dashboard
and curl, so low risk, but "the same code, called from Discord" hasn't
been clicked through end to end for those specific commands yet.

## Multi-device concurrency: tested for real (2026-09-13)

Every prior test was one device at a time. Before running a live beta
with several testers connected simultaneously, actually verified the
backend handles real concurrent load rather than assuming `threaded=True`
in `app.run()` was enough on its own:

- **8 truly concurrent requests** (`curl ... &` fired together, not
  sequentially) to `/api/status` — all returned `200` in ~0.4s total for
  all 8, not ~0.4s × 8, confirming they actually ran in parallel rather
  than queueing.
- **2 concurrent `/api/chat` calls** with different prompts — each got
  its own correct, non-cross-contaminated reply, and both usage-log
  writes landed in the SQLite database with no lock errors
  (`sqlite3.connect(..., timeout=10)` gives real headroom here).
- **12 interleaved concurrent requests from two different beta
  testers** (`alice` and `bob`, real distinct tokens, fired in rapid
  alternating pairs) — `/api/whoami` correctly identified the right
  tester on every single request. Zero identity bleed under real
  concurrent load, not just "looks thread-safe by reading the code."

**Two real constraints to know about before a multi-tester day** — both
deliberate, documented, cost-control features, not bugs, but they're
*shared across everyone*, not per-tester:

- **Chat rate limit**: `ULTRON_CHAT_RATE_LIMIT_PER_MINUTE`, defaults to
  20/minute *total*, across admin and every beta tester combined. A
  handful of people chatting actively at once can trip this faster than
  one person testing alone would expect.
- **Daily token budget**: `ULTRON_LLM_DAILY_TOKEN_BUDGET`, set to 50,000
  in `start-ultron.ps1` (active by default), also a *combined* ceiling
  for the whole day, not per-tester.

Neither was changed — the right value depends on how many testers you
actually end up with, which isn't known yet. Rough starting point once
it is: budget roughly a few thousand tokens per tester per short
conversation, so for N simultaneous testers doing real testing, a daily
budget in the tens-of-thousands-times-N range is more realistic than the
single-user 50k default. Both are one-line edits in
`ultron-backend/start-ultron.ps1`.

**A third cost control, added since — but per-tester, not shared:**
`ULTRON_BETA_MAX_SPEND_USD` caps each beta tester at $1.00 of real spend
for their whole time testing (default, one-line override in `.env`).
Unlike the two above, this doesn't get tighter as tester count grows —
each person gets their own $1.00, independent of everyone else's. See
`ultron-backend/BETA-TESTERS.md`'s "Spend cap" section and the backend
README's Cost controls for the enforcement details.

## Final pre-launch check (2026-09-13)

Re-verified everything live, from a cold state, after the git history
rewrite and several rounds of token rotation — not assumed still-good
from earlier passes:

- Git: `main` fully synced with `origin/main`, clean working tree.
- Backend: started fresh from `.env`, `/api/health` and `/` (dashboard
  route) both 200, admin token resolves correctly, no-token request
  correctly 401s.
- Concurrency: re-ran the 8-parallel-request test — still ~0.4s total,
  genuinely parallel, not queued.
- Discord bot: token still valid (Discord API confirms the app), still
  a member of the test server, all 15 commands still synced.
- Secrets: swept git-tracked files for every real token/key value
  currently in use — none found. `.env` remains correctly gitignored.

**The one real gap before a live multi-tester beta:** `ULTRON_BETA_TOKENS`
is currently unset in `.env` — the `beta_tester` role doesn't exist yet.
This is expected, not a bug (the roster in `BETA-TESTERS.md` is still
empty), but it's the one concrete step left: once you have a real
tester, follow `BETA-TESTERS.md`'s add process (generate their token,
add it to `.env`, restart the backend) before sending them anything.

Everything else — RBAC, concurrency, the bot, the dashboard's mobile
fix, the guide/invite docs — is verified and ready.

---

Everything below is pulled fresh from the actual code as of this write-up
(env var names, defaults, and what's required vs. optional were all
re-verified against `app.py` and `bot.py` directly, not recalled from
memory). This is the single consolidated path from "I have these files"
to "it's running and I can start testing" — the individual READMEs go
deeper on any one piece, but this is the order to actually do things in.

## 0. Prerequisites

- **Python 3.10+** — [python.org](https://www.python.org/downloads/), check
  "Add python.exe to PATH" during install. Required; the Anthropic SDK
  won't install on anything older.
- **Docker Desktop** — only if you want the Home Lab panel (container
  list, CVE scanning) to show real data. Everything else works without it.
- **Git** — only if you want the Development tab (repo status/diffs) to
  show real data. Usually already present on a dev machine.
- **A Discord bot token** — only if you want remote control via Discord.
  Entirely optional; skip this section if you just want the dashboard.

You do **not** need Tailscale, an MCP server, or anything else to get a
working beta running today — those are all later, optional steps.

## 1. Get the files onto your PC

Two folders and one standalone file:

```
C:\Ultron\
  ultron-backend\          <- app.py, README.md, REMOTE-ACCESS.md, requirements.txt, get-tailscale-address.ps1
  ultron-discord-bot\      <- bot.py, README.md, requirements.txt (skip if not using Discord)
  ultron-dashboard.html    <- open this directly in a browser, no server needed for the file itself
```

## 2. Backend — minimum to get running

```powershell
cd C:\Ultron\ultron-backend
python -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

If `Activate.ps1` is blocked, run once as admin:
`Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`

Two environment variables matter for a first run — one is **required**,
one you'll almost certainly want:

```powershell
$env:ULTRON_API_TOKEN = -join ((48..57)+(97..102)|Get-Random -Count 32|%{[char]$_})
$env:ANTHROPIC_API_KEY = "sk-ant-..."
```

- `ULTRON_API_TOKEN` — **required**. The app refuses to start without it.
  This is the bearer token every client (dashboard, bot) needs to talk to
  the backend. Save it in a password manager — you'll need it again in
  step 5, and every time you restart the backend in a new PowerShell
  session unless you use the startup script in step 3.
- `ANTHROPIC_API_KEY` — this is the real beta key. Without it, every panel
  except AI Assistant chat still works; chat itself returns a clear 503
  until this is set. This is the one env var this whole project has been
  waiting on — plugging in a real key here is what actually turns the
  beta on for chat.

## 3. Use the startup script instead of retyping env vars every time

Retyping a dozen `$env:X = "..."` lines every session is exactly the kind
of thing that gets skipped or fat-fingered. `start-ultron.ps1` (in this
same folder) has every environment variable this backend reads, commented
with what it does, required ones un-commented with a placeholder, optional
ones commented out. Open it once, fill in what you want, save it, and
from then on:

```powershell
.\start-ultron.ps1
```

is the entire startup process. Section 8 below is the guide to which
optional lines in that script are worth turning on for your beta.

## 4. Windows Firewall — so the dashboard and phone can actually reach it

```powershell
New-NetFirewallRule -DisplayName "Ultron Backend" -Direction Inbound -Protocol TCP -LocalPort 5000 -Action Allow
```

One rule, run once. Needed even for same-machine dashboard access if
Windows Firewall's default inbound policy is blocking it — cheap to run
now rather than debug a "why won't it connect" later.

## 5. Start it and verify it's actually alive

```powershell
.\start-ultron.ps1
```

(or `python app.py` if you skipped step 3). You should see it print that
it's listening. In a browser, or a second PowerShell window:

```powershell
curl http://127.0.0.1:5000/api/health
```

Expect `{"ok":true}`. If you get a connection error, the backend isn't
running or the firewall rule didn't take — check the PowerShell window
running it for a Python traceback before anything else.

## 6. Open the dashboard and connect it

The backend serves the dashboard itself now — for any device other than
the one running the backend, just visit its URL in a browser rather than
copying `ultron-dashboard.html` around: opening it as a local file breaks
the Connect button on mobile browsers (confirmed on Android Chrome), so
the URL is the reliable path for anything but quick local testing on the
host machine itself, where double-clicking the file still works fine.

- Same machine: `http://127.0.0.1:5000/` (or double-click
  `ultron-dashboard.html` directly, either works here)
- Another device on the same Wi-Fi: `http://<your-LAN-IP>:5000/` (found
  via `ipconfig`)

Go to **Settings → Connection**, enter:

- Backend URL: the same address you just opened (drop the trailing
  `/api/...` if your browser added one)
- API token: the `ULTRON_API_TOKEN` value from step 2

Click Connect. The mock numbers across every panel should start being
replaced by real ones within about 15 seconds.

## 7. Smoke test — confirm the beta actually works before calling it done

Work through these in order; each one exercises a genuinely different
part of the system, not just "does the page load":

1. **Home page** shows real CPU/memory/uptime numbers, not the static mock
   values from before you connected.
2. **AI Assistant → ask it something** like "what's my CPU usage right
   now?" — it should call a real tool and answer with the actual number,
   not a guess. This is the one that needs `ANTHROPIC_API_KEY` set.
3. **Home Lab tab** shows your actual running Docker containers (skip if
   you don't have Docker Desktop running).
4. **Settings → Usage & cost controls** shows the request you just made in
   step 2 — confirms real token tracking is working.
5. **Try a backup preview** (Home Lab → Backup, if you've set
   `ULTRON_BACKUP_SOURCES`/`DEST`) — click "Preview backup" and confirm it
   shows real source/destination info. **Don't click Confirm** unless you
   actually want a real backup to run — this is exactly the two-step
   design working as intended.
6. **Record a test trade** (Crypto tab → My trades) — a small buy, then a
   matching sell, and confirm the FIFO gain/loss calculation in the
   summary looks right. Delete it afterward if it was just a test.
7. **If you're using the Discord bot**, run `/status` from Discord and
   confirm it shows the same numbers the dashboard does.

If all seven work, the beta is genuinely functional, not just "the page
loaded."

## 8. Optional features — what's worth turning on now vs. later

Everything here is a line in `start-ultron.ps1` you can uncomment. None of
it is required to start testing.

| Feature | Env var(s) | Worth it now? |
|---|---|---|
| Backups (dashboard/chat can preview+run) | `ULTRON_BACKUP_SOURCES`, `ULTRON_BACKUP_DEST` | Yes, if you have something worth backing up — low risk, two-step confirm |
| Development tab (real git status) | `ULTRON_CODE_REPOS` | Yes, if you have local repos — quick to set up, no downside |
| Daily token budget (hard spend cap) | `ULTRON_LLM_DAILY_TOKEN_BUDGET` | Worth setting during beta specifically — a real ceiling while you're finding out how much you actually use |
| Chat rate limit | `ULTRON_CHAT_RATE_LIMIT_PER_MINUTE` | Already on by default (20/min) — only touch this if you hit it |
| External tools (MCP) | `ULTRON_MCP_CONFIG` | Later — only if you have a specific MCP server in mind; read the backend README's "External tools (MCP)" section first, this is the one with real security implications |
| Discord bot | separate folder, see below | Whenever you want remote control — not required for the dashboard beta |

## 9. Optional: the Discord bot

Separate process, separate folder:

```powershell
cd C:\Ultron\ultron-discord-bot
python -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Fill in `start-bot.ps1` the same way as the backend's script — it needs
the **same** `ULTRON_API_TOKEN` from step 2, plus a Discord bot token and
your Discord user ID (comma-separated if more than one person should have
access). All three are required; the bot refuses to start without them.
Full setup (creating the Discord application, inviting the bot to a
server) is in `ultron-discord-bot/README.md`.

## 10. Optional: remote access and always-on

Neither is needed to start beta testing today — both are here for when
you want this running continuously rather than only while you're at the
PC with a PowerShell window open:

- **Remote access from your phone**: `REMOTE-ACCESS.md` — Tailscale setup,
  fully walked through.
- **Run automatically at boot / stay running when you're not watching a
  terminal**: the backend README's "Running it permanently at startup"
  section covers Task Scheduler.

## What to expect during beta — known, by-design behavior, not bugs

- **The first chat message after starting the backend is slower** than
  the rest — that's real tool/MCP discovery happening once, not a hang.
  Every message after is fast.
- **CVE scanning is genuinely slow** (real per-image scans) and is a
  manual "Scan now" button, never automatic — that's deliberate, not
  something that got missed.
- **Backup and deploy-container never run without you clicking Confirm**
  on the actual preview — if you ask Ultron via chat to do either, it will
  tell you to use the dashboard instead. That's the security boundary
  working, not a missing feature.
- **A closed PowerShell window stops the backend** unless you've set up
  Task Scheduler (step 10) — expected for a manual beta run, not a crash.
