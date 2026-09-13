"""
Ultron home lab monitoring backend.

Exposes a small JSON API that the dashboard (ultron-dashboard.html) can poll
for real system, container, and storage data. Designed to run on the
Raspberry Pi 400 (or any Linux host) alongside Docker.

Endpoints:
    GET /api/status       -> overview: cpu, mem, temp, uptime, container counts
    GET /api/containers    -> list of Docker containers with cpu/mem/status
    GET /api/storage        -> disk usage per configured mount/path
    GET /api/systems         -> pending OS package updates + hardware health
    GET /api/health              -> simple liveness check, no auth required

Auth:
    Every route except /api/health requires header:
        Authorization: Bearer <ULTRON_API_TOKEN>
    Set ULTRON_API_TOKEN as an environment variable before starting the
    service. There is no default — the app refuses to start without one.

Run:
    pip install -r requirements.txt
    export ULTRON_API_TOKEN="change-me-to-something-long-and-random"
    python app.py
"""

"""
Ultron home lab monitoring backend.

Exposes a small JSON API that the dashboard (ultron-dashboard.html) can poll
for real system, container, and storage data. Runs on the Windows 11
Cyberpower PC (also works unmodified on Linux/Raspberry Pi OS hosts — the
platform-specific bits below detect the OS at runtime).

Endpoints:
    GET /api/status       -> overview: cpu, mem, temp, uptime, container counts
    GET /api/containers    -> list of Docker containers with cpu/mem/status
    GET /api/storage        -> disk usage per configured drive/mount
    GET /api/systems         -> pending OS updates + hardware health
    GET /api/health              -> simple liveness check, no auth required

Auth:
    Every route except /api/health requires header:
        Authorization: Bearer <ULTRON_API_TOKEN>
    Set ULTRON_API_TOKEN as an environment variable before starting the
    service. There is no default — the app refuses to start without one.

Run (PowerShell):
    pip install -r requirements.txt
    $env:ULTRON_API_TOKEN = "change-me-to-something-long-and-random"
    python app.py

Windows-specific notes:
    - CPU temperature reads via WMI (MSAcpi_ThermalZoneTemperature). Many
      consumer motherboards don't expose this to Windows at all — if it
      returns null, that's the hardware/firmware, not a bug. Consider an
      OEM tool (HWiNFO, etc.) as a source of truth if you need this.
    - "Pending updates" queries the real Windows Update Agent via COM, which
      requires pywin32 and can take several seconds to run.
"""

import hmac
import os
import platform
import shutil
import subprocess
import sys
import time
from functools import wraps

import psutil
from flask import Flask, jsonify, request

app = Flask(__name__)

API_TOKEN = os.environ.get("ULTRON_API_TOKEN")
if not API_TOKEN:
    sys.exit(
        "ULTRON_API_TOKEN is not set. Refusing to start with no auth token.\n"
        "Set it with (PowerShell): $env:ULTRON_API_TOKEN = '<a long random string>'"
    )

# Origin the dashboard is served from, for CORS. Set this to your actual
# dashboard origin (e.g. "http://192.168.1.50:8080") in production — the "*"
# default is fine for local-network testing but allows any site to read
# responses if this API is ever reachable beyond your LAN.
ALLOWED_ORIGIN = os.environ.get("ULTRON_ALLOWED_ORIGIN", "*")

# Paths/drives to report on for the Storage panel. Defaults match a stock
# Windows 11 install (C:\); add other drive letters as needed, e.g.
# {"c_drive": "C:\\", "d_drive": "D:\\"}.
STORAGE_MOUNTS = (
    {"c_drive": "C:\\"}
    if platform.system() == "Windows"
    else {"ssd": "/mnt/ssd", "root": "/"}
)


@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = ALLOWED_ORIGIN
    response.headers["Access-Control-Allow-Headers"] = "Authorization, Content-Type"
    response.headers["Access-Control-Allow-Methods"] = "GET, OPTIONS"
    return response


