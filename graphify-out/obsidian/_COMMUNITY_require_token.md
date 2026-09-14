---
type: community
members: 13
---

# require_token

**Members:** 13 nodes

## Members
- [[Admin-only. Existing routes are unchanged a valid beta token is a real…]] - rationale - ultron-backend/app.py
- [[Matches only against the pre-configured repo basenames — a caller can never…]] - rationale - ultron-backend/app.py
- [[Runs a read-only git command in repo_path. Returns (stdout, error) — never…]] - rationale - ultron-backend/app.py
- [[_find_repo_dir()]] - code - ultron-backend/app.py
- [[_repo_status()]] - code - ultron-backend/app.py
- [[_run_git()]] - code - ultron-backend/app.py
- [[_storage_data()]] - code - ultron-backend/app.py
- [[dev_repo_diff()]] - code - ultron-backend/app.py
- [[dev_repos()]] - code - ultron-backend/app.py
- [[get_repo_diff()]] - code - ultron-backend/app.py
- [[get_repo_status()]] - code - ultron-backend/app.py
- [[require_token()]] - code - ultron-backend/app.py
- [[storage()]] - code - ultron-backend/app.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/require_token
SORT file.name ASC
```

## Connections to other communities
- 13 edges to [[_COMMUNITY_ultron-backendapp.py]]
- 9 edges to [[_COMMUNITY_route]]
- 2 edges to [[_COMMUNITY_action_backup]]
- 1 edge to [[_COMMUNITY_trades_export]]
- 1 edge to [[_COMMUNITY__ensure_mcp_discovered]]
- 1 edge to [[_COMMUNITY_require_role]]
- 1 edge to [[_COMMUNITY_scan_container_cves]]

## Top bridge nodes
- [[require_token()]] - degree 18, connects to 7 communities
- [[dev_repo_diff()]] - degree 5, connects to 2 communities
- [[dev_repos()]] - degree 5, connects to 2 communities
- [[storage()]] - degree 4, connects to 2 communities
- [[get_repo_diff()]] - degree 4, connects to 1 community