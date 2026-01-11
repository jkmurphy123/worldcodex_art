from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .registry import STYLE_PROFILES


@dataclass(frozen=True)
class PromptPackage:
    prompt: str
    negative: str | None
    size: str
    style_profile: str
    render_intent: str
    debug: dict[str, Any]


def build_prompt(
    world_text: str,
    subject: str,
    *,
    style_profile: str,
    render_intent: str,
    size: str,
    palette: str | None = None,
    negative: str | None = None,
) -> PromptPackage:
    sp = STYLE_PROFILES.get(style_profile)
    if not sp:
        raise ValueError(f"Unknown style_profile: {style_profile}")

    # Keep world context bounded: later you can summarize/cache.
    world_excerpt = world_text.strip()
    if len(world_excerpt) > 4000:
        world_excerpt = world_excerpt[:4000] + "\n[...truncated...]"

    parts: list[str] = []
    parts.append("WORLD CONTEXT (authoritative):")
    parts.append(world_excerpt)
    parts.append("")
    parts.append("STYLE DIRECTIVE:")
    parts.append(sp.prompt)
    if palette:
        parts.append(f"Palette emphasis: {palette}")
    parts.append(f"Render intent: {render_intent}")
    parts.append("")
    parts.append("SUBJECT TO DEPICT:")
    parts.append(subject.strip())

    merged_negative = negative or sp.negative

    return PromptPackage(
        prompt="\n".join(parts).strip(),
        negative=merged_negative,
        size=size,
        style_profile=style_profile,
        render_intent=render_intent,
        debug={
            "world_excerpt_chars": len(world_excerpt),
            "style_profile": style_profile,
            "render_intent": render_intent,
            "size": size,
            "palette": palette,
        },
    )
