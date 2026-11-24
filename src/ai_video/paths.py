"""Repository-relative path resolution.

Nothing in the package hardcodes an absolute path. Every location is derived from
:func:`repo_root`, which is resolved in this order:

1. ``AIVIDEO_REPO_ROOT`` environment variable (explicit override).
2. Walking up from this file looking for the repo marker (``pyproject.toml`` next to
   ``assets/``) — works for editable installs and source checkouts.
3. Walking up from the current working directory with the same marker.

If none matches, :class:`~ai_video.errors.ConfigError` is raised with a hint.
"""

from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path

from ai_video.errors import ConfigError

PACKAGE_DIR = Path(__file__).resolve().parent
PROMPTS_DIR = PACKAGE_DIR / "prompts"

_MARKERS = ("pyproject.toml", "assets")


def _looks_like_root(p: Path) -> bool:
    return all((p / m).exists() for m in _MARKERS)


def _walk_up(start: Path) -> Path | None:
    for cand in [start, *start.parents]:
        if _looks_like_root(cand):
            return cand
    return None


@lru_cache(maxsize=1)
def repo_root() -> Path:
    env = os.environ.get("AIVIDEO_REPO_ROOT")
    if env:
        p = Path(env).expanduser().resolve()
        if not p.is_dir():
            raise ConfigError(f"AIVIDEO_REPO_ROOT={env!r} is not a directory")
        return p
    for start in (PACKAGE_DIR, Path.cwd().resolve()):
        found = _walk_up(start)
        if found is not None:
            return found
    raise ConfigError(
        "Could not locate the ai-video repository root (looked for pyproject.toml + assets/). "
        "Run from inside the repo or set AIVIDEO_REPO_ROOT."
    )


def assets_dir() -> Path:
    return repo_root() / "assets"


def library_dir() -> Path:
    """SFX / music / voice catalogs (``assets/library``)."""
    return assets_dir() / "library"


def transitions_dir() -> Path:
    """Global transitions catalog root (contains ``catalog.json``)."""
    return assets_dir() / "transitions"


def avu_dir() -> Path:
    """Pre-rendered audio-visual atomic units (countdowns, outro cards...)."""
    return assets_dir() / "avu"


def voice_effects_catalog() -> Path:
    return assets_dir() / "voice-effects" / "presets-catalog.json"


def templates_dir() -> Path:
    return repo_root() / "templates"


def docs_dir() -> Path:
    return repo_root() / "docs"


def skills_dir() -> Path:
    return repo_root() / ".claude" / "skills"


def model_capabilities_matrix() -> Path:
    return skills_dir() / "ai-video-production" / "MODEL-CAPABILITIES-MATRIX.md"


def hard_rules_doc() -> Path:
    """Doc holding the Hard Rules summary table parsed by :mod:`ai_video.core.hard_rules_parser`.

    The compact table (one row per rule, with thresholds) lives in the operating manual;
    ``docs/HARD-RULES.md`` holds the long-form rationale per rule.
    """
    env = os.environ.get("AIVIDEO_HARD_RULES_PATH")
    return Path(env) if env else docs_dir() / "OPERATING-MANUAL.md"


def human_checklist_doc() -> Path:
    env = os.environ.get("AIVIDEO_HUMAN_CHECKLIST_PATH")
    return Path(env) if env else skills_dir() / "video-director" / "HUMAN-CHECKLIST.md"


def referent_analysis_dir() -> Path:
    """Sanitised empirical referent measurements (``data/referent-analysis``)."""
    env = os.environ.get("REFERENT_ANALYSIS_DIR")
    return Path(env) if env else repo_root() / "data" / "referent-analysis"


def specs_dir() -> Path:
    """Local working directory for per-video creative specs (git-ignored)."""
    return repo_root() / "creative-specs"


def example_specs_dir() -> Path:
    return repo_root() / "examples" / "specs"


def prompt_path(name: str) -> Path:
    p = PROMPTS_DIR / name
    if not p.is_file():
        raise ConfigError(f"Bundled prompt not found: {name}")
    return p


def resolve_asset(ref: str | Path, *, base: Path | None = None) -> Path:
    """Resolve an asset reference as written in specs/catalogs.

    Accepts absolute paths, repo-relative paths (``assets/library/...``) and the legacy
    ``library/...`` / ``transitions/...`` prefixes used by older specs.
    """
    p = Path(ref)
    if p.is_absolute():
        return p
    root = base or repo_root()
    s = p.as_posix()
    for legacy, new in (("library/", "assets/library/"), ("transitions/", "assets/transitions/")):
        if s.startswith(legacy):
            return root / (new + s[len(legacy) :])
    return root / p
