## graphify

This project has a knowledge graph at graphify-out/ with god nodes, community structure, and cross-file relationships.

Rules:
- For codebase questions, first run `graphify query "<question>"` when graphify-out/graph.json exists. Use `graphify path "<A>" "<B>"` for relationships and `graphify explain "<concept>"` for focused concepts. These return a scoped subgraph, usually much smaller than GRAPH_REPORT.md or raw grep output.
- If graphify-out/wiki/index.md exists, use it for broad navigation instead of raw source browsing.
- Read graphify-out/GRAPH_REPORT.md only for broad architecture review or when query/path/explain do not surface enough context.
- After modifying code, run `graphify update .` to keep the graph current (AST-only, no API cost).

## Hand-written notes (vault)

This folder is also an Obsidian vault. Graphify's rules above are for code/project questions. For questions about the user's own hand-written notes, use a separate, cheaper path:

- Read `_master-index.md` at the vault root first.
- Then read only the relevant folder's `_index.md` (not every folder has one — only folders with more than a couple of notes).
- Then open only the specific note(s) that are actually relevant. Never bulk-read a whole folder.
- Whenever a note is added or materially edited, update that folder's `_index.md` and the root `_master-index.md` in the same turn — this is your job, not the user's.
- Prefer Obsidian `[[wikilink]]` references over duplicating information across notes.

## Home lab (viking)

Proxmox host `viking` = 192.168.0.50 (web UI :8006, `ssh root@192.168.0.50`, key auth). Tailnet node `viking` is also the LAN subnet router. Access sheet lives in Slack #viking-lab-access.

| Guest | Address | Purpose | Login |
|---|---|---|---|
| CT 101 `viking-dev` | 192.168.0.54 | Coding dev box for VS Code Remote-SSH (Debian 13, Docker, Python 3.13, Node 20). Day-to-day user is `archangel`, never root. | `ssh viking-dev` (entry in ~/.ssh/config, key id_ed25519) |
| CT 110 `pihole` | 192.168.0.52 | Pi-hole DNS for the LAN and tailnet (router DHCP hands out .52) | http://192.168.0.52/admin, tailnet `pihole-1` |
| VM 120 `odin-docker` | 192.168.0.53 | Docker + Ollama host for lab services | `ssh odin@192.168.0.53` |
| CT 100 `viking-dash` | 192.168.0.51 | bare Debian 13, purpose TBD | root via pct |

Nightly `vzdump` of all guests at 03:00 to the `zima-backups` share (keep last 7). Other boxes: `viking-ai` 192.168.0.141 (ZimaOS, local AI project, Jellyfin :8096), `viking-storage` 192.168.0.176 (ZimaOS, backups).
