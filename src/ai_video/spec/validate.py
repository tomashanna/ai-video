"""Validate creative specs (YAML) against the v11 schema.

Usage:
    ai-video validate-spec creative-specs/my-video.yaml [more.yaml ...]
    ai-video validate-spec examples/specs/*.yaml --strict      # warnings fail too
    ai-video validate-spec spec.yaml --json                    # machine-readable report
    ai-video validate-spec --print-json-schema > spec.schema.json

Exit codes: 0 valid · 1 invalid (or warnings with --strict) · 2 unreadable input.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml
from pydantic import ValidationError

from ai_video.errors import SpecValidationError
from ai_video.spec.schema import CreativeSpec

MAX_SPEC_BYTES = 5 * 1024 * 1024


@dataclass
class Report:
    path: str
    valid: bool
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


def load_yaml(path: Path) -> dict[str, Any]:
    """Safely load a spec file: size-capped, ``yaml.safe_load`` only, mapping at top level."""
    try:
        size = path.stat().st_size
    except OSError as exc:
        raise SpecValidationError(f"cannot read {path}: {exc}") from exc
    if size > MAX_SPEC_BYTES:
        raise SpecValidationError(f"{path} is {size} bytes (limit {MAX_SPEC_BYTES})")
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        raise SpecValidationError(f"{path}: invalid YAML: {exc}") from exc
    if not isinstance(data, dict):
        raise SpecValidationError(f"{path}: top level must be a mapping, got {type(data).__name__}")
    return data


def format_errors(exc: ValidationError) -> list[str]:
    out = []
    for err in exc.errors():
        loc = ".".join(str(p) for p in err["loc"]) or "<root>"
        out.append(f"{loc}: {err['msg']}")
    return out


def parse_spec(data: dict[str, Any]) -> CreativeSpec:
    """Validate a loaded spec dict; raises SpecValidationError with readable messages."""
    try:
        return CreativeSpec.model_validate(data)
    except ValidationError as exc:
        errors = format_errors(exc)
        raise SpecValidationError(f"{len(errors)} schema error(s)", errors) from exc


def load_spec(path: Path) -> CreativeSpec:
    return parse_spec(load_yaml(path))


def validate_file(path: Path) -> Report:
    try:
        spec = load_spec(path)
    except SpecValidationError as exc:
        return Report(str(path), False, exc.errors or [str(exc)])
    return Report(str(path), True, warnings=spec.warnings())


def main() -> int:
    ap = argparse.ArgumentParser(description="Validate creative specs against the v11 schema")
    ap.add_argument("specs", nargs="*", type=Path)
    ap.add_argument("--strict", action="store_true", help="treat warnings as failures")
    ap.add_argument("--json", action="store_true", help="emit a JSON report")
    ap.add_argument("--print-json-schema", action="store_true", help="print the JSON Schema and exit")
    a = ap.parse_args()

    if a.print_json_schema:
        print(json.dumps(CreativeSpec.model_json_schema(), indent=2, ensure_ascii=False))
        return 0
    if not a.specs:
        ap.error("at least one spec path is required")

    reports = [validate_file(p) for p in a.specs]
    if a.json:
        print(json.dumps([r.__dict__ for r in reports], indent=2, ensure_ascii=False))
    else:
        for r in reports:
            status = "OK  " if r.valid and not (a.strict and r.warnings) else "FAIL"
            print(f"{status} {r.path}")
            for e in r.errors:
                print(f"     error: {e}")
            for w in r.warnings:
                print(f"     warn:  {w}")
    failed = any((not r.valid) or (a.strict and r.warnings) for r in reports)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
