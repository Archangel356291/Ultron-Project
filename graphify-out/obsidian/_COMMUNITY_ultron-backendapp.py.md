---
type: community
members: 29
---

# ultron-backend/app.py

**Members:** 29 nodes

## Members
- [[NOTE this hits Windows Update and can take several seconds.]] - rationale - ultron-backend/app.py
- [[Best-effort CPU temperature read. Returns None if unavailable — which, on…]] - rationale - ultron-backend/app.py
- [[Count of pending OS updates. Real implementation on both platforms Windows…]] - rationale - ultron-backend/app.py
- [[Live CPUmem per container, keyed by name. Best-effort; returns {} on any…]] - rationale - ultron-backend/app.py
- [[Loads and validates the MCP server list from ULTRON_MCP_CONFIG (a path to a…]] - rationale - ultron-backend/app.py
- [[Return container info via the Docker CLI, avoiding a hard dependency on the…]] - rationale - ultron-backend/app.py
- [[Splits a multi-path env var into a clean list of paths. Windows uses ';' as the…]] - rationale - ultron-backend/app.py
- [[Ultron home lab monitoring backend. Exposes a small JSON API that the dashboard…]] - rationale - ultron-backend/app.py
- [[Validates and normalizes a deploy-container request body. Returns (params,…]] - rationale - ultron-backend/app.py
- [[_containers_data()]] - code - ultron-backend/app.py
- [[_load_mcp_config()]] - code - ultron-backend/app.py
- [[_split_platform_paths()]] - code - ultron-backend/app.py
- [[_status_data()]] - code - ultron-backend/app.py
- [[_systems_data()]] - code - ultron-backend/app.py
- [[_validate_container_name()]] - code - ultron-backend/app.py
- [[_validate_deploy_params()]] - code - ultron-backend/app.py
- [[_validate_image_ref()]] - code - ultron-backend/app.py
- [[_validate_port()]] - code - ultron-backend/app.py
- [[add_cors_headers()]] - code - ultron-backend/app.py
- [[after_request]] - code
- [[containers()]] - code - ultron-backend/app.py
- [[docker_ps()]] - code - ultron-backend/app.py
- [[docker_stats()]] - code - ultron-backend/app.py
- [[get_cpu_temp_c()]] - code - ultron-backend/app.py
- [[get_uptime_str()]] - code - ultron-backend/app.py
- [[pending_os_updates()]] - code - ultron-backend/app.py
- [[status()]] - code - ultron-backend/app.py
- [[systems()]] - code - ultron-backend/app.py
- [[ultron-backendapp.py]] - code - ultron-backend/app.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/ultron-backend/apppy
SORT file.name ASC
```

## Connections to other communities
- 20 edges to [[_COMMUNITY_route]]
- 13 edges to [[_COMMUNITY_require_token]]
- 12 edges to [[_COMMUNITY_action_backup]]
- 11 edges to [[_COMMUNITY_require_role]]
- 9 edges to [[_COMMUNITY_run_ultron_chat]]
- 6 edges to [[_COMMUNITY__mcp_jsonrpc_call]]
- 6 edges to [[_COMMUNITY_scan_container_cves]]
- 4 edges to [[_COMMUNITY_trades_export]]
- 3 edges to [[_COMMUNITY__ensure_mcp_discovered]]
- 3 edges to [[_COMMUNITY_chat]]
- 1 edge to [[_COMMUNITY_anthropic__init__.py]]

## Top bridge nodes
- [[ultron-backendapp.py]] - degree 98, connects to 11 communities
- [[docker_ps()]] - degree 7, connects to 2 communities
- [[containers()]] - degree 5, connects to 2 communities
- [[status()]] - degree 4, connects to 2 communities
- [[systems()]] - degree 4, connects to 2 communities