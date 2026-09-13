---
type: community
members: 22
---

# Legacy App Status Functions

**Members:** 22 nodes

## Members
- [[NOTE this hits Windows Update and can take several seconds.]] - rationale - app.py
- [[Best-effort CPU temperature read. Returns None if unavailable — which, on…]] - rationale - app.py
- [[Count of pending OS updates. Real implementation on both platforms Windows…]] - rationale - app.py
- [[Live CPUmem per container, keyed by name. Best-effort; returns {} on any…]] - rationale - app.py
- [[Return container info via the Docker CLI, avoiding a hard dependency on the…]] - rationale - app.py
- [[Ultron home lab monitoring backend. Exposes a small JSON API that the dashboard…]] - rationale - app.py
- [[add_cors_headers()_1]] - code - app.py
- [[after_request_2]] - code
- [[app.py]] - code - app.py
- [[containers()_1]] - code - app.py
- [[docker_ps()_1]] - code - app.py
- [[docker_stats()_1]] - code - app.py
- [[get_cpu_temp_c()_1]] - code - app.py
- [[get_uptime_str()_1]] - code - app.py
- [[health()_1]] - code - app.py
- [[pending_os_updates()_1]] - code - app.py
- [[require_token()_1]] - code - app.py
- [[route_2]] - code
- [[status()_1]] - code - app.py
- [[storage()_1]] - code - app.py
- [[systems()_1]] - code - app.py
- [[wrapper()_1]] - code - app.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Legacy_App_Status_Functions
SORT file.name ASC
```

## Connections to other communities
- 6 edges to [[_COMMUNITY_Host Status Functions]]

## Top bridge nodes
- [[Ultron home lab monitoring backend. Exposes a small JSON API that the dashboard…]] - degree 2, connects to 1 community
- [[Best-effort CPU temperature read. Returns None if unavailable — which, on…]] - degree 2, connects to 1 community
- [[Return container info via the Docker CLI, avoiding a hard dependency on the…]] - degree 2, connects to 1 community
- [[Live CPUmem per container, keyed by name. Best-effort; returns {} on any…]] - degree 2, connects to 1 community
- [[Count of pending OS updates. Real implementation on both platforms Windows…]] - degree 2, connects to 1 community