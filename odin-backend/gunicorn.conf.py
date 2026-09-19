"""How the backend is served in the container: gunicorn, not Flask's
development server (LAUNCH-READINESS item 1). `python app.py` still works for
local, non-Docker development on Windows, where gunicorn does not run.

One worker, on purpose. Sign-in lockouts, the chat rate limit, action
confirmation tokens, presence and Sentinel's state all live in this process's
memory, and the background schedulers start at import -- a second worker
would mean a second, disagreeing copy of each. Concurrency comes from
threads instead, which is also what the dev server's threaded=True gave:
a chat request waiting on the LLM must not queue the dashboard's polling
behind it.
"""
import os

bind = "0.0.0.0:5000"
workers = 1
worker_class = "gthread"
threads = 16
# A thread worker heartbeats independently of the requests it is serving, so
# this is a hang detector for the process, not a cap on how long a streamed
# chat reply may take.
timeout = 120
graceful_timeout = 20
keepalive = 5
accesslog = "-"   # request lines to stdout, as before, so `docker logs` reads the same
errorlog = "-"

# Same rule as app._resolve_ssl_context (kept in step by
# dev-tools/test_tls_fallback.py): TLS only when both the certificate and the
# key are configured, otherwise plain HTTP rather than a half-configured state.
_cert = (os.environ.get("ODIN_TLS_CERT") or "").strip()
_key = (os.environ.get("ODIN_TLS_KEY") or "").strip()
if _cert and _key:
    certfile, keyfile = _cert, _key
