# TLS cert for the backend

`ultron.crt` / `ultron.key` in this directory are a real certificate
issued by Tailscale (`tailscale cert`) for this specific device's
`*.ts.net` name — not committed to git, not baked into the Docker image
(see `.gitignore` / `.dockerignore`), bind-mounted read-only into the
`ultron-backend` container instead (`docker-compose.yml`).

## Regenerating

Needed the first time, and again whenever the cert expires (Tailscale
certs are short-lived, similar to Let's Encrypt — check the actual
expiry with `openssl x509 -enddate -noout -in ultron.crt`; there's no
automatic renewal wired up here, this is a manual step):

```powershell
cd "C:\Ultron Project\Ultron Project\ultron-backend\tls"
tailscale cert --cert-file=ultron.crt --key-file=ultron.key <this-device>.<tailnet>.ts.net
```

Get the exact hostname to use with `tailscale status` (your own device's
row) — it's printed there, e.g. `desktop-47v3oim.tailc5bde9.ts.net`.
Requires "HTTPS Certificates" to be turned on for the tailnet first, in
the Tailscale admin console's DNS tab.

Then recreate the backend container so it picks up the refreshed files:

```powershell
docker compose up -d --force-recreate ultron-backend
```

## What happens without a cert here

`app.py` checks `ULTRON_TLS_CERT`/`ULTRON_TLS_KEY` at startup — if either
file is missing, it falls back to plain HTTP automatically. That's the
normal state for local/non-Docker dev (`start-ultron.ps1`), which has no
reason to have Tailscale certs configured at all.
