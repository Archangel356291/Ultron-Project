# Open-sourcing Ultron (Module 12) — v1

The roadmap's own gate for this module: *"last, only once Module 3, 4,
and 9 are solid"* — confirmed true (`GIT-SECRET-AUDIT.md`, this module's
own history re-scan below, `GRAPH-SCHEMA-DESIGN.md`, and
`backup/README.md` / the verified restore test respectively). Steps 36-39
from the roadmap, in order:

## 36. Confirm Module 3 and Module 4 are solid

- **Module 3** (repo history clean): re-confirmed below, this module's
  own re-scan.
- **Module 4** (public/private split exists): `graph-schema/enrich_visibility.py`
  still classifies and encrypts private nodes; `graphify-out/private-nodes.enc.json`
  stays gitignored (never committed even encrypted, per Module 9's own
  rule). Unaffected by Module 10's refactor — the classification logic
  moved to `ultron-backend/graph_schema_shared.py`, not its behavior.

## 37. Pick a license

MIT — the roadmap's own named default, and there's no reason here to
deviate from it (a personal project with no patent concerns, no prior
license commitments to reconcile with). Added as `LICENSE` at the repo
root, referenced from `README.md`'s new License section.

## 38. Public-facing documentation, without exposing home lab layout, network details, or financial specifics

**A real finding, not a clean pass.** `gitleaks` (Module 3's own gate)
only looks for credential-shaped strings — API keys, tokens, private
keys — and correctly found none. It has no concept of "personally-
identifying but not a credential," which is exactly the gap step 38
calls out separately from step 39's automated scan. Manually reviewing
every doc (not just grepping for dollar signs and IPs) found real
personal/network-identifying content that gitleaks would never catch:

| File | What was exposed | Fix |
|---|---|---|
| `ultron-backend/PI-SETUP.md` | The real Windows username (`C:\Users\redacted-user\...`), three real device hostnames (`pc-device-name`, `phone-device-name`, `phone2-device-name`), the real Tailscale account handle (`Archangel356291@`), and a real SSH public key tied to real infrastructure | All replaced with generic placeholders (`C:\Users\<you>\...`, "your other devices," a placeholder key format) |
| `ultron-backend/BETA-LAUNCH-CHECKLIST.md` | The real hostname + real tailnet ID (`pc-device-name.tailXXXX.ts.net`) in a historical test-log entry | Replaced with the same placeholder pattern `REMOTE-ACCESS.md` already used (`your-pc-name.tailXXXX.ts.net`) |
| `.githooks/pre-commit` | The real Windows username hardcoded into the gitleaks-binary fallback path | Changed to `$HOME`-relative — also just a correctness fix, since a hardcoded username breaks the hook for anyone else who clones this repo |
| `graphify-out/.graphify_python` | A machine-local sidecar (graphify's own skill writes it) containing the real username in an absolute interpreter path — and meaningless to anyone else regardless, since it points at *this* machine's own Python install | Untracked (`git rm --cached`) and added to `.gitignore` — same category as `.env`, local environment state that was never a deliverable |

`REMOTE-ACCESS.md` itself was already clean — it was written with
placeholder hostnames throughout from the start, which is why the same
sweep didn't flag it.

**What was checked and found clean:** dollar amounts across every `.md`
file (all `$1.00` hits are the designed, public beta-spend-cap feature,
not real financial data — see `BETA-TESTERS.md`); IP addresses (the one
hit, `192.168.1.50` in `ultron-backend/README.md`, is a standard
RFC1918 documentation example, same category as gitleaks' own allowlisted
AWS example key); no real names beyond the GitHub handles already
public in this repo's commit history and contributor credits.

**What this fix does and doesn't cover:** these are working-tree edits —
every commit from here forward is clean. The *same* username/hostnames/
handle are still sitting in already-pushed commit history (multiple
commits, since these files have existed since early in the project).
gitleaks' full-history scan (step 39, below) genuinely can't catch this
class of leak — it isn't credential-shaped, so there's nothing for a
secret scanner's ruleset to match. **This is the one item Module 12
surfaces back to the user rather than resolving unilaterally**: scrubbing
it from history means `git filter-repo` (installed, per Module 3, but
never used) plus a force-push — a destructive, hard-to-reverse operation
on a repo other people may already have cloned privately. Leaving it
means a personal Windows username, three real device names, and a
Tailscale account handle are visible in history to anyone who digs past
the current `main` once the repo goes public. Both are legitimate calls;
neither is this module's to make alone.

## 39. Secret scanner one final time, then manual review, before flipping visibility

```
gitleaks detect --source . --log-opts="--all" -c .gitleaks.toml --report-format json --report-path <scratch>.json --exit-code 0
```

Run deliberately **without** `-v` on the console this time and with
output redirected to a report file instead — printing verbose match
output was exactly how this session accidentally leaked real credential
values (Anthropic API key, Discord bot token, graph encryption key) into
its own transcript earlier tonight, during Module 7's work. The report
file was then parsed for finding count only (never printed raw), found
empty (`[]`), and deleted.

**Result: 94 commits scanned (~56.2 MB), zero findings** — same clean
result as Module 3's original audit (85 commits then), confirming
nothing credential-shaped slipped in across every module built since.

The manual review beyond the scanner is step 38's table above, not a
separate pass — the whole point of a *manual* review step, distinct from
the automated one, is to catch exactly the class of thing an automated
scanner's ruleset structurally cannot.

## What's NOT done here — deliberately left to the user

**The repo's GitHub visibility has not been changed.** Flipping a
private repo to public is externally visible, effectively irreversible
in practice (anyone who clones it during the brief public window keeps
their copy even if visibility is reverted), and is exactly the class of
action this project's own standing rule treats as requiring a human
directly confirming it themselves in the moment — not something to do
as a natural continuation of "next roadmap module." Everything steps
36-39 asked for is done and verified; the actual switch is the user's
call, informed by the git-history question above.
