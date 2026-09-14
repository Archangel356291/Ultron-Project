# run-beta.ps1
#
# Same as ".\start-ultron.ps1" but activates this folder's venv first —
# for launching from a non-interactive context (a scheduled task, a
# background process, an already-running script) where you can't just
# activate the venv yourself in the current shell first. If you're typing
# commands interactively, activate the venv and run start-ultron.ps1
# directly instead; this exists for everything else.
& "$PSScriptRoot\venv\Scripts\Activate.ps1"
& "$PSScriptRoot\start-ultron.ps1"
