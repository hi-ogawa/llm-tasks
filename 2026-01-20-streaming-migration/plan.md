# Plan

## Phase 1: Evaluate workflow viability ✅

**Question:** Can YouTube + YouTube Music replace VLC workflow?

**Research:** See `notes/youtube-music-library.md`

- Artists tab only shows Art Tracks (official music with ISRCs)
- Linked music videos can be added to library via YT Music
- Regular videos (covers, live performances) → Liked playlist only

**Conclusion:** Yes, workable.

New workflow:

1. Add to "Good music" playlist on YouTube
2. Async review on YT Music → "Add to library" if available
3. Listen on mobile

---

## Phase 2: Map local files → YouTube video IDs 🔄

### Data extraction

**Source:** 738 opus files in `D:\music\Download` (Windows)

**Filename format:** `Artist - Title.opus` (already searchable)

```bash
# Extract clean queries from Windows file list
grep '\.opus"$' data/files.txt | \
  sed 's|.*\\||; s|\.opus"$||; s|^"||' | \
  sort > data/queries.txt
```

### Search script

`scripts/search_youtube.py` - async batch YouTube search

**Usage:**

```bash
python search_youtube.py --start 0 --end 100      # test batch
python search_youtube.py --overwrite              # full run, overwrite
python search_youtube.py --concurrency 5          # slower, gentler
```

**How it works:**

- Runs `yt-dlp --flat-playlist -j "ytsearch1:{query}"` for each line
- Async with semaphore for parallel execution
- Outputs JSONL with: index, query, video_id, title, channel, view_count, confidence

**Confidence scoring:**

- `high` = artist in channel/title AND song in title
- `medium` = artist OR song matches
- `low` = neither matches (likely false positive)
- `none` = no search result

### Re-scoring

`scripts/rescore.py` - re-process confidence scores without re-searching

**Usage:**

```bash
uv run rescore.py                # re-score in place
uv run rescore.py -o new.jsonl   # output to different file
```

**Why separate script:**

- Tweak scoring algorithm without re-running 738 YouTube searches
- Normalizes punctuation (`-:_.'` etc.) for fuzzy matching
- Handles Windows filename artifacts (e.g., `ME-I` vs `ME:I`)

### Output

`data/results.jsonl` - one JSON object per line:

```json
{
  "index": 0,
  "query": "APRIL - Dream Candy",
  "video_id": "H2T1yZbTMzo",
  "title": "...",
  "channel": "1theK",
  "confidence": "high"
}
```

**Results (738 queries):**

| Confidence | Count | %   |
| ---------- | ----- | --- |
| high       | 545   | 74% |
| medium     | 158   | 21% |
| low        | 31    | 4%  |
| none       | 4     | 1%  |

703/738 (95%) high or medium → ready for import

### Manual review list

```bash
# Extract low/none confidence for manual review
jq -r 'select(.confidence == "low" or .confidence == "none") |
  "\(.index)\t\(.confidence)\t\(.query)\t\(.title // "N/A")\t\(.channel // "N/A")"' \
  data/results.jsonl | sort -n > data/review.tsv
```

`data/review.tsv` - tab-separated: index, youtube URL, confidence, query, matched title, matched channel

---

## Phase 3: Review & batch import ✅

### Manual review

1. ✅ Reviewed low/none confidence matches
2. ✅ Kept 12 low + 3 none (need manual search)
3. ✅ Dropped 19 low + 1 none

review-low.tsv and review-none.tsv are manually handled and added to the playlist.

### Automation scripts

**Research:** Evaluated batch import options in `notes/batch-import-options.md`

- Chose `ytmusicapi` (Python library that emulates YT Music web client)
- Requires browser auth from `music.youtube.com` (not youtube.com)

**Scripts:**

Target playlist: https://www.youtube.com/playlist?list=PL7sA_SkHX5ydlos2CA-8zf9Smx3Ph7xtE

`scripts/import_to_playlist.py` - Import videos to playlist

```bash
uv run python scripts/import_to_playlist.py -i data/results.jsonl -c high -p PL7sA_SkHX5ydlos2CA-8zf9Smx3Ph7xtE
uv run python scripts/import_to_playlist.py -i data/results.jsonl -c medium -p PL7sA_SkHX5ydlos2CA-8zf9Smx3Ph7xtE

# dry run
uv run python scripts/import_to_playlist.py -i data/results.jsonl -c high -p PL7sA_SkHX5ydlos2CA-8zf9Smx3Ph7xtE -n
```

`scripts/playlist_to_library.py` - Add eligible songs to library (Artists tab)

