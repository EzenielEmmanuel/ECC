# OpenClaw — Resource Registry

- Official repository: https://github.com/openclaw/openclaw
- Website: https://openclaw.ai
- Publisher: OpenClaw Foundation
- Category: Local-first personal AI assistant, communications gateway and device-agent platform
- License: MIT for first-party source; preserve THIRD_PARTY_NOTICES.md
- Status: High-priority private adaptation candidate; documented, not installed or integrated
- Priority: Very high
- Reviewed: 2026-10-18

## Core strengths

- Personal assistant runtime with local ownership of state, memory and credentials
- Replaceable model and agent-harness plugins, including local-model support
- One gateway for personal or team deployment
- More than twenty communication channels and platform adapters
- Native and web experiences across Windows, Linux, macOS, Android and iOS
- Tools, skills, plugins, device nodes and MCP support
- Extensible plugin SDK and broad integration surface
- Architecture that separates trusted gateway coordination from restricted execution
- Local-first operation with optional external model providers

## Why it matters to ORIS

OpenClaw is a strong candidate for the embodiment, communications and device-integration layer of ORIS. Its broad platform reach and plugin architecture could provide the connective structure through which ORIS communicates, acts and maintains continuity across devices.

## Fork and adaptation status

OpenClaw's first-party source is MIT licensed. It may be copied, modified, privately hosted, commercially used and redistributed while retaining the copyright and license notice. Incorporated or adapted third-party code has additional attribution recorded in THIRD_PARTY_NOTICES.md and those notices must be preserved.

A normal GitHub fork of this public repository would remain public. Confidential ORIS work should begin as a private imported or mirrored repository with an upstream remote maintained separately.

## Proposed ORIS evolution

- Replace the lobster-themed frontend and product presentation with the ORIS visual system.
- Preserve the modular gateway, channels, applications, nodes and plugin interfaces.
- Add ORIS authorization, cost controls, explainability and execution records.
- Integrate Hermes-derived learning, memory and skill-evolution concepts behind governance gates.
- Connect OmniRoute as a controlled model-routing option.
- Add explicit separation between personal memory, project memory and shared-team memory.
- Use restricted sandboxes for shell, browser, filesystem and device actions.
- Keep each channel and tool independently revocable.

## Evaluation plan

1. Mirror a pinned upstream release into an isolated private repository.
2. Inventory first-party code, bundled assets, trademarks and third-party notices.
3. Build the core gateway and web interface without connecting personal messaging accounts.
4. Replace branding only after the clean build is reproducible.
5. Test one model, one sandboxed tool and one non-sensitive channel.
6. Audit authentication, plugin permissions, prompt-injection defenses and secrets handling.
7. Measure runtime footprint and identify subsystems that ORIS should adopt, adapt or omit.
8. Track upstream security fixes and selectively merge reviewed changes.

## Governance

Never connect live personal accounts during the first evaluation. Keep credentials outside source control, restrict filesystem and command access, and require approval for consequential actions. Preserve the MIT license, OpenClaw Foundation copyright notice and THIRD_PARTY_NOTICES.md. Do not imply endorsement by the OpenClaw Foundation or use protected upstream branding for the ORIS derivative.
