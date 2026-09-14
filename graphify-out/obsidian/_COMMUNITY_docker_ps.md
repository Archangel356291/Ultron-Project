---
type: community
members: 14
---

# docker_ps

**Members:** 14 nodes

## Members
- [[Defensive SARIF parser Docker Scout's exact SARIF property layout isn't…]] - rationale - ultron-backend/app.py
- [[Live CPUmem per container, keyed by name. Best-effort; returns {} on any…]] - rationale - ultron-backend/app.py
- [[Return container info via the Docker CLI, avoiding a hard dependency on the…]] - rationale - ultron-backend/app.py
- [[Runs `docker scout cves` for one image. Returns a result dict — never raises.…]] - rationale - ultron-backend/app.py
- [[Scans the images of currently running containers. Capped to CVE_SCAN_MAX_IMAGES…]] - rationale - ultron-backend/app.py
- [[_containers_data()]] - code - ultron-backend/app.py
- [[_parse_scout_sarif()]] - code - ultron-backend/app.py
- [[_scan_image_cves()]] - code - ultron-backend/app.py
- [[_severity_from_score()]] - code - ultron-backend/app.py
- [[containers()]] - code - ultron-backend/app.py
- [[docker_ps()]] - code - ultron-backend/app.py
- [[docker_stats()]] - code - ultron-backend/app.py
- [[scan_container_cves()]] - code - ultron-backend/app.py
- [[security_cve_scan()]] - code - ultron-backend/app.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/docker_ps
SORT file.name ASC
```

## Connections to other communities
- 11 edges to [[_COMMUNITY_app.py]]
- 5 edges to [[_COMMUNITY_route]]
- 2 edges to [[_COMMUNITY__json_result]]
- 1 edge to [[_COMMUNITY_run_ultron_chat]]

## Top bridge nodes
- [[containers()]] - degree 5, connects to 3 communities
- [[security_cve_scan()]] - degree 5, connects to 3 communities
- [[docker_ps()]] - degree 7, connects to 2 communities
- [[_scan_image_cves()]] - degree 5, connects to 2 communities
- [[scan_container_cves()]] - degree 5, connects to 1 community