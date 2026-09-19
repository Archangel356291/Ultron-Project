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
# Secrets — loaded from ..\.env (KEY=value per line) if it exists, instead
# of being pasted into this file. This file is git-tracked; .env is
# gitignored. This is how a real token/API key should get here — the
# manual fallback lines below exist only for people not using a .env file,
# and are commented out by default so nothing real ever lands in git by
# accident (this is exactly the mistake this project already made once).
# ============================================================
$envFile = Join-Path $PSScriptRoot "..\.env"
if (Test-Path $envFile) {
    Get-Content $envFile | ForEach-Object {
        if ($_ -match '^\s*([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(.*?)\s*$') {
            [System.Environment]::SetEnvironmentVariable($matches[1], $matches[2], "Process")
        }
    }
    Write-Host "Loaded secrets from $envFile" -ForegroundColor DarkGray
}

# ============================================================
# REQUIRED — the backend will not start without this one
# ============================================================
# Generate once, save it (in .env above, or a password manager), and reuse
# the SAME value every time — this is the token the dashboard and bot both
# need. Only applied if .env didn't already supply one.
if (-not $env:ODIN_API_TOKEN) {
    $env:ODIN_API_TOKEN = "PASTE-YOUR-TOKEN-HERE"
}

# Need to generate one? Uncomment the next two lines, run this script once,
# copy the printed token into .env as ODIN_API_TOKEN=..., then re-comment:
# $generated = -join ((48..57)+(97..102)|Get-Random -Count 32|%{[char]$_})
# Write-Host "Generated token (save this to .env):" $generated

# ============================================================
# Beta testers — optional, restricted role
# ============================================================
# One SEPARATE, DISTINCT token per beta tester — never your own
# ODIN_API_TOKEN, and never one token shared between people. Each gets
# chat (full) + trading data (view-only); everything else 403s for this
# role, at the API level, not just hidden in the dashboard. Leave unset
# (default) and the beta_tester role doesn't exist at all — no one can
# use it, whatever token they try.
#
# Format: "name:token,name:token,..." — see BETA-TESTERS.md for how to
# generate a token and add someone to the roster.
# if (-not $env:ODIN_BETA_TOKENS) {
#     $env:ODIN_BETA_TOKENS = "alice:PASTE-ALICES-TOKEN-HERE,bob:PASTE-BOBS-TOKEN-HERE"
# }

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
# $env:ODIN_LLM_MODEL = "claude-sonnet-5"

# Uncomment to change how long a request can wait on the LLM before
# timing out (defaults to 60 seconds):
# $env:ODIN_LLM_TIMEOUT_SECONDS = "60"

# Uncomment to cap how long a single reply can be (defaults to 1024
# tokens) — lower for tighter cost control, raise if replies feel cut off:
# $env:ODIN_LLM_MAX_TOKENS = "1024"

# Daily hard spend cap, in total tokens (input + output). ON by default
# during beta — a real ceiling while you're finding out how much you
# actually use. Raise it or comment it out once you trust your usage:
$env:ODIN_LLM_DAILY_TOKEN_BUDGET = "50000"

# Uncomment to change the chat rate limit (defaults to 20 requests/minute
# already — only touch this if you're actually hitting it):
# $env:ODIN_CHAT_RATE_LIMIT_PER_MINUTE = "20"

# Lifetime dollar cap per beta tester (not per-day — never resets on its
# own). Already the default even if you don't set this, listed here so
# it's visible alongside the other cost controls. Each tester gets their
# own $1.00; admin chat is never subject to this:
$env:ODIN_BETA_MAX_SPEND_USD = "1.00"

# ============================================================
# Voice replies — optional. Both must be set together for the feature to
# work; requires a Fish Audio account (fish.audio) and API key. Both the
# key AND the voice ID belong in .env — this one points at a private
# cloned voice, not a public library one, so it's a secret too.
# ============================================================
# ODIN_FISH_AUDIO_API_KEY and ODIN_FISH_VOICE_ID both come from .env —
# nothing to add here.

# ============================================================
# Backups — optional. Both must be set together for the feature to work.
# ============================================================
# Semicolon-separated list of directories to back up:
# $env:ODIN_BACKUP_SOURCES = "C:\Users\you\docker-volumes;C:\Users\you\configs"
# Where the backup .zip files get written:
# $env:ODIN_BACKUP_DEST = "D:\Backups"

# ============================================================
# Development tab — optional. Real git status/diff for your own repos.
# ============================================================
# Semicolon-separated list of local git repo paths:
# $env:ODIN_CODE_REPOS = "C:\Users\you\ultron-core;C:\Users\you\lab-infra"

# ============================================================
# External tools (MCP) — optional, read the backend README's
# "External tools (MCP)" section before turning this on. Real security
# implications: only approve tools from servers you actually trust.
# ============================================================
# Path to a JSON config file listing MCP servers and per-server approved
# tool names:
# $env:ODIN_MCP_CONFIG = "C:\Users\you\mcp-config.json"

# ============================================================
# Advanced / rarely needed
# ============================================================
# Where the SQLite database (activity log, trades, LLM usage) lives.
# Defaults to odin.db next to app.py — only change this if you have a
# specific reason to:
# $env:ODIN_DB_PATH = "C:\Odin\data\odin.db"

# CORS origin restriction. Defaults to "*" (any origin), which is fine on
# your own network. Once the dashboard has a fixed address, restrict it:
# $env:ODIN_ALLOWED_ORIGIN = "http://your-dashboard-host:port"

# ============================================================
# Start it
# ============================================================
if ($env:ODIN_API_TOKEN -eq "PASTE-YOUR-TOKEN-HERE" -or [string]::IsNullOrWhiteSpace($env:ODIN_API_TOKEN)) {
    Write-Host "ODIN_API_TOKEN is still the placeholder value — edit this script and set a real token before running it." -ForegroundColor Red
    exit 1
}
python app.py
