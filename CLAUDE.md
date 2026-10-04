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
| CT 110 `pihole` | 192.168.0.52 | Pi-hole DNS for the LAN and tailnet (router DHCP hands out .52); upstream is Unbound on 127.0.0.1#5335 in the same CT; serves `*.lan` names -> odin-docker's Caddy | http://192.168.0.52/admin, https://pihole.lan, tailnet `pihole-1` |
| VM 120 `odin-docker` | 192.168.0.53 | Docker + Ollama host for lab services. Stacks in `/opt/stacks/<svc>/compose.yaml`: Dockge :5001, Uptime Kuma :3001, Homepage :3000, Open WebUI :8080, Watchtower (monitor-only). Secrets in `/root/viking-secrets/`. Full inventory: `docs/homelab.md` | `ssh odin@192.168.0.53` |
| CT 100 `viking-dash` | 192.168.0.51 | bare Debian 13, purpose TBD | root via pct |

Nightly `vzdump` of all guests at 03:00 to the `zima-backups` share (keep last 7). Other boxes: `viking-ai` 192.168.0.141 (ZimaOS, local AI project, Jellyfin :8096), `viking-storage` 192.168.0.176 (ZimaOS, backups).

### viking-dev as home base (2026-10-02)

- **Browser VS Code:** code-server on viking-dev, port 8080, password auth (password lives in Slack #viking-lab-access, never in this repo). Listens on 127.0.0.1:8080 only; reach it via Tailnet HTTPS https://viking-dev.tailc5bde9.ts.net (the LAN :8080 URL no longer works). Not exposed to the internet.
- **Claude Code:** installed for `archangel`; also runs as a Remote Control service named `viking-dev` (systemd user unit `claude-remote`).
- **Syncthing:** one folder `ultron-project` = `C:\Ultron Project` on the PC <-> `/home/archangel/sync/Ultron Project` on viking-dev. `.stignore` excludes .env, keys, .ssh, credentials, node_modules, .venv. PC runs Syncthing from a Startup shortcut; viking-dev runs `syncthing@archangel`.
- **GitHub:** viking-dev has its own key `~/.ssh/id_ed25519_github` (pinned to github.com in ~/.ssh/config); git identity matches the PC. Repos stay private.
- **Gitea (self-hosted git):** https://git.lan on viking-dev (`/opt/stacks/gitea`, port 3000, SSH 2222). `Bitcoin Mining Tycoon` and `Ultrons APK Game` push to remote `gitea` there (`ssh://git@192.168.0.54:2222/archangel/<repo>.git`). Registration disabled.

### Security hardening (2026-10-02)

- **viking (Proxmox host):** SSH key-only, root `prohibit-password`; non-root admin `archangel@pve` (Administrator on /, TOTP via Datacenter > Permissions > Two Factor); CrowdSec (nftables bouncer, LAN/Tailscale whitelisted; replaced fail2ban 2026-10-03) also on odin-docker; Netdata local-only on :19999; datacenter firewall ON (input DROP; allows 8006, 22, ping from 192.168.0.0/24 + 100.64.0.0/10, UDP 41641 for Tailscale). Rollback: `pve-firewall stop` in the web console shell. Security-only unattended-upgrades (Proxmox repos excluded, no auto-reboot). rpcbind disabled. Alerts (backup results, SMART, update notices) go to Gmail via the Proxmox SMTP target `gmail` (default matcher); smartd mails root, which proxmox-mail-forward feeds into the same system.
- **Guests:** all CTs unprivileged, SSH key-only, security-only unattended-upgrades. Per-guest Proxmox firewalls (LAN + Tailscale sources only): viking-dash 22; pihole 53/80/443/22; viking-dev 22/8080/22000/21027 + 41641; odin-docker 22 + 41641. **Publishing a new service on odin-docker or viking-dev needs a rule in `/etc/pve/firewall/<id>.fw`.**
- **code-server / Syncthing:** both GUIs LAN+Tailscale only (code-server) or localhost only (Syncthing GUI, now with a login); Syncthing global discovery, relays and NAT traversal are off on both ends. The PC runs `tailscale set --accept-routes=false` so LAN traffic never detours via viking.
- **Passwords** (code-server, Pi-hole admin, Syncthing GUI) live only in Slack #viking-lab-access, never here.
- **Backups:** nightly 03:00 vzdump of all guests to `zima-backups` (keep 7). Test restore of viking-dash to a temp CT verified 2026-10-02. Off-site encrypted copy (restic -> Backblaze B2) recommended, not yet set up.
- **Monthly checklist:** apply pending updates (`apt list --upgradable` on viking + guests, ZimaOS update page); review Tailscale machines list and remove unknown/expired devices; restore one backup to a temp CT and boot it; re-run the LAN port scan from viking-dev (`sudo nmap -sS -Pn --top-ports 1000 --open 192.168.0.0/24`) and compare with the last one; check fail2ban (`fail2ban-client status sshd`).
