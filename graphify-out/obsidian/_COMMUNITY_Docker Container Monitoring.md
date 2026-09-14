---
type: community
cohesion: 0.33
members: 6
---

# Docker Container Monitoring

**Cohesion:** 0.33 - loosely connected
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
TABLE source_file, type FROM #community/Docker_Container_Monitoring
SORT file.name ASC
```

## Connections to other communities
- 5 edges to [[_COMMUNITY_Backend Core (app.py, Trades)]]
- 3 edges to [[_COMMUNITY_Backend REST Routes]]
- 1 edge to [[_COMMUNITY_BackupDeploy Action Endpoints]]
- 1 edge to [[_COMMUNITY_Activity Log & CVE Scanning]]
- 1 edge to [[_COMMUNITY_System Status & Updates]]

## Top bridge nodes
- [[docker_ps()]] - degree 7, connects to 4 communities
- [[containers()]] - degree 5, connects to 2 communities
- [[_containers_data()]] - degree 4, connects to 1 community
- [[docker_stats()]] - degree 3, connects to 1 community