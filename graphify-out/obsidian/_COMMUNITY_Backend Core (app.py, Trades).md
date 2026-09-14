---
type: community
cohesion: 0.16
members: 19
---

# Backend Core (app.py, Trades)

**Cohesion:** 0.16 - loosely connected
**Members:** 19 nodes

## Members
- [[NOTE this hits Windows Update and can take several seconds.]] - rationale - ultron-backend/app.py
- [[Per-disposal FIFO tax report as CSV text — one row per sell-vs-buy-lot match,…]] - rationale - ultron-backend/app.py
- [[Raw transaction ledger as CSV text.]] - rationale - ultron-backend/app.py
- [[Returns (normalized_dict, None) or (None, error_message).]] - rationale - ultron-backend/app.py
- [[Ultron home lab monitoring backend. Exposes a small JSON API that the dashboard…]] - rationale - ultron-backend/app.py
- [[Validates and normalizes a deploy-container request body. Returns (params,…]] - rationale - ultron-backend/app.py
- [[_parse_beta_tokens()]] - code - ultron-backend/app.py
- [[_tax_lots_to_csv()]] - code - ultron-backend/app.py
- [[_trades_to_csv()]] - code - ultron-backend/app.py
- [[_validate_container_name()]] - code - ultron-backend/app.py
- [[_validate_deploy_params()]] - code - ultron-backend/app.py
- [[_validate_image_ref()]] - code - ultron-backend/app.py
- [[_validate_port()]] - code - ultron-backend/app.py
- [[_validate_trade_input()]] - code - ultron-backend/app.py
- [[add_trade()]] - code - ultron-backend/app.py
- [[app.py]] - code - ultron-backend/app.py
- [[get_trades()]] - code - ultron-backend/app.py
- [[trades()]] - code - ultron-backend/app.py
- [[trades_export()]] - code - ultron-backend/app.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Backend_Core_apppy_Trades
SORT file.name ASC
```

## Connections to other communities
- 23 edges to [[_COMMUNITY_Backend REST Routes]]
- 16 edges to [[_COMMUNITY_MCP Client & Dispatch]]
- 12 edges to [[_COMMUNITY_BackupDeploy Action Endpoints]]
- 8 edges to [[_COMMUNITY_Chat Auth, Rate Limit & TTS]]
- 8 edges to [[_COMMUNITY_Memory & Trend Distillation]]
- 7 edges to [[_COMMUNITY_FIFO Trade Engine]]
- 7 edges to [[_COMMUNITY_Git Repo Status Tools]]
- 7 edges to [[_COMMUNITY_System Status & Updates]]
- 6 edges to [[_COMMUNITY_Activity Log & CVE Scanning]]
- 5 edges to [[_COMMUNITY_Docker Container Monitoring]]
- 2 edges to [[_COMMUNITY_Auth & Role Resolution]]
- 2 edges to [[_COMMUNITY_Anthropic SDK Fake]]
- 1 edge to [[_COMMUNITY_Community 28]]
- 1 edge to [[_COMMUNITY_Community 30]]
- 1 edge to [[_COMMUNITY_Community 31]]
- 1 edge to [[_COMMUNITY_Memory Feature Tests]]
- 1 edge to [[_COMMUNITY_Beta Spend Cap Test & Bug Fixes]]

## Top bridge nodes
- [[app.py]] - degree 112, connects to 17 communities
- [[_validate_deploy_params()]] - degree 7, connects to 2 communities
- [[trades()]] - degree 6, connects to 2 communities
- [[trades_export()]] - degree 5, connects to 1 community
- [[add_trade()]] - degree 4, connects to 1 community