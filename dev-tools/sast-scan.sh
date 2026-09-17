#!/usr/bin/env bash
# Sandboxed static analysis for Ultron (Auditor's runtime half).
#
# Runs three open-source scanners against this repository, each inside a
# throwaway container with the repo mounted READ-ONLY -- nothing executes on
# the host, nothing can write back, no network is needed after the images
# are pulled:
#   gitleaks  -- secrets in the working tree (the pre-commit hook covers commits)
#   bandit    -- Python security issues (ultron-backend, ultron-discord-bot)
#   semgrep   -- multi-language rules (p/ci: secrets, injection, crypto, ...)
# Prints a short summary per tool and writes full JSON reports to
# dev-tools/sast-reports/ (gitignored). Exit code 0 = clean, 1 = findings.
#
#   bash dev-tools/sast-scan.sh            # everything
#   bash dev-tools/sast-scan.sh bandit     # one tool
set -u
# Git Bash on Windows: pwd -W gives the C:/... form Docker Desktop wants for
# -v, and MSYS_NO_PATHCONV stops Git Bash rewriting the container-side
# "/src" and "/out" into C:\Program Files\Git\src.
export MSYS_NO_PATHCONV=1
REPO="$(cd "$(dirname "$0")/.." && (pwd -W 2>/dev/null || pwd))"
OUT="$REPO/dev-tools/sast-reports"
mkdir -p "$OUT"
ONLY="${1:-all}"
status=0
run() { [ "$ONLY" = all ] || [ "$ONLY" = "$1" ]; }

if run gitleaks; then
  echo "== gitleaks (working tree)"
  docker run --rm -v "$REPO:/src:ro" -v "$OUT:/out" zricethezav/gitleaks:latest \
    detect --source /src --no-git --redact --config /src/dev-tools/sast-gitleaks.toml \
    --report-format json --report-path /out/gitleaks.json >/dev/null 2>&1
  n=$(python -c "import json;print(len(json.load(open(r'$OUT/gitleaks.json'))))" 2>/dev/null || echo "?")
  echo "   findings: $n"; [ "$n" = "0" ] || status=1
fi

if run bandit; then
  echo "== bandit (python)"
  docker run --rm -v "$REPO:/src:ro" -v "$OUT:/out" ghcr.io/pycqa/bandit/bandit:latest \
    -q -r /src/ultron-backend/app.py /src/ultron-backend/graph_schema_shared.py /src/ultron-discord-bot/bot.py \
    -f json -o /out/bandit.json >/dev/null 2>&1
  python - "$OUT/bandit.json" <<'EOF' || status=1
import json, sys, collections
d = json.load(open(sys.argv[1]))
c = collections.Counter(r["issue_severity"] for r in d["results"])
print("   findings:", dict(c) or 0)
for r in d["results"]:
    if r["issue_severity"] in ("HIGH", "MEDIUM"):
        print(f"   {r['issue_severity']:6s} {r['test_id']} {r['filename'].replace('/src/','')}:{r['line_number']} {r['issue_text'][:80]}")
sys.exit(1 if any(r["issue_severity"] in ("HIGH", "MEDIUM") for r in d["results"]) else 0)
EOF
fi

if run semgrep; then
  echo "== semgrep (p/ci)"
  docker run --rm -v "$REPO:/src:ro" -v "$OUT:/out" -e SEMGREP_SEND_METRICS=off semgrep/semgrep:latest \
    semgrep scan --config p/ci --json -o /out/semgrep.json --quiet --metrics=off \
    --exclude 'graphify-out' --exclude 'three-pipeline' --exclude 'dev-tools/fake_pkgs' --exclude '*.min.js' /src >/dev/null 2>&1
  python - "$OUT/semgrep.json" <<'EOF' || status=1
import json, sys, collections
d = json.load(open(sys.argv[1]))
res = d.get("results", [])
c = collections.Counter(r["extra"]["severity"] for r in res)
print("   findings:", dict(c) or 0)
for r in res:
    if r["extra"]["severity"] in ("ERROR", "WARNING"):
        print(f"   {r['extra']['severity']:7s} {r['check_id'].split('.')[-1][:40]} {r['path'].replace('/src/','')}:{r['start']['line']}")
sys.exit(1 if res else 0)
EOF
fi

echo "reports: $OUT"
exit $status
