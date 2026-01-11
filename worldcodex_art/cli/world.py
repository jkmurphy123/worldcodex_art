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

list_app = typer.Typer(no_args_is_help=True, help="List entities from the loaded world JSON.")
show_app = typer.Typer(no_args_is_help=True, help="Show details for one entity from the loaded world JSON.")

app.add_typer(list_app, name="list")
app.add_typer(show_app, name="show")


def _require_world_json():
    cfg = load_config()
    if not cfg.world.world_bible_json_path:
        raise typer.BadParameter(
            "No world JSON loaded. Run: worldcodex-art world load-json /path/to/world_bible.json"
        )
    return load_world_bible_json(cfg.world.world_bible_json_path)


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
    typer.echo(f"  factions: {len(wb.factions)}")
    typer.echo(f"  motifs: {len(wb.motifs)}")
    typer.echo(f"  styles: {len(wb.styles)}")
    typer.echo(f"Saved config: {out}")


@app.command("status")
def status():
    """
    Show currently loaded world bibles (md and json).
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


# ----------------------------
# world list <entity_type>
# ----------------------------

@list_app.command("places")
def list_places():
    wb = _require_world_json()
    for k in sorted(wb.places.keys()):
        typer.echo(k)

@list_app.command("characters")
def list_characters():
    wb = _require_world_json()
    for k in sorted(wb.characters.keys()):
        typer.echo(k)

@list_app.command("props")
def list_props():
    wb = _require_world_json()
    for k in sorted(wb.props.keys()):
        typer.echo(k)

@list_app.command("factions")
def list_factions():
    wb = _require_world_json()
    for k in sorted(wb.factions.keys()):
        typer.echo(k)

@list_app.command("motifs")
def list_motifs():
    wb = _require_world_json()
    for k in sorted(wb.motifs.keys()):
        typer.echo(k)

@list_app.command("styles")
def list_styles():
    wb = _require_world_json()
    for k in sorted(wb.styles.keys()):
        typer.echo(k)


# ----------------------------
# world show <entity_type> <id>
# ----------------------------

@show_app.command("place")
def show_place(place_id: str = typer.Argument(..., help="Place id")):
    wb = _require_world_json()
    p = wb.places.get(place_id)
    if not p:
        raise typer.BadParameter(f"Unknown place id: {place_id}")
    typer.echo(f"{p.id}  ({p.name})")
    if getattr(p, "type", None):
        typer.echo(f"type: {p.type}")
    if p.keywords:
        typer.echo("keywords: " + ", ".join(p.keywords))
    if p.prompt_positive:
        typer.echo("\nprompt_positive:")
        for x in p.prompt_positive:
            typer.echo(f"  - {x}")
    if p.set_dressing:
        typer.echo("\nset_dressing:")
        for x in p.set_dressing:
            typer.echo(f"  - {x}")
    if p.prompt_negative:
        typer.echo("\nprompt_negative:")
        for x in p.prompt_negative:
            typer.echo(f"  - {x}")

@show_app.command("character")
def show_character(character_id: str = typer.Argument(..., help="Character id")):
    wb = _require_world_json()
    c = wb.characters.get(character_id)
    if not c:
        raise typer.BadParameter(f"Unknown character id: {character_id}")
    typer.echo(f"{c.id}  ({c.name})")
    if getattr(c, "role", None):
        typer.echo(f"role: {c.role}")
    if c.keywords:
        typer.echo("keywords: " + ", ".join(c.keywords))
    if c.wardrobe:
        typer.echo("\nwardrobe:")
        for x in c.wardrobe:
            typer.echo(f"  - {x}")
    if c.props:
        typer.echo("\nprops:")
        for x in c.props:
            typer.echo(f"  - {x}")
    if c.prompt_positive:
        typer.echo("\nprompt_positive:")
        for x in c.prompt_positive:
            typer.echo(f"  - {x}")
    if c.prompt_negative:
        typer.echo("\nprompt_negative:")
        for x in c.prompt_negative:
            typer.echo(f"  - {x}")

@show_app.command("prop")
def show_prop(prop_id: str = typer.Argument(..., help="Prop id")):
    wb = _require_world_json()
    p = wb.props.get(prop_id)
    if not p:
        raise typer.BadParameter(f"Unknown prop id: {prop_id}")
    typer.echo(f"{p.id}  ({p.name})")
    if p.keywords:
        typer.echo("keywords: " + ", ".join(p.keywords))
    if p.prompt_positive:
        typer.echo("\nprompt_positive:")
        for x in p.prompt_positive:
            typer.echo(f"  - {x}")
    if p.prompt_negative:
        typer.echo("\nprompt_negative:")
        for x in p.prompt_negative:
            typer.echo(f"  - {x}")

@show_app.command("faction")
def show_faction(faction_id: str = typer.Argument(..., help="Faction id")):
    wb = _require_world_json()
    f = wb.factions.get(faction_id)
    if not f:
        raise typer.BadParameter(f"Unknown faction id: {faction_id}")
    typer.echo(f"{f.id}  ({f.name})")
    if f.keywords:
        typer.echo("keywords: " + ", ".join(f.keywords))
    if getattr(f, "visual_cues", None):
        cues = getattr(f, "visual_cues", [])
        if cues:
            typer.echo("visual_cues: " + ", ".join(cues))

@show_app.command("motif")
def show_motif(motif_id: str = typer.Argument(..., help="Motif id")):
    wb = _require_world_json()
    m = wb.motifs.get(motif_id)
    if not m:
        raise typer.BadParameter(f"Unknown motif id: {motif_id}")
    typer.echo(f"{m.id}: {m.text}")

@show_app.command("style")
def show_style(style_id: str = typer.Argument(..., help="Style profile id")):
    wb = _require_world_json()
    s = wb.styles.get(style_id)
    if not s:
        raise typer.BadParameter(f"Unknown style id: {style_id}")
    typer.echo(f"{s.id}  ({s.name})")
    if s.prompt_positive:
        typer.echo("\nprompt_positive:")
        for x in s.prompt_positive:
            typer.echo(f"  - {x}")
    if s.prompt_negative:
        typer.echo("\nprompt_negative:")
        for x in s.prompt_negative:
            typer.echo(f"  - {x}")
