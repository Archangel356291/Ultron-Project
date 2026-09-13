---
type: community
members: 24
---

# Host Status Functions

**Members:** 24 nodes

## Members
- [[Loads and validates the MCP server list from ULTRON_MCP_CONFIG (a path to a…]] - rationale - ultron-backend/app.py
- [[Splits a multi-path env var into a clean list of paths. Windows uses ';' as the…]] - rationale - ultron-backend/app.py
- [[Validates and normalizes a deploy-container request body. Returns (params,…]] - rationale - ultron-backend/app.py
- [[_containers_data()]] - code - ultron-backend/app.py
- [[_load_mcp_config()]] - code - ultron-backend/app.py
- [[_run_deploy_container()]] - code - ultron-backend/app.py
- [[_split_platform_paths()]] - code - ultron-backend/app.py
- [[_status_data()]] - code - ultron-backend/app.py
- [[_systems_data()]] - code - ultron-backend/app.py
- [[_validate_container_name()]] - code - ultron-backend/app.py
- [[_validate_deploy_params()]] - code - ultron-backend/app.py
- [[_validate_image_ref()]] - code - ultron-backend/app.py
- [[_validate_port()]] - code - ultron-backend/app.py
- [[add_cors_headers()]] - code - ultron-backend/app.py
- [[after_request_1]] - code
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
TABLE source_file, type FROM #community/Host_Status_Functions
SORT file.name ASC
```

## Connections to other communities
- 26 edges to [[_COMMUNITY_Backend Read Routes]]
- 13 edges to [[_COMMUNITY_BackupDeploy Action Tokens]]
- 11 edges to [[_COMMUNITY_Trade FIFO Engine]]
- 11 edges to [[_COMMUNITY_MCP Tool Dispatch]]
- 6 edges to [[_COMMUNITY_MCP JSON-RPC Client]]
- 6 edges to [[_COMMUNITY_CVE Scanning]]
- 6 edges to [[_COMMUNITY_Legacy App Status Functions]]
- 5 edges to [[_COMMUNITY_Git Repo Diff]]
- 3 edges to [[_COMMUNITY_Chat Rate Limiting]]
- 2 edges to [[_COMMUNITY_Fish Audio TTS]]

## Top bridge nodes
- [[ultron-backendapp.py]] - degree 93, connects to 10 communities
- [[docker_ps()]] - degree 7, connects to 2 communities
- [[_validate_deploy_params()]] - degree 7, connects to 1 community
- [[containers()]] - degree 5, connects to 1 community
- [[get_cpu_temp_c()]] - degree 4, connects to 1 community