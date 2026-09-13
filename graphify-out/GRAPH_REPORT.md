# Graph Report - Ultron AI Project  (2026-09-12)

## Corpus Check
- Corpus is ~36,133 words - fits in a single context window. You may not need a graph.

## Summary
- 441 nodes · 739 edges · 38 communities (22 shown, 10 thin omitted)
- Extraction: 97% EXTRACTED · 3% INFERRED · 0% AMBIGUOUS · INFERRED: 24 edges (avg confidence: 0.85)
- Token cost: 0 input · 178,496 output

## Community Hubs (Navigation)
- Discord Bot Commands
- API Surface & Dashboard Client
- Fake Discord Core (UI/Embed)
- Fake Anthropic SDK
- MCP Tool Discovery
- Fake Discord Slash Commands
- Backup & Deploy Actions
- Testing Infra & Remote Access
- Preview/Confirm Pattern
- Fake aiohttp Client
- Auth Tokens & Status Routes
- Trade Activity & DB Access
- Trade CRUD & Export
- FIFO Tax-Lot Engine
- System Monitoring (CPU/Uptime)
- Container CVE Scanning
- Project Overview (README)
- Git Repo Diff/Status
- Dev-Tools Test MCP Server
- Docker Containers
- Chat Rate Limiting
- Discord Bot Lifecycle
- Windows/Linux Platform Support
- Trade Export (Cross-Repo)
- MCP Config Loading
- Beta Launch Checklist
- Obsidian Welcome Note
- Config Warning
- Task Scheduler Startup
- psutil Dependency
- Forget Command Doc
- Require Auth Doc

## God Nodes (most connected - your core abstractions)
1. `Interaction` - 21 edges
2. `require_token()` - 21 edges
3. `POST /api/chat (Ultron's brain)` - 20 edges
4. `require_auth()` - 18 edges
5. `format_error_embed()` - 16 edges
6. `_json_result()` - 13 edges
7. `backend_get()` - 12 edges
8. `_get_db_connection()` - 11 edges
9. `apiGet()` - 11 edges
10. `deploy_command()` - 10 edges

## Surprising Connections (you probably didn't know these)
- `previewDeploy()` --semantically_similar_to--> `/deploy command`  [INFERRED] [semantically similar]
  ultron-dashboard.html → ultron-discord-bot/README.md
- `previewBackup()` --semantically_similar_to--> `/backup command`  [INFERRED] [semantically similar]
  ultron-dashboard.html → ultron-discord-bot/README.md
- `export_command()` --references--> `Choice`  [EXTRACTED]
  ultron-discord-bot/bot.py → dev-tools/fake_pkgs/discord/__init__.py
- `Read-only by default, everywhere` --rationale_for--> `POST /api/chat (Ultron's brain)`  [EXTRACTED]
  README.md → ultron-backend/README.md
- `Destructive host actions require a human-confirmed token` --rationale_for--> `POST /api/actions/backup`  [EXTRACTED]
  README.md → ultron-backend/README.md

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Preview-then-confirm action pattern across backend, dashboard, and bot** — ultron_backend_readme_preview_confirm_pattern, ultron_backend_readme_api_actions_backup, ultron_backend_readme_api_actions_deploy_container, ultron_discord_bot_readme_backup_cmd, ultron_discord_bot_readme_deploy_cmd, ultron_dashboard_previewbackup, ultron_dashboard_previewdeploy [EXTRACTED 1.00]
- **MCP opt-in security model participants** — ultron_backend_readme_mcp_security_model, ultron_backend_readme_api_mcp_servers, dev_tools_readme_test_mcp_server, ultron_dashboard_loadmcpservers, ultron_discord_bot_readme_mcp_cmd [EXTRACTED 1.00]
- **Fake SDKs built to match real SDK shape** — dev_tools_readme_fake_anthropic, dev_tools_readme_fake_discord, dev_tools_readme_fake_aiohttp, ultron_backend_requirements_anthropic, ultron_discord_bot_requirements_discordpy, ultron_discord_bot_requirements_aiohttp [EXTRACTED 1.00]

## Communities (38 total, 10 thin omitted)

### Community 0 - "Discord Bot Commands"
Cohesion: 0.09
Nodes (54): button, choices, command, describe, Interaction, Fake interaction for testing command and button handlers directly., event, ask_command() (+46 more)

