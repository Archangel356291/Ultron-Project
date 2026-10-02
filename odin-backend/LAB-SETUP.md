# Home-lab hosts setup — M920q + ZimaBoard 2, phase 1

Supersedes `PI-SETUP.md` (the Pi 5 was dropped 2026-09-28). Same scope,
same stop line: get each box on the tailnet, key-only SSH reachable from
this PC, running Docker. **No `app.py`/dashboard/bot changes here** —
that's phase 2, built against the real boxes once this works.

> **Status 2026-09-28 — paused.** USB stick is flashed (Etcher) and the
> M920q boots the Proxmox installer, but it only has a Wi-Fi dongle and
> the installer needs wired Ethernet. Resume at section 2 once a cable
> (or powerline adapter) reaches the M920q's built-in RJ45 port.

Hardware as of 2026-09-28:

| Box | Specs | Ships with | Target OS |
|-----|-------|-----------|-----------|
| Lenovo ThinkCentre M920q | 32 GB RAM, 1 TB SSD, no GPU | Windows 11 | Proxmox VE 9.2 (wipe Windows) |
| ZimaBoard 2 (x1+) | — | ZimaOS (Linux) | keep ZimaOS |

Why Proxmox and not plain Debian: the M920q has to run VMs, Docker
containers, and a local AI runtime. Proxmox is Debian underneath with a
web UI for VMs/LXC; Docker and the AI go in one Debian VM on top.
Everything below the VM line (Tailscale, SSH key) is the same as the Pi
doc. ZimaOS already has Docker and a Tailscale app, so no reinstall.

AI note: no GPU means CPU-only inference. 32 GB RAM comfortably runs
7B–14B quantized models via Ollama; anything bigger needs a GPU box.

## 0. SSH key (already generated for the Pi, reuse it)

```
C:\Users\<you>\.ssh\odin_pi_ed25519      (private — stays on this PC)
C:\Users\<you>\.ssh\odin_pi_ed25519.pub  (public — goes on every lab box)
```

One key for "this PC → lab hosts" is fine; revoke it on all of them at
once if it ever leaks.

## 1. Write the USB stick (on this PC — already set up)

balenaEtcher and Rufus are both installed (`winget`), and the ISO is in
Downloads with its SHA256 verified against
`enterprise.proxmox.com/iso/SHA256SUMS`:

```
C:\Users\kyean\Downloads\proxmox-ve_9.2-1.iso
```

