---
type: community
members: 14
---

# run_ultron_chat

**Members:** 14 nodes

## Members
- [[Best-effort logging — never raises. A logging failure (disk full, permissions,…]] - rationale - ultron-backend/app.py
- [[Best-effort — never raises. A logging failure must not break the chat response…]] - rationale - ultron-backend/app.py
- [[Closure matching the same handler(kwargs) - dict contract every internal…]] - rationale - ultron-backend/app.py
- [[Ensures discovery has run, then returns (schemas, dispatch) for every APPROVED…]] - rationale - ultron-backend/app.py
- [[Returns a NEW message dict with a cache_control breakpoint on its last content…]] - rationale - ultron-backend/app.py
- [[Runs the tool-use loop against the Claude API and returns (reply_text,…]] - rationale - ultron-backend/app.py
- [[_add_cache_breakpoint()]] - code - ultron-backend/app.py
- [[_log_llm_usage()]] - code - ultron-backend/app.py
- [[_make_mcp_tool_handler()]] - code - ultron-backend/app.py
- [[_mcp_call_tool()]] - code - ultron-backend/app.py
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
- 10 edges to [[_COMMUNITY_app.py]]
- 2 edges to [[_COMMUNITY__json_result]]
- 2 edges to [[_COMMUNITY__mcp_jsonrpc_call]]
- 1 edge to [[_COMMUNITY_docker_ps]]
- 1 edge to [[_COMMUNITY_require_role]]

## Top bridge nodes
- [[log_activity()]] - degree 7, connects to 3 communities
- [[run_ultron_chat()]] - degree 8, connects to 2 communities
- [[get_mcp_tools_and_dispatch()]] - degree 5, connects to 2 communities
- [[_log_llm_usage()]] - degree 4, connects to 2 communities
- [[_mcp_call_tool()]] - degree 3, connects to 2 communities