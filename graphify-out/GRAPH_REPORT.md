# Graph Report - Ultron Project  (2026-09-14)

## Corpus Check
- 542 files · ~0 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 542 nodes · 844 edges · 70 communities (26 shown, 38 thin omitted)
- Extraction: 95% EXTRACTED · 5% INFERRED · 0% AMBIGUOUS · INFERRED: 46 edges (avg confidence: 0.85)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- Private/Mixed Community 0
- Private/Mixed Community 1
- discord/__init__.py
- anthropic/__init__.py
- Private/Mixed Community 4
- run_ultron_chat
- View
- Private/Mixed Community 7
- Private/Mixed Community 8
- ClientSession
- Private/Mixed Community 10
- Private/Mixed Community 11
- enrich_visibility.py
- docker_ps
- Private/Mixed Community 14
- Private/Mixed Community 15
- log_activity
- fake_pkgs/ (drop-in fake SDKs)
- dev_repo_diff
- Knowledge graph schema design (Module 4) — v1
- MCP Support (External Tool/Plugin System)
- test_mcp_server.py
- Knowledge graph gap spec (Module 2 deliverable)
- UltronBot
- test_tts_streaming.py
- Private/Mixed Community 25
- test_memory.py
- safe_report.py
- Action Endpoints (backup, deploy-container)
- aiultronproject Slack Workspace
- add_cors_headers
- Preview-Then-Confirm Action Pattern
- _load_mcp_config
- _split_platform_paths
- Private/Mixed Community 34
- Private/Mixed Community 35
- The Importer (Obsidian plugin)
- Ultron Project CLAUDE.md (graphify + vault instructions)
- docker-compose.yml (Compose Orchestration)
- ultron Bridge Network
- Coding Sub-Agent (Emergent, Not In Original Spec)
- Private/Mixed Community 42
- Ethical Hacking Agent (Refused)
- Private/Mixed Community 44
- Private/Mixed Community 45
- LyraWolf (Contributor)
- Archangel356291 (Project Owner)
- dev-tools (Testing Infrastructure)
- Private/Mixed Community 49
- ultron-backend (Flask Backend)
- Nothing Works Until Explicitly Configured
- One Source of Truth Per Piece of Logic
- Real-Dependency Testing Approach
- Private/Mixed Community 54
- Private/Mixed Community 55
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
5. `backend_get()` - 13 edges
6. `deploy_command()` - 10 edges
7. `require_role()` - 10 edges
8. `ultron-backend index (_index.md)` - 10 edges
9. `ConfirmActionView` - 9 edges
10. `APIStatusError` - 9 edges

## Surprising Connections (you probably didn't know these)
- `ultron-backend Service (Docker Compose)` --shares_data_with--> `ultron-backend README (Backend API Reference)`  [INFERRED]
  docker-compose.yml → ultron-backend/README.md
- `ultron-discord-bot Service (Docker Compose)` --shares_data_with--> `ultron-discord-bot (Thin Remote-Control Layer)`  [INFERRED]
  docker-compose.yml → README.md
- `export_command()` --references--> `Choice`  [EXTRACTED]
  ultron-discord-bot/bot.py → dev-tools/fake_pkgs/discord/__init__.py
- `ultron-backend Service (Docker Compose)` --conceptually_related_to--> `beta_tester RBAC Role`  [INFERRED]
  docker-compose.yml → ultron-backend/README.md
- `ultron-dashboard.html (Single-file Dashboard)` --shares_data_with--> `POST /api/chat (Claude Chat Tool-Use Loop)`  [INFERRED]
  README.md → ultron-backend/README.md

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Fake SDKs built to match real SDK shape** — dev_tools_readme_fake_anthropic, dev_tools_readme_fake_discord, dev_tools_readme_fake_aiohttp, ultron_backend_requirements_anthropic, ultron_discord_bot_requirements_discordpy, ultron_discord_bot_requirements_aiohttp [EXTRACTED 1.00]
- **Preview-Then-Confirm Pattern Across Current and Planned Actions** — readme_preview_then_confirm_pattern, ultron_backend_readme_action_endpoints, ultron_backend_pi_setup_phase2_plan [INFERRED 0.80]
- **MCP Discovery/Execution Separation Security Model** — project_summary_for_claude_code_mcp_support, readme_mcp_opt_in_principle, ultron_backend_readme_mcp_external_tools [INFERRED 0.85]
- **Original Four-Agent Spec Plus Emergent Fifth** — project_summary_for_claude_code_ethical_hacking_agent, project_summary_for_claude_code_investment_agent, project_summary_for_claude_code_crypto_trade_agent, project_summary_for_claude_code_home_lab_monitor_agent, project_summary_for_claude_code_coding_subagent [INFERRED 0.85]

