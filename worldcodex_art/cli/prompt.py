from __future__ import annotations

import typer

from worldcodex_art.core.config import load_config
from worldcodex_art.core.world import load_world_bible
from worldcodex_art.core.prompt_builder import build_prompt as build_prompt_md

from worldcodex_art.core.world_bible_json import load_world_bible_json
from worldcodex_art.core.prompt_builder_json import build_prompt_from_world_json

app = typer.Typer(no_args_is_help=True)


@app.command("preview")
def preview(
    subject: str = typer.Argument(..., help="What to depict"),
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

        typer.echo("----- PROMPT (JSON) -----")
        typer.echo(pkg.prompt)
        typer.echo("\n----- NEGATIVE -----")
        typer.echo(pkg.negative or "")
        typer.echo("\n----- DEBUG -----")
        for k, v in pkg.debug.items():
            typer.echo(f"{k}: {v}")
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
    typer.echo("----- PROMPT (MD fallback) -----")
    typer.echo(pkg_md.prompt)
    typer.echo("\n----- NEGATIVE -----")
    typer.echo(pkg_md.negative or "")
