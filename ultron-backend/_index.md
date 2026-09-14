# ultron-backend index

- [[CODE-AUDIT|CODE-AUDIT]] — living log of full-codebase audits (backend + bot). Latest pass (2026-09-13): no bugs found.
- [[README|README]] — what the backend does: Flask API for CPU/memory/temp/Docker/disk/updates, primary target Windows 11, runs unmodified on the Raspberry Pi 400/Linux. Covers the `beta_tester` role and now also serves the dashboard itself at `/` (fixes a mobile-browser `file://` bug).
- [[BETA-LAUNCH-CHECKLIST|BETA-LAUNCH-CHECKLIST]] — beta launch readiness tracker. Beta test #1 closed out (2026-09-13) as a full success across two real devices over Tailscale, both roles, voice included.
- [[REMOTE-ACCESS|REMOTE-ACCESS]] — Tailscale remote-access walkthrough. Its grants example was fixed (2026-09-13) after being caught by a real save error — `autogroup:self` only works as a destination, not a source.
