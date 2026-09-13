---
type: community
members: 14
---

# Cost Controls & Beta Config

**Members:** 14 nodes

## Members
- [[7-Step Smoke Test]] - concept - ultron-backend/BETA-LAUNCH-CHECKLIST.md
- [[ANTHROPIC_API_KEY (real beta key)]] - concept - ultron-backend/BETA-LAUNCH-CHECKLIST.md
- [[Backup Feature (ULTRON_BACKUP_SOURCES  DEST)]] - concept - ultron-backend/BETA-LAUNCH-CHECKLIST.md
- [[Cost Controls (caching, token budget, rate limit)]] - concept - PROJECT-SUMMARY-FOR-CLAUDE-CODE.md
- [[Discord Bot Setup (start-bot.ps1)]] - concept - ultron-backend/BETA-LAUNCH-CHECKLIST.md
- [[Known By-Design Beta Behaviors]] - rationale - ultron-backend/BETA-LAUNCH-CHECKLIST.md
- [[Phase 1 Status (complete, 2026-09-13)]] - document - ultron-backend/BETA-LAUNCH-CHECKLIST.md
- [[Security Pass (gitignore hardening, token scrub, bandit SAST)]] - rationale - ultron-backend/BETA-LAUNCH-CHECKLIST.md
- [[ULTRON_API_TOKEN (required env var)]] - concept - ultron-backend/BETA-LAUNCH-CHECKLIST.md
- [[ULTRON_CHAT_RATE_LIMIT_PER_MINUTE]] - concept - ultron-backend/BETA-LAUNCH-CHECKLIST.md
- [[ULTRON_LLM_DAILY_TOKEN_BUDGET]] - concept - ultron-backend/BETA-LAUNCH-CHECKLIST.md
- [[ULTRON_MCP_CONFIG (optional MCP feature)]] - concept - ultron-backend/BETA-LAUNCH-CHECKLIST.md
- [[fetchLlmUsage()]] - code - ultron-dashboard.html
- [[start-ultron.ps1]] - code - ultron-backend/start-ultron.ps1

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Cost_Controls__Beta_Config
SORT file.name ASC
```

## Connections to other communities
- 3 edges to [[_COMMUNITY_Dashboard Live Data Fetch]]
- 2 edges to [[_COMMUNITY_Development Tab & Docs]]
- 2 edges to [[_COMMUNITY_Architecture Overview]]
- 2 edges to [[_COMMUNITY_Safety Boundaries & MCP Bugs]]
- 1 edge to [[_COMMUNITY_Trade Export & Bot Parity]]
- 1 edge to [[_COMMUNITY_Voice & Chat Dashboard JS]]

## Top bridge nodes
- [[start-ultron.ps1]] - degree 9, connects to 2 communities
- [[Phase 1 Status (complete, 2026-09-13)]] - degree 6, connects to 2 communities
- [[ULTRON_API_TOKEN (required env var)]] - degree 5, connects to 1 community
- [[Backup Feature (ULTRON_BACKUP_SOURCES  DEST)]] - degree 4, connects to 1 community
- [[fetchLlmUsage()]] - degree 3, connects to 1 community