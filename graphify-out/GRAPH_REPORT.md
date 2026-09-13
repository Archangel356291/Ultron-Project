# Graph Report - Ultron Project  (2026-09-13)

## Corpus Check
- 9 files · ~40,379 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 506 nodes · 857 edges · 47 communities (27 shown, 14 thin omitted)
- Extraction: 93% EXTRACTED · 7% INFERRED · 0% AMBIGUOUS · INFERRED: 57 edges (avg confidence: 0.87)
- Token cost: 163,897 input · 0 output

## Community Hubs (Navigation)
- Discord Test Fakes
- Discord Bot Core
- Anthropic Client Fakes
- Backend API & Principles
- Discord UI Component Fakes
- Backend Read Routes
- Host Status Functions
- Legacy App Status Functions
- MCP Tool Dispatch
- aiohttp Client Fake
- Dashboard Live Data Fetch
- Development Tab & Docs
- Trade FIFO Engine
- Test Infra & MCP Security
- Safety Boundaries & MCP Bugs
- Cost Controls & Beta Config
- Backup/Deploy Action Tokens
- Architecture Overview
- MCP JSON-RPC Client
- Voice & Chat Dashboard JS
- MCP Test Server
- Trade Export & Bot Parity
- CVE Scanning
- Preview-Confirm Action Pattern
- Git Repo Diff
- Chat Rate Limiting
- Fish Audio TTS
- Config Value Hardening
- Financial Disclaimer Boundary
- Trade Export Endpoint
- Obsidian Vault Notes
- CORS After-Request Hook
- Discord Error-Text Bug
- Discord Truncation Bug
- Tool Registration Bug
- Configured-By-Default Principle
- Isolated Exception Node
- CVE Scan Endpoint
- Startup/Task Scheduler Doc
- Forget Command Doc
- Discord Auth Allowlist

## God Nodes (most connected - your core abstractions)
1. `require_token()` - 22 edges
2. `Interaction` - 21 edges
3. `require_auth()` - 18 edges
4. `POST /api/chat (Ultron's brain)` - 18 edges
5. `format_error_embed()` - 16 edges
6. `Ultron (personal AI home lab system)` - 13 edges
7. `_json_result()` - 13 edges
8. `backend_get()` - 12 edges
9. `apiGet()` - 12 edges
10. `refreshAll()` - 12 edges

## Surprising Connections (you probably didn't know these)
- `Ultron (personal AI home lab system)` --conceptually_related_to--> `Investment/Financial Predictive Agent (reinterpreted)`  [EXTRACTED]
  README.md → PROJECT-SUMMARY-FOR-CLAUDE-CODE.md
- `Return container info via the Docker CLI, avoiding a hard dependency on the…` --rationale_for--> `docker_ps()`  [EXTRACTED]
  app.py → ultron-backend/app.py
- `pywin32 (==306, Windows only)` --shares_data_with--> `Flask Backend (app.py)`  [INFERRED]
  ultron-backend/requirements.txt → PROJECT-SUMMARY-FOR-CLAUDE-CODE.md
- `WMI (==1.5.1, Windows only)` --shares_data_with--> `Flask Backend (app.py)`  [INFERRED]
  ultron-backend/requirements.txt → PROJECT-SUMMARY-FOR-CLAUDE-CODE.md
