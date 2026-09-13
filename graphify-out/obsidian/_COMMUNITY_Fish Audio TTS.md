---
type: community
members: 3
---

# Fish Audio TTS

**Members:** 3 nodes

## Members
- [[One TTS request to Fish Audio. Returns (audio_bytes, content_type, error).]] - rationale - ultron-backend/app.py
- [[_fish_audio_tts()]] - code - ultron-backend/app.py
- [[tts()]] - code - ultron-backend/app.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Fish_Audio_TTS
SORT file.name ASC
```

## Connections to other communities
- 2 edges to [[_COMMUNITY_Host Status Functions]]
- 2 edges to [[_COMMUNITY_Backend Read Routes]]

## Top bridge nodes
- [[tts()]] - degree 4, connects to 2 communities
- [[_fish_audio_tts()]] - degree 3, connects to 1 community