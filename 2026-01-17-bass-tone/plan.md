# Plan

## Questions

- [x] Traditional synth bass signal chain with octaver?
- [x] Key effects: octaver, envelope filter, fuzz/overdrive order?
- [x] Software vs hardware options for Ableton setup?
- [ ] Try in Ableton: pitch shifter → saturator → auto filter chain

## Future Ideas

- [ ] Port Linux LV2 plugins (e.g., Guitarix octaver) to Windows VST3
  - DSP is platform-agnostic, just need API wrapper + build system
  - Could use JUCE or similar cross-platform framework
  - Good candidate for coding agent assisted porting

## Progress

### 2026-01-17

- Migrated clean tone guide from ableton-document task
- Researched synth bass signal chain - wrote `notes/synth-bass.md`
- Explored octaver plugin options (Pitchproof, KPP, OC-D2)
- Set up VST2 folder at `~/projects/vst2`
