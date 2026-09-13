---
type: community
members: 6
---

# docker_ps

**Members:** 6 nodes

## Members
- [[Live CPUmem per container, keyed by name. Best-effort; returns {} on any…]] - rationale - ultron-backend/app.py
- [[Return container info via the Docker CLI, avoiding a hard dependency on the…]] - rationale - ultron-backend/app.py
- [[_containers_data()]] - code - ultron-backend/app.py
- [[containers()]] - code - ultron-backend/app.py
- [[docker_ps()]] - code - ultron-backend/app.py
- [[docker_stats()]] - code - ultron-backend/app.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/docker_ps
SORT file.name ASC
```

## Connections to other communities
- 6 edges to [[_COMMUNITY_ultron-backendapp.py]]
- 2 edges to [[_COMMUNITY_route]]
- 1 edge to [[_COMMUNITY_log_activity]]
- 1 edge to [[_COMMUNITY_require_token]]
- 1 edge to [[_COMMUNITY__json_result]]

## Top bridge nodes
- [[containers()]] - degree 5, connects to 4 communities
- [[docker_ps()]] - degree 7, connects to 3 communities
- [[_containers_data()]] - degree 4, connects to 1 community
- [[docker_stats()]] - degree 3, connects to 1 community