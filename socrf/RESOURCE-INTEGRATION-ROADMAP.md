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

### Verification status (2026-10-11)

| Resource | Availability | License | Install / runtime | Cost posture |
|---|---|---|---|---|
| FreeLLMAPI | Verified public repo, 33.2k stars | MIT (code) | Node >=20.18.0 <25.0.0, Docker or npm | Free tier; self-hosted. Usage review required (upstream labels it personal experimentation only) |
| Ornith 1.5-9B | Verified public repo (docs only) + Hugging Face checkpoint | MIT (repo and weights) | Transformers >=5.8.1, vLLM >=0.19.1 or SGLang >=0.5.9; single 80 GB GPU | Weights free; GPU host required. ~19 GB download, not pulled |
| LTX 2.5 | Verified public repo + gated Hugging Face weights | LTX Community License Agreement (custom, non-OSI) | Python >=3.11, torch 2.13+cu132, uv; CUDA GPU | ~66 GiB gated weights; legal review blocking |

Details: `socrf/FREELLMAPI-VERIFICATION.md`, `socrf/ORNITH-VERIFICATION.md`,
`socrf/LTX-VERIFICATION.md`. All three now have dry-run adapters under
`socrf/adapters/` with dedicated tests; none can execute.

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
