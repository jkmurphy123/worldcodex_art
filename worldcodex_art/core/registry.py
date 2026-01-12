from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from worldcodex_art.providers.mock_provider import MockProvider
from worldcodex_art.providers.fal_ai_provider import FalAIImageProvider
from worldcodex_art.providers.openai_provider import OpenAIImageProvider

ProviderFactory = Callable[[], object]


@dataclass(frozen=True)
class StyleProfile:
    name: str
    prompt: str
    negative: str | None = None


PROVIDERS: dict[str, ProviderFactory] = {
    "mock": lambda: MockProvider(),
    "fal_ai": lambda: FalAIImageProvider(),
    "openai": lambda: OpenAIImageProvider(),
}

STYLE_PROFILES: dict[str, StyleProfile] = {
    "industrial_amber": StyleProfile(
        name="industrial_amber",
        prompt=(
            "Industrial sci-fi interior, amber maintenance lighting, "
            "clean but worn surfaces, subtle frost/condensation, "
            "utilitarian signage, realistic materials, high detail"
        ),
        negative="text, watermark, logo",
    ),
    "blueprint": StyleProfile(
        name="blueprint",
        prompt="Technical blueprint / schematic aesthetic, clean lines, labeled shapes (no readable text)",
        negative="photorealism, clutter, watermark, logo",
    ),
}
