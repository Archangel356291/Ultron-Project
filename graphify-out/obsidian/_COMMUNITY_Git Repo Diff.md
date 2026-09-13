---
type: community
members: 7
---

# Git Repo Diff

**Members:** 7 nodes

## Members
- [[Matches only against the pre-configured repo basenames — a caller can never…]] - rationale - ultron-backend/app.py
- [[Runs a read-only git command in repo_path. Returns (stdout, error) — never…]] - rationale - ultron-backend/app.py
- [[_find_repo_dir()]] - code - ultron-backend/app.py
- [[_repo_status()]] - code - ultron-backend/app.py
- [[_run_git()]] - code - ultron-backend/app.py
- [[dev_repo_diff()]] - code - ultron-backend/app.py
- [[get_repo_diff()]] - code - ultron-backend/app.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Git_Repo_Diff
SORT file.name ASC
```

## Connections to other communities
- 5 edges to [[_COMMUNITY_Host Status Functions]]
- 4 edges to [[_COMMUNITY_Backend Read Routes]]

## Top bridge nodes
- [[dev_repo_diff()]] - degree 5, connects to 2 communities
- [[_repo_status()]] - degree 3, connects to 2 communities
- [[get_repo_diff()]] - degree 4, connects to 1 community
- [[_run_git()]] - degree 4, connects to 1 community
- [[_find_repo_dir()]] - degree 3, connects to 1 community