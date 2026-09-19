# Agent capabilities and governance

Single source of truth for Odin's agents: what exists, what each may do,
with which tools, on which systems, at what cost, and how work moves.
Audit date 2026-09-16; implementation status at the end. Owner:
Archangel356291. Everything below applies to **this PC only** unless the
owner adds a system to the allowlist described in §5.

## 1. Audit — what existed before this document

| Agent | Kind | Role | Tools / access | Permissions | Work at audit time |
|---|---|---|---|---|---|
| **Odin** | Claude via `/api/chat` | Conversational core | 21 read-only built-ins (+ opt-in MCP); only writes: `remember_note`, `propose_idea` | Admin: all built-ins + approved MCP · beta: 3 trade tools · Economy: 8 · Deep: all, admin-only | Answering the owner with situational context |
| **Sentinel** | daemon thread, 0 tokens | Security watchdog | `docker_ps`, lockout state, CVE cache — reads | Writes to the activity log only, on change | 5-minute passes |
| **Scout** | tool + container | Web research | `web_search` → private SearXNG (no host port) | Admin-only; results wrapped untrusted; not in Economy | On demand |
| **Learner** | opt-in lite-model call | Memory extraction | `remember_note` | Admin-only; skipped if Odin already remembered | Off unless switched on |
| cyan / green | pixel-room sprites | none recorded at audit time; since assigned as the room's **Engineer** (cyan → `engineering`) and **Learner** (green → `learner`) desks, lit by real task/learn events | — | — | scenery → live indicators |
| **Claude Code** | external session | Engineering | repository, `dev-tools` tests, `docker compose` on this PC, Chrome for verification | Per-session grants; gitleaks pre-commit hook; graphify hook-guard | This work |

**Role coverage found**

1. *Software engineering* — exists **outside the backend**: Claude Code with the owner in the loop, and `evolution_ideas` (chat may only propose; admin approves via PATCH) as the queue. There is deliberately no in-process code-writing agent: Odin modifying Odin from chat would break the read-only principle the whole project rests on. → **extended, not duplicated** (registered as `engineering`, tracked in the task ledger).
2. *Ethical security testing* — **partial**: Sentinel (runtime signals), Docker Scout CVE scan (manual), auth log, gitleaks hook, security tests. Gap: no configuration/posture review, no per-agent spend control. → **Sentinel extended** with a local posture review; no new agent.
3. *Remote monitoring* — **partial**: this PC's containers only. Gap: no owner-authorized target allowlist, no service-level probes. → **Sentinel extended** with `monitoring-targets.json` (deny-by-default, private hosts only) and Docker healthcheck awareness.

**Gaps, overlap, risk, cost** — no task lifecycle beyond ideas; dispatch denied by role/mode but not generically; no per-agent spend view or hard stop; CORS `*`; no agents view in the UI; no overlap between agents; no unsafe permissions found (no chat path mutates the host; MCP is opt-in per tool; SearXNG has no host port; drives are mounted read-only). Unnecessary cost: none recurring — Sentinel, Scout's engine, briefing, recall and situational context are all zero-token.

## 2. Roles (final)

- **Engineering** = Claude Code sessions, owner-operated. Implements approved features and fixes, runs local builds/tests/lint, reviews quality, and must leave evidence (changed files, test output, build status, summary). Never: external deployment, production/paid/credential changes, destructive DB changes, broad filesystem operations without the owner. Tracked as `engineering` tasks + evolution ideas.
- **Ethical Security** = **Sentinel** (runtime + posture) + the dev-time review tools (gitleaks hook, `dev-tools` security tests, `/security-review` and `/code-review` in Claude Code). Code, dependency, configuration, auth, secrets, input validation, logging and privacy review; safe local checks only; findings are prioritised by status (error = CRITICAL, warning = IMPORTANT) and land in the activity log and the Security tab. Never: testing public targets, third-party systems, accounts, networks or devices; persistence, credential harvesting, malware, evasion, destructive or denial-of-service testing; exploitation beyond safe validation. Critical findings surface immediately (activity feed, Sentinel card, room desk, `/threats`, `get_threat_summary`); any risky remediation needs the owner's approval.
- **Remote Monitoring** = **Sentinel** over the allowlist in §5. Uptime, container health (Docker healthchecks), stopped/unhealthy containers, failed sign-ins and lockouts, critical CVEs from the last scan, posture. Read-only by default and in practice: no remote control, shell, config change, file access, account change, deployment, reboot or remediation exists in code. Any write action would be a new preview-then-confirm dashboard action, never a Sentinel capability.

