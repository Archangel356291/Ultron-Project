# Graph Report - Ultron Project  (2026-09-14)

## Corpus Check
- 38 files · ~59,063 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 6 file(s) not represented in the graph (top: (none) 6)

## Summary
- 479 nodes · 763 edges · 67 communities (24 shown, 37 thin omitted)
- Extraction: 94% EXTRACTED · 6% INFERRED · 0% AMBIGUOUS · INFERRED: 45 edges (avg confidence: 0.85)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- Discord Bot Command Tests
- discord.py Bot Framework
- Anthropic SDK Fake
- Beta Spend Cap Test & Bug Fixes
- MCP Client & Dispatch
- Discord Slash-Command Framework
- Backend REST Routes
- aiohttp Fake Client
- Backend Core (app.py, Trades)
- Project Docs & Pi Setup
- Backup/Deploy Action Endpoints
- Beta Program & Tailscale Docs
- Chat Auth, Rate Limit & TTS
- Memory & Trend Distillation
- FIFO Trade Engine
- Activity Log & CVE Scanning
- Dev-Tools Fake SDKs
- Git Repo Status Tools
- System Status & Updates
- MCP Design & Bug History
- MCP Test Server Routes
- Docker Container Monitoring
- Discord Bot Core Class
- Auth & Role Resolution
- Memory Feature Tests
- Dashboard Visual Design Spec
- Backup Concurrency Fix
- Community 27
- Community 28
- Community 29
- Community 30
- Community 31
- Community 33
- Community 34
- Community 35
- Community 36
- Community 37
- Community 38
- Community 39
- Community 40
- Community 41
- Community 42
- Community 43
- Community 44
- Community 45
- Community 46
- Community 47
- Community 48
- Community 49
- Community 50
- Community 51
- Community 52
- Community 53
- Community 54
- Community 55
- Community 56
- Community 57
- Community 58
- Community 59
- Community 60
- Community 61

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
10. `APIStatusError` - 9 edges

## Surprising Connections (you probably didn't know these)
- `ultron-discord-bot Service (Docker Compose)` --shares_data_with--> `ultron-discord-bot (Thin Remote-Control Layer)`  [INFERRED]
  docker-compose.yml → README.md
- `Real Safeguards, Not Just Docs` --conceptually_related_to--> `Cost Controls (Budget, Spend Cap, Rate Limit, Caching)`  [INFERRED]
  README.md → ultron-backend/README.md
- `ultron-backend Service (Docker Compose)` --shares_data_with--> `ultron-backend README (Backend API Reference)`  [INFERRED]
  docker-compose.yml → ultron-backend/README.md
- `export_command()` --references--> `Choice`  [EXTRACTED]
  ultron-discord-bot/bot.py → dev-tools/fake_pkgs/discord/__init__.py
- `Claude Code (Anthropic) - AI Pair-Programming Assistant` --conceptually_related_to--> `Project & Conversation Summary (History/Rationale Doc)`  [INFERRED]
  README.md → PROJECT-SUMMARY-FOR-CLAUDE-CODE.md

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Original Four-Agent Spec Plus Emergent Fifth** — project_summary_for_claude_code_ethical_hacking_agent, project_summary_for_claude_code_investment_agent, project_summary_for_claude_code_crypto_trade_agent, project_summary_for_claude_code_home_lab_monitor_agent, project_summary_for_claude_code_coding_subagent [INFERRED 0.85]
- **MCP Discovery/Execution Separation Security Model** — project_summary_for_claude_code_mcp_support, readme_mcp_opt_in_principle, ultron_backend_readme_mcp_external_tools [INFERRED 0.85]
- **Preview-Then-Confirm Pattern Across Current and Planned Actions** — readme_preview_then_confirm_pattern, ultron_backend_readme_action_endpoints, ultron_backend_pi_setup_phase2_plan [INFERRED 0.80]
- **Fake SDKs built to match real SDK shape** — dev_tools_readme_fake_anthropic, dev_tools_readme_fake_discord, dev_tools_readme_fake_aiohttp, ultron_backend_requirements_anthropic, ultron_discord_bot_requirements_discordpy, ultron_discord_bot_requirements_aiohttp [EXTRACTED 1.00]

## Communities (67 total, 37 thin omitted)

### Community 0 - "Discord Bot Command Tests"
Cohesion: 0.09
Nodes (56): button, choices, command, describe, Interaction, Fake interaction for testing command and button handlers directly., event, ask_command() (+48 more)

### Community 1 - "discord.py Bot Framework"
Cohesion: 0.06
Nodes (15): Bot, ButtonStyle, Embed, File, _Followup, HTTPException, Intents, _InteractionResponse (+7 more)

### Community 2 - "Anthropic SDK Fake"
Cohesion: 0.09
Nodes (20): Anthropic, APIConnectionError, APIError, APIStatusError, APITimeoutError, AuthenticationError, BadRequestError, ContentBlock (+12 more)

