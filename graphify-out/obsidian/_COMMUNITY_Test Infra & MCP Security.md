---
type: community
members: 14
---

# Test Infra & MCP Security

**Members:** 14 nodes

## Members
- [[External tools (MCP) security model]] - rationale - ultron-backend/README.md
- [[MCP is opt-in at the tool level, not the server level]] - rationale - README.md
- [[MagicDNS hostname]] - document - ultron-backend/REMOTE-ACCESS.md
- [[Tailscale (mesh VPN)]] - document - ultron-backend/REMOTE-ACCESS.md
- [[Tailscale grantsACLs (tailnet policy)]] - rationale - ultron-backend/REMOTE-ACCESS.md
- [[Testing approach (test against real dependency behavior)]] - rationale - README.md
- [[Why this exists as a separate folder (test against real-like dependencies)]] - rationale - dev-tools/README.md
- [[WireGuard]] - document - ultron-backend/REMOTE-ACCESS.md
- [[aiohttp]] - code - ultron-discord-bot/requirements.txt
- [[discord.py]] - code - ultron-discord-bot/requirements.txt
- [[fake_pkgs (drop-in fake SDKs)]] - document - dev-tools/README.md
- [[fake_pkgsaiohttp (aiohttp client fake)]] - document - dev-tools/README.md
- [[fake_pkgsdiscord (Discord SDK fake)]] - document - dev-tools/README.md
- [[test_mcp_server.py (real protocol-compliant local MCP server)]] - document - dev-tools/README.md

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Test_Infra__MCP_Security
SORT file.name ASC
```

## Connections to other communities
- 1 edge to [[_COMMUNITY_Architecture Overview]]
- 1 edge to [[_COMMUNITY_Backend API & Principles]]

## Top bridge nodes
- [[fake_pkgs (drop-in fake SDKs)]] - degree 5, connects to 1 community
- [[External tools (MCP) security model]] - degree 4, connects to 1 community