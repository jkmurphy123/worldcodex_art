from __future__ import annotations

import typer

from worldcodex_art.core.config import load_config, save_config
from worldcodex_art.core.registry import PROVIDERS

app = typer.Typer(no_args_is_help=True)

@app.command("show")
def show():
    cfg = load_config()
    typer.echo(f"provider: {cfg.provider.name}")
    typer.echo(f"model: {cfg.provider.model}")

@app.command("set")
def set_(name: str = typer.Argument(..., help="Provider name (e.g. mock, openai later)")):
    if name not in PROVIDERS:
        raise typer.BadParameter(f"Unknown provider: {name}. Known: {', '.join(sorted(PROVIDERS.keys()))}")
    cfg = load_config()
    cfg.provider.name = name
    out = save_config(cfg)
    typer.echo(f"Provider set to: {name}")
    typer.echo(f"Saved config: {out}")

@app.command("list")
def list_():
    for n in sorted(PROVIDERS.keys()):
        typer.echo(n)
