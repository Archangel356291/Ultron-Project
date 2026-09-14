---
type: community
members: 9
---

# _get_db_connection

**Members:** 9 nodes

## Members
- [[Raw transaction ledger as CSV text.]] - rationale - ultron-backend/app.py
- [[Returns (normalized_dict, None) or (None, error_message).]] - rationale - ultron-backend/app.py
- [[_get_db_connection()]] - code - ultron-backend/app.py
- [[_init_db()]] - code - ultron-backend/app.py
- [[_trades_to_csv()]] - code - ultron-backend/app.py
- [[_validate_trade_input()]] - code - ultron-backend/app.py
- [[add_trade()]] - code - ultron-backend/app.py
- [[get_trades()]] - code - ultron-backend/app.py
- [[trades()]] - code - ultron-backend/app.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/_get_db_connection
SORT file.name ASC
```

## Connections to other communities
- 7 edges to [[_COMMUNITY_ultron-backendapp.py]]
- 5 edges to [[_COMMUNITY_route]]
- 2 edges to [[_COMMUNITY__fifo_engine]]
- 2 edges to [[_COMMUNITY_require_role]]
- 1 edge to [[_COMMUNITY_action_backup]]
- 1 edge to [[_COMMUNITY_run_ultron_chat]]

## Top bridge nodes
- [[_get_db_connection()]] - degree 11, connects to 6 communities
- [[trades()]] - degree 6, connects to 3 communities
- [[_trades_to_csv()]] - degree 4, connects to 2 communities
- [[add_trade()]] - degree 4, connects to 1 community
- [[get_trades()]] - degree 4, connects to 1 community