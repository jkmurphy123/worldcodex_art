from __future__ import annotations

from pathlib import Path
import typer

from worldcodex_art.core.config import load_config
from worldcodex_art.core.dry_run import format_dry_run_output
from worldcodex_art.core.registry import PROVIDERS
from worldcodex_art.providers.base import ImageRequest

from worldcodex_art.core.world import load_world_bible
from worldcodex_art.core.prompt_builder import build_prompt as build_prompt_md

from worldcodex_art.core.world_bible_json import load_world_bible_json
from worldcodex_art.core.prompt_builder_json import build_prompt_from_world_json

app = typer.Typer(no_args_is_help=True)


@app.command("gen")
def gen(
    subject: str = typer.Argument(...),
    n: int = typer.Option(1, "--n", min=1, max=8),
    out_dir: Path = typer.Option(Path(".worldcodex_art/outputs"), "--out"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Print prompt and request without generating images"),
    seed: int | None = typer.Option(None, "--seed"),
    place: str | None = typer.Option(None, "--place", help="Place id from world JSON"),
    character: str | None = typer.Option(None, "--character", help="Character id from world JSON"),
    prop: str | None = typer.Option(None, "--prop", help="Prop id from world JSON"),
    faction: str | None = typer.Option(None, "--faction", help="Faction id from world JSON"),
    motif: list[str] = typer.Option([], "--motif", help="Motif id (repeatable)"),
    style_profile: str | None = typer.Option(None, "--style-profile", help="World style profile id"),
    palette: str | None = typer.Option(None, "--palette", help="World palette name"),
    image_style: str | None = typer.Option(
        None,
        "--image-style",
        help="Image style override separate from world styles",
    ),
):
    cfg = load_config()

    provider_factory = PROVIDERS.get(cfg.provider.name)
    if not provider_factory:
        raise typer.BadParameter(f"Provider not available: {cfg.provider.name}")
    provider = provider_factory()

    # Prefer JSON if loaded
    if cfg.world.world_bible_json_path:
        wb = load_world_bible_json(cfg.world.world_bible_json_path)
        pkg = build_prompt_from_world_json(
            wb,
            subject=subject,
            place_id=place,
            character_id=character,
            prop_id=prop,
            faction_id=faction,
            motif_ids=motif,
            style_profile_id=style_profile,
            palette_name=palette,
            render_intent=cfg.art.render_intent,
            image_style=image_style,
            negative_override=cfg.art.negative,
        )

        req = ImageRequest(
            prompt=pkg.prompt,
            negative=pkg.negative,
            size=cfg.art.size,
            n=n,
            seed=seed,
            style_profile=style_profile or cfg.art.style_profile,
            image_style=image_style,
            render_intent=cfg.art.render_intent,
            extra={"source": "world_json", "debug": pkg.debug},
        )
        if dry_run:
            for line in format_dry_run_output(
                req,
                provider_name=cfg.provider.name,
                model=cfg.provider.model,
                out_dir=out_dir,
            ):
                typer.echo(line)
            return
        res = provider.generate(req, out_dir=out_dir)
        typer.echo(f"provider: {res.provider}")
        for p in res.images:
            typer.echo(str(p))
        return

    # Fallback: markdown
    if not cfg.world.world_bible_path:
        raise typer.BadParameter("No world loaded. Run: worldcodex-art world load /path/to/world_bible.md")

    wb_md = load_world_bible(cfg.world.world_bible_path)
    pkg_md = build_prompt_md(
        wb_md.text,
        subject,
        style_profile=cfg.art.style_profile,
        render_intent=cfg.art.render_intent,
        size=cfg.art.size,
        palette=cfg.art.palette,
        negative=cfg.art.negative,
        image_style=image_style,
    )
    req = ImageRequest(
        prompt=pkg_md.prompt,
        negative=pkg_md.negative,
        size=cfg.art.size,
        n=n,
        seed=seed,
        style_profile=cfg.art.style_profile,
        image_style=image_style,
        render_intent=cfg.art.render_intent,
        extra={"source": "world_md"},
    )
    if dry_run:
        for line in format_dry_run_output(
            req,
            provider_name=cfg.provider.name,
            model=cfg.provider.model,
            out_dir=out_dir,
        ):
            typer.echo(line)
        return
    res = provider.generate(req, out_dir=out_dir)
    typer.echo(f"provider: {res.provider}")
    for p in res.images:
        typer.echo(str(p))
