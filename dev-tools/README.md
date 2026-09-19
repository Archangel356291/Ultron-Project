# dev-tools

Testing infrastructure used throughout this project's development —
**not part of the shipped product**, don't deploy this folder alongside
the real backend/bot. This is what let every feature in this project get
tested against realistic behavior without needing a real Anthropic API
key, a real Discord connection, or a real third-party MCP server.

## `fake_pkgs/` — drop-in fakes for `anthropic`, `discord`, and `aiohttp`

Point `PYTHONPATH` at this directory (before the real packages, or
instead of installing them) and `import anthropic` / `import discord` /
`import aiohttp` in `app.py` or `bot.py` will resolve to these instead of
the real SDKs:

```powershell
$env:PYTHONPATH = "C:\Odin\dev-tools\fake_pkgs"
```

Each fake mimics the real SDK's shape closely enough that code written
against it works unmodified against the real thing:

- **`fake_pkgs/anthropic`** — `Anthropic` client with a scriptable
  `.messages.create()`. Set `anthropic_client.messages.script = [Message(...), ...]`
  to queue canned responses (including tool-use turns), and
  `anthropic_client.messages.raise_on_call = SomeException()` to test
  error-handling paths. Includes the real exception hierarchy
  (`AuthenticationError`, `RateLimitError`, `APIConnectionError`, etc.)
  and a `Usage` class matching the real token-count fields, including
  `cache_read_input_tokens` / `cache_creation_input_tokens` for testing
  prompt-caching behavior.
- **`fake_pkgs/discord`** — `Interaction`, `Embed`, a `CommandTree` whose
  `.command()` decorator just registers the function directly (so you can
  call `bot.status_command(interaction)` in a test without going through
  real Discord networking), `ui.View`/`ui.Button` support for testing the
  Confirm/Cancel button flows, `File` for testing attachments, and
  `app_commands.Choice` for dropdown-style parameters.
- **`fake_pkgs/aiohttp`** — `ClientSession` with a scriptable
  `.calls` log and `.script` queue of `_MockResponse` objects (which
  support `.json()`, `.text()`, and `.headers` for testing
  Content-Disposition-based filename extraction, etc.).

Every one of these was extended incrementally as new features needed new
surface area — if the next feature needs something these don't support
yet, that's expected; extend the fake rather than skip the test.

## `test_mcp_server.py` — a real, protocol-compliant local MCP server

Not a mock — an actual Flask server implementing the real MCP JSON-RPC
methods (`initialize`, `notifications/initialized`, `tools/list`,
`tools/call`) with strict `assert`s on incoming request shape, so a bug
in the client's requests fails loudly here instead of being silently
tolerated. This is what caught two real bugs in the backend's MCP client
during development — testing against a lenient hand-rolled mock would
likely have hidden both.

Run it standalone:

```bash
python test_mcp_server.py <optional-auth-token> <port>
# e.g.: python test_mcp_server.py secret-token-123 6001
```

Offers four test tools: `echo` (round-trips input), `fail_on_purpose`
(always returns `isError: true`), `huge_response` (50,000 chars, for
testing truncation), and `not_approved_tool` (exists but should never be
in any test's `auto_approve` list — useful for verifying the approval
gate actually excludes it).

Point the backend's `ODIN_MCP_CONFIG` at a JSON file referencing
`http://127.0.0.1:<port>/mcp` to test the full MCP integration against
real request/response traffic.

## Why this exists as a separate folder

Every feature in this project was tested against something that behaves
like the real dependency, not just "doesn't crash." Real local git repos
for the Development tab, a real SQLite database for trades/activity/
usage tracking, a real local Flask server for MCP — and where a real
external dependency wasn't reachable (Anthropic's API, Discord's
gateway), these fakes stood in with enough fidelity to catch real bugs,
several of which are called out in the backend and bot READMEs where
they were found and fixed. Keeping using this approach for anything new
built here will hold new code to the same bar.
