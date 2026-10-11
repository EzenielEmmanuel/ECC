# FreeLLMAPI upstream verification and SOCRF integration gates

Verified on 2026-10-11 by reading the upstream GitHub repository
`tashfeenahmed/freellmapi` README, LICENSE and package.json. No code was
cloned, installed, or executed, and no provider keys were created.

## Confirmed upstream facts
- Repository: https://github.com/tashfeenahmed/freellmapi (33.2k stars, 4.6k forks, 863 commits, public).
- Code license: **MIT**, Copyright (c) 2026 Tashfeen Ahmed — preserve the notice if any code is copied.
- Runtime: **Node >=20.18.0 <25.0.0** and **npm >=10.0.0** (monorepo: shared, server, client, cli).
- Install paths: upstream one-line installer (requires Docker), docker-compose, npm local development, and desktop release binaries.
- Capability: a self-hosted OpenAI-compatible `/v1` router that aggregates free tiers from 34 providers behind one endpoint, with smart routing, failover, per-key rate tracking and an admin dashboard.
- Security posture: provider keys are AES-256-GCM encrypted in upstream's SQLite store; applications only see one unified token. Local-first and single-user by design.
- Cost: free install tracks a monthly model-catalog snapshot. An optional paid live-catalog subscription ($19/yr) exists and is **not required**.

## Not yet verified
- Upstream code quality, dependency tree size, and vulnerability status (no clone or audit performed).
- Actual free-tier quotas, provider terms of service, and whether those terms permit SOCRF's intended use.
- Uptime and behaviour of the self-hosted router under SOCRF's traffic pattern.

## Integration gates
1. **Usage review (blocking).** The upstream project describes itself as *personal experimentation only*. Legal/usage review is required before any commercial or product-facing use.
2. Credentials must live in the SOCRF credential vault; never in the repository, never passed as call arguments.
3. Pin the Node runtime and audit the dependency tree in an isolated sandbox before any install.
4. Add per-provider quota budgets, request timeouts, failover policy and audit logging.
5. Enable live execution only after contract tests and security review, per SOCRF governance.

The existing `socrf/adapters/freellmapi_dry_run.py` is an offline planning stub, not a client. No network calls or secrets are involved.
