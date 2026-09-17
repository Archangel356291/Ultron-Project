# Roadmap findings — 2026-09-16

The investigation items from `FUTURE-TASKS-2026-09-19.md` (2, 3, 4, 5),
pulled forward per the owner's 2026-09-16 brief. Each one says what was
found, what was built because it was clearly worth it, and what is
proposed but deliberately not built without a go-ahead.

## 2. Offline mode

**Finding: Ultron is already offline-capable by architecture.** The backend
is local (Flask on this PC, SQLite, psutil, the Docker socket, local git).
With no internet at all, every one of these keeps working over the LAN or
an already-established Tailscale link: status, containers, storage,
systems, activity log, memory notes, knowledge graph, git status/diff,
trades and tax lots, metrics history, evolution ideas, login, the
dashboard itself.

What genuinely needs the internet, and already fails with a clear message
rather than pretending:

| Feature | Dependency | Behaviour offline |
|---|---|---|
| Chat | Anthropic API | 502 "could not reach the Anthropic API — check network connectivity" |
| Voice replies | Fish Audio TTS | silent (best-effort by design, chat itself unaffected) |
| CVE scan | `docker scout` → registry | scan returns an error result |
| MCP tools | whatever servers are configured | discovery/call errors |
| Dashboard fonts | Google Fonts CDN | **was** a system-font fallback; **now self-hosted** (below) |

Two real defects were found and fixed, and one improvement built:

- **Fixed — the dashboard never recovered from an outage.** After any lost
  connection the poll timer was cleared and `refreshAll()` was gated on
  `state.connected`, so it could never run again: "offline · showing last
  known data" until a manual reload. Now a single explicit heartbeat
  (`GET /api/whoami`) decides connected, polling continues while
  disconnected (each tick is the reconnect), the topbar reads
  "reconnecting · showing data from 26s ago" with the age ticking, and a
  401 stops retrying and says to sign in again. Verified by killing and
  restarting the backend under a live dashboard.
- **Fixed — one flaky feed read as "connection lost".** `Promise.all` over
  twelve feeds meant one 502 flipped the core to alert. Partial failures
  are now reported as "N of 12 feeds failed" while staying connected.
- **Built — self-hosted fonts.** The dashboard's only third-party request
  was four typefaces from Google. They are now served from `fonts/` by
  this backend (OFL-licensed, see `fonts/README.md`), and the CSP no
  longer allows any Google origin. The page renders identically with no
  internet, and no third party sees a page view.

**Not built, on purpose:** a "local chat" that answers without Claude. It
would either be canned responses dressed up as Ultron (the fake offline
mode the task warned against) or a second, weaker brain to maintain. The
honest offline story is: everything works except talking to him, and he
says so.

**Two things worth knowing about Tailscale offline:** an existing LAN
peer keeps working without the coordination server, and MagicDNS names
resolve from the local netmap — but the `*.ts.net` TLS certificate only
matches that name, so reaching the backend by raw LAN IP means a
certificate warning. Also, the whole tailnet's DNS routes through the
Pi-hole container; when that container lost its network namespace on
2026-09-16, DNS broke on every device (fixed the same day with a
healthcheck + autoheal in the Pi-hole compose stack, outside this repo).

## 3. API-lite mode

**Finding: most of the levers already exist as environment variables;
what is missing is a way to flip them per conversation.**

Already there: `ULTRON_LLM_MODEL` (with a pricing row for
`claude-haiku-4-5` already in `LLM_PRICING_PER_MTOK`), `ULTRON_LLM_MAX_TOKENS`
(default 1024), `ULTRON_LLM_DAILY_TOKEN_BUDGET`, `ULTRON_CHAT_RATE_LIMIT_PER_MINUTE`,
`MAX_TOOL_ITERATIONS` (5), prompt caching on the system prompt, tool
schemas and history, and the beta role's tool allowlist (3 of 21 tools).

What "lite" would actually cut, in order of dollar impact:

1. **Model:** Sonnet 5 ($2 / $10 per MTok in/out) → Haiku 4.5 ($1 / $5).
   Roughly halves every call.
2. **Tool rounds:** cap at 2 instead of 5. Each round re-sends the
   (cached) context plus the tool result; the cap bounds the worst case.
3. **Tool list:** 21 schemas ≈ 3–4k input tokens, cached at 0.1×. Trimming
   to the six cheap reads (status, containers, storage, updates, recall
   notes, recent activity) saves a little per call and, more usefully,
   keeps Haiku from wandering into trades/git/MCP.
