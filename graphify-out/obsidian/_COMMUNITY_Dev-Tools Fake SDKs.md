---
type: community
cohesion: 0.22
members: 9
---

# Dev-Tools Fake SDKs

**Cohesion:** 0.22 - loosely connected
**Members:** 9 nodes

## Members
- [[Why this exists as a separate folder (test against real-like dependencies)]] - rationale - dev-tools/README.md
- [[aiohttp]] - code - ultron-discord-bot/requirements.txt
- [[anthropic (=1.0.0,2.0.0)]] - code - ultron-backend/requirements.txt
- [[discord.py]] - code - ultron-discord-bot/requirements.txt
- [[fake_pkgs (drop-in fake SDKs)]] - document - dev-tools/README.md
- [[fake_pkgsaiohttp (aiohttp client fake)]] - document - dev-tools/README.md
- [[fake_pkgsanthropic (scriptable Anthropic client fake)]] - document - dev-tools/README.md
- [[fake_pkgsdiscord (Discord SDK fake)]] - document - dev-tools/README.md
- [[test_mcp_server.py (real protocol-compliant local MCP server)]] - document - dev-tools/README.md

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Dev-Tools_Fake_SDKs
SORT file.name ASC
```
