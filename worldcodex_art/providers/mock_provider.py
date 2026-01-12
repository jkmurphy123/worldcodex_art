from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import uuid

from .base import ImageProvider, ProviderCapabilities, ImageRequest, ImageResult


@dataclass
class MockProvider:
    name: str = "mock"
    capabilities: ProviderCapabilities = ProviderCapabilities(
        supports_seed=True,
        supports_variations=True,
        supports_multiple_images=True,
        supports_sizes=True,
    )

    def generate(self, req: ImageRequest, out_dir: Path) -> ImageResult:
        out_dir.mkdir(parents=True, exist_ok=True)
        paths: list[Path] = []
        for i in range(req.n):
            p = out_dir / f"mock_{uuid.uuid4().hex[:8]}_{i+1}.txt"
            p.write_text(
                "MOCK IMAGE\n\n"
                f"size: {req.size}\n"
                f"seed: {req.seed}\n"
                f"style: {req.style_profile}\n"
                f"image_style: {req.image_style}\n"
                f"intent: {req.render_intent}\n\n"
                f"prompt:\n{req.prompt}\n\n"
                f"negative:\n{req.negative}\n"
            )
            paths.append(p)

        return ImageResult(images=paths, provider=self.name, model=None, request_id=None, metadata={})
