# OmniRoute AI — Resource Registry

- Official repository: https://github.com/diegosouzapw/OmniRoute
- Website: https://omniroute.online
- Category: Open-source AI model gateway and quota-aware router
- License: MIT (verified from the upstream repository; recheck before integration)
- Status: Candidate for evaluation; documented, not installed or integrated into SOCRF
- Priority: High
- Reviewed: 2026-10-18

## What it provides

- One OpenAI-compatible endpoint for many model providers
- Automatic routing and fallback based on quota, health, cost, latency and task type
- Presets for coding, speed, low cost, subscriptions and offline/local capacity
- Custom routing strategies, including priority, cost-optimized, context-aware, fusion and pipeline routes
- Compatibility claims for tools including Codex, OpenCode, Cursor, Cline and Claude Code
- MCP and A2A support, self-hosting, headless operation, desktop interface and PWA

## Why it may help ORIS/SOCRF

OmniRoute could become a provider-routing layer between ORIS/SOCRF and free, subscription, paid or locally hosted models. It may reduce interruptions by moving eligible work to another configured provider when quota is exhausted or a service fails. It could also centralize provider selection for coding, research and low-cost workloads.

## Important limitation

OmniRoute does not itself grant the advertised aggregate free-token capacity. Users must bring eligible third-party provider accounts and credentials where required. Each provider controls its own availability, quotas, regional requirements, acceptable-use rules and pricing.

## Recommended evaluation

1. Review the current release, dependency manifests, security policy and provider terms.
2. Deploy in an isolated GitHub Codespace or disposable cloud environment.
3. Connect only two approved free-tier providers for the first test.
4. Route OpenCode or another coding client through the local OpenAI-compatible endpoint.
5. Test quota exhaustion, provider failure, context continuity, tool calling and streaming.
6. Measure output quality, token use, latency and failure recovery.
7. Keep credentials outside the repository and disable paid fallback by default.
8. Compare it with FreeLLMAPI and LiteLLM before selecting ORIS's routing layer.

## Governance

Preserve independent ORIS/SOCRF governance. Keep execution disabled until testing is complete. Never commit API keys, cookies or OAuth tokens. Use least-privilege provider accounts, explicit spending limits and fail-closed routing so free-tier exhaustion cannot create an unexpected bill. Preserve the upstream MIT copyright and license notice in any fork or substantial reuse.
