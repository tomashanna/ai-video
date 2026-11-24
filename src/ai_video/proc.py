"""Safe subprocess helpers.

* Commands are always argument lists — never ``shell=True`` — so untrusted file names
  or spec values cannot inject shell syntax.
* Every call has a timeout.
* Missing binaries (ffmpeg, ffprobe, npx) raise :class:`MissingDependencyError` with an
  install hint instead of a bare ``FileNotFoundError``.
"""

from __future__ import annotations

import json
import shutil
import subprocess
from collections.abc import Sequence
from pathlib import Path

from ai_video.errors import MissingDependencyError

_INSTALL_HINTS = {
    "ffmpeg": "brew install ffmpeg  |  apt-get install ffmpeg",
    "ffprobe": "ships with ffmpeg (brew install ffmpeg)",
    "npx": "install Node.js >= 22 (https://nodejs.org)",
}


def which(binary: str) -> str | None:
    return shutil.which(binary)


def require_binary(binary: str) -> str:
    path = which(binary)
    if path is None:
        hint = _INSTALL_HINTS.get(binary, "install it and make sure it is on PATH")
        raise MissingDependencyError(f"'{binary}' not found on PATH ({hint}).")
    return path


def run(
    cmd: Sequence[str | Path],
    *,
    timeout: float = 600.0,
    check: bool = True,
    capture: bool = True,
    cwd: Path | None = None,
) -> subprocess.CompletedProcess[str]:
    """Run ``cmd`` (a list) with a timeout; raise CalledProcessError on failure if ``check``."""
    if isinstance(cmd, (str, bytes)):
        raise TypeError("cmd must be a sequence of arguments, not a shell string")
    args = [str(c) for c in cmd]
    if not Path(args[0]).is_absolute():
        require_binary(args[0])
    return subprocess.run(
        args,
        check=check,
        capture_output=capture,
        text=True,
        timeout=timeout,
        cwd=cwd,
    )


def ffprobe_json(path: Path, *, timeout: float = 60.0) -> dict:
    res = run(
        ["ffprobe", "-v", "error", "-print_format", "json", "-show_format", "-show_streams", str(path)],
        timeout=timeout,
    )
    data: dict = json.loads(res.stdout or "{}")
    return data


def media_duration_s(path: Path) -> float:
    """Container duration in seconds (raises ValueError if unknown)."""
    fmt = ffprobe_json(path).get("format", {})
    try:
        return float(fmt["duration"])
    except (KeyError, TypeError, ValueError) as exc:
        raise ValueError(f"could not read duration of {path}") from exc
