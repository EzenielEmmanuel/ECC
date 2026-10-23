# FreeLLMAPI connection plan (Phase 1 — preparation, no live execution)

Prepared 2026-10-11 on branch `socrf/freellmapi-connection` (based on `socrf/resource-integration`).

**Status: awaiting approval. No service has been installed, started, or called. No
provider account has been created and no credential has been obtained.**

## 1. Upstream inspection findings

Source: https://github.com/tashfeenahmed/freellmapi README, `docs/en/install/01-install.md`,
`docs/en/api/01-rest-api.md`, `docs/en/architecture/00-high-level-index.md` (read 2026-10-11).

**Installation**
- Three install paths: a one-line installer that requires Docker, `docker compose`, or npm local development.
- Server requires **Node >= 20.18.0 < 25.0.0** and **npm >= 10.0.0**; the production image is multi-arch (`linux/amd64` + `linux/arm64`).
- `ENCRYPTION_KEY` is mandatory for startup when provider keys are real; provider keys are stored AES-256-GCM encrypted in SQLite and decrypted in memory per request.
- Declarative startup config (`FREEAPI_CONFIG_PATH` / `FREEAPI_CONFIG_JSON`) can provision admin, model and fallback rows on boot, but that file **carries plaintext secrets** and must be treated exactly like `ENCRYPTION_KEY`.
- By default the container binds **`127.0.0.1` only**; exposing it requires `HOST_BIND=0.0.0.0`, which upstream itself warns against outside a trusted LAN.

**Endpoints used by SOCRF**
| Endpoint | Purpose |
|---|---|
| `GET /v1/models` (`?available=true`, `?execution_status=ready`) | Model discovery |
| `POST /v1/chat/completions` | Inference |
| `X-Routed-Via`, `X-Fallback-Attempts`, `X-Fallback-Trail` headers | Which provider served the call, failover trail |
| `GET /api/free-tier` (dashboard session) | Pooled monthly free-tier budget |
| `PATCH /api/keys/:id` | Per-key `monthlyRequestCap` / `monthlyTokenCap` |
| `GET /v1/docs`, `GET /v1/openapi.json` | Interactive API documentation |

Routing: `auto` follows the active fallback chain; `auto:fast`, `auto:cheap`, `auto:smart`,
`auto:reliable`, `auto:balanced` steer a single request; `auto:<profile>` uses a named chain.
`fusion` is a virtual multi-model panel + judge route.

**Documented restrictions (upstream, verbatim intent)**
- "Personal experimentation only" in the repository description — a commercial-use review is required before this gateway touches a product.
- "Local-first. There's no multi-tenant auth. Run this for yourself; don't expose it to the internet."
- Latest model catalog is a paid Premium feature ($19/yr). Free installs receive the monthly snapshot, so new models appear up to 30 days later.
- No `/v1/moderations`, no `n > 1`, no per-user billing. Upstream's own limitations section warns that effective model quality degrades during the day as daily caps are consumed, and that free tiers change without notice.
- Upstream re-reviewed provider ToS in May 2026 — see section 3.

## 2. Can a Kilo Cloud Agent run an isolated instance?

**Yes, with documented caveats.** Kilo Cloud Agent provides an isolated Linux container
(Node.js, git, gh/glab CLI) with secrets encrypted at rest and injected as environment
variables. Caveats found in the Kilo documentation:

| Factor | Finding | Impact |
|---|---|---|
| Language runtime | Node.js is preinstalled; **Python is not in the base image**, `apt` is available | FreeLLMAPI (Node) runs directly; our Python test client needs `apt install python3` in a setup command |
| Node version | Documented as preinstalled, version unspecified | Must verify `node --version` satisfies `>=20.18.0 <25.0.0` before install |
| Docker | The `docker compose` path needs a Docker daemon, which is not confirmed in the base container; a "Docker" Cloud Agent size exists at the same $0.60/hr rate | Prefer the **npm local development** path, or confirm Docker availability first |
| Container sharing | **All Cloud Agent chats share a single container instance**; each worktree gets its own checkout directory | A gateway bound to `127.0.0.1` is not public, but is reachable from other chats in the same container — acceptable only because those are our own sessions; still worth a distinct worktree |
| Ephemerality | Containers spindown when idle; sessions are deleted after 7 days (beta) | The SQLite DB and `.env` do not survive; provider keys must be re-injected from the vault each session, never stored in the repo |
| Message limit | Each message can run up to 15 minutes | Start the gateway as a background process from a startup command, not inside a single message |
| Triggers | Personal triggers execute in the same sandbox container as Cloud Agent sessions | An automated restart path exists, but it is beta; not proposed yet |

**Conclusion:** the npm local-development path on a Kilo Cloud Agent (Small or Docker size,
$0.60/hr) is a safe, low-cost, non-public host for a first connection. The Cloud Agent
environment variables/secrets feature keeps every credential outside the repository.

## 3. Compatible free-tier providers

Upstream's May 2026 provider ToS review, mapped to SOCRF's proposed use (single-user,
internal development, no resale, no public exposure):

