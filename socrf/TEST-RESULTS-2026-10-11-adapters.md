# Resource integration test results

Date: 2026-10-11
Branch: `socrf/resource-integration` (based on `socrf-development`)

Command: `python3 -m unittest discover -s socrf/tests -v`

**Result: 46 tests passed; 0 failures; 0 errors.**

Breakdown:
- `test_octop_dry_run.py` — 5 tests (pre-existing)
- `test_resource_planner.py` — 6 tests (pre-existing)
- `test_freellmapi_dry_run.py` — 12 tests (new)
- `test_ornith_dry_run.py` — 10 tests (new)
- `test_ltx_dry_run.py` — 13 tests (new)

What the new tests validate: dry-run planning only, `executed` and `approved`
always false, fail-closed rejection of live execution and of provider keys or
weight downloads passed in through config, input validation for actions,
models, prompts, strategies, resolutions and clip lengths, and that the
verified license and runtime facts are recorded on every plan.

Scope: isolated local copy of committed files, Python 3.10.12. **Not** a
GitHub Actions run, not an ECC full-suite run, not an install of any upstream
project, not a model download, not a GPU provisioning, not a security audit.

## Limitations
- CI runs Python 3.12; local verification used 3.10.12. The adapters use only
  3.10-compatible syntax, so no discrepancy is expected, but CI should confirm.
- No coverage measurement is available in this environment (`coverage` is not
  installed). Every public function in the three new adapters is exercised by
  at least one test, including each rejection branch.
- FreeLLMAPI's own dependency tree has not been audited; nothing upstream was
  installed.
- All license, runtime, hardware and size facts are read from upstream
  documentation on 2026-10-11 and can drift.

## Recommended next steps (before any live execution)
1. Legal review of the LTX Community License Agreement and of FreeLLMAPI's
   personal-experimentation usage note.
2. Usage review of the free-tier provider terms behind FreeLLMAPI.
3. Resolve the `deepreinforce-ai` vs `ornith-ai` checkpoint namespace
   discrepancy in the upstream Ornith documentation.
4. Provision an isolated, least-privilege cloud sandbox; decide between FreeLLMAPI
   self-hosted (free, Node) and hosted GPU options for Ornith and LTX.
5. Only then write reviewed live adapters with timeouts, budgets, approval
   gates and audit logging, and re-run these tests plus new contract tests.
