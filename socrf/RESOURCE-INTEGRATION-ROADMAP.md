# SOCRF Resource Integration Roadmap

Source registry: EzenielEmmanuel/ORIS-Workshop, branch `oris-workshop`, `resources/` and `strategy/`.

## Architecture
ECC skills/agents/commands -> SOCRF governed capability adapters -> ORIS Workshop orchestration and approval gates -> external tool/model services -> human-centered products.

Keep original upstream projects independently identifiable. Register adapters rather than copying entire codebases into ECC. Preserve licenses, source provenance, and independent updates.

## Integration candidates (not installed yet)

| Resource | SOCRF role | Priority | Gate |
|---|---|---|---|
| Octop | Optional multi-agent coordination service | 1 | Verify repository/license; compare to ECC/ORIS; sandbox tool permissions |
| FreeLLMAPI | Optional provider gateway for low-cost model routing | 2 | Verify providers, quota claims, terms, secrets handling, uptime |
| Ornith 1.0/1.5 | Research on adaptive/self-scaffolding task workflows | 3 | Verify source and weights, licenses, reproducible benchmarks |
| LTX 2.5 | On-demand GPU-backed media/video production | 4 | Verify exact release, code and weight licenses, GPU costs |

## First build increment
1. Inspect ECC agent/skill/command conventions and test suite.
2. Create a **resource registry schema**: id, upstream, role, license, deployment mode, permissions, costs, maturity, health, owner.
3. Build a **dry-run capability adapter** for Octop (no external execution or secrets).
4. Add test cases for least-privilege access, human approval, failure handling, cost budgets and provenance.
5. Only after approval and passing tests, connect live services in an isolated cloud sandbox.

## Boundaries
No API keys in Git. No production credentials or unrestricted shell/browser permissions for autonomous agents. No assumption that advertised free tokens or model versions are verified. Do not modify upstream ECC baseline branch; use `socrf-development` and small reviewed branches.

## Foundational strategy
The factory produces capabilities; ORIS Workshop transforms capabilities into systems; KEYS, HotWavz Plus and ORIZE'N Global transform systems into human opportunities.
