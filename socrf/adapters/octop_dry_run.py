"""SOCRF Octop adapter: safe dry-run planning only.

This module intentionally makes no network requests, launches no processes,
and reads no credentials. Live execution requires a separately reviewed adapter.
"""
from dataclasses import dataclass
from typing import Any, Mapping

ALLOWED_ACTIONS = frozenset({"delegate_task", "check_status"})

@dataclass(frozen=True)
class OctopRequest:
    action: str
    task: str
    approved: bool = False

def plan_octop_request(request: OctopRequest, *, config: Mapping[str, Any] | None = None) -> dict[str, Any]:
    """Validate and return a non-executing proposal for a future Octop integration."""
    if request.action not in ALLOWED_ACTIONS:
        raise ValueError("Unsupported Octop action")
    if not isinstance(request.task, str) or not request.task.strip():
        raise ValueError("Task must be non-empty")
    if len(request.task) > 4000:
        raise ValueError("Task exceeds maximum length")
    config = config or {}
    # Fail closed even when an external caller supplies approval.
    if config.get("execution_enabled", False):
        raise PermissionError("Live execution is not implemented; fail closed")
    return {
        "adapter": "octop",
        "mode": "dry_run",
        "action": request.action,
        "task": request.task.strip(),
        "approved": bool(request.approved),
        "executed": False,
        "requires": ["verified_octop_api", "isolated_runtime", "credential_vault", "approval_gate", "audit_logging"],
    }
