from __future__ import annotations

import typer

from worldcodex_art.core.config import load_config
from worldcodex_art.core.world import load_world_bible
from worldcodex_art.core.prompt_builder import build_prompt

app = typer.Typer(no_args_is_help=True)

@app.command("preview")
def preview(subject: str = typer.Argument(..., help="What to depict")):
    cfg = load_config()
    if not cfg.world.world_bible_path:
        raise typer.BadParameter("No world loaded. Run: world load PATH")

    wb = load_world_bible(cfg.world.world_bible_path)
    pkg = build_prompt(
        wb.text,
        subject,
        style_profile=cfg.art.style_profile,
        render_intent=cfg.art.render_intent,
        size=cfg.art.size,
        palette=cfg.art.palette,
        negative=cfg.art.negative,
    )

    typer.echo("----- PROMPT -----")
    typer.echo(pkg.prompt)
    typer.echo("\n----- NEGATIVE -----")
    typer.echo(pkg.negative or "")
    typer.echo("\n----- SETTINGS -----")
    typer.echo(f"size: {pkg.size}")
    typer.echo(f"style_profile: {pkg.style_profile}")
    typer.echo(f"render_intent: {pkg.render_intent}")
