---
type: community
cohesion: 0.07
members: 30
---

# Beta Spend Cap Test & Bug Fixes

**Cohesion:** 0.07 - loosely connected
**Members:** 30 nodes

## Members
- [[Bug apitts Had No Spend-Cap Check]] - rationale - ultron-backend/CODE-AUDIT.md
- [[Bug Discord Bot Only Caught ClientError, Not TimeoutError]] - rationale - ultron-backend/CODE-AUDIT.md
- [[Bug Discord Field-Truncation Off-By-N]] - rationale - PROJECT-SUMMARY-FOR-CLAUDE-CODE.md
- [[Bug Discord Token Stored Under Wrong .env Key]] - rationale - ultron-backend/CODE-AUDIT.md
- [[Bug Discord backend_get Showed Raw Error Text]] - rationale - PROJECT-SUMMARY-FOR-CLAUDE-CODE.md
- [[Bug No Per-History-Message Size Cap]] - rationale - ultron-backend/CODE-AUDIT.md
- [[Bug Spend-Cap Check Was Read-Then-Act, No Lock]] - rationale - ultron-backend/CODE-AUDIT.md
- [[Bug Tool-Registration Ordering (get_llm_usage NameError Risk)]] - rationale - PROJECT-SUMMARY-FOR-CLAUDE-CODE.md
- [[Bug _PRESENCE Dict Race (Dictionary Changed Size During Iteration)]] - rationale - ultron-backend/CODE-AUDIT.md
- [[Bug bot.chat_histories Raced On Double-Fired ask]] - rationale - ultron-backend/CODE-AUDIT.md
- [[Bug sendFromHome() Bypassed Disabled-Input Guard]] - rationale - ultron-backend/CODE-AUDIT.md
- [[Bug start-bot.ps1 Never Loaded .env, Expected Git-Tracked Secrets]] - rationale - ultron-backend/CODE-AUDIT.md
- [[Config Value Hardening (Min-1 Clamp on TokenRate Limits)]] - rationale - PROJECT-SUMMARY-FOR-CLAUDE-CODE.md
- [[Cost Controls (Budget, Spend Cap, Rate Limit, Caching)]] - rationale - ultron-backend/README.md
- [[POST apichat (Claude Chat Tool-Use Loop)]] - code - ultron-backend/README.md
- [[Real Safeguards, Not Just Docs]] - rationale - README.md
- [[Self-check for the beta-tester $1 spend cap (ULTRON_BETA_MAX_SPEND_USD) and the…]] - rationale - dev-tools/test_beta_spend_cap.py
- [[_PRESENCE (Connection-Tracking Dict)]] - code - ultron-backend/CODE-AUDIT.md
- [[_fire()]] - code - dev-tools/test_beta_spend_cap.py
- [[_queue_reply()]] - code - dev-tools/test_beta_spend_cap.py
- [[appendChatBubble()]] - code - ultron-dashboard.html
- [[demo()_2]] - code - dev-tools/test_beta_spend_cap.py
- [[postChat()]] - code - ultron-dashboard.html
- [[sendChatMessage()]] - code - ultron-dashboard.html
- [[sendFromHome()]] - code - ultron-dashboard.html
- [[speakReply()]] - code - ultron-dashboard.html
- [[test_beta_spend_cap.py]] - code - dev-tools/test_beta_spend_cap.py
- [[ultron-dashboard.html (Single-file Dashboard)]] - concept - README.md
- [[ultron-discord-bot (Thin Remote-Control Layer)]] - concept - README.md
- [[ultron-discord-bot Service (Docker Compose)]] - code - docker-compose.yml

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Beta_Spend_Cap_Test__Bug_Fixes
SORT file.name ASC
```

## Connections to other communities
- 1 edge to [[_COMMUNITY_Anthropic SDK Fake]]
- 1 edge to [[_COMMUNITY_Backend Core (app.py, Trades)]]

## Top bridge nodes
- [[test_beta_spend_cap.py]] - degree 7, connects to 2 communities