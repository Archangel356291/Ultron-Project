# Graph Report - Ultron Project  (2026-09-13)

## Corpus Check
- 32 files · ~52,041 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 2 file(s) not represented in the graph (top: (none) 2)

## Summary
- 520 nodes · 858 edges · 45 communities (23 shown, 12 thin omitted)
- Extraction: 96% EXTRACTED · 4% INFERRED · 0% AMBIGUOUS · INFERRED: 32 edges (avg confidence: 0.85)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `7dce8b50`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- bot.py
- discord/__init__.py
- anthropic/__init__.py
- POST /api/chat (Ultron's brain)
- View
- app.py
- run_ultron_chat
- start-ultron.ps1
- run_ultron_chat
- require_token
- apiGet
- Flask Backend (app.py)
- docker_ps
- _get_db_connection
- route
- _fifo_engine
- require_role
- Ultron (personal AI home lab system)
- test_mcp_server.py
- dev_repo_diff
- run-bot-bg.ps1
- _fifo_engine
- docker_ps
- Preview-then-confirm action pattern
- _ensure_mcp_discovered
- Testing Ultron — a quick guide
- Financial and legal boundaries are explicit, not implied
- get-tailscale-address.ps1
- GET /api/trades/export
- The Importer (Obsidian plugin)
- .__init__
- Discord backend_get Raw-Error-Text Bug
- Discord Field Truncation Off-by-N Bug
- get_llm_usage Tool Registration Ordering Bug
- Raspberry Pi setup — getting it reachable, phase 1

## God Nodes (most connected - your core abstractions)
1. `require_auth()` - 19 edges
2. `require_token()` - 19 edges
3. `Ultron Backend README` - 19 edges
4. `format_error_embed()` - 17 edges
5. `Ultron Project README` - 15 edges
6. `backend_get()` - 13 edges
7. `_json_result()` - 13 edges
8. `apiGet()` - 13 edges
9. `refreshAll()` - 13 edges
10. `_get_db_connection()` - 12 edges

## Surprising Connections (you probably didn't know these)
- `Flask (>=3.0,<4.0)` --shares_data_with--> `Flask Backend (app.py)`  [INFERRED]
  ultron-backend/requirements.txt → PROJECT-SUMMARY-FOR-CLAUDE-CODE.md
- `pywin32 (==306, Windows only)` --shares_data_with--> `Flask Backend (app.py)`  [INFERRED]
  ultron-backend/requirements.txt → PROJECT-SUMMARY-FOR-CLAUDE-CODE.md
- `WMI (==1.5.1, Windows only)` --shares_data_with--> `Flask Backend (app.py)`  [INFERRED]
  ultron-backend/requirements.txt → PROJECT-SUMMARY-FOR-CLAUDE-CODE.md
- `Ultron Dashboard Design Spec` --references--> `ultron-dashboard.html (single-file dashboard)`  [EXTRACTED]
  ULTRON-DASHBOARD-DESIGN-SPEC.md → ultron-dashboard.html
- `Ultron Discord Bot README` --references--> `Connection/Device Tracking (/api/connections)`  [EXTRACTED]
  ultron-discord-bot/README.md → ultron-backend/README.md

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Fake SDKs built to match real SDK shape** — dev_tools_readme_fake_anthropic, dev_tools_readme_fake_discord, dev_tools_readme_fake_aiohttp, ultron_backend_requirements_anthropic, ultron_discord_bot_requirements_discordpy, ultron_discord_bot_requirements_aiohttp [EXTRACTED 1.00]
- **Beta Tester Cost & Access Guardrails** — concept_beta_tester_role, concept_beta_spend_cap, concept_chat_rate_limit, concept_daily_token_budget, concept_rbac_enforcement [INFERRED 0.85]
- **Dashboard Live Data Refresh Flow** — ultron_dashboard_connectbackend, ultron_dashboard_startpolling, ultron_dashboard_refreshall, ultron_dashboard_apiget, ultron_dashboard_fetchstatus [INFERRED 0.85]
- **Preview-Then-Confirm Action Flow (backup + deploy)** — concept_preview_confirm_pattern, ultron_dashboard_previewdeploy, ultron_dashboard_confirmdeploy, ultron_dashboard_previewbackup, ultron_dashboard_confirmbackup [INFERRED 0.85]

## Communities (45 total, 12 thin omitted)

### Community 0 - "bot.py"
Cohesion: 0.09
Nodes (56): button, Choice, choices, command, describe, event, Interaction, ask_command() (+48 more)

### Community 1 - "discord/__init__.py"
Cohesion: 0.08
Nodes (46): Vault Master Index, Ultron Project CLAUDE.md (graphify + vault instructions), $1.00 Lifetime Beta Spend Cap (ULTRON_BETA_MAX_SPEND_USD), Backend-Served Dashboard Route (GET /), beta_tester RBAC Role, Chamfered-Corner UI Design (45° cut panels), Chat Rate Limit (ULTRON_CHAT_RATE_LIMIT_PER_MINUTE), Connection/Device Tracking (/api/connections) (+38 more)

### Community 2 - "anthropic/__init__.py"
Cohesion: 0.06
Nodes (17): Bot, ButtonStyle, Embed, File, _Followup, HTTPException, Intents, Interaction (+9 more)

### Community 3 - "POST /api/chat (Ultron's brain)"
Cohesion: 0.07
Nodes (23): apiGet(), apiPost(), appendChatBubble(), authHeaders(), connectBackend(), fetchActivity(), fetchConnections(), fetchContainers() (+15 more)

### Community 4 - "View"
Cohesion: 0.10
Nodes (17): Anthropic, APIConnectionError, APIError, APIStatusError, APITimeoutError, AuthenticationError, BadRequestError, ContentBlock (+9 more)

### Community 5 - "app.py"
Cohesion: 0.12
Nodes (26): after_request, action_backup(), action_deploy_container(), add_cors_headers(), _backup_preview(), _consume_action_token(), _dir_size_bytes(), _load_mcp_config() (+18 more)

### Community 6 - "run_ultron_chat"
Cohesion: 0.06
Nodes (35): _add_cache_breakpoint(), _ensure_mcp_discovered(), get_mcp_tools_and_dispatch(), log_activity(), _log_llm_usage(), _make_mcp_tool_handler(), handler(), _mcp_call_tool() (+27 more)

### Community 7 - "start-ultron.ps1"
Cohesion: 0.08
Nodes (8): app_commands, Button, Choice, CommandTree, Matches @discord.ui.button(...). The fake doesn't need the full component-…, ui, decorator(), View

### Community 8 - "run_ultron_chat"
Cohesion: 0.10
Nodes (25): jsonrpc_error(), jsonrpc_result(), mcp_endpoint(), route, A real MCP server for testing app.py's MCP client against genuine JSON-RPC…, Real Action Endpoints (backup, deploy-container), Coding Sub-Agent / Development Tab (git data), Trade CSV Export (transactions + tax-lots) (+17 more)

### Community 9 - "require_token"
Cohesion: 0.12
Nodes (19): activity(), chat_usage(), connections(), delete_trade(), get_auth_log(), get_llm_usage(), get_mcp_servers(), get_recent_activity() (+11 more)

### Community 10 - "apiGet"
Cohesion: 0.12
Nodes (7): ClientError, ClientSession, ClientTimeout, _MockResponse, Exception, Minimal fake of 'aiohttp' — enough to test bot.py's backend_get/backend_chat…, Test double: configure `.script` with a queue of _MockResponse objects (or an…

### Community 11 - "Flask Backend (app.py)"
Cohesion: 0.12
Nodes (15): fake_pkgs/aiohttp (aiohttp client fake), fake_pkgs/anthropic (scriptable Anthropic client fake), fake_pkgs/discord (Discord SDK fake), fake_pkgs/ (drop-in fake SDKs), test_mcp_server.py (real protocol-compliant local MCP server), Why this exists as a separate folder (test against real-like dependencies), Flask Backend (app.py), HTML/JS Dashboard (+7 more)

### Community 12 - "docker_ps"
Cohesion: 0.22
Nodes (9): containers(), _containers_data(), docker_ps(), docker_stats(), Return container info via the Docker CLI, avoiding a hard dependency on the…, Live CPU/mem per container, keyed by name. Best-effort; returns {} on any…, Scans the images of currently running containers. Capped to CVE_SCAN_MAX_IMAGES…, scan_container_cves() (+1 more)

### Community 13 - "_get_db_connection"
Cohesion: 0.25
Nodes (9): add_trade(), _get_db_connection(), get_trades(), _init_db(), Returns (normalized_dict, None) or (None, error_message)., Sums input+output tokens (real spend) for calls logged today (local date,…, _todays_token_usage(), trades() (+1 more)

### Community 14 - "route"
Cohesion: 0.25
Nodes (9): route, _beta_tester_spend_usd(), chat(), _check_rate_limit(), dashboard(), health(), Returns None if the request is allowed, or an error message if the caller…, Lifetime spend for one beta tester, in dollars. Returns 0.0 on any read failure… (+1 more)

### Community 15 - "_fifo_engine"
Cohesion: 0.17
Nodes (12): _fifo_engine(), get_trade_tax_lots(), Best-effort date -> integer day count, for holding-period math. Never raises;…, The one place FIFO matching happens. Returns both an aggregated per-asset view…, Per-disposal detail: each row is one sell matched against one consumed buy lot,…, Raw transaction ledger as CSV text., Per-disposal FIFO tax report as CSV text — one row per sell-vs-buy-lot match,…, _tax_lots_to_csv() (+4 more)

### Community 16 - "require_role"
Cohesion: 0.18
Nodes (13): _fish_audio_tts(), get_trade_summary(), Simplified FIFO realized gain/loss per asset — the aggregated view. See…, One TTS request to Fish Audio. Returns (audio_bytes, content_type, error)., Constant-time-ish token check against admin and every registered beta tester.…, Admin or beta_tester. Use only on endpoints in the beta tester's allowed scope…, require_role(), wrapper() (+5 more)

### Community 17 - "Ultron (personal AI home lab system)"
Cohesion: 0.25
Nodes (9): get_cpu_temp_c(), get_uptime_str(), pending_os_updates(), Best-effort CPU temperature read. Returns None if unavailable — which, on…, Count of pending OS updates. Real implementation on both platforms: Windows…, status(), _status_data(), systems() (+1 more)

### Community 18 - "test_mcp_server.py"
Cohesion: 0.25
Nodes (8): Step 1 — Connect Tailscale, Step 2 — Open Ultron, Step 3 — Connect with your token, Testing Ultron — a quick guide, Trying out the chat, What to report, What you can actually do, What you'll need

### Community 19 - "dev_repo_diff"
Cohesion: 0.22
Nodes (9): dev_repo_diff(), dev_repos(), _find_repo_dir(), get_repo_diff(), get_repo_status(), Runs a read-only git command in repo_path. Returns (stdout, error) — never…, Matches only against the pre-configured repo basenames — a caller can never…, _repo_status() (+1 more)

### Community 20 - "run-bot-bg.ps1"
Cohesion: 0.33
Nodes (6): Color palette (sampled), Layout structure, Recommended next step, Structural/decorative details worth getting right, The one real, actionable color finding, Ultron AI Dashboard — Design Specification (from reference image)

### Community 22 - "docker_ps"
Cohesion: 0.67
Nodes (3): demo(), _queue_reply(), Self-check for the beta-tester $1 spend cap (ULTRON_BETA_MAX_SPEND_USD). Proves…

### Community 44 - "Raspberry Pi setup — getting it reachable, phase 1"
Cohesion: 0.20
Nodes (9): 0. What's already been generated for this, 1. Flash the SD card, 2. First boot and SSH in, 3. Update the OS, 4. Install Tailscale, join the same tailnet, 5. Install Docker, Raspberry Pi setup — getting it reachable, phase 1, Where this leaves things (+1 more)

## Ambiguous Edges - Review These
- `Coding Sub-Agent / Development Tab (git data)` → `Home Lab Monitor & Command Router`  [AMBIGUOUS]
  PROJECT-SUMMARY-FOR-CLAUDE-CODE.md · relation: conceptually_related_to

## Knowledge Gaps
- **54 isolated node(s):** `Why this order`, `0. What's already been generated for this`, `1. Flash the SD card`, `2. First boot and SSH in`, `3. Update the OS` (+49 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 212 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **12 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **What is the exact relationship between `Coding Sub-Agent / Development Tab (git data)` and `Home Lab Monitor & Command Router`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._
- **Why does `app_commands` connect `start-ultron.ps1` to `anthropic/__init__.py`?**
  _High betweenness centrality (0.005) - this node is a cross-community bridge._
- **Why does `Ultron Dashboard Design Spec` connect `discord/__init__.py` to `run-bot-bg.ps1`?**
  _High betweenness centrality (0.004) - this node is a cross-community bridge._
- **What connects `Why this order`, `0. What's already been generated for this`, `1. Flash the SD card` to the rest of the system?**
  _54 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `bot.py` be split into smaller, more focused modules?**
  _Cohesion score 0.0898995240613432 - nodes in this community are weakly interconnected._
- **Should `discord/__init__.py` be split into smaller, more focused modules?**
  _Cohesion score 0.07607843137254902 - nodes in this community are weakly interconnected._
- **Should `anthropic/__init__.py` be split into smaller, more focused modules?**
  _Cohesion score 0.05512820512820513 - nodes in this community are weakly interconnected._