### Community 1 - "API Surface & Dashboard Client"
Cohesion: 0.05
Nodes (48): Read-only by default, everywhere, ANTHROPIC_API_KEY (enables chat), GET /api/activity, POST /api/chat (Ultron's brain), GET /api/chat/usage, GET /api/dev/repos/<repo>/diff, GET /api/dev/repos, GET /api/health (+40 more)

### Community 2 - "Fake Discord Core (UI/Embed)"
Cohesion: 0.06
Nodes (15): Bot, ButtonStyle, Embed, File, _Followup, HTTPException, Intents, _InteractionResponse (+7 more)

### Community 3 - "Fake Anthropic SDK"
Cohesion: 0.10
Nodes (17): Anthropic, APIConnectionError, APIError, APIStatusError, APITimeoutError, AuthenticationError, BadRequestError, ContentBlock (+9 more)

### Community 4 - "MCP Tool Discovery"
Cohesion: 0.08
Nodes (28): _add_cache_breakpoint(), _ensure_mcp_discovered(), get_mcp_servers(), get_mcp_tools_and_dispatch(), _log_llm_usage(), _make_mcp_tool_handler(), handler(), _mcp_call_tool() (+20 more)

### Community 5 - "Fake Discord Slash Commands"
Cohesion: 0.08
Nodes (8): app_commands, Button, Choice, CommandTree, Matches @discord.ui.button(...). The fake doesn't need the full component-…, ui, decorator(), View

### Community 6 - "Backup & Deploy Actions"
Cohesion: 0.14
Nodes (24): after_request, action_backup(), action_deploy_container(), add_cors_headers(), _backup_preview(), _consume_action_token(), _dir_size_bytes(), log_activity() (+16 more)

### Community 7 - "Testing Infra & Remote Access"
Cohesion: 0.11
Nodes (20): fake_pkgs/aiohttp (aiohttp client fake), fake_pkgs/anthropic (scriptable Anthropic client fake), fake_pkgs/discord (Discord SDK fake), fake_pkgs/ (drop-in fake SDKs), test_mcp_server.py (real protocol-compliant local MCP server), Why this exists as a separate folder (test against real-like dependencies), MCP is opt-in at the tool level, not the server level, Real safeguards, not just docs (+12 more)

### Community 8 - "Preview/Confirm Pattern"
Cohesion: 0.15
Nodes (18): Financial and legal boundaries are explicit, not implied, Destructive host actions require a human-confirmed token, Smoke test (7-step beta verification), POST /api/actions/backup, POST /api/actions/deploy-container, GET /api/containers, Preview-then-confirm action pattern, Trade ledger disclaimer (not tax/legal/financial advice) (+10 more)

### Community 9 - "Fake aiohttp Client"
Cohesion: 0.12
Nodes (7): ClientError, ClientSession, ClientTimeout, _MockResponse, Exception, Minimal fake of 'aiohttp' — enough to test bot.py's backend_get/backend_chat…, Test double: configure `.script` with a queue of _MockResponse objects (or an…

### Community 10 - "Auth Tokens & Status Routes"
Cohesion: 0.21
Nodes (11): dev_repos(), get_auth_log(), get_repo_status(), health(), mcp_servers(), route, Recent login attempts. Platform-aware: - Windows: Security event log (IDs…, require_token() (+3 more)

### Community 11 - "Trade Activity & DB Access"
Cohesion: 0.22
Nodes (11): activity(), chat_usage(), delete_trade(), _get_db_connection(), get_llm_usage(), get_recent_activity(), _init_db(), _json_result() (+3 more)

### Community 12 - "Trade CRUD & Export"
Cohesion: 0.20
Nodes (10): add_trade(), get_trades(), Returns (normalized_dict, None) or (None, error_message)., Raw transaction ledger as CSV text., Per-disposal FIFO tax report as CSV text — one row per sell-vs-buy-lot match,…, _tax_lots_to_csv(), trades(), trades_export() (+2 more)

### Community 13 - "FIFO Tax-Lot Engine"
Cohesion: 0.20
Nodes (10): _fifo_engine(), get_trade_summary(), get_trade_tax_lots(), Best-effort date -> integer day count, for holding-period math. Never raises;…, The one place FIFO matching happens. Returns both an aggregated per-asset view…, Simplified FIFO realized gain/loss per asset — the aggregated view. See…, Per-disposal detail: each row is one sell matched against one consumed buy lot,…, _trade_date_to_epoch_days() (+2 more)

### Community 14 - "System Monitoring (CPU/Uptime)"
Cohesion: 0.25
Nodes (9): get_cpu_temp_c(), get_uptime_str(), pending_os_updates(), Best-effort CPU temperature read. Returns None if unavailable — which, on…, Count of pending OS updates. Real implementation on both platforms: Windows…, status(), _status_data(), systems() (+1 more)

### Community 15 - "Container CVE Scanning"
Cohesion: 0.25
Nodes (8): _parse_scout_sarif(), Defensive SARIF parser: Docker Scout's exact SARIF property layout isn't…, Runs `docker scout cves` for one image. Returns a result dict — never raises.…, Scans the images of currently running containers. Capped to CVE_SCAN_MAX_IMAGES…, scan_container_cves(), _scan_image_cves(), security_cve_scan(), _severity_from_score()

### Community 16 - "Project Overview (README)"
Cohesion: 0.43
Nodes (7): dev-tools (testing infrastructure), One source of truth per piece of logic, Ultron (personal AI home lab system), ultron-backend (Flask backend), ultron-dashboard.html, ultron-discord-bot, Discord bot setup step

### Community 17 - "Git Repo Diff/Status"
Cohesion: 0.29
Nodes (7): dev_repo_diff(), _find_repo_dir(), get_repo_diff(), Matches only against the pre-configured repo basenames — a caller can never…, Runs a read-only git command in repo_path. Returns (stdout, error) — never…, _repo_status(), _run_git()

### Community 18 - "Dev-Tools Test MCP Server"
Cohesion: 0.47
Nodes (5): jsonrpc_error(), jsonrpc_result(), mcp_endpoint(), route, A real MCP server for testing app.py's MCP client against genuine JSON-RPC…

### Community 19 - "Docker Containers"
Cohesion: 0.33
Nodes (6): containers(), _containers_data(), docker_ps(), docker_stats(), Return container info via the Docker CLI, avoiding a hard dependency on the…, Live CPU/mem per container, keyed by name. Best-effort; returns {} on any…

### Community 20 - "Chat Rate Limiting"
Cohesion: 0.40
Nodes (5): chat(), _check_rate_limit(), Returns None if the request is allowed, or an error message if the caller…, Sums input+output tokens (real spend) for calls logged today (local date,…, _todays_token_usage()

### Community 22 - "Windows/Linux Platform Support"
Cohesion: 0.50
Nodes (4): Windows/Linux platform detection (temps, updates, storage mounts), "Ultron Backend" Windows Firewall rule, pywin32, WMI

## Knowledge Gaps
- **33 isolated node(s):** `ButtonStyle`, `dev-tools (testing infrastructure)`, `Obsidian vault (default welcome note)`, `The Importer (Obsidian plugin)`, `ULTRON_API_TOKEN (required env var)` (+28 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 165 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **10 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `POST /api/chat (Ultron's brain)` connect `API Surface & Dashboard Client` to `Preview/Confirm Pattern`, `Testing Infra & Remote Access`?**
  _High betweenness centrality (0.027) - this node is a cross-community bridge._
- **Why does `app_commands` connect `Fake Discord Slash Commands` to `Fake Discord Core (UI/Embed)`?**
  _High betweenness centrality (0.016) - this node is a cross-community bridge._
- **Why does `ui` connect `Fake Discord Slash Commands` to `Fake Discord Core (UI/Embed)`?**
  _High betweenness centrality (0.015) - this node is a cross-community bridge._
- **What connects `ButtonStyle`, `dev-tools (testing infrastructure)`, `Obsidian vault (default welcome note)` to the rest of the system?**
  _33 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Discord Bot Commands` be split into smaller, more focused modules?**
  _Cohesion score 0.08907103825136611 - nodes in this community are weakly interconnected._
- **Should `API Surface & Dashboard Client` be split into smaller, more focused modules?**
  _Cohesion score 0.05333333333333334 - nodes in this community are weakly interconnected._
- **Should `Fake Discord Core (UI/Embed)` be split into smaller, more focused modules?**
  _Cohesion score 0.05689900426742532 - nodes in this community are weakly interconnected._