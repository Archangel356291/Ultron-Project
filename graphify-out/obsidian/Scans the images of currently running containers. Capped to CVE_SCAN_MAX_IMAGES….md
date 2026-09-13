---
source_file: "ultron-backend/app.py"
type: "rationale"
community: "CVE Scanning"
location: "L737"
tags:
  - graphify/rationale
  - graphify/EXTRACTED
  - community/CVE_Scanning
---

# Scans the images of currently running containers. Capped to CVE_SCAN_MAX_IMAGES…

## Connections
- [[scan_container_cves()]] - `rationale_for` [EXTRACTED]

#graphify/rationale #graphify/EXTRACTED #community/CVE_Scanning