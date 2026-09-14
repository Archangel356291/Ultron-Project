---
type: community
cohesion: 0.29
members: 7
---

# MCP Design & Bug History

**Cohesion:** 0.29 - loosely connected
**Members:** 7 nodes

## Members
- [[Bug MCP Empty Notification Response Mishandled]] - rationale - PROJECT-SUMMARY-FOR-CLAUDE-CODE.md
- [[Bug MCP Response-Size Cap Applied At Wrong Layer]] - rationale - PROJECT-SUMMARY-FOR-CLAUDE-CODE.md
- [[External Tools (MCP) Section]] - rationale - ultron-backend/README.md
- [[MCP Opt-In At the Tool Level, Not Server Level]] - rationale - README.md
- [[MCP Support (External ToolPlugin System)]] - rationale - PROJECT-SUMMARY-FOR-CLAUDE-CODE.md
- [[dev-toolsfake_pkgs (Scriptable Fakes for anthropicdiscordaiohttp)]] - concept - PROJECT-SUMMARY-FOR-CLAUDE-CODE.md
- [[dev-toolstest_mcp_server.py (Real Protocol-Strict MCP Test Server)]] - concept - PROJECT-SUMMARY-FOR-CLAUDE-CODE.md

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/MCP_Design__Bug_History
SORT file.name ASC
```
