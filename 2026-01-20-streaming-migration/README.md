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

**On YT Music (async, when needed for mobile):** 3. Review "Good music" playlist 4. For songs with "Add to library" option → do it → Artists tab

**Why this works:**

- "Save" action stays on YouTube (playlist, not like)
- "Organize" action happens async on YT Music
- Keeps curated music separate from likes (which affect recommendations)
- Still simpler than: download → transfer → VLC

**Fallback playlist:** For non-library-able songs (OMV/UGC), use `scripts/export_non_library.py` to copy them to a separate playlist for mobile access.

## Results

Migration of 727 unique tracks from VLC collection:

| Category          | Count | %   |
| ----------------- | ----- | --- |
| Art Tracks (ATV)  | 458   | 63% |
| Non-ATV (OMV/UGC) | 269   | 37% |

**What this means:**

- 63% get full Artists tab experience (browse by artist on mobile)
- 37% are in fallback playlist only (no artist organization)
- Within non-ATV, some are unplayable on YT Music entirely (licensing issues)

**Why non-ATV is high:**

- Live performances, covers, unofficial content
- Indie/smaller labels without YT Music distribution deals
- Some Asian labels focused on home market streaming (not YT Music)

**Verdict:** ~60-70% good experience, not the 90-95% hoped for. Collection has a lot of non-mainstream content that doesn't fit YT Music's library model.

## Follow-up (2026-02-14)

After using YT Music passively for a while (mostly looping `Good music`), we did a manual false-positive cleanup pass:

- Reviewed playlist entries on PC
- Replaced clearly wrong/unofficial picks with official song versions where available
- Kept entries when they mapped correctly to YT Music counterparts even if channel looked like distributor/mirror (`1theK`, `avex`, etc.)

### Current snapshot (after cleanup)

Dry run from `scripts/playlist_to_library.py`:

- Total tracks in `Good music`: 713
- Art Tracks already in library: 441
- Art Tracks pending add: 156
- Non-ATV skipped: 116

Derived fractions:

- ATV total: 597/713 (83.7%)
- Non-ATV: 116/713 (16.3%)

Compared to migration-time snapshot (37% non-ATV), non-ATV fraction improved substantially.

```sh
$ uv run python scripts/playlist_to_library.py -p PL7sA_SkHX5ydlos2CA-8zf9Smx3Ph7xtE -n
Checking credentials...
Auth OK
Fetching playlist PL7sA_SkHX5ydlos2CA-8zf9Smx3Ph7xtE...
Found 713 tracks

Art Tracks to add: 156
Already in library: 441
Skipped (OMV/UGC): 116

[DRY RUN] Would add 156 tracks to library
```

### Practical conclusion

- For passive listening (`Good music` + occasional Likes), ATV/non-ATV distinction is mostly irrelevant
- Library/Artists-tab behavior matters only when doing explicit library organization
- Use manual replacement only for obvious false positives or when artist-tab quality matters

### Auth helper for Chrome

`ytmusicapi browser` is Firefox-oriented, so this task now includes a Chrome helper:

```bash
uv run python scripts/chrome_auth_to_ytmusic.py
```

Preferred real workflow:

1. In Chrome DevTools Network, copy one YT Music API request as `Copy as cURL (bash)`
2. Pipe/paste that into `scripts/chrome_auth_to_ytmusic.py`
3. Script writes `data/ytmusicapi-browser.json`
4. Validate with dry run (`playlist_to_library.py -n`)

Security note: copied curl blobs can contain full session cookies; do not commit raw dumps.

## Files

- `plan.md` - Detailed planning, research, and progress
- `notes/` - Research findings
