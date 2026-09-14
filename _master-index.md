# Master Index

Vault root. Read this first, then only the folder `_index.md` you need, then only the specific note.

## Folders

- [[ultron-backend/_index|ultron-backend]] — Flask backend (home lab data, chat/voice, beta launch checklist, Tailscale remote-access setup).
- [[dev-tools/README|dev-tools]] — test/mock infrastructure for development only, not deployed with the real backend. Single note, no sub-index yet.
- [[ultron-discord-bot/README|ultron-discord-bot]] — Discord remote-control surface for the backend; no logic of its own. Single note, no sub-index yet.

## Root notes

- [[README|README]] — architecture and design principles: Flask backend + dashboard + Discord bot, one shared implementation. Now links to the beta-tester guide/credits and carries its own "Beta testers" section.
- [[PROJECT-SUMMARY-FOR-CLAUDE-CODE|PROJECT-SUMMARY-FOR-CLAUDE-CODE]] — the history/why behind the build, for judgment calls not covered in README.
- [[ULTRON-DASHBOARD-DESIGN-SPEC|ULTRON-DASHBOARD-DESIGN-SPEC]] — pixel-sampled design analysis of the dashboard against the reference image. Recovered (2026-09-13) from an untracked backup zip after going missing pre-repo; mostly historical, its one open recommendation is now applied.
- [[Welcome|Welcome]] — unedited default Obsidian starter note.

`graphify-out/` is excluded here — it's Graphify's own auto-generated graph output, browse it directly or via `graphify query`.
