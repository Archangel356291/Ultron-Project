# Field Kit Guide

Your complete mobile security kit — what each item is, what it's for, and how to use it.
Plain-English reference. Goal: a full, capable kit ready for DEF CON 35 (Aug 2027).

---

## The one rule (read first, every time)

**Only test what you own or have written permission for.** For client work that means a **signed SAAP authorization packet** naming the exact scope (IPs/domains/hours) in hand *before* you touch anything. Your own lab, TryHackMe, and HTB are always fair game. Everything else without paperwork is a crime, not a test.

Tools below marked **[LAB-ONLY]** (WiFi deauth, rogue APs, USB payloads, RF jamming-capable gear) are legal **only** against your own lab or a client range explicitly in scope. Using them on anyone else's network/devices is illegal regardless of intent.

---

## Kit at a glance

| Item | One-line role |
|------|---------------|
| Dell Latitude 5400 (Kali) | Main hub — scanning, exploitation, notes, reports, storage |
| Pixel 7 (GrapheneOS) + KaliDroid | Pocket Linux terminal + secure comms |
| Main phone | Everyday phone — kept *out* of security work |
| M5 Shark (ESP32 Marauder) | WiFi/Bluetooth auditing **[LAB-ONLY]** |
| Chameleon Ultra | RFID/NFC read, clone, emulate |
| Heltec V3 LoRa ×2 | Off-grid encrypted mesh messaging (Meshtastic) |
| Bootable Kali USB | Run Kali on any PC with no install |
| GL.iNet travel router *(planned)* | Private, trusted field network for your kit |
| Alfa AWUS036ACM *(ordered)* | External WiFi adapter — monitor mode + injection **[LAB-ONLY]** |
| ESP32-DIV V2.0 *(inbound)* | Multiband sub-GHz/RF learning tool |
| WiFi Pineapple Pager *(ordering)* | Rogue-AP / WiFi audit platform **[LAB-ONLY]** |
| Bash Bunny Mk II *(ordering)* | USB attack/payload device **[LAB-ONLY]** |
| Faraday bag + USB data blockers *(ordering)* | RF isolation + charge-only safety |
| A16 cyberdeck (stays home) | Backup rig / SIM reader, reachable over Tailscale |

---

## Core devices

### Dell Latitude 5400 — the hub
**What:** Your main Kali laptop (tailnet name `gelus`). **For:** everything heavy — full scans, exploitation, Burp Suite, report writing, and permanent storage of engagement data. Also your reverse-shell catcher on-site.
**How to use:**
- All field data lands here (not the phones). One folder per job: `~/engagements/<client>/<date>/`.
- Reach your lab/range over Tailscale: `ssh root@192.168.0.50 range up`, then scan `10.9.9.x` normally (`nmap -sV -sC`, ping all work — it routes natively).
- Catch reverse shells here when you're on the client's network: `nc -lvnp 4444`, point the payload at the laptop's LAN IP.
**Tip:** this is the trusted brain of the kit — keep it encrypted, keep it backed up to the home lab.

### Pixel 7 (GrapheneOS) + KaliDroid — pocket terminal
**What:** Hardened phone doing double duty: secure comms **and** a real Kali VM in your pocket (KaliDroid = QEMU VM, not a toy chroot). **For:** quick recon, grabbing a shell, or working a box when the laptop's in the bag.
**How to use:**
- Launch KaliDroid → auto-logs into Kali as root. Tools already installed (nmap, metasploit, sqlmap, hydra, netexec…).
- **Scanning quirk that matters:** the VM is behind QEMU NAT, so `ping` and SYN/UDP scans **don't work**. Always `nmap -sT -Pn`; test reachability with `nc -vz <ip> <port>`. (On the laptop, normal scans work — this limit is phone-only.)
- Reaches your practice range (tagged `tag:attacker`). Reverse shells *to* the phone won't work (carrier NAT) — catch them on the laptop or CT102 instead.
- Phone Downloads shows up inside Kali at `/mnt/downloads` for moving files.
**Tip:** full command-by-command guide was emailed to you ("Field Guide v2") and lives in the repo at `homelab/range/FIELD-GUIDE-pixel7.md`.

