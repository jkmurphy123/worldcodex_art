import typer

from worldcodex_art.cli.world import app as world_app
from worldcodex_art.cli.art import app as art_app
from worldcodex_art.cli.provider import app as provider_app
from worldcodex_art.cli.prompt import app as prompt_app
from worldcodex_art.cli.image import app as image_app

app = typer.Typer(no_args_is_help=True, add_completion=False)

app.add_typer(world_app, name="world")
app.add_typer(art_app, name="art")
app.add_typer(provider_app, name="provider")
app.add_typer(prompt_app, name="prompt")
app.add_typer(image_app, name="image")

def main():
    app()

if __name__ == "__main__":
    main()
