# Bonto — Cloud Application Deployment

Website: https://bonto.dev/pricing
Recorded: 2026-10-30
Status: Candidate resource; evaluation pending

Potential use: Host lightweight ORIS services, previews, websites and apps built by specialized agents. Investigate GitHub deployment workflows and MCP agent integrations. Advertised unlimited app deployments are subject to per-app resources and plan restrictions.

Critical caveat: GPU acceleration, GPU passthrough, and running local inference models on Bonto are NOT confirmed. Cloud hosting does not imply GPU access. Do not treat Bonto as a substitute for dedicated 12–24GB VRAM inference infrastructure without evidence.

Next steps: (1) Verify current plan quotas and always-on limits. (2) Ask provider whether GPU is available to user containers and whether self-hosted AI models are permitted. (3) Prototype a free-tier app connected to an external model API. (4) Benchmark deployment and latency before subscribing.

Architecture concept: ORIS cloud inference/agent runtime -> GitHub -> Bonto app deployment (subject to compatibility).
