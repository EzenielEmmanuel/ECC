"""Offline integration planner for registered SOCRF resources; no network or execution."""
from dataclasses import dataclass
from typing import Any

CAPABILITIES = {
    "freellmapi": frozenset({"route_model", "list_models"}),
    "ornith": frozenset({"evaluate_workflow", "compare_strategies"}),
    "ltx-2": frozenset({"generate_video", "estimate_render"}),
}

@dataclass(frozen=True)
class ResourceRequest:
    resource_id: str
    action: str
    payload: dict[str, Any]

def plan_resource_request(request: ResourceRequest) -> dict[str, Any]:
    if request.resource_id not in CAPABILITIES:
        raise ValueError("Unknown resource")
    if request.action not in CAPABILITIES[request.resource_id]:
        raise ValueError("Unsupported action")
    if not isinstance(request.payload, dict):
        raise TypeError("Payload must be a dictionary")
    if len(str(request.payload)) > 4000:
        raise ValueError("Payload exceeds limit")
    return {
        "resource_id": request.resource_id,
        "action": request.action,
        "mode": "dry_run",
        "executed": False,
        "approved": False,
        "required_checks": ["license", "auth", "cost", "sandbox", "human_approval"],
        "payload_keys": sorted(str(k) for k in request.payload),
    }
