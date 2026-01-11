from __future__ import annotations

from pathlib import Path
import typer

from worldcodex_art.core.config import load_config, save_config
from worldcodex_art.core.world import load_world_bible
from worldcodex_art.core.world_bible_json import load_world_bible_json

app = typer.Typer(
    no_args_is_help=True,
    help="Load and inspect world bible files (markdown or JSON).",
)


@app.command("load")
def load_md(
    path: Path = typer.Argument(..., help="Path to world_bible.md"),
):
    """
    Load a markdown world bible (legacy / fallback).
    """
    wb = load_world_bible(path)

    cfg = load_config()
    cfg.world.world_bible_path = str(wb.path)
    cfg.world.world_bible_sha256 = wb.sha256

    out = save_config(cfg)

    typer.echo("World markdown loaded:")
    typer.echo(f"  path: {wb.path}")
    typer.echo(f"  sha256: {wb.sha256[:12]}…")
    typer.echo(f"Saved config: {out}")


@app.command("load-json")
def load_json(
    path: Path = typer.Argument(..., help="Path to world_bible.json"),
):
    """
    Load a structured JSON world bible (preferred for image generation).
    """
    wb = load_world_bible_json(path)

    cfg = load_config()
    cfg.world.world_bible_json_path = str(wb.path)
    cfg.world.world_bible_json_sha256 = wb.sha256

    out = save_config(cfg)

    typer.echo("World JSON loaded:")
    typer.echo(f"  path: {wb.path}")
    typer.echo(f"  schema: {wb.data.schema_version}")
    typer.echo(f"  places: {len(wb.places)}")
    typer.echo(f"  characters: {len(wb.characters)}")
    typer.echo(f"  props: {len(wb.props)}")
    typer.echo(f"  motifs: {len(wb.motifs)}")
    typer.echo(f"Saved config: {out}")


@app.command("show")
def show():
    """
    Show currently loaded world bibles.
    """
    cfg = load_config()

    typer.echo("Markdown world bible:")
    if cfg.world.world_bible_path:
        typer.echo(f"  path: {cfg.world.world_bible_path}")
        if cfg.world.world_bible_sha256:
            typer.echo(f"  sha256: {cfg.world.world_bible_sha256[:12]}…")
    else:
        typer.echo("  (not set)")

    typer.echo("\nJSON world bible:")
    if cfg.world.world_bible_json_path:
        typer.echo(f"  path: {cfg.world.world_bible_json_path}")
        if cfg.world.world_bible_json_sha256:
            typer.echo(f"  sha256: {cfg.world.world_bible_json_sha256[:12]}…")
    else:
        typer.echo("  (not set)")