Use **balenaEtcher first** — it's the tool Proxmox's own wiki recommends
on Windows, and Rufus has an open bug (pbatard/rufus#2854) where Proxmox
9.x sticks sometimes don't boot even in DD mode.

1. Plug in a USB stick (4 GB+, gets erased).
2. Open **balenaEtcher** → Flash from file: the ISO → Select target: the
   stick → Flash. Ignore Windows' "you need to format this disk" popups
   afterwards — that's Windows not understanding the Linux partitions.
3. Fallback only if Etcher fails: Rufus → SELECT the ISO → START → pick
   **Write in DD Image mode** at the ISOHybrid prompt (that prompt is
   normal, not an error).

## 2. M920q: install Proxmox VE

1. First go into BIOS (`F1` at the Lenovo logo) and set, then save:
   - Security → Secure Boot → **Disabled** (Proxmox isn't Microsoft-signed;
     this is the #1 cause of "no bootable device").
   - Startup → Fast Boot **off**; CSM **off** / boot mode **UEFI only**.
   - Advanced → CPU Setup → **Intel Virtualization Technology** and
     **VT-d** both **Enabled** (needed for VMs).
   Then reboot, `F12` at the logo, pick the USB stick.
2. Installer: **Install Proxmox VE (Graphical)**.
   - Target disk: the 1 TB SSD, filesystem **ext4** (default). This
     wipes Windows.
   - Country/timezone/keyboard.
   - Root password + your email.
   - Network: hostname `odin-m920q.lan`, plug into Ethernet, accept the
     DHCP-suggested IP or set a static one. Write the IP down.
3. Reboot, pull the stick. Web UI is at `https://<ip>:8006` (accept the
   self-signed cert), login `root`, realm PAM.

## 3. M920q host: key, Tailscale, no-subscription repo

From this PC, drop the key onto the Proxmox host (root, password once):

```powershell
type C:\Users\<you>\.ssh\odin_pi_ed25519.pub | ssh root@<ip> "mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys && chmod 700 ~/.ssh && chmod 600 ~/.ssh/authorized_keys"
ssh -i C:\Users\<you>\.ssh\odin_pi_ed25519 root@<ip>
```

Then on the host:

```bash
# switch to the free repo so apt update stops erroring
sed -i 's/^Enabled:.*/Enabled: false/' /etc/apt/sources.list.d/pve-enterprise.sources /etc/apt/sources.list.d/ceph.sources
cat > /etc/apt/sources.list.d/pve-no-subscription.sources <<'X'
Types: deb
URIs: http://download.proxmox.com/debian/pve
Suites: trixie
Components: pve-no-subscription
Signed-By: /usr/share/keyrings/proxmox-archive-keyring.gpg
X
apt update && apt full-upgrade -y
# key-only SSH
sed -i 's/^#\?PasswordAuthentication.*/PasswordAuthentication no/' /etc/ssh/sshd_config
systemctl restart ssh
# tailnet — same account as PC/phones
curl -fsSL https://tailscale.com/install.sh | sh
tailscale up
```

Now `https://odin-m920q:8006` works from anywhere on the tailnet.

## 3b. The Docker + AI VM

In the web UI: upload a Debian 12 netinst ISO (local → ISO Images), then
Create VM → 8 cores, 16 GB RAM, 200 GB disk, VirtIO disk and network.
Install Debian headless with SSH server only, hostname `odin-docker`,
then inside it:

```bash
curl -fsSL https://tailscale.com/install.sh | sh && sudo tailscale up
curl -fsSL https://get.docker.com | sh && sudo usermod -aG docker $USER
curl -fsSL https://ollama.com/install.sh | sh   # AI runtime, CPU-only
```

Drop the same SSH key as section 3. The other 16 GB / cores stay free
for further VMs.

## 4. ZimaBoard 2: join the tailnet, add the key

1. Open the ZimaOS web UI (`http://<zima-ip>` — the box shows its IP on
   the display, or check the router).
2. App Store → install **Tailscale** → open it, sign into the same
   account. Give each board a distinct hostname (`odin-zima-1`, `-2`).
3. Settings → enable SSH. Then from this PC, same key-drop as section 2
   but against `<zima-user>@<zima-ip>`, then disable password login the
   same way (ZimaOS is Debian-based; `sshd_config` lives in the same
   place). Docker is already installed — `docker ps` should just work.

## 5. Verify from the PC — the whole point

```powershell
tailscale status
ssh -i C:\Users\<you>\.ssh\odin_pi_ed25519 root@odin-m920q pveversion
ssh -i C:\Users\<you>\.ssh\odin_pi_ed25519 <username>@odin-docker docker ps
ssh -i C:\Users\<you>\.ssh\odin_pi_ed25519 <zima-user>@odin-zima-1 docker ps
```

All four succeed over Tailscale (bare MagicDNS names, no `.local`) →
phase 1 done. Then flip the matching `KNOWN_DEVICES` entries in `app.py`
to `connected` — and only then. Nothing else in code should change until
that's true.

## Where this leaves things

Two (or more) real Linux hosts Odin can eventually target. Phase 2 —
extending the preview-then-confirm action pattern (`/api/actions/backup`,
`/api/actions/deploy-container`) to a remote host, with Discord-button
or Slack exact-match approval — is unchanged from the plan at the bottom
of `PI-SETUP.md`.
