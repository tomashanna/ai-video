"""Factory functions for vendor SDK clients.

Centralises three concerns every provider shares:

* credentials come from :class:`ai_video.config.Settings` (fail fast if missing),
* every client gets an explicit network timeout,
* optional SDKs are imported lazily with an install hint if absent.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from ai_video.config import Settings, get_settings
from ai_video.errors import MissingDependencyError

_EXTRA_HINT = "install the provider extras: uv sync --extra providers"


def settings_with_env_file(env_file: str | Path | None) -> Settings:
    """Settings, optionally layering an explicit ``.env`` file (``--env`` CLI flags)."""
    if env_file is None:
        return get_settings()
    return Settings(_env_file=str(env_file))  # type: ignore[call-arg]


def gemini_client(settings: Settings | None = None) -> Any:
    s = settings or get_settings()
    key = s.require("gemini_api_key")
    try:
        from google import genai
        from google.genai import types
    except ImportError as exc:  # pragma: no cover - depends on environment
        raise MissingDependencyError(f"google-genai is not installed ({_EXTRA_HINT})") from exc
    return genai.Client(api_key=key, http_options=types.HttpOptions(timeout=int(s.http_timeout_s * 1000)))


def elevenlabs_client(settings: Settings | None = None) -> Any:
    s = settings or get_settings()
    key = s.require("elevenlabs_api_key")
    try:
        from elevenlabs import ElevenLabs
    except ImportError as exc:  # pragma: no cover
        raise MissingDependencyError(f"elevenlabs is not installed ({_EXTRA_HINT})") from exc
    return ElevenLabs(api_key=key, timeout=s.http_timeout_s)


def replicate_client(settings: Settings | None = None) -> Any:
    s = settings or get_settings()
    token = s.require("replicate_api_token")
    try:
        import httpx
        import replicate
    except ImportError as exc:  # pragma: no cover
        raise MissingDependencyError(f"replicate/httpx are not installed ({_EXTRA_HINT})") from exc
    return replicate.Client(api_token=token, timeout=httpx.Timeout(s.http_timeout_s, connect=30.0))