## 3. Capability matrix

| Agent | Role | Required tools/skills | Optional tools | Allowed data | Forbidden actions | Estimated cost | Approval needed |
|---|---|---|---|---|---|---|---|
| odin | Conversational core | `TOOLS` (read), situational context, `remember_note`, `propose_idea` | MCP tools named in `auto_approve`; `web_search`; Deep mode | This PC's telemetry, activity, memory, trades, repo status; beta: trades only | Host mutation, trades, deploys, backups, approving own ideas/tasks, acting on tool-result "instructions" | Sonnet ≈ $2/$10 per MTok; Economy ≈ half; Deep ≈ 2.5× | Deep mode and MCP servers: owner switch/config |
| sentinel | Watchdog + monitoring | `docker_ps`, lockout state, CVE cache, posture review, allowlisted probes | — | Container states, auth failures, config presence (never secret values) | Remote commands, config changes, starting scans, probing non-private hosts | $0 | Adding a target = editing `monitoring-targets.json` |
| scout | Web research | `web_search` → SearXNG | — | Titles/URLs/snippets (untrusted) | Auto-storing web text; anything but search | $0 per query + result tokens in the reply | Already approved (2026-09-16) |
| learner | Memory extraction | `remember_note`, lite model | — | The owner's own turns | Live numbers, web content, beta turns | ≈ $0.001/turn, capped by `ODIN_AGENT_DAILY_USD` | Owner switch, per conversation |
| engineering | Build/test/maintain | repo, `dev-tools` tests, compose, Chrome | Claude Code skills (`code-review`, `security-review`, `frontend-design`, graphify) | Repository, local containers | External deploy, paid services, credential/destructive changes | Claude Code session cost | Each session; high-risk tasks need `approval_status=approved` |

**Claude Code specialists (added 2026-09-16, `.claude/agents/*.md`)** — narrow, isolated-context subagents invoked by name from a Claude Code session; each states a plan, runs its scoped task, and returns a synthesized result. Registered in `AGENT_REGISTRY` so each has a desk, a task queue and a spend line. All are dev-time (owner in the loop) and local-only.

| Agent | Role | Tools | Forbidden | Runtime half |
|---|---|---|---|---|
| `docker_orchestrator` (Dockhand) | compose/Dockerfile changes, rebuilds | Read/Grep/Glob/Edit/Write/Bash — local `docker compose` only | publishing internal ports, writable host mounts, secrets in compose | `deploy-container` action (preview-then-confirm) |
| `tailscale_topology` (Relay) | tailnet diagnosis, MagicDNS, `tailscale serve`/cert, ACL review | Bash read-only tailscale/docker exec | `tailscale up/down/set`, ACL/serve changes, Funnel, peers that aren't this PC — without approval | Tailscale Watchdog task |
| `pihole_guard` (Gatekeeper) | DNS answering, port 53/admin exposure, stack health | Bash read-only docker/nslookup | blocklist/upstream/password changes, restarts, exposing 53/admin | Sentinel HTTPS probe + Docker healthcheck |
| `test_automation` (Proof) | run `dev-tools` tests, write the one needed check | Read/Grep/Glob/Edit/Write/Bash (tests, syntax checks) | weakening assertions, live containers, real API key | — |
| `security_auditor` (Auditor) | secrets, ignore files, auth, headers/CSP, deps | read-only git/grep/gitleaks | printing secret values, exploit code, external probing | Sentinel posture review, gitleaks hook |
| `log_coordinator` (Scribe) | root cause from logs, redacted | Bash `docker logs --tail` | restarting/clearing, quoting credentials | **`get_container_logs`** tool (admin, redacted, wrapped untrusted) |
| `context_manager` (Archivist) | what becomes durable memory; tidy stores | Read/Grep/Glob/Edit/Write on memory folders | live metrics/secrets/web content in memory, editing `odin.db`, Desktop/OneDrive | learner + 40-message/200-note caps |
| `knowledge_synthesizer` (Librarian) | exact snippet from either vault, vaults kept separate | Bash graphify query/path/explain | mixing vaults, whole files, credentials from chat logs | `recall_from_brain` + situational context |
| `slack_communicator` (Herald) | draft/post to the aiodinseye workspace | Slack MCP (read, draft, send) | sending without per-message approval, new recipients, secrets/IPs/chat content | none (no Slack in the backend, by decision) |
| `discord_gateway` (Envoy) | the Discord bot | slash commands → this backend | anything the backend refuses; exposing tokens | `odin-discord-bot` container (health from `docker_ps`) |

