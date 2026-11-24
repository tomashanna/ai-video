"""Retry with exponential backoff + jitter, and a deadline-bounded polling helper.

Both helpers take an injectable ``sleep``/``clock`` so they are fully unit-testable
without real waiting.
"""

from __future__ import annotations

import random
import time
from collections.abc import Callable
from typing import TypeVar

from ai_video.log import get_logger

T = TypeVar("T")
log = get_logger(__name__)


def backoff_delays(
    attempts: int,
    *,
    base_s: float = 2.0,
    max_s: float = 60.0,
    jitter: float = 0.25,
    rng: random.Random | None = None,
) -> list[float]:
    """Delays to wait *between* ``attempts`` tries (len == attempts - 1)."""
    r = rng or random.Random()
    out = []
    for i in range(max(attempts - 1, 0)):
        d = min(max_s, base_s * (2**i))
        if jitter:
            d *= 1 + r.uniform(-jitter, jitter)
        out.append(max(0.0, d))
    return out


def retry_call(
    fn: Callable[[], T],
    *,
    attempts: int = 3,
    retry_on: tuple[type[BaseException], ...] = (Exception,),
    should_retry: Callable[[BaseException], bool] | None = None,
    base_s: float = 2.0,
    max_s: float = 60.0,
    sleep: Callable[[float], None] = time.sleep,
    describe: str = "call",
) -> T:
    """Call ``fn`` up to ``attempts`` times, backing off exponentially on failure.

    ``should_retry`` can veto retrying a matching exception (e.g. HTTP 4xx other than 429).
    The last exception is re-raised unchanged.
    """
    if attempts < 1:
        raise ValueError("attempts must be >= 1")
    delays = backoff_delays(attempts, base_s=base_s, max_s=max_s)
    for i in range(attempts):
        try:
            return fn()
        except retry_on as exc:
            last = i == attempts - 1
            if last or (should_retry is not None and not should_retry(exc)):
                raise
            wait = delays[i]
            log.warning(
                "%s failed (%s: %s); retry %d/%d in %.1fs",
                describe,
                type(exc).__name__,
                exc,
                i + 1,
                attempts - 1,
                wait,
            )
            sleep(wait)
    raise AssertionError("unreachable")  # pragma: no cover


def poll_until(
    check: Callable[[], T | None],
    *,
    timeout_s: float,
    interval_s: float = 5.0,
    sleep: Callable[[float], None] = time.sleep,
    clock: Callable[[], float] = time.monotonic,
    describe: str = "operation",
) -> T:
    """Call ``check`` until it returns non-None or ``timeout_s`` elapses (TimeoutError)."""
    deadline = clock() + timeout_s
    while True:
        result = check()
        if result is not None:
            return result
        if clock() >= deadline:
            raise TimeoutError(f"{describe} did not finish within {timeout_s:.0f}s")
        sleep(interval_s)
