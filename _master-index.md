# Master Index

Vault root. Read this first, then only the folder `_index.md` you need, then only the specific note.

## Folders

- `docs/` — design specs, roadmaps, and module/graph/game design notes moved out of the root (COLOR_PALETTES, LOOT_SYSTEM, GAME_MASTER_ROADMAP, ULTRON-COLOR-SYSTEM, the MODULE-* and KNOWLEDGE-GRAPH/GRAPH-SCHEMA/HOME-* notes, LAUNCH-READINESS, FUTURE-TASKS, FINANCIAL-ACTION-BOUNDARY, GIT-SECRET-AUDIT). Wikilinks resolve by name, so `[[COLOR_PALETTES]]` etc. still work from anywhere.
- [[odin-backend/_index|odin-backend]] — Flask backend (home lab data, chat/voice, beta launch checklist, Tailscale remote-access setup).
- [[dev-tools/README|dev-tools]] — test/mock infrastructure for development only, not deployed with the real backend. Single note, no sub-index yet.
- [[odin-discord-bot/README|odin-discord-bot]] — Discord remote-control surface for the backend; no logic of its own. Single note, no sub-index yet.

## Root notes

- [[README|README]] — architecture and design principles: Flask backend + dashboard + Discord bot, one shared implementation. Has a "Contributors" section (Core: owner + Claude Code; Beta testers; Other contributors) with room to grow.
- [[PROJECT-SUMMARY-FOR-CLAUDE-CODE|PROJECT-SUMMARY-FOR-CLAUDE-CODE]] — the history/why behind the build, for judgment calls not covered in README.
- [[AGENT_CAPABILITIES_AND_GOVERNANCE|AGENT_CAPABILITIES_AND_GOVERNANCE]] — the single source of truth for Odin's agents: audit, roles (engineering = Claude Code; security + monitoring = Sentinel), capability matrix, approved scope (this PC only), task lifecycle, budgets, controls, status.
- [[ROADMAP-FINDINGS-2026-09-16|ROADMAP-FINDINGS-2026-09-16]] — findings for roadmap items 2–5 (offline mode: fixed reconnect + self-hosted fonts; API-lite and PWA scoped as yes/no proposals; tool survey). Item 6 blocked on the owner naming the two missing subagents.
- [[fonts/README|fonts]] — self-hosted OFL typefaces served at `/fonts/`, sources and licence table. Single note, no sub-index.
- [[ULTRON-DASHBOARD-DESIGN-SPEC|ULTRON-DASHBOARD-DESIGN-SPEC]] — pixel-sampled design analysis of the dashboard against the reference image. Recovered (2026-09-13) from an untracked backup zip after going missing pre-repo; mostly historical, its one open recommendation is now applied.
- [[Welcome|Welcome]] — unedited default Obsidian starter note.

`graphify-out/` is excluded here — it's Graphify's own auto-generated graph output, browse it directly or via `graphify query`.

## Slack channels

External (not part of this vault) — the `aiodinseye` Slack workspace, for team communication:

- `#all-ai-odin-project` — team-wide announcements.
- `#odin-ai-personal-home-lab-assistant-` — project-specific discussion, technical implementation updates.
- `#beta-testers` — for anyone helping test Odin: access scope, voice-reply instructions, the $1.00 spend cap, and where to report issues.
- `#contributors` — for anyone contributing beyond beta testing (code, docs, funding, infrastructure); mirrors the README's "Other contributors" table.
