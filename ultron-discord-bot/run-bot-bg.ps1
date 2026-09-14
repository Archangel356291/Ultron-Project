# run-bot-bg.ps1
#
# Same as ".\start-bot.ps1" but activates this folder's venv first — for
# launching from a non-interactive context (a scheduled task, a
# background process, an already-running script) where you can't just
# activate the venv yourself in the current shell first. If you're typing
# commands interactively, activate the venv and run start-bot.ps1 directly
# instead; this exists for everything else. Mirrors
# ultron-backend/run-beta.ps1.
& "$PSScriptRoot\venv\Scripts\Activate.ps1"
& "$PSScriptRoot\start-bot.ps1"
