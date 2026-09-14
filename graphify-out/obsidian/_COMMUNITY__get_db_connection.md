---
type: community
members: 10
---

# _get_db_connection

**Members:** 10 nodes

## Members
- [[Real usage summary for today — inputoutputcache tokens, request count, and…]] - rationale - ultron-backend/app.py
- [[Returns None if the request is allowed, or an error message if the caller…]] - rationale - ultron-backend/app.py
- [[Sums input+output tokens (real spend) for calls logged today (local date,…]] - rationale - ultron-backend/app.py
- [[_check_rate_limit()]] - code - ultron-backend/app.py
- [[_get_db_connection()]] - code - ultron-backend/app.py
- [[_init_db()]] - code - ultron-backend/app.py
- [[_todays_token_usage()]] - code - ultron-backend/app.py
- [[chat()]] - code - ultron-backend/app.py
- [[chat_usage()]] - code - ultron-backend/app.py
- [[get_llm_usage()]] - code - ultron-backend/app.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/_get_db_connection
SORT file.name ASC
```

## Connections to other communities
- 8 edges to [[_COMMUNITY_ultron-backendapp.py]]
- 6 edges to [[_COMMUNITY_route]]
- 2 edges to [[_COMMUNITY_run_ultron_chat]]
- 2 edges to [[_COMMUNITY_trades]]
- 1 edge to [[_COMMUNITY_require_role]]
- 1 edge to [[_COMMUNITY__fifo_engine]]

## Top bridge nodes
- [[_get_db_connection()]] - degree 11, connects to 5 communities
- [[chat()]] - degree 6, connects to 4 communities
- [[chat_usage()]] - degree 5, connects to 2 communities
- [[get_llm_usage()]] - degree 4, connects to 1 community
- [[_todays_token_usage()]] - degree 4, connects to 1 community