# LTX-2 upstream verification and SOCRF integration gates

Verified on 2026-10-11 by reading the upstream GitHub repository
`Lightricks/LTX-2` README, LICENSE files and pyproject.toml, plus the Hugging
Face `Lightricks/LTX-2.5` model page references in the README. Nothing was
installed, downloaded, or executed.

## Confirmed upstream facts
- Repository: https://github.com/Lightricks/LTX-2 (9.7k stars, 1.5k forks, 53 commits, public).
- **Code and weights are NOT open source.** They are distributed under the **LTX Community License Agreement**, a custom license with two files: `LICENSE-2` (LTX-2, dated January 5 2026) and `LICENSE-2_x` (LTX-2.x, dated August 11 2026, covering LTX-2.5 and later).
- Python `>=3.11`, `torch 2.13+cu132`, package manager `uv`; monorepo of `ltx-core`, `ltx-pipelines` and `ltx-trainer`. The `natten` backend is Linux + CUDA only and falls back to Triton or eager neighbourhood attention elsewhere.
- Weights: gated Hugging Face repository `Lightricks/LTX-2.5`, accepted model terms and a read token required. The standard component set is roughly **66 GiB** (22B distilled transformer, Gemma 4 12B text encoder, video and audio VAEs, spatial upscaler).
- Capabilities: audio-video DiT generation, image-to-video, keyframe interpolation, audio-to-video, retake, dubbing, HDR/EXR output, prompt enhancement, ComfyUI integration.
- Defaults: 1024x1536 at 24 fps; UHD 4K is 3840x2176. DistilledPipeline is the fast path (8 stage-1 steps, 4 stage-2 steps); DFR is the production-quality path.

## Not yet verified
- The exact license obligations, redistribution terms and commercial-use position — the full license text has not been legally reviewed.
- Whether gated access is granted to a SOCRF identity, and at what cost.
- Real GPU VRAM usage, generation time and per-clip cost on rented hardware.
- Whether an `ltx.io` API tier would be cheaper than self-hosting for SOCRF's expected volume.

## Integration gates
1. **Legal review (blocking).** Read `LICENSE-2_x` in full before any use in a product, and decide whether the custom license is acceptable for KEYS, HotWavz Plus and future platforms.
2. Decide the access route: gated self-hosted weights (~66 GiB, CUDA GPU) versus the paid `ltx.io` API. No decision has been made.
3. If self-hosting: accept model terms with a least-privilege Hugging Face read token from the credential vault, provision an isolated GPU sandbox, then verify VRAM and cost with a single short clip.
4. Add explicit cost budgets per clip, generation timeouts, output validation and audit logging.
5. Enable live execution only after contract tests, cost validation and security review, per SOCRF governance.

The existing `socrf/adapters/ltx_dry_run.py` is an offline planning stub. It downloads nothing and makes no network calls.
