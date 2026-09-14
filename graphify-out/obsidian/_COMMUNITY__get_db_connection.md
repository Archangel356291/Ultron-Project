---
type: community
members: 14
---

# _get_db_connection

**Members:** 14 nodes

## Members
- [[Raw transaction ledger as CSV text.]] - rationale - ultron-backend/app.py
- [[Returns (normalized_dict, None) or (None, error_message).]] - rationale - ultron-backend/app.py
- [[Returns None if the request is allowed, or an error message if the caller…]] - rationale - ultron-backend/app.py
- [[Sums input+output tokens (real spend) for calls logged today (local date,…]] - rationale - ultron-backend/app.py
- [[_check_rate_limit()]] - code - ultron-backend/app.py
- [[_get_db_connection()]] - code - ultron-backend/app.py
- [[_init_db()]] - code - ultron-backend/app.py
- [[_todays_token_usage()]] - code - ultron-backend/app.py
- [[_trades_to_csv()]] - code - ultron-backend/app.py
- [[_validate_trade_input()]] - code - ultron-backend/app.py
- [[add_trade()]] - code - ultron-backend/app.py
- [[chat()]] - code - ultron-backend/app.py
- [[get_trades()]] - code - ultron-backend/app.py
- [[trades()]] - code - ultron-backend/app.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/_get_db_connection
SORT file.name ASC
```

## Connections to other communities
- 11 edges to [[_COMMUNITY_app.py]]
- 4 edges to [[_COMMUNITY_route]]
- 4 edges to [[_COMMUNITY_require_token]]
- 2 edges to [[_COMMUNITY_run_ultron_chat]]
- 2 edges to [[_COMMUNITY__fifo_engine]]

## Top bridge nodes
- [[_get_db_connection()]] - degree 11, connects to 4 communities
- [[chat()]] - degree 6, connects to 3 communities
- [[trades()]] - degree 6, connects to 3 communities
- [[_trades_to_csv()]] - degree 4, connects to 2 communities
- [[add_trade()]] - degree 4, connects to 1 community