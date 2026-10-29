#!/usr/bin/env bash
# Build CT106 "misa" (10.9.9.30) — all-in-one Linux practice target on the isolated lab bridge vmbr9.
# Network services + Linux privesc suite + labctl-misa difficulty dial.
# Temp LAN NIC (vmbr0) is attached ONLY for apt, then removed. AUTHORIZED LAB TARGET ONLY.
set -euo pipefail
ID=106
IP=10.9.9.30
TMPL=local:vztmpl/debian-13-standard_13.6-1_amd64.tar.zst
REMPUB='ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAILFvnsnfJN04cUAP9FIC+X5VUHU0winjNTlfjkOWaCIV ryuk-remediate->practice-targets'

echo "[*] 1. create CT $ID (skip if exists)..."
if ! pct status $ID >/dev/null 2>&1; then
  pct create $ID "$TMPL" --hostname misa --cores 1 --memory 1024 --swap 512 \
    --rootfs local-lvm:12 --net0 name=eth0,bridge=vmbr9,ip=${IP}/24,type=veth \
    --ostype debian --unprivileged 1 --features nesting=1 --onboot 0 \
    --description "practice target: network services + linux privesc (range)" \
    --password "TempRoot-$(openssl rand -hex 4)"
fi

echo "[*] 2. attach TEMP LAN NIC (vmbr0, DHCP) for provisioning only..."
pct set $ID --net1 name=eth1,bridge=vmbr0,ip=dhcp,type=veth
pct start $ID 2>/dev/null || true
sleep 8
# bring eth1 up / get a lease
pct exec $ID -- bash -c 'dhclient eth1 2>/dev/null || true; sleep 3'
echo "    lan ip: $(pct exec $ID -- bash -c 'ip -4 -br addr show eth1 2>/dev/null')"

echo "[*] 3. apt install the weak service set..."
pct exec $ID -- bash -c 'export DEBIAN_FRONTEND=noninteractive; apt-get update -qq && \
  apt-get install -y -qq vsftpd samba snmpd snmp telnetd openssh-server cron sudo python3 >/dev/null 2>&1' \
  || { echo "APT FAILED"; exit 1; }

echo "[*] 4. push config payloads..."
pct exec $ID -- mkdir -p /opt/range /srv/ftp /srv/smbshare
# --- deploy service configs via pushed files (done below over pct exec here-docs) ---

########################### WEAK NETWORK SERVICES ###########################
echo "[*] 5a. anonymous FTP with a readable finding..."
pct exec $ID -- bash -c 'cat > /etc/vsftpd.conf' <<"EOF"
listen=YES
listen_ipv6=NO
anonymous_enable=YES
anon_root=/srv/ftp
no_anon_password=YES
dirmessage_enable=YES
ftpd_banner=Welcome to misa FTP (vsftpd 3.0)
EOF
pct exec $ID -- bash -c 'echo "Internal only. Do not share. backup svc creds: svc-backup / Spring2021!" > /srv/ftp/notes.txt; chmod 644 /srv/ftp/notes.txt; chown -R ftp:ftp /srv/ftp 2>/dev/null || true'

echo "[*] 5b. SMB guest share with a creds.txt finding..."
pct exec $ID -- bash -c 'cat >> /etc/samba/smb.conf' <<"EOF"

[public]
   path = /srv/smbshare
   browseable = yes
   read only = yes
   guest ok = yes
   guest only = yes
EOF
pct exec $ID -- bash -c 'sed -i "s/^\(\s*\)\(workgroup\s*=\).*/\1\2 WORKGROUP/" /etc/samba/smb.conf; grep -q "map to guest" /etc/samba/smb.conf || sed -i "/\[global\]/a \   map to guest = Bad User\n   server string = misa fileserver" /etc/samba/smb.conf'
pct exec $ID -- bash -c 'printf "domain admin backup\nuser: administrator\npass: P@ssw0rd-Winter23\n" > /srv/smbshare/creds.txt; chmod 644 /srv/smbshare/creds.txt'

echo "[*] 5c. weak SSH user (brute-force practice)..."
pct exec $ID -- bash -c 'id bob >/dev/null 2>&1 || useradd -m -s /bin/bash bob; echo "bob:password123" | chpasswd; \
  sed -i "s/^#\?PasswordAuthentication.*/PasswordAuthentication yes/" /etc/ssh/sshd_config; \
  printf "PasswordAuthentication yes\nPermitRootLogin no\n" > /etc/ssh/sshd_config.d/zz-lab.conf'

echo "[*] 5d. telnet (inetd-style via telnetd)..."
pct exec $ID -- bash -c 'systemctl enable --now inetutils-telnetd 2>/dev/null || systemctl enable --now telnetd 2>/dev/null || true'

