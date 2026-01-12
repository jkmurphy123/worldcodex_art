from pathlib import Path

from typer.testing import CliRunner

from worldcodex_art.core.config import AppConfig, ProviderConfig, WorldConfig, save_config
from worldcodex_art.main import app
from worldcodex_art.providers import mock_provider


def test_image_gen_dry_run_prints_prompt(monkeypatch):
    runner = CliRunner()
    with runner.isolated_filesystem():
        world_path = Path(__file__).resolve().parent.parent / "worldcodex_art" / "world_bible.json"
        cfg = AppConfig(
            world=WorldConfig(world_bible_json_path=str(world_path)),
            provider=ProviderConfig(name="mock", model=None),
        )
        save_config(cfg)

        def boom(*args, **kwargs):
            raise AssertionError("generate should not be called in dry-run")

        monkeypatch.setattr(mock_provider.MockProvider, "generate", boom)

        result = runner.invoke(
            app,
            ["image", "gen", "test subject", "--dry-run", "--image-style", "oil painting, Monet"],
        )
        assert result.exit_code == 0
        assert "prompt:" in result.stdout
        assert "Image style override" in result.stdout
        assert "SUBJECT:" in result.stdout
        assert "provider: mock" in result.stdout
