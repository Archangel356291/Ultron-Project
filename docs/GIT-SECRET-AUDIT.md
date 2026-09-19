# Git secret audit (Module 3) — 2026-09-14

## Result: no real secrets found in git history. No history rewrite performed.

Full-history scan with [gitleaks](https://github.com/gitleaks/gitleaks)
v8.30.1 (local, free — installed via `winget install --id Gitleaks.Gitleaks -e`):

```
gitleaks detect --source . --log-opts="--all"
```

85 commits scanned (~49.6 MB). **2 findings, both verified false positives:**

| File | Rule | What it actually is |
|---|---|---|
| `.obsidian/plugins/terminal/main.js` | `generic-api-key` | Minified third-party Obsidian plugin bundle — high-entropy variable names (`t.TwoKeyMap`, etc.) triggering the generic heuristic. Not this project's code, not a secret. |
| `graphify-out/cache/stat-index.json` | `generic-api-key` | graphify's own SHA-256 content-hash cache (`"remote-access.md": "b286b35d..."`) — a hash of a file's content, used for change detection, not a credential. |

**Targeted checks beyond gitleaks' generic ruleset** (in case something
secret-shaped slipped past the heuristics without matching a pattern):

- `git log --all --full-history --diff-filter=A -- .env` → **empty**. `.env`
  was never committed, at any point in this repo's history.
- `git log --all --full-history --diff-filter=A -- "*.db" "*.db*"` → **empty**.
  `odin.db` (holds trade/financial records) was never committed.
- Searched every filename ever added, for anything credential-shaped
  (`.env`, `credential`, `secret`, `.pem`, `.key`, `id_rsa`, `id_ed25519`) →
  one hit, an Obsidian vault note *about* a historical bug
  (`start-bot.ps1` failing to load `.env`) — documentation of a bug, not a
  leaked value. Content verified directly, no real secret inside it.

**Conclusion:** nothing to remove. The roadmap's step 7
(`git filter-repo` history rewrite) is conditional on step 6 finding
something — since nothing real was found, performing a destructive,
force-pushed history rewrite would be doing real, irreversible work
(and asking for a force-push the user would need to separately confirm)
to fix a problem that doesn't exist. Skipped, deliberately.

## Ongoing: gitleaks as a mandatory pre-commit gate

`.gitleaks.toml` — extends gitleaks' default ruleset (doesn't replace
it), with a **path-scoped** allowlist for the two verified false
positives above. Deliberately not a content/regex allowlist (e.g. "any
64-char hex string") — that would also hide a real hex-shaped secret,
many of which are exactly that shape.

`.githooks/pre-commit` — runs `gitleaks protect --staged` before every
commit. **Fails closed**: if gitleaks isn't installed, the commit is
blocked with an install instruction, rather than silently skipping the
scan (a secret scanner that's quietly disabled is worse than no
scanner — it looks protected and isn't).

Verified against both directions, not just assumed to work:
- A commit staging a realistic-looking fake AWS secret was genuinely
  blocked (exit 1, no commit created).
- (Note while testing: AWS's own textbook documentation example key,
  `AKIAIOSFODNN7EXAMPLE`, is deliberately allowlisted by gitleaks itself
  to avoid flagging docs that use it — don't mistake that for the hook
  not working if you ever re-test with that specific value.)

**One-time setup required after cloning this repo** — git hooks live in
the untracked `.git/hooks/` directory by default, so they don't travel
with a clone on their own. This repo's hook is tracked at
`.githooks/pre-commit` instead, activated per-clone with:

```
git config core.hooksPath .githooks
```

This was run once already on this machine (recorded in local
`.git/config`, itself untracked) — a fresh clone anywhere else needs to
run it again. Consider adding this to whichever setup doc a new
contributor reads first (`BETA-LAUNCH-CHECKLIST.md` or similar) if this
project ever gets a second contributor with commit access.

## Before any future open-source visibility change (Module 12 gate)

Re-run the full-history scan one more time, immediately before flipping
the repo's visibility — not just relying on the pre-commit hook having
caught everything incrementally since this audit:

```
gitleaks detect --source . --log-opts="--all" -c .gitleaks.toml -v
```

If it reports anything beyond the two allowlisted paths above, stop and
investigate before proceeding — don't allowlist a new path without
verifying what it actually is first, the same way both entries above
were verified by hand before being added.
