# Ableton Live Lite Setup

Extracted from `2026-01-07-ableton-document/docs/workflow.md`.

## Plugin Management

**Plugin Formats:**

- **VST3** (.vst3) - Modern standard, use this for Ableton
- **VST2** (.dll) - Older format, manual folder setup required
- **AAX** - Pro Tools only, skip
- **Standalone** - Runs without DAW, useful for testing

**VST Folder Locations (Windows):**

- **VST2**: `~/projects/vst2` (my choice, avoids admin prompts)
- **VST3**: `C:\Program Files\Common Files\VST3\` (fixed by spec, installers handle this)

**Ableton Plugin Config:**

1. Preferences → Plug-Ins
2. VST3: Enable "Use VST3 Plug-in System Folder"
3. VST2: Enable "Use VST Plug-In Custom Folder" and set path
4. Click "Rescan"

## Latency Settings

- Sample Rate: 44100 Hz
- Buffer Size: 128 samples (~15ms round-trip)
- Lower option: 64 samples (~7-8ms, test stability)

Adjust in: Preferences → Audio → Buffer Size

## Signal Chain (Practice)

Basic chain for daily practice:

1. Tuner
2. Amp sim (Live Lite built-in or plugin)
3. Reverb

## Blending with Backing Tracks

**Driver-level blend** (YouTube + DAW):

- Browser audio through Windows audio
- Live Lite through ASIO
- Focusrite blends both
- Match sample rates: Windows Sound Settings → Scarlett → 44100 Hz

**DAW-internal** (better for recording):

- Import backing track WAV into Live Lite
- Everything through ASIO, no sample rate issues
