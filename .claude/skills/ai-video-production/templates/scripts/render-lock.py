#!/usr/bin/env python3
"""
render-lock.py — Coordinate long renders across multiple Claude instances.

Prevents the EPIPE / FFmpeg SIGTERM failures that happen when two agents
launch `npx hyperframes render` simultaneously and starve each other of CPU.

Mechanism:
  - A global lockfile at ~/.claude-render-lock.json holds:
      { pid, project, started_at, expected_duration_min, agent_label }
  - `acquire` checks if the lock exists and the holder pid is alive.
    If alive → exit 1 (caller must wait or retry). If stale → take it.
  - `release` deletes the lockfile if pid matches current process.
  - `wait` polls until acquire succeeds (with optional timeout).
  - `status` prints current lock holder.

Usage:
    # Before render
    python scripts/render-lock.py acquire mina-abandonada --duration 15 || \
      python scripts/render-lock.py wait mina-abandonada --timeout 1800

    # Run the render
    npx hyperframes render --output renders/v8.mp4

    # After render
    python scripts/render-lock.py release

    # Anytime
    python scripts/render-lock.py status

Exit codes:
  0 = success (lock acquired / released / waited / status shown)
  1 = lock held by another live process
  2 = stale lock cleaned and re-acquired (still ok, just informative)
  3 = timeout while waiting

Aprendizajes amargos que originaron este script:
  - Sesión 2026-05-10 (mina-abandonada): 3 renders consecutivos fallaron con
    "FFmpeg exited with code 255 / signal 15" porque otro agente estaba a
    12-25% CPU. Diagnóstico tardó ~45 min porque el mensaje de error no
    sugiere "wait for the other agent".

Documentado en: .claude/skills/video-director/ANTI-PATTERNS.md y
                .claude/skills/ai-video-production/PIPELINE.md
"""
import argparse
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

LOCK_PATH = Path.home() / ".claude-render-lock.json"


def is_pid_alive(pid: int) -> bool:
    """POSIX-only check. Returns True if process exists."""
    if pid <= 0:
        return False
    try:
        os.kill(pid, 0)
        return True
    except (OSError, ProcessLookupError):
        return False


def read_lock():
    if not LOCK_PATH.exists():
        return None
    try:
        return json.loads(LOCK_PATH.read_text())
    except (json.JSONDecodeError, OSError):
        return None


def write_lock(project: str, duration_min: float, agent_label: str):
    payload = {
        "pid": os.getpid(),
        "project": project,
        "started_at": datetime.now(timezone.utc).isoformat(),
        "expected_duration_min": duration_min,
        "agent_label": agent_label or "unknown",
    }
    LOCK_PATH.write_text(json.dumps(payload, indent=2))


def cmd_acquire(args):
    existing = read_lock()
    if existing:
        holder_pid = existing.get("pid", 0)
        if is_pid_alive(holder_pid):
            print(f"render-lock: held by pid={holder_pid} project={existing.get('project')} "
                  f"started={existing.get('started_at')}", file=sys.stderr)
            sys.exit(1)
        # stale → clean
        print(f"render-lock: stale lock from dead pid={holder_pid}, taking it", file=sys.stderr)
        LOCK_PATH.unlink(missing_ok=True)
        write_lock(args.project, args.duration, args.agent)
        print(f"render-lock: acquired (stale recovered) pid={os.getpid()}")
        sys.exit(2)
    write_lock(args.project, args.duration, args.agent)
    print(f"render-lock: acquired pid={os.getpid()} project={args.project}")
    sys.exit(0)


def cmd_release(args):
    existing = read_lock()
    if not existing:
        print("render-lock: no lock to release")
        sys.exit(0)
    held_pid = existing.get("pid", 0)
    if held_pid == os.getpid() or args.force:
        LOCK_PATH.unlink(missing_ok=True)
        print(f"render-lock: released (was pid={held_pid})")
        sys.exit(0)
    if not is_pid_alive(held_pid):
        LOCK_PATH.unlink(missing_ok=True)
        print(f"render-lock: cleaned stale lock from pid={held_pid}")
        sys.exit(0)
    print(f"render-lock: cannot release — held by live pid={held_pid} (not us). "
          f"Use --force only if you know what you're doing.", file=sys.stderr)
    sys.exit(1)


def cmd_wait(args):
    deadline = time.time() + args.timeout
    poll_interval = 5  # seconds — render times are minutes, no point polling fast
    while time.time() < deadline:
        existing = read_lock()
        if not existing or not is_pid_alive(existing.get("pid", 0)):
            # stale or absent → take it
            if existing:
                LOCK_PATH.unlink(missing_ok=True)
            write_lock(args.project, args.duration, args.agent)
            print(f"render-lock: acquired after wait pid={os.getpid()}")
            sys.exit(0)
        time.sleep(poll_interval)
    existing = read_lock() or {}
    print(f"render-lock: timeout after {args.timeout}s waiting for "
          f"pid={existing.get('pid')} project={existing.get('project')}",
          file=sys.stderr)
    sys.exit(3)


def cmd_status(args):
    existing = read_lock()
    if not existing:
        print("render-lock: free")
        sys.exit(0)
    holder_pid = existing.get("pid", 0)
    alive = is_pid_alive(holder_pid)
    started = existing.get("started_at", "?")
    project = existing.get("project", "?")
    duration = existing.get("expected_duration_min", "?")
    agent = existing.get("agent_label", "?")
    state = "ALIVE" if alive else "STALE"
    print(f"render-lock: {state} pid={holder_pid} project={project} "
          f"agent={agent} started={started} expected_min={duration}")
    sys.exit(0 if alive else 2)


def main():
    p = argparse.ArgumentParser(description="Coordinate long renders across agents")
    sub = p.add_subparsers(dest="action", required=True)

    a = sub.add_parser("acquire")
    a.add_argument("project")
    a.add_argument("--duration", type=float, default=15, help="Expected duration in minutes (default 15)")
    a.add_argument("--agent", default="", help="Optional label for the agent holding the lock")
    a.set_defaults(func=cmd_acquire)

    r = sub.add_parser("release")
    r.add_argument("--force", action="store_true")
    r.set_defaults(func=cmd_release)

    w = sub.add_parser("wait")
    w.add_argument("project")
    w.add_argument("--timeout", type=int, default=1800, help="Max seconds to wait (default 1800)")
    w.add_argument("--duration", type=float, default=15)
    w.add_argument("--agent", default="")
    w.set_defaults(func=cmd_wait)

    s = sub.add_parser("status")
    s.set_defaults(func=cmd_status)

    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