## Communities (70 total, 38 thin omitted)

### Community 0 - "Private/Mixed Community 0"
Cohesion: 0.09
Nodes (56): button, choices, command, describe, Interaction, Fake interaction for testing command and button handlers directly., event, ask_command() (+48 more)

### Community 1 - "Private/Mixed Community 1"
Cohesion: 0.07
Nodes (37): Master Index (Obsidian Vault Root), [private], Chamfered-Corner UI Design (45° cut panels), file:// Origin fetch() Bug (mobile Chrome Connect button), --line Panel Border Color Variable, [private], [private], ultron-backend Service (Docker Compose) (+29 more)

### Community 2 - "discord/__init__.py"
Cohesion: 0.06
Nodes (15): Bot, ButtonStyle, Embed, File, _Followup, HTTPException, Intents, _InteractionResponse (+7 more)

### Community 3 - "anthropic/__init__.py"
Cohesion: 0.09
Nodes (20): Anthropic, APIConnectionError, APIError, APIStatusError, APITimeoutError, AuthenticationError, BadRequestError, ContentBlock (+12 more)

### Community 4 - "Private/Mixed Community 4"
Cohesion: 0.07
Nodes (26): demo(), _queue_reply(), [private], ultron-discord-bot Service (Docker Compose), Bug: Discord backend_get Showed Raw Error Text, Bug: Discord Field-Truncation Off-By-N, Bug: Tool-Registration Ordering (get_llm_usage NameError Risk), [private] (+18 more)

### Community 5 - "run_ultron_chat"
Cohesion: 0.08
Nodes (28): _add_cache_breakpoint(), _ensure_mcp_discovered(), get_mcp_tools_and_dispatch(), _log_llm_usage(), _make_mcp_tool_handler(), handler(), _mcp_call_tool(), _mcp_discover_all() (+20 more)

### Community 6 - "View"
Cohesion: 0.08
Nodes (8): app_commands, Button, Choice, CommandTree, Matches @discord.ui.button(...). The fake doesn't need the full component-…, ui, decorator(), View

### Community 7 - "Private/Mixed Community 7"
Cohesion: 0.16
Nodes (22): action_backup(), action_deploy_container(), _backup_preview(), [private], _dir_size_bytes(), [private], [private], [private] (+14 more)

### Community 8 - "Private/Mixed Community 8"
Cohesion: 0.11
Nodes (20): add_trade(), chat_usage(), distill_activity_trends(), _get_db_connection(), get_llm_usage(), get_trades(), _init_db(), Returns (normalized_dict, None) or (None, error_message). (+12 more)

### Community 9 - "ClientSession"
Cohesion: 0.12
Nodes (7): ClientError, ClientSession, ClientTimeout, _MockResponse, Exception, Minimal fake of 'aiohttp' — enough to test bot.py's backend_get/backend_chat…, Test double: configure `.script` with a queue of _MockResponse objects (or an…

### Community 10 - "Private/Mixed Community 10"
Cohesion: 0.13
Nodes (18): [private], [private], [private], [private], [private], [private], [private], [private] (+10 more)

### Community 11 - "Private/Mixed Community 11"
Cohesion: 0.14
Nodes (17): _beta_tester_spend_usd(), chat(), _check_rate_limit(), dashboard(), _fish_audio_tts(), get_trade_summary(), health(), route (+9 more)

### Community 12 - "enrich_visibility.py"
Cohesion: 0.21
Nodes (15): classify_visibility(), decrypt_private_node(), derive_tags(), enrich(), _file_mtime_iso(), _get_or_create_key(), _load_json(), Post-processing enrichment for graphify's graph.json -- adds what KNOWLEDGE-… (+7 more)

### Community 13 - "docker_ps"
Cohesion: 0.14
Nodes (15): containers(), _containers_data(), docker_ps(), docker_stats(), get_cpu_temp_c(), get_uptime_str(), pending_os_updates(), Best-effort CPU temperature read. Returns None if unavailable — which, on… (+7 more)

### Community 14 - "Private/Mixed Community 14"
Cohesion: 0.17
Nodes (12): [private], [private], [private], [private], [private], [private], [private], [private] (+4 more)

### Community 15 - "Private/Mixed Community 15"
Cohesion: 0.20
Nodes (10): [private], [private], [private], [private], [private], [private], [private], [private] (+2 more)

