"""SOCRF Ornith dry-run adapter: planning only, no network, no weights, no execution.

Upstream facts verified on 2026-10-11 from https://github.com/ornith-ai/Ornith-1
and https://huggingface.co/ornith-ai/Ornith-1.5-9B: the repository is MIT
licensed documentation only and ships no code; the Ornith-1.5-9B checkpoint is
MIT licensed, roughly 19 GB in bf16, and serves an OpenAI-compatible endpoint
through vLLM or SGLang. Weight downloads and live serving are deliberately out
of scope for this adapter.
"""
from collections.abc import Mapping
from dataclasses import dataclass, field
from typing import Any

ADAPTER = "ornith"
UPSTREAM_REPO = "https://github.com/ornith-ai/Ornith-1"
CHECKPOINT = "ornith-ai/Ornith-1.5-9B"
CHECKPOINT_URL = "https://huggingface.co/ornith-ai/Ornith-1.5-9B"
LICENSE = "MIT"

RUNTIME_REQUIREMENTS = {
    "transformers": ">=5.8.1",
    "vllm": ">=0.19.1",
    "sglang": ">=0.5.9",
}
CHECKPOINT_FACTS = {
    "params": "10B",
    "format": "safetensors bf16",
    "approximate_size_gib": 19,
    "context_tokens": 262144,
    "serving": "OpenAI-compatible /v1 via vLLM or SGLang",
    "hardware": "single 80 GB GPU for the dense 9B checkpoint",
}

ALLOWED_ACTIONS = frozenset({"evaluate_workflow", "compare_strategies"})
MAX_TASK_CHARS = 4000
MAX_STRATEGIES = 8


@dataclass(frozen=True)
class OrnithRequest:
    action: str
    task: str
    strategies: tuple[str, ...] = field(default=())


def plan_ornith_request(
    request: OrnithRequest, *, config: Mapping[str, Any] | None = None
) -> dict[str, Any]:
    """Validate and return a non-executing proposal for a future Ornith integration."""
    if request.action not in ALLOWED_ACTIONS:
        raise ValueError("Unsupported Ornith action")
    if not isinstance(request.task, str) or not request.task.strip():
        raise ValueError("Task must be non-empty")
    if len(request.task) > MAX_TASK_CHARS:
        raise ValueError("Task exceeds maximum length")
    if not isinstance(request.strategies, tuple):
        raise TypeError("Strategies must be a tuple of strings")
    if any(not isinstance(item, str) or not item.strip() for item in request.strategies):
        raise ValueError("Each strategy must be a non-empty string")
    if request.action == "compare_strategies" and len(request.strategies) < 2:
        raise ValueError("compare_strategies requires at least two strategies")
    if len(request.strategies) > MAX_STRATEGIES:
        raise ValueError("Too many strategies")
    config = config or {}
    # Fail closed even when an external caller supplies approval.
    if config.get("execution_enabled", False):
        raise PermissionError("Live execution is not implemented; fail closed")
    if config.get("download_weights", False):
        raise PermissionError("Weight downloads are not implemented; run a separate reviewed provisioning step")
    return {
        "adapter": ADAPTER,
        "mode": "dry_run",
        "action": request.action,
        "task": request.task.strip(),
        "strategies": list(request.strategies),
        "checkpoint": CHECKPOINT,
        "checkpoint_url": CHECKPOINT_URL,
        "license": LICENSE,
        "executed": False,
        "approved": False,
        "requires": [
            "gpu_host_provisioning",
            "weights_download_approval",
            "runtime_pinning",
            "approval_gate",
            "audit_logging",
        ],
    }
