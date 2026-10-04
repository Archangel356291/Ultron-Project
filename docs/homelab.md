# Viking home lab — inventory

Phase 0 discovery, 2026-10-03. Read-only snapshot; no secrets here (those live in
Bitwarden and in `/root/viking-secrets/<service>.env` on the host that runs the service).
Access sheet for people: Slack #viking-lab-access.

## Network

- LAN: `192.168.0.0/24`, gateway/router TP-Link Archer C4000 at `192.168.0.1` (DHCP primary DNS = `.52`).
- Tailnet: `tailc5bde9.ts.net`, MagicDNS on. `viking` advertises `192.168.0.0/24` as a subnet router (approved),
  so phones reach LAN addresses directly. Tailscale global nameserver = pihole-1 (`100.71.18.122`).
- Nothing is port-forwarded on the router. No Funnel, no public reverse proxy. LAN + Tailscale only.

## Hosts

| Host | Role | LAN IP | Tailscale IP | OS | CPU / RAM / Disk | Headroom (2026-10-03) |
|---|---|---|---|---|---|---|
| `viking` | Proxmox VE hub, subnet router | 192.168.0.50 | 100.124.181.29 | PVE 9.2.21 / Debian 13 | 6c, 31 GB, 1 TB NVMe (local-lvm 816 GB) | 22 GB RAM avail, root 8 % used, local-lvm 2 % used |
| `viking-ai` | ZimaBoard #1: Jellyfin, future local-AI box (T4 on order) | 192.168.0.141 | 100.111.185.110 | ZimaOS 1.7.1 | 4c Alder Lake-N, 15 GB | 13 GB RAM avail, /DATA 15 %, models 1 %, models2 1 % |
| `viking-storage` | ZimaBoard #2: backup target | 192.168.0.176 | 100.77.41.83 | ZimaOS 1.7.1 | 4c Alder Lake-N, 15 GB | 14 GB RAM avail, /media/backups 26 % used (236/932 GB) |
| `desktop-47v3oim` | Owner's Windows PC (not lab infra) | DHCP | 100.114.166.96 | Windows 11 | — | runs Odin's Eye backend + security-lab stacks in Docker Desktop |

## Proxmox guests (on viking)

| ID | Name | LAN IP | Tailscale | Type / size | Purpose | Status |
|---|---|---|---|---|---|---|
| CT 100 | `viking-dash` | 192.168.0.51 | — | LXC 2c/2 GB/16 GB | Bare Debian 13 template for throwaway test CTs | running, empty |
| CT 101 | `viking-dev` | 192.168.0.54 | 100.104.198.83 | LXC 4c/4 GB/32 GB | Coding box: code-server, Syncthing, Claude remote control | running, 3.1 GB RAM avail, disk 22 % |
| CT 110 | `pihole` | 192.168.0.52 | 100.71.18.122 (`pihole-1`) | LXC 1c/512 MB/4 GB | Pi-hole v6 DNS for LAN + tailnet | running, 443 MB RAM avail, disk 29 % |
| VM 120 | `odin-docker` | 192.168.0.53 | 100.87.191.83 | VM 4c/16 GB/200 GB | Docker 29 + Ollama (CPU, no models yet); Phase 1 stacks in `/opt/stacks` | running, snapshot `pre-phase1-20261003` exists |

All guests: `onboot=1`, Proxmox firewall on (`/etc/pve/firewall/<id>.fw`), unprivileged CTs, SSH key-only.
CT 9100 (restore test) no longer exists.

## Services and ports

| Service | Host | URL / port | Notes |
|---|---|---|---|
| Proxmox web UI | viking | https://192.168.0.50:8006 | TOTP on root@pam and archangel@pve |
| Pi-hole admin | pihole | http://192.168.0.52/admin, https://pihole-1.tailc5bde9.ts.net | DNS :53 TCP/UDP. Upstreams currently `8.8.8.8`, `8.8.4.4` (roll-back values for Phase 3 Unbound) |
| Jellyfin | viking-ai | http://192.168.0.141:8096 | ZimaOS App Store install; `/media/models` -> `/Media` (Movies, Music, TV Shows). `/health` returns 200 |
| ZimaOS web UI | viking-ai, viking-storage | http://<ip>/ (:80) | SMB :139/:445 on both; SSH :22 key-only, user `Archangel` |
| code-server | viking-dev | http://192.168.0.54:8080, https://viking-dev.tailc5bde9.ts.net | `tailscale serve` -> 127.0.0.1:8080, tailnet only |
| Syncthing | viking-dev + PC | sync :22000; GUI localhost-only | folder `ultron-project` |
| Dockge | odin-docker | http://192.168.0.53:5001 | `/opt/stacks/dockge`, image `louislam/dockge:1.5.0`. Has the docker socket (root-equivalent); first visit creates the admin |
| Uptime Kuma | odin-docker | http://192.168.0.53:3001 | `/opt/stacks/uptime-kuma`, image `louislam/uptime-kuma:2.5.5`; first visit creates the admin; notifications: pending Slack webhook / Gmail app password |
| Homepage | odin-docker | http://192.168.0.53:3000 | `/opt/stacks/homepage`, image `ghcr.io/gethomepage/homepage:v2.4.0`; config in `config/*.yaml`; Proxmox widget uses token `homepage@pve!homepage` (PVEAuditor) from `/root/viking-secrets/homepage.env` |
| Watchtower | odin-docker | (no UI) | `/opt/stacks/watchtower`, `containrrr/watchtower:1.7.1`, **monitor-only** (`WATCHTOWER_MONITOR_ONLY=true`, `NO_RESTART`), daily 07:00 check; needs `DOCKER_API_VERSION=1.44` with Docker 29; Slack URL goes in `/root/viking-secrets/watchtower.env`. Upstream repo is archived; `nickfedor/watchtower` is the maintained fork if it breaks |
| Ollama | odin-docker | 127.0.0.1:11434 (loopback only) | containers on the same VM must use `host.docker.internal` or an `OLLAMA_HOST` change |
| Odin's Eye backend | PC | https://100.114.166.96:5000 | see `odin-backend/`, `odin-portfix.cmd` |

