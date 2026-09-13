---
type: community
members: 11
---

# Architecture Overview

**Members:** 11 nodes

## Members
- [[Ultron Backend Windows Firewall rule]] - document - ultron-backend/REMOTE-ACCESS.md
- [[Flask (=3.0,4.0)]] - code - ultron-backend/requirements.txt
- [[Flask Backend (app.py)]] - concept - PROJECT-SUMMARY-FOR-CLAUDE-CODE.md
- [[GET apihealth]] - document - ultron-backend/README.md
- [[HTMLJS Dashboard]] - concept - PROJECT-SUMMARY-FOR-CLAUDE-CODE.md
- [[LLM Chat Brain (Claude)]] - concept - PROJECT-SUMMARY-FOR-CLAUDE-CODE.md
- [[WMI (==1.5.1, Windows only)]] - code - ultron-backend/requirements.txt
- [[WindowsLinux platform detection (temps, updates, storage mounts)]] - document - ultron-backend/README.md
- [[anthropic (=1.0.0,2.0.0)]] - code - ultron-backend/requirements.txt
- [[fake_pkgsanthropic (scriptable Anthropic client fake)]] - document - dev-tools/README.md
- [[pywin32 (==306, Windows only)]] - code - ultron-backend/requirements.txt

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Architecture_Overview
SORT file.name ASC
```

## Connections to other communities
- 3 edges to [[_COMMUNITY_Dashboard Live Data Fetch]]
- 2 edges to [[_COMMUNITY_Cost Controls & Beta Config]]
- 1 edge to [[_COMMUNITY_Test Infra & MCP Security]]
- 1 edge to [[_COMMUNITY_Backend API & Principles]]
- 1 edge to [[_COMMUNITY_Trade Export & Bot Parity]]
- 1 edge to [[_COMMUNITY_Voice & Chat Dashboard JS]]

## Top bridge nodes
- [[Flask Backend (app.py)]] - degree 9, connects to 2 communities
- [[anthropic (=1.0.0,2.0.0)]] - degree 4, connects to 2 communities
- [[Flask (=3.0,4.0)]] - degree 3, connects to 1 community
- [[LLM Chat Brain (Claude)]] - degree 3, connects to 1 community
- [[fake_pkgsanthropic (scriptable Anthropic client fake)]] - degree 2, connects to 1 community