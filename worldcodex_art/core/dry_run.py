from __future__ import annotations

from pathlib import Path

from worldcodex_art.providers.base import ImageRequest


def format_dry_run_output(
    req: ImageRequest,
    *,
    provider_name: str,
    model: str | None,
    out_dir: Path,
) -> list[str]:
    lines = [
        "dry_run: true",
        f"provider: {provider_name}",
        f"model: {model}",
        f"out_dir: {out_dir}",
        f"size: {req.size}",
        f"n: {req.n}",
        f"seed: {req.seed}",
        f"style_profile: {req.style_profile}",
        f"image_style: {req.image_style}",
        f"render_intent: {req.render_intent}",
        "prompt:",
        req.prompt,
        "negative:",
        req.negative or "",
        f"extra: {req.extra}",
    ]
    return lines
