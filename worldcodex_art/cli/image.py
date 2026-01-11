from __future__ import annotations

from pathlib import Path
import typer

from worldcodex_art.core.config import load_config
from worldcodex_art.core.registry import PROVIDERS
from worldcodex_art.core.world import load_world_bible
from worldcodex_art.core.prompt_builder import build_prompt
from worldcodex_art.providers.base import ImageRequest

app = typer.Typer(no_args_is_help=True)

@app.command("gen")
def gen(
    subject: str = typer.Argument(...),
    n: int = typer.Option(1, "--n", min=1, max=8),
    out_dir: Path = typer.Option(Path("images"), "--out"),
    seed: int | None = typer.Option(None, "--seed"),
):
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

    provider_factory = PROVIDERS.get(cfg.provider.name)
    if not provider_factory:
        raise typer.BadParameter(f"Provider not available: {cfg.provider.name}")
    provider = provider_factory()

    req = ImageRequest(
        prompt=pkg.prompt,
        negative=pkg.negative,
        size=pkg.size,
        n=n,
        seed=seed,
        style_profile=pkg.style_profile,
        render_intent=pkg.render_intent,
        extra=None,
    )
    res = provider.generate(req, out_dir=out_dir)
    typer.echo(f"provider: {res.provider}")
    for p in res.images:
        typer.echo(str(p))