### Community 16 - "log_activity"
Cohesion: 0.20
Nodes (10): log_activity(), _parse_scout_sarif(), Runs `docker scout cves` for one image. Returns a result dict — never raises.…, Scans the images of currently running containers. Capped to CVE_SCAN_MAX_IMAGES…, Best-effort logging — never raises. A logging failure (disk full, permissions,…, Defensive SARIF parser: Docker Scout's exact SARIF property layout isn't…, scan_container_cves(), _scan_image_cves() (+2 more)

### Community 17 - "fake_pkgs/ (drop-in fake SDKs)"
Cohesion: 0.22
Nodes (9): fake_pkgs/aiohttp (aiohttp client fake), fake_pkgs/anthropic (scriptable Anthropic client fake), fake_pkgs/discord (Discord SDK fake), fake_pkgs/ (drop-in fake SDKs), test_mcp_server.py (real protocol-compliant local MCP server), Why this exists as a separate folder (test against real-like dependencies), anthropic (>=1.0.0,<2.0.0), aiohttp (+1 more)

### Community 18 - "dev_repo_diff"
Cohesion: 0.22
Nodes (9): dev_repo_diff(), dev_repos(), _find_repo_dir(), get_repo_diff(), get_repo_status(), Runs a read-only git command in repo_path. Returns (stdout, error) — never…, Matches only against the pre-configured repo basenames — a caller can never…, _repo_status() (+1 more)

### Community 19 - "Knowledge graph schema design (Module 4) — v1"
Cohesion: 0.29
Nodes (6): Full workflow after a graphify rebuild, Knowledge graph schema design (Module 4) — v1, Known limitations — not solved tonight, Schema additions (per node), Visibility: classification and enforcement, What's committed to git vs. what never is

### Community 20 - "MCP Support (External Tool/Plugin System)"
Cohesion: 0.29
Nodes (7): Bug: MCP Empty Notification Response Mishandled, Bug: MCP Response-Size Cap Applied At Wrong Layer, dev-tools/fake_pkgs (Scriptable Fakes for anthropic/discord/aiohttp), MCP Support (External Tool/Plugin System), dev-tools/test_mcp_server.py (Real Protocol-Strict MCP Test Server), MCP Opt-In At the Tool Level, Not Server Level, External Tools (MCP) Section

### Community 21 - "test_mcp_server.py"
Cohesion: 0.47
Nodes (5): jsonrpc_error(), jsonrpc_result(), mcp_endpoint(), route, A real MCP server for testing app.py's MCP client against genuine JSON-RPC…

### Community 22 - "Knowledge graph gap spec (Module 2 deliverable)"
Cohesion: 0.33
Nodes (5): 1. Beta test results already recorded — pulled in as ground truth, 2. Graphify's actual output format, verified from the real files, 3. Ponytail — what it actually limits/strips, 4. The gap — what Module 4 actually needs to add, Knowledge graph gap spec (Module 2 deliverable)

### Community 24 - "test_tts_streaming.py"
Cohesion: 0.50
Nodes (3): demo(), _fake_streaming_tts(), Self-check for the /api/tts streaming fix (Module 1 of the roadmap: "text…

### Community 25 - "Private/Mixed Community 25"
Cohesion: 0.50
Nodes (5): [private], wrapper(), wrapper(), _resolve_role(), _touch_presence()

### Community 27 - "safe_report.py"
Cohesion: 0.67
Nodes (3): main(), make_safe_labels(), Regenerates graph.json's community_name field, GRAPH_REPORT.md, and graph.html…

## Knowledge Gaps
- **44 isolated node(s):** `ButtonStyle`, `1. Beta test results already recorded — pulled in as ground truth`, `2. Graphify's actual output format, verified from the real files`, `3. Ponytail — what it actually limits/strips`, `4. The gap — what Module 4 actually needs to add` (+39 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 242 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **38 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **What connects `ButtonStyle`, `1. Beta test results already recorded — pulled in as ground truth`, `2. Graphify's actual output format, verified from the real files` to the rest of the system?**
  _44 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Private/Mixed Community 0` be split into smaller, more focused modules?**
  _Cohesion score 0.08755760368663594 - nodes in this community are weakly interconnected._
- **Should `Private/Mixed Community 1` be split into smaller, more focused modules?**
  _Cohesion score 0.07152496626180836 - nodes in this community are weakly interconnected._
- **Should `discord/__init__.py` be split into smaller, more focused modules?**
  _Cohesion score 0.05689900426742532 - nodes in this community are weakly interconnected._
- **Should `anthropic/__init__.py` be split into smaller, more focused modules?**
  _Cohesion score 0.08571428571428572 - nodes in this community are weakly interconnected._
- **Should `Private/Mixed Community 4` be split into smaller, more focused modules?**
  _Cohesion score 0.0735632183908046 - nodes in this community are weakly interconnected._
- **Should `run_ultron_chat` be split into smaller, more focused modules?**
  _Cohesion score 0.082010582010582 - nodes in this community are weakly interconnected._