### Community 3 - "Beta Spend Cap Test & Bug Fixes"
Cohesion: 0.07
Nodes (26): demo(), _queue_reply(), Self-check for the beta-tester $1 spend cap (ULTRON_BETA_MAX_SPEND_USD) and the…, ultron-discord-bot Service (Docker Compose), Bug: Discord backend_get Showed Raw Error Text, Bug: Discord Field-Truncation Off-By-N, Bug: Tool-Registration Ordering (get_llm_usage NameError Risk), Config Value Hardening (Min-1 Clamp on Token/Rate Limits) (+18 more)

### Community 4 - "MCP Client & Dispatch"
Cohesion: 0.08
Nodes (28): _add_cache_breakpoint(), _ensure_mcp_discovered(), get_mcp_tools_and_dispatch(), _log_llm_usage(), _make_mcp_tool_handler(), handler(), _mcp_call_tool(), _mcp_discover_all() (+20 more)

### Community 5 - "Discord Slash-Command Framework"
Cohesion: 0.08
Nodes (8): app_commands, Button, Choice, CommandTree, Matches @discord.ui.button(...). The fake doesn't need the full component-…, ui, decorator(), View

### Community 6 - "Backend REST Routes"
Cohesion: 0.11
Nodes (26): activity(), chat_usage(), connections(), dashboard(), delete_trade(), get_auth_log(), get_llm_usage(), get_mcp_servers() (+18 more)

### Community 7 - "aiohttp Fake Client"
Cohesion: 0.12
Nodes (7): ClientError, ClientSession, ClientTimeout, _MockResponse, Exception, Minimal fake of 'aiohttp' — enough to test bot.py's backend_get/backend_chat…, Test double: configure `.script` with a queue of _MockResponse objects (or an…

