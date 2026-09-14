---
type: community
members: 17
---

# run_ultron_chat

**Members:** 17 nodes

## Members
- [[Best-effort logging — never raises. A logging failure (disk full, permissions,…]] - rationale - ultron-backend/app.py
- [[Best-effort — never raises. A logging failure must not break the chat response…]] - rationale - ultron-backend/app.py
- [[Closure matching the same handler(kwargs) - dict contract every internal…]] - rationale - ultron-backend/app.py
- [[Ensures discovery has run, then returns (schemas, dispatch) for every APPROVED…]] - rationale - ultron-backend/app.py
- [[Returns a NEW message dict with a cache_control breakpoint on its last content…]] - rationale - ultron-backend/app.py
- [[Runs the tool-use loop against the Claude API and returns (reply_text,…]] - rationale - ultron-backend/app.py
- [[Turn an SDK content-block object into a plain dict so it can be JSON-returned…]] - rationale - ultron-backend/app.py
- [[_add_cache_breakpoint()]] - code - ultron-backend/app.py
- [[_log_llm_usage()]] - code - ultron-backend/app.py
- [[_make_mcp_tool_handler()]] - code - ultron-backend/app.py
- [[_mcp_call_tool()]] - code - ultron-backend/app.py
- [[_serialize_block()]] - code - ultron-backend/app.py
- [[_serialize_content()]] - code - ultron-backend/app.py
- [[get_mcp_tools_and_dispatch()]] - code - ultron-backend/app.py
- [[handler()]] - code - ultron-backend/app.py
- [[log_activity()]] - code - ultron-backend/app.py
- [[run_ultron_chat()]] - code - ultron-backend/app.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/run_ultron_chat
SORT file.name ASC
```

## Connections to other communities
- 9 edges to [[_COMMUNITY_ultron-backendapp.py]]
- 2 edges to [[_COMMUNITY_route]]
- 2 edges to [[_COMMUNITY_action_backup]]
- 1 edge to [[_COMMUNITY__mcp_jsonrpc_call]]
- 1 edge to [[_COMMUNITY__ensure_mcp_discovered]]
- 1 edge to [[_COMMUNITY_scan_container_cves]]
- 1 edge to [[_COMMUNITY_chat]]

## Top bridge nodes
- [[log_activity()]] - degree 7, connects to 4 communities
- [[run_ultron_chat()]] - degree 8, connects to 2 communities
- [[get_mcp_tools_and_dispatch()]] - degree 5, connects to 2 communities
- [[_log_llm_usage()]] - degree 4, connects to 2 communities
- [[_mcp_call_tool()]] - degree 3, connects to 2 communities