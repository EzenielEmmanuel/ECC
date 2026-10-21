# MiniMax M3 — Resource Assessment

Reviewed: 2026-10-21.
Identity: MiniMax-M3 language/multimodal model; distinct from MiniMax Music 3.0 and H3.
Status: Official documentation and model-license review only; not downloaded, forked, tested or integrated.

## Official sources
- https://github.com/MiniMax-AI/MiniMax-M3
- https://huggingface.co/MiniMaxAI/MiniMax-M3
- https://huggingface.co/MiniMaxAI/MiniMax-M3/blob/main/LICENSE
- https://www.minimax.io/blog/minimax-m3

## Capabilities and availability
Open weights are available. Official model card describes text/image/video understanding, a 1M-token context, approximately 428B total parameters and 23B activated parameters. Upstream documents coding/agent uses, hosted API access and self-hosted inference frameworks. Performance claims have not been independently reproduced here.

## License — important distinction
The weights use the custom MiniMax Community License, not MIT/Apache. It permits copying and modification subject to terms. Commercial use requires attribution and notice; products/services above USD20 million annual revenue require prior written authorization. The license also contains use restrictions. Read the linked full license for scope before adoption. No licensing notice has been sent and no commercial authorization obtained by this assessment.

## ORIS/SOCRF fit (assessment)
Promising candidate for coding, planning and visual reasoning behind an ORIS-controlled application. The model is not a complete frontend, agent harness or memory service. Evaluate an endpoint first rather than assuming the full weights fit ordinary free cloud hardware. Activated parameters do not mean the remaining weights need no storage or memory. Full 1M context adds further resource demands.

## Evaluation plan
Pin model revision and deployment stack; verify license against intended use. Compare a bounded coding task and image-understanding task with existing models. Measure correctness, latency and total cost. Establish hardware needs from an actual quantization/backend configuration; do not assume an 8GB PC or standard CPU Codespace is suitable. Keep hosted API terms separate from the weights license. Preserve ORIS governance and use project-scoped tool permissions.

Priority: High for controlled evaluation; not approved as a free hosting solution. Current endpoint prices, free quotas and exact hardware minimums were not verified.
