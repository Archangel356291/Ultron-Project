#!/bin/bash
# Range network guard (installed on viking at /usr/local/bin/range-netguard.sh, run by
# range-netguard.service at boot). Makes the Tailscale<->lab return path work while keeping
# the intentionally-vulnerable targets unable to pivot off the isolated bridge.
#
# Why this exists: vmbr9 (the isolated lab bridge) ships with per-interface forwarding OFF,
# so the kernel forwarded attacker->target packets (in on tailscale0, fwd=1) but silently
# dropped the target->attacker replies (in on vmbr9, fwd=0). Enabling vmbr9 forwarding fixes
# the return path; the FORWARD guard below ensures vmbr9 can ONLY forward to tailscale0, so a
# compromised target still cannot reach the home LAN / internet even if it adds its own gateway.
sysctl -w net.ipv4.conf.vmbr9.forwarding=1 >/dev/null 2>&1
sysctl -w net.ipv4.conf.all.rp_filter=2 >/dev/null 2>&1
iptables -C FORWARD -i vmbr9 ! -o tailscale0 -j DROP 2>/dev/null || iptables -I FORWARD 1 -i vmbr9 ! -o tailscale0 -j DROP
