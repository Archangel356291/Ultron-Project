---
type: community
members: 20
---

# require_role

**Members:** 20 nodes

## Members
- [[Admin or beta_tester. Use only on endpoints in the beta tester's allowed scope…]] - rationale - ultron-backend/app.py
- [[Best-effort date - integer day count, for holding-period math. Never raises;…]] - rationale - ultron-backend/app.py
- [[Constant-time-ish token check against both roles. Returns 'admin', 'beta', or…]] - rationale - ultron-backend/app.py
- [[One TTS request to Fish Audio. Returns (audio_bytes, content_type, error).]] - rationale - ultron-backend/app.py
- [[Per-disposal detail each row is one sell matched against one consumed buy lot,…]] - rationale - ultron-backend/app.py
- [[Simplified FIFO realized gainloss per asset — the aggregated view. See…]] - rationale - ultron-backend/app.py
- [[The one place FIFO matching happens. Returns both an aggregated per-asset view…]] - rationale - ultron-backend/app.py
- [[_fifo_engine()]] - code - ultron-backend/app.py
- [[_fish_audio_tts()]] - code - ultron-backend/app.py
- [[_resolve_role()]] - code - ultron-backend/app.py
- [[_trade_date_to_epoch_days()]] - code - ultron-backend/app.py
- [[get_trade_summary()]] - code - ultron-backend/app.py
- [[get_trade_tax_lots()]] - code - ultron-backend/app.py
- [[require_role()]] - code - ultron-backend/app.py
- [[trades_summary()]] - code - ultron-backend/app.py
- [[trades_tax_lots()]] - code - ultron-backend/app.py
- [[tts()]] - code - ultron-backend/app.py
- [[whoami()]] - code - ultron-backend/app.py
- [[wrapper()]] - code - ultron-backend/app.py
- [[wrapper()_1]] - code - ultron-backend/app.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/require_role
SORT file.name ASC
```

## Connections to other communities
- 11 edges to [[_COMMUNITY_ultron-backendapp.py]]
- 8 edges to [[_COMMUNITY_route]]
- 1 edge to [[_COMMUNITY_trades_export]]
- 1 edge to [[_COMMUNITY_chat]]
- 1 edge to [[_COMMUNITY_require_token]]

## Top bridge nodes
- [[require_role()]] - degree 10, connects to 3 communities
- [[_fifo_engine()]] - degree 7, connects to 3 communities
- [[trades_summary()]] - degree 5, connects to 2 communities
- [[trades_tax_lots()]] - degree 5, connects to 2 communities
- [[tts()]] - degree 4, connects to 2 communities