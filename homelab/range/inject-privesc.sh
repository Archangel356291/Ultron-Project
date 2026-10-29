#!/usr/bin/env bash
# inject-privesc.sh <CTID> — add a Linux privilege-escalation practice suite to an existing LXC target.
# Pure file/sudo/cron config, no internet needed. Re-snapshots vulnbaseline afterward.
# AUTHORIZED LAB TARGETS ONLY.
set -euo pipefail
ID="${1:?usage: inject-privesc.sh <CTID>}"
pct status "$ID" >/dev/null || { echo "CT $ID not found"; exit 1; }
pct start "$ID" 2>/dev/null || true; sleep 3

echo "[*] CT$ID: low-priv foothold user (lowpriv/lowpriv123) + weak ssh password..."
pct exec "$ID" -- bash -c '
id lowpriv >/dev/null 2>&1 || useradd -m -s /bin/bash lowpriv
echo "lowpriv:lowpriv123" | chpasswd
# only add a drop-in if labctl is NOT managing ssh here (avoid clobbering CT103 dial)
if [ ! -x /usr/local/bin/labctl ]; then
  printf "PasswordAuthentication yes\n" > /etc/ssh/sshd_config.d/zz-privesc.conf
  systemctl reload ssh 2>/dev/null || systemctl restart ssh 2>/dev/null || systemctl restart sshd 2>/dev/null || true
fi'

echo "[*] CT$ID: (a) sudo misconfig — NOPASSWD GTFOBins binary (awk)..."
pct exec "$ID" -- bash -c 'if command -v sudo >/dev/null 2>&1; then mkdir -p /etc/sudoers.d; echo "lowpriv ALL=(ALL) NOPASSWD: /usr/bin/awk" > /etc/sudoers.d/lowpriv; chmod 440 /etc/sudoers.d/lowpriv; echo "   sudo vector added"; else echo "   SKIP: sudo not installed on this CT"; fi'

echo "[*] CT$ID: (b) SUID binary that should not be (find)..."
pct exec "$ID" -- bash -c 'cp "$(command -v find)" /usr/local/bin/find-suid 2>/dev/null && chmod 4755 /usr/local/bin/find-suid'

echo "[*] CT$ID: (c) root cron running a world-writable script..."
pct exec "$ID" -- bash -c 'mkdir -p /opt/range; printf "#!/bin/bash\ndate >> /var/log/range-cron.log\n" > /opt/range/maint.sh; chmod 777 /opt/range/maint.sh; echo "* * * * * root /opt/range/maint.sh" > /etc/cron.d/range-maint; chmod 644 /etc/cron.d/range-maint'

echo "[*] CT$ID: (d) readable credentials in config + history..."
pct exec "$ID" -- bash -c 'mkdir -p /opt/range; printf "DB_USER=admin\nDB_PASS=Autumn2022!\n" > /opt/range/db.conf; chmod 644 /opt/range/db.conf; printf "mysql -uadmin -pAutumn2022! -h 10.9.9.20\nssh root@10.9.9.1 # jump host\n" >> /home/lowpriv/.bash_history; chmod 644 /home/lowpriv/.bash_history'

echo "[*] CT$ID: (e) writable PATH dir used by a root cron (PATH hijack)..."
pct exec "$ID" -- bash -c 'mkdir -p /usr/local/sbin; chmod 777 /usr/local/sbin; printf "#!/bin/bash\ncd /opt/range && logrotate-helper >/dev/null 2>&1 || true\n" > /opt/range/rotate.sh; chmod 755 /opt/range/rotate.sh; echo "*/3 * * * * root PATH=/usr/local/sbin:/usr/bin:/bin /opt/range/rotate.sh" > /etc/cron.d/range-rotate; chmod 644 /etc/cron.d/range-rotate'

echo "[*] CT$ID: re-snapshot vulnbaseline (now includes privesc)..."
pct delsnapshot "$ID" vulnbaseline 2>/dev/null || true
pct snapshot "$ID" vulnbaseline -description "vulnerable baseline + linux privesc suite" 2>&1 | tail -1 || true
echo "[*] CT$ID privesc injection complete."
