---
type: community
cohesion: 0.20
members: 10
---

# Activity Log & CVE Scanning

**Cohesion:** 0.20 - loosely connected
**Members:** 10 nodes

## Members
- [[Best-effort logging — never raises. A logging failure (disk full, permissions,…]] - rationale - ultron-backend/app.py
- [[Defensive SARIF parser Docker Scout's exact SARIF property layout isn't…]] - rationale - ultron-backend/app.py
- [[Runs `docker scout cves` for one image. Returns a result dict — never raises.…]] - rationale - ultron-backend/app.py
- [[Scans the images of currently running containers. Capped to CVE_SCAN_MAX_IMAGES…]] - rationale - ultron-backend/app.py
- [[_parse_scout_sarif()]] - code - ultron-backend/app.py
- [[_scan_image_cves()]] - code - ultron-backend/app.py
- [[_severity_from_score()]] - code - ultron-backend/app.py
- [[log_activity()]] - code - ultron-backend/app.py
- [[scan_container_cves()]] - code - ultron-backend/app.py
- [[security_cve_scan()]] - code - ultron-backend/app.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Activity_Log__CVE_Scanning
SORT file.name ASC
```

## Connections to other communities
- 6 edges to [[_COMMUNITY_Backend Core (app.py, Trades)]]
- 3 edges to [[_COMMUNITY_Backend REST Routes]]
- 2 edges to [[_COMMUNITY_BackupDeploy Action Endpoints]]
- 1 edge to [[_COMMUNITY_Memory & Trend Distillation]]
- 1 edge to [[_COMMUNITY_MCP Client & Dispatch]]
- 1 edge to [[_COMMUNITY_Docker Container Monitoring]]

## Top bridge nodes
- [[log_activity()]] - degree 7, connects to 4 communities
- [[scan_container_cves()]] - degree 5, connects to 2 communities
- [[security_cve_scan()]] - degree 5, connects to 2 communities
- [[_scan_image_cves()]] - degree 5, connects to 1 community
- [[_parse_scout_sarif()]] - degree 4, connects to 1 community