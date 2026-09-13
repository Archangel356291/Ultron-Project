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