4. **Reply length:** `max_tokens` 1024 → ~400.

What it would NOT change: any safety boundary. Same read-only tools,
same preview-then-confirm actions, same MCP opt-in, same spend caps.

**Proposed build (~40 backend lines + a Settings switch + one test):**
`ULTRON_LITE_MODEL` (default `claude-haiku-4-5`) and a per-request
`"lite": true` flag from the dashboard (an "Economy mode" switch in
Settings → AI, persisted like Reduced Visual Mode). Server-side enforced:
lite swaps the model, caps tool rounds at 2, trims the tool list, and
caps `max_tokens`. Usage logging already records real dollars per call,
so the saving would be visible on the Data & analytics tab, not asserted.

**Not built yet** — the task said to scope before building. It is a
yes/no.

## 4. Installable app for phones

**Finding: a PWA is realistic and small; a native app is not worth it.**

The stack (one HTML file served by Flask, no build step) is close to
PWA-ready already: HTTPS via the Tailscale-issued certificate (a hard
requirement, satisfied), `theme-color` and the `apple-mobile-web-app-*`
metas are in the `<head>`, and the CSP's `script-src 'self'` permits a
same-origin service worker.

What is missing, and the honest effort:

| Piece | Effort | Notes |
|---|---|---|
| `manifest.webmanifest` route | small | name, `start_url: /`, `display: standalone`, `theme_color`, icons |
| Icons (192, 512, maskable, apple-touch) | small | original art generated from the existing hex logo mark with Pillow, same pipeline as `gen_pixel_assets.py` |
| `/sw.js` service worker | medium | cache-first for the shell (`/`, `/fonts/*`, `/pixel-assets/*`), **network-only for `/api/*`** (never cache live data or anything behind the token), versioned cache name + `skipWaiting` so a redeploy is picked up |
| Install hint | small | a one-line "Add to home screen" prompt in Settings, shown only when `beforeinstallprompt` fires |

Total: about a day, no new dependencies. Result: a home-screen icon,
full-screen standalone window, instant shell load, and the dashboard
opening even with the backend unreachable (it then shows the reconnect
state from item 2 rather than a browser error page).

Caveats to state up front: iOS Safari supports installed PWAs but with
its own quirks (no `beforeinstallprompt`, the user adds via Share →
"Add to Home Screen"; the metas already present handle the standalone
chrome). Service-worker caching of the HTML means a stale shell can
persist for one load after a redeploy unless `skipWaiting` + a reload
prompt is wired — worth doing in the same pass. The sign-in token is
kept in memory/localStorage exactly as today; the worker never touches it.

Native (Capacitor / Trusted Web Activity / Electron): rejected. It adds
a build toolchain and app-store or sideload distribution for no
capability this dashboard needs.

**Built (owner approved 2026-09-16):** `/manifest.webmanifest` and a
versioned `/sw.js` served by `app.py`, three original icons generated
from the header's hex mark (`gen_pixel_assets.py`, incl. a maskable
one), the manifest/icon links and worker registration in the dashboard,
and a Settings row that offers "Install" only when the browser fires
`beforeinstallprompt` (iOS gets the Share → Add to Home Screen pointer
instead). The worker is network-first for the page, stale-while-
revalidate for fonts and sprites, and **never intercepts `/api/*`** —
`dev-tools/test_pwa.py` asserts that bypass is present in the served
source, that the cache version tracks the dashboard's content, and that
every manifest icon serves as a real PNG. Also in the findings for item
3: Economy mode was built and verified the same day.

## 8. Intelligence — "real knowledge, smarter than anyone in the room"

Owner's ask (2026-09-16, after the roadmap items). The honest reading:
Ultron's raw reasoning is Claude's; what this project can add is that
he *already knows the room and already remembers you* when a
conversation starts, learns on request with provenance, and carries
himself like someone who has already looked. Built, all at zero
recurring token cost:

- **Situational context** — before every admin turn `run_ultron_chat`
  appends a second, uncached system block assembled locally: the live
  briefing (below) plus the memory notes related to what was just said
  (`recall_related_notes`, graph retrieval, no LLM). Marked as
  information, never instruction. Beta testers never receive it. Effect
  measured live: "anything I should know?" answered with CPU, memory,
  containers, free disk and Sentinel's state in one reply and **no tool
  round at all** (previously two or three).