### Main phone — stays clean
**What:** Your everyday T-Mobile phone. **For:** normal life. **Rule:** keep it *out* of security work entirely — it's the one device that ties to your real identity and daily accounts.

---

## Wireless & RF tools

### M5 Shark (ESP32 Marauder) — WiFi/Bluetooth auditing **[LAB-ONLY]**
**What:** A pocket ESP32 running Marauder firmware with a touchscreen. **For:** seeing the WiFi/BLE world around you — list access points and clients, sniff beacons/probes, capture handshakes, detect BLE devices.
**How to use:** power on → touch menu. Common flows: *Scan APs* → pick a target (your lab AP) → *Sniff* or *Capture handshake*; *Packet Monitor* to watch traffic volume.
**Legal:** passive scanning/listening is generally fine; **deauth, beacon spam, and handshake-forcing are LAB-ONLY** — never against networks you don't own.

### Chameleon Ultra — RFID/NFC
**What:** A credit-card-sized RFID/NFC tool (125 kHz + 13.56 MHz) that reads, stores, clones, and *emulates* cards. Pairs to the phone app over Bluetooth. **For:** learning access-control security — clone your own badge, test readers you're authorized on.
**How to use:** open the phone app → read a card into a slot → emulate that slot to present it to a reader. Holds multiple card profiles.
**Legal:** only your own cards or cards in an authorized engagement scope.

### Heltec V3 LoRa nodes ×2 — off-grid comms (Meshtastic)
**What:** Two long-range LoRa radios running Meshtastic. **For:** encrypted text messaging with **no cell, no WiFi, no internet** — useful off-grid or when you want comms that don't touch carrier networks. Range is km-scale line-of-sight.
**How to use:** pair a node to the phone's Meshtastic app over Bluetooth → join/create an encrypted channel → text. The second node (or any Meshtastic node in range) receives it. Nodes also relay for each other (mesh).
**Tip:** set a private channel key; power from a kit power bank for all-day use.

### ESP32-DIV V2.0 *(inbound)* — multiband RF learning
**What:** A multiband wireless/sub-GHz learning board. **For:** exploring the RF spectrum beyond WiFi (sub-GHz signals, scanning). Learning tool — use against your own devices/lab.

---

## Access & payload tools

### Bootable Kali USB (16 GB) — Kali anywhere
**What:** A full Kali Linux you boot from USB on almost any PC, no install, no trace on the host disk. **For:** turning a borrowed/spare machine into a working attack box, or recovery.
**How to use:** insert → boot the PC from USB (F12/boot menu) → run Kali live. Pair with the two repair-tool USBs for fixing/wiping machines.

