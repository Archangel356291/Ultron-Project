---
source_file: "ultron-backend/app.py"
type: "rationale"
community: "scan_container_cves"
location: "L725"
tags:
  - graphify/rationale
  - graphify/EXTRACTED
  - community/scan_container_cves
---

# Runs `docker scout cves` for one image. Returns a result dict — never raises.…

## Connections
- [[_scan_image_cves()]] - `rationale_for` [EXTRACTED]

#graphify/rationale #graphify/EXTRACTED #community/scan_container_cves