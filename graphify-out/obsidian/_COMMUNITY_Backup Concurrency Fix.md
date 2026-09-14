---
type: community
cohesion: 0.67
members: 3
---

# Backup Concurrency Fix

**Cohesion:** 0.67 - moderately connected
**Members:** 3 nodes

## Members
- [[Action Endpoints (backup, deploy-container)]] - concept - ultron-backend/README.md
- [[Bug _run_backup() Lacked Collision RecheckLock]] - rationale - ultron-backend/CODE-AUDIT.md
- [[apiPost()]] - code - ultron-dashboard.html

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Backup_Concurrency_Fix
SORT file.name ASC
```