### Alfa AWUS036ACM *(ordered ~Nov 2)* — proper WiFi adapter **[LAB-ONLY]**
**What:** An external USB WiFi adapter that supports **monitor mode and packet injection** (the built-in laptop/phone WiFi usually can't). **For:** real WiFi testing — capturing WPA handshakes, injection attacks.
**How to use:** plug into the Latitude (or KaliDroid via USB passthrough) → `airmon-ng start wlan0` → `airodump-ng` to capture → crack offline. **Lab/authorized networks only.**

### WiFi Pineapple Pager *(ordering)* — rogue-AP platform **[LAB-ONLY]**
**What:** A dedicated WiFi auditing device that can stand up rogue/evil-twin APs and run automated WiFi attacks from a clean web UI. **For:** testing how clients and networks handle hostile WiFi. **Lab/authorized only** — rogue APs capture real traffic.

### Bash Bunny Mk II *(ordering)* — USB attack tool **[LAB-ONLY]**
**What:** A USB device that pretends to be a keyboard/network adapter/storage to run payloads the instant it's plugged in (keystroke injection, credential capture, exfil). **For:** physical-access testing. **Only on machines in an authorized scope** — this is a break-in tool by design.

---

## Infrastructure & opsec gear

### GL.iNet travel router *(planned ~Nov 6)* — your own field network
**What:** A pocket router. **For:** giving your kit devices one private, trusted WiFi network (with VPN/Tailscale baked in) instead of trusting hotel/client WiFi. Everything connects to the GL.iNet; the GL.iNet handles the uplink and the tunnel home.
**Tip:** this becomes the backbone that ties the whole kit together in the field.

### Faraday bag + USB data blockers *(ordering)*
- **OffGrid faraday bag:** blocks all RF to a device inside (no WiFi/cell/BT/GPS) — kills tracking and remote wipe; use it to transport a seized or sensitive device.
- **USB data blockers ("USB condoms"):** pass power but **not data** — plug these between your cable and any untrusted charger/port so a malicious port can't talk to your device (juice-jacking defense).

### A16 cyberdeck — home backup
**What:** Samsung A16 handheld rig (stays home). **For:** grab it only when you need its SIM reader or a smaller second rig. Reachable from the field over Tailscale.

---

## Using the practice range (skills home base)
Your isolated, resettable vuln lab lives on the home server, reachable from phone + laptop over Tailscale:
```
ssh root@192.168.0.50 range up        # start targets (10.9.9.20 DVWA, .21 shop, .30 misa)
ssh root@192.168.0.50 range reset     # wipe back to clean vulnerable state
ssh root@192.168.0.50 range down      # stop, free server RAM
```
Full walkthrough with creds + privesc paths: `homelab/range/FIELD-GUIDE-pixel7.md` and `ANSWERS.md`. Safe to hammer — reset anytime.

---

## Client engagement — the loop
1. **Authorize:** signed SAAP packet in hand, scope confirmed in writing. No signature, no testing.
2. **Set up:** connect kit to the GL.iNet (or trusted network); start an `~/engagements/<client>/<date>/` folder on the Latitude.
3. **Find scope:** on their network `ip a` + `ip route` (your /24, gateway = router); external, `whois <ip>` for their CIDR. Only touch what's authorized.
4. **Recon → enumerate:** `nmap -sV -sC -oA scan <range>` (laptop) or `nmap -sT -Pn` (KaliDroid). Go slow on production (`-T2`).
5. **Validate → (if authorized) exploit:** confirm each finding; catch shells on the laptop (not the phone).
6. **Document as you go:** screenshot every finding with the command that produced it.
7. **Wrap up:** remove anything you dropped on their systems; write the report (summary + findings: severity, evidence, reproduction, fix); pull data to the Latitude; wipe client data off the phones.

---

## Opsec — habits that keep you safe & legal
- **Data flows to the Latitude**, never parked on the phones. Wipe client data after each job.
- **Don't post screenshots showing your external IP.**
- **Charge through a data blocker** on any untrusted port.
- **Faraday bag** anything you need to go truly dark.
- **Authorization paperwork rides in the bag** — if you can't produce it, you shouldn't be testing.

---

## One-line quick reference
| Need | Grab / command |
|------|----------------|
| Heavy scan, exploit, report | Latitude (hub) |
| Quick pocket recon | Pixel 7 / KaliDroid — `nmap -sT -Pn`, `nc -vz` |
| See nearby WiFi/BLE | M5 Shark (passive = anywhere; attacks = lab only) |
| Clone/test a badge | Chameleon Ultra (own cards only) |
| Comms with no cell/wifi | Heltec LoRa + Meshtastic app |
| Attack box on a borrowed PC | Bootable Kali USB |
| Real WiFi capture/injection | Alfa adapter (lab only) |
| Trusted field network | GL.iNet router |
| Charge on a sketchy port | USB data blocker |
| Start / reset the lab | `ssh root@192.168.0.50 range up` / `range reset` |
