from pathlib import Path

from worldcodex_art.core.prompt_builder_json import build_prompt_from_world_json
from worldcodex_art.core.world_bible_json import load_world_bible_json


def test_prompt_builder_json_includes_image_style_override():
    world_path = Path(__file__).resolve().parent.parent / "worldcodex_art" / "world_bible.json"
    wb = load_world_bible_json(world_path)

    pkg = build_prompt_from_world_json(
        wb,
        subject="A lone engineer in a corridor",
        image_style="oil painting, Monet",
    )

    assert "Image style override" in pkg.prompt
    assert "oil painting, Monet" in pkg.prompt
    assert pkg.prompt.find("Image style override") < pkg.prompt.find("SUBJECT:")
    assert pkg.debug["image_style"] == "oil painting, Monet"
