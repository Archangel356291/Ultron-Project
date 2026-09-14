---
type: community
members: 24
---

# ultron-backend/app.py

**Members:** 24 nodes

## Members
- [[NOTE this hits Windows Update and can take several seconds.]] - rationale - ultron-backend/app.py
- [[Live CPUmem per container, keyed by name. Best-effort; returns {} on any…]] - rationale - ultron-backend/app.py
- [[Loads and validates the MCP server list from ULTRON_MCP_CONFIG (a path to a…]] - rationale - ultron-backend/app.py
- [[Read-only view of every configured server and everything it offers — approved…]] - rationale - ultron-backend/app.py
- [[Return container info via the Docker CLI, avoiding a hard dependency on the…]] - rationale - ultron-backend/app.py
- [[Splits a multi-path env var into a clean list of paths. Windows uses ';' as the…]] - rationale - ultron-backend/app.py
- [[Ultron home lab monitoring backend. Exposes a small JSON API that the dashboard…]] - rationale - ultron-backend/app.py
- [[Validates and normalizes a deploy-container request body. Returns (params,…]] - rationale - ultron-backend/app.py
- [[_containers_data()]] - code - ultron-backend/app.py
- [[_load_mcp_config()]] - code - ultron-backend/app.py
- [[_parse_beta_tokens()]] - code - ultron-backend/app.py
- [[_split_platform_paths()]] - code - ultron-backend/app.py
- [[_validate_container_name()]] - code - ultron-backend/app.py
- [[_validate_deploy_params()]] - code - ultron-backend/app.py
- [[_validate_image_ref()]] - code - ultron-backend/app.py
- [[_validate_port()]] - code - ultron-backend/app.py
- [[add_cors_headers()]] - code - ultron-backend/app.py
- [[after_request]] - code
- [[containers()]] - code - ultron-backend/app.py
- [[docker_ps()]] - code - ultron-backend/app.py
- [[docker_stats()]] - code - ultron-backend/app.py
- [[get_mcp_servers()]] - code - ultron-backend/app.py
- [[mcp_servers()]] - code - ultron-backend/app.py
- [[ultron-backendapp.py]] - code - ultron-backend/app.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/ultron-backend/apppy
SORT file.name ASC
```

## Connections to other communities
- 21 edges to [[_COMMUNITY_route]]
- 16 edges to [[_COMMUNITY_run_ultron_chat]]
- 13 edges to [[_COMMUNITY_action_backup]]
- 8 edges to [[_COMMUNITY__status_data]]
- 8 edges to [[_COMMUNITY__fifo_engine]]
- 8 edges to [[_COMMUNITY_require_role]]
- 7 edges to [[_COMMUNITY__get_db_connection]]
- 6 edges to [[_COMMUNITY_scan_container_cves]]
- 5 edges to [[_COMMUNITY_dev_repo_diff]]
- 1 edge to [[_COMMUNITY_anthropic__init__.py]]

## Top bridge nodes
- [[ultron-backendapp.py]] - degree 99, connects to 10 communities
- [[docker_ps()]] - degree 7, connects to 3 communities
- [[_validate_deploy_params()]] - degree 7, connects to 1 community
- [[containers()]] - degree 5, connects to 1 community
- [[get_mcp_servers()]] - degree 4, connects to 1 community