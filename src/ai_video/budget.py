"""Cost guard for paid API calls.

Every provider call is *estimated* before it runs. :class:`BudgetGuard` keeps an
append-only JSONL ledger (default ``.ai-video/spend.jsonl``) and refuses any call whose
estimate would push the recorded total over ``AIVIDEO_BUDGET_USD``.

Prices are conservative *estimates* in USD (list prices at the time of writing);
override them with ``AIVIDEO_PRICE_<KEY>=<usd>`` (e.g. ``AIVIDEO_PRICE_KLING_PER_S=0.08``).
The guard is a safety net against runaway loops, not an invoice.
"""

from __future__ import annotations

import json
import os
from collections.abc import Callable, Iterator
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

from ai_video.errors import BudgetExceededError
from ai_video.log import get_logger

log = get_logger(__name__)

# Unit prices (USD). Keys are stable identifiers used by providers.
DEFAULT_PRICES: dict[str, float] = {
    "elevenlabs_tts_per_1k_chars": 0.30,
    "elevenlabs_sfx_per_call": 0.10,
    "gemini_image_per_image": 0.04,
    "gemini_vision_per_call": 0.01,
    "veo_per_s": 0.40,
    "kling_per_s": 0.07,
}


def price(key: str) -> float:
    env = os.environ.get(f"AIVIDEO_PRICE_{key.upper()}")
    if env is not None:
        try:
            return float(env)
        except ValueError as exc:
            raise ValueError(f"AIVIDEO_PRICE_{key.upper()} must be a number, got {env!r}") from exc
    return DEFAULT_PRICES[key]


def estimate(key: str, units: float = 1.0) -> float:
    """Estimated cost for ``units`` of ``key`` (e.g. seconds of video, 1k chars)."""
    if units < 0:
        raise ValueError("units must be >= 0")
    return round(price(key) * units, 4)


@dataclass(frozen=True)
class Charge:
    provider: str
    operation: str
    usd: float
    ts: str


class BudgetGuard:
    def __init__(self, ledger: Path, limit_usd: float, *, now: Callable[[], datetime] | None = None) -> None:
        self.ledger = Path(ledger)
        self.limit_usd = float(limit_usd)
        self._now = now or (lambda: datetime.now(UTC))

    def spent(self) -> float:
        if not self.ledger.exists():
            return 0.0
        total = 0.0
        for n, line in enumerate(self.ledger.read_text(encoding="utf-8").splitlines(), 1):
            if not line.strip():
                continue
            try:
                total += float(json.loads(line)["usd"])
            except (ValueError, KeyError, TypeError):
                log.warning("ignoring malformed ledger line %d in %s", n, self.ledger)
        return round(total, 4)

    def remaining(self) -> float:
        return round(self.limit_usd - self.spent(), 4)

    def check(self, usd: float, *, what: str = "call") -> None:
        spent = self.spent()
        if spent + usd > self.limit_usd + 1e-9:
            raise BudgetExceededError(
                f"Refusing {what}: estimated ${usd:.2f} would exceed budget "
                f"(${spent:.2f} spent of ${self.limit_usd:.2f}). Raise AIVIDEO_BUDGET_USD "
                f"or reset the ledger at {self.ledger} if this is intentional."
            )

    def record(self, provider: str, operation: str, usd: float) -> Charge:
        charge = Charge(provider, operation, round(usd, 4), self._now().isoformat())
        self.ledger.parent.mkdir(parents=True, exist_ok=True)
        with self.ledger.open("a", encoding="utf-8") as f:
            f.write(json.dumps(charge.__dict__) + "\n")
        return charge

    @contextmanager
    def charge(self, provider: str, operation: str, usd: float) -> Iterator[None]:
        """Check before the call; record only if the call body succeeds."""
        self.check(usd, what=f"{provider}:{operation}")
        yield
        self.record(provider, operation, usd)
        log.info("spend +$%.3f %s:%s (remaining $%.2f)", usd, provider, operation, self.remaining())


def default_guard() -> BudgetGuard:
    from ai_video.config import get_settings

    s = get_settings()
    return BudgetGuard(s.spend_ledger, s.budget_usd)
