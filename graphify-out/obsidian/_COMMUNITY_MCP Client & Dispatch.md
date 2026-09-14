---
type: community
cohesion: 0.08
members: 28
---

# MCP Client & Dispatch

**Cohesion:** 0.08 - loosely connected
**Members:** 28 nodes

## Members
- [[Best-effort — never raises. A logging failure must not break the chat response…]] - rationale - ultron-backend/app.py
- [[Closure matching the same handler(kwargs) - dict contract every internal…]] - rationale - ultron-backend/app.py
- [[Connects to every configured server once and lists its tools. A server that's…]] - rationale - ultron-backend/app.py
- [[Ensures discovery has run, then returns (schemas, dispatch) for every APPROVED…]] - rationale - ultron-backend/app.py
- [[Exception_3]] - code
- [[MCPError]] - code - ultron-backend/app.py
- [[One raw JSON-RPC POST. Hard timeout, hard response-size cap. Handles both a…]] - rationale - ultron-backend/app.py
- [[Real dollar cost of one API call from its actual usage counts. Returns 0.0 for…]] - rationale - ultron-backend/app.py
- [[Returns a NEW message dict with a cache_control breakpoint on its last content…]] - rationale - ultron-backend/app.py
- [[Runs discovery at most once, lazily, on first use — not at module import time.…]] - rationale - ultron-backend/app.py
- [[Runs the tool-use loop against the Claude API and returns (reply_text,…]] - rationale - ultron-backend/app.py
- [[Turn an SDK content-block object into a plain dict so it can be JSON-returned…]] - rationale - ultron-backend/app.py
- [[_add_cache_breakpoint()]] - code - ultron-backend/app.py
- [[_ensure_mcp_discovered()]] - code - ultron-backend/app.py
- [[_log_llm_usage()]] - code - ultron-backend/app.py
- [[_make_mcp_tool_handler()]] - code - ultron-backend/app.py
- [[_mcp_call_tool()]] - code - ultron-backend/app.py
- [[_mcp_discover_all()]] - code - ultron-backend/app.py
- [[_mcp_http_post()]] - code - ultron-backend/app.py
- [[_mcp_initialize()]] - code - ultron-backend/app.py
- [[_mcp_jsonrpc_call()]] - code - ultron-backend/app.py
- [[_mcp_list_tools()]] - code - ultron-backend/app.py
- [[_serialize_block()]] - code - ultron-backend/app.py
- [[_serialize_content()]] - code - ultron-backend/app.py
- [[_usage_cost_usd()]] - code - ultron-backend/app.py
- [[get_mcp_tools_and_dispatch()]] - code - ultron-backend/app.py
- [[handler()]] - code - ultron-backend/app.py
- [[run_ultron_chat()]] - code - ultron-backend/app.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/MCP_Client__Dispatch
SORT file.name ASC
```

## Connections to other communities
- 16 edges to [[_COMMUNITY_Backend Core (app.py, Trades)]]
- 1 edge to [[_COMMUNITY_Chat Auth, Rate Limit & TTS]]
- 1 edge to [[_COMMUNITY_Memory & Trend Distillation]]
- 1 edge to [[_COMMUNITY_Activity Log & CVE Scanning]]
- 1 edge to [[_COMMUNITY_Backend REST Routes]]

## Top bridge nodes
- [[run_ultron_chat()]] - degree 8, connects to 2 communities
- [[_ensure_mcp_discovered()]] - degree 5, connects to 2 communities
- [[_log_llm_usage()]] - degree 5, connects to 2 communities
- [[_mcp_jsonrpc_call()]] - degree 6, connects to 1 community
- [[get_mcp_tools_and_dispatch()]] - degree 5, connects to 1 community