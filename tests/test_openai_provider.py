import base64

from worldcodex_art.core.registry import PROVIDERS
from worldcodex_art.providers.base import ImageRequest
from worldcodex_art.providers import openai_provider


def test_openai_provider_registered():
    assert "openai" in PROVIDERS


def test_openai_provider_instantiation():
    provider = PROVIDERS["openai"]()
    assert provider.name == "openai"


def test_openai_generate_writes_files(monkeypatch, tmp_path):
    calls: dict[str, object] = {}

    class FakeItem:
        def __init__(self, b64_json: str):
            self.b64_json = b64_json
            self.url = None

    class FakeResponse:
        def __init__(self, data):
            self.data = data
            self.id = "resp_123"

    class FakeImages:
        def generate(self, model, prompt, size, n):
            calls.update(
                {
                    "model": model,
                    "prompt": prompt,
                    "size": size,
                    "n": n,
                }
            )
            payload = base64.b64encode(b"fakeimage").decode("ascii")
            return FakeResponse([FakeItem(payload) for _ in range(n)])

    class FakeOpenAI:
        def __init__(self, api_key: str):
            self.api_key = api_key
            self.images = FakeImages()

    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    monkeypatch.setattr(openai_provider, "OpenAI", FakeOpenAI)

    req = ImageRequest(prompt="heroic skyline", negative="text, watermark", size="1024x1024", n=2)
    provider = openai_provider.OpenAIImageProvider()
    result = provider.generate(req, out_dir=tmp_path)

    assert result.provider == "openai"
    assert result.model == "gpt-image-1"
    assert result.request_id == "resp_123"
    assert len(result.images) == 2
    assert all(path.exists() for path in result.images)
    assert calls["model"] == "gpt-image-1"
    assert calls["size"] == "1024x1024"
    assert calls["n"] == 2
    assert calls["prompt"].startswith("Avoid: text, watermark")
