from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
import json

from .paths import get_project_config_path, ensure_dir


@dataclass
class WorldConfig:
    world_bible_path: str | None = None
    world_bible_sha256: str | None = None


@dataclass
class ArtConfig:
    size: str = "1024x1024"
    aspect: str = "square"
    style_profile: str = "industrial_amber"
    render_intent: str = "concept"
    palette: str | None = None
    negative: str | None = "text, watermark, logo"


@dataclass
class ProviderConfig:
    name: str = "mock"
    model: str | None = None


@dataclass
class AppConfig:
    world: WorldConfig = WorldConfig()
    art: ArtConfig = ArtConfig()
    provider: ProviderConfig = ProviderConfig()


def load_config() -> AppConfig:
    cfg_path = get_project_config_path()
    if not cfg_path.exists():
        return AppConfig()
    data = json.loads(cfg_path.read_text(encoding="utf-8"))
    # Minimal, forgiving load:
    cfg = AppConfig()
    cfg.world = WorldConfig(**data.get("world", {}))
    cfg.art = ArtConfig(**data.get("art", {}))
    cfg.provider = ProviderConfig(**data.get("provider", {}))
    return cfg


def save_config(cfg: AppConfig) -> Path:
    cfg_path = get_project_config_path()
    ensure_dir(cfg_path.parent)
    cfg_path.write_text(json.dumps(asdict(cfg), indent=2), encoding="utf-8")
    return cfg_path
