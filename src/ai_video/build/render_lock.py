"""Coordinate long renders across multiple agents/terminals with a global lockfile.

Prevents the EPIPE / FFmpeg SIGTERM failures that happen when two agents launch
``npx hyperframes render`` at the same time and starve each other of CPU.

Usage:
    ai-video render-lock acquire <project> --duration 15 \\
      || ai-video render-lock wait <project> --timeout 1800
    npx hyperframes render --output renders/v8.mp4
    ai-video render-lock release <project>
    ai-video render-lock status

Exit codes: 0 ok · 1 held by another live holder · 2 stale lock recovered (still ok) · 3 wait timeout

Design (fixes over the original script):
* The holder is identified by project + the *parent* pid (the long-lived shell/agent),
  and a lock also counts as live until ``started_at + 1.5 x expected duration`` — the old
  version stored the pid of the short-lived CLI process itself, so every lock looked stale
  the moment ``acquire`` returned and never actually protected a render.
* ``acquire`` creates the file atomically (``O_CREAT | O_EXCL``), closing the
  check-then-write race between two agents.
* ``release`` accepts the project name (as the docs always used) and refuses to release
  someone else's live lock without ``--force``.
* Lock location is configurable with ``AIVIDEO_RENDER_LOCK``.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any

EXIT_OK, EXIT_HELD, EXIT_STALE_RECOVERED, EXIT_TIMEOUT = 0, 1, 2, 3
MIN_TTL_MIN = 5.0
TTL_FACTOR = 1.5


def lock_path() -> Path:
    env = os.environ.get("AIVIDEO_RENDER_LOCK")
    return Path(env).expanduser() if env else Path.home() / ".claude-render-lock.json"


def is_pid_alive(pid: int) -> bool:
    """POSIX check. True if the process exists (EPERM also means it exists)."""
    if pid <= 0:
        return False
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    except OSError:
        return False
    return True


def read_lock(path: Path | None = None) -> dict[str, Any] | None:
    p = path or lock_path()
    try:
        data = json.loads(p.read_text())
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return None
    return data if isinstance(data, dict) else None


def is_live(lock: dict[str, Any], *, now: datetime | None = None) -> bool:
    """A lock is live if its holder pid is alive OR it is still within its TTL."""
    if is_pid_alive(int(lock.get("pid", 0) or 0)):
        return True
    try:
        started = datetime.fromisoformat(str(lock["started_at"]))
        minutes = max(MIN_TTL_MIN, float(lock.get("expected_duration_min", 0)) * TTL_FACTOR)
    except (KeyError, ValueError, TypeError):
        return False
    return (now or datetime.now(UTC)) < started + timedelta(minutes=minutes)


def _payload(project: str, duration_min: float, agent: str, pid: int) -> dict[str, Any]:
    return {
        "pid": pid,
        "project": project,
        "started_at": datetime.now(UTC).isoformat(),
        "expected_duration_min": duration_min,
        "agent_label": agent or "unknown",
    }


def try_create(path: Path, payload: dict[str, Any]) -> bool:
    """Atomically create the lockfile. False if it already exists."""
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        fd = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o644)
    except FileExistsError:
        return False
    with os.fdopen(fd, "w") as f:
        json.dump(payload, f, indent=2)
    return True


def acquire(
    project: str,
    duration_min: float = 15,
    agent: str = "",
    *,
    pid: int | None = None,
    path: Path | None = None,
) -> int:
    p = path or lock_path()
    payload = _payload(project, duration_min, agent, pid if pid is not None else os.getppid())
    if try_create(p, payload):
        return EXIT_OK
    existing = read_lock(p)
    if existing is not None and is_live(existing):
        return EXIT_HELD
    p.unlink(missing_ok=True)  # stale (or corrupt) lock
    return EXIT_STALE_RECOVERED if try_create(p, payload) else EXIT_HELD


def release(project: str | None, *, force: bool = False, path: Path | None = None) -> int:
    p = path or lock_path()
    existing = read_lock(p)
    if existing is None:
        p.unlink(missing_ok=True)
        return EXIT_OK
    ours = project is not None and existing.get("project") == project
    if ours or force or not is_live(existing):
        p.unlink(missing_ok=True)
        return EXIT_OK
    return EXIT_HELD


def _cmd_acquire(a: argparse.Namespace) -> int:
    rc = acquire(a.project, a.duration, a.agent)
    if rc == EXIT_HELD:
        lk = read_lock() or {}
        print(
            f"render-lock: held by project={lk.get('project')} pid={lk.get('pid')} "
            f"started={lk.get('started_at')}",
            file=sys.stderr,
        )
    else:
        print(f"render-lock: acquired project={a.project}" + (" (stale lock recovered)" if rc else ""))
    return rc


def _cmd_release(a: argparse.Namespace) -> int:
    rc = release(a.project, force=a.force)
    if rc == EXIT_HELD:
        lk = read_lock() or {}
        print(
            f"render-lock: cannot release — live lock held by project={lk.get('project')}. "
            f"Use --force only if you know what you're doing.",
            file=sys.stderr,
        )
    else:
        print("render-lock: released")
    return rc


def _cmd_wait(a: argparse.Namespace) -> int:
    deadline = time.monotonic() + a.timeout
    while True:
        rc = acquire(a.project, a.duration, a.agent)
        if rc != EXIT_HELD:
            print(f"render-lock: acquired after wait project={a.project}")
            return EXIT_OK
        if time.monotonic() >= deadline:
            lk = read_lock() or {}
            print(
                f"render-lock: timeout after {a.timeout}s waiting for project={lk.get('project')}",
                file=sys.stderr,
            )
            return EXIT_TIMEOUT
        time.sleep(a.poll)


def _cmd_status(_: argparse.Namespace) -> int:
    lk = read_lock()
    if lk is None:
        print("render-lock: free")
        return EXIT_OK
    live = is_live(lk)
    print(
        f"render-lock: {'LIVE' if live else 'STALE'} project={lk.get('project')} pid={lk.get('pid')} "
        f"agent={lk.get('agent_label')} started={lk.get('started_at')} "
        f"expected_min={lk.get('expected_duration_min')}"
    )
    return EXIT_OK if live else EXIT_STALE_RECOVERED


def main() -> int:
    p = argparse.ArgumentParser(description="Coordinate long renders across agents")
    sub = p.add_subparsers(dest="action", required=True)

    a = sub.add_parser("acquire")
    a.add_argument("project")
    a.add_argument("--duration", type=float, default=15, help="Expected minutes (default 15)")
    a.add_argument("--agent", default="", help="Optional label for the holder")
    a.set_defaults(func=_cmd_acquire)

    r = sub.add_parser("release")
    r.add_argument("project", nargs="?", default=None)
    r.add_argument("--force", action="store_true")
    r.set_defaults(func=_cmd_release)

    w = sub.add_parser("wait")
    w.add_argument("project")
    w.add_argument("--timeout", type=int, default=1800, help="Max seconds to wait (default 1800)")
    w.add_argument("--duration", type=float, default=15)
    w.add_argument("--agent", default="")
    w.add_argument("--poll", type=float, default=5.0, help=argparse.SUPPRESS)
    w.set_defaults(func=_cmd_wait)

    s = sub.add_parser("status")
    s.set_defaults(func=_cmd_status)

    args = p.parse_args()
    rc: int = args.func(args)
    return rc


if __name__ == "__main__":
    sys.exit(main())
