from __future__ import annotations

from typing import Literal
from pydantic import BaseModel, Field, ConfigDict


class PaletteItem(BaseModel):
    name: str
    keywords: list[str] = Field(default_factory=list)


class Motif(BaseModel):
    id: str
    text: str


class Constraints(BaseModel):
    always_true: list[str] = Field(default_factory=list)
    never_show: list[str] = Field(default_factory=list)


class Tone(BaseModel):
    keywords: list[str] = Field(default_factory=list)
    do: list[str] = Field(default_factory=list)
    avoid: list[str] = Field(default_factory=list)


class WorldMeta(BaseModel):
    id: str
    name: str
    logline: str | None = None
    genre_tags: list[str] = Field(default_factory=list)
    timeframe: str | None = None
    technology_level: str | None = None
    tone: Tone = Field(default_factory=Tone)


class VisualIdentity(BaseModel):
    palette: list[PaletteItem] = Field(default_factory=list)
    materials: list[str] = Field(default_factory=list)
    lighting: list[str] = Field(default_factory=list)
    motifs: list[Motif] = Field(default_factory=list)
    constraints: Constraints = Field(default_factory=Constraints)


class PromptBlocks(BaseModel):
    global_positive: list[str] = Field(default_factory=list)
    global_negative: list[str] = Field(default_factory=list)
    camera_defaults: list[str] = Field(default_factory=list)


class Place(BaseModel):
    id: str
    name: str
    type: str | None = None
    keywords: list[str] = Field(default_factory=list)
    prompt_positive: list[str] = Field(default_factory=list)
    prompt_negative: list[str] = Field(default_factory=list)
    set_dressing: list[str] = Field(default_factory=list)


class Faction(BaseModel):
    id: str
    name: str
    keywords: list[str] = Field(default_factory=list)
    visual_cues: list[str] = Field(default_factory=list)


class Character(BaseModel):
    id: str
    name: str
    role: str | None = None
    keywords: list[str] = Field(default_factory=list)
    wardrobe: list[str] = Field(default_factory=list)
    props: list[str] = Field(default_factory=list)
    prompt_positive: list[str] = Field(default_factory=list)
    prompt_negative: list[str] = Field(default_factory=list)


class Prop(BaseModel):
    id: str
    name: str
    keywords: list[str] = Field(default_factory=list)
    prompt_positive: list[str] = Field(default_factory=list)
    prompt_negative: list[str] = Field(default_factory=list)


class StyleProfile(BaseModel):
    id: str
    name: str
    prompt_positive: list[str] = Field(default_factory=list)
    prompt_negative: list[str] = Field(default_factory=list)


class WorldBibleJSON(BaseModel):
    """
    v1 world bible optimized for image prompting.
    Keep strings short. Prefer lists of prompt snippets.
    """
    model_config = ConfigDict(extra="forbid")  # catch typos early

    schema_version: Literal["worldcodex.world_bible.v1"]
    world: WorldMeta
    visual_identity: VisualIdentity = Field(default_factory=VisualIdentity)
    prompt_blocks: PromptBlocks = Field(default_factory=PromptBlocks)

    places: list[Place] = Field(default_factory=list)
    factions: list[Faction] = Field(default_factory=list)
    characters: list[Character] = Field(default_factory=list)
    props: list[Prop] = Field(default_factory=list)
    style_profiles: list[StyleProfile] = Field(default_factory=list)
