---
source_file: "ultron-backend/app.py"
type: "code"
community: "CVE Scanning"
location: "L683"
tags:
  - graphify/code
  - graphify/EXTRACTED
  - community/CVE_Scanning
---

# _scan_image_cves()

## Connections
- [[Runs `docker scout cves` for one image. Returns a result dict — never raises.…]] - `rationale_for` [EXTRACTED]
- [[_parse_scout_sarif()]] - `calls` [EXTRACTED]
- [[log_activity()]] - `calls` [EXTRACTED]
- [[scan_container_cves()]] - `calls` [EXTRACTED]
- [[ultron-backendapp.py]] - `contains` [EXTRACTED]

#graphify/code #graphify/EXTRACTED #community/CVE_Scanning