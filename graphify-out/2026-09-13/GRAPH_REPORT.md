# Graph Report - Ultron Project  (2026-09-13)

## Corpus Check
- 21 files · ~50,280 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 510 nodes · 849 edges · 44 communities (22 shown, 12 thin omitted)
- Extraction: 96% EXTRACTED · 4% INFERRED · 0% AMBIGUOUS · INFERRED: 32 edges (avg confidence: 0.85)
- Token cost: 155,630 input · 0 output

## Community Hubs (Navigation)
- Community 0
- Community 1
- Community 2
- Community 3
- Community 4
- Community 5
- Community 6
- Community 7
- Community 8
- Community 9
- Community 10
- Community 11
- Community 12
- Community 13
- Community 14
- Community 15
- Community 16
- Community 17
- Community 18
- Community 19
- Community 20
- Community 21
- Community 22
- Community 23
- Community 24
- Community 26
- Community 28
- Community 29
- Community 30
- Community 31
- Community 32
- Community 33
- Community 34
- Community 35

## God Nodes (most connected - your core abstractions)
1. `require_token()` - 19 edges
2. `require_auth()` - 19 edges
3. `Ultron Backend README` - 19 edges
4. `format_error_embed()` - 17 edges
5. `Ultron Project README` - 15 edges
6. `_json_result()` - 13 edges
7. `backend_get()` - 13 edges
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
- `psutil (>=6.0,<7.0)` --shares_data_with--> `Home Lab Monitor & Command Router`  [INFERRED]
  ultron-backend/requirements.txt → PROJECT-SUMMARY-FOR-CLAUDE-CODE.md

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Fake SDKs built to match real SDK shape** — dev_tools_readme_fake_anthropic, dev_tools_readme_fake_discord, dev_tools_readme_fake_aiohttp, ultron_backend_requirements_anthropic, ultron_discord_bot_requirements_discordpy, ultron_discord_bot_requirements_aiohttp [EXTRACTED 1.00]
- **Beta Tester Cost & Access Guardrails** — concept_beta_tester_role, concept_beta_spend_cap, concept_chat_rate_limit, concept_daily_token_budget, concept_rbac_enforcement [INFERRED 0.85]
- **Dashboard Live Data Refresh Flow** — ultron_dashboard_connectbackend, ultron_dashboard_startpolling, ultron_dashboard_refreshall, ultron_dashboard_apiget, ultron_dashboard_fetchstatus [INFERRED 0.85]
- **Preview-Then-Confirm Action Flow (backup + deploy)** — concept_preview_confirm_pattern, ultron_dashboard_previewdeploy, ultron_dashboard_confirmdeploy, ultron_dashboard_previewbackup, ultron_dashboard_confirmbackup [INFERRED 0.85]

## Communities (44 total, 12 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.09
Nodes (56): button, Choice, choices, command, describe, event, Interaction, ask_command() (+48 more)

### Community 1 - "Community 1"
Cohesion: 0.08
Nodes (47): Vault Master Index, Ultron Project CLAUDE.md (graphify + vault instructions), $1.00 Lifetime Beta Spend Cap (ULTRON_BETA_MAX_SPEND_USD), Backend-Served Dashboard Route (GET /), beta_tester RBAC Role, Chamfered-Corner UI Design (45° cut panels), Chat Rate Limit (ULTRON_CHAT_RATE_LIMIT_PER_MINUTE), Connection/Device Tracking (/api/connections) (+39 more)

### Community 2 - "Community 2"
Cohesion: 0.06
Nodes (17): Bot, ButtonStyle, Embed, File, _Followup, HTTPException, Intents, Interaction (+9 more)

### Community 3 - "Community 3"
Cohesion: 0.07
Nodes (23): apiGet(), apiPost(), appendChatBubble(), authHeaders(), connectBackend(), fetchActivity(), fetchConnections(), fetchContainers() (+15 more)

### Community 4 - "Community 4"
Cohesion: 0.10
Nodes (17): Anthropic, APIConnectionError, APIError, APIStatusError, APITimeoutError, AuthenticationError, BadRequestError, ContentBlock (+9 more)

### Community 5 - "Community 5"
Cohesion: 0.12
Nodes (26): after_request, action_backup(), action_deploy_container(), add_cors_headers(), _backup_preview(), _consume_action_token(), _dir_size_bytes(), _load_mcp_config() (+18 more)

### Community 6 - "Community 6"
Cohesion: 0.08
Nodes (28): _add_cache_breakpoint(), _ensure_mcp_discovered(), get_mcp_tools_and_dispatch(), _log_llm_usage(), _make_mcp_tool_handler(), handler(), _mcp_call_tool(), _mcp_discover_all() (+20 more)

### Community 7 - "Community 7"
Cohesion: 0.08
Nodes (8): app_commands, Button, Choice, CommandTree, Matches @discord.ui.button(...). The fake doesn't need the full component-…, ui, decorator(), View

### Community 8 - "Community 8"
Cohesion: 0.10
Nodes (25): jsonrpc_error(), jsonrpc_result(), mcp_endpoint(), route, A real MCP server for testing app.py's MCP client against genuine JSON-RPC…, Real Action Endpoints (backup, deploy-container), Coding Sub-Agent / Development Tab (git data), Trade CSV Export (transactions + tax-lots) (+17 more)

### Community 9 - "Community 9"
Cohesion: 0.11
Nodes (26): route, activity(), chat_usage(), connections(), dashboard(), delete_trade(), dev_repos(), get_auth_log() (+18 more)

