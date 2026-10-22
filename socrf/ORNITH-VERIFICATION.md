# Ornith upstream verification and SOCRF integration gates

Verified on 2026-10-11 by reading the upstream GitHub repository
`ornith-ai/Ornith-1` and the Hugging Face model page for
`ornith-ai/Ornith-1.5-9B`. No weights were downloaded, no server was started,
and no GPU was provisioned.

## Confirmed upstream facts
- Repository: https://github.com/ornith-ai/Ornith-1 (2.1k stars, 206 forks, 20 commits, public).
- Repository content: README, LICENSE and assets only — **the repository ships no code**. It is a research release, not an installable package.
- Repository license: **MIT**.
- Weights: https://huggingface.co/ornith-ai/Ornith-1.5-9B, licence recorded as **mit** on Hugging Face, ~10B parameters, safetensors BF16, roughly **19 GB** for the 9B checkpoint.
- Serving runtimes required: **Transformers >= 5.8.1**, **vLLM >= 0.19.1**, **SGLang >= 0.5.9**.
- Interface: OpenAI-compatible `/v1` chat completions with a reasoning parser and tool-call parsing, 262,144-token context (extendable with YaRN RoPE scaling).
- Hardware: the dense 9B checkpoint serves on a **single 80 GB GPU**; MoE 35B/397B checkpoints need multi-GPU tensor parallelism. GGUF builds exist for llama.cpp/Ollama, MLX builds for Apple Silicon.
- Family: Ornith-1.0 and Ornith-1.5, both MIT licensed and free of regional limitations per the README.

## Not yet verified
- No reproducible benchmark has been run by SOCRF; all figures above are upstream-reported.
- **Documentation inconsistency:** the README serving commands reference a `deepreinforce-ai/Ornith-1.5-*` namespace, while the checkpoint tables and Hugging Face collection use `ornith-ai/...`. Only `ornith-ai/Ornith-1.5-9B` has been directly confirmed to exist.
- Memory, throughput and cost on a rented GPU; nothing has been provisioned.
- Training/self-improvement pipeline: only the model artefacts are published, not the loop implementation.

## Integration gates
1. Resolve the `deepreinforce-ai` vs `ornith-ai` namespace discrepancy against the official Hugging Face collection before referencing any checkpoint.
2. Provision an isolated cloud sandbox GPU host (or local 80 GB GPU) with least-privilege credentials; weights download is a separate reviewed step.
3. Pin vLLM/SGLang and Transformers versions, then run contract tests against `/v1/chat/completions`.
4. Add sampling-parameter presets, timeouts, token budgets and audit logging.
5. Enable live execution only after contract tests and security review, per SOCRF governance.

The existing `socrf/adapters/ornith_dry_run.py` is an offline planning stub. It performs no downloads and no network calls.
