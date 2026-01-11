from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import json
import hashlib

from .world_bible_models import WorldBibleJSON


@dataclass(frozen=True)
class LoadedWorldBibleJSON:
    path: Path
    sha256: str
    data: WorldBibleJSON

    # Convenience indexes (id -> object)
    places: dict[str, object]
    factions: dict[str, object]
    characters: dict[str, object]
    props: dict[str, object]
    motifs: dict[str, object]
    styles: dict[str, object]


def load_world_bible_json(path: str | Path) -> LoadedWorldBibleJSON:
    p = Path(path).expanduser().resolve()
    if not p.exists():
        raise FileNotFoundError(f"world_bible.json not found: {p}")
    if p.suffix.lower() != ".json":
        raise ValueError(f"Expected a .json file, got: {p.name}")

    raw = p.read_text(encoding="utf-8")
    sha = hashlib.sha256(raw.encode("utf-8")).hexdigest()
    payload = json.loads(raw)

    data = WorldBibleJSON.model_validate(payload)

    places = {x.id: x for x in data.places}
    factions = {x.id: x for x in data.factions}
    characters = {x.id: x for x in data.characters}
    props = {x.id: x for x in data.props}
    motifs = {x.id: x for x in data.visual_identity.motifs}
    styles = {x.id: x for x in data.style_profiles}

    return LoadedWorldBibleJSON(
        path=p,
        sha256=sha,
        data=data,
        places=places,
        factions=factions,
        characters=characters,
        props=props,
        motifs=motifs,
        styles=styles,
    )
