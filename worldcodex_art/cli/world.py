from pathlib import Path
import typer

from worldcodex_art.core.config import load_config, save_config
from worldcodex_art.core.world import load_world_bible
from worldcodex_art.core.world_bible_json import load_world_bible_json

app = typer.Typer(no_args_is_help=True)

@app.command("load")
def load_md(path: Path = typer.Argument(..., help="Path to world_bible.md")):
    wb = load_world_bible(path)
    cfg = load_config()
    cfg.world.world_bible_path = str(wb.path)
    cfg.world.world_bible_sha256 = wb.sha256
    out = save_config(cfg)
    typer.echo(f"World markdown loaded: {wb.path}")
    typer.echo(f"Saved config: {out}")

@app.command("load-json")
def load_json(path: Path = typer.Argument(..., help="Path to world_bible.json")):
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
