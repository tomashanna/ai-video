"""Shared pytest configuration.

* Tests marked ``ffmpeg`` are skipped when ffmpeg/ffprobe are not on PATH (CI installs them).
* Every test runs with an isolated environment: no real API keys, a temp spend ledger and a
  fresh settings cache, so nothing can reach a paid API or write outside tmp.
"""

from __future__ import annotations

import shutil

import pytest

HAVE_FFMPEG = shutil.which("ffmpeg") is not None and shutil.which("ffprobe") is not None


def pytest_collection_modifyitems(config: pytest.Config, items: list[pytest.Item]) -> None:
    if HAVE_FFMPEG:
        return
    skip = pytest.mark.skip(reason="ffmpeg/ffprobe not on PATH")
    for item in items:
        if "ffmpeg" in item.keywords:
            item.add_marker(skip)


@pytest.fixture(autouse=True)
def _isolated_env(monkeypatch: pytest.MonkeyPatch, tmp_path_factory: pytest.TempPathFactory):
    for var in ("GEMINI_API_KEY", "ELEVENLABS_API_KEY", "REPLICATE_API_TOKEN"):
        monkeypatch.delenv(var, raising=False)
    ledger_dir = tmp_path_factory.mktemp("ledger")
    monkeypatch.setenv("AIVIDEO_SPEND_LEDGER", str(ledger_dir / "spend.jsonl"))
    monkeypatch.setenv("AIVIDEO_RENDER_LOCK", str(ledger_dir / "render.lock"))
    from ai_video.config import reset_settings_cache

    reset_settings_cache()
    yield
    reset_settings_cache()