echo "[*] 5e. SNMP with public community..."
pct exec $ID -- bash -c 'cat > /etc/snmp/snmpd.conf' <<"EOF"
agentAddress udp:0.0.0.0:161
rocommunity public
sysLocation misa-lab
sysContact admin@deathnote.lab
EOF

echo "[*] 5f. deliberately-outdated service banner (nmap -sV recon practice)..."
pct exec $ID -- bash -c 'cat > /opt/range/oldbanner.py' <<"EOF"
#!/usr/bin/env python3
# Minimal banner service advertising a known-old version string, for `nmap -sV` fingerprint practice.
import socket
HOST, PORT = "0.0.0.0", 2121
BANNER = b"220 ProFTPD 1.3.3c Server (misa legacy) [::ffff:10.9.9.30]\r\n"
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST, PORT)); s.listen(5)
while True:
    c, _ = s.accept()
    try: c.sendall(BANNER)
    except OSError: pass
    finally: c.close()
EOF
pct exec $ID -- bash -c 'cat > /etc/systemd/system/oldbanner.service' <<"EOF"
[Unit]
Description=range legacy banner (recon practice)
After=network.target
[Service]
ExecStart=/usr/bin/python3 /opt/range/oldbanner.py
Restart=always
[Install]
WantedBy=multi-user.target
EOF

########################### LINUX PRIVESC SUITE ###########################
echo "[*] 6a. sudo misconfig (GTFOBins: NOPASSWD /usr/bin/find for bob)..."
pct exec $ID -- bash -c 'echo "bob ALL=(ALL) NOPASSWD: /usr/bin/find" > /etc/sudoers.d/bob; chmod 440 /etc/sudoers.d/bob'

echo "[*] 6b. SUID binary that should not be (cp)..."
pct exec $ID -- bash -c 'cp /bin/cp /usr/local/bin/cp-suid 2>/dev/null; chmod 4755 /usr/local/bin/cp-suid'

echo "[*] 6c. root cron running a world-writable script..."
pct exec $ID -- bash -c 'cat > /opt/range/backup.sh' <<"EOF"
#!/bin/bash
# "nightly backup" — intentionally world-writable (privesc: overwrite me)
date >> /var/log/range-backup.log
EOF
pct exec $ID -- bash -c 'chmod 777 /opt/range/backup.sh; echo "* * * * * root /opt/range/backup.sh" > /etc/cron.d/range-backup; chmod 644 /etc/cron.d/range-backup'

echo "[*] 6d. readable credentials in a config + history file..."
pct exec $ID -- bash -c 'printf "DB_USER=root\nDB_PASS=Sup3rS3cret-DB!\n" > /opt/range/app.conf; chmod 644 /opt/range/app.conf; \
  printf "mysql -uroot -pSummer2020! -h db.internal\nexport API_TOKEN=ghp_FAKEtoken1234567890\n" >> /home/bob/.bash_history; chmod 644 /home/bob/.bash_history'

echo "[*] 6e. PATH-hijack opportunity (root cron calls a bare command; writable dir on PATH)..."
pct exec $ID -- bash -c 'mkdir -p /usr/local/sbin; chmod 777 /usr/local/sbin; \
  cat > /opt/range/sysmon.sh <<SM
#!/bin/bash
# root job that calls a bare binary name (hijackable if attacker writes ./backup in a writable PATH dir)
cd /opt/range && backup >/dev/null 2>&1 || true
SM
chmod 755 /opt/range/sysmon.sh; echo "*/2 * * * * root PATH=/usr/local/sbin:/usr/bin:/bin /opt/range/sysmon.sh" > /etc/cron.d/range-sysmon; chmod 644 /etc/cron.d/range-sysmon'

########################### REMEDIATE KEY + ENABLE ###########################
echo "[*] 7. remediate SSH key for root (blue-team fix phase)..."
pct exec $ID -- mkdir -p /root/.ssh
printf '%s\n' "$REMPUB" > /tmp/rem.pub
pct push $ID /tmp/rem.pub /root/.ssh/authorized_keys
pct exec $ID -- bash -c 'chmod 700 /root/.ssh; chmod 600 /root/.ssh/authorized_keys'

echo "[*] 8. enable services..."
pct exec $ID -- bash -c 'systemctl daemon-reload; \
  systemctl enable --now vsftpd smbd nmbd snmpd ssh oldbanner 2>/dev/null; \
  systemctl restart ssh 2>/dev/null || true'

rm -f /tmp/rem.pub
echo "[*] misa service+privesc build complete (NIC still attached; labctl + isolation done by caller)."
