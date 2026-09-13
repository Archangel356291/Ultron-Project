---
type: community
members: 9
---

# MCP JSON-RPC Client

**Members:** 9 nodes

## Members
- [[Connects to every configured server once and lists its tools. A server that's…]] - rationale - ultron-backend/app.py
- [[Exception_2]] - code
- [[MCPError]] - code - ultron-backend/app.py
- [[One raw JSON-RPC POST. Hard timeout, hard response-size cap. Handles both a…]] - rationale - ultron-backend/app.py
- [[_mcp_discover_all()]] - code - ultron-backend/app.py
- [[_mcp_http_post()]] - code - ultron-backend/app.py
- [[_mcp_initialize()]] - code - ultron-backend/app.py
- [[_mcp_jsonrpc_call()]] - code - ultron-backend/app.py
- [[_mcp_list_tools()]] - code - ultron-backend/app.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/MCP_JSON-RPC_Client
SORT file.name ASC
```

## Connections to other communities
- 6 edges to [[_COMMUNITY_Host Status Functions]]
- 2 edges to [[_COMMUNITY_MCP Tool Dispatch]]

## Top bridge nodes
- [[_mcp_jsonrpc_call()]] - degree 6, connects to 2 communities
- [[_mcp_discover_all()]] - degree 5, connects to 2 communities
- [[MCPError]] - degree 4, connects to 1 community
- [[_mcp_http_post()]] - degree 4, connects to 1 community
- [[_mcp_initialize()]] - degree 3, connects to 1 community