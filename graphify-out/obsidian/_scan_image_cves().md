---
source_file: "ultron-backend/app.py"
type: "code"
community: "docker_ps"
location: "L747"
tags:
  - graphify/code
  - graphify/EXTRACTED
  - community/docker_ps
---

# _scan_image_cves()

## Connections
- [[Runs `docker scout cves` for one image. Returns a result dict — never raises.…]] - `rationale_for` [EXTRACTED]
- [[_parse_scout_sarif()]] - `calls` [EXTRACTED]
- [[app.py]] - `contains` [EXTRACTED]
- [[log_activity()]] - `calls` [EXTRACTED]
- [[scan_container_cves()]] - `calls` [EXTRACTED]

#graphify/code #graphify/EXTRACTED #community/docker_ps