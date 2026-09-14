---
type: community
members: 6
---

# trades_export

**Members:** 6 nodes

## Members
- [[Per-disposal FIFO tax report as CSV text — one row per sell-vs-buy-lot match,…]] - rationale - ultron-backend/app.py
- [[Raw transaction ledger as CSV text.]] - rationale - ultron-backend/app.py
- [[_tax_lots_to_csv()]] - code - ultron-backend/app.py
- [[_trades_to_csv()]] - code - ultron-backend/app.py
- [[get_trades()]] - code - ultron-backend/app.py
- [[trades_export()]] - code - ultron-backend/app.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/trades_export
SORT file.name ASC
```

## Connections to other communities
- 4 edges to [[_COMMUNITY_ultron-backendapp.py]]
- 3 edges to [[_COMMUNITY_route]]
- 1 edge to [[_COMMUNITY_require_role]]
- 1 edge to [[_COMMUNITY_require_token]]

## Top bridge nodes
- [[trades_export()]] - degree 5, connects to 3 communities
- [[get_trades()]] - degree 4, connects to 2 communities
- [[_tax_lots_to_csv()]] - degree 4, connects to 2 communities
- [[_trades_to_csv()]] - degree 4, connects to 1 community