- **`get_briefing()`** — a deterministic read of the host: status,
  storage headroom with a plain verdict, anything ≥15 points above its
  24-hour baseline, Sentinel findings, warning/error events in the last
  day, memory size and pace, ideas awaiting review. Home tab card
  "Ultron's read", admin-only `GET /api/briefing`, chat tool (also in
  Economy mode). `dev-tools/test_situational_context.py`.
- **Bearing** (system prompt): lead with the answer, then the fact it
  rests on, then the next thing you'll ask; say what was checked; keep
  verified / inferred / unknown distinct; use memory naturally and with
  dates; never hedge vaguely.
- **Learning with provenance** (system prompt): research via Scout,
  answer in his own words with the source URL, *offer* to keep it, save
  one distilled fact with its URL only when you say yes.

**Both approved and built the same day, plus the Brain & Knowledge
folder the owner asked for:**

1. **Deep thought mode** — `"deep": true` (Settings switch) answers with
   `ULTRON_DEEP_MODEL` (default `claude-opus-5`), `max_tokens` ≥ 2048,
   up to 8 tool rounds; admin-only, wins over Economy, replies tagged
   `deep`. Writing the test caught a real ordering bug (with both flags
   sent, the Economy tool-trim ran before Deep took over).
2. **Learn from our conversations** — opt-in `"learn": true`: after an
   admin reply, one lite-model call asks whether the exchange held one
   fact or preference worth remembering next month; if new, it is saved
   through `remember_note` and logged as a "learned" activity event.
   Background thread, never for beta, skipped when Ultron already used
   `remember_note` that turn (the first live run showed the learner
   paraphrasing what he had just saved himself — fixed before commit).
3. **`D:\ultron's Brain&Knowledge`** — already the data dir; it now holds
   `chat logs\dashboard\YYYY-MM-DD.txt` and `chat logs\discord\…` (web
   and Discord kept apart, decided by the `speaker` label in one place)
   and `knowledge\memory-notes.md`, the notebook rewritten on every save
   for reading without a SQLite client. `dev-tools/test_deep_learn_brain.py`.

## Also fixed on the way

- **Crypto & Markets no longer shows fake data.** The hardcoded
  BTC/ETH/SOL/SPY ticker and the three "armed" alerts (flagged in both
  `HOME-DASHBOARD-REDESIGN.md` and `ULTRON-COLOR-SYSTEM.md`, never
  removed) are gone; the page now says plainly that this backend has no
  market-data connection and shows only the real ledger and FIFO figures.
- **`/threats` in the Discord bot** — Sentinel parity, per the project's
  every-feature-gets-a-command rule; `dev-tools/test_bot_threats.py`.
  Writing it exposed that `bot.py` could not even be imported under the
  fake `discord` package (`commands.when_mentioned` was missing), which
  is why no bot test had existed — the fake was extended, per
  `dev-tools/README.md`'s own rule.
- **Local time in every container** (`TZ` on backend, bot and SearXNG);
  activity, chat-log and Sentinel timestamps were UTC.

## 5. Tools, plugins and skills survey

Checked with `claude plugin list` / `claude plugin marketplace list` on
2026-09-16 in the Claude Code environment used for this work.

**Installed and used this session**

- `frontend-design` — loaded before the presence-layer design pass;
  its "spend boldness in one place" and copy guidance shaped the reply
  reveal and the presence vocabulary.
- `claude-in-chrome` (built-in) — every visual and behavioural check was
  done live over HTTPS in Chrome: chat round-trip, presence states,
  Esc/Stop, the kill-and-restart outage test, font loading, CSP.
- `graphify` — `graphify update .` after each code change, per
  `CLAUDE.md`.
- `ponytail` (v4.9.0, user scope) — minimalism guard; the deliberate
  shortcuts it left are marked `ponytail:` in code (currently one: the
  fixed 15s reconnect interval, no backoff).

**Installed, not usable this session**

- `playwright` (official plugin) — its MCP server failed to connect and
  was skipped. This is the single most useful missing capability: it
  gives a real, resizable viewport, which would close the "phone-width
  layout never live-verified" gap that every pass since Module 13 has
  had to report. Recommendation: fix the connection (restart Claude
  Code / the plugin) and make a 400px check part of every dashboard
  pass.

**Available, deliberately not used**

- `figma` — the design source of truth here is the reference imagery
  and the shipped dashboard itself, not a Figma file. Would add a
  parallel artifact to keep in sync for no gain.
