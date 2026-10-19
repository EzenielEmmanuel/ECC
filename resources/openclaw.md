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

OpenClaw is a strong candidate for its own ORIS-evolved high-level agent fork. The intended path mirrors the evolution of OpenCode into ORIS Code: retain OpenClaw as a complete working application, upgrade its frontend and user experience, then progressively extend its capabilities according to its strengths in communications, devices, plugins and local-first personal assistance.

## Fork and adaptation status

OpenClaw's first-party source is MIT licensed. It may be copied, modified, privately hosted, commercially used and redistributed while retaining the copyright and license notice. Incorporated or adapted third-party code has additional attribution recorded in THIRD_PARTY_NOTICES.md and those notices must be preserved.

A normal GitHub fork of this public repository would remain public. Confidential ORIS work should begin as a private imported or mirrored repository with an upstream remote maintained separately.

## Independent evolutionary-fork strategy

OpenClaw should remain a distinct high-level agent project rather than being reduced to a subsystem of another fork. Development should proceed in stages:

1. Reproduce and stabilize the complete upstream application.
2. Upgrade its existing frontend, navigation, visual system and interaction experience.
3. Establish the ORIS identity and governance layer while preserving upstream attribution.
4. Improve OpenClaw's strongest native faculties: channels, device reach, plugins, gateways and local-first operation.
5. Add new capabilities incrementally, with tests and rollback for every major subsystem.
6. Connect optional model routing, memory and intelligence services only where they strengthen this fork without erasing its distinct identity.
7. Maintain this evolved OpenClaw line as a separate ORIS family application, comparable to the evolution of OpenCode into ORIS Code.

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
