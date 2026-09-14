---
type: community
cohesion: 0.11
members: 26
---

# Backend REST Routes

**Cohesion:** 0.11 - loosely connected
**Members:** 26 nodes

## Members
- [[Admin-only. Existing routes are unchanged a valid beta token is a real…]] - rationale - ultron-backend/app.py
- [[Admin-only who's connected right now — every identity (admin or a beta tester)…]] - rationale - ultron-backend/app.py
- [[Read-only view of every configured server and everything it offers — approved…]] - rationale - ultron-backend/app.py
- [[Real usage summary for today — inputoutputcache tokens, request count, and…]] - rationale - ultron-backend/app.py
- [[Recent login attempts. Platform-aware - Windows Security event log (IDs…]] - rationale - ultron-backend/app.py
- [[Shared response shaping for the many routes below that just wrap a function…]] - rationale - ultron-backend/app.py
- [[_json_result()]] - code - ultron-backend/app.py
- [[_storage_data()]] - code - ultron-backend/app.py
- [[activity()]] - code - ultron-backend/app.py
- [[chat_usage()]] - code - ultron-backend/app.py
- [[connections()]] - code - ultron-backend/app.py
- [[dashboard()]] - code - ultron-backend/app.py
- [[delete_trade()]] - code - ultron-backend/app.py
- [[get_auth_log()]] - code - ultron-backend/app.py
- [[get_llm_usage()]] - code - ultron-backend/app.py
- [[get_mcp_servers()]] - code - ultron-backend/app.py
- [[get_recent_activity()]] - code - ultron-backend/app.py
- [[health()]] - code - ultron-backend/app.py
- [[mcp_servers()]] - code - ultron-backend/app.py
- [[memory()]] - code - ultron-backend/app.py
- [[recall_notes()]] - code - ultron-backend/app.py
- [[require_token()]] - code - ultron-backend/app.py
- [[route_1]] - code
- [[security_auth_log()]] - code - ultron-backend/app.py
- [[storage()]] - code - ultron-backend/app.py
- [[trade_delete()]] - code - ultron-backend/app.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Backend_REST_Routes
SORT file.name ASC
```

## Connections to other communities
- 23 edges to [[_COMMUNITY_Backend Core (app.py, Trades)]]
- 6 edges to [[_COMMUNITY_Git Repo Status Tools]]
- 4 edges to [[_COMMUNITY_BackupDeploy Action Endpoints]]
- 4 edges to [[_COMMUNITY_Memory & Trend Distillation]]
- 4 edges to [[_COMMUNITY_FIFO Trade Engine]]
- 4 edges to [[_COMMUNITY_System Status & Updates]]
- 3 edges to [[_COMMUNITY_Chat Auth, Rate Limit & TTS]]
- 3 edges to [[_COMMUNITY_Activity Log & CVE Scanning]]
- 3 edges to [[_COMMUNITY_Docker Container Monitoring]]
- 1 edge to [[_COMMUNITY_Auth & Role Resolution]]
- 1 edge to [[_COMMUNITY_MCP Client & Dispatch]]

## Top bridge nodes
- [[route_1]] - degree 25, connects to 8 communities
- [[require_token()]] - degree 20, connects to 7 communities
- [[_json_result()]] - degree 14, connects to 5 communities
- [[get_llm_usage()]] - degree 4, connects to 2 communities
- [[get_mcp_servers()]] - degree 4, connects to 2 communities