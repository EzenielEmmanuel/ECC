"""SOCRF LTX dry-run adapter: planning only, no weights, no GPU work, no execution.

Upstream facts verified on 2026-10-11 from https://github.com/Lightricks/LTX-2:
the code and the LTX-2.5 weights are distributed under the LTX Community
License Agreement (a custom, non-OSI license), the weights are gated on Hugging
Face behind accepted model terms, the standard component set is roughly 66 GiB,
and generation needs a CUDA GPU. LTX-2.3 and earlier sit under a separate
license file, so the exact version must be pinned before any live use.
"""
from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any

ADAPTER = "ltx"
UPSTREAM_REPO = "https://github.com/Lightricks/LTX-2"
WEIGHTS_REPO = "https://huggingface.co/Lightricks/LTX-2.5"
LICENSE = "LTX Community License Agreement (custom, non-OSI)"
LICENSE_SOURCE = "https://github.com/Lightricks/LTX-2/blob/main/LICENSE"

RUNTIME_REQUIREMENTS = {
    "python": ">=3.11",
    "torch": "2.13+cu132",
    "package_manager": "uv",
    "extra": "uv sync --extra natten (Linux + CUDA only; Triton or eager fallback elsewhere)",
}
INSTALL_METHODS = (
    "uv sync --extra natten from a clone of the upstream repository",
    "Hugging Face CLI download of the per-component safetensors files behind accepted model terms",
)
WEIGHTS_FACTS = {
    "approximate_size_gib": 66,
    "gated": True,
    "components": [
        "diffusion_models/ltx-2.5-22b-distilled-transformer-bf16.safetensors",
        "text_encoders/gemma4-12b-with-proj-ltx-2.5-bf16.safetensors",
        "vae/ltx-2.5-video-vae-bf16.safetensors",
        "vae/ltx-2.5-audio-vae-bf16.safetensors",
        "latent_upscale_models/ltx-2.5-latent-spatial-upscaler-x2-bf16-1.0.safetensors",
    ],
}

ALLOWED_ACTIONS = frozenset({"generate_video", "estimate_render"})
SUPPORTED_RESOLUTIONS = frozenset({"1024x1536", "3840x2176"})
DEFAULT_RESOLUTION = "1024x1536"
DEFAULT_FPS = 24
PROMPT_MAX_WORDS = 200
MAX_PROMPT_CHARS = 4000
# SOCRF policy cap, not an upstream limit.
MAX_CLIP_SECONDS = 60.0


@dataclass(frozen=True)
class LTXRequest:
    action: str
    prompt: str = ""
    seconds: float = 5.0
    resolution: str = DEFAULT_RESOLUTION


def plan_ltx_request(request: LTXRequest, *, config: Mapping[str, Any] | None = None) -> dict[str, Any]:
    """Validate and return a non-executing proposal for a future LTX integration."""
    if request.action not in ALLOWED_ACTIONS:
        raise ValueError("Unsupported LTX action")
    if request.resolution not in SUPPORTED_RESOLUTIONS:
        raise ValueError("Unsupported resolution")
    if isinstance(request.seconds, bool) or not isinstance(request.seconds, (int, float)):
        raise TypeError("Seconds must be a number")
    if not 0 < float(request.seconds) <= MAX_CLIP_SECONDS:
        raise ValueError("Clip length outside SOCRF policy range")
    if request.action == "generate_video":
        if not isinstance(request.prompt, str) or not request.prompt.strip():
            raise ValueError("Prompt must be non-empty")
        if len(request.prompt) > MAX_PROMPT_CHARS:
            raise ValueError("Prompt exceeds maximum length")
        if len(request.prompt.split()) > PROMPT_MAX_WORDS:
            raise ValueError("Prompt exceeds the upstream word guidance")
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
        "prompt_words": len(request.prompt.split()),
        "resolution": request.resolution,
        "estimated_frames": int(round(float(request.seconds) * DEFAULT_FPS)),
        "license": LICENSE,
        "license_review_required": True,
        "weights": WEIGHTS_FACTS,
        "executed": False,
        "approved": False,
        "requires": [
            "license_legal_review",
            "huggingface_terms_acceptance",
            "gpu_host_provisioning",
            "cost_budget",
            "approval_gate",
            "audit_logging",
        ],
    }
