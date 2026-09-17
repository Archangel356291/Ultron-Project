# Launch readiness — 2026-09-16

Owner's question: how much building is left before Ultron is a solid, live
system that can be updated as needed — held to the standard an app store
would expect of a working product, without actually submitting to one.
Hardware is out of scope.

**Short answer.** The features are there. What is left is hardening: how it
is served, how it signs you in, how it is updated, and how much it could
damage if it were ever broken into. About two weeks of focused work clears
the must-fix list; the full list is four to six weeks. The day counts are
estimates from reading the code, not measurements.

Everything below was checked against the code or the running system on
2026-09-16; each item says what was seen.

## Where it stands

- Running: 8 containers up, no errors in the backend or bot logs, hourly
  Brain refresh succeeding, installable app served and its worker active.
- 31 self-checks in `dev-tools/` pass (`test_mcp_server.py` is a fixture
  server, not a check).
- Already at a good bar: HTTPS with a real certificate, sign-in lockout,
  security headers, spend caps, read-only tools with preview-then-confirm
  actions, secret scanning on commit, SAST script (gitleaks clean, semgrep
  one warning).
- Size: `app.py` 5,961 lines, `ultron-dashboard.html` 5,818, bot 941.

## Must fix before calling it a release (about 9–13 days)

| # | Gap | What was seen | Work |
|---|---|---|---|
| 1 | Served by Flask's development server | Container log prints "This is a development server. Do not use it in a production deployment"; Dockerfile `CMD ["python", "app.py"]` | Serve with waitress or gunicorn, add a container `HEALTHCHECK` (backend, bot and SearXNG have none), run as a non-root user (backend runs as root). ~1 day |
| 2 | The password is the session | `performConnect` keeps the password as the bearer token for every call; "remember me" writes `{url, username, password}` to `localStorage` in plain text; nothing expires or can be revoked | Sign-in returns a session token with an expiry; remember-me stores that token, not the password; sign-out invalidates it; the bot gets its own token. ~2–3 days with tests |
| 3 | Blast radius of a break-in | The backend container is root, has `/var/run/docker.sock`, and mounts all of `C:\` and `D:\` read-only. Anyone who got code running in it could read every file on the PC and control Docker | Mount only what the storage figures need; put a socket proxy in front of Docker limited to the calls Ultron makes. ~1–2 days |
| 4 | Made-up data still on screen | Media tab's folder table is hard-coded (`plex-media 1.9 TB`, `backups 410 GB`…) with no id, so live data never replaces it. "mock data" wording and sample container rows remain as page defaults | Remove the table or back it with a real endpoint; delete the sample defaults. ~½ day |
| 5 | No release or update path | No version number, changelog, git tags or CI. `requirements.txt` uses ranges with no lock file, so two builds a month apart are different software. Database changes are 15 ad-hoc `CREATE/ALTER` statements with no schema version | A `VERSION` shown in Settings; pinned, hashed dependencies; migrations keyed on `PRAGMA user_version`; one update command that backs up the DB first and can roll back; CI running the self-checks and SAST on every push. ~2–3 days |
| 6 | Backups without a restore | `_run_backup` exists; there is no restore function and no restore has been rehearsed | Restore command plus a check that restores into a temp dir and reads it back. ~1 day |
| 7 | Failures are not handled centrally | No `@app.errorhandler`, no `logging` use: an unexpected exception returns an HTML error page to code expecting JSON, and nothing rotates logs | JSON error handler, structured logging with rotation, surface the last errors in the dashboard. ~1 day |

## Should fix to meet the quality bar (about 12–15 days)

| # | Gap | What was seen | Work |
|---|---|---|---|
| 8 | CSP allows inline script | `script-src 'self' 'unsafe-inline'` because all JS lives inside the one HTML file, 47 inline `onclick=`. That removes most of the protection CSP gives against injected script | Move JS and CSS into files (no build tool needed), bind events in code, drop `'unsafe-inline'`. ~2 days plus a regression pass |
| 9 | No automated UI checks | Every check is backend-side; the dashboard is verified by hand each time | A small Playwright smoke run: sign in, every tab renders without console errors, a chat round trip against the fake Anthropic package, phone width. The preview harness used on 2026-09-16 is most of it. ~2 days |
| 10 | Accessibility not audited | 14 `aria-` attributes in 5,818 lines; the sidebar items are `div`s with no `tabindex` or role, so they cannot be reached by keyboard | Keyboard and screen-reader pass, contrast check, real buttons for navigation. ~2 days |
| 11 | Setup is hand-assembly | Install means editing `.env`, issuing a Tailscale certificate, registering a scheduled task from PowerShell | A setup script and a `doctor` command that verifies each piece and says what is wrong. ~2–3 days |
| 12 | Privacy controls | Conversations and memories are kept in plain text by design, but there is no in-app way to export or delete them (only trades have a DELETE route) and no note saying what is sent to Anthropic, Fish Audio and Discord | Export and delete for chats and memories; a plain privacy note in Settings. ~1–2 days |
| 13 | Memory fills with duplicates | 9 of his 18 memories are near-identical "Recurring activity, last 7 days: 7x evolution_status_change" notes written by the trend distiller | Update the existing trend note instead of adding another; clean up the duplicates. ~½ day |
| 14 | SAST findings drift | Bandit: 1 high, 9 medium, 41 low. The findings doc records them as triaged, but nothing re-checks on change | Covered by CI in item 5; record accepted findings in a baseline file |

## Only if it is ever distributed beyond the owner

Not needed for the goal above, listed so it is not a surprise later.

- **The name and likeness.** "Ultron" is Marvel's trademark. The art is
  original, and personal use is fine, but a public or store release would
  need a different name and would be rejected with this one.
- Real multi-user accounts (today: one admin, beta testers as static tokens).
- A native wrapper and store paperwork; an inventory of third-party licences.

## Suggested order

1, 3, 2 (the security trio, since each limits the damage of the others),
then 5 so every later change ships through a repeatable path, then 4, 6, 7.
The should-fix list after that, 9 first so the rest are regression-checked.
