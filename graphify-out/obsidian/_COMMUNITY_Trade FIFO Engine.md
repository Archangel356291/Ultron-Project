---
type: community
members: 16
---

# Trade FIFO Engine

**Members:** 16 nodes

## Members
- [[Best-effort date - integer day count, for holding-period math. Never raises;…]] - rationale - ultron-backend/app.py
- [[Per-disposal FIFO tax report as CSV text — one row per sell-vs-buy-lot match,…]] - rationale - ultron-backend/app.py
- [[Raw transaction ledger as CSV text.]] - rationale - ultron-backend/app.py
- [[Returns (normalized_dict, None) or (None, error_message).]] - rationale - ultron-backend/app.py
- [[The one place FIFO matching happens. Returns both an aggregated per-asset view…]] - rationale - ultron-backend/app.py
- [[_fifo_engine()]] - code - ultron-backend/app.py
- [[_get_db_connection()]] - code - ultron-backend/app.py
- [[_init_db()]] - code - ultron-backend/app.py
- [[_tax_lots_to_csv()]] - code - ultron-backend/app.py
- [[_trade_date_to_epoch_days()]] - code - ultron-backend/app.py
- [[_trades_to_csv()]] - code - ultron-backend/app.py
- [[_validate_trade_input()]] - code - ultron-backend/app.py
- [[add_trade()]] - code - ultron-backend/app.py
- [[get_trades()]] - code - ultron-backend/app.py
- [[trades()]] - code - ultron-backend/app.py
- [[trades_export()]] - code - ultron-backend/app.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Trade_FIFO_Engine
SORT file.name ASC
```

## Connections to other communities
- 11 edges to [[_COMMUNITY_Host Status Functions]]
- 10 edges to [[_COMMUNITY_Backend Read Routes]]
- 1 edge to [[_COMMUNITY_BackupDeploy Action Tokens]]
- 1 edge to [[_COMMUNITY_MCP Tool Dispatch]]
- 1 edge to [[_COMMUNITY_Chat Rate Limiting]]

## Top bridge nodes
- [[_get_db_connection()]] - degree 11, connects to 5 communities
- [[_fifo_engine()]] - degree 7, connects to 2 communities
- [[trades()]] - degree 6, connects to 2 communities
- [[trades_export()]] - degree 5, connects to 2 communities
- [[add_trade()]] - degree 4, connects to 1 community