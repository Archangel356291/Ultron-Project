# System audit log

Append-only, deterministic record of agent/tool activity — the target for the
**Overwatch** (`overwatch-logger`) agent and, optionally, Claude Code lifecycle
hooks. One event per line, JSON.

## Files

- `system_audit.log` — append-only JSONL. Created on first write. Never
  truncated or rewritten in place; new entries are appended.
- `audit-append.py` — tiny helper: reads a hook's JSON event on stdin and
  appends a compact record here. Safe to call from a hook or by hand.

## Enabling deterministic hooks (optional, off by default)

The orchestration design uses two Claude Code lifecycle hooks. They are **not
enabled automatically** — turning on a hook changes every session, so enable it
deliberately. To enable, add to `.claude/settings.json`:

```json
{
  "hooks": {
    "PreToolUse": [
      { "matcher": "Bash|Write|Edit",
        "hooks": [ { "type": "command", "command": "python dev-tools/audit/audit-append.py" } ] }
    ],
    "Stop": [
      { "hooks": [ { "type": "command", "command": "python dev-tools/audit/audit-append.py" } ] }
    ]
  }
}
```

- **PreToolUse** (matched to destructive tools) records a line before a Bash /
  Write / Edit runs.
- **Stop** records a session-end delta.

The record is written by us (the hook), not by a subagent — so it stays
deterministic even though subagents run in isolated contexts. Overwatch reads
this file to analyze activity; it may also append its own structured findings,
and only ever writes here (never to source).

Do not log secret values, credentials, or chat content. Records are counts,
event types, tool names, and short summaries.
