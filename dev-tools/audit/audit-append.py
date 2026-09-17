#!/usr/bin/env python3
"""Append one JSON line to the append-only system audit log.

Reads a Claude Code hook event (JSON) on stdin and appends a compact record to
dev-tools/audit/system_audit.log. Safe to call from a PreToolUse / Stop hook or
by hand. Never truncates; never logs secret values (it records event/tool/agent
metadata, not tool inputs).

Usage (hook): stdin = the hook's JSON payload.
Usage (manual): echo '{"event":"note","summary":"..."}' | python audit-append.py
"""
import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
LOG = os.path.join(HERE, "system_audit.log")


def main():
    raw = sys.stdin.read() if not sys.stdin.isatty() else ""
    payload = {}
    try:
        payload = json.loads(raw) if raw.strip() else {}
    except ValueError:
        payload = {"raw": raw[:200]}

    # Keep only non-sensitive metadata — never tool inputs / secrets / content.
    rec = {
        "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "event": payload.get("hook_event_name") or payload.get("event") or "event",
        "tool": payload.get("tool_name") or payload.get("tool"),
        "agent": payload.get("agent") or payload.get("subagent"),
        "summary": (payload.get("summary") or "")[:200],
    }
    rec = {k: v for k, v in rec.items() if v}
    try:
        os.makedirs(HERE, exist_ok=True)
        with open(LOG, "a", encoding="utf-8") as f:  # append-only
            f.write(json.dumps(rec, separators=(",", ":")) + "\n")
    except OSError:
        pass  # logging must never break the tool it observes
    # hooks expect a 0 exit and no blocking output
    sys.exit(0)


if __name__ == "__main__":
    main()
