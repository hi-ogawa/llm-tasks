# Local Audio → Streaming Migration

Enabling mobile listening via YouTube Music while keeping YouTube as the primary activity hub.

## Background

**Current workflow:**
- Desktop: YouTube + ublock for discovery/listening
- "Todo" YouTube playlist: bass cover candidates (ephemeral - remove after covering)
- Custom desktop GUI app (yt-dlp-like) to download with proper metadata
- VLC downloads: permanent archive, superset of todo playlist
- Mobile: VLC for commuting, browsing curated collection by artist

**Pain point:** Manual download/transfer workflow for mobile listening

**YouTube Music state:** Only 8 songs in library (from rare likes + official song associations)

## Goal

Primary: VLC collection accessible on mobile via YouTube Music

Secondary:
- "Todo" playlist items sync to YT Music library
- Recover removed "todo" items by cross-referencing VLC downloads
- Handle unofficial content (live performances, etc.) gracefully

**Open to:** Changing YouTube habits (e.g., liking videos) if it replaces the local download workflow

## Constraints

**YouTube Music "Artists tab" limitation:**
- Only shows content with official music metadata (ISRCs) - "songs"
- Regular YouTube videos (covers, live performances, unofficial) don't appear
- See `notes/youtube-music-library.md` for details

**Implication:** Not all VLC content will get Artists tab organization. Unofficial content still accessible via Liked playlist or custom playlist - just no per-artist mobile browsing.

## Conclusion

**Yes, YouTube + YouTube Music can replace the VLC workflow.**

New workflow:

**On YouTube (main activity):**
1. Add to "Good music" playlist
2. (Optional) Also add to "todo" playlist if bass practice candidate

**On YT Music (async, when needed for mobile):**
3. Review "Good music" playlist
4. For songs with "Add to library" option → do it → Artists tab

**Why this works:**
- "Save" action stays on YouTube (playlist, not like)
- "Organize" action happens async on YT Music
- Keeps curated music separate from likes (which affect recommendations)
- Still simpler than: download → transfer → VLC

**Deferred:** Fallback playlist for non-library-able songs. Revisit when filtering becomes needed.

## Next Steps

Migrate existing VLC collection (batch import) - see `plan.md`

## Files

- `plan.md` - Detailed planning, research, and progress
- `notes/` - Research findings
