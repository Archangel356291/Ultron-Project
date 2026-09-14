---
type: community
members: 15
---

# require_role

**Members:** 15 nodes

## Members
- [[Admin or beta_tester. Use only on endpoints in the beta tester's allowed scope…]] - rationale - ultron-backend/app.py
- [[Constant-time-ish token check against admin and every registered beta tester.…]] - rationale - ultron-backend/app.py
- [[One TTS request to Fish Audio. Returns (audio_bytes, content_type, error).]] - rationale - ultron-backend/app.py
- [[Returns None if the request is allowed, or an error message if the caller…]] - rationale - ultron-backend/app.py
- [[Sums input+output tokens (real spend) for calls logged today (local date,…]] - rationale - ultron-backend/app.py
- [[_check_rate_limit()]] - code - ultron-backend/app.py
- [[_fish_audio_tts()]] - code - ultron-backend/app.py
- [[_resolve_role()]] - code - ultron-backend/app.py
- [[_todays_token_usage()]] - code - ultron-backend/app.py
- [[chat()]] - code - ultron-backend/app.py
- [[require_role()]] - code - ultron-backend/app.py
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
- 8 edges to [[_COMMUNITY_ultron-backendapp.py]]
- 4 edges to [[_COMMUNITY_route]]
- 2 edges to [[_COMMUNITY__get_db_connection]]
- 2 edges to [[_COMMUNITY__fifo_engine]]
- 1 edge to [[_COMMUNITY_run_ultron_chat]]

## Top bridge nodes
- [[require_role()]] - degree 10, connects to 3 communities
- [[chat()]] - degree 6, connects to 3 communities
- [[_todays_token_usage()]] - degree 4, connects to 2 communities
- [[tts()]] - degree 4, connects to 2 communities
- [[whoami()]] - degree 3, connects to 2 communities