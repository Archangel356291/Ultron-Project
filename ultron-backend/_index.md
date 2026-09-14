# ultron-backend index

- [[CODE-AUDIT|CODE-AUDIT]] — living log of full-codebase audits (backend + bot). Latest pass (2026-09-13): found and fixed a real bug — the Discord bot's start script never loaded `.env`, so its token had to be pasted into a git-tracked file.
- [[README|README]] — what the backend does: Flask API for CPU/memory/temp/Docker/disk/updates, primary target Windows 11, runs unmodified on the Raspberry Pi 400/Linux. Covers the `beta_tester` role and now also serves the dashboard itself at `/` (fixes a mobile-browser `file://` bug).
- [[BETA-TESTER-GUIDE|BETA-TESTER-GUIDE]] — plain-language walkthrough written for the tester themselves (not a dev) — installing Tailscale, connecting, what they can/can't do, what to report. Hand this to people directly, don't just point them at the repo.
- [[BETA-TESTERS|BETA-TESTERS]] — credits roster for beta testers plus the add/remove process. Each tester now gets their own distinct token (`ULTRON_BETA_TOKENS`, name:token pairs) — independently revocable, attributed via `/api/whoami`. Roster empty for now.
- [[BETA-LAUNCH-CHECKLIST|BETA-LAUNCH-CHECKLIST]] — beta launch readiness tracker. Discord bot now set up, invited to a real server, and verified live (2026-09-13) — closes the last "never started" gap from Phase 1.
- [[REMOTE-ACCESS|REMOTE-ACCESS]] — Tailscale remote-access walkthrough. Its grants example was fixed (2026-09-13) after being caught by a real save error — `autogroup:self` only works as a destination, not a source.
