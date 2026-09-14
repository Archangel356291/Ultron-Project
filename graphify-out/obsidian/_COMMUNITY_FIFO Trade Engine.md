---
type: community
cohesion: 0.20
members: 10
---

# FIFO Trade Engine

**Cohesion:** 0.20 - loosely connected
**Members:** 10 nodes

## Members
- [[Best-effort date - integer day count, for holding-period math. Never raises;…]] - rationale - ultron-backend/app.py
- [[Per-disposal detail each row is one sell matched against one consumed buy lot,…]] - rationale - ultron-backend/app.py
- [[Simplified FIFO realized gainloss per asset — the aggregated view. See…]] - rationale - ultron-backend/app.py
- [[The one place FIFO matching happens. Returns both an aggregated per-asset view…]] - rationale - ultron-backend/app.py
- [[_fifo_engine()]] - code - ultron-backend/app.py
- [[_trade_date_to_epoch_days()]] - code - ultron-backend/app.py
- [[get_trade_summary()]] - code - ultron-backend/app.py
- [[get_trade_tax_lots()]] - code - ultron-backend/app.py
- [[trades_summary()]] - code - ultron-backend/app.py
- [[trades_tax_lots()]] - code - ultron-backend/app.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/FIFO_Trade_Engine
SORT file.name ASC
```

## Connections to other communities
- 7 edges to [[_COMMUNITY_Backend Core (app.py, Trades)]]
- 4 edges to [[_COMMUNITY_Backend REST Routes]]
- 2 edges to [[_COMMUNITY_Chat Auth, Rate Limit & TTS]]
- 1 edge to [[_COMMUNITY_Memory & Trend Distillation]]

## Top bridge nodes
- [[trades_summary()]] - degree 5, connects to 3 communities
- [[trades_tax_lots()]] - degree 5, connects to 3 communities
- [[_fifo_engine()]] - degree 7, connects to 2 communities
- [[get_trade_summary()]] - degree 4, connects to 1 community
- [[get_trade_tax_lots()]] - degree 4, connects to 1 community