# --------------------------------------------------------------------------
# auth
# --------------------------------------------------------------------------
def require_token(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        auth = request.headers.get("Authorization", "")
        token = auth[7:] if auth.startswith("Bearer ") else ""
        if not hmac.compare_digest(token, API_TOKEN):
            return jsonify({"error": "unauthorized"}), 401
        return fn(*args, **kwargs)
    return wrapper


# --------------------------------------------------------------------------
# helpers
# --------------------------------------------------------------------------
def get_cpu_temp_c():
    """Best-effort CPU temperature read. Returns None if unavailable —
    which, on Windows, is common: most consumer boards don't expose this
    to the OS without vendor-specific tooling."""
    system = platform.system()

    if system == "Windows":
        try:
            import wmi  # requires the 'wmi' + 'pywin32' packages
            w = wmi.WMI(namespace="root\\wmi")
            zones = w.MSAcpi_ThermalZoneTemperature()
            if zones:
                # value is in tenths of a degree Kelvin
                kelvin = zones[0].CurrentTemperature / 10.0
                return round(kelvin - 273.15, 1)
        except Exception:
            pass
        return None

    # Linux (Raspberry Pi OS, Ubuntu Server, etc.)
    thermal_path = "/sys/class/thermal/thermal_zone0/temp"
    try:
        with open(thermal_path) as f:
            milli_c = int(f.read().strip())
            return round(milli_c / 1000.0, 1)
    except (FileNotFoundError, ValueError, PermissionError):
        pass

    if shutil.which("vcgencmd"):
        try:
            out = subprocess.run(
                ["vcgencmd", "measure_temp"],
                capture_output=True, text=True, timeout=2,
            ).stdout.strip()
            # format: temp=51.4'C
            return float(out.split("=")[1].split("'")[0])
        except Exception:
            pass
    return None


def get_uptime_str():
    boot = psutil.boot_time()
    seconds = int(time.time() - boot)
    days, rem = divmod(seconds, 86400)
    hours, rem = divmod(rem, 3600)
    minutes = rem // 60
    if days:
        return f"{days}d {hours}h"
    if hours:
        return f"{hours}h {minutes}m"
    return f"{minutes}m"


def docker_ps():
    """Return container info via the Docker CLI, avoiding a hard dependency
    on the docker Python SDK. Requires the service user to be in the
    'docker' group (or run with access to the Docker socket)."""
    if not shutil.which("docker"):
        return None, "docker CLI not found on this host"

    fmt = "{{.Names}}|{{.Image}}|{{.Status}}|{{.RunningFor}}"
    try:
        result = subprocess.run(
            ["docker", "ps", "-a", "--format", fmt],
            capture_output=True, text=True, timeout=5,
        )
    except Exception as e:
        return None, str(e)

    if result.returncode != 0:
        return None, result.stderr.strip() or "docker ps failed"

    containers = []
    for line in result.stdout.strip().splitlines():
        if not line:
            continue
        name, image, status, running_for = (line.split("|") + ["", "", "", ""])[:4]
        containers.append({
            "name": name,
            "image": image,
            "status": status,
            "running_for": running_for,
            "state": "running" if status.lower().startswith("up") else "stopped",
        })
    return containers, None


def docker_stats():
    """Live CPU/mem per container, keyed by name. Best-effort; returns {}
    on any failure so /api/containers still works without it."""
    if not shutil.which("docker"):
        return {}
    fmt = "{{.Name}}|{{.CPUPerc}}|{{.MemUsage}}"
    try:
        result = subprocess.run(
            ["docker", "stats", "--no-stream", "--format", fmt],
            capture_output=True, text=True, timeout=8,
        )
    except Exception:
        return {}
    stats = {}
    for line in result.stdout.strip().splitlines():
        parts = line.split("|")
        if len(parts) == 3:
            name, cpu, mem = parts
            stats[name.lstrip("/")] = {"cpu": cpu, "mem": mem}
    return stats


def pending_os_updates():
    """Count of pending OS updates. Real implementation on both platforms:
    Windows Update Agent (COM) on Windows, apt on Debian-family Linux.
    Returns None if the platform's mechanism isn't available."""
    system = platform.system()

    if system == "Windows":
        try:
            import win32com.client  # requires 'pywin32'
            session = win32com.client.Dispatch("Microsoft.Update.Session")
            searcher = session.CreateUpdateSearcher()
            # NOTE: this hits Windows Update and can take several seconds.
            result = searcher.Search("IsInstalled=0 and IsHidden=0")
            return result.Updates.Count
        except Exception:
            return None

    if not shutil.which("apt"):
        return None
    try:
        result = subprocess.run(
            ["apt", "list", "--upgradable"],
            capture_output=True, text=True, timeout=10,
        )
        lines = [l for l in result.stdout.strip().splitlines() if "/" in l]
        return len(lines)
    except Exception:
        return None


# --------------------------------------------------------------------------
# routes
# --------------------------------------------------------------------------
@app.route("/api/health")
def health():
    return jsonify({"ok": True})


@app.route("/api/status")
@require_token
def status():
    containers, err = docker_ps()
    running = sum(1 for c in containers if c["state"] == "running") if containers else 0
    total = len(containers) if containers else 0

    return jsonify({
        "cpu_percent": psutil.cpu_percent(interval=0.3),
        "mem_percent": psutil.virtual_memory().percent,
        "cpu_temp_c": get_cpu_temp_c(),
        "uptime": get_uptime_str(),
        "containers_running": running,
        "containers_total": total,
        "containers_error": err,
    })


@app.route("/api/containers")
@require_token
def containers():
    containers, err = docker_ps()
    if err:
        return jsonify({"error": err}), 502
    stats = docker_stats()
    for c in containers:
        s = stats.get(c["name"])
        if s:
            c["cpu"] = s["cpu"]
            c["mem"] = s["mem"]
    return jsonify({"containers": containers})


@app.route("/api/storage")
@require_token
def storage():
    result = {}
    for label, path in STORAGE_MOUNTS.items():
        try:
            usage = shutil.disk_usage(path)
            result[label] = {
                "path": path,
                "total_gb": round(usage.total / 1e9, 1),
                "used_gb": round(usage.used / 1e9, 1),
                "percent_used": round(usage.used / usage.total * 100, 1),
            }
        except (FileNotFoundError, OSError):
            result[label] = {"path": path, "error": "path not found"}
    return jsonify(result)


@app.route("/api/systems")
@require_token
def systems():
    return jsonify({
        "pending_updates": pending_os_updates(),
        "cpu_temp_c": get_cpu_temp_c(),
        "uptime": get_uptime_str(),
        "load_avg": os.getloadavg() if hasattr(os, "getloadavg") else None,
    })


if __name__ == "__main__":
    # Bind to all interfaces so it's reachable from the dashboard on other
    # devices on your network. Put this behind Tailscale/WireGuard + a
    # reverse proxy with HTTPS for anything beyond local-network use —
    # this dev server is not meant to be exposed directly to the internet.
    app.run(host="0.0.0.0", port=5000)
