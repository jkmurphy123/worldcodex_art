from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime
import os
from pathlib import Path
from typing import Any
from urllib.request import Request, urlopen

import typer

from .base import ImageProvider, ProviderCapabilities, ImageRequest, ImageResult

FAL_MODEL = "fal-ai/flux/schnell"
FAL_ENDPOINT = f"https://fal.run/{FAL_MODEL}"
FAL_KEY_ENV = "FAL_KEY"


def _parse_size(size: str) -> dict[str, int] | str:
    try:
        width_str, height_str = size.lower().split("x", 1)
        width = int(width_str)
        height = int(height_str)
        return {"width": width, "height": height}
    except Exception:
        return size


def _extract_urls(payload: str) -> list[str]:
    try:
        data: Any = json.loads(payload)
    except json.JSONDecodeError:
        data = payload.strip()

    urls: list[str] = []

    def add_url(value: Any) -> None:
        if isinstance(value, str) and value.startswith("http"):
            urls.append(value)

    if isinstance(data, dict):
        if "images" in data:
            images = data["images"]
            if isinstance(images, list):
                for item in images:
                    if isinstance(item, dict):
                        add_url(item.get("url"))
                    else:
                        add_url(item)
        if "url" in data:
            add_url(data["url"])
        if "image" in data:
            image = data["image"]
            if isinstance(image, dict):
                add_url(image.get("url"))
            else:
                add_url(image)
    elif isinstance(data, list):
        for item in data:
            if isinstance(item, dict):
                add_url(item.get("url"))
            else:
                add_url(item)
    elif isinstance(data, str):
        add_url(data)

    return urls


@dataclass
class FalAIImageProvider:
    name: str = "fal_ai"
    capabilities: ProviderCapabilities = ProviderCapabilities(
        supports_seed=False,
        supports_variations=False,
        supports_multiple_images=True,
        supports_sizes=True,
    )

    def generate(self, req: ImageRequest, out_dir: Path) -> ImageResult:
        api_key = os.getenv(FAL_KEY_ENV)
        if not api_key:
            raise typer.BadParameter(
                f"{FAL_KEY_ENV} is not set. Set it to your fal.ai API key."
            )

        payload: dict[str, Any] = {
            "prompt": req.prompt,
            "image_size": _parse_size(req.size),
            "num_images": req.n,
        }
        if req.negative:
            payload["negative_prompt"] = req.negative

        body = json.dumps(payload).encode("utf-8")
        request = Request(
            FAL_ENDPOINT,
            data=body,
            headers={
                "Authorization": f"Key {api_key}",
                "Content-Type": "application/json",
            },
            method="POST",
        )

        try:
            with urlopen(request) as response:  # nosec - endpoint is trusted
                raw = response.read().decode("utf-8", errors="ignore")
        except Exception as exc:  # pragma: no cover - HTTP errors vary
            raise typer.BadParameter(f"fal.ai image generation failed: {exc}") from exc

        urls = _extract_urls(raw)
        if not urls:
            raise typer.BadParameter("fal.ai response did not include image URLs.")

        out_dir.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        paths: list[Path] = []

        for idx, url in enumerate(urls, start=1):
            try:
                with urlopen(url) as handle:  # nosec - URL comes from fal.ai
                    image_bytes = handle.read()
            except Exception as exc:  # pragma: no cover - HTTP errors vary
                raise typer.BadParameter(f"fal.ai image download failed: {exc}") from exc
            path = out_dir / f"fal_ai_{timestamp}_{idx}.png"
            path.write_bytes(image_bytes)
            paths.append(path)

        return ImageResult(
            images=paths,
            provider=self.name,
            model=FAL_MODEL,
            request_id=None,
            metadata={},
        )
