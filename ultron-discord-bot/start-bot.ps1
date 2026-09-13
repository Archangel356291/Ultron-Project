# start-bot.ps1
#
# Fill in the values below once, save this file, and from then on
# ".\start-bot.ps1" starts the Discord bot. Run this in a SEPARATE
# PowerShell window from the backend — they're two independent processes.
#
# The backend must already be running (see ..\ultron-backend\start-ultron.ps1)
# before this bot can do anything useful — every command it has is an
# HTTP call to that backend.

# ============================================================
# REQUIRED — the bot will not start without all three of these
# ============================================================

# From the Discord Developer Portal (discord.com/developers/applications) —
# create an application, add a Bot, copy its token:
$env:DISCORD_BOT_TOKEN = "PASTE-YOUR-DISCORD-BOT-TOKEN-HERE"

# The SAME token you set in ultron-backend\start-ultron.ps1 — this is how
# the bot authenticates to the backend:
$env:ULTRON_API_TOKEN = "PASTE-YOUR-TOKEN-HERE"

# Comma-separated Discord user IDs allowed to use the bot. Right-click
# your own username in Discord (with Developer Mode on, in Settings ->
# Advanced) -> "Copy User ID". Without this, the bot refuses to start —
# there is no default allowlist, on purpose:
$env:ULTRON_DISCORD_ALLOWED_USERS = "PASTE-YOUR-DISCORD-USER-ID-HERE"

# ============================================================
# Optional
# ============================================================

# Only needed if the bot runs on a DIFFERENT machine than the backend.
# If they're on the same PC, the default (127.0.0.1) is already correct —
# leave this commented out:
# $env:ULTRON_BACKEND_URL = "http://127.0.0.1:5000"

# Speeds up slash-command syncing to ONE server during setup/testing
# (instant instead of up to an hour for global sync). Right-click your
# Discord server icon -> "Copy Server ID" (Developer Mode required).
# Remove this once you're done testing and want the bot in more than
# one server:
# $env:ULTRON_DISCORD_DEV_GUILD_ID = "PASTE-YOUR-SERVER-ID-HERE"

# ============================================================
# Start it
# ============================================================
$placeholders = @{
    "DISCORD_BOT_TOKEN"            = $env:DISCORD_BOT_TOKEN
    "ULTRON_API_TOKEN"              = $env:ULTRON_API_TOKEN
    "ULTRON_DISCORD_ALLOWED_USERS"   = $env:ULTRON_DISCORD_ALLOWED_USERS
}
$hasPlaceholder = $false
foreach ($name in $placeholders.Keys) {
    $value = $placeholders[$name]
    if ([string]::IsNullOrWhiteSpace($value) -or $value -like "PASTE-*") {
        Write-Host "$name is still a placeholder — edit this script and set a real value before running it." -ForegroundColor Red
        $hasPlaceholder = $true
    }
}
if ($hasPlaceholder) { exit 1 }

python bot.py
