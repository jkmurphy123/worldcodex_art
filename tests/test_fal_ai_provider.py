import json
from urllib.request import Request

from worldcodex_art.core.registry import PROVIDERS
from worldcodex_art.providers import fal_ai_provider
from worldcodex_art.providers.base import ImageRequest


def test_fal_ai_provider_registered():
    assert "fal_ai" in PROVIDERS


def test_fal_ai_provider_instantiation():
    provider = PROVIDERS["fal_ai"]()
    assert provider.name == "fal_ai"


def test_fal_ai_generate_downloads_images(monkeypatch, tmp_path):
    calls = {"posts": [], "gets": []}

    class FakeResponse:
        def __init__(self, data: bytes):
            self._data = data

        def read(self):
            return self._data

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            return False

    def fake_urlopen(request):
        if isinstance(request, Request):
            body = json.loads(request.data.decode("utf-8"))
            calls["posts"].append(body)
            payload = {"images": [{"url": "https://example.com/image.png"}]}
            return FakeResponse(json.dumps(payload).encode("utf-8"))
        calls["gets"].append(request)
        return FakeResponse(b"fake_image_bytes")

    monkeypatch.setenv("FAL_KEY", "test-key")
    monkeypatch.setattr(fal_ai_provider, "urlopen", fake_urlopen)

    req = ImageRequest(prompt="test prompt", negative=None, size="1024x1024", n=1)
    provider = fal_ai_provider.FalAIImageProvider()
    result = provider.generate(req, out_dir=tmp_path)

    assert result.provider == "fal_ai"
    assert result.model == "fal-ai/flux/schnell"
    assert len(result.images) == 1
    assert result.images[0].exists()
    assert calls["posts"][0]["prompt"] == "test prompt"
    assert calls["posts"][0]["num_images"] == 1