```bash
uv run python scripts/playlist_to_library.py -p PL7sA_SkHX5ydlos2CA-8zf9Smx3Ph7xtE

# dry run
uv run python scripts/playlist_to_library.py -p PL7sA_SkHX5ydlos2CA-8zf9Smx3Ph7xtE -n
```

`scripts/export_non_library.py` - Export OMV/UGC (non-library-able) to fallback playlist

Target playlist: https://www.youtube.com/playlist?list=PL7sA_SkHX5ycNBiSYfwrSwp_xO50JcF0G

```bash
uv run python scripts/export_non_library.py -s PL7sA_SkHX5ydlos2CA-8zf9Smx3Ph7xtE -t PL7sA_SkHX5ycNBiSYfwrSwp_xO50JcF0G

# dry run
uv run python scripts/export_non_library.py -s PL7sA_SkHX5ydlos2CA-8zf9Smx3Ph7xtE -t PL7sA_SkHX5ycNBiSYfwrSwp_xO50JcF0G -n
```

**What it does:**

- Reads source playlist, filters to non-ATV tracks (OMV/UGC)
- Skips tracks already in target playlist
- Adds remaining to fallback playlist

⚠️ **WARNING: Propagation delay**

`edit_song_library_status()` may not commit all tracks immediately. Run multiple times until "Art Tracks to add" reaches 0:

```
Run 1: 296 to add → 296 added
Run 2: 100 to add → 100 added  (not 0!)
Run 3: 34 to add → 34 added
Run 4: 0 to add → done
```

**How "Add to library" works:**

- Only Art Tracks (MUSIC_VIDEO_TYPE_ATV) can be added to library
- `get_playlist()` returns `feedbackTokens` directly for ATVs (no album fetch needed)
- Calls `edit_song_library_status()` with tokens
- OMV/UGC are skipped (no library support)

**Auth validation:**

- Uses known counterpart pair (Dirty Loops - Next to You) as auth check
- Stale auth causes `get_playlist()` to return degraded data (missing album info, missing tokens)
- See `notes/art-track-mapping.md` for counterpart API research

### Auth setup

⚠️ **WARNING: Credentials go stale quickly (hours, not days)**

Symptoms of stale auth:

- Script runs but adds fewer tracks than expected
- `get_playlist()` returns ATVs without `feedbackTokens`
- Counterpart lookups return `None`

To refresh:

1. Go to `music.youtube.com` (logged in)
2. DevTools → Network → find any `/browse` POST request
3. Copy `Authorization` and `Cookie` headers
4. Update `data/ytmusicapi-browser.json`:

```json
{
  "Accept": "*/*",
  "Authorization": "===== paste here =====",
  "Content-Type": "application/json",
  "X-Goog-AuthUser": "0",
  "x-origin": "https://music.youtube.com",
  "Cookie": "===== paste here ======"
}
```

The script validates auth using a known counterpart pair before proceeding.

---

## Phase 4: Post-migration cleanup & re-baseline (2026-02-14) ✅

### What changed

- Initial migration had false positives where search picked non-ATV videos
- Manual review/replacement pass was done on PC against `Good music`
- Some distributor channels (`1theK`, `avex`) were kept when mapping behaved correctly

### Manual cleanup workflow that worked

1. Open `Good music` in YT Music web
2. Spot obvious false positives (wrong upload/non-official-ish content)
3. Search artist + title in YT Music
4. Add better official/ATV-mapped candidate first
5. Remove old wrong entry second (never remove first)

This was efficient enough and avoided over-automation complexity.

### Re-audit commands

```bash
uv run python scripts/playlist_to_library.py -p PL7sA_SkHX5ydlos2CA-8zf9Smx3Ph7xtE -n
uv run python scripts/export_non_library.py -s PL7sA_SkHX5ydlos2CA-8zf9Smx3Ph7xtE -t PL7sA_SkHX5ycNBiSYfwrSwp_xO50JcF0G -n
uv run python scripts/find_duplicates.py -p PL7sA_SkHX5ydlos2CA-8zf9Smx3Ph7xtE
```

### Re-audit snapshot

From `playlist_to_library.py -n`:

- Total: 713
- Art Tracks to add: 156
- Already in library: 441
- Skipped non-ATV: 116

Derived:

- ATV = 597/713 (83.7%)
- Non-ATV = 116/713 (16.3%)

### Auth acquisition (Chrome)

New helper script:

```bash
uv run python scripts/chrome_auth_to_ytmusic.py
```

Input format: one Chrome DevTools `Copy as cURL (bash)` request from `music.youtube.com`.

Then validate with dry run before any write operations.
