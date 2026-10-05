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
| CT 110 | `pihole` | 192.168.0.52 | 100.71.18.122 (`pihole-1`) | LXC 1c/1 GB/4 GB (raised from 512 MB 2026-10-03, snapshot `pre-unbound-20261003`) | Pi-hole v6 DNS for LAN + tailnet, **Unbound** recursive resolver on 127.0.0.1#5335 | running, ~940 MB RAM avail |
| VM 130 | `viking-pbs` | 192.168.0.55 | — | VM 2c/3 GB (balloon 2 GB)/32 GB | Proxmox Backup Server 4.2.7 (Debian 13 cloud image + PBS repo). Datastore `viking-storage` = CIFS `//192.168.0.176/backups/pbs` mounted at `/mnt/pbs` (uid/gid 34 = backup). SSH `pbsadmin@192.168.0.55` (ultron_pi_ed25519 key, sudo). Secrets `/root/viking-secrets/pbs.env` in the VM (copies: odin-docker `pbs.env`, viking `pbs-client.env`) | running; 130.fw allows 22 + 8007 |
| VM 120 | `odin-docker` | 192.168.0.53 | 100.87.191.83 | VM 4c/16 GB/200 GB | Docker 29 + Ollama (CPU, no models yet); Phase 1 stacks in `/opt/stacks` | running, snapshot `pre-phase1-20261003` exists |

All guests: `onboot=1`, Proxmox firewall on (`/etc/pve/firewall/<id>.fw`), unprivileged CTs, SSH key-only.
CT 9100 (restore test) no longer exists.

## Services and ports

