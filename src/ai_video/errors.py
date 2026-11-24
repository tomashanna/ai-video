"""Typed errors so callers (and the CLI) can fail fast with actionable messages."""

from __future__ import annotations


class AIVideoError(Exception):
    """Base class for all ai_video errors."""


class ConfigError(AIVideoError):
    """Configuration is missing or invalid (e.g. an API key is not set)."""


class MissingDependencyError(AIVideoError):
    """An optional Python package or external binary (ffmpeg, npx) is not installed."""


class BudgetExceededError(AIVideoError):
    """A paid API call would push spend over the configured budget."""


class SpecValidationError(AIVideoError):
    """A creative spec does not conform to the schema."""

    def __init__(self, message: str, errors: list[str] | None = None) -> None:
        super().__init__(message)
        self.errors = errors or []


class ProviderError(AIVideoError):
    """A generative provider returned an error or an unusable response."""
