# Graph Report - Ultron Project  (2026-09-13)

## Corpus Check
- 24 files · ~42,843 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 2 file(s) not represented in the graph (top: (none) 2)

## Summary
- 529 nodes · 877 edges · 50 communities (28 shown, 16 thin omitted)
- Extraction: 93% EXTRACTED · 7% INFERRED · 0% AMBIGUOUS · INFERRED: 58 edges (avg confidence: 0.87)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `a73ea829`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- bot.py
- discord/__init__.py
- anthropic/__init__.py
- POST /api/chat (Ultron's brain)
- View
- route
- docker_ps
- app.py
- run_ultron_chat
- ClientSession
- apiGet
- Ultron (personal AI home lab system)
- _get_db_connection
- fake_pkgs/ (drop-in fake SDKs)
- escapeHtml
- start-ultron.ps1
- action_backup
- Flask Backend (app.py)
- require_token
- authHeaders
- test_mcp_server.py
- _fifo_engine
- scan_container_cves
- Preview-then-confirm action pattern
- ultron-backend/app.py
- require_role
- Coding Sub-Agent / Development Tab (git data)
- Config Value Floor Hardening
- Financial and legal boundaries are explicit, not implied
- GET /api/trades/export
- The Importer (Obsidian plugin)
- after_request
- Discord backend_get Raw-Error-Text Bug
- Discord Field Truncation Off-by-N Bug
- get_llm_usage Tool Registration Ordering Bug
- Nothing works until explicitly configured
- Exception
- GET /api/security/cve-scan
- Running permanently at startup (Task Scheduler/NSSM)
- /forget command
- require_auth (Discord ID allowlist check)
- Master Index
- CLAUDE.md
- route

## God Nodes (most connected - your core abstractions)
1. `Interaction` - 21 edges
2. `require_token()` - 18 edges
3. `require_auth()` - 18 edges
4. `POST /api/chat (Ultron's brain)` - 18 edges
5. `format_error_embed()` - 16 edges
6. `_json_result()` - 13 edges
7. `Ultron (personal AI home lab system)` - 13 edges
8. `backend_get()` - 12 edges
9. `apiGet()` - 12 edges
10. `refreshAll()` - 12 edges

## Surprising Connections (you probably didn't know these)
- `connectBackend()` --shares_data_with--> `Flask Backend (app.py)`  [INFERRED]
  ultron-dashboard.html → PROJECT-SUMMARY-FOR-CLAUDE-CODE.md
- `loadAuthLog()` --shares_data_with--> `Flask Backend (app.py)`  [INFERRED]
  ultron-dashboard.html → PROJECT-SUMMARY-FOR-CLAUDE-CODE.md
- `fetchDevRepos()` --shares_data_with--> `get_repo_diff Chat Tool (parameterized)`  [INFERRED]
  ultron-dashboard.html → PROJECT-SUMMARY-FOR-CLAUDE-CODE.md
- `Coding Sub-Agent / Development Tab (git data)` --conceptually_related_to--> `Development Tab Feature (ULTRON_CODE_REPOS)`  [INFERRED]
  PROJECT-SUMMARY-FOR-CLAUDE-CODE.md → ultron-backend/BETA-LAUNCH-CHECKLIST.md
- `confirmBackup()` --shares_data_with--> `Real Action Endpoints (backup, deploy-container)`  [INFERRED]
  ultron-dashboard.html → PROJECT-SUMMARY-FOR-CLAUDE-CODE.md

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Fake SDKs built to match real SDK shape** — dev_tools_readme_fake_anthropic, dev_tools_readme_fake_discord, dev_tools_readme_fake_aiohttp, ultron_backend_requirements_anthropic, ultron_discord_bot_requirements_discordpy, ultron_discord_bot_requirements_aiohttp [EXTRACTED 1.00]
- **MCP opt-in security model participants** — ultron_backend_readme_mcp_security_model, ultron_backend_readme_api_mcp_servers, dev_tools_readme_test_mcp_server, ultron_dashboard_loadmcpservers, ultron_discord_bot_readme_mcp_cmd [EXTRACTED 1.00]
- **Preview-then-confirm action pattern across backend, dashboard, and bot** — ultron_backend_readme_preview_confirm_pattern, ultron_backend_readme_api_actions_backup, ultron_backend_readme_api_actions_deploy_container, ultron_discord_bot_readme_backup_cmd, ultron_discord_bot_readme_deploy_cmd, ultron_dashboard_previewbackup, ultron_dashboard_previewdeploy [EXTRACTED 1.00]
- **AI Assistant Chat Flow** — ultron_dashboard_sendchatmessage, ultron_dashboard_postchat, ultron_dashboard_appendchatbubble, ultron_dashboard_speakreply, ultron_dashboard_togglevoiceinput, ultron_dashboard_sendfromhome [INFERRED 0.80]
- **Dashboard Live Data Refresh Flow** — ultron_dashboard_refreshall, ultron_dashboard_fetchstatus, ultron_dashboard_fetchcontainers, ultron_dashboard_fetchstorage, ultron_dashboard_fetchsystems, ultron_dashboard_fetchactivity, ultron_dashboard_fetchdevrepos, ultron_dashboard_fetchtrades, ultron_dashboard_fetchllmusage [INFERRED 0.85]
- **Preview-Confirm Action Flow (deploy & backup)** — ultron_dashboard_previewdeploy, ultron_dashboard_confirmdeploy, ultron_dashboard_canceldeploy, ultron_dashboard_previewbackup, ultron_dashboard_confirmbackup, ultron_dashboard_cancelbackup, project_summary_for_claude_code_action_endpoints [INFERRED 0.85]

## Communities (50 total, 16 thin omitted)

### Community 0 - "bot.py"
Cohesion: 0.08
Nodes (55): button, choices, command, describe, Interaction, Fake interaction for testing command and button handlers directly., event, ask_command() (+47 more)

### Community 1 - "discord/__init__.py"
Cohesion: 0.06
Nodes (15): Bot, ButtonStyle, Embed, File, _Followup, HTTPException, Intents, _InteractionResponse (+7 more)

### Community 2 - "anthropic/__init__.py"
Cohesion: 0.10
Nodes (17): Anthropic, APIConnectionError, APIError, APIStatusError, APITimeoutError, AuthenticationError, BadRequestError, ContentBlock (+9 more)

### Community 3 - "POST /api/chat (Ultron's brain)"
Cohesion: 0.07
Nodes (29): Read-only by default, everywhere, Real safeguards, not just docs, GET /api/activity, POST /api/chat (Ultron's brain), GET /api/chat/usage, GET /api/containers, GET /api/dev/repos/<repo>/diff, GET /api/dev/repos (+21 more)

### Community 4 - "View"
Cohesion: 0.08
Nodes (8): app_commands, Button, Choice, CommandTree, Matches @discord.ui.button(...). The fake doesn't need the full component-…, ui, decorator(), View

### Community 5 - "route"
Cohesion: 0.15
Nodes (17): route, activity(), chat_usage(), delete_trade(), get_auth_log(), get_llm_usage(), get_recent_activity(), get_trade_summary() (+9 more)

### Community 6 - "docker_ps"
Cohesion: 0.18
Nodes (11): containers(), _containers_data(), docker_ps(), docker_stats(), Return container info via the Docker CLI, avoiding a hard dependency on the…, Live CPU/mem per container, keyed by name. Best-effort; returns {} on any…, Validates and normalizes a deploy-container request body. Returns (params,…, _validate_container_name() (+3 more)

### Community 7 - "app.py"
Cohesion: 0.16
Nodes (20): add_cors_headers(), containers(), docker_ps(), docker_stats(), get_cpu_temp_c(), get_uptime_str(), health(), pending_os_updates() (+12 more)

### Community 8 - "run_ultron_chat"
Cohesion: 0.09
Nodes (26): Exception, _add_cache_breakpoint(), _ensure_mcp_discovered(), get_mcp_tools_and_dispatch(), _log_llm_usage(), _make_mcp_tool_handler(), handler(), _mcp_call_tool() (+18 more)

### Community 9 - "ClientSession"
Cohesion: 0.12
Nodes (7): ClientError, ClientSession, ClientTimeout, _MockResponse, Exception, Minimal fake of 'aiohttp' — enough to test bot.py's backend_get/backend_chat…, Test double: configure `.script` with a queue of _MockResponse objects (or an…

### Community 10 - "apiGet"
Cohesion: 0.26
Nodes (12): Real Activity Log (SQLite-backed), apiGet(), connectBackend(), fetchActivity(), fetchLlmUsage(), fetchStatus(), fetchStorage(), fetchSystems() (+4 more)

### Community 11 - "Ultron (personal AI home lab system)"
Cohesion: 0.15
Nodes (19): dev-tools/README.md, Ethical Hacking Agent (refused outright), Explicit Safety Boundaries Maintained, Investment/Financial Predictive Agent (reinterpreted), Known, Deliberate Gaps, MCP Empty Notification Response Bug, MCP Response-Size Cap Applied at Wrong Layer, MCP (external tool/plugin) Support (+11 more)

### Community 12 - "_get_db_connection"
Cohesion: 0.25
Nodes (9): add_trade(), _get_db_connection(), get_trades(), _init_db(), Returns (normalized_dict, None) or (None, error_message)., Raw transaction ledger as CSV text., trades(), _trades_to_csv() (+1 more)

### Community 13 - "fake_pkgs/ (drop-in fake SDKs)"
Cohesion: 0.14
Nodes (15): fake_pkgs/aiohttp (aiohttp client fake), fake_pkgs/anthropic (scriptable Anthropic client fake), fake_pkgs/discord (Discord SDK fake), fake_pkgs/ (drop-in fake SDKs), test_mcp_server.py (real protocol-compliant local MCP server), Why this exists as a separate folder (test against real-like dependencies), MCP is opt-in at the tool level, not the server level, Testing approach (test against real dependency behavior) (+7 more)

### Community 14 - "escapeHtml"
Cohesion: 0.21
Nodes (12): Real Action Endpoints (backup, deploy-container), _fifo_engine() Shared Trade Calculation, addTrade(), apiPost(), confirmBackup(), confirmDeploy(), escapeHtml(), fetchContainers() (+4 more)

### Community 15 - "start-ultron.ps1"
Cohesion: 0.19
Nodes (14): Cost Controls (caching, token budget, rate limit), LLM Chat Brain (Claude), ANTHROPIC_API_KEY (real beta key), Backup Feature (ULTRON_BACKUP_SOURCES / DEST), ULTRON_CHAT_RATE_LIMIT_PER_MINUTE, ULTRON_LLM_DAILY_TOKEN_BUDGET, Discord Bot Setup (start-bot.ps1), Known By-Design Beta Behaviors (+6 more)

### Community 16 - "action_backup"
Cohesion: 0.22
Nodes (13): action_backup(), action_deploy_container(), _backup_preview(), _consume_action_token(), _dir_size_bytes(), log_activity(), _new_action_token(), _prune_expired_tokens_locked() (+5 more)

### Community 17 - "Flask Backend (app.py)"
Cohesion: 0.25
Nodes (9): Flask Backend (app.py), HTML/JS Dashboard, GET /api/health, Windows/Linux platform detection (temps, updates, storage mounts), "Ultron Backend" Windows Firewall rule, Flask (>=3.0,<4.0), pywin32 (==306, Windows only), WMI (==1.5.1, Windows only) (+1 more)

### Community 18 - "require_token"
Cohesion: 0.16
Nodes (14): get_cpu_temp_c(), get_mcp_servers(), get_uptime_str(), mcp_servers(), pending_os_updates(), Read-only view of every configured server and everything it offers — approved…, Admin-only. Existing routes are unchanged: a valid beta token is a real…, Best-effort CPU temperature read. Returns None if unavailable — which, on… (+6 more)

### Community 19 - "authHeaders"
Cohesion: 0.17
Nodes (11): Trade CSV Export (transactions + tax-lots), Discord Bot (bot.py), Discord Bot Feature Parity, Voice / TTS (Fish Audio, /api/tts), authHeaders(), deleteTradeRow(), downloadTradeExport(), postChat() (+3 more)

### Community 20 - "test_mcp_server.py"
Cohesion: 0.32
Nodes (7): jsonrpc_error(), jsonrpc_result(), mcp_endpoint(), route, A real MCP server for testing app.py's MCP client against genuine JSON-RPC…, dev-tools/fake_pkgs/ (anthropic/discord/aiohttp fakes), Testing Philosophy (real services + scriptable fakes)

### Community 21 - "_fifo_engine"
Cohesion: 0.20
Nodes (10): _fifo_engine(), get_trade_tax_lots(), Best-effort date -> integer day count, for holding-period math. Never raises;…, The one place FIFO matching happens. Returns both an aggregated per-asset view…, Per-disposal detail: each row is one sell matched against one consumed buy lot,…, Per-disposal FIFO tax report as CSV text — one row per sell-vs-buy-lot match,…, _tax_lots_to_csv(), _trade_date_to_epoch_days() (+2 more)

### Community 22 - "scan_container_cves"
Cohesion: 0.25
Nodes (8): _parse_scout_sarif(), Defensive SARIF parser: Docker Scout's exact SARIF property layout isn't…, Runs `docker scout cves` for one image. Returns a result dict — never raises.…, Scans the images of currently running containers. Capped to CVE_SCAN_MAX_IMAGES…, scan_container_cves(), _scan_image_cves(), security_cve_scan(), _severity_from_score()

### Community 23 - "Preview-then-confirm action pattern"
Cohesion: 0.52
Nodes (7): Destructive host actions require a human-confirmed token, POST /api/actions/backup, POST /api/actions/deploy-container, Preview-then-confirm action pattern, /backup command, /deploy command, Confirm/Cancel button flow (bot action commands)

### Community 24 - "ultron-backend/app.py"
Cohesion: 0.14
Nodes (19): after_request, add_cors_headers(), dev_repo_diff(), dev_repos(), _find_repo_dir(), get_repo_diff(), get_repo_status(), _load_mcp_config() (+11 more)

### Community 25 - "require_role"
Cohesion: 0.14
Nodes (15): chat(), _check_rate_limit(), _fish_audio_tts(), Returns None if the request is allowed, or an error message if the caller…, Sums input+output tokens (real spend) for calls logged today (local date,…, One TTS request to Fish Audio. Returns (audio_bytes, content_type, error)., Constant-time-ish token check against both roles. Returns 'admin', 'beta', or…, Admin or beta_tester. Use only on endpoints in the beta tester's allowed scope… (+7 more)

### Community 26 - "Coding Sub-Agent / Development Tab (git data)"
Cohesion: 0.40
Nodes (6): Coding Sub-Agent / Development Tab (git data), get_repo_diff Chat Tool (parameterized), Home Lab Monitor & Command Router, Development Tab Feature (ULTRON_CODE_REPOS), psutil (>=6.0,<7.0), fetchDevRepos()

### Community 47 - "Master Index"
Cohesion: 0.33
Nodes (4): Folders, Master Index, Root notes, ultron-backend index

## Ambiguous Edges - Review These
- `Coding Sub-Agent / Development Tab (git data)` → `Home Lab Monitor & Command Router`  [AMBIGUOUS]
  PROJECT-SUMMARY-FOR-CLAUDE-CODE.md · relation: conceptually_related_to

## Knowledge Gaps
- **40 isolated node(s):** `ButtonStyle`, `Folders`, `Root notes`, `ultron-backend index`, `graphify` (+35 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 195 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **16 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **What is the exact relationship between `Coding Sub-Agent / Development Tab (git data)` and `Home Lab Monitor & Command Router`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._
- **Why does `anthropic (>=1.0.0,<2.0.0)` connect `start-ultron.ps1` to `POST /api/chat (Ultron's brain)`, `fake_pkgs/ (drop-in fake SDKs)`?**
  _High betweenness centrality (0.034) - this node is a cross-community bridge._
- **Why does `POST /api/chat (Ultron's brain)` connect `POST /api/chat (Ultron's brain)` to `fake_pkgs/ (drop-in fake SDKs)`, `start-ultron.ps1`?**
  _High betweenness centrality (0.032) - this node is a cross-community bridge._
- **What connects `ButtonStyle`, `Folders`, `Root notes` to the rest of the system?**
  _40 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `bot.py` be split into smaller, more focused modules?**
  _Cohesion score 0.07878787878787878 - nodes in this community are weakly interconnected._
- **Should `discord/__init__.py` be split into smaller, more focused modules?**
  _Cohesion score 0.05689900426742532 - nodes in this community are weakly interconnected._
- **Should `anthropic/__init__.py` be split into smaller, more focused modules?**
  _Cohesion score 0.09879032258064516 - nodes in this community are weakly interconnected._