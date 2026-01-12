from __future__ import annotations

import base64
from dataclasses import dataclass
from datetime import datetime
import os
from pathlib import Path
from urllib.request import urlopen

import typer
from openai import OpenAI

from .base import ImageProvider, ProviderCapabilities, ImageRequest, ImageResult

MODEL_NAME = "gpt-image-1"


def _merge_prompt(prompt: str, negative: str | None) -> str:
    if not negative:
        return prompt
    return f"Avoid: {negative}\n\n{prompt}"


@dataclass
class OpenAIImageProvider:
    name: str = "openai"
    capabilities: ProviderCapabilities = ProviderCapabilities(
        supports_seed=False,
        supports_variations=False,
        supports_multiple_images=True,
        supports_sizes=True,
    )

    def generate(self, req: ImageRequest, out_dir: Path) -> ImageResult:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise typer.BadParameter(
                "OPENAI_API_KEY is not set. Set it to your OpenAI API key."
            )

        prompt = _merge_prompt(req.prompt, req.negative)
        client = OpenAI(api_key=api_key)

        try:
            response = client.images.generate(
                model=MODEL_NAME,
                prompt=prompt,
                size=req.size,
                n=req.n,
            )
        except Exception as exc:  # pragma: no cover - OpenAI SDK exceptions vary
            raise typer.BadParameter(f"OpenAI image generation failed: {exc}") from exc

        out_dir.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        paths: list[Path] = []

        for idx, item in enumerate(response.data, start=1):
            if item.b64_json:
                image_bytes = base64.b64decode(item.b64_json)
            elif item.url:
                with urlopen(item.url) as handle:  # nosec - URL comes from OpenAI response
                    image_bytes = handle.read()
            else:
                raise typer.BadParameter("OpenAI response missing image data.")
            path = out_dir / f"openai_{timestamp}_{idx}.png"
            path.write_bytes(image_bytes)
            paths.append(path)

        return ImageResult(
            images=paths,
            provider=self.name,
            model=MODEL_NAME,
            request_id=getattr(response, "id", None),
            metadata={},
        )
