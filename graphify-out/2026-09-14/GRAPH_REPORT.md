# Graph Report - Ultron Project  (2026-09-14)

## Corpus Check
- 35 files · ~60,014 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 6 file(s) not represented in the graph (top: (none) 6)

## Summary
- 487 nodes · 768 edges · 71 communities (25 shown, 40 thin omitted)
- Extraction: 94% EXTRACTED · 6% INFERRED · 0% AMBIGUOUS · INFERRED: 46 edges (avg confidence: 0.85)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `37f3eaf0`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- bot.py
- discord/__init__.py
- anthropic/__init__.py
- ultron-discord-bot (Thin Remote-Control Layer)
- run_ultron_chat
- View
- route
- ClientSession
- trades
- ultron-backend README (Backend API Reference)
- action_backup
- Beta Testers Roster & Add Process
- require_role
- _get_db_connection
- _fifo_engine
- action_deploy_container
- fake_pkgs/ (drop-in fake SDKs)
- app.py
- _status_data
- MCP Support (External Tool/Plugin System)
- test_mcp_server.py
- test_tts_streaming.py
- UltronBot
- wrapper
- test_memory.py
- Ultron Dashboard Design Spec
- Action Endpoints (backup, deploy-container)
- aiultronproject Slack Workspace
- add_cors_headers
- Preview-Then-Confirm Action Pattern
- _load_mcp_config
- _split_platform_paths
- _fifo_engine() (Shared FIFO Trade Computation)
- The Importer (Obsidian plugin)
- Ultron Project CLAUDE.md (graphify + vault instructions)
- docker-compose.yml (Compose Orchestration)
- ultron Bridge Network
- Coding Sub-Agent (Emergent, Not In Original Spec)
- Crypto/Trade Record & Tax Agent
- Ethical Hacking Agent (Refused)
- Home Lab Monitor & Command Router Agent
- Investment/Financial Predictive Agent (Refused, Reinterpreted)
- LyraWolf (Contributor)
- Archangel356291 (Project Owner)
- dev-tools (Testing Infrastructure)
- Explicit Financial/Legal Boundaries
- ultron-backend (Flask Backend)
- Nothing Works Until Explicitly Configured
- One Source of Truth Per Piece of Logic
- Real-Dependency Testing Approach
- Ultron (Personal AI Home Lab System)
- Pi Phase 2 Plan (Preview-Then-Confirm Extended To Pi)
- /api/activity (Persistent Activity Log)
- app.py (Flask Backend Entrypoint)
- /api/security/auth-log
- /api/security/cve-scan (Docker Scout CVE Scan)
- /api/dev/* (Development Tab Git Status/Diff)
- Flask (>=3.0,<4.0)
- psutil (>=6.0,<7.0)
- pywin32 (==306, Windows only)
- WMI (==1.5.1, Windows only)
- _fish_audio_tts
- _start_memory_trend_scheduler
- Exception
- route

## God Nodes (most connected - your core abstractions)
1. `Interaction` - 22 edges
2. `require_token()` - 20 edges
3. `require_auth()` - 19 edges
4. `format_error_embed()` - 17 edges
5. `_get_db_connection()` - 15 edges
6. `_json_result()` - 14 edges
7. `backend_get()` - 13 edges
8. `require_role()` - 10 edges
9. `deploy_command()` - 10 edges
10. `ConfirmActionView` - 9 edges

## Surprising Connections (you probably didn't know these)
- `ultron-discord-bot Service (Docker Compose)` --shares_data_with--> `ultron-discord-bot (Thin Remote-Control Layer)`  [INFERRED]
  docker-compose.yml → README.md
- `Real Safeguards, Not Just Docs` --conceptually_related_to--> `Cost Controls (Budget, Spend Cap, Rate Limit, Caching)`  [INFERRED]
  README.md → ultron-backend/README.md
- `ultron-backend Service (Docker Compose)` --shares_data_with--> `ultron-backend README (Backend API Reference)`  [INFERRED]
  docker-compose.yml → ultron-backend/README.md
- `export_command()` --references--> `Choice`  [EXTRACTED]
  ultron-discord-bot/bot.py → dev-tools/fake_pkgs/discord/__init__.py
- `Beta Testers Roster & Add Process` --references--> `Ultron Discord Bot README`  [EXTRACTED]
  ultron-backend/BETA-TESTERS.md → ultron-discord-bot/README.md

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Fake SDKs built to match real SDK shape** — dev_tools_readme_fake_anthropic, dev_tools_readme_fake_discord, dev_tools_readme_fake_aiohttp, ultron_backend_requirements_anthropic, ultron_discord_bot_requirements_discordpy, ultron_discord_bot_requirements_aiohttp [EXTRACTED 1.00]
- **Preview-Then-Confirm Pattern Across Current and Planned Actions** — readme_preview_then_confirm_pattern, ultron_backend_readme_action_endpoints, ultron_backend_pi_setup_phase2_plan [INFERRED 0.80]
- **MCP Discovery/Execution Separation Security Model** — project_summary_for_claude_code_mcp_support, readme_mcp_opt_in_principle, ultron_backend_readme_mcp_external_tools [INFERRED 0.85]
- **Original Four-Agent Spec Plus Emergent Fifth** — project_summary_for_claude_code_ethical_hacking_agent, project_summary_for_claude_code_investment_agent, project_summary_for_claude_code_crypto_trade_agent, project_summary_for_claude_code_home_lab_monitor_agent, project_summary_for_claude_code_coding_subagent [INFERRED 0.85]

## Communities (71 total, 40 thin omitted)

### Community 0 - "bot.py"
Cohesion: 0.09
Nodes (56): button, choices, command, describe, Interaction, Fake interaction for testing command and button handlers directly., event, ask_command() (+48 more)

### Community 1 - "discord/__init__.py"
Cohesion: 0.06
Nodes (15): Bot, ButtonStyle, Embed, File, _Followup, HTTPException, Intents, _InteractionResponse (+7 more)

### Community 2 - "anthropic/__init__.py"
Cohesion: 0.09
Nodes (20): Anthropic, APIConnectionError, APIError, APIStatusError, APITimeoutError, AuthenticationError, BadRequestError, ContentBlock (+12 more)

### Community 3 - "ultron-discord-bot (Thin Remote-Control Layer)"
Cohesion: 0.07
Nodes (26): demo(), _queue_reply(), Self-check for the beta-tester $1 spend cap (ULTRON_BETA_MAX_SPEND_USD) and the…, ultron-discord-bot Service (Docker Compose), Bug: Discord backend_get Showed Raw Error Text, Bug: Discord Field-Truncation Off-By-N, Bug: Tool-Registration Ordering (get_llm_usage NameError Risk), Config Value Hardening (Min-1 Clamp on Token/Rate Limits) (+18 more)

### Community 4 - "run_ultron_chat"
Cohesion: 0.08
Nodes (28): Exception, _add_cache_breakpoint(), _ensure_mcp_discovered(), get_mcp_tools_and_dispatch(), _log_llm_usage(), _make_mcp_tool_handler(), handler(), _mcp_call_tool() (+20 more)

### Community 5 - "View"
Cohesion: 0.08
Nodes (8): app_commands, Button, Choice, CommandTree, Matches @discord.ui.button(...). The fake doesn't need the full component-…, ui, decorator(), View

### Community 6 - "route"
Cohesion: 0.11
Nodes (26): route, chat_usage(), connections(), containers(), _containers_data(), dashboard(), delete_trade(), docker_stats() (+18 more)

### Community 7 - "ClientSession"
Cohesion: 0.12
Nodes (7): ClientError, ClientSession, ClientTimeout, _MockResponse, Exception, Minimal fake of 'aiohttp' — enough to test bot.py's backend_get/backend_chat…, Test double: configure `.script` with a queue of _MockResponse objects (or an…

### Community 8 - "trades"
Cohesion: 0.20
Nodes (10): add_trade(), get_trades(), Returns (normalized_dict, None) or (None, error_message)., Raw transaction ledger as CSV text., Per-disposal FIFO tax report as CSV text — one row per sell-vs-buy-lot match,…, _tax_lots_to_csv(), trades(), trades_export() (+2 more)

### Community 9 - "ultron-backend README (Backend API Reference)"
Cohesion: 0.17
Nodes (14): Master Index (Obsidian Vault Root), ultron-backend Service (Docker Compose), Bug: Startup Script ANTHROPIC_API_KEY UX Trap, Project & Conversation Summary (History/Rationale Doc), Claude Code (Anthropic) - AI Pair-Programming Assistant, README.md (Top-level Architecture & Principles), ultron-backend index (_index.md), Bug: Beta Testers Couldn't See Own Spend (+6 more)

### Community 10 - "action_backup"
Cohesion: 0.27
Nodes (10): action_backup(), _backup_preview(), _consume_action_token(), _dir_size_bytes(), _new_action_token(), _prune_expired_tokens_locked(), Pops and returns (params, None) on success, or (None, error_message). Tokens…, _run_backup() (+2 more)

### Community 11 - "Beta Testers Roster & Add Process"
Cohesion: 0.27
Nodes (11): $1.00 Lifetime Beta Spend Cap (ULTRON_BETA_MAX_SPEND_USD), file:// Origin fetch() Bug (mobile Chrome Connect button), Tailscale Grants/ACLs (autogroup:self), Tailscale Remote Access, Why Tailscale Instead of Raw WireGuard, Beta Invite Message, Beta Launch Checklist, Beta Tester Guide (+3 more)

### Community 12 - "require_role"
Cohesion: 0.28
Nodes (9): _beta_tester_spend_usd(), chat(), _check_rate_limit(), Returns None if the request is allowed, or an error message if the caller…, Lifetime spend for one beta tester, in dollars. Returns 0.0 on any read failure…, Admin or beta_tester. Use only on endpoints in the beta tester's allowed scope…, require_role(), tts() (+1 more)

### Community 13 - "_get_db_connection"
Cohesion: 0.25
Nodes (9): activity(), distill_activity_trends(), _get_db_connection(), get_recent_activity(), _init_db(), Sums input+output tokens (real spend) for calls logged today (local date,…, Best-effort, like log_activity — this runs unattended on a background timer…, remember_note() (+1 more)

### Community 14 - "_fifo_engine"
Cohesion: 0.20
Nodes (10): _fifo_engine(), get_trade_summary(), get_trade_tax_lots(), Best-effort date -> integer day count, for holding-period math. Never raises;…, The one place FIFO matching happens. Returns both an aggregated per-asset view…, Simplified FIFO realized gain/loss per asset — the aggregated view. See…, Per-disposal detail: each row is one sell matched against one consumed buy lot,…, _trade_date_to_epoch_days() (+2 more)

### Community 15 - "action_deploy_container"
Cohesion: 0.12
Nodes (19): action_deploy_container(), docker_ps(), log_activity(), _parse_scout_sarif(), Runs `docker scout cves` for one image. Returns a result dict — never raises.…, Scans the images of currently running containers. Capped to CVE_SCAN_MAX_IMAGES…, Validates and normalizes a deploy-container request body. Returns (params,…, Best-effort logging — never raises. A logging failure (disk full, permissions,… (+11 more)

### Community 16 - "fake_pkgs/ (drop-in fake SDKs)"
Cohesion: 0.22
Nodes (9): fake_pkgs/aiohttp (aiohttp client fake), fake_pkgs/anthropic (scriptable Anthropic client fake), fake_pkgs/discord (Discord SDK fake), fake_pkgs/ (drop-in fake SDKs), test_mcp_server.py (real protocol-compliant local MCP server), Why this exists as a separate folder (test against real-like dependencies), anthropic (>=1.0.0,<2.0.0), aiohttp (+1 more)

### Community 17 - "app.py"
Cohesion: 0.20
Nodes (13): dev_repo_diff(), dev_repos(), _find_repo_dir(), get_repo_diff(), get_repo_status(), Ultron home lab monitoring backend. Exposes a small JSON API that the dashboard…, Runs a read-only git command in repo_path. Returns (stdout, error) — never…, Matches only against the pre-configured repo basenames — a caller can never… (+5 more)

### Community 18 - "_status_data"
Cohesion: 0.25
Nodes (9): get_cpu_temp_c(), get_uptime_str(), pending_os_updates(), Best-effort CPU temperature read. Returns None if unavailable — which, on…, Count of pending OS updates. Real implementation on both platforms: Windows…, status(), _status_data(), systems() (+1 more)

### Community 19 - "MCP Support (External Tool/Plugin System)"
Cohesion: 0.29
Nodes (7): Bug: MCP Empty Notification Response Mishandled, Bug: MCP Response-Size Cap Applied At Wrong Layer, dev-tools/fake_pkgs (Scriptable Fakes for anthropic/discord/aiohttp), MCP Support (External Tool/Plugin System), dev-tools/test_mcp_server.py (Real Protocol-Strict MCP Test Server), MCP Opt-In At the Tool Level, Not Server Level, External Tools (MCP) Section

### Community 20 - "test_mcp_server.py"
Cohesion: 0.47
Nodes (5): jsonrpc_error(), jsonrpc_result(), mcp_endpoint(), route, A real MCP server for testing app.py's MCP client against genuine JSON-RPC…

### Community 21 - "test_tts_streaming.py"
Cohesion: 0.50
Nodes (3): demo(), _fake_streaming_tts(), Self-check for the /api/tts streaming fix (Module 1 of the roadmap: "text…

### Community 23 - "wrapper"
Cohesion: 0.50
Nodes (5): Constant-time-ish token check against admin and every registered beta tester.…, wrapper(), wrapper(), _resolve_role(), _touch_presence()

### Community 25 - "Ultron Dashboard Design Spec"
Cohesion: 0.67
Nodes (3): Chamfered-Corner UI Design (45° cut panels), --line Panel Border Color Variable, Ultron Dashboard Design Spec

### Community 68 - "_start_memory_trend_scheduler"
Cohesion: 0.67
Nodes (3): Runs distill_activity_trends() once now, then every 24h, in a daemon thread so…, _start_memory_trend_scheduler(), _loop()

## Knowledge Gaps
- **43 isolated node(s):** `ButtonStyle`, `file:// Origin fetch() Bug (mobile Chrome Connect button)`, `Tailscale Grants/ACLs (autogroup:self)`, `Ultron Discord Bot README`, `anthropic (>=1.0.0,<2.0.0)` (+38 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 212 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **40 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **What connects `ButtonStyle`, `file:// Origin fetch() Bug (mobile Chrome Connect button)`, `Tailscale Grants/ACLs (autogroup:self)` to the rest of the system?**
  _43 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `bot.py` be split into smaller, more focused modules?**
  _Cohesion score 0.08755760368663594 - nodes in this community are weakly interconnected._
- **Should `discord/__init__.py` be split into smaller, more focused modules?**
  _Cohesion score 0.05689900426742532 - nodes in this community are weakly interconnected._
- **Should `anthropic/__init__.py` be split into smaller, more focused modules?**
  _Cohesion score 0.08571428571428572 - nodes in this community are weakly interconnected._
- **Should `ultron-discord-bot (Thin Remote-Control Layer)` be split into smaller, more focused modules?**
  _Cohesion score 0.0735632183908046 - nodes in this community are weakly interconnected._
- **Should `run_ultron_chat` be split into smaller, more focused modules?**
  _Cohesion score 0.082010582010582 - nodes in this community are weakly interconnected._
- **Should `View` be split into smaller, more focused modules?**
  _Cohesion score 0.08307692307692308 - nodes in this community are weakly interconnected._