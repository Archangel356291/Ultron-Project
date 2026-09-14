---
type: community
members: 10
---

# trades

**Members:** 10 nodes

## Members
- [[Per-disposal FIFO tax report as CSV text — one row per sell-vs-buy-lot match,…]] - rationale - ultron-backend/app.py
- [[Raw transaction ledger as CSV text.]] - rationale - ultron-backend/app.py
- [[Returns (normalized_dict, None) or (None, error_message).]] - rationale - ultron-backend/app.py
- [[_tax_lots_to_csv()]] - code - ultron-backend/app.py
- [[_trades_to_csv()]] - code - ultron-backend/app.py
- [[_validate_trade_input()]] - code - ultron-backend/app.py
- [[add_trade()]] - code - ultron-backend/app.py
- [[get_trades()]] - code - ultron-backend/app.py
- [[trades()]] - code - ultron-backend/app.py
- [[trades_export()]] - code - ultron-backend/app.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/trades
SORT file.name ASC
```

## Connections to other communities
- 7 edges to [[_COMMUNITY_ultron-backendapp.py]]
- 4 edges to [[_COMMUNITY_route]]
- 2 edges to [[_COMMUNITY__get_db_connection]]
- 1 edge to [[_COMMUNITY__fifo_engine]]
- 1 edge to [[_COMMUNITY_require_role]]

## Top bridge nodes
- [[trades()]] - degree 6, connects to 3 communities
- [[trades_export()]] - degree 5, connects to 2 communities
- [[add_trade()]] - degree 4, connects to 2 communities
- [[get_trades()]] - degree 4, connects to 2 communities
- [[_tax_lots_to_csv()]] - degree 4, connects to 2 communities