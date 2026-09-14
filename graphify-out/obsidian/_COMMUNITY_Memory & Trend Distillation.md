---
type: community
cohesion: 0.22
members: 10
---

# Memory & Trend Distillation

**Cohesion:** 0.22 - loosely connected
**Members:** 10 nodes

## Members
- [[Best-effort, like log_activity — this runs unattended on a background timer…]] - rationale - ultron-backend/app.py
- [[Runs distill_activity_trends() once now, then every 24h, in a daemon thread so…]] - rationale - ultron-backend/app.py
- [[Sums input+output tokens (real spend) for calls logged today (local date,…]] - rationale - ultron-backend/app.py
- [[_get_db_connection()]] - code - ultron-backend/app.py
- [[_init_db()]] - code - ultron-backend/app.py
- [[_loop()]] - code - ultron-backend/app.py
- [[_start_memory_trend_scheduler()]] - code - ultron-backend/app.py
- [[_todays_token_usage()]] - code - ultron-backend/app.py
- [[distill_activity_trends()]] - code - ultron-backend/app.py
- [[remember_note()]] - code - ultron-backend/app.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Memory__Trend_Distillation
SORT file.name ASC
```

## Connections to other communities
- 8 edges to [[_COMMUNITY_Backend Core (app.py, Trades)]]
- 4 edges to [[_COMMUNITY_Backend REST Routes]]
- 2 edges to [[_COMMUNITY_Chat Auth, Rate Limit & TTS]]
- 1 edge to [[_COMMUNITY_FIFO Trade Engine]]
- 1 edge to [[_COMMUNITY_Activity Log & CVE Scanning]]
- 1 edge to [[_COMMUNITY_MCP Client & Dispatch]]

## Top bridge nodes
- [[_get_db_connection()]] - degree 15, connects to 6 communities
- [[_todays_token_usage()]] - degree 4, connects to 2 communities
- [[distill_activity_trends()]] - degree 5, connects to 1 community
- [[remember_note()]] - degree 3, connects to 1 community
- [[_start_memory_trend_scheduler()]] - degree 3, connects to 1 community