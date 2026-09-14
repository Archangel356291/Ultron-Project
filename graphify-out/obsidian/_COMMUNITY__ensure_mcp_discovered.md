---
type: community
members: 5
---

# _ensure_mcp_discovered

**Members:** 5 nodes

## Members
- [[Read-only view of every configured server and everything it offers — approved…]] - rationale - ultron-backend/app.py
- [[Runs discovery at most once, lazily, on first use — not at module import time.…]] - rationale - ultron-backend/app.py
- [[_ensure_mcp_discovered()]] - code - ultron-backend/app.py
- [[get_mcp_servers()]] - code - ultron-backend/app.py
- [[mcp_servers()]] - code - ultron-backend/app.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/_ensure_mcp_discovered
SORT file.name ASC
```

## Connections to other communities
- 3 edges to [[_COMMUNITY_ultron-backendapp.py]]
- 1 edge to [[_COMMUNITY__mcp_jsonrpc_call]]
- 1 edge to [[_COMMUNITY_run_ultron_chat]]
- 1 edge to [[_COMMUNITY_route]]
- 1 edge to [[_COMMUNITY_require_token]]

## Top bridge nodes
- [[_ensure_mcp_discovered()]] - degree 5, connects to 3 communities
- [[mcp_servers()]] - degree 4, connects to 3 communities
- [[get_mcp_servers()]] - degree 4, connects to 1 community