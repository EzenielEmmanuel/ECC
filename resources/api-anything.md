# API Anything — Resource Assessment

- Reviewed: 2026-10-20
- Repository: https://github.com/goodnight000/api-anything
- License: MIT, copyright 2026 Tianjun Zheng. Forking, modification and commercial reuse are permitted; retain copyright and license notices.
- Package inspected: 0.1.0; Node.js >=22.13.0; TypeScript project.
- Status: Documentation review; not forked, installed or runtime-tested.
- Priority: Promising evaluation candidate for ORIS/SOCRF (assessment).

## What it does
Learns reusable operations from website network traffic, then exposes calls through MCP, CLI or a TypeScript library. HTTP requests can replace repeated browser navigation; browser fallbacks and operation repair are documented.

## Limits
Self-hosted tool, not a free hosted API or model. Only learned operations work; repairs can fail. Chrome may be required. CAPTCHA challenges require manual handling. Credentials use a local store. Writes require explicit enablement; bundled operations are read-only. Upstream performance figures are author-reported and unverified here.

## Proposed ORIS use
Evaluate as an optional website connector for repeated permitted lookups. Potentially reduces browsing overhead; actual savings and cloud compatibility require testing. Prefer official APIs where suitable.

## Evaluation plan
Pin a commit, inspect code and dependencies, then test one public read-only operation with unseen inputs. Measure correctness, latency and token use. Check session isolation, site terms, secret handling and browser resource needs before cloud integration.

## Sources
- https://github.com/goodnight000/api-anything
- https://github.com/goodnight000/api-anything/blob/main/LICENSE
- https://github.com/goodnight000/api-anything/blob/main/package.json
