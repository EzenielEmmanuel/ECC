# Hermes Agent — Resource Registry

- Official repository: https://github.com/NousResearch/hermes-agent
- Documentation: https://hermes-agent.nousresearch.com/docs/
- Publisher: Nous Research
- Category: Self-improving personal AI agent and multi-channel agent runtime
- License: MIT
- Status: High-priority private adaptation candidate; documented, not installed or integrated
- Priority: Very high
- Reviewed: 2026-10-18

## Core strengths

- Persistent user memory and cross-session conversation search
- User-profile development through MEMORY.md and USER.md
- Learning loop that creates and improves reusable skills
- Parallel isolated subagents
- Natural-language scheduled tasks
- MCP integration and extensible toolsets
- Model-provider independence
- Terminal, desktop and messaging access
- Local, Docker, SSH, VPS and serverless execution backends
- Telegram, Discord, Slack, WhatsApp, Signal and other communication channels

## Why it matters to ORIS

Hermes is a strong candidate for the adaptive personal-intelligence layer of ORIS. Its memory, skill evolution, user modeling, delegation and multi-channel continuity align closely with the goal of an assistant that develops with its user over time.

## Fork and adaptation status

Hermes Agent is MIT licensed. Its source may be copied, modified, privately hosted, commercially used and redistributed while retaining the copyright and license notice. A normal GitHub fork of this public repository would remain public. For confidential ORIS development, import or mirror the source into a new private repository and record the upstream remote manually.

## Proposed ORIS evolution

- Replace the frontend, visual identity and interaction model with an ORIS interface.
- Add ORIS governance, authorization, cost controls and auditable execution.
- Map persistent memory into the ORIS project-state and knowledge architecture.
- Govern automatic skill creation through review, provenance and rollback.
- Connect Hermes to OmniRoute for controlled free, subscription, paid and local model routing.
- Integrate ORIS worldview selection without weakening evidence provenance.
- Add voice and real-time conversational interfaces as separate governed adapters.
- Keep provider, messaging and tool permissions modular and least-privileged.

## Evaluation plan

1. Mirror a pinned upstream release into an isolated private test repository.
2. Build in a disposable Codespace or container.
3. Run with one approved low-cost model provider and restricted tools.
4. Test memory accuracy, skill creation, session continuity and subagent isolation.
5. Audit credential storage, shell execution, messaging authentication and prompt-injection boundaries.
6. Measure token cost, latency and performance before choosing which subsystems to retain.
7. Maintain an upstream-change ledger so selected improvements can be reviewed and merged safely.

## Governance

Do not expose production accounts, unrestricted shell access, personal communications or repository-wide credentials during evaluation. Default all consequential tools to disabled or approval-gated. Preserve the MIT notice and upstream attribution. Treat learned skills and persistent memories as governed artifacts with provenance, inspection and deletion controls.
