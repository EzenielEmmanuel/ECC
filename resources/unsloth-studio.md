# Unsloth Studio — Resource Assessment

Reviewed: 2026-10-20.
Official repository: https://github.com/unslothai/unsloth
Documentation: https://unsloth.ai/docs/new/studio
Installation: https://unsloth.ai/docs/new/studio/install
Status: Official documentation review only; not installed, forked or benchmarked.
Priority: High for evaluation as an ORIS model-development tool (assessment).

## Capabilities
A web interface for running, training and exporting open models. Documents dataset workflows and support across text and other modalities. Windows, Linux, WSL and macOS installation paths exist. The project documents OpenAI-compatible serving and remote access. Platform, model and backend compatibility vary.

## Licensing
Upstream README distinguishes Apache-2.0 core code from AGPL-3.0 Studio UI components. Forkable under the applicable terms; review component-level licenses, notices and source-sharing obligations before modification, distribution or deployment. Base model and dataset licenses remain separate.

## ORIS relevance (assessment)
Potential model workshop for adapting a suitable small open model to ORIS tasks, then testing it behind ORIS-Code or another runtime. It complements orchestration, memory and application construction; fine-tuning does not automatically create those capabilities.

## Hardware and cost assessment
Do not assume an 8GB RAM PC can train the desired model. Inference and training have different requirements; determine fit from model size, quantization, context length, tuning method, GPU VRAM and host RAM. A CPU-only cloud environment should not be assumed suitable for GPU training. Open-source software is not free compute. No free-GPU availability or exact minimum hardware was verified here.

## Evaluation plan
1. Pin an upstream release/commit and inspect component licenses.
2. Choose one task and establish an untuned baseline before deciding whether tuning is needed.
3. Confirm supported OS/backend and budget GPU, storage and checkpoints for the chosen model.
4. Test a small authorized dataset using a supported parameter-efficient method.
5. Compare held-out task quality, memory, latency and total cost; check regressions.
6. Verify export, serving and ORIS client compatibility; preserve provenance and rollback artifacts.

Upstream speed and memory-saving claims are not independently verified. Nothing has been deployed or connected to private project data.
