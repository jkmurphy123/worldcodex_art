from __future__ import annotations

import typer

from worldcodex_art.core.config import load_config, save_config
from worldcodex_art.core.registry import STYLE_PROFILES

app = typer.Typer(no_args_is_help=True)

@app.command("show")
def show():
    cfg = load_config()
    typer.echo(f"size: {cfg.art.size}")
    typer.echo(f"aspect: {cfg.art.aspect}")
    typer.echo(f"style_profile: {cfg.art.style_profile}")
    typer.echo(f"render_intent: {cfg.art.render_intent}")
    typer.echo(f"palette: {cfg.art.palette}")
    typer.echo(f"negative: {cfg.art.negative}")

@app.command("set")
def set_(
    size: str | None = typer.Option(None, help="e.g. 1024x1024"),
    aspect: str | None = typer.Option(None, help="square|portrait|landscape"),
    style: str | None = typer.Option(None, help="Style profile name"),
    intent: str | None = typer.Option(None, help="concept|illustration|cinematic|blueprint|poster|ui_mock"),
    palette: str | None = typer.Option(None, help="Optional palette hint"),
    negative: str | None = typer.Option(None, help="Negative prompt override"),
):
    cfg = load_config()
    if size: cfg.art.size = size
    if aspect: cfg.art.aspect = aspect
    if style:
        if style not in STYLE_PROFILES:
            raise typer.BadParameter(f"Unknown style profile: {style}")
        cfg.art.style_profile = style
    if intent: cfg.art.render_intent = intent
    if palette is not None: cfg.art.palette = palette
    if negative is not None: cfg.art.negative = negative
    out = save_config(cfg)
    typer.echo(f"Saved config: {out}")

@app.command("styles")
def styles():
    for name in sorted(STYLE_PROFILES.keys()):
        typer.echo(name)
