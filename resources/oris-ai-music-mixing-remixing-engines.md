# ORIS AI Music Mixing & Remixing Engines — Research Registry
Date: 2026-10-22
Status: research candidates only; not installed, forked, tested, or integrated.

## Objectives
1. Autonomously mix original multitrack sessions (vocals, drums, bass, instruments), including reggae/dancehall.
2. Separate already-mixed songs into stems, remix, replace instruments, and eventually produce alternate-genre arrangements.
3. Reference-based and streaming-ready mastering; export WAV, MP3 and stems; Windows DAW integration (FL Studio, Pro Tools).
4. Prefer free/open-source components and preserve ORIS independence.

## Autonomous / intelligent mixing research
- Sony FxNorm-Automix — https://github.com/sony/fxnorm-automix — research automatic mixing; check model/data availability.
- Diff-MST — https://github.com/sai-soum/Diff-MST — reference-guided multitrack mixing; check noncommercial license.
- Neural Mixing Console — https://github.com/stevemurr/neural-mixing-console — experimental neural parameter prediction; not production-ready.
- Automix Toolkit — https://github.com/csteinmetz1/automix-toolkit — research/training toolkit.

## Studio / agent-controllable frontends
- Audiola — https://github.com/fgilde/Audiola — inspect multitrack editor, separation and mastering.
- SoundCraft — https://github.com/storytold/soundcraft — inspect Rust DAW and automation/agent controls.
- Isolate — https://github.com/mc-acoustics/Isolate — inspect local separation and mixing interface.

## Stem separation and reconstruction
- Demucs — https://github.com/adefossez/demucs — archived upstream; separation backend candidate.
- StemSplit — https://github.com/StemSplit — inspect ONNX implementations and licenses.
- StemForge — https://github.com/tsondo/StemForge — inspect separation/MIDI reconstruction workflow.

## Audio processing / mastering
- Spotify Pedalboard — https://github.com/spotify/pedalboard — plugin hosting and DSP backend candidate.
- Matchering — https://github.com/sergree/matchering — reference mastering; GPL-3.0 implications.

## Commercial benchmarks (not assumed open-source)
- RoEx Automix — https://automix.roexaudio.com/
- StemDesk — https://stemdesk.ai/
- iZotope Neutron — https://www.izotope.com/products/neutron/
- TonalBrain — https://tonalbrain.com/
- sonible — https://www.sonible.com/
- LANDR — https://www.landr.com/ai-music-tools

## Proposed prototype
Multitrack import -> analysis / automatic mix parameter proposal -> Spotify Pedalboard DSP -> render/export.
Stereo import -> Demucs stems -> remix/arrangement workflow -> processing -> mastering/export.
Candidate initial stack: Pedalboard + Sony FxNorm-Automix + Demucs. Audiola/SoundCraft to be evaluated for UI/agent orchestration.

## Evaluation checklist
Verify each URL, current maintenance, license and model-weight permissions, commercial-use restrictions, Windows/Codespaces compatibility, CPU/GPU/RAM requirements, audio quality and artifacts, DAW plugin support, reproducibility, and security. No repository should be represented as integrated before actual tests. Prioritize a small reggae/dancehall multitrack test and a stereo-to-stems remix test.
