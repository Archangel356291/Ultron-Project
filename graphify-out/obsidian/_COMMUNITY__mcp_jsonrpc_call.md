---
type: community
members: 13
---

# _mcp_jsonrpc_call

**Members:** 13 nodes

## Members
- [[Connects to every configured server once and lists its tools. A server that's…]] - rationale - ultron-backend/app.py
- [[Exception_3]] - code
- [[MCPError]] - code - ultron-backend/app.py
- [[One raw JSON-RPC POST. Hard timeout, hard response-size cap. Handles both a…]] - rationale - ultron-backend/app.py
- [[Read-only view of every configured server and everything it offers — approved…]] - rationale - ultron-backend/app.py
- [[Runs discovery at most once, lazily, on first use — not at module import time.…]] - rationale - ultron-backend/app.py
- [[_ensure_mcp_discovered()]] - code - ultron-backend/app.py
- [[_mcp_discover_all()]] - code - ultron-backend/app.py
- [[_mcp_http_post()]] - code - ultron-backend/app.py
- [[_mcp_initialize()]] - code - ultron-backend/app.py
- [[_mcp_jsonrpc_call()]] - code - ultron-backend/app.py
- [[_mcp_list_tools()]] - code - ultron-backend/app.py
- [[get_mcp_servers()]] - code - ultron-backend/app.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/_mcp_jsonrpc_call
SORT file.name ASC
```

## Connections to other communities
- 8 edges to [[_COMMUNITY_app.py]]
- 2 edges to [[_COMMUNITY_run_ultron_chat]]
- 1 edge to [[_COMMUNITY_route]]

## Top bridge nodes
- [[_mcp_jsonrpc_call()]] - degree 6, connects to 2 communities
- [[_ensure_mcp_discovered()]] - degree 5, connects to 2 communities
- [[get_mcp_servers()]] - degree 4, connects to 2 communities
- [[_mcp_discover_all()]] - degree 5, connects to 1 community
- [[MCPError]] - degree 4, connects to 1 community