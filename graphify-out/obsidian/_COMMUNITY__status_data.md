---
type: community
members: 9
---

# _status_data

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
TABLE source_file, type FROM #community/_status_data
SORT file.name ASC
```

## Connections to other communities
- 7 edges to [[_COMMUNITY_app.py]]
- 2 edges to [[_COMMUNITY_route]]
- 2 edges to [[_COMMUNITY_require_token]]
- 1 edge to [[_COMMUNITY_docker_ps]]

## Top bridge nodes
- [[status()]] - degree 4, connects to 3 communities
- [[systems()]] - degree 4, connects to 3 communities
- [[_status_data()]] - degree 5, connects to 2 communities
- [[_systems_data()]] - degree 5, connects to 1 community
- [[get_cpu_temp_c()]] - degree 4, connects to 1 community