Where compose files live: Docker services on `odin-docker` go in `/opt/stacks/<service>/compose.yaml`, all on the user-defined docker network `lab`.
Secrets: `/root/viking-secrets/<service>.env` (root, 0600) **hardlinked** to `/opt/stacks/<service>/.env` so Dockge (root inside its container) and
`sudo docker compose` read the same single file. Stacks with an `.env` must be started with `sudo docker compose up -d`; the odin user can run the others.
New ports need a rule in `/etc/pve/firewall/120.fw` (LAN + tailnet sources only).
Jellyfin is a ZimaOS App Store app (ZimaOS manages its compose). Nothing on `viking-dev` or `viking-dash` runs in Docker yet.

## Backups

- Job `backup-7360b01c-6b75`: nightly `vzdump` of **all** guests, 03:00 local (`America/Los_Angeles`), zstd, snapshot mode,
  `keep-last=7`, to storage `zima-backups` = CIFS `//192.168.0.176/proxmox` mounted at `/mnt/pve/zima-backups`
  (= `/media/backups/proxmox` on viking-storage, md0 RAID).
- Last run: **2026-10-03 05:00–05:02, finished successfully** (CT 100 13 s, CT 101 57 s, CT 110 12 s, VM 120 82 s). VM 120 archive 2.4 GB, CT 101 2.7 GB, CT 110 0.4 GB.
- Older artefact: `/mnt/pve/zima-backups/pc-stacks/pc-pihole-jellyfin-stacks-2026-10-02.tgz` (archive of the retired PC Pi-hole/Jellyfin stacks).
- Off-site: restic -> Backblaze B2 bucket `viking-backups`. **Disabled** (`restic-backup.timer` disabled) because the one 10.8 GB snapshot exceeds the 10 GB free cap. Decision pending (Phase 8).
- Proxmox e-mail alerts go to Gmail via SMTP target `gmail`.

## Security state

- viking: SSH key-only, fail2ban jails `sshd` + `proxmox`, datacenter firewall input-DROP with LAN + tailnet allow for 22/8006/ICMP and UDP 41641.
- Guests: per-guest firewall files; **a new published service needs a rule in `/etc/pve/firewall/<id>.fw`**.
- ZimaBoards: SSH key-only. Docker socket needs sudo (password), so container listing from automation is not possible there.
- Tailscale ACL draft exists, **not applied** (Phase 3).

## Observations from Phase 0 (nothing changed)

1. Clocks/timezones differ: viking, viking-dev, viking-ai = `America/Los_Angeles`; pihole, odin-docker, viking-storage = `UTC`. Harmless, but log correlation is confusing. Fix candidate: `timedatectl set-timezone America/Los_Angeles` on the three UTC hosts (needs OK).
2. `lm-sensors` is not installed on viking, so no temperature readout there yet (Netdata in Phase 4 covers it).
3. Ollama has **no models pulled** and listens on loopback only.
4. Backblaze remains over the free cap; timer disabled; nothing lost (nightly local vzdump is healthy).
5. Loose ends from the brief already resolved: CT 9100 is gone, and the old `pihole`/`jellyfin` Tailscale nodes are no longer in the machine list. Remaining tailnet devices: viking, viking-dev, viking-ai, viking-storage, odin-docker, pihole-1, desktop-47v3oim, galaxy-s25-fe, dedede (android, offline 10 h), pixel-7 (android, offline 15 d).
6. `/media/models2` (932 GB) on viking-ai is empty — good candidate for Immich/Paperless data if viking-storage gets tight.

## TODO

- Move Ollama to viking-ai after the T4 is installed and passthrough/drivers are verified (Phase 2 note).
- Wazuh skipped (too heavy for this hardware); revisit if a bigger box arrives.
