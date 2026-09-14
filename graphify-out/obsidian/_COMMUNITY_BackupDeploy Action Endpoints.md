---
type: community
cohesion: 0.23
members: 12
---

# Backup/Deploy Action Endpoints

**Cohesion:** 0.23 - loosely connected
**Members:** 12 nodes

## Members
- [[Pops and returns (params, None) on success, or (None, error_message). Tokens…]] - rationale - ultron-backend/app.py
- [[_backup_preview()]] - code - ultron-backend/app.py
- [[_consume_action_token()]] - code - ultron-backend/app.py
- [[_dir_size_bytes()]] - code - ultron-backend/app.py
- [[_new_action_token()]] - code - ultron-backend/app.py
- [[_prune_expired_tokens_locked()]] - code - ultron-backend/app.py
- [[_run_backup()]] - code - ultron-backend/app.py
- [[_run_backup_locked()]] - code - ultron-backend/app.py
- [[_run_deploy_container()]] - code - ultron-backend/app.py
- [[_validate_backup_config()]] - code - ultron-backend/app.py
- [[action_backup()]] - code - ultron-backend/app.py
- [[action_deploy_container()]] - code - ultron-backend/app.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Backup/Deploy_Action_Endpoints
SORT file.name ASC
```

## Connections to other communities
- 12 edges to [[_COMMUNITY_Backend Core (app.py, Trades)]]
- 4 edges to [[_COMMUNITY_Backend REST Routes]]
- 2 edges to [[_COMMUNITY_Activity Log & CVE Scanning]]
- 1 edge to [[_COMMUNITY_Docker Container Monitoring]]

## Top bridge nodes
- [[_run_deploy_container()]] - degree 4, connects to 3 communities
- [[action_backup()]] - degree 7, connects to 2 communities
- [[action_deploy_container()]] - degree 7, connects to 2 communities
- [[_run_backup_locked()]] - degree 5, connects to 2 communities
- [[_consume_action_token()]] - degree 5, connects to 1 community