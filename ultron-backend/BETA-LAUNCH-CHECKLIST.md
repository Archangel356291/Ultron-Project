# Beta launch checklist

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

Double-click `ultron-dashboard.html` (or open it via `File → Open` in a
browser — no server needed for the file itself). Go to **Settings →
Connection**, enter:

- Backend URL: `http://127.0.0.1:5000` (same machine) or
  `http://<your-LAN-IP>:5000` (found via `ipconfig`, for another device
  on the same Wi-Fi)
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
