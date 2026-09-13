---
type: community
members: 20
---

# MCP Tool Dispatch

**Members:** 20 nodes

## Members
- [[Best-effort — never raises. A logging failure must not break the chat response…]] - rationale - ultron-backend/app.py
- [[Closure matching the same handler(kwargs) - dict contract every internal…]] - rationale - ultron-backend/app.py
- [[Ensures discovery has run, then returns (schemas, dispatch) for every APPROVED…]] - rationale - ultron-backend/app.py
- [[Read-only view of every configured server and everything it offers — approved…]] - rationale - ultron-backend/app.py
- [[Returns a NEW message dict with a cache_control breakpoint on its last content…]] - rationale - ultron-backend/app.py
- [[Runs discovery at most once, lazily, on first use — not at module import time.…]] - rationale - ultron-backend/app.py
- [[Runs the tool-use loop against the Claude API and returns (reply_text,…]] - rationale - ultron-backend/app.py
- [[Turn an SDK content-block object into a plain dict so it can be JSON-returned…]] - rationale - ultron-backend/app.py
- [[_add_cache_breakpoint()]] - code - ultron-backend/app.py
- [[_ensure_mcp_discovered()]] - code - ultron-backend/app.py
- [[_log_llm_usage()]] - code - ultron-backend/app.py
- [[_make_mcp_tool_handler()]] - code - ultron-backend/app.py
- [[_mcp_call_tool()]] - code - ultron-backend/app.py
- [[_serialize_block()]] - code - ultron-backend/app.py
- [[_serialize_content()]] - code - ultron-backend/app.py
- [[get_mcp_servers()]] - code - ultron-backend/app.py
- [[get_mcp_tools_and_dispatch()]] - code - ultron-backend/app.py
- [[handler()]] - code - ultron-backend/app.py
- [[mcp_servers()]] - code - ultron-backend/app.py
- [[run_ultron_chat()]] - code - ultron-backend/app.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/MCP_Tool_Dispatch
SORT file.name ASC
```

## Connections to other communities
- 11 edges to [[_COMMUNITY_Host Status Functions]]
- 2 edges to [[_COMMUNITY_MCP JSON-RPC Client]]
- 2 edges to [[_COMMUNITY_Backend Read Routes]]
- 1 edge to [[_COMMUNITY_Trade FIFO Engine]]
- 1 edge to [[_COMMUNITY_BackupDeploy Action Tokens]]
- 1 edge to [[_COMMUNITY_Chat Rate Limiting]]

## Top bridge nodes
- [[run_ultron_chat()]] - degree 8, connects to 2 communities
- [[_ensure_mcp_discovered()]] - degree 5, connects to 2 communities
- [[_log_llm_usage()]] - degree 4, connects to 2 communities
- [[mcp_servers()]] - degree 4, connects to 2 communities
- [[_mcp_call_tool()]] - degree 3, connects to 2 communities