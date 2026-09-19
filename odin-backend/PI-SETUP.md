# Raspberry Pi setup — getting it reachable, phase 1

This is step one of "let Odin reach into the home lab on the Pi": get
the Pi itself flashed, on the same Tailscale tailnet as the Cyberpower
PC, SSH-reachable with a key (no password guessing), and running Docker.
**This document stops there.** Nothing in `app.py`, the dashboard, or
either bot talks to the Pi yet — that's phase 2, and it gets built and
verified against the real device once it exists, not guessed at now.
Same reasoning as `REMOTE-ACCESS.md`: this is a hardware/third-party-tool
setup guide, not code with a test suite behind it — sanity-check each
step against what you actually see, don't assume it's exactly right.

## Why this order

The Pi currently doesn't exist on the network at all — no IP, no SSH, no
way for this PC (or Odin) to reach it. Everything below fixes exactly
that, in the order that makes each later step possible:

1. Flash the SD card with SSH and your Tailscale-account SSH key already
   configured, so first boot is immediately reachable — no monitor,
   keyboard, or "what's its IP" guessing needed.
2. Join the same tailnet the PC and your phones are already on
   (`REMOTE-ACCESS.md`), so the Pi is reachable from anywhere, not just
   this LAN.
3. Install Docker, so there's something for a future deploy action to
   actually target.

## 0. What's already been generated for this

A dedicated SSH keypair, used for nothing except this PC talking to this
Pi — not your personal SSH key, not shared with anything else, so it can
be revoked independently later if needed:

```
C:\Users\<you>\.ssh\odin_pi_ed25519       (private key — stays on this PC)
C:\Users\<you>\.ssh\odin_pi_ed25519.pub   (public key — goes on the Pi)
```

Public key (paste this into the Imager in step 2 — copy it exactly, one
line, no wrapping; yours will look like this, a different random string
after `ssh-ed25519`):

```
ssh-ed25519 AAAA...<your generated key>... odin-pc-to-pi
```

Raspberry Pi Imager is already installed on this PC (`v2.0.11.1`, via
winget) — no separate download needed.

## 1. Flash the SD card

1. Insert the SD card (8GB+, a real one you're OK wiping — this erases
   it completely).
2. Open **Raspberry Pi Imager**.
3. **Device**: pick your actual Pi model (e.g. Raspberry Pi 4, Pi 5).
4. **Operating System**: Raspberry Pi OS (64-bit) is the right default
   unless you have a specific reason for something else — Docker and
   Tailscale both fully support it.
5. **Storage**: select the SD card. Double-check this is the SD card and
   not another drive — the next step erases whatever you pick.
6. Click the **gear icon** (or `Ctrl+Shift+X`) for **Advanced options**
   before writing — this is the step that makes the Pi reachable on
   first boot instead of needing a monitor/keyboard:
   - **Set hostname**: `odin-pi` (or any name that matches whatever
     naming pattern your other devices already use on the tailnet).
   - **Enable SSH** → **Allow public-key authentication only** (not
     password) → paste the public key from section 0 above.
   - **Set username and password**: pick a username (e.g. your own
     name, or `odin`). A password is still asked for even with
     key-only SSH enabled — Imager requires one; it just won't be
     usable for SSH login since public-key-only is selected above.
   - **Configure wireless LAN**: fill in your Wi-Fi SSID/password and
     country code if the Pi isn't going to be wired via Ethernet. Skip
     this entirely if it'll be plugged into Ethernet.
   - **Set locale settings**: timezone and keyboard layout, for
     correctness (log timestamps, etc.) — not critical but easy to get
     right now.
7. Save, then **Write**. Takes a few minutes; it verifies after writing.

## 2. First boot and SSH in

1. Insert the SD card into the Pi, connect Ethernet (or let it join the
   Wi-Fi you configured), and power it on. Give it a minute or two for
   first boot.
2. From this PC (PowerShell or the terminal here):
   ```powershell
   ssh -i C:\Users\<you>\.ssh\odin_pi_ed25519 <username>@odin-pi.local
   ```
   Replace `<username>` with whatever you set in step 1. Raspberry Pi OS
   ships with mDNS (Avahi) enabled by default, so `<hostname>.local`
   resolves on the same LAN without needing to find the IP manually.
3. First connection asks to confirm the host key fingerprint — type
   `yes`. If `.local` doesn't resolve (some routers/networks block
   mDNS), find the IP instead: check your router's connected-devices
   page, or run `arp -a` on this PC and look for the Pi's MAC vendor
   prefix, then `ssh -i ... <username>@<that-ip>`.

If this step fails, nothing past it will work — get this working before
moving on. Common causes: wrong hostname/IP, Wi-Fi didn't take (check
the SSID/password typed into Imager), or the Pi is still booting.

## 3. Update the OS

```bash
sudo apt update && sudo apt full-upgrade -y
sudo reboot
```

Reconnect with the same `ssh` command after it reboots.

## 4. Install Tailscale, join the same tailnet

```bash
curl -fsSL https://tailscale.com/install.sh | sh
sudo tailscale up
```

The second command prints a URL — open it in a browser (on any device)
and **sign into the same account already used for this PC and the
phones**, not a new one. Signing into a different account puts the Pi on
a *different* tailnet, invisible to everything else.

Confirm it worked — from this PC:

```powershell
tailscale status
```

You should now see the Pi (`odin-pi`) alongside your other devices.
Then confirm the SSH key still works **over Tailscale specifically**
(not just the LAN — this is the whole point, reachability from
anywhere):

```powershell
ssh -i C:\Users\<you>\.ssh\odin_pi_ed25519 <username>@odin-pi
```

(MagicDNS resolves the bare Tailscale hostname once both devices are on
the tailnet — no `.local` suffix needed here.)

**Firewall note, same reasoning as `REMOTE-ACCESS.md`:** the default
tailnet policy (`autogroup:member` → `autogroup:self`) already covers
this — it's "your own devices can reach each other," and the Pi joining
your account makes it one of "your own devices." Nothing to change here
unless you later tag the Pi or want to scope it more narrowly.

## 5. Install Docker

```bash
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker $USER
```

Log out and back in (or `newgrp docker`) for the group change to take
effect without needing `sudo` on every `docker` command. Verify:

```bash
docker run hello-world
```

## Where this leaves things

At the end of this: the Pi is flashed, key-only SSH reachable both on
the LAN and over Tailscale from anywhere, fully updated, and running
Docker — a real second host Odin can eventually target, not a
hypothetical one.

**Not done here, and deliberately not guessed at:** any code change to
`app.py`, the dashboard, or the bots. The plan discussed for that next
phase — extending the existing preview-then-confirm action pattern
(the same one `/api/actions/backup` and `/api/actions/deploy-container`
already use) to a Pi as the target, with approval requested through the
Discord bot's existing Confirm/Cancel button flow and/or a new Slack
approval channel using an exact-match confirmation tied to one specific
pending action (never a free-text "yes" the model could be tricked into
reading as approval) — gets built once this Pi actually exists and can
be tested against for real, the same bar every other feature in this
project has held to.
