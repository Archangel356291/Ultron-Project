---
type: community
members: 10
---

# _fifo_engine

**Members:** 10 nodes

## Members
- [[Best-effort date - integer day count, for holding-period math. Never raises;…]] - rationale - ultron-backend/app.py
- [[Per-disposal FIFO tax report as CSV text — one row per sell-vs-buy-lot match,…]] - rationale - ultron-backend/app.py
- [[Simplified FIFO realized gainloss per asset — the aggregated view. See…]] - rationale - ultron-backend/app.py
- [[The one place FIFO matching happens. Returns both an aggregated per-asset view…]] - rationale - ultron-backend/app.py
- [[_fifo_engine()]] - code - ultron-backend/app.py
- [[_tax_lots_to_csv()]] - code - ultron-backend/app.py
- [[_trade_date_to_epoch_days()]] - code - ultron-backend/app.py
- [[get_trade_summary()]] - code - ultron-backend/app.py
- [[trades_export()]] - code - ultron-backend/app.py
- [[trades_summary()]] - code - ultron-backend/app.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/_fifo_engine
SORT file.name ASC
```

## Connections to other communities
- 6 edges to [[_COMMUNITY_app.py]]
- 4 edges to [[_COMMUNITY_route]]
- 2 edges to [[_COMMUNITY__get_db_connection]]
- 2 edges to [[_COMMUNITY_require_token]]

## Top bridge nodes
- [[trades_export()]] - degree 5, connects to 4 communities
- [[_fifo_engine()]] - degree 7, connects to 3 communities
- [[trades_summary()]] - degree 5, connects to 3 communities
- [[get_trade_summary()]] - degree 4, connects to 1 community
- [[_tax_lots_to_csv()]] - degree 4, connects to 1 community