### Community 10 - "Community 10"
Cohesion: 0.12
Nodes (7): ClientError, ClientSession, ClientTimeout, _MockResponse, Exception, Minimal fake of 'aiohttp' — enough to test bot.py's backend_get/backend_chat…, Test double: configure `.script` with a queue of _MockResponse objects (or an…

### Community 11 - "Community 11"
Cohesion: 0.12
Nodes (15): fake_pkgs/aiohttp (aiohttp client fake), fake_pkgs/anthropic (scriptable Anthropic client fake), fake_pkgs/discord (Discord SDK fake), fake_pkgs/ (drop-in fake SDKs), test_mcp_server.py (real protocol-compliant local MCP server), Why this exists as a separate folder (test against real-like dependencies), Flask Backend (app.py), HTML/JS Dashboard (+7 more)

### Community 12 - "Community 12"
Cohesion: 0.14
Nodes (14): containers(), _containers_data(), docker_ps(), docker_stats(), _parse_scout_sarif(), Return container info via the Docker CLI, avoiding a hard dependency on the…, Live CPU/mem per container, keyed by name. Best-effort; returns {} on any…, Defensive SARIF parser: Docker Scout's exact SARIF property layout isn't… (+6 more)

### Community 13 - "Community 13"
Cohesion: 0.20
Nodes (10): add_trade(), get_trades(), Returns (normalized_dict, None) or (None, error_message)., Raw transaction ledger as CSV text., Per-disposal FIFO tax report as CSV text — one row per sell-vs-buy-lot match,…, _tax_lots_to_csv(), trades(), trades_export() (+2 more)

### Community 14 - "Community 14"
Cohesion: 0.22
Nodes (10): _beta_tester_spend_usd(), chat(), _check_rate_limit(), _get_db_connection(), _init_db(), Returns None if the request is allowed, or an error message if the caller…, Lifetime spend for one beta tester, in dollars. Returns 0.0 on any read failure…, Sums input+output tokens (real spend) for calls logged today (local date,… (+2 more)

### Community 15 - "Community 15"
Cohesion: 0.20
Nodes (10): _fifo_engine(), get_trade_summary(), get_trade_tax_lots(), Best-effort date -> integer day count, for holding-period math. Never raises;…, The one place FIFO matching happens. Returns both an aggregated per-asset view…, Simplified FIFO realized gain/loss per asset — the aggregated view. See…, Per-disposal detail: each row is one sell matched against one consumed buy lot,…, _trade_date_to_epoch_days() (+2 more)

### Community 16 - "Community 16"
Cohesion: 0.24
Nodes (10): _fish_audio_tts(), One TTS request to Fish Audio. Returns (audio_bytes, content_type, error)., Constant-time-ish token check against admin and every registered beta tester.…, Admin or beta_tester. Use only on endpoints in the beta tester's allowed scope…, require_role(), wrapper(), wrapper(), _resolve_role() (+2 more)

### Community 17 - "Community 17"
Cohesion: 0.25
Nodes (9): get_cpu_temp_c(), get_uptime_str(), pending_os_updates(), Best-effort CPU temperature read. Returns None if unavailable — which, on…, Count of pending OS updates. Real implementation on both platforms: Windows…, status(), _status_data(), systems() (+1 more)

### Community 18 - "Community 18"
Cohesion: 0.25
Nodes (8): Step 1 — Connect Tailscale, Step 2 — Open Ultron, Step 3 — Connect with your token, Testing Ultron — a quick guide, Trying out the chat, What to report, What you can actually do, What you'll need

### Community 19 - "Community 19"
Cohesion: 0.29
Nodes (7): dev_repo_diff(), _find_repo_dir(), get_repo_diff(), Runs a read-only git command in repo_path. Returns (stdout, error) — never…, Matches only against the pre-configured repo basenames — a caller can never…, _repo_status(), _run_git()

### Community 20 - "Community 20"
Cohesion: 0.33
Nodes (6): Color palette (sampled), Layout structure, Recommended next step, Structural/decorative details worth getting right, The one real, actionable color finding, Ultron AI Dashboard — Design Specification (from reference image)

### Community 22 - "Community 22"
Cohesion: 0.67
Nodes (3): demo(), _queue_reply(), Self-check for the beta-tester $1 spend cap (ULTRON_BETA_MAX_SPEND_USD). Proves…

## Ambiguous Edges - Review These
- `Coding Sub-Agent / Development Tab (git data)` → `Home Lab Monitor & Command Router`  [AMBIGUOUS]
  PROJECT-SUMMARY-FOR-CLAUDE-CODE.md · relation: conceptually_related_to

## Knowledge Gaps
- **46 isolated node(s):** `ButtonStyle`, `Folders`, `Root notes`, `Beta tester invite message`, `Step 1 — Connect Tailscale` (+41 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 203 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **12 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **What is the exact relationship between `Coding Sub-Agent / Development Tab (git data)` and `Home Lab Monitor & Command Router`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._
- **Why does `app_commands` connect `Community 7` to `Community 2`?**
  _High betweenness centrality (0.005) - this node is a cross-community bridge._
- **Why does `Ultron Dashboard Design Spec` connect `Community 1` to `Community 20`?**
  _High betweenness centrality (0.005) - this node is a cross-community bridge._
- **What connects `ButtonStyle`, `Folders`, `Root notes` to the rest of the system?**
  _46 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Community 0` be split into smaller, more focused modules?**
  _Cohesion score 0.0898995240613432 - nodes in this community are weakly interconnected._
- **Should `Community 1` be split into smaller, more focused modules?**
  _Cohesion score 0.07607843137254902 - nodes in this community are weakly interconnected._
- **Should `Community 2` be split into smaller, more focused modules?**
  _Cohesion score 0.05512820512820513 - nodes in this community are weakly interconnected._