| Provider | Upstream verdict | Proposed SOCRF use |
|---|---|---|
| Groq | Likely OK | **Primary candidate** for inference tests |
| Cerebras | Likely OK | **Primary candidate** — fast, low-latency |
| Mistral | Likely OK | Secondary |
| OpenRouter | Likely OK | Secondary (many `:free` routes) |
| OVH AI Endpoints | Likely OK | Optional; anonymous 2 req/min per IP |
| AI Horde | Likely OK | Optional community-run commons |
| Ollama Cloud | Likely OK | Optional; 1 concurrent, 5-hour session caps |
| Google Gemini | Caution | Avoid until reviewed (March 2026 ToS narrows to business purposes) |
| Cloudflare Workers AI | Ambiguous | Avoid until reviewed |
| NVIDIA NIM | Caution | Avoid — trial ToS is evaluation-only |
| GitHub Models | Caution | Avoid — experimentation/prototyping scope |
| Z.ai | Caution | Avoid — anti-traffic-redirect clause |
| Cohere | **Avoid** | Excluded — terms forbid personal/household purposes |

Recommended first pair: **Groq + Cerebras**, both rated "likely OK" upstream, with OpenRouter
as a third key for failover breadth. No accounts have been created.

## 4. Secure connection design

Credentials stay out of the repository at every layer:

| Setting | Source | Notes |
|---|---|---|
| `SOCRF_FREELLMAPI_BASE_URL` | Environment / Cloud Agent env var | Defaults to `http://127.0.0.1:3001/v1` |
| `SOCRF_FREELLMAPI_TOKEN` | Environment / Cloud Agent **encrypted secret** | The gateway's unified `freellmapi-…` token |
| `SOCRF_FREELLMAPI_ARMED` | Environment | `false` by default; must be explicitly enabled to obtain a network transport |
| `SOCRF_FREELLMAPI_ALLOW_REMOTE` | Environment | `false` by default; a non-loopback base URL is refused unless this is set, and must then be `https` |

Code already staged (inert, no network): `socrf/adapters/freellmapi_client.py`
- Transport is **injected**. The default client has no transport and raises `FreeLLMAPIDisabledError`.
- `http_transport()` refuses to build a real transport unless `armed=True`.
- Loopback-only by default; non-loopback requires explicit override and HTTPS.
- Tokens are redacted from every error message; 30s timeout; up to 3 attempts with exponential backoff on 408/425/429/5xx only; 401/403 and 4xx fail fast; response bodies non-JSON or missing `choices` are rejected rather than guessed.
- Usage is captured as a `Usage` record (model, provider, prompt/completion tokens) so Phase 2 can report cost per request.
- 28 unit tests cover all of the above with a fake transport — 74 SOCRF tests pass in total.

## 5. Licensing considerations

| Component | License | Impact |
|---|---|---|
| FreeLLMAPI code | MIT | Permissive; preserve the copyright notice if any code is copied. SOCRF registers an adapter, it does not vendor the codebase. |
| FreeLLMAPI usage scope | "Personal experimentation only" (repository description) | **Blocking for product use.** Requires usage/legal review before SOCRF products depend on it. Internal-only development and testing is the intended scope for Phase 2. |
| Premium live catalog | Paid subscription ($19/yr) | Optional; the free monthly snapshot is sufficient for Phase 2. |
| Provider terms | Per section 3 | Free tiers are per-provider; Cohere excluded, several "caution" rows avoided. |
| Kilo Cloud Agent compute | Kilo credits, $0.60/hr (Small/Docker) | Billed per second; separate from model inference. Requires a $5 balance to launch (not a minimum spend). |

## 6. Expected costs

| Item | Cost |
|---|---|
| FreeLLMAPI gateway (MIT, self-hosted) | $0 |
| Free-tier provider inference (Groq/Cerebras free tiers) | $0 within caps |
| Kilo Cloud Agent compute (Small, $0.60/hr) | ~$0.01/min; a 1-hour test session ≈ $0.60 |
| Kilo model inference for agent reasoning | Separate credit spend, unchanged from current usage |
| Premium live catalog | $0 (skipped) |
| Ornith / LTX-2 GPU work | Not in scope for this phase |

## 7. Phase 2 test plan (only after approval)

1. Provision a Cloud Agent worktree from `socrf/freellmapi-connection`; inject `SOCRF_FREELLMAPI_TOKEN` as an encrypted secret, never into the repo.
2. Verify `node --version` satisfies `>=20.18.0 <25.0.0`; install FreeLLMAPI via npm local development; start it as a background process on `127.0.0.1:3001`.
3. Startup and health check; confirm the port is loopback-only.
4. `GET /v1/models?available=true` — model discovery.
5. One inference request with `auto:fast` on an approved provider; capture `X-Routed-Via`.
6. Error handling: invalid model, invalid token, forced timeout, restart and recovery.
7. Record token usage via the `Usage` records and the `GET /api/free-tier` budget; confirm $0 provider cost.
8. Document results in `socrf/TEST-RESULTS-2026-10-11-freellmapi.md` and commit to the branch.

## 8. Approval requested

Please approve Phase 2 as scoped above. Until then the client module stays inert, and I will not:

- install, start, or call FreeLLMAPI;
- create any provider account or request any credential;
- spend Kilo credits on Cloud Agent compute;
- expose any port beyond loopback;
- modify any file outside `socrf/` or touch `main`.

## 9. Limitations of this report

- All Kilo Cloud Agent facts are from kilo.ai documentation, not from a provisioned session; Docker availability in the base container and the preinstalled Node version are the two items that still need runtime confirmation.
- Provider ToS verdicts are upstream FreeLLMAPI's May 2026 review, not independent legal advice.
- The gateway's own behaviour under load, and actual free-tier quotas, are unverified.
