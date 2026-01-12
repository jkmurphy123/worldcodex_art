from typer.testing import CliRunner

from worldcodex_art.main import app


def test_cli_provider_list_includes_openai():
    runner = CliRunner()
    result = runner.invoke(app, ["provider", "list"])
    assert result.exit_code == 0
    assert "openai" in result.stdout
    assert "fal_ai" in result.stdout
