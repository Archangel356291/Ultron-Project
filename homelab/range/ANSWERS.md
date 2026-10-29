# Target Range — private answers / walkthrough

PRIVATE. Lab-only weak credentials. Never deploy this file onto a target, never paste in Slack.
All targets live on the isolated bridge `vmbr9` (10.9.9.0/24, no internet, no home-LAN). Off by default.
Control from viking: `range status|up|down|reset [--start]`.

## Targets

| VMID | Host | IP | Teaches | Dial |
|------|------|----|---------|------|
| 103 | vuln-target | 10.9.9.20 | DVWA web app + Linux privesc | `labctl` (5 rungs) |
| 105 | vuln-shop | 10.9.9.21 | SQLi shop + Linux privesc | — |
| 106 | misa | 10.9.9.30 | Network services + Linux privesc | `labctl-misa` (5 rungs) |

## CT106 "misa" — network services (foothold creds)

- **Anonymous FTP** (21): login `anonymous` / any pass → `notes.txt` reveals `svc-backup / Spring2021!`.
- **SMB guest** (139/445): `//10.9.9.30/public` guest/null session → `creds.txt` = `administrator / P@ssw0rd-Winter23`.
- **Weak SSH user** (22): `bob / password123`.
- **Telnet** (23): classic cleartext service, up at beginner/easy levels.
- **SNMP** (161/udp): community string `public` (`snmpwalk -v2c -c public 10.9.9.30`).
- **Legacy banner** (2121): advertises `ProFTPD 1.3.3c` for `nmap -sV` recon / CVE lookup practice (banner only).

## Linux privesc vectors

CT106 foothold = `bob`; CT103/CT105 foothold = `lowpriv / lowpriv123`.

| Vector | Where | Escalation |
|--------|-------|-----------|
| sudo NOPASSWD (CT106 only) | `bob ALL=NOPASSWD: /usr/bin/find` | `sudo find . -exec /bin/sh \; -quit` (GTFOBins) |
| sudo NOPASSWD (CT103/105: skipped, no sudo installed) | `lowpriv …: /usr/bin/awk` if sudo present | `sudo awk 'BEGIN{system("/bin/sh")}'` |
| SUID binary | `/usr/local/bin/cp-suid` (106) / `find-suid` (103/105), mode 4755 | SUID `find`: `find-suid . -exec /bin/sh -p \; -quit` |
| root cron + world-writable script | `/opt/range/backup.sh` (106) / `maint.sh` (103/105), mode 777, run by root each minute | overwrite the script → root shell/reverse shell on next tick |
| readable creds | `/opt/range/app.conf` / `db.conf`; `~/.bash_history` | harvested DB creds + jump-host hints |
| PATH hijack | root cron runs `/opt/range/sysmon.sh|rotate.sh` with writable `/usr/local/sbin` on PATH | drop a malicious `backup`/`logrotate-helper` in `/usr/local/sbin` → root on next tick |

## Difficulty dials

`labctl <beginner|easy|intermediate|advanced|expert>` (CT103) and `labctl-misa …` (CT106) move offense difficulty + defense posture together:
beginner (no firewall/f2b, everything exposed) → expert (firewall + fail2ban on, key-only SSH, noisy services off).

## Reset

`range reset` rolls all three back to their `vulnbaseline` snapshot (leaves them stopped). `range reset --start` resets then boots.
Ryuk can drive it read/limited via its lab-ops key: `range status|up|down|reset [--start]` (nothing else).
