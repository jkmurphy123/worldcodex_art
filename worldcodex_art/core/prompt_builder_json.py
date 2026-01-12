from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .world_bible_json import LoadedWorldBibleJSON


@dataclass(frozen=True)
class PromptPackage:
    prompt: str
    negative: str | None
    debug: dict[str, Any]


def _bullets(title: str, items: list[str], max_items: int | None = None) -> list[str]:
    if not items:
        return []
    if max_items is not None:
        items = items[:max_items]
    out = [f"{title}:"]
    out.extend([f"- {x}" for x in items])
    return out


def _pick_palette_keywords(wb: LoadedWorldBibleJSON, palette_name: str | None) -> list[str]:
    if not palette_name:
        return []
    for p in wb.data.visual_identity.palette:
        if p.name == palette_name:
            return p.keywords
    return []


def build_prompt_from_world_json(
    wb: LoadedWorldBibleJSON,
    subject: str,
    *,
    place_id: str | None = None,
    character_id: str | None = None,
    prop_id: str | None = None,
    faction_id: str | None = None,
    motif_ids: list[str] | None = None,
    style_profile_id: str | None = None,
    palette_name: str | None = None,
    render_intent: str | None = None,
    image_style: str | None = None,
    # user overrides
    negative_override: str | None = None,
) -> PromptPackage:
    d = wb.data
    motif_ids = motif_ids or []

    # Resolve entities (fail fast with friendly messages)
    place = wb.places.get(place_id) if place_id else None
    character = wb.characters.get(character_id) if character_id else None
    prop = wb.props.get(prop_id) if prop_id else None
    faction = wb.factions.get(faction_id) if faction_id else None
    style = wb.styles.get(style_profile_id) if style_profile_id else None

    missing = []
    if place_id and not place: missing.append(f"place_id={place_id}")
    if character_id and not character: missing.append(f"character_id={character_id}")
    if prop_id and not prop: missing.append(f"prop_id={prop_id}")
    if faction_id and not faction: missing.append(f"faction_id={faction_id}")
    if style_profile_id and not style: missing.append(f"style_profile_id={style_profile_id}")
    if missing:
        raise ValueError("Unknown id(s): " + ", ".join(missing))

    # Motifs
    motif_texts = []
    unknown_motifs = []
    for mid in motif_ids:
        m = wb.motifs.get(mid)
        if not m:
            unknown_motifs.append(mid)
        else:
            motif_texts.append(m.text)
    if unknown_motifs:
        raise ValueError("Unknown motif id(s): " + ", ".join(unknown_motifs))

    palette_keywords = _pick_palette_keywords(wb, palette_name)

    # Global identity: keep it compact
    global_positive = list(d.prompt_blocks.global_positive)
    camera_defaults = list(d.prompt_blocks.camera_defaults)

    # Tone: keywords are good; "do/avoid" too, but cap it
    tone_bits = []
    if d.world.tone.keywords:
        tone_bits.extend(d.world.tone.keywords[:6])
    if render_intent:
        tone_bits.append(f"render intent: {render_intent}")

    # Style profile prompt positives
    style_positive = list(style.prompt_positive) if style else []
    style_negative = list(style.prompt_negative) if style else []

    # Entity contributions
    entity_positive: list[str] = []
    entity_negative: list[str] = []

    if place:
        entity_positive.extend(place.keywords[:8])
        entity_positive.extend(place.prompt_positive[:10])
        if place.set_dressing:
            entity_positive.append("set dressing: " + ", ".join(place.set_dressing[:12]))
        entity_negative.extend(place.prompt_negative[:10])

    if character:
        entity_positive.extend(character.keywords[:6])
        if character.role:
            entity_positive.append(f"character role: {character.role}")
        if character.wardrobe:
            entity_positive.append("wardrobe: " + ", ".join(character.wardrobe[:10]))
        if character.props:
            entity_positive.append("carried props: " + ", ".join(character.props[:8]))
        entity_positive.extend(character.prompt_positive[:8])
        entity_negative.extend(character.prompt_negative[:8])

    if prop:
        entity_positive.extend(prop.keywords[:6])
        entity_positive.extend(prop.prompt_positive[:8])
        entity_negative.extend(prop.prompt_negative[:8])

    if faction:
        entity_positive.extend(faction.keywords[:6])
        if faction.visual_cues:
            entity_positive.append("faction visual cues: " + ", ".join(faction.visual_cues[:10]))

    # Constraints (important but short)
    always_true = d.visual_identity.constraints.always_true[:5]
    never_show = d.visual_identity.constraints.never_show[:12]

    # Materials + lighting + palette cues
    material_bits = d.visual_identity.materials[:8]
    lighting_bits = d.visual_identity.lighting[:6]

    # Compose prompt
    parts: list[str] = []
    parts.append(f"WORLD: {d.world.name}")
    if d.world.logline:
        parts.append(f"World vibe: {d.world.logline}")

    parts.extend(_bullets("Tone keywords", tone_bits, max_items=10))
    parts.extend(_bullets("Visual motifs", motif_texts, max_items=8))

    if palette_keywords:
        parts.extend(_bullets(f"Palette ({palette_name})", palette_keywords, max_items=8))

    parts.extend(_bullets("Materials", material_bits, max_items=8))
    parts.extend(_bullets("Lighting", lighting_bits, max_items=6))

    parts.extend(_bullets("Global prompt cues", global_positive, max_items=10))
    if style_positive:
        parts.extend(_bullets("Style profile cues", style_positive, max_items=12))

    if entity_positive:
        parts.extend(_bullets("Scene-specific cues", entity_positive, max_items=18))

    parts.extend(_bullets("Always true", always_true, max_items=5))

    if image_style:
        parts.extend(_bullets("Image style override", [image_style], max_items=1))

    # Subject last, like a clap of thunder
    parts.append("SUBJECT:")
    parts.append(subject.strip())

    if camera_defaults:
        parts.extend(_bullets("Camera", camera_defaults, max_items=6))

    prompt = "\n".join([p for p in parts if p.strip()]).strip()

    # Merge negatives
    negatives: list[str] = []
    negatives.extend(d.prompt_blocks.global_negative)
    negatives.extend(style_negative)
    negatives.extend(entity_negative)
    negatives.extend(never_show)
    if negative_override:
        negatives.append(negative_override)

    # De-dupe while preserving order
    seen = set()
    negatives_deduped = []
    for x in [n.strip() for n in negatives if n and n.strip()]:
        if x not in seen:
            seen.add(x)
            negatives_deduped.append(x)

    negative = ", ".join(negatives_deduped) if negatives_deduped else None

    return PromptPackage(
        prompt=prompt,
        negative=negative,
        debug={
            "place_id": place_id,
            "character_id": character_id,
            "prop_id": prop_id,
            "faction_id": faction_id,
            "motif_ids": motif_ids,
            "style_profile_id": style_profile_id,
            "palette_name": palette_name,
            "render_intent": render_intent,
            "image_style": image_style,
            "negative_terms": len(negatives_deduped),
        },
    )
