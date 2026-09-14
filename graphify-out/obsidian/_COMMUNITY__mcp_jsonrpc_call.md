---
type: community
members: 9
---

# _mcp_jsonrpc_call

**Members:** 9 nodes

## Members
- [[Connects to every configured server once and lists its tools. A server that's…]] - rationale - ultron-backend/app.py
- [[Exception_3]] - code
- [[MCPError]] - code - ultron-backend/app.py
- [[One raw JSON-RPC POST. Hard timeout, hard response-size cap. Handles both a…]] - rationale - ultron-backend/app.py
- [[_mcp_discover_all()]] - code - ultron-backend/app.py
- [[_mcp_http_post()]] - code - ultron-backend/app.py
- [[_mcp_initialize()]] - code - ultron-backend/app.py
- [[_mcp_jsonrpc_call()]] - code - ultron-backend/app.py
- [[_mcp_list_tools()]] - code - ultron-backend/app.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/_mcp_jsonrpc_call
SORT file.name ASC
```

## Connections to other communities
- 6 edges to [[_COMMUNITY_app.py]]
- 1 edge to [[_COMMUNITY__ensure_mcp_discovered]]
- 1 edge to [[_COMMUNITY_run_ultron_chat]]

## Top bridge nodes
- [[_mcp_jsonrpc_call()]] - degree 6, connects to 2 communities
- [[_mcp_discover_all()]] - degree 5, connects to 2 communities
- [[MCPError]] - degree 4, connects to 1 community
- [[_mcp_http_post()]] - degree 4, connects to 1 community
- [[_mcp_initialize()]] - degree 3, connects to 1 community