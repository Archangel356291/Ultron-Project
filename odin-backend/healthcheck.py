"""Container HEALTHCHECK: exit 0 if this backend answers GET /api/health.

Talks to 127.0.0.1 in whichever scheme the server is using. The certificate
is issued for the device's *.ts.net name, so it can never match 127.0.0.1;
verification is skipped for this one loopback call to ourselves, the same
reasoning as the Discord bot's connection over the private bridge network.
"""
import os
import ssl
import sys
import urllib.request

tls = bool((os.environ.get("ODIN_TLS_CERT") or "").strip() and (os.environ.get("ODIN_TLS_KEY") or "").strip())
ctx = ssl._create_unverified_context() if tls else None
try:
    with urllib.request.urlopen(("https" if tls else "http") + "://127.0.0.1:5000/api/health", timeout=5, context=ctx) as res:
        sys.exit(0 if res.status == 200 else 1)
except Exception as err:  # a failed check must say why in `docker inspect`
    print("unhealthy:", err)
    sys.exit(1)
