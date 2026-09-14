# Runs both privacy-enforcement steps in the right order, with each
# step's own required interpreter. See GRAPH-SCHEMA-DESIGN.md.
#
# IMPORTANT: run this after ANY graphify activity that touches
# graph.json -- not just a manual `graphify update`, but also
# graphify's own post-commit/post-checkout hook, which fires
# automatically and regenerates GRAPH_REPORT.md/graph.html with
# graphify's own (leaky) community-naming logic every time. Verified
# during Module 4 development: the hook reopened the community-name
# leak this script closes, on the very next commit after it was fixed,
# with no warning. There is currently no automatic trigger for this --
# you have to remember to run it.
#
#   powershell -File graph-schema\run.ps1

$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $PSScriptRoot

Write-Host "[graph-schema] enrich_visibility.py (system Python, needs cryptography)..."
python "$root\graph-schema\enrich_visibility.py"
if ($LASTEXITCODE -ne 0) { throw "enrich_visibility.py failed" }

Write-Host "[graph-schema] safe_report.py (graphify's own interpreter)..."
$graphifyPython = Get-Content "$root\graphify-out\.graphify_python" -ErrorAction SilentlyContinue
if (-not $graphifyPython) {
    Write-Warning "graphify-out\.graphify_python not found -- falling back to 'python', which may not have graphify installed."
    $graphifyPython = "python"
}
& $graphifyPython "$root\graph-schema\safe_report.py"
if ($LASTEXITCODE -ne 0) { throw "safe_report.py failed" }

Write-Host "[graph-schema] done."
