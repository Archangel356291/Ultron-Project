# Graph Report - Ultron Project  (2026-09-14)

## Corpus Check
- 491 files · ~0 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 491 nodes · 783 edges · 63 communities (23 shown, 35 thin omitted)
- Extraction: 94% EXTRACTED · 6% INFERRED · 0% AMBIGUOUS · INFERRED: 46 edges (avg confidence: 0.85)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- Private/Mixed Community 0
- discord/__init__.py
- anthropic/__init__.py
- Private/Mixed Community 3
- Private/Mixed Community 4
- View
- Private/Mixed Community 6
- Private/Mixed Community 7
- run_ultron_chat
- ClientSession
- Private/Mixed Community 10
- Private/Mixed Community 11
- _get_db_connection
- Private/Mixed Community 13
- Private/Mixed Community 14
- log_activity
- fake_pkgs/ (drop-in fake SDKs)
- _status_data
- MCP Support (External Tool/Plugin System)
- test_mcp_server.py
- Knowledge graph gap spec (Module 2 deliverable)
- docker_ps
- UltronBot
- test_tts_streaming.py
- test_memory.py
- Action Endpoints (backup, deploy-container)
- aiultronproject Slack Workspace
- Preview-Then-Confirm Action Pattern
- Private/Mixed Community 28
- Private/Mixed Community 29
- The Importer (Obsidian plugin)
- Ultron Project CLAUDE.md (graphify + vault instructions)
- docker-compose.yml (Compose Orchestration)
- ultron Bridge Network
- Coding Sub-Agent (Emergent, Not In Original Spec)
- Private/Mixed Community 35
- Ethical Hacking Agent (Refused)
- Private/Mixed Community 37
- Private/Mixed Community 38
- LyraWolf (Contributor)
- Archangel356291 (Project Owner)
- dev-tools (Testing Infrastructure)
- Private/Mixed Community 42
- ultron-backend (Flask Backend)
- Nothing Works Until Explicitly Configured
- One Source of Truth Per Piece of Logic
- Real-Dependency Testing Approach
- Private/Mixed Community 47
- Private/Mixed Community 48
- /api/activity (Persistent Activity Log)
- app.py (Flask Backend Entrypoint)
- /api/security/auth-log
- /api/security/cve-scan (Docker Scout CVE Scan)
- /api/dev/* (Development Tab Git Status/Diff)
- Flask (>=3.0,<4.0)
- psutil (>=6.0,<7.0)
- pywin32 (==306, Windows only)
- WMI (==1.5.1, Windows only)

## God Nodes (most connected - your core abstractions)
1. `Interaction` - 22 edges
2. `require_auth()` - 19 edges
3. `format_error_embed()` - 17 edges
4. `_get_db_connection()` - 15 edges
5. `_json_result()` - 14 edges
6. `backend_get()` - 13 edges
7. `deploy_command()` - 10 edges
8. `require_role()` - 10 edges
9. `ConfirmActionView` - 9 edges
10. `APIStatusError` - 9 edges

## Surprising Connections (you probably didn't know these)
- `ultron-discord-bot Service (Docker Compose)` --shares_data_with--> `ultron-discord-bot (Thin Remote-Control Layer)`  [INFERRED]
  docker-compose.yml → README.md
- `ultron-backend Service (Docker Compose)` --shares_data_with--> `ultron-backend README (Backend API Reference)`  [INFERRED]
  docker-compose.yml → ultron-backend/README.md
- `export_command()` --references--> `Choice`  [EXTRACTED]
  ultron-discord-bot/bot.py → dev-tools/fake_pkgs/discord/__init__.py
- `ultron-dashboard.html (Single-file Dashboard)` --shares_data_with--> `POST /api/chat (Claude Chat Tool-Use Loop)`  [INFERRED]
  README.md → ultron-backend/README.md
- `ultron-discord-bot (Thin Remote-Control Layer)` --shares_data_with--> `POST /api/chat (Claude Chat Tool-Use Loop)`  [INFERRED]
  README.md → ultron-backend/README.md

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Fake SDKs built to match real SDK shape** — dev_tools_readme_fake_anthropic, dev_tools_readme_fake_discord, dev_tools_readme_fake_aiohttp, ultron_backend_requirements_anthropic, ultron_discord_bot_requirements_discordpy, ultron_discord_bot_requirements_aiohttp [EXTRACTED 1.00]
- **Preview-Then-Confirm Pattern Across Current and Planned Actions** — readme_preview_then_confirm_pattern, ultron_backend_readme_action_endpoints, ultron_backend_pi_setup_phase2_plan [INFERRED 0.80]
- **MCP Discovery/Execution Separation Security Model** — project_summary_for_claude_code_mcp_support, readme_mcp_opt_in_principle, ultron_backend_readme_mcp_external_tools [INFERRED 0.85]
- **Original Four-Agent Spec Plus Emergent Fifth** — project_summary_for_claude_code_ethical_hacking_agent, project_summary_for_claude_code_investment_agent, project_summary_for_claude_code_crypto_trade_agent, project_summary_for_claude_code_home_lab_monitor_agent, project_summary_for_claude_code_coding_subagent [INFERRED 0.85]

## Communities (63 total, 35 thin omitted)

### Community 0 - "Private/Mixed Community 0"
Cohesion: 0.09
Nodes (56): button, choices, command, describe, Interaction, Fake interaction for testing command and button handlers directly., event, ask_command() (+48 more)

### Community 1 - "discord/__init__.py"
Cohesion: 0.06
Nodes (15): Bot, ButtonStyle, Embed, File, _Followup, HTTPException, Intents, _InteractionResponse (+7 more)

### Community 2 - "anthropic/__init__.py"
Cohesion: 0.09
Nodes (20): Anthropic, APIConnectionError, APIError, APIStatusError, APITimeoutError, AuthenticationError, BadRequestError, ContentBlock (+12 more)

### Community 3 - "Private/Mixed Community 3"
Cohesion: 0.07
Nodes (26): demo(), _queue_reply(), [private], ultron-discord-bot Service (Docker Compose), Bug: Discord backend_get Showed Raw Error Text, Bug: Discord Field-Truncation Off-By-N, Bug: Tool-Registration Ordering (get_llm_usage NameError Risk), [private] (+18 more)

### Community 4 - "Private/Mixed Community 4"
Cohesion: 0.11
Nodes (28): Master Index (Obsidian Vault Root), [private], Chamfered-Corner UI Design (45° cut panels), file:// Origin fetch() Bug (mobile Chrome Connect button), --line Panel Border Color Variable, [private], [private], ultron-backend Service (Docker Compose) (+20 more)

### Community 5 - "View"
Cohesion: 0.08
Nodes (8): app_commands, Button, Choice, CommandTree, Matches @discord.ui.button(...). The fake doesn't need the full component-…, ui, decorator(), View

### Community 6 - "Private/Mixed Community 6"
Cohesion: 0.11
Nodes (26): activity(), chat_usage(), connections(), dashboard(), delete_trade(), get_auth_log(), get_llm_usage(), get_mcp_servers() (+18 more)

### Community 7 - "Private/Mixed Community 7"
Cohesion: 0.12
Nodes (23): after_request, add_cors_headers(), dev_repo_diff(), dev_repos(), _find_repo_dir(), get_repo_diff(), get_repo_status(), _load_mcp_config() (+15 more)

### Community 8 - "run_ultron_chat"
Cohesion: 0.10
Nodes (24): _add_cache_breakpoint(), _ensure_mcp_discovered(), get_mcp_tools_and_dispatch(), _make_mcp_tool_handler(), handler(), _mcp_call_tool(), _mcp_discover_all(), _mcp_http_post() (+16 more)

### Community 9 - "ClientSession"
Cohesion: 0.12
Nodes (7): ClientError, ClientSession, ClientTimeout, _MockResponse, Exception, Minimal fake of 'aiohttp' — enough to test bot.py's backend_get/backend_chat…, Test double: configure `.script` with a queue of _MockResponse objects (or an…

### Community 10 - "Private/Mixed Community 10"
Cohesion: 0.13
Nodes (18): _beta_tester_spend_usd(), chat(), _check_rate_limit(), _fish_audio_tts(), Returns None if the request is allowed, or an error message if the caller…, Lifetime spend for one beta tester, in dollars. Returns 0.0 on any read failure…, [private], One TTS request to Fish Audio. Fish Audio's own /v1/tts already streams its… (+10 more)

### Community 11 - "Private/Mixed Community 11"
Cohesion: 0.23
Nodes (12): action_backup(), action_deploy_container(), _backup_preview(), [private], _dir_size_bytes(), [private], [private], [private] (+4 more)

### Community 12 - "_get_db_connection"
Cohesion: 0.18
Nodes (12): distill_activity_trends(), _get_db_connection(), _init_db(), _log_llm_usage(), Best-effort — never raises. A logging failure must not break the chat response…, Best-effort, like log_activity — this runs unattended on a background timer…, Runs distill_activity_trends() once now, then every 24h, in a daemon thread so…, Real dollar cost of one API call from its actual usage counts. Returns 0.0 for… (+4 more)

### Community 13 - "Private/Mixed Community 13"
Cohesion: 0.20
Nodes (10): add_trade(), get_trades(), Returns (normalized_dict, None) or (None, error_message)., Raw transaction ledger as CSV text., [private], _tax_lots_to_csv(), trades(), trades_export() (+2 more)

### Community 14 - "Private/Mixed Community 14"
Cohesion: 0.20
Nodes (10): [private], [private], [private], [private], [private], [private], [private], [private] (+2 more)

### Community 15 - "log_activity"
Cohesion: 0.20
Nodes (10): log_activity(), _parse_scout_sarif(), Runs `docker scout cves` for one image. Returns a result dict — never raises.…, Scans the images of currently running containers. Capped to CVE_SCAN_MAX_IMAGES…, Best-effort logging — never raises. A logging failure (disk full, permissions,…, Defensive SARIF parser: Docker Scout's exact SARIF property layout isn't…, scan_container_cves(), _scan_image_cves() (+2 more)

### Community 16 - "fake_pkgs/ (drop-in fake SDKs)"
Cohesion: 0.22
Nodes (9): fake_pkgs/aiohttp (aiohttp client fake), fake_pkgs/anthropic (scriptable Anthropic client fake), fake_pkgs/discord (Discord SDK fake), fake_pkgs/ (drop-in fake SDKs), test_mcp_server.py (real protocol-compliant local MCP server), Why this exists as a separate folder (test against real-like dependencies), anthropic (>=1.0.0,<2.0.0), aiohttp (+1 more)

### Community 17 - "_status_data"
Cohesion: 0.25
Nodes (9): get_cpu_temp_c(), get_uptime_str(), pending_os_updates(), Best-effort CPU temperature read. Returns None if unavailable — which, on…, Count of pending OS updates. Real implementation on both platforms: Windows…, status(), _status_data(), systems() (+1 more)

### Community 18 - "MCP Support (External Tool/Plugin System)"
Cohesion: 0.29
Nodes (7): Bug: MCP Empty Notification Response Mishandled, Bug: MCP Response-Size Cap Applied At Wrong Layer, dev-tools/fake_pkgs (Scriptable Fakes for anthropic/discord/aiohttp), MCP Support (External Tool/Plugin System), dev-tools/test_mcp_server.py (Real Protocol-Strict MCP Test Server), MCP Opt-In At the Tool Level, Not Server Level, External Tools (MCP) Section

### Community 19 - "test_mcp_server.py"
Cohesion: 0.47
Nodes (5): jsonrpc_error(), jsonrpc_result(), mcp_endpoint(), route, A real MCP server for testing app.py's MCP client against genuine JSON-RPC…

### Community 20 - "Knowledge graph gap spec (Module 2 deliverable)"
Cohesion: 0.33
Nodes (5): 1. Beta test results already recorded — pulled in as ground truth, 2. Graphify's actual output format, verified from the real files, 3. Ponytail — what it actually limits/strips, 4. The gap — what Module 4 actually needs to add, Knowledge graph gap spec (Module 2 deliverable)

### Community 21 - "docker_ps"
Cohesion: 0.33
Nodes (6): containers(), _containers_data(), docker_ps(), docker_stats(), Return container info via the Docker CLI, avoiding a hard dependency on the…, Live CPU/mem per container, keyed by name. Best-effort; returns {} on any…

### Community 23 - "test_tts_streaming.py"
Cohesion: 0.50
Nodes (3): demo(), _fake_streaming_tts(), Self-check for the /api/tts streaming fix (Module 1 of the roadmap: "text…

## Knowledge Gaps
- **39 isolated node(s):** `ButtonStyle`, `1. Beta test results already recorded — pulled in as ground truth`, `2. Graphify's actual output format, verified from the real files`, `3. Ponytail — what it actually limits/strips`, `4. The gap — what Module 4 actually needs to add` (+34 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 214 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **35 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **What connects `ButtonStyle`, `1. Beta test results already recorded — pulled in as ground truth`, `2. Graphify's actual output format, verified from the real files` to the rest of the system?**
  _39 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Private/Mixed Community 0` be split into smaller, more focused modules?**
  _Cohesion score 0.08755760368663594 - nodes in this community are weakly interconnected._
- **Should `discord/__init__.py` be split into smaller, more focused modules?**
  _Cohesion score 0.05689900426742532 - nodes in this community are weakly interconnected._
- **Should `anthropic/__init__.py` be split into smaller, more focused modules?**
  _Cohesion score 0.08571428571428572 - nodes in this community are weakly interconnected._
- **Should `Private/Mixed Community 3` be split into smaller, more focused modules?**
  _Cohesion score 0.0735632183908046 - nodes in this community are weakly interconnected._
- **Should `Private/Mixed Community 4` be split into smaller, more focused modules?**
  _Cohesion score 0.10591133004926108 - nodes in this community are weakly interconnected._
- **Should `View` be split into smaller, more focused modules?**
  _Cohesion score 0.08307692307692308 - nodes in this community are weakly interconnected._