- `design` (Claude Design canvas) — the owner asked for the real
  interface to improve, not mockups of it.
- `dataviz` — worth loading for the next pass that touches the Systems
  tab history charts or Vitals sparklines; not touched this session.

**Recommended before each backend-touching commit going forward:**
`/security-review` (available as a skill) on the diff, and
`/code-review` at medium effort. Both were available and neither had
been part of the routine.

Marketplaces configured: `claude-plugins-official`, `ponytail`. No new
plugin was installed: nothing in reach materially improved on what was
already present, and the one gap (viewport control) is an installed
plugin that needs reconnecting, not a missing one.

## 6. Two of four subagents missing from the pixel room — done

The owner named them on 2026-09-16: a **security watchdog** ("any and
all security threats") and a **web-research agent** that should cost
next to nothing in tokens. In the room they are **Sentinel** (amber,
the dashboard's `--amber`) and **Scout** (violet, the purple the
activity feed already uses). All four agents now share one sprite/desk/
tube set generated from the same code in four colours; the desks sit at
x = 696/786/876/966 with the conveyor starting at the first desk and
Ultron's walk range shortened so he never overlaps them.

Sentinel is the room's first non-scenery element: its screen stays lit
and its plate reads `SENTINEL · ALERT` in red while the activity log
holds a warning or error from the last hour (fed by the existing
`fetchActivity` poll, no new request). The cyan and green agents still
have no recorded role, so no name plate yet.

## 7. Making Sentinel and Scout real — proposals

The owner's phrasing reads as feature asks, not just sprites. Both can
be built inside this project's rules; one needs a decision first.

**Sentinel — a zero-token security watchdog.** A backend scheduler
thread (same shape as `_start_metrics_history_scheduler`, every 5 min)
that checks what the backend can already see: failed logins and
lockouts (`get_auth_log`, `_login_lockouts`), containers that exited or
restarted since the last check (`docker_ps`), the cached CVE scan's
critical count (`scan_container_cves`), and expired/rotated tokens. It
writes to the activity log only on a *change* (a new threat, or a
threat clearing) with `status: warning|error`, which is exactly what
already lights Sentinel's desk and lands in the Home feed and the
Security tab — and it uses no LLM call at all. Read-only, host-safe,
inert until `ULTRON_SENTINEL_INTERVAL_SECONDS` is set. Ultron himself
can be asked about it through a new read tool (`get_threat_summary`).
**No decision needed; about 120 lines plus a test.**

**Scout — web research at minimal token cost.** "Minimal to no tokens"
rules out the obvious route (Anthropic's `web_search` server tool
inside chat: every result page becomes input tokens, plus a per-search
fee). The honest low-cost shape is:

1. A search backend that costs nothing per query and stays private —
   **SearXNG self-hosted in a container on this PC** (free, no account,
   aggregates other engines, one more `docker compose` service beside
   Pi-hole and Jellyfin). Inert until `ULTRON_SEARXNG_URL` is set.
2. A read-only `web_search` chat tool returning titles + snippets only
   (a few hundred tokens), wrapped in the same
   `<untrusted_external_data>` tag MCP results get, so a page can't
   instruct Ultron.
3. Knowledge is kept only when the owner says so: "remember that" →
   the existing `remember_note`, never automatic ingestion of web text.
   Economy mode makes the summarising step Haiku-priced.

The token cost is then a short question plus a few snippets per lookup,
and zero when nobody is asking.

**Both built 2026-09-16 (SearXNG approved by the owner):**

- *Sentinel* — `_sentinel_run_once()` on a daemon thread
  (`ULTRON_SENTINEL_INTERVAL_SECONDS`, default 300), admin-only
  `GET /api/security/threats`, chat tool `get_threat_summary`, a live
  Security-tab card replacing the old illustrative "Posture" card, and
  `dev-tools/test_sentinel.py`. Zero LLM tokens.
- *Scout* — `ultron-searxng` service in `docker-compose.yml` (no host
  port, compose-network only, `searxng/settings.yml` enables JSON and
  disables the limiter), the `web_search` chat tool (inert until
  `ULTRON_SEARXNG_URL`; results wrapped as `<untrusted_external_data>`;
  admin-only; outside Economy mode), the room's Scout desk lighting up
  after a reply that used it, and `dev-tools/test_web_search.py`.
  Verified end-to-end: a real chat reply cited a real URL from the
  self-hosted engine.