| Service | Host | URL / port | Notes |
|---|---|---|---|
| Proxmox web UI | viking | https://192.168.0.50:8006 | TOTP on root@pam and archangel@pve |
| Pi-hole admin | pihole | http://192.168.0.52/admin, https://pihole.lan, https://pihole-1.tailc5bde9.ts.net | DNS :53 TCP/UDP. Upstream = `127.0.0.1#5335` (Unbound) since 2026-10-03. **Rollback:** `pihole-FTL --config dns.upstreams '["8.8.8.8","8.8.4.4"]'` (pre-change copy: `/etc/pihole/pihole.toml.bak-2026-10-03`). Local DNS records `dns.hosts`: all `*.lan` names -> 192.168.0.53 |
| Unbound | pihole CT | 127.0.0.1:5335 (loopback only) | `/etc/unbound/unbound.conf.d/pi-hole.conf`, root hints `/var/lib/unbound/root.hints`, DNSSEC validating (dnssec-failed.org -> SERVFAIL verified), `unbound-resolvconf` disabled |
| Caddy | odin-docker | :80 / :443, names `dash.lan` `kuma.lan` `dockge.lan` `chat.lan` `jellyfin.lan` `pihole.lan` `proxmox.lan` | `/opt/stacks/caddy`, image `caddy:2.10`, internal CA (`tls internal`). Root CA download for devices: **http://ca.lan/viking-lab-root-ca.crt** (fingerprint SHA256 0F:17:51:C5:63:8D...2C:6A, valid to 2036-08). Installed in the PC's user Root store 2026-10-03. Key material in `/opt/stacks/caddy/data/caddy/pki/` (never copy root.key) |
| Jellyfin | viking-ai | http://192.168.0.141:8096, https://jellyfin.lan | ZimaOS App Store install; `/media/models` -> `/Media`. Libraries: Movies, Shows, Music, **Adult** (type home-videos, no internet metadata). Users: `Archangel` = owner's daily account (normal user, sees everything except Adult), `archangel-admin` = hidden admin for the dashboard, `private` = sees ONLY Adult, password is a 6-digit PIN (5 wrong tries locks it). Admins always see all libraries in Jellyfin, which is why the daily account was demoted. Media copied 2026-10-04 from the PC drive `E:\media copies` (39 movies, Angel S1-S5 partial, 9 adult titles) via SMB |
| ZimaOS web UI | viking-ai, viking-storage | http://<ip>/ (:80) | SMB :139/:445 on both; SSH :22 key-only, user `Archangel` |
| Gitea | viking-dev | https://git.lan (Caddy on odin-docker -> 192.168.0.54:3000); git over SSH `ssh://git@192.168.0.54:2222/archangel/<repo>.git` | `/opt/stacks/gitea` on viking-dev, `gitea/gitea:1.27.3`, SQLite, registration disabled, sign-in required to view, Actions off. Admin `archangel` (`~/viking-secrets/gitea.env` on viking-dev, copy in odin-docker's `/root/viking-secrets/gitea.env`). Repos: `bitcoin-mining-tycoon`, `ultrons-apk-game` (private, pushed 2026-10-04 from the PC; PC key id_ed25519 registered). 101.fw allows 3000 + 2222 from LAN/tailnet |
| n8n | odin-docker | https://flow.lan | `/opt/stacks/n8n`, `docker.n8n.io/n8nio/n8n:2.41.6`, SQLite in `./data`, owner = owner's Gmail (`/root/viking-secrets/n8n.env`, also holds `N8N_ENCRYPTION_KEY`, keep it or credentials in backups are unreadable). Sample workflow **Inbox file -> Slack**: Local File Trigger (polling, read-only mount of viking-storage `backups/inbox` at `/files/inbox`) -> HTTP Request to the Slack webhook via `$env.SLACK_WEBHOOK_URL` (so the URL is not stored in the workflow). Diagnostics/telemetry off. `NODES_EXCLUDE` keeps only the shell-command node disabled (n8n 2.x hides the Local File Trigger by default); file access limited to `/files` |
| code-server | viking-dev | https://viking-dev.tailc5bde9.ts.net | listens on 127.0.0.1:8080 only; published by `tailscale serve`, tailnet only (the old LAN URL :8080 is dead) |
| Syncthing | viking-dev + PC + phone | sync :22000; GUI localhost-only (`ssh -L 8384:127.0.0.1:8384 viking-dev`) | folders: `ultron-project` (PC <-> viking-dev), `phone` = `/home/archangel/sync/Phone` (viking-dev <-> Samsung phone, Syncthing-Fork, trashcan versioning 30 d). Discovery/relays off: devices are added by ID + explicit address (phone uses `tcp://192.168.0.54:22000`; it connects via the viking subnet router) |
| Dockge | odin-docker | http://192.168.0.53:5001 | `/opt/stacks/dockge`, image `louislam/dockge:1.5.0`. Has the docker socket (root-equivalent). Admin `archangel`, password in `/root/viking-secrets/dockge.env` |
| Uptime Kuma | odin-docker | http://192.168.0.53:3001 | `/opt/stacks/uptime-kuma`, image `louislam/uptime-kuma:2.5.5`, SQLite. Admin `archangel` (`/root/viking-secrets/uptime-kuma.env`). 19 monitors created by `/opt/stacks/_tools/setup.js` (idempotent); default notification = Slack #viking-alerts via incoming webhook (`/opt/stacks/_tools/notify.js`, URL in `/root/viking-secrets/slack-webhook.env`) |
| Homepage | odin-docker | http://192.168.0.53:3000 | `/opt/stacks/homepage`, image `ghcr.io/gethomepage/homepage:v2.4.0`; config in `config/*.yaml`; Proxmox widget uses token `homepage@pve!homepage` (PVEAuditor) from `/root/viking-secrets/homepage.env` |
| Watchtower | odin-docker | (no UI) | `/opt/stacks/watchtower`, `containrrr/watchtower:1.7.1`, **monitor-only** (`WATCHTOWER_MONITOR_ONLY=true`, `NO_RESTART`), daily 07:00 check; needs `DOCKER_API_VERSION=1.44` with Docker 29; Slack #viking-alerts notifications via shoutrrr, URL in `/root/viking-secrets/watchtower.env`. Upstream repo is archived; `nickfedor/watchtower` is the maintained fork if it breaks |
| Proxmox Backup Server | viking-pbs | https://backup.lan (Caddy -> https://192.168.0.55:8007), root@pam | Datastore `viking-storage` with prune job daily 04:30 (keep 7d/4w/3m), GC Saturday 03:30, verify Sunday 05:00 (re-verify after 30 days). PVE storage `viking-pbs` uses token `backup@pbs!pve` (DatastoreBackup on the datastore; the *user* backup@pbs needs the same ACL or the token's effective permission is empty). Creating the datastore over SMB took ~25 min (65k chunk dirs). First full backup of all guests 2026-10-04 08:44 UTC. **Test restore verified** the same day: CT 100 snapshot -> CT 9100 (192.168.0.59, unprivileged) restored in 1m28s at 12 MiB/s over SMB, booted Debian 13.7, stopped; CT 9100 kept until the owner OKs deletion |
| Netdata | viking | http://192.168.0.50:19999 (LAN + tailnet; cluster.fw rule) | v2.12 via kickstart, `--disable-cloud --disable-telemetry`, **not claimed** to Netdata Cloud (`/var/lib/netdata/cloud.d/cloud.conf` enabled=no). lm-sensors installed for CPU temps. Sees LXC guests via cgroups. **Not on the ZimaBoards**: ZimaOS has no package manager and `Archangel` has no passwordless sudo, so Docker can't be driven from automation there (owner can install Netdata from the ZimaOS App Store) |
| CrowdSec | viking + odin-docker | local API 127.0.0.1:8080 (viking) / **127.0.0.1:8081** (odin-docker, 8080 is Open WebUI) | v1.8.1 from the official repo, collections `crowdsecurity/linux` + `sshd`, community blocklist (CAPI) enabled, **nftables firewall bouncer** (own `crowdsec`/`crowdsec6` tables, independent of pve-firewall). Whitelist `/etc/crowdsec/parsers/s02-enrich/viking-whitelist.yaml`: 192.168.0.0/24, 100.64.0.0/10, 127/8 (+172.16/12 on odin-docker). viking also watches `pvedaemon`/`pveproxy` journald for web-UI brute force. **fail2ban replaced**: stopped + disabled on viking (config copy `/root/fail2ban.bak-2026-10-03`, package kept). Not installed on pihole / viking-dev (unprivileged LXC, SSH-only, LAN+tailnet-only already) |
| Vaultwarden | odin-docker | **https://vault.lan** only (no host port; Caddy -> `vaultwarden:80`) | `/opt/stacks/vaultwarden`, image `vaultwarden/server:1.37.3`, data `./data` (SQLite, in nightly vzdump). `SIGNUPS_ALLOWED=false`, invitations on: the owner's Gmail was **invited** from /admin, so "Create account" with that address works, anyone else gets refused. Admin page https://vault.lan/admin protected by an **argon2id** token stored in `data/config.json` (not env: Compose env-file interpolation eats the `$` in the hash); the plain admin password + hash are in `/root/viking-secrets/vaultwarden.env`. Push notifications off, password hints off. Bitwarden apps: set server URL to https://vault.lan after trusting the lab CA on the device |
| Immich | odin-docker | https://photos.lan, app URL http://192.168.0.53:2283 (fw rule) | `/opt/stacks/immich` (upstream compose v3.2.4 + `.env` hardlink of `/root/viking-secrets/immich.env`). Uploads on **viking-storage** via CIFS `/mnt/viking-storage/immich`; Postgres + ML cache on the VM disk. Admin = owner Gmail; phone app connected 2026-10-04 (URL must include `http://`, the app assumes https otherwise) |
| Paperless-ngx | odin-docker | https://docs.lan | `/opt/stacks/paperless`, `ghcr.io/paperless-ngx/paperless-ngx:3.2.1` + redis:8, SQLite. media/export/consume on viking-storage (`/mnt/viking-storage/paperless/*`), index+db local. Consumer polls every 30 s (inotify does not work over SMB). Admin `archangel` |
| Navidrome | odin-docker | https://music.lan | `/opt/stacks/navidrome`, `deluan/navidrome:0.64.2`, music **read-only** from viking-ai `/mnt/viking-ai/models/Music`. Admin `archangel`. Subsonic API for mobile apps |
| Audiobookshelf | odin-docker | https://books.lan | `/opt/stacks/audiobookshelf`, `ghcr.io/advplyr/audiobookshelf:2.37.1`. **No library yet** (no Audiobooks folder exists on the media drive and we do not create folders there). Admin `archangel` |
| Jellyseerr | odin-docker | https://requests.lan | `/opt/stacks/jellyseerr`, `fallenbagel/jellyseerr:2.7.3`, title "Viking Requests". Owner signed in with Jellyfin 2026-10-04; Movies + Shows libraries enabled; Sonarr/Radarr linked with `preventSearch` on (requests queue until sources exist) |
| Sonarr / Radarr / Prowlarr | odin-docker | https://sonarr.lan, https://radarr.lan, https://prowlarr.lan | `/opt/stacks/arr` (lscr.io/linuxserver sonarr:4.0.20, radarr:6.4.4, prowlarr:2.6.5). Forms auth, user `archangel`. Root folders `/tv` and `/movies` = viking-ai TV Shows / Movies (rw mount, nothing writes). Prowlarr synced to both. **Zero indexers, zero download clients by design** |
| Open WebUI | odin-docker | http://192.168.0.53:8080 | `/opt/stacks/open-webui`, image `ghcr.io/open-webui/open-webui:v0.11.4`, **host network** (reaches loopback Ollama). Admin = owner's Gmail, password in `/root/viking-secrets/open-webui.env`; `ENABLE_SIGNUP=false` (verified 403), new users would land as `pending`; OpenAI API + community sharing off |
| Ollama | odin-docker | 127.0.0.1:11434 (loopback only, unchanged) | model pulled: `llama3.2:3b` (2 GB, CPU). Only Open WebUI (host net) reaches it |
| Odin's Eye backend | PC | https://100.114.166.96:5000 | see `odin-backend/`, `odin-portfix.cmd` |

