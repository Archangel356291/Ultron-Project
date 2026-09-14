# Code audit log

Living log of full-codebase audits (backend + Discord bot), separate from
the beta launch checklist's feature-by-feature verification. Each entry
covers what was actually checked and how, not just "looked fine."

## 2026-09-13 — clean pass, no bugs found

**What was checked:**
- `ast.parse` on every `.py` file in the project (`app.py`, `bot.py`,
  `test_mcp_server.py`, everything in `dev-tools/fake_pkgs/`) — all parse
  clean.
- Live-ran the real backend (real venv, no fakes) and hit every read
  endpoint: health, status, containers, storage, systems, activity,
  dev/repos, trades (+ summary + tax-lots), security auth-log, CVE scan,
  chat usage, MCP servers, whoami. The 502s that came back (docker CLI
  missing, no Security event log entries on this dev machine) are real
  "dependency unavailable" responses, not bugs.
- Live-tested the trade write path (`POST /api/trades`, FIFO summary,
  `DELETE /api/trades/<id>`) against the **real** `ultron.db` — inserted
  one test BTC trade, confirmed the summary/holding math was correct,
  then deleted it immediately to restore the database to its prior state.
  Worth calling out since it means the real trade ledger was briefly
  touched during this audit, not a throwaway copy.
- Re-verified the `beta_tester` RBAC boundary still holds (200 on
  trades, 403 on status) after everything else above.
- Read the path-traversal guard on `/api/dev/repos/<repo>/diff`
  (basename-matched against the `ULTRON_CODE_REPOS` allowlist, can't be
  pointed at an arbitrary path), grepped every `subprocess.run` call for
  `shell=True` (none), and every `conn.execute` call for string-built SQL
  (none — all parameterized).
- Loaded `bot.py` as a module against `dev-tools/fake_pkgs`'s fake
  `discord`/`aiohttp` — all `@bot.tree.command` registrations and
  module-level config parsing (`DISCORD_BOT_TOKEN`, `ULTRON_API_TOKEN`,
  `ULTRON_DISCORD_ALLOWED_USERS`) execute without error.
- Grepped for `TODO`/`FIXME`/`XXX`/`HACK` across `app.py` and `bot.py` —
  none.
- Confirmed `requirements.txt` for both backend and bot matches actual
  top-level imports in each.

**Result:** no bugs found. The graceful-degradation patterns (missing
`anthropic` package, missing Docker CLI, no configured repos) all behave
as documented rather than crashing.

**Not covered this pass:** `ultron-dashboard.html`'s JS — already
verified separately (see git log) via `node --check`, ID-count, and
live click-through during the visual-match work; not re-audited here.

## 2026-09-13 (later) — Discord bot actually launched for real, plus a genuine bug found and fixed

**What was checked:**
- Re-ran `ast.parse` on `app.py` and `bot.py` after the per-tester token
  change and the new dashboard-serving route — clean.
- Re-verified RBAC live: admin token 200s on `/api/status`, no/garbage
  token 401s, `/api/whoami` reports role and name correctly.
- Re-grepped for `shell=True` (still none) and string-built SQL (still
  none — 13 `conn.execute` calls, all parameterized).
- Confirmed `.env` is still correctly gitignored after this session's
  edits to it.
- Confirmed the Discord bot's confirm-button per-user gate
  (`interaction.user.id != self.author_id`) is still intact on
  `ConfirmActionView`.

**Real bug found and fixed:** `ultron-discord-bot/start-bot.ps1` never
loaded from `.env` at all — unlike the backend's `start-ultron.ps1`, it
expected secrets pasted directly into the script itself, which is
git-tracked. That's the exact mistake this project already got burned by
once (see the Phase 1 security-pass note above about a hardcoded token
found and scrubbed from history). Rewrote it to load `.env` the same way
the backend does, with the paste-into-script path now commented out and
clearly marked as a fallback. Separately, `.env` had a real, working
Discord bot token stored under the wrong key (`discord_token`, lowercase,
which nothing reads) instead of `DISCORD_BOT_TOKEN` — renamed it, which
is what let the bot actually start for the first time.

**Live-verified, not just read:** started the real backend and bot
together, confirmed the bot token authenticates with Discord (gateway
connects), invited it to a real test server, confirmed all 15 slash
commands synced, then had a human run `/status` and `/ask` for real in
Discord — cross-checked against the backend's own request log
(`GET /api/status` → 200, `POST /api/chat` → 200) to confirm the full
round trip, not just "Discord showed a reply."

**Result:** one real security-hygiene bug fixed (token in a git-tracked
script instead of `.env`); everything else re-verified clean.

## 2026-09-13 (later still) — connection tracking + beta spend cap added

**What was checked:**
- `ast.parse` / `python -m py_compile` on `app.py` and `bot.py` after
  adding the `_PRESENCE` table, `/api/connections`, the
  `LLM_PRICING_PER_MTOK` cost math, and the `beta_name`/`cost_usd`
  columns on `llm_usage` — both clean.
- Grepped `app.py` for `shell=True` (still none) and every
  `conn.execute` call (now 18, all still parameterized with `?` — no
  string-built SQL introduced by the two new queries added).
- Confirmed the `llm_usage` schema change is a live migration
  (`PRAGMA table_info` + `ALTER TABLE ADD COLUMN`), not a
  `CREATE TABLE IF NOT EXISTS` that would silently no-op against an
  existing `ultron.db` — verified by running it against the real
  pre-existing database file, not a fresh one.
- Confirmed the spend cap only applies to `g.role == "beta"` and never
  to admin — read the check in `chat()` directly rather than trusting
  the comment.
- `/api/connections` and `/api/whoami`'s new fields are read-only (no
  write path, no new mutation of host state) — consistent with this
  project's "every chat tool is read-only" boundary; neither is exposed
  to Ultron's own chat tools.

**Live-verified, not just read:** `dev-tools/test_beta_spend_cap.py`
drives real `/api/chat` requests through Flask's test client against a
scripted fake Anthropic client, asserting: a call under the cap
succeeds; cumulative spend is computed correctly from real usage
numbers at real per-model pricing; the call that pushes spend over the
cap still succeeds (the cap gates the *next* call, using spend-so-far);
the following call is genuinely refused (429, Anthropic never called —
proven by not queuing a canned reply, so a bypass would surface as the
fake's "script exhausted" error instead of a clean 429); and an admin
token making the same request immediately after is unaffected. Also
asserts both identities (the capped-out beta tester and the admin) show
up correctly in `/api/connections`.

**Result:** no bugs found. New Discord bot command (`/connections`) and
dashboard card (Settings → Connections) reuse the existing `require_auth`
/ admin-gating patterns rather than introducing new ones — checked for
whether either added a second gate to keep in sync with the backend's,
and neither does; both are thin callers of the one backend endpoint.
