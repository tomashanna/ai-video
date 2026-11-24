"""Structured logging with secret redaction.

``configure_logging()`` installs a single stderr handler that emits either a compact
human format or one JSON object per line (``AIVIDEO_LOG_JSON=1``). A redaction filter
masks configured API keys and common key shapes so secrets never reach logs, even if a
provider exception message echoes a request header.
"""

from __future__ import annotations

import json
import logging
import re
import sys
from collections.abc import Iterable
from datetime import UTC, datetime
from typing import Any

# Shapes of common credentials (Google API keys, Replicate tokens, ElevenLabs/OpenAI-style keys).
_SECRET_PATTERNS = [
    re.compile(r"AIza[0-9A-Za-z_\-]{30,}"),
    re.compile(r"r8_[0-9A-Za-z]{20,}"),
    re.compile(r"\bsk[_-][0-9A-Za-z_\-]{20,}"),
    re.compile(r"(?i)(x-goog-api-key|xi-api-key|authorization)(['\"]?\s*[:=]\s*['\"]?)([^'\"\s,}]+)"),
]
REDACTED = "***REDACTED***"


def redact(text: str, extra_secrets: Iterable[str] = ()) -> str:
    """Mask secrets in ``text``. Pure function — easy to test."""
    for s in extra_secrets:
        if s and len(s) >= 6:
            text = text.replace(s, REDACTED)
    for pat in _SECRET_PATTERNS:
        if pat.groups >= 3:
            text = pat.sub(lambda m: f"{m.group(1)}{m.group(2)}{REDACTED}", text)
        else:
            text = pat.sub(REDACTED, text)
    return text


class RedactingFilter(logging.Filter):
    def __init__(self, secrets: Iterable[str] = ()) -> None:
        super().__init__()
        self._secrets = [s for s in secrets if s]

    def filter(self, record: logging.LogRecord) -> bool:
        msg = record.getMessage()
        record.msg = redact(msg, self._secrets)
        record.args = None
        return True


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        payload: dict[str, Any] = {
            "ts": datetime.fromtimestamp(record.created, tz=UTC).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "msg": record.getMessage(),
        }
        extra = getattr(record, "fields", None)
        if isinstance(extra, dict):
            payload.update(extra)
        if record.exc_info:
            payload["exc"] = self.formatException(record.exc_info)
        return json.dumps(payload, ensure_ascii=False, default=str)


_configured = False


def configure_logging(level: str | None = None, json_output: bool | None = None) -> None:
    """Idempotently configure the ``ai_video`` logger tree."""
    global _configured
    from ai_video.config import get_settings

    settings = get_settings()
    lvl = (level or settings.log_level).upper()
    use_json = settings.log_json if json_output is None else json_output

    root = logging.getLogger("ai_video")
    root.setLevel(lvl)
    if _configured:
        for h in root.handlers:
            h.setFormatter(JsonFormatter() if use_json else _human_formatter())
        return
    handler = logging.StreamHandler(sys.stderr)
    handler.setFormatter(JsonFormatter() if use_json else _human_formatter())
    handler.addFilter(RedactingFilter(settings.secret_values()))
    root.addHandler(handler)
    root.propagate = False
    _configured = True


def _human_formatter() -> logging.Formatter:
    return logging.Formatter("%(asctime)s %(levelname)-7s %(name)s: %(message)s", "%H:%M:%S")


def get_logger(name: str) -> logging.Logger:
    if not name.startswith("ai_video"):
        name = f"ai_video.{name}"
    return logging.getLogger(name)
