# Rebuilds the graph of Ultron's Brain vault (D:\ultron's Brain&Knowledge)
# so recall_from_brain in the backend sees new conversations and notes.
# AST-only graphify pass over Markdown: no API key, no tokens. Registered as
# an hourly user-level scheduled task ("Ultron Brain Graph") -- see the
# backend README, "Where his knowledge lives".
$vault = "D:\ultron's Brain&Knowledge"
if (-not (Test-Path $vault)) { exit 0 }
& graphify update $vault 2>&1 | Out-Null
