---
type: community
members: 29
---

# app.py

**Members:** 29 nodes

## Members
- [[NOTE this hits Windows Update and can take several seconds.]] - rationale - ultron-backend/app.py
- [[Loads and validates the MCP server list from ULTRON_MCP_CONFIG (a path to a…]] - rationale - ultron-backend/app.py
- [[Pops and returns (params, None) on success, or (None, error_message). Tokens…]] - rationale - ultron-backend/app.py
- [[Splits a multi-path env var into a clean list of paths. Windows uses ';' as the…]] - rationale - ultron-backend/app.py
- [[Turn an SDK content-block object into a plain dict so it can be JSON-returned…]] - rationale - ultron-backend/app.py
- [[Ultron home lab monitoring backend. Exposes a small JSON API that the dashboard…]] - rationale - ultron-backend/app.py
- [[Validates and normalizes a deploy-container request body. Returns (params,…]] - rationale - ultron-backend/app.py
- [[_backup_preview()]] - code - ultron-backend/app.py
- [[_consume_action_token()]] - code - ultron-backend/app.py
- [[_dir_size_bytes()]] - code - ultron-backend/app.py
- [[_load_mcp_config()]] - code - ultron-backend/app.py
- [[_new_action_token()]] - code - ultron-backend/app.py
- [[_parse_beta_tokens()]] - code - ultron-backend/app.py
- [[_prune_expired_tokens_locked()]] - code - ultron-backend/app.py
- [[_run_backup()]] - code - ultron-backend/app.py
- [[_run_deploy_container()]] - code - ultron-backend/app.py
- [[_serialize_block()]] - code - ultron-backend/app.py
- [[_serialize_content()]] - code - ultron-backend/app.py
- [[_split_platform_paths()]] - code - ultron-backend/app.py
- [[_validate_backup_config()]] - code - ultron-backend/app.py
- [[_validate_container_name()]] - code - ultron-backend/app.py
- [[_validate_deploy_params()]] - code - ultron-backend/app.py
- [[_validate_image_ref()]] - code - ultron-backend/app.py
- [[_validate_port()]] - code - ultron-backend/app.py
- [[action_backup()]] - code - ultron-backend/app.py
- [[action_deploy_container()]] - code - ultron-backend/app.py
- [[add_cors_headers()]] - code - ultron-backend/app.py
- [[after_request]] - code
- [[app.py]] - code - ultron-backend/app.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/apppy
SORT file.name ASC
```

## Connections to other communities
- 19 edges to [[_COMMUNITY_route]]
- 14 edges to [[_COMMUNITY__json_result]]
- 11 edges to [[_COMMUNITY_docker_ps]]
- 10 edges to [[_COMMUNITY_run_ultron_chat]]
- 8 edges to [[_COMMUNITY__mcp_jsonrpc_call]]
- 8 edges to [[_COMMUNITY__fifo_engine]]
- 8 edges to [[_COMMUNITY_require_role]]
- 7 edges to [[_COMMUNITY_dev_repo_diff]]
- 1 edge to [[_COMMUNITY_anthropic__init__.py]]

## Top bridge nodes
- [[app.py]] - degree 99, connects to 9 communities
- [[_run_deploy_container()]] - degree 4, connects to 2 communities
- [[action_backup()]] - degree 7, connects to 1 community
- [[action_deploy_container()]] - degree 7, connects to 1 community
- [[_validate_deploy_params()]] - degree 7, connects to 1 community