Where compose files live: Docker services on `odin-docker` go in `/opt/stacks/<service>/compose.yaml`, all on the user-defined docker network `lab`.
Secrets on odin-docker (root, 0600): `homepage.env` (Proxmox token `homepage@pve!homepage`, PVEAuditor), `watchtower.env`, `slack-webhook.env` (Slack app 'Viking Alerts', channel #viking-alerts), `vaultwarden.env`, `tailscale-api.env`, `uptime-kuma.env`, `dockge.env`, `open-webui.env`. Layout: `/root/viking-secrets/<service>.env` **hardlinked** to `/opt/stacks/<service>/.env` so Dockge (root inside its container) and
`sudo docker compose` read the same single file. Stacks with an `.env` must be started with `sudo docker compose up -d`; the odin user can run the others.
New ports need a rule in `/etc/pve/firewall/120.fw` (LAN + tailnet sources only).
CIFS mounts on odin-docker (`/etc/fstab`, creds `/root/viking-secrets/zima-smb.cred`, uid/gid 1000, `_netdev,nofail`): `//192.168.0.176/backups` -> `/mnt/viking-storage`, `//192.168.0.141/models` -> `/mnt/viking-ai/models`.
ZimaOS shares (user `Archangel`): viking-storage `backups`, `proxmox`, `ZimaOS-HD`; viking-ai `models`, `models2`, `ZimaOS-HD`.
Jellyfin is a ZimaOS App Store app (ZimaOS manages its compose). Nothing on `viking-dev` or `viking-dash` runs in Docker yet.

## Backups

- **Since 2026-10-04** job `backup-7360b01c-6b75`: nightly 03:00 snapshot-mode backup of all guests **except VM 130** to **PBS** (`viking-pbs`, deduplicated; retention = PBS prune job 7d/4w/3m, PVE side `keep-all`). VM 130 (the PBS server itself) must never back up to PBS: snapshot mode freezes its filesystem via the guest agent and the upload deadlocks (happened on the first run, aborted). Job `backup-pbs-vm-weekly`: Sunday 02:00, VM 130 -> `zima-backups` (plain vzdump, keep 2).
- Legacy: `zima-backups` = CIFS `//192.168.0.176/proxmox` at `/mnt/pve/zima-backups` (= `/media/backups/proxmox` on viking-storage). The seven vzdump archives per guest from before the switch stay there until the owner says they can go (`/root/jobs.cfg.bak-2026-10-04` has the old job).
- Last run: **2026-10-03 05:00–05:02, finished successfully** (CT 100 13 s, CT 101 57 s, CT 110 12 s, VM 120 82 s). VM 120 archive 2.4 GB, CT 101 2.7 GB, CT 110 0.4 GB.
- Older artefact: `/mnt/pve/zima-backups/pc-stacks/pc-pihole-jellyfin-stacks-2026-10-02.tgz` (archive of the retired PC Pi-hole/Jellyfin stacks).
- Off-site: restic -> Backblaze B2 bucket `viking-backups` (`/root/restic/{env,backup.sh,repo-password}` on viking). **Disabled** (`restic-backup.timer`). Measured 2026-10-04: repo holds 1 snapshot, 10.4 GiB raw in the bucket vs the 10 GiB free cap, so locks/prune/restore fail. Today's "newest archive per guest + /etc/pve" set = 5.5 GB; "critical only" (pihole archive + /etc/pve) = 381 MB. **Owner chose option B on 2026-10-04:** the bucket turned out to be empty already (the 10 GB figure was restic's stale local cache), repo `b2:viking-backups:viking` re-initialised, `backup.sh` now sends only the newest Pi-hole archive + `/etc/pve` + the repo password (381 MB/snapshot, keep 7d/4w/3m), first snapshot `9446f05a` saved, `restic-backup.timer` re-enabled. Old script kept as `backup.sh.bak-2026-10-04`.
- Proxmox e-mail alerts go to Gmail via SMTP target `gmail`.
- **2026-10-03 fix:** the ZimaOS password had been changed after Proxmox first mounted the share; `/etc/pve/priv/storage/zima-backups.pw` was stale and the storage showed `inactive`. Rewritten in the required `password=...` format; storage active again. The same password is also in `/root/viking-secrets/zima-smb.env` on odin-docker.