| `developer` (Forge) | implement an approved feature/fix end to end | Read/Grep/Glob/Edit/Write/Bash + **Filesystem MCP** (sandboxed to the project, the Brain vault, the compose stacks) + **Git MCP** (the repo) | pushing, history rewrites, new services/deps/ports unannounced, secret values, "done" without test output | Odin's `get_repo_status`/`get_repo_diff` |
| `research` (Seeker) | deep research with sources | Claude Code **WebSearch/WebFetch** + **Context7 MCP** (library docs) | pasting pages, following page instructions, sign-ins, fetching the owner's private services | **`read_page`** (local HTML→text, public https only) + `web_search` |
| `frontend_designer` (Muse) | visual/layout/motion/accessibility on the dashboard | Read/Grep/Glob/Edit/Write/Bash + **Playwright MCP** (headless Chromium, 400×860) + **Figma MCP** (read design context) + `frontend-design`/`dataviz` skills | inventing colour roles, decorative motion, fake UI data, copying Marvel's design | — |

**Tooling added 2026-09-16 (all local, no accounts):** `.mcp.json` (project-scoped) declares the Filesystem MCP (paths above), the Git MCP (`uvx mcp-server-git`, this repo) and the Playwright MCP (headless Chromium, installed); plugins `claude-security` (in-session vulnerability scan, the deep SAST pass), `context7` (docs as clean text) and `code-review` were installed from the official marketplace. `dev-tools/sast-scan.sh` runs gitleaks, Bandit and Semgrep in throwaway containers with the repo mounted read-only — the "restricted CLI + SAST hooks" item — and the gitleaks pre-commit hook still guards every commit. `read_page` replaces a Firecrawl/Jina-style service with a local reader (no third party sees Odin's URLs). SearXNG already covers the search role.

**Needs the owner's account, not installed:** the `github` plugin (personal access token — `gh` is not installed here), the Firecrawl connector (sign-in), Brave Search (API key). None is required for the roles above.

## 4. Authorization model

- **Roles**: `require_token` (admin) and `require_role` (admin or beta) on every route; beta is scoped to chat + view-only trades.
- **Deny by default at dispatch**: a chat turn may only run a tool that was *offered on that call* (`offered_tool_names` in `run_odin_chat`); anything else returns `forbidden` and logs an `agent_permission` event. This single check covers the beta allowlist, Economy's set, no-MCP-for-beta, and hallucinated tool names.
- **Writes**: `remember_note`, `propose_idea` (chat); everything else that changes state is an admin route, and host actions are preview-then-confirm with a server token.
- **External data**: MCP and web results are wrapped `<untrusted_external_data>`; tool results are never instructions.
- **Secrets**: live in the untracked `.env`; Sentinel's posture check reports token *length*, never a value; nothing logs or displays a secret; gitleaks runs on every commit.
- **Tasks** (§6) carry `authorized_scope`, `allowed_tools`, `risk_level`, `approval_status`; a high-risk task cannot enter `in_progress` without `approved`.

## 5. Approved scope (authoritative)

| Role | In scope | Explicitly out of scope |
|---|---|---|
| All | This Windows PC; its Docker containers (`odin-backend`, `odin-discord-bot`, `odin-searxng`, the pihole stack, the jellyfin stack); the Odin repository; the owner's dashboard and Discord (allowlisted user IDs); `D:\ultron's Brain&Knowledge` | Tailnet devices other than this PC (phones, the pihole/jellyfin *tailscale sidecars* as peers), any Pi/M715q/M920q/NAS, any public host, any third-party account, network or API |
| Monitoring probes | Entries in `D:\ultron's Brain&Knowledge\monitoring-targets.json` (private hosts, or names directly under the owner's tailnet suffix `ODIN_TAILNET_SUFFIX`; currently Odin's port, `https://jellyfin.tailc5bde9.ts.net/health`, `https://pihole.tailc5bde9.ts.net/admin/`, SearXNG `/healthz`) | Pi-hole DNS itself (watched via its Docker healthcheck + autoheal); anything not listed |
| Security review | The repository, this deployment's configuration, the running containers' images (CVE scan, manual) | Any target not owned by the owner; any active exploitation |
| Web access | SearXNG on the compose network; Anthropic API; Fish Audio TTS; Docker Hub for Scout scans | Any other outbound service without the owner's approval |

Adding to scope = adding an entry to the allowlist file (monitoring) or a line here (everything else), by the owner.

## 6. Coordination — the task ledger

`agent_tasks` (SQLite) with `task_uid`, `agent`, `objective`, `acceptance_criteria`, `authorized_scope`, `allowed_tools`, `risk_level`, `approval_status`, `status`, `progress`, `evidence`, `review_status`, `blocker`, timestamps.

Lifecycle: `created → assigned → acknowledged → in_progress → blocked | awaiting_review | completed | failed | cancelled` (`TASK_TRANSITIONS`). Rules enforced in code: illegal jumps rejected; `completed` requires evidence; `risk_level=high` requires `approval_status=approved` before `in_progress`; an open duplicate objective for the same agent is refused (409); every transition is an `agent_task` activity entry. Routes (admin-only): `GET /api/agents`, `GET/POST /api/agents/tasks`, `PATCH /api/agents/tasks/<uid>`. Chat has the read-only `get_agent_status`; it cannot create or move tasks. The Odin tab's **Agents** card shows each agent's role, health, last update, current task, today's spend against its cap, tools and forbidden actions.

Routing: coding → `engineering`; security/monitoring → `sentinel`; research → `scout`; the owner assigns (dashboard/API). Escalation: permission violations (`agent_permission`), budget stops (`agent_budget`), Sentinel findings (`sentinel`) all land in the activity feed with severity and light the Sentinel desk.

## 7. Budget, security and safety controls

- **Budgets**: global daily token budget (`ODIN_LLM_DAILY_TOKEN_BUDGET`), beta lifetime cap ($1), and new **per-agent daily USD caps** (`ODIN_AGENT_DAILY_USD="odin=5.00,learner=0.25"`): chat returns 429 and the learner pauses with an `agent_budget` event once over. Usage is logged per agent and per model at real prices; `/api/chat/usage` shows `by_agent`.
- **Rate limits**: `/api/chat` per-minute limit; Sentinel probes once per pass with a 5 s timeout; SearXNG has one internal caller.
- **Dry run**: host actions already are (preview → token → confirm). Tasks can be created and reviewed without any agent acting.
- **Allowlists**: tools per role/mode, MCP tools by name, monitoring targets by file, Discord users by ID, storage paths by env. **Deny by default** everywhere above.
- **Audit**: `activity_log` (`agent_task`, `agent_permission`, `agent_budget`, `sentinel`, `learned`, actions, scans) with severity; chat transcripts in `chat logs/`; usage in `llm_usage`.
- **User controls**: Settings switches (Economy, Deep, Learn, voice, auto-refresh); `ODIN_SENTINEL_INTERVAL_SECONDS=0` disables Sentinel; removing `ODIN_SEARXNG_URL` disables Scout; revoking a token or Discord ID cuts access; cancelling a task is a transition.
- **Safe failure**: every scheduler swallows errors and continues; probes and learners degrade to logged events; nothing escalates its own access.

## 8. Implementation status (2026-09-16)

| Item | Status |
|---|---|
| Registry, `/api/agents`, `get_agent_status`, Agents card | done |
| Task ledger + lifecycle enforcement + audit | done |
| Deny-by-default dispatch + `agent_permission` events | done |
| Per-agent usage + `ODIN_AGENT_DAILY_USD` caps | done (caps unset by default; set in `.env` to enforce) |
| Sentinel posture review (CORS, TLS, token length, interval) | done |
| Monitoring allowlist, private-host rule, Docker-healthcheck awareness | done; file at `D:\ultron's Brain&Knowledge\monitoring-targets.json` |
| Tests | `dev-tools/test_agents.py` |
| Admin token rotated to 48 random characters; `ODIN_ALLOWED_ORIGIN` pinned to the dashboard origin | done 2026-09-16 (owner-approved); Sentinel's two posture findings cleared on its next pass |
| HTTPS everywhere the owner reaches: Odin (Tailscale cert), Jellyfin and Pi-hole via `tailscale serve` in their sidecars (`https://jellyfin.tailc5bde9.ts.net`, `https://pihole.tailc5bde9.ts.net/admin/`); URLs recorded in `.env` (`ODIN_PUBLIC_URL`, `JELLYFIN_URL`, `PIHOLE_URL`) and monitored by Sentinel | done 2026-09-16. SearXNG stays plain HTTP on the private compose bridge (no host port; traffic never leaves this PC) — the standard choice, noted rather than hidden |
| Specialist subagents (`.claude/agents/`: Dockhand, Relay, Gatekeeper, Proof, Auditor, Scribe, Archivist, Librarian, Herald, Forge, Seeker, Muse) registered with desks; `get_container_logs` and `read_page` runtime tools | done 2026-09-16 |
| Tooling: Filesystem/Git/Playwright MCP, `claude-security` + `context7` + `code-review` plugins, sandboxed SAST (`dev-tools/sast-scan.sh`), headless Chromium installed | done 2026-09-16; verified with `claude mcp list`: `filesystem ✔ git ✔ playwright-headless ✔` (registered at user scope in `~/.claude.json` so they connect from any start directory; `.mcp.json` carries the same definitions for other clones), plugin `playwright ✔ context7 ✔ figma ✔`. Firecrawl shows "needs authentication" — owner sign-in, optional |
| Phone-width verification | done 2026-09-16 via headless Chromium at 400×860 (signed in): Home overflow fixed, `/api/dev/repos` 400 fixed, no console errors |
| Not done, needs the owner | setting real per-agent caps in `.env`; the `github` plugin (needs a token), Firecrawl (sign-in), Brave Search (key) |

## Blueprint agents added 2026-09-16 (subagent_blueprint.md gaps)

Audited Odin's registry against `C:\Ultron Project\subagent_blueprint.md`.
Six of the blueprint's eight roles were already covered (Home Lab Monitoring →
Sentinel/Dockhand; Coding Assistant → Forge/Engineering/Proof; Code Repository
Librarian → Librarian; Records Keeper → Archivist; Security Watch Sentinel →
Sentinel). Three gaps were filled:

