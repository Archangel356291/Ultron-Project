---
source_file: "ultron-backend/app.py"
type: "code"
community: "docker_ps"
location: "L800"
tags:
  - graphify/code
  - graphify/EXTRACTED
  - community/docker_ps
---

# scan_container_cves()

## Connections
- [[Scans the images of currently running containers. Capped to CVE_SCAN_MAX_IMAGES…]] - `rationale_for` [EXTRACTED]
- [[_scan_image_cves()]] - `calls` [EXTRACTED]
- [[app.py]] - `contains` [EXTRACTED]
- [[docker_ps()]] - `calls` [EXTRACTED]
- [[security_cve_scan()]] - `calls` [EXTRACTED]

#graphify/code #graphify/EXTRACTED #community/docker_ps