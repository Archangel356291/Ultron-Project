---
type: community
members: 13
---

# action_backup

**Members:** 13 nodes

## Members
- [[Best-effort logging — never raises. A logging failure (disk full, permissions,…]] - rationale - ultron-backend/app.py
- [[Pops and returns (params, None) on success, or (None, error_message). Tokens…]] - rationale - ultron-backend/app.py
- [[_backup_preview()]] - code - ultron-backend/app.py
- [[_consume_action_token()]] - code - ultron-backend/app.py
- [[_dir_size_bytes()]] - code - ultron-backend/app.py
- [[_new_action_token()]] - code - ultron-backend/app.py
- [[_prune_expired_tokens_locked()]] - code - ultron-backend/app.py
- [[_run_backup()]] - code - ultron-backend/app.py
- [[_run_deploy_container()]] - code - ultron-backend/app.py
- [[_validate_backup_config()]] - code - ultron-backend/app.py
- [[action_backup()]] - code - ultron-backend/app.py
- [[action_deploy_container()]] - code - ultron-backend/app.py
- [[log_activity()]] - code - ultron-backend/app.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/action_backup
SORT file.name ASC
```

## Connections to other communities
- 13 edges to [[_COMMUNITY_app.py]]
- 4 edges to [[_COMMUNITY_route]]
- 1 edge to [[_COMMUNITY_scan_container_cves]]
- 1 edge to [[_COMMUNITY__get_db_connection]]
- 1 edge to [[_COMMUNITY_run_ultron_chat]]

## Top bridge nodes
- [[log_activity()]] - degree 7, connects to 4 communities
- [[action_backup()]] - degree 7, connects to 2 communities
- [[action_deploy_container()]] - degree 7, connects to 2 communities
- [[_consume_action_token()]] - degree 5, connects to 1 community
- [[_run_backup()]] - degree 5, connects to 1 community