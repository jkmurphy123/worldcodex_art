from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Protocol


@dataclass(frozen=True)
class ProviderCapabilities:
    supports_seed: bool = False
    supports_variations: bool = False
    supports_multiple_images: bool = True
    supports_sizes: bool = True


@dataclass(frozen=True)
class ImageRequest:
    prompt: str
    negative: str | None
    size: str
    n: int = 1
    seed: int | None = None
    style_profile: str | None = None
    image_style: str | None = None
    render_intent: str | None = None
    extra: dict[str, Any] | None = None  # provider-specific escape hatch


@dataclass(frozen=True)
class ImageResult:
    images: list[Path]
    provider: str
    model: str | None
    request_id: str | None = None
    metadata: dict[str, Any] | None = None


class ImageProvider(Protocol):
    name: str
    capabilities: ProviderCapabilities

    def generate(self, req: ImageRequest, out_dir: Path) -> ImageResult:
        ...
