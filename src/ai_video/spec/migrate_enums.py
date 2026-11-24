#!/usr/bin/env python3
"""
migrate-spec-enums.py — Rename vendor-coupled enum values + field names in creative-specs/*.yaml.

Triggered by Bloque G2 2026-05-16 (vendor decoupling of CREATIVE-SPEC enums).

Renames applied:
  - `motion_intensity_intent: kling_full` → `motion_intensity_intent: animation_full`
  - `primeros_30s_kling_obligatorio:`     → `primeros_30s_animation_ai_obligatorio:`
  - (futuras renames se agregan a RENAMES dict abajo)

Modo dry-run por default. Pasá --apply para escribir cambios.

Usage:
  python migrate-spec-enums.py                     # dry-run, reports what WOULD change
  python migrate-spec-enums.py --apply             # writes changes (creates .bak.migration first)
  python migrate-spec-enums.py --apply --dir <D>   # custom specs dir

Safety:
  - Solo opera sobre archivos *.yaml
  - Crea <file>.bak.migration antes de modificar
  - String-level replacement (no YAML parser) para preservar comments/formatting
  - Exit 0 si nada cambió, exit 0 con report si aplicó cambios, exit 1 si error
"""

import argparse
import sys
from pathlib import Path

# Add new renames here as the system evolves
RENAMES = [
    # (old_string, new_string, reason)
    (
        "motion_intensity_intent: kling_full",
        "motion_intensity_intent: animation_full",
        "G2 2026-05-16: vendor decoupling enum value",
    ),
    (
        "primeros_30s_kling_obligatorio:",
        "primeros_30s_animation_ai_obligatorio:",
        "G2 2026-05-16: vendor decoupling field name (CLAUDE.md hard rule #6)",
    ),
]

from ai_video.paths import specs_dir

DEFAULT_DIR = specs_dir()


def migrate_file(path: Path, apply: bool) -> dict:
    """Apply renames to a single yaml file. Returns stats dict."""
    stats = {"path": str(path), "changes": [], "would_change": False}
    try:
        original = path.read_text()
    except Exception as e:
        stats["error"] = str(e)
        return stats

    new = original
    for old_s, new_s, reason in RENAMES:
        n = new.count(old_s)
        if n > 0:
            new = new.replace(old_s, new_s)
            stats["changes"].append(
                {
                    "rename": f"{old_s} → {new_s}",
                    "occurrences": n,
                    "reason": reason,
                }
            )

    if new != original:
        stats["would_change"] = True
        if apply:
            backup = path.with_suffix(path.suffix + ".bak.migration")
            backup.write_text(original)
            path.write_text(new)
            stats["backup"] = str(backup)
            stats["written"] = True

    return stats


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true", help="Apply changes. Without this flag, runs dry-run.")
    ap.add_argument("--dir", default=str(DEFAULT_DIR), help=f"Specs directory (default: {DEFAULT_DIR})")
    args = ap.parse_args()

    specs_dir = Path(args.dir)
    if not specs_dir.exists():
        print(f"ERROR: directory not found: {specs_dir}", file=sys.stderr)
        return 1

    yaml_files = sorted(specs_dir.glob("*.yaml"))
    if not yaml_files:
        print(f"No *.yaml files in {specs_dir} — nothing to migrate.")
        return 0

    mode = "APPLY" if args.apply else "DRY-RUN"
    print(f"=== migrate-spec-enums.py [{mode}] ===")
    print(f"Specs dir: {specs_dir}")
    print(f"Files found: {len(yaml_files)}")
    print()

    total_changed = 0
    for f in yaml_files:
        if f.name.endswith(".bak.migration"):
            continue
        s = migrate_file(f, apply=args.apply)
        if s.get("error"):
            print(f"✗ {f.name}: {s['error']}")
            continue
        if not s["would_change"]:
            print(f"  {f.name}: no changes needed")
            continue
        total_changed += 1
        print(f"{'✓' if args.apply else '→'} {f.name}:")
        for c in s["changes"]:
            print(f"    {c['occurrences']}× {c['rename']}")
            print(f"       ({c['reason']})")
        if args.apply:
            print(f"    backup: {s['backup']}")
        print()

    print("---")
    if total_changed == 0:
        print("✅ No specs need migration. System already aligned.")
    elif args.apply:
        print(f"✅ Migration applied to {total_changed} file(s). Backups created as .bak.migration.")
    else:
        print(f"ℹ️  Dry-run: {total_changed} file(s) would change. Re-run with --apply to write.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
