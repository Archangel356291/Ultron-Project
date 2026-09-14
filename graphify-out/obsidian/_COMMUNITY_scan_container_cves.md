---
type: community
members: 8
---

# scan_container_cves

**Members:** 8 nodes

## Members
- [[Defensive SARIF parser Docker Scout's exact SARIF property layout isn't…]] - rationale - ultron-backend/app.py
- [[Runs `docker scout cves` for one image. Returns a result dict — never raises.…]] - rationale - ultron-backend/app.py
- [[Scans the images of currently running containers. Capped to CVE_SCAN_MAX_IMAGES…]] - rationale - ultron-backend/app.py
- [[_parse_scout_sarif()]] - code - ultron-backend/app.py
- [[_scan_image_cves()]] - code - ultron-backend/app.py
- [[_severity_from_score()]] - code - ultron-backend/app.py
- [[scan_container_cves()]] - code - ultron-backend/app.py
- [[security_cve_scan()]] - code - ultron-backend/app.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/scan_container_cves
SORT file.name ASC
```

## Connections to other communities
- 6 edges to [[_COMMUNITY_ultron-backendapp.py]]
- 3 edges to [[_COMMUNITY_route]]
- 1 edge to [[_COMMUNITY_action_backup]]

## Top bridge nodes
- [[_scan_image_cves()]] - degree 5, connects to 2 communities
- [[security_cve_scan()]] - degree 5, connects to 2 communities
- [[scan_container_cves()]] - degree 5, connects to 1 community
- [[_parse_scout_sarif()]] - degree 4, connects to 1 community
- [[_severity_from_score()]] - degree 2, connects to 1 community