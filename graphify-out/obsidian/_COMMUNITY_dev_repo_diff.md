---
type: community
members: 9
---

# dev_repo_diff

**Members:** 9 nodes

## Members
- [[Matches only against the pre-configured repo basenames — a caller can never…]] - rationale - ultron-backend/app.py
- [[Runs a read-only git command in repo_path. Returns (stdout, error) — never…]] - rationale - ultron-backend/app.py
- [[_find_repo_dir()]] - code - ultron-backend/app.py
- [[_repo_status()]] - code - ultron-backend/app.py
- [[_run_git()]] - code - ultron-backend/app.py
- [[dev_repo_diff()]] - code - ultron-backend/app.py
- [[dev_repos()]] - code - ultron-backend/app.py
- [[get_repo_diff()]] - code - ultron-backend/app.py
- [[get_repo_status()]] - code - ultron-backend/app.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/dev_repo_diff
SORT file.name ASC
```

## Connections to other communities
- 7 edges to [[_COMMUNITY_app.py]]
- 4 edges to [[_COMMUNITY_route]]
- 2 edges to [[_COMMUNITY__json_result]]

## Top bridge nodes
- [[dev_repo_diff()]] - degree 5, connects to 3 communities
- [[dev_repos()]] - degree 5, connects to 3 communities
- [[get_repo_diff()]] - degree 4, connects to 1 community
- [[_run_git()]] - degree 4, connects to 1 community
- [[_find_repo_dir()]] - degree 3, connects to 1 community