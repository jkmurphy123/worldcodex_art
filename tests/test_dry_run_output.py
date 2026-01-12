from pathlib import Path

from worldcodex_art.core.dry_run import format_dry_run_output
from worldcodex_art.providers.base import ImageRequest


def test_format_dry_run_output_includes_prompt_and_negative():
    req = ImageRequest(
        prompt="WORLD: Test\nSUBJECT:\nA tower",
        negative="text, watermark",
        size="1024x1024",
        n=1,
        seed=None,
        style_profile="industrial_amber",
        image_style="oil painting, Monet",
        render_intent="concept",
        extra={"source": "world_json"},
    )
    lines = format_dry_run_output(
        req,
        provider_name="mock",
        model=None,
        out_dir=Path("outputs"),
    )
    joined = "\n".join(lines)
    assert "prompt:" in joined
    assert "WORLD: Test" in joined
    assert "negative:" in joined
    assert "text, watermark" in joined
    assert "image_style: oil painting, Monet" in joined