## Security state

- viking: SSH key-only, CrowdSec + nftables bouncer (fail2ban retired 2026-10-03), datacenter firewall input-DROP with LAN + tailnet allow for 22/8006/ICMP and UDP 41641.
- Guests: per-guest firewall files; **a new published service needs a rule in `/etc/pve/firewall/<id>.fw`**. 120.fw now also allows 3000,3001,5001,8080 and 80,443 from LAN + tailnet (backups `/root/120.fw.bak-*` on viking).
- ZimaBoards: SSH key-only. Docker socket needs sudo (password), so container listing from automation is not possible there.
- Tailscale policy reviewed 2026-10-03: two grants (member->self, member->192.168.0.0/24), single-user tailnet, no tags; kept as is. Rollback copy `docs/tailscale/policy-2026-10-03-before-phase3.hujson`. Key expiry disabled on all six lab nodes via API (key in `/root/viking-secrets/tailscale-api.env` on odin-docker, expires ~2027-01). Devices kept: pixel-7, dedede (owner's).

## Gotchas learned

- Compose env files: never put a value containing `$` in them (argon2 hashes); Compose interpolates even `$$`. Use the app's own config file.
- n8n: activating a workflow is `POST /rest/workflows/<id>/activate` with `{versionId}`; a PATCH with `active: true` is silently ignored. `/healthz` is green before the REST API is ready; during migrations every route returns the SPA HTML with 200. Wait for `/rest/settings` to return JSON. Its session cookie is `Secure` (N8N_PROTOCOL=https), so plain-http API scripts must carry `n8n-auth` by hand.
- Uptime Kuma socket API: register the `monitorList` listener before `login` or you create duplicates.
- Immich app: the server URL must include `http://`; the app assumes https otherwise.
- Proxmox CIFS credential file (`/etc/pve/priv/storage/<id>.pw`) is in `password=...` format, not a raw password.
- ZimaOS: `Archangel` cannot sudo without a password and cannot write to `/media/*` over SSH; use SMB (same password) for storage access.
- Git Bash curl on the PC is a Schannel debug build that reports `000` for working HTTPS; verify with PowerShell `Invoke-WebRequest`.

## Observations from Phase 0 (nothing changed)

1. Timezones: pihole and odin-docker switched to `America/Los_Angeles` on 2026-10-03 (owner OK). viking-storage (ZimaOS) still UTC: no passwordless sudo there; change it in the ZimaOS UI if it matters.
2. `lm-sensors` is not installed on viking, so no temperature readout there yet (Netdata in Phase 4 covers it).
3. Ollama listens on loopback only (kept); `llama3.2:3b` pulled 2026-10-03 for Open WebUI.
4. Backblaze remains over the free cap; timer disabled; nothing lost (nightly local vzdump is healthy).
5. Loose ends from the brief already resolved: CT 9100 is gone, and the old `pihole`/`jellyfin` Tailscale nodes are no longer in the machine list. Remaining tailnet devices: viking, viking-dev, viking-ai, viking-storage, odin-docker, pihole-1, desktop-47v3oim, galaxy-s25-fe, dedede (android, offline 10 h), pixel-7 (android, offline 15 d).
6. `/media/models2` (932 GB) on viking-ai is empty — good candidate for Immich/Paperless data if viking-storage gets tight.

## Pending owner actions


- Vaultwarden: open https://vault.lan, **Create account** with your Gmail (it is pre-invited), then export your Bitwarden vault yourself (Bitwarden web vault > Tools > Export, .json) and import it at vault.lan > Tools > Import. Claude never touches vault data.

- Trust the lab root CA on phones/other devices: open http://ca.lan/viking-lab-root-ca.crt on the device (LAN or Tailscale) and install it as a CA certificate. Android: Settings > Security > Encryption & credentials > Install a certificate > CA certificate.
- Netdata on viking-ai / viking-storage: install from the ZimaOS App Store, or grant `Archangel` NOPASSWD sudo so Claude can run the official container.

## Phase log

- 2026-10-03 Phase 0 inventory; Phase 1 Dockge/Uptime Kuma/Homepage/Watchtower; Phase 2 Open WebUI + llama3.2:3b; Phase 3 Unbound (Pi-hole upstream switched), Caddy + .lan names + internal CA, firewall rules. Stale cleanup: nothing left (CT 9100 and old Tailscale nodes were already gone). Tailscale: policy reviewed and kept, key expiry disabled on servers. Phase 4: Netdata on viking, CrowdSec on viking + odin-docker replacing fail2ban. Wazuh skipped (too heavy), future option. Phase 5: Vaultwarden at vault.lan, owner invited, signups closed. Phase 6: Immich, Paperless, Navidrome, Audiobookshelf, Jellyseerr, Sonarr/Radarr/Prowlarr; CIFS mounts of both ZimaBoards; Proxmox backup credential repaired. Phase 7 (2026-10-04): Gitea on viking-dev with both game repos pushed; n8n on odin-docker with the inbox->Slack sample workflow. Phase 8 (2026-10-04): PBS VM 130, datastore on viking-storage, first full backup, verified restore (CT 9100, deleted after owner OK), nightly job switched to PBS, weekly plain backup of the PBS VM, Backblaze option B.

## TODO

- Move Ollama to viking-ai after the T4 is installed and passthrough/drivers are verified (Phase 2 note).
- Wazuh skipped (too heavy for this hardware); revisit if a bigger box arrives.
- viking RAM: ~11-12 GB available with the VM's 16 GB fully touched by Ollama + containers. Fine for now; shrink VM 120 to 12 GB or enable ballooning if Phase 6 needs room.
