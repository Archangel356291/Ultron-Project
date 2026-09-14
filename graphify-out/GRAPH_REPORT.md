# Graph Report - Ultron Project  (2026-09-13)

## Corpus Check
- 27 files · ~45,147 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 2 file(s) not represented in the graph (top: (none) 2)

## Summary
- 522 nodes · 861 edges · 42 communities (21 shown, 14 thin omitted)
- Extraction: 93% EXTRACTED · 7% INFERRED · 0% AMBIGUOUS · INFERRED: 57 edges (avg confidence: 0.87)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `773954ca`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- bot.py
- discord/__init__.py
- anthropic/__init__.py
- POST /api/chat (Ultron's brain)
- View
- require_token
- run_ultron_chat
- ClientSession
- apiGet
- _get_db_connection
- fake_pkgs/ (drop-in fake SDKs)
- app.py
- _status_data
- Ultron (personal AI home lab system)
- _fifo_engine
- docker_ps
- Preview-then-confirm action pattern
- _ensure_mcp_discovered
- route
- _index.md
- Config Value Floor Hardening
- Financial and legal boundaries are explicit, not implied
- GET /api/trades/export
- The Importer (Obsidian plugin)
- .__init__
- Discord backend_get Raw-Error-Text Bug
- Discord Field Truncation Off-by-N Bug
- get_llm_usage Tool Registration Ordering Bug
- Nothing works until explicitly configured
- GET /api/security/cve-scan
- Running permanently at startup (Task Scheduler/NSSM)
- /forget command
- require_auth (Discord ID allowlist check)
- CLAUDE.md
- _mcp_jsonrpc_call

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
- `MCP (external tool/plugin) Support` --conceptually_related_to--> `ULTRON_MCP_CONFIG (optional MCP feature)`  [INFERRED]
  PROJECT-SUMMARY-FOR-CLAUDE-CODE.md → ultron-backend/BETA-LAUNCH-CHECKLIST.md
- `fetchDevRepos()` --shares_data_with--> `get_repo_diff Chat Tool (parameterized)`  [INFERRED]
  ultron-dashboard.html → PROJECT-SUMMARY-FOR-CLAUDE-CODE.md
- `Coding Sub-Agent / Development Tab (git data)` --conceptually_related_to--> `Development Tab Feature (ULTRON_CODE_REPOS)`  [INFERRED]
  PROJECT-SUMMARY-FOR-CLAUDE-CODE.md → ultron-backend/BETA-LAUNCH-CHECKLIST.md
- `confirmBackup()` --shares_data_with--> `Real Action Endpoints (backup, deploy-container)`  [INFERRED]
  ultron-dashboard.html → PROJECT-SUMMARY-FOR-CLAUDE-CODE.md
- `pywin32 (==306, Windows only)` --shares_data_with--> `Flask Backend (app.py)`  [INFERRED]
  ultron-backend/requirements.txt → PROJECT-SUMMARY-FOR-CLAUDE-CODE.md

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Fake SDKs built to match real SDK shape** — dev_tools_readme_fake_anthropic, dev_tools_readme_fake_discord, dev_tools_readme_fake_aiohttp, ultron_backend_requirements_anthropic, ultron_discord_bot_requirements_discordpy, ultron_discord_bot_requirements_aiohttp [EXTRACTED 1.00]
- **MCP opt-in security model participants** — ultron_backend_readme_mcp_security_model, ultron_backend_readme_api_mcp_servers, dev_tools_readme_test_mcp_server, ultron_dashboard_loadmcpservers, ultron_discord_bot_readme_mcp_cmd [EXTRACTED 1.00]
- **Preview-then-confirm action pattern across backend, dashboard, and bot** — ultron_backend_readme_preview_confirm_pattern, ultron_backend_readme_api_actions_backup, ultron_backend_readme_api_actions_deploy_container, ultron_discord_bot_readme_backup_cmd, ultron_discord_bot_readme_deploy_cmd, ultron_dashboard_previewbackup, ultron_dashboard_previewdeploy [EXTRACTED 1.00]
- **AI Assistant Chat Flow** — ultron_dashboard_sendchatmessage, ultron_dashboard_postchat, ultron_dashboard_appendchatbubble, ultron_dashboard_speakreply, ultron_dashboard_togglevoiceinput, ultron_dashboard_sendfromhome [INFERRED 0.80]
- **Dashboard Live Data Refresh Flow** — ultron_dashboard_refreshall, ultron_dashboard_fetchstatus, ultron_dashboard_fetchcontainers, ultron_dashboard_fetchstorage, ultron_dashboard_fetchsystems, ultron_dashboard_fetchactivity, ultron_dashboard_fetchdevrepos, ultron_dashboard_fetchtrades, ultron_dashboard_fetchllmusage [INFERRED 0.85]
- **Preview-Confirm Action Flow (deploy & backup)** — ultron_dashboard_previewdeploy, ultron_dashboard_confirmdeploy, ultron_dashboard_canceldeploy, ultron_dashboard_previewbackup, ultron_dashboard_confirmbackup, ultron_dashboard_cancelbackup, project_summary_for_claude_code_action_endpoints [INFERRED 0.85]

## Communities (42 total, 14 thin omitted)

### Community 0 - "bot.py"
Cohesion: 0.09
Nodes (54): button, choices, command, describe, Interaction, Fake interaction for testing command and button handlers directly., event, ask_command() (+46 more)

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

### Community 5 - "require_token"
Cohesion: 0.11
Nodes (23): activity(), chat_usage(), delete_trade(), dev_repo_diff(), dev_repos(), _find_repo_dir(), get_auth_log(), get_llm_usage() (+15 more)

### Community 8 - "run_ultron_chat"
Cohesion: 0.14
Nodes (15): _add_cache_breakpoint(), get_mcp_tools_and_dispatch(), _log_llm_usage(), _make_mcp_tool_handler(), handler(), _mcp_call_tool(), Best-effort — never raises. A logging failure must not break the chat response…, Closure matching the same handler(**kwargs) -> dict contract every internal… (+7 more)

### Community 9 - "ClientSession"
Cohesion: 0.12
Nodes (7): ClientError, ClientSession, ClientTimeout, _MockResponse, Exception, Minimal fake of 'aiohttp' — enough to test bot.py's backend_get/backend_chat…, Test double: configure `.script` with a queue of _MockResponse objects (or an…

### Community 10 - "apiGet"
Cohesion: 0.05
Nodes (60): fake_pkgs/anthropic (scriptable Anthropic client fake), Real Action Endpoints (backup, deploy-container), Real Activity Log (SQLite-backed), Flask Backend (app.py), Cost Controls (caching, token budget, rate limit), Trade CSV Export (transactions + tax-lots), HTML/JS Dashboard, Discord Bot (bot.py) (+52 more)

### Community 12 - "_get_db_connection"
Cohesion: 0.15
Nodes (14): add_trade(), chat(), _check_rate_limit(), _get_db_connection(), get_trades(), _init_db(), Returns (normalized_dict, None) or (None, error_message)., Raw transaction ledger as CSV text. (+6 more)

### Community 13 - "fake_pkgs/ (drop-in fake SDKs)"
Cohesion: 0.15
Nodes (14): fake_pkgs/aiohttp (aiohttp client fake), fake_pkgs/discord (Discord SDK fake), fake_pkgs/ (drop-in fake SDKs), test_mcp_server.py (real protocol-compliant local MCP server), Why this exists as a separate folder (test against real-like dependencies), MCP is opt-in at the tool level, not the server level, Testing approach (test against real dependency behavior), External tools (MCP) security model (+6 more)

### Community 14 - "app.py"
Cohesion: 0.12
Nodes (26): after_request, action_backup(), action_deploy_container(), add_cors_headers(), _backup_preview(), _consume_action_token(), _dir_size_bytes(), _load_mcp_config() (+18 more)

### Community 16 - "_status_data"
Cohesion: 0.25
Nodes (9): get_cpu_temp_c(), get_uptime_str(), pending_os_updates(), Best-effort CPU temperature read. Returns None if unavailable — which, on…, Count of pending OS updates. Real implementation on both platforms: Windows…, status(), _status_data(), systems() (+1 more)

### Community 17 - "Ultron (personal AI home lab system)"
Cohesion: 0.08
Nodes (31): jsonrpc_error(), jsonrpc_result(), mcp_endpoint(), route, A real MCP server for testing app.py's MCP client against genuine JSON-RPC…, Coding Sub-Agent / Development Tab (git data), dev-tools/README.md, Ethical Hacking Agent (refused outright) (+23 more)

### Community 21 - "_fifo_engine"
Cohesion: 0.20
Nodes (10): _fifo_engine(), get_trade_summary(), Best-effort date -> integer day count, for holding-period math. Never raises;…, The one place FIFO matching happens. Returns both an aggregated per-asset view…, Simplified FIFO realized gain/loss per asset — the aggregated view. See…, Per-disposal FIFO tax report as CSV text — one row per sell-vs-buy-lot match,…, _tax_lots_to_csv(), _trade_date_to_epoch_days() (+2 more)

### Community 22 - "docker_ps"
Cohesion: 0.14
Nodes (14): containers(), _containers_data(), docker_ps(), docker_stats(), _parse_scout_sarif(), Return container info via the Docker CLI, avoiding a hard dependency on the…, Live CPU/mem per container, keyed by name. Best-effort; returns {} on any…, Defensive SARIF parser: Docker Scout's exact SARIF property layout isn't… (+6 more)

### Community 23 - "Preview-then-confirm action pattern"
Cohesion: 0.52
Nodes (7): Destructive host actions require a human-confirmed token, POST /api/actions/backup, POST /api/actions/deploy-container, Preview-then-confirm action pattern, /backup command, /deploy command, Confirm/Cancel button flow (bot action commands)

### Community 24 - "_ensure_mcp_discovered"
Cohesion: 0.40
Nodes (5): _ensure_mcp_discovered(), get_mcp_servers(), mcp_servers(), Runs discovery at most once, lazily, on first use — not at module import time.…, Read-only view of every configured server and everything it offers — approved…

### Community 25 - "route"
Cohesion: 0.13
Nodes (18): dashboard(), _fish_audio_tts(), get_trade_tax_lots(), health(), route, Per-disposal detail: each row is one sell matched against one consumed buy lot,…, One TTS request to Fish Audio. Returns (audio_bytes, content_type, error)., Constant-time-ish token check against admin and every registered beta tester.… (+10 more)

### Community 26 - "_index.md"
Cohesion: 0.10
Nodes (16): Folders, Master Index, Root notes, Beta testers, How someone gets added, Roster, What's still not covered, 2026-09-13 — clean pass, no bugs found (+8 more)

### Community 51 - "_mcp_jsonrpc_call"
Cohesion: 0.28
Nodes (9): _mcp_discover_all(), _mcp_http_post(), _mcp_initialize(), _mcp_jsonrpc_call(), _mcp_list_tools(), MCPError, Exception, One raw JSON-RPC POST. Hard timeout, hard response-size cap. Handles both a… (+1 more)

## Ambiguous Edges - Review These
- `Coding Sub-Agent / Development Tab (git data)` → `Home Lab Monitor & Command Router`  [AMBIGUOUS]
  PROJECT-SUMMARY-FOR-CLAUDE-CODE.md · relation: conceptually_related_to

## Knowledge Gaps
- **48 isolated node(s):** `ButtonStyle`, `graphify`, `Hand-written notes (vault)`, `The one real, actionable color finding`, `Layout structure` (+43 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 193 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **14 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **What is the exact relationship between `Coding Sub-Agent / Development Tab (git data)` and `Home Lab Monitor & Command Router`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._
- **Why does `anthropic (>=1.0.0,<2.0.0)` connect `apiGet` to `POST /api/chat (Ultron's brain)`?**
  _High betweenness centrality (0.040) - this node is a cross-community bridge._
- **Why does `POST /api/chat (Ultron's brain)` connect `POST /api/chat (Ultron's brain)` to `apiGet`, `fake_pkgs/ (drop-in fake SDKs)`?**
  _High betweenness centrality (0.036) - this node is a cross-community bridge._
- **Why does `Phase 1 Status (complete, 2026-09-13)` connect `apiGet` to `Ultron (personal AI home lab system)`, `_index.md`?**
  _High betweenness centrality (0.033) - this node is a cross-community bridge._
- **What connects `ButtonStyle`, `graphify`, `Hand-written notes (vault)` to the rest of the system?**
  _48 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `bot.py` be split into smaller, more focused modules?**
  _Cohesion score 0.08907103825136611 - nodes in this community are weakly interconnected._
- **Should `discord/__init__.py` be split into smaller, more focused modules?**
  _Cohesion score 0.05689900426742532 - nodes in this community are weakly interconnected._