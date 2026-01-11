from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import hashlib


@dataclass(frozen=True)
class WorldBible:
    path: Path
    sha256: str
    text: str


def load_world_bible(path: str | Path) -> WorldBible:
    p = Path(path).expanduser().resolve()
    if not p.exists():
        raise FileNotFoundError(f"world_bible.md not found: {p}")
    if p.suffix.lower() not in {".md", ".markdown"}:
        raise ValueError(f"Expected a markdown file, got: {p.name}")

    text = p.read_text(encoding="utf-8")
    sha = hashlib.sha256(text.encode("utf-8")).hexdigest()
    return WorldBible(path=p, sha256=sha, text=text)
