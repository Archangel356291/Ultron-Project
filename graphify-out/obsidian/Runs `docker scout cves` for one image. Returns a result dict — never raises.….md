---
source_file: "ultron-backend/app.py"
type: "rationale"
community: "CVE Scanning"
location: "L684"
tags:
  - graphify/rationale
  - graphify/EXTRACTED
  - community/CVE_Scanning
---

# Runs `docker scout cves` for one image. Returns a result dict — never raises.…

## Connections
- [[_scan_image_cves()]] - `rationale_for` [EXTRACTED]

#graphify/rationale #graphify/EXTRACTED #community/CVE_Scanning