- `connectBackend()` --shares_data_with--> `Flask Backend (app.py)`  [INFERRED]
  ultron-dashboard.html → PROJECT-SUMMARY-FOR-CLAUDE-CODE.md

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Fake SDKs built to match real SDK shape** — dev_tools_readme_fake_anthropic, dev_tools_readme_fake_discord, dev_tools_readme_fake_aiohttp, ultron_backend_requirements_anthropic, ultron_discord_bot_requirements_discordpy, ultron_discord_bot_requirements_aiohttp [EXTRACTED 1.00]
- **MCP opt-in security model participants** — ultron_backend_readme_mcp_security_model, ultron_backend_readme_api_mcp_servers, dev_tools_readme_test_mcp_server, ultron_dashboard_loadmcpservers, ultron_discord_bot_readme_mcp_cmd [EXTRACTED 1.00]
- **Preview-then-confirm action pattern across backend, dashboard, and bot** — ultron_backend_readme_preview_confirm_pattern, ultron_backend_readme_api_actions_backup, ultron_backend_readme_api_actions_deploy_container, ultron_discord_bot_readme_backup_cmd, ultron_discord_bot_readme_deploy_cmd, ultron_dashboard_previewbackup, ultron_dashboard_previewdeploy [EXTRACTED 1.00]
- **Preview-Confirm Action Flow (deploy & backup)** — ultron_dashboard_previewdeploy, ultron_dashboard_confirmdeploy, ultron_dashboard_canceldeploy, ultron_dashboard_previewbackup, ultron_dashboard_confirmbackup, ultron_dashboard_cancelbackup, project_summary_for_claude_code_action_endpoints [INFERRED 0.85]
- **AI Assistant Chat Flow** — ultron_dashboard_sendchatmessage, ultron_dashboard_postchat, ultron_dashboard_appendchatbubble, ultron_dashboard_speakreply, ultron_dashboard_togglevoiceinput, ultron_dashboard_sendfromhome [INFERRED 0.80]
- **Dashboard Live Data Refresh Flow** — ultron_dashboard_refreshall, ultron_dashboard_fetchstatus, ultron_dashboard_fetchcontainers, ultron_dashboard_fetchstorage, ultron_dashboard_fetchsystems, ultron_dashboard_fetchactivity, ultron_dashboard_fetchdevrepos, ultron_dashboard_fetchtrades, ultron_dashboard_fetchllmusage [INFERRED 0.85]

## Communities (47 total, 14 thin omitted)

### Community 0 - "Discord Test Fakes"
Cohesion: 0.08
Nodes (55): button, choices, command, describe, Interaction, Fake interaction for testing command and button handlers directly., event, ask_command() (+47 more)

### Community 1 - "Discord Bot Core"
Cohesion: 0.06
Nodes (15): Bot, ButtonStyle, Embed, File, _Followup, HTTPException, Intents, _InteractionResponse (+7 more)

### Community 2 - "Anthropic Client Fakes"
Cohesion: 0.10
Nodes (17): Anthropic, APIConnectionError, APIError, APIStatusError, APITimeoutError, AuthenticationError, BadRequestError, ContentBlock (+9 more)

