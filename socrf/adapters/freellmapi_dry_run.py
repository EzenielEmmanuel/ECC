"""SOCRF FreeLLMAPI dry-run adapter: planning only, no network or execution.

Upstream facts verified on 2026-10-11 from the GitHub README, LICENSE and
package.json of https://github.com/tashfeenahmed/freellmapi: MIT licensed code,
Node >=20.18.0 <25.0.0, self-hosted OpenAI-compatible /v1 router that
aggregates free provider tiers. Provider keys stay in a credential vault and
are never passed through this module or stored in the repository.
"""
from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any

ADAPTER = "freellmapi"
UPSTREAM = "https://github.com/tashfeenahmed/freellmapi"
LICENSE = "MIT"
LICENSE_SOURCE = "https://github.com/tashfeenahmed/freellmapi/blob/main/LICENSE"
USAGE_NOTE = (
    "Upstream describes the project as personal experimentation only; "
    "commercial use inside SOCRF products needs a separate usage review."
)
SOURCE_REGISTRY = "https://github.com/EzenielEmmanuel/ORIS-Workshop"

RUNTIME_REQUIREMENTS = {
    "node": ">=20.18.0 <25.0.0",
    "npm": ">=10.0.0",
    "optional": {"docker": "any current stable release"},
}
INSTALL_METHODS = (
    "self-hosted Docker or docker-compose (upstream one-line installer requires Docker)",
    "npm local development across the shared, server, client and cli workspaces",
    "upstream desktop release binaries for macOS and Windows",
)
COST_MODEL = "upstream free provider tiers; self-hosted on any Node 20+ host"

ALLOWED_ACTIONS = frozenset({"route_model", "list_models"})
MAX_MODEL_CHARS = 200
MAX_PROMPT_CHARS = 20000
MAX_TOKENS_LIMIT = 8192


@dataclass(frozen=True)
class FreeLLMAPIRequest:
    action: str
    model: str
    payload: dict[str, Any]


def plan_freellmapi_request(
    request: FreeLLMAPIRequest, *, config: Mapping[str, Any] | None = None
) -> dict[str, Any]:
    """Validate and return a non-executing proposal for a FreeLLMAPI integration."""
    if request.action not in ALLOWED_ACTIONS:
        raise ValueError("Unsupported FreeLLMAPI action")
    if not isinstance(request.model, str) or not request.model.strip():
        raise ValueError("Model must be a non-empty string")
    if len(request.model) > MAX_MODEL_CHARS:
        raise ValueError("Model identifier exceeds maximum length")
    if not isinstance(request.payload, dict):
        raise TypeError("Payload must be a dictionary")
    prompt = request.payload.get("prompt", "")
    if not isinstance(prompt, str):
        raise TypeError("Payload prompt must be a string")
    if len(prompt) > MAX_PROMPT_CHARS:
        raise ValueError("Prompt exceeds limit")
    max_tokens = request.payload.get("max_tokens", 1024)
    if isinstance(max_tokens, bool) or not isinstance(max_tokens, int):
        raise TypeError("max_tokens must be an integer")
    if not 1 <= max_tokens <= MAX_TOKENS_LIMIT:
        raise ValueError("max_tokens outside permitted range")
    config = config or {}
    # Fail closed even when an external caller supplies approval.
    if config.get("execution_enabled", False):
        raise PermissionError("Live execution is not implemented; fail closed")
    if config.get("provider_key") is not None:
        raise PermissionError("Provider keys must come from a credential vault, never a call argument")
    return {
        "adapter": ADAPTER,
        "mode": "dry_run",
        "action": request.action,
        "model": request.model.strip(),
        "upstream": UPSTREAM,
        "license": LICENSE,
        "usage_review_required": True,
        "cost_model": COST_MODEL,
        "executed": False,
        "approved": False,
        "requires": [
            "usage_terms_review",
            "credential_vault",
            "quota_budget_per_provider",
            "approval_gate",
            "audit_logging",
        ],
        "payload_keys": sorted(str(k) for k in request.payload),
    }
