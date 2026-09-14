---
type: community
cohesion: 0.22
members: 9
---

# Git Repo Status Tools

**Cohesion:** 0.22 - loosely connected
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
TABLE source_file, type FROM #community/Git_Repo_Status_Tools
SORT file.name ASC
```

## Connections to other communities
- 7 edges to [[_COMMUNITY_Backend Core (app.py, Trades)]]
- 6 edges to [[_COMMUNITY_Backend REST Routes]]

## Top bridge nodes
- [[dev_repo_diff()]] - degree 5, connects to 2 communities
- [[dev_repos()]] - degree 5, connects to 2 communities
- [[get_repo_diff()]] - degree 4, connects to 1 community
- [[_run_git()]] - degree 4, connects to 1 community
- [[_find_repo_dir()]] - degree 3, connects to 1 community