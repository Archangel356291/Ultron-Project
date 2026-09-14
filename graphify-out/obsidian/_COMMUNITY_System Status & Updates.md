---
type: community
cohesion: 0.25
members: 9
---

# System Status & Updates

**Cohesion:** 0.25 - loosely connected
**Members:** 9 nodes

## Members
- [[Best-effort CPU temperature read. Returns None if unavailable — which, on…]] - rationale - ultron-backend/app.py
- [[Count of pending OS updates. Real implementation on both platforms Windows…]] - rationale - ultron-backend/app.py
- [[_status_data()]] - code - ultron-backend/app.py
- [[_systems_data()]] - code - ultron-backend/app.py
- [[get_cpu_temp_c()]] - code - ultron-backend/app.py
- [[get_uptime_str()]] - code - ultron-backend/app.py
- [[pending_os_updates()]] - code - ultron-backend/app.py
- [[status()]] - code - ultron-backend/app.py
- [[systems()]] - code - ultron-backend/app.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/System_Status__Updates
SORT file.name ASC
```

## Connections to other communities
- 7 edges to [[_COMMUNITY_Backend Core (app.py, Trades)]]
- 4 edges to [[_COMMUNITY_Backend REST Routes]]
- 1 edge to [[_COMMUNITY_Docker Container Monitoring]]

## Top bridge nodes
- [[_status_data()]] - degree 5, connects to 2 communities
- [[status()]] - degree 4, connects to 2 communities
- [[systems()]] - degree 4, connects to 2 communities
- [[_systems_data()]] - degree 5, connects to 1 community
- [[get_cpu_temp_c()]] - degree 4, connects to 1 community