### Community 8 - "Backend Core (app.py, Trades)"
Cohesion: 0.16
Nodes (17): add_trade(), get_trades(), Ultron home lab monitoring backend. Exposes a small JSON API that the dashboard…, Validates and normalizes a deploy-container request body. Returns (params,…, Returns (normalized_dict, None) or (None, error_message)., Raw transaction ledger as CSV text., Per-disposal FIFO tax report as CSV text — one row per sell-vs-buy-lot match,…, # NOTE: this hits Windows Update and can take several seconds. (+9 more)

### Community 9 - "Project Docs & Pi Setup"
Cohesion: 0.17
Nodes (14): Master Index (Obsidian Vault Root), ultron-backend Service (Docker Compose), Bug: Startup Script ANTHROPIC_API_KEY UX Trap, Project & Conversation Summary (History/Rationale Doc), Claude Code (Anthropic) - AI Pair-Programming Assistant, README.md (Top-level Architecture & Principles), ultron-backend index (_index.md), Bug: Beta Testers Couldn't See Own Spend (+6 more)

### Community 10 - "Backup/Deploy Action Endpoints"
Cohesion: 0.23
Nodes (12): action_backup(), action_deploy_container(), _backup_preview(), _consume_action_token(), _dir_size_bytes(), _new_action_token(), _prune_expired_tokens_locked(), Pops and returns (params, None) on success, or (None, error_message). Tokens… (+4 more)

### Community 11 - "Beta Program & Tailscale Docs"
Cohesion: 0.27
Nodes (11): $1.00 Lifetime Beta Spend Cap (ULTRON_BETA_MAX_SPEND_USD), file:// Origin fetch() Bug (mobile Chrome Connect button), Tailscale Grants/ACLs (autogroup:self), Tailscale Remote Access, Why Tailscale Instead of Raw WireGuard, Beta Invite Message, Beta Launch Checklist, Beta Tester Guide (+3 more)

### Community 12 - "Chat Auth, Rate Limit & TTS"
Cohesion: 0.22
Nodes (11): _beta_tester_spend_usd(), chat(), _check_rate_limit(), _fish_audio_tts(), Returns None if the request is allowed, or an error message if the caller…, Lifetime spend for one beta tester, in dollars. Returns 0.0 on any read failure…, One TTS request to Fish Audio. Returns (audio_bytes, content_type, error)., Admin or beta_tester. Use only on endpoints in the beta tester's allowed scope… (+3 more)

### Community 13 - "Memory & Trend Distillation"
Cohesion: 0.22
Nodes (10): distill_activity_trends(), _get_db_connection(), _init_db(), Sums input+output tokens (real spend) for calls logged today (local date,…, Best-effort, like log_activity — this runs unattended on a background timer…, Runs distill_activity_trends() once now, then every 24h, in a daemon thread so…, remember_note(), _start_memory_trend_scheduler() (+2 more)

### Community 14 - "FIFO Trade Engine"
Cohesion: 0.20
Nodes (10): _fifo_engine(), get_trade_summary(), get_trade_tax_lots(), Best-effort date -> integer day count, for holding-period math. Never raises;…, The one place FIFO matching happens. Returns both an aggregated per-asset view…, Simplified FIFO realized gain/loss per asset — the aggregated view. See…, Per-disposal detail: each row is one sell matched against one consumed buy lot,…, _trade_date_to_epoch_days() (+2 more)

### Community 15 - "Activity Log & CVE Scanning"
Cohesion: 0.20
Nodes (10): log_activity(), _parse_scout_sarif(), Scans the images of currently running containers. Capped to CVE_SCAN_MAX_IMAGES…, Best-effort logging — never raises. A logging failure (disk full, permissions,…, Defensive SARIF parser: Docker Scout's exact SARIF property layout isn't…, Runs `docker scout cves` for one image. Returns a result dict — never raises.…, scan_container_cves(), _scan_image_cves() (+2 more)

### Community 16 - "Dev-Tools Fake SDKs"
Cohesion: 0.22
Nodes (9): fake_pkgs/aiohttp (aiohttp client fake), fake_pkgs/anthropic (scriptable Anthropic client fake), fake_pkgs/discord (Discord SDK fake), fake_pkgs/ (drop-in fake SDKs), test_mcp_server.py (real protocol-compliant local MCP server), Why this exists as a separate folder (test against real-like dependencies), anthropic (>=1.0.0,<2.0.0), aiohttp (+1 more)

### Community 17 - "Git Repo Status Tools"
Cohesion: 0.22
Nodes (9): dev_repo_diff(), dev_repos(), _find_repo_dir(), get_repo_diff(), get_repo_status(), Runs a read-only git command in repo_path. Returns (stdout, error) — never…, Matches only against the pre-configured repo basenames — a caller can never…, _repo_status() (+1 more)

### Community 18 - "System Status & Updates"
Cohesion: 0.25
Nodes (9): get_cpu_temp_c(), get_uptime_str(), pending_os_updates(), Best-effort CPU temperature read. Returns None if unavailable — which, on…, Count of pending OS updates. Real implementation on both platforms: Windows…, status(), _status_data(), systems() (+1 more)

### Community 19 - "MCP Design & Bug History"
Cohesion: 0.29
Nodes (7): Bug: MCP Empty Notification Response Mishandled, Bug: MCP Response-Size Cap Applied At Wrong Layer, dev-tools/fake_pkgs (Scriptable Fakes for anthropic/discord/aiohttp), MCP Support (External Tool/Plugin System), dev-tools/test_mcp_server.py (Real Protocol-Strict MCP Test Server), MCP Opt-In At the Tool Level, Not Server Level, External Tools (MCP) Section

### Community 20 - "MCP Test Server Routes"
Cohesion: 0.47
Nodes (5): jsonrpc_error(), jsonrpc_result(), mcp_endpoint(), route, A real MCP server for testing app.py's MCP client against genuine JSON-RPC…

### Community 21 - "Docker Container Monitoring"
Cohesion: 0.33
Nodes (6): containers(), _containers_data(), docker_ps(), docker_stats(), Return container info via the Docker CLI, avoiding a hard dependency on the…, Live CPU/mem per container, keyed by name. Best-effort; returns {} on any…

### Community 23 - "Auth & Role Resolution"
Cohesion: 0.50
Nodes (5): Constant-time-ish token check against admin and every registered beta tester.…, wrapper(), wrapper(), _resolve_role(), _touch_presence()

### Community 25 - "Dashboard Visual Design Spec"
Cohesion: 0.67
Nodes (3): Chamfered-Corner UI Design (45° cut panels), --line Panel Border Color Variable, Ultron Dashboard Design Spec

## Knowledge Gaps
- **43 isolated node(s):** `ButtonStyle`, `Ultron Project CLAUDE.md (graphify + vault instructions)`, `Crypto/Trade Record & Tax Agent`, `Home Lab Monitor & Command Router Agent`, `Coding Sub-Agent (Emergent, Not In Original Spec)` (+38 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 207 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **37 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **What connects `ButtonStyle`, `Ultron Project CLAUDE.md (graphify + vault instructions)`, `Crypto/Trade Record & Tax Agent` to the rest of the system?**
  _43 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Discord Bot Command Tests` be split into smaller, more focused modules?**
  _Cohesion score 0.08755760368663594 - nodes in this community are weakly interconnected._
- **Should `discord.py Bot Framework` be split into smaller, more focused modules?**
  _Cohesion score 0.05689900426742532 - nodes in this community are weakly interconnected._
- **Should `Anthropic SDK Fake` be split into smaller, more focused modules?**
  _Cohesion score 0.08571428571428572 - nodes in this community are weakly interconnected._
- **Should `Beta Spend Cap Test & Bug Fixes` be split into smaller, more focused modules?**
  _Cohesion score 0.0735632183908046 - nodes in this community are weakly interconnected._
- **Should `MCP Client & Dispatch` be split into smaller, more focused modules?**
  _Cohesion score 0.082010582010582 - nodes in this community are weakly interconnected._
- **Should `Discord Slash-Command Framework` be split into smaller, more focused modules?**
  _Cohesion score 0.08307692307692308 - nodes in this community are weakly interconnected._