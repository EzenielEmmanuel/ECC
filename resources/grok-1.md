# Grok-1 — Resource Registry

- Official repository: https://github.com/xai-org/grok-1
- Official weights: https://huggingface.co/xai-org/grok-1
- Publisher: xAI
- Category: Open-weights large language model / mixture-of-experts intelligence
- License: Apache License 2.0 for the released code and associated Grok-1 weights
- Status: Fork candidate for research; documented, not downloaded, executed or integrated
- Priority: High for architectural study; low for near-term deployment
- Reviewed: 2026-10-18

## What it is

Grok-1 is an open-weights 314-billion-parameter mixture-of-experts model. It uses eight experts, activates two experts per token, contains 64 layers and has an 8,192-token context window in the released configuration. The repository supplies JAX example code for loading and sampling from the checkpoint.

Grok-1 is a model intelligence layer, not a complete personal-agent application or frontend. It would require an agent harness, memory, tools, governance and user interface around it.

## Fork and adaptation status

The released source files and Grok-1 weights are licensed under Apache 2.0. They may be copied, modified and used commercially while preserving the required copyright, license and NOTICE obligations. The Grok and xAI names and marks should not be treated as licensed branding.

## Strengths relevant to ORIS

- Sparse mixture-of-experts architecture
- Useful reference for specialized intelligence activated per task
- Open weights and inspectable inference code
- Potential research source for ORIS modular-brain and expert-routing concepts
- Freedom to experiment with quantization, adapters and alternative serving layers within the license

## Practical limitations

- Approximately 314 billion parameters
- Requires substantial multi-GPU memory and storage
- The provided MoE implementation prioritizes clarity over inference efficiency
- Far beyond the present low-cost ORIS deployment target
- The original context length and age make it less practical than newer efficient models for production

## Independent evolutionary-fork strategy

Grok-1 differs from Hermes and OpenClaw because it is a model rather than a complete agent with an existing frontend. Its independent evolution should therefore proceed as a model-centered ORIS project:

1. Preserve and study the complete released Grok-1 model architecture.
2. Explore efficient serving, quantization and specialized expert routing when infrastructure permits.
3. Build an upgraded ORIS frontend and agent experience around the model rather than treating the checkpoint alone as an application.
4. Add memory, tools, governance and other capabilities incrementally around its particular intelligence strengths.
5. Keep this Grok-derived experimental line distinct, with its own tests, identity and roadmap.
6. Delay full-weight deployment until suitable infrastructure and a clear experiment justify the cost.

## Governance

Do not download the checkpoint into ECC. Keep model artifacts in controlled external storage. Preserve Apache 2.0 notices, verify derivative-model licenses, isolate inference, keep credentials outside repositories and require explicit authorization before tool execution or paid compute is enabled.
