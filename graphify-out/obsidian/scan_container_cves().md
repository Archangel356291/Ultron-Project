---
source_file: "ultron-backend/app.py"
type: "code"
community: "log_activity"
location: "L777"
tags:
  - graphify/code
  - graphify/EXTRACTED
  - community/log_activity
---

# scan_container_cves()

## Connections
- [[Scans the images of currently running containers. Capped to CVE_SCAN_MAX_IMAGES…]] - `rationale_for` [EXTRACTED]
- [[_scan_image_cves()]] - `calls` [EXTRACTED]
- [[docker_ps()]] - `calls` [EXTRACTED]
- [[security_cve_scan()]] - `calls` [EXTRACTED]
- [[ultron-backendapp.py]] - `contains` [EXTRACTED]

#graphify/code #graphify/EXTRACTED #community/log_activity