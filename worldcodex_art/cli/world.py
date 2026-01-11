from __future__ import annotations

from pathlib import Path
import typer

from worldcodex_art.core.config import load_config, save_config
from worldcodex_art.core.world import load_world_bible

app = typer.Typer(no_args_is_help=True)

@app.command("load")
def load(path: Path = typer.Argument(..., help="Path to world_bible.md")):
    wb = load_world_bible(path)
    cfg = load_config()
    cfg.world.world_bible_path = str(wb.path)
    cfg.world.world_bible_sha256 = wb.sha256
    out = save_config(cfg)
    typer.echo(f"World loaded: {wb.path}")
    typer.echo(f"SHA256: {wb.sha256[:12]}…")
    typer.echo(f"Saved config: {out}")

@app.command("show")
def show():
    cfg = load_config()
    typer.echo(f"world_bible_path: {cfg.world.world_bible_path}")
    typer.echo(f"world_bible_sha256: {cfg.world.world_bible_sha256}")
