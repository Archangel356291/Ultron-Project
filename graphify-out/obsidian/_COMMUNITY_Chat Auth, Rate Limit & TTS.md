---
type: community
cohesion: 0.22
members: 11
---

# Chat Auth, Rate Limit & TTS

**Cohesion:** 0.22 - loosely connected
**Members:** 11 nodes

## Members
- [[Admin or beta_tester. Use only on endpoints in the beta tester's allowed scope…]] - rationale - ultron-backend/app.py
- [[Lifetime spend for one beta tester, in dollars. Returns 0.0 on any read failure…]] - rationale - ultron-backend/app.py
- [[One TTS request to Fish Audio. Returns (audio_bytes, content_type, error).]] - rationale - ultron-backend/app.py
- [[Returns None if the request is allowed, or an error message if the caller…]] - rationale - ultron-backend/app.py
- [[_beta_tester_spend_usd()]] - code - ultron-backend/app.py
- [[_check_rate_limit()]] - code - ultron-backend/app.py
- [[_fish_audio_tts()]] - code - ultron-backend/app.py
- [[chat()]] - code - ultron-backend/app.py
- [[require_role()]] - code - ultron-backend/app.py
- [[tts()]] - code - ultron-backend/app.py
- [[whoami()]] - code - ultron-backend/app.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Chat_Auth_Rate_Limit__TTS
SORT file.name ASC
```

## Connections to other communities
- 8 edges to [[_COMMUNITY_Backend Core (app.py, Trades)]]
- 3 edges to [[_COMMUNITY_Backend REST Routes]]
- 2 edges to [[_COMMUNITY_Memory & Trend Distillation]]
- 2 edges to [[_COMMUNITY_FIFO Trade Engine]]
- 2 edges to [[_COMMUNITY_Auth & Role Resolution]]
- 1 edge to [[_COMMUNITY_MCP Client & Dispatch]]

## Top bridge nodes
- [[chat()]] - degree 7, connects to 4 communities
- [[require_role()]] - degree 10, connects to 3 communities
- [[_beta_tester_spend_usd()]] - degree 6, connects to 2 communities
- [[tts()]] - degree 5, connects to 2 communities
- [[whoami()]] - degree 4, connects to 2 communities