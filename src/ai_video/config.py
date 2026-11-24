"""Centralised, environment-driven configuration.

All runtime knobs live in :class:`Settings` (pydantic-settings). Values come from, in
order of precedence: real environment variables, then a ``.env`` file in the current
working directory. API keys are stored as :class:`~pydantic.SecretStr` so they never
appear in ``repr()`` or logs.

Use :func:`get_settings` (cached) everywhere instead of ``os.environ``. Providers call
:meth:`Settings.require` to fail fast with an actionable message when a key is missing.
"""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Literal

from pydantic import AliasChoices, Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

from ai_video.errors import ConfigError

SecretName = Literal["gemini_api_key", "elevenlabs_api_key", "replicate_api_token"]

_ENV_NAMES: dict[str, str] = {
    "gemini_api_key": "GEMINI_API_KEY",
    "elevenlabs_api_key": "ELEVENLABS_API_KEY",
    "replicate_api_token": "REPLICATE_API_TOKEN",
}


class Settings(BaseSettings):
    """Runtime configuration. See ``.env.example`` for every variable."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        populate_by_name=True,
    )

    # --- Provider credentials (standard vendor variable names) ---------------
    gemini_api_key: SecretStr | None = Field(default=None, validation_alias="GEMINI_API_KEY")
    elevenlabs_api_key: SecretStr | None = Field(default=None, validation_alias="ELEVENLABS_API_KEY")
    replicate_api_token: SecretStr | None = Field(
        default=None, validation_alias="REPLICATE_API_TOKEN"
    )

    # --- Cost guard -----------------------------------------------------------
    budget_usd: float = Field(
        default=10.0,
        ge=0,
        validation_alias=AliasChoices("AIVIDEO_BUDGET_USD", "budget_usd"),
        description="Hard ceiling for estimated paid-API spend recorded in the ledger.",
    )
    spend_ledger: Path = Field(
        default=Path(".ai-video/spend.jsonl"),
        validation_alias=AliasChoices("AIVIDEO_SPEND_LEDGER", "spend_ledger"),
    )
    dry_run: bool = Field(
        default=False,
        validation_alias=AliasChoices("AIVIDEO_DRY_RUN", "dry_run"),
        description="If true, providers validate inputs and budget but never call the API.",
    )

    # --- Network robustness ---------------------------------------------------
    http_timeout_s: float = Field(
        default=120.0, gt=0, validation_alias=AliasChoices("AIVIDEO_HTTP_TIMEOUT_S", "http_timeout_s")
    )
    max_retries: int = Field(
        default=3, ge=0, le=10, validation_alias=AliasChoices("AIVIDEO_MAX_RETRIES", "max_retries")
    )
    poll_timeout_s: float = Field(
        default=900.0,
        gt=0,
        validation_alias=AliasChoices("AIVIDEO_POLL_TIMEOUT_S", "poll_timeout_s"),
        description="Max wall-clock time to wait for long-running generations (Veo, Kling).",
    )

    # --- Logging --------------------------------------------------------------
    log_level: str = Field(default="INFO", validation_alias=AliasChoices("AIVIDEO_LOG_LEVEL", "log_level"))
    log_json: bool = Field(default=False, validation_alias=AliasChoices("AIVIDEO_LOG_JSON", "log_json"))

    def require(self, name: SecretName) -> str:
        """Return the secret value or raise :class:`ConfigError` with a fix hint."""
        value: SecretStr | None = getattr(self, name)
        if value is None or not value.get_secret_value().strip():
            env = _ENV_NAMES[name]
            raise ConfigError(
                f"{env} is not set. Add it to your environment or to a .env file "
                f"(see .env.example). It is required for this command."
            )
        return value.get_secret_value()

    def secret_values(self) -> list[str]:
        """All configured secret values — used by the log redaction filter."""
        out = []
        for name in _ENV_NAMES:
            v: SecretStr | None = getattr(self, name)
            if v is not None and v.get_secret_value():
                out.append(v.get_secret_value())
        return out


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()


def reset_settings_cache() -> None:
    """Testing helper: forget the cached settings so env changes are picked up."""
    get_settings.cache_clear()
