---
type: community
members: 11
---

# action_backup

**Members:** 11 nodes

## Members
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

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/action_backup
SORT file.name ASC
```

## Connections to other communities
- 12 edges to [[_COMMUNITY_ultron-backendapp.py]]
- 2 edges to [[_COMMUNITY_require_token]]
- 2 edges to [[_COMMUNITY_route]]
- 2 edges to [[_COMMUNITY_run_ultron_chat]]

## Top bridge nodes
- [[action_backup()]] - degree 7, connects to 3 communities
- [[action_deploy_container()]] - degree 7, connects to 3 communities
- [[_run_backup()]] - degree 5, connects to 2 communities
- [[_run_deploy_container()]] - degree 4, connects to 2 communities
- [[_consume_action_token()]] - degree 5, connects to 1 community