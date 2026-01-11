from __future__ import annotations
from pathlib import Path

PROJECT_DIRNAME = ".worldcodex_art"

def get_project_config_path() -> Path:
    return Path.cwd() / PROJECT_DIRNAME / "config.json"

def ensure_dir(p: Path) -> None:
    p.mkdir(parents=True, exist_ok=True)
