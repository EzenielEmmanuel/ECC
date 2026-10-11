# Octop upstream verification and SOCRF integration gates

Verified by reading the upstream GitHub repository `TencentCloud/Octop` README and LICENSE on 2026-10-11.

## Confirmed upstream facts
- Repository: https://github.com/TencentCloud/Octop
- MIT license (LICENSE file inspected; preserve copyright/license notice if copying code).
- README describes a self-hosted Python 3.12+ multi-user, multi-agent assistant.
- README documents HTTP/SSE/WebSocket programmatic interfaces, ACP inbound/outbound, expert sharing, multi-agent coordination, workspace backends and optional Docker sandbox.
- Upstream components include Octop Harness, Gateway, Memory and Browser.

## Not yet verified
- Exact authenticated API endpoints and request/response schemas for task delegation.
- Whether the relevant endpoint is enabled by default, how permissions apply to it, and whether a low-privilege service account is supported.
- Current security posture and practical cloud RAM/CPU cost.
- Any deployment or live API connection from SOCRF.

## Integration plan
1. Run `python -m unittest discover -s socrf/tests -v` from the SOCRF repository root (tests are committed but not yet executed in a runtime).
2. Inspect Octop API route definitions and auth middleware upstream before writing an HTTP adapter; never guess an endpoint.
3. Set up a dedicated cloud sandbox with isolated credentials and disabled terminal/browser tools initially.
4. Add explicit auth, timeouts, output validation, approval, audit logging, cost limits and rollback.
5. Enable live execution only after contract tests and security review.

The existing `socrf/adapters/octop_dry_run.py` is an offline planning stub, not an Octop client. No secrets or remote calls are involved.