| Agent | Kind | Role | Tools | Forbidden | Scope |
|---|---|---|---|---|---|
| **Oracle** (`market_analyst`) | tool, 0-token | Read-only crypto market analyst (blueprint #2) | `get_crypto_market` (CoinGecko free public API, cached ~60s), `get_trades`/`get_trade_summary` | placing/recommending trades, any buy/sell/transfer, calling prices advice, exchange/order-book/private-key access | public spot prices + the owner's own manual ledger |
| **Tally** (`stats_tracker`) | tool, 0-token | Daily efficiency insights (blueprint #8) | `get_stats_rollup` (read-only aggregation over `llm_usage`, agent tasks, activity log, docker) | new data collection, per-user profiling, storing live metrics as memory | this backend's own local records |
| **Redcell** (`ethical_hacking`) | Claude Code subagent | Authorized ethical-hacking **lab** agent (blueprint #3) | `Read`, `Grep`, `Glob` over the lab vault only. **Scanning tools (nmap, sqlmap, etc.) stay UNWIRED until the lab plan is approved** | any scan/exploit/probe of any host (incl. lab targets) before an approved trial, any non-lab/public/production/unknown system, malware/persistence/evasion/DoS, storing secrets or payloads | ONLY `D:\Ethical Hacking Lab` systems the owner authorizes; see `D:\Ethical Hacking Lab\docs\AGENT_LAB_GOVERNANCE.md` |

**Decisions & boundaries:**
- Oracle adds a **read-only** live price feed (owner-approved 2026-09-16),
  reversing the earlier no-feed default for display/analysis only. Module 11's
  financial-action boundary is **unchanged**: no tool buys, sells, or moves
  anything; `get_crypto_market` is a `get_`-prefixed read like `get_trades`,
  and `test_no_financial_action_tools.py` still passes.
- The blueprint's Crypto **order-book / exchange APIs** and the Ethical
  Hacking agent's **active scanners** were deliberately **not** wired — the
  first would cross the financial boundary, the second is gated behind the
  Ethical Hacking Lab approval plan.
- Coverage extensions not needing a new agent: Records Keeper OCR and the
  Repository Librarian's vector search remain future work under Archivist /
  Librarian; the Home Lab Monitoring agent's Prometheus/Netdata hooks remain
  future work under Sentinel.
- Checks: `dev-tools/test_blueprint_agents.py` (new), `test_agents.py` and
  `test_no_financial_action_tools.py` updated/passing. All three have desks in
  Odin's corner (Oracle = bitcoin/coin, Tally = gold/chart, Redcell =
  crimson/crosshair).
