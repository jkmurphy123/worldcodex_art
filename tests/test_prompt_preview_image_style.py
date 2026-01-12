from pathlib import Path

from typer.testing import CliRunner

from worldcodex_art.core.config import AppConfig, WorldConfig, save_config
from worldcodex_art.main import app


def test_prompt_preview_includes_image_style():
    runner = CliRunner()
    with runner.isolated_filesystem():
        world_path = Path(__file__).resolve().parent.parent / "worldcodex_art" / "world_bible.json"
        cfg = AppConfig(world=WorldConfig(world_bible_json_path=str(world_path)))
        save_config(cfg)

        result = runner.invoke(
            app,
            ["prompt", "preview", "test subject", "--image-style", "oil painting, Monet"],
        )

        assert result.exit_code == 0
        assert "Image style override" in result.stdout
        assert "oil painting, Monet" in result.stdout
