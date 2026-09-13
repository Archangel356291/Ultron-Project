# start-ultron.ps1
#
# Fill in the values below once, save this file, and from then on
# ".\start-ultron.ps1" is the entire startup process instead of retyping
# a dozen $env: lines every session.
#
# Every variable here was pulled directly from app.py's actual
# os.environ.get() calls — nothing in this file is aspirational or
# for a feature that doesn't exist yet.

# ============================================================
# REQUIRED — the backend will not start without this one
# ============================================================
# Generate once, save it in a password manager, and reuse the SAME value
# here every time — this is the token the dashboard and bot both need.
$env:ULTRON_API_TOKEN = "PASTE-YOUR-TOKEN-HERE"

# Need to generate one? Uncomment the next two lines, run this script once,
# copy the printed token into the line above, then re-comment these two:
# $generated = -join ((48..57)+(97..102)|Get-Random -Count 32|%{[char]$_})
# Write-Host "Generated token (save this, then paste it above):" $generated

# ============================================================
# Chat — optional, but this is almost certainly why you're here
# ============================================================
# Without this, every panel except AI Assistant chat still works, and
# /api/chat returns a clear "not configured" message. Uncomment and fill
# in your real key to turn chat on — an unedited placeholder here would
# cause a confusing authentication error instead, so leave it commented
# out entirely rather than active-with-a-placeholder:
# $env:ANTHROPIC_API_KEY = "sk-ant-..."

# Uncomment to override the model (defaults to claude-sonnet-5):
# $env:ULTRON_LLM_MODEL = "claude-sonnet-5"

# Uncomment to change how long a request can wait on the LLM before
# timing out (defaults to 60 seconds):
# $env:ULTRON_LLM_TIMEOUT_SECONDS = "60"

# Uncomment to cap how long a single reply can be (defaults to 1024
# tokens) — lower for tighter cost control, raise if replies feel cut off:
# $env:ULTRON_LLM_MAX_TOKENS = "1024"

# Uncomment to set a real daily hard spend cap, in total tokens
# (input + output). Unset by default = no limit. Worth turning on during
# a beta specifically, while you're finding out how much you actually use:
# $env:ULTRON_LLM_DAILY_TOKEN_BUDGET = "100000"

# Uncomment to change the chat rate limit (defaults to 20 requests/minute
# already — only touch this if you're actually hitting it):
# $env:ULTRON_CHAT_RATE_LIMIT_PER_MINUTE = "20"

# ============================================================
# Backups — optional. Both must be set together for the feature to work.
# ============================================================
# Semicolon-separated list of directories to back up:
# $env:ULTRON_BACKUP_SOURCES = "C:\Users\you\docker-volumes;C:\Users\you\configs"
# Where the backup .zip files get written:
# $env:ULTRON_BACKUP_DEST = "D:\Backups"

# ============================================================
# Development tab — optional. Real git status/diff for your own repos.
# ============================================================
# Semicolon-separated list of local git repo paths:
# $env:ULTRON_CODE_REPOS = "C:\Users\you\ultron-core;C:\Users\you\lab-infra"

# ============================================================
# External tools (MCP) — optional, read the backend README's
# "External tools (MCP)" section before turning this on. Real security
# implications: only approve tools from servers you actually trust.
# ============================================================
# Path to a JSON config file listing MCP servers and per-server approved
# tool names:
# $env:ULTRON_MCP_CONFIG = "C:\Users\you\mcp-config.json"

# ============================================================
# Advanced / rarely needed
# ============================================================
# Where the SQLite database (activity log, trades, LLM usage) lives.
# Defaults to ultron.db next to app.py — only change this if you have a
# specific reason to:
# $env:ULTRON_DB_PATH = "C:\Ultron\data\ultron.db"

# CORS origin restriction. Defaults to "*" (any origin), which is fine on
# your own network. Once the dashboard has a fixed address, restrict it:
# $env:ULTRON_ALLOWED_ORIGIN = "http://your-dashboard-host:port"

# ============================================================
# Start it
# ============================================================
if ($env:ULTRON_API_TOKEN -eq "PASTE-YOUR-TOKEN-HERE" -or [string]::IsNullOrWhiteSpace($env:ULTRON_API_TOKEN)) {
    Write-Host "ULTRON_API_TOKEN is still the placeholder value — edit this script and set a real token before running it." -ForegroundColor Red
    exit 1
}
python app.py
