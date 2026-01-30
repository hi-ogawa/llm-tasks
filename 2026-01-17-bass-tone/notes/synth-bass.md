# Synth Bass Tone: Octaver + Filter Setup

Getting synth-like tones from bass guitar using effects.

## Core Signal Chain

```
Bass → Compressor (light) → Octave → Overdrive/Fuzz → Envelope Filter → Amp
```

### Why This Order?

1. **Compressor first** (optional): Evens dynamics, improves octave tracking
2. **Octave early**: Analog octavers need clean signal to track properly
3. **Drive after octave**: Adds harmonics for filter to "chew on"
4. **Envelope filter last**: Reacts to full synth-y signal

## Key Effects

### Octaver

- Adds sub-octave (-1 or -2 octaves below)
- Creates thick, synth-like foundation
- **Analog** (e.g., Boss OC-2, EHX Octave Multiplexer): Warmer, more "synthy", but tracking sensitive
- **Digital** (e.g., Boss OC-5, TC Sub'n'Up): Better tracking, more options

**Tips:**

- Play cleanly for best tracking (especially analog)
- Favor neck pickup for cleaner fundamental
- Single notes track better than chords

**Classic synth bass technique:**

- Play an octave higher than the "actual" bass part
- Let the octaver (-1 oct) fill in the sub bass root
- Example: Part is in E → play at 7th fret (octave E), octaver adds low E
- Result: Thick synth foundation + your articulation on top
- Blend dry signal with octave to taste

### Overdrive/Fuzz

- Adds harmonic content
- Makes tone "fatter" and more aggressive
- Light OD = warm synth; heavy fuzz = aggressive synth

**Placement debate:**

- Before filter = more harmonics for filter to shape (classic)
- After filter = cleaner filter response, then dirtied up

### Envelope Filter (Auto-wah)

- Sweeps filter based on playing dynamics
- Creates the "wah" / "bow" synth sound
- **Sensitivity**: How hard you play to trigger sweep
- **Range/Depth**: How wide the filter sweeps
- **Direction**: Up (classic funk) or down (synth bass)

**Common pedals:** EHX Q-Tron, MXR Bass Envelope Filter, Source Audio Spectrum

## Alternative Chain: Octave After Filter

Some prefer digital octave after filter:

```
Bass → Envelope Filter → Octave (digital) → Drive → Amp
```

- Digital octavers handle filtered signal fine
- Can sound more "synth-y" in a different way
- Experiment to taste

## Classic Synth Bass References

| Artist/Song          | Tone Character                          |
| -------------------- | --------------------------------------- |
| Bootsy Collins       | Envelope filter + octave, funky squelch |
| Muse (Hysteria)      | Fuzz + octave, aggressive               |
| RHCP (Higher Ground) | Envelope filter, funky                  |
| Jamiroquai           | Clean synth-ish, envelope filter        |

## Software Options (Ableton)

### Live Lite (Focusrite bundle)

Live Lite includes: Auto Filter, Saturator, Compressor, Reverb
Missing: Amp, Overdrive, Shifter (no native pitch shifting)

### Octave/Pitch Shifting

**Free plugins (required for Live Lite):**

- **Pitchproof** (Aegean Music) - General pitch shifter, set to -12st for octave down
  - Works but not octaver-style UI (no dedicated Oct1/Oct2/Dry blend)
  - Manage dry/wet manually
- **Kapitonov Plugins Pack** - Includes analog Octaver + tubeAmp, Fuzz, etc.
  - Windows VST3 available (marked "experimental")
  - Ported from Linux/Guitarix ecosystem
- **OC-D2** (Chris Hooker) - True OC-2 emulation with blend controls
  - 32-bit only, won't work in 64-bit Ableton

**Paid option:**

- **Audiority Octaver 82** (~$29) - Proper OC-2 emulation, 64-bit

**Note:** MFreqShifter is a _frequency_ shifter, not pitch shifter.
Adds fixed Hz (breaks harmonics) vs multiplying (preserves pitch).
Good for weird FX, not clean octave-down.

**Hybrid approach:**

- Use Zoom B1 Four for octave (zero latency)
- Send into Ableton for filter/drive

### Filter

- **Auto Filter** with envelope follower mode
- Set "Envelope" amount, adjust attack/release
- BP or LP filter for synth character

### Drive

- **Saturator** - Works well for synth bass warmth/grit

### Example Chain (Live Lite)

```
[Pitchproof -12st] → [Saturator] → [Auto Filter envelope] → [Compressor]
```

## Quick Start Settings

### Octave

- Sub level: 50-70%
- Dry level: 30-50%
- Upper octave: Off or subtle

### Envelope Filter

- Sensitivity: Medium (adjust to playing)
- Range: Wide for synth sweep
- Direction: Down for classic synth bass

### Drive

- Gain: Low-medium (warmth, not distortion)
- Tone: Darker for synth, brighter for cut

## Sources

### Signal Chain & Pedal Order

- [BOSS - Order of Operation: Bass Effects Signal Chain](https://articles.boss.info/order-of-operation-a-guide-to-bass-effects-signal-chain/)
- [TalkBass - Octaver before or after envelope filter?](https://www.talkbass.com/threads/octaver-before-or-after-envelope-filter.1542704/)
- [TalkBass - Pedal order guide](https://www.talkbass.com/threads/pedal-order-a-guide.1358441/)
- [TalkBass - Comps, Synths, Filters & Octaves](https://www.talkbass.com/threads/can-we-talk-about-the-start-of-the-signal-chain-comps-synths-filters-octaves.1456465/)

### Software & Plugins

- [Pitchproof (free pitch shifter)](https://aegeanmusic.com/pitchproof-specs)
- [Kapitonov Plugins Pack (free, includes Octaver)](https://github.com/olegkapitonov/Kapitonov-Plugins-Pack) - Linux origin, experimental Win VST3
- [OC-D2 (free OC-2 emulation, 32-bit only)](https://bedroomproducersblog.com/2015/04/16/free-octaver-vst-plugin/)
- [Audiority Octaver 82 (paid, 64-bit)](https://www.audiority.com/shop/octaver-82/)
- [MFreqShifter | MeldaProduction](https://www.meldaproduction.com/MFreqShifter) - Frequency shifter, not pitch shifter
- [Ableton Live Lite Features](https://www.ableton.com/en/products/live-lite/features/)

### Frequency vs Pitch Shifting

- Pitch shifting: multiplies frequencies (preserves harmonics)
- Frequency shifting: adds fixed Hz (breaks harmonics, metallic FX)
