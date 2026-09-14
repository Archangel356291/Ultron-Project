---
type: community
cohesion: 0.50
members: 5
---

# Auth & Role Resolution

**Cohesion:** 0.50 - moderately connected
**Members:** 5 nodes

## Members
- [[Constant-time-ish token check against admin and every registered beta tester.…]] - rationale - ultron-backend/app.py
- [[_resolve_role()]] - code - ultron-backend/app.py
- [[_touch_presence()]] - code - ultron-backend/app.py
- [[wrapper()]] - code - ultron-backend/app.py
- [[wrapper()_1]] - code - ultron-backend/app.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Auth__Role_Resolution
SORT file.name ASC
```

## Connections to other communities
- 2 edges to [[_COMMUNITY_Chat Auth, Rate Limit & TTS]]
- 2 edges to [[_COMMUNITY_Backend Core (app.py, Trades)]]
- 1 edge to [[_COMMUNITY_Backend REST Routes]]

## Top bridge nodes
- [[wrapper()_1]] - degree 4, connects to 2 communities
- [[_resolve_role()]] - degree 4, connects to 1 community
- [[wrapper()]] - degree 3, connects to 1 community
- [[_touch_presence()]] - degree 3, connects to 1 community