### Community 3 - "Backend API & Principles"
Cohesion: 0.07
Nodes (29): Read-only by default, everywhere, Real safeguards, not just docs, GET /api/activity, POST /api/chat (Ultron's brain), GET /api/chat/usage, GET /api/containers, GET /api/dev/repos/<repo>/diff, GET /api/dev/repos (+21 more)

### Community 4 - "Discord UI Component Fakes"
Cohesion: 0.08
Nodes (8): app_commands, Button, Choice, CommandTree, Matches @discord.ui.button(...). The fake doesn't need the full component-…, ui, decorator(), View

### Community 5 - "Backend Read Routes"
Cohesion: 0.12
Nodes (25): activity(), chat_usage(), delete_trade(), dev_repos(), get_auth_log(), get_llm_usage(), get_recent_activity(), get_repo_status() (+17 more)

### Community 6 - "Host Status Functions"
Cohesion: 0.14
Nodes (23): add_cors_headers(), containers(), _containers_data(), docker_ps(), docker_stats(), get_cpu_temp_c(), get_uptime_str(), _load_mcp_config() (+15 more)

### Community 7 - "Legacy App Status Functions"
Cohesion: 0.16
Nodes (20): add_cors_headers(), containers(), docker_ps(), docker_stats(), get_cpu_temp_c(), get_uptime_str(), health(), pending_os_updates() (+12 more)

### Community 8 - "MCP Tool Dispatch"
Cohesion: 0.11
Nodes (20): _add_cache_breakpoint(), _ensure_mcp_discovered(), get_mcp_servers(), get_mcp_tools_and_dispatch(), _log_llm_usage(), _make_mcp_tool_handler(), handler(), _mcp_call_tool() (+12 more)

### Community 9 - "aiohttp Client Fake"
Cohesion: 0.12
Nodes (7): ClientError, ClientSession, ClientTimeout, _MockResponse, Exception, Minimal fake of 'aiohttp' — enough to test bot.py's backend_get/backend_chat…, Test double: configure `.script` with a queue of _MockResponse objects (or an…

### Community 10 - "Dashboard Live Data Fetch"
Cohesion: 0.21
Nodes (16): Real Activity Log (SQLite-backed), apiGet(), connectBackend(), escapeHtml(), fetchActivity(), fetchContainers(), fetchStatus(), fetchStorage() (+8 more)

### Community 11 - "Development Tab & Docs"
Cohesion: 0.16
Nodes (17): Coding Sub-Agent / Development Tab (git data), dev-tools/README.md, get_repo_diff Chat Tool (parameterized), Home Lab Monitor & Command Router, Known, Deliberate Gaps, Top-level README.md, REMOTE-ACCESS.md (Tailscale setup), dev-tools (testing infrastructure) (+9 more)

### Community 12 - "Trade FIFO Engine"
Cohesion: 0.14
Nodes (16): add_trade(), _fifo_engine(), _get_db_connection(), get_trades(), _init_db(), Returns (normalized_dict, None) or (None, error_message)., Best-effort date -> integer day count, for holding-period math. Never raises;…, The one place FIFO matching happens. Returns both an aggregated per-asset view… (+8 more)

### Community 13 - "Test Infra & MCP Security"
Cohesion: 0.15
Nodes (14): fake_pkgs/aiohttp (aiohttp client fake), fake_pkgs/discord (Discord SDK fake), fake_pkgs/ (drop-in fake SDKs), test_mcp_server.py (real protocol-compliant local MCP server), Why this exists as a separate folder (test against real-like dependencies), MCP is opt-in at the tool level, not the server level, Testing approach (test against real dependency behavior), External tools (MCP) security model (+6 more)

### Community 14 - "Safety Boundaries & MCP Bugs"
Cohesion: 0.20
Nodes (12): Real Action Endpoints (backup, deploy-container), Ethical Hacking Agent (refused outright), Explicit Safety Boundaries Maintained, Investment/Financial Predictive Agent (reinterpreted), MCP Empty Notification Response Bug, MCP Response-Size Cap Applied at Wrong Layer, MCP (external tool/plugin) Support, apiPost() (+4 more)

### Community 15 - "Cost Controls & Beta Config"
Cohesion: 0.21
Nodes (13): Cost Controls (caching, token budget, rate limit), ANTHROPIC_API_KEY (real beta key), Backup Feature (ULTRON_BACKUP_SOURCES / DEST), ULTRON_CHAT_RATE_LIMIT_PER_MINUTE, ULTRON_LLM_DAILY_TOKEN_BUDGET, Discord Bot Setup (start-bot.ps1), Known By-Design Beta Behaviors, ULTRON_MCP_CONFIG (optional MCP feature) (+5 more)

### Community 16 - "Backup/Deploy Action Tokens"
Cohesion: 0.23
Nodes (12): action_backup(), action_deploy_container(), _backup_preview(), _consume_action_token(), _dir_size_bytes(), log_activity(), _new_action_token(), _prune_expired_tokens_locked() (+4 more)

### Community 17 - "Architecture Overview"
Cohesion: 0.20
Nodes (11): fake_pkgs/anthropic (scriptable Anthropic client fake), Flask Backend (app.py), HTML/JS Dashboard, LLM Chat Brain (Claude), GET /api/health, Windows/Linux platform detection (temps, updates, storage mounts), "Ultron Backend" Windows Firewall rule, anthropic (>=1.0.0,<2.0.0) (+3 more)

### Community 18 - "MCP JSON-RPC Client"
Cohesion: 0.28
Nodes (9): Exception, _mcp_discover_all(), _mcp_http_post(), _mcp_initialize(), _mcp_jsonrpc_call(), _mcp_list_tools(), MCPError, One raw JSON-RPC POST. Hard timeout, hard response-size cap. Handles both a… (+1 more)

### Community 19 - "Voice & Chat Dashboard JS"
Cohesion: 0.25
Nodes (7): Voice / TTS (Fish Audio, /api/tts), authHeaders(), deleteTradeRow(), postChat(), sendChatMessage(), sendFromHome(), speakReply()

### Community 20 - "MCP Test Server"
Cohesion: 0.32
Nodes (7): jsonrpc_error(), jsonrpc_result(), mcp_endpoint(), route, A real MCP server for testing app.py's MCP client against genuine JSON-RPC…, dev-tools/fake_pkgs/ (anthropic/discord/aiohttp fakes), Testing Philosophy (real services + scriptable fakes)

### Community 21 - "Trade Export & Bot Parity"
Cohesion: 0.32
Nodes (8): Trade CSV Export (transactions + tax-lots), Discord Bot (bot.py), Discord Bot Feature Parity, _fifo_engine() Shared Trade Calculation, Crypto/Trade Record & Tax Agent, addTrade(), downloadTradeExport(), fetchTrades()

### Community 22 - "CVE Scanning"
Cohesion: 0.25
Nodes (8): _parse_scout_sarif(), Defensive SARIF parser: Docker Scout's exact SARIF property layout isn't…, Runs `docker scout cves` for one image. Returns a result dict — never raises.…, Scans the images of currently running containers. Capped to CVE_SCAN_MAX_IMAGES…, scan_container_cves(), _scan_image_cves(), security_cve_scan(), _severity_from_score()

### Community 23 - "Preview-Confirm Action Pattern"
Cohesion: 0.52
Nodes (7): Destructive host actions require a human-confirmed token, POST /api/actions/backup, POST /api/actions/deploy-container, Preview-then-confirm action pattern, /backup command, /deploy command, Confirm/Cancel button flow (bot action commands)

### Community 24 - "Git Repo Diff"
Cohesion: 0.29
Nodes (7): dev_repo_diff(), _find_repo_dir(), get_repo_diff(), Runs a read-only git command in repo_path. Returns (stdout, error) — never…, Matches only against the pre-configured repo basenames — a caller can never…, _repo_status(), _run_git()

### Community 25 - "Chat Rate Limiting"
Cohesion: 0.40
Nodes (5): chat(), _check_rate_limit(), Returns None if the request is allowed, or an error message if the caller…, Sums input+output tokens (real spend) for calls logged today (local date,…, _todays_token_usage()

### Community 26 - "Fish Audio TTS"
Cohesion: 0.67
Nodes (3): _fish_audio_tts(), One TTS request to Fish Audio. Returns (audio_bytes, content_type, error)., tts()

## Ambiguous Edges - Review These
- `Home Lab Monitor & Command Router` → `Coding Sub-Agent / Development Tab (git data)`  [AMBIGUOUS]
  PROJECT-SUMMARY-FOR-CLAUDE-CODE.md · relation: conceptually_related_to

## Knowledge Gaps
- **35 isolated node(s):** `ButtonStyle`, `GET /api/activity`, `GET /api/health`, `GET /api/security/auth-log`, `GET /api/security/cve-scan` (+30 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 175 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **14 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **What is the exact relationship between `Home Lab Monitor & Command Router` and `Coding Sub-Agent / Development Tab (git data)`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._
- **Why does `anthropic (>=1.0.0,<2.0.0)` connect `Architecture Overview` to `Backend API & Principles`, `Cost Controls & Beta Config`?**
  _High betweenness centrality (0.035) - this node is a cross-community bridge._
- **Why does `POST /api/chat (Ultron's brain)` connect `Backend API & Principles` to `Architecture Overview`, `Test Infra & MCP Security`?**
  _High betweenness centrality (0.033) - this node is a cross-community bridge._
- **Why does `ANTHROPIC_API_KEY (real beta key)` connect `Cost Controls & Beta Config` to `Architecture Overview`?**
  _High betweenness centrality (0.019) - this node is a cross-community bridge._
- **What connects `ButtonStyle`, `GET /api/activity`, `GET /api/health` to the rest of the system?**
  _35 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Discord Test Fakes` be split into smaller, more focused modules?**
  _Cohesion score 0.07878787878787878 - nodes in this community are weakly interconnected._
- **Should `Discord Bot Core` be split into smaller, more focused modules?**
  _Cohesion score 0.05689900426742532 - nodes in this community are weakly interconnected._