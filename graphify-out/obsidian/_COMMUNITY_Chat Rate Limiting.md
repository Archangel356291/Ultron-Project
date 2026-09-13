---
type: community
members: 5
---

# Chat Rate Limiting

**Members:** 5 nodes

## Members
- [[Returns None if the request is allowed, or an error message if the caller…]] - rationale - ultron-backend/app.py
- [[Sums input+output tokens (real spend) for calls logged today (local date,…]] - rationale - ultron-backend/app.py
- [[_check_rate_limit()]] - code - ultron-backend/app.py
- [[_todays_token_usage()]] - code - ultron-backend/app.py
- [[chat()]] - code - ultron-backend/app.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Chat_Rate_Limiting
SORT file.name ASC
```

## Connections to other communities
- 3 edges to [[_COMMUNITY_Host Status Functions]]
- 2 edges to [[_COMMUNITY_Backend Read Routes]]
- 1 edge to [[_COMMUNITY_Trade FIFO Engine]]
- 1 edge to [[_COMMUNITY_MCP Tool Dispatch]]

## Top bridge nodes
- [[chat()]] - degree 6, connects to 3 communities
- [[_todays_token_usage()]] - degree 4, connects to 2 communities
- [[_check_rate_limit()]] - degree 3, connects to 1 community