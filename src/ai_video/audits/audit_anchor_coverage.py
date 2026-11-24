#!/usr/bin/env python3
"""audit-anchor-coverage.py — CP1 anchor-coverage gate (Hard Rule #26 companion).

BUG REAL que cierra (consigna anti-theater): un character/setting/prop que aparece en
>1 shot (o está declarado en reference_anchors) SIN su archivo anchor generado → el batch
de CP4 (animación image-to-video) explota con FileNotFoundError a mitad de camino, DESPUÉS
de haber gastado $ animando los clips previos. CP1 hoy no tiene NINGÚN chequeo de código:
la cobertura de anchors es 100% ojo humano. Este gate la mide.

REGLA:
  needed = set de anchor ids que (a) están declarados en `reference_anchors`
           (characters/settings/props) O (b) aparecen en >1 shot del shot_list.
  present = anchor ids con archivo en <project>/assets/anchors/<id>.{png,jpg,jpeg,webp}.
  Cada needed sin present → FAIL nombrando QUÉ falta (id + por qué es necesario).
  Algo que aparece en 1 SOLO shot y NO está declarado → NO requerido (no se exige anchor).

Anchor ids se derivan de los DOS dialectos de SPEC que conviven:
  (1) matadero-style: bloque `reference_anchors:` con listas characters/settings/props,
      cada entry con `id` + `appears_in_shots`.
  (2) sala-limpia/champions-style: characters con `anchor_image_id` + shots con
      `anchor_id_required: {rol: "anchor_id"}`. Un anchor_id en ≥2 shots → needed.

Capability-gate: --format requerido (agnostic-by-design). has_ai_generated_clips=false →
not_applicable (sin clips AI no hay batch i2v que romper). video_capabilities ausente → Bug #9.

Exit: 0 PASS / 0 not_applicable / 1 FAIL (anchors faltantes) / 2 can't-measure.

DISEÑO TESTEABLE: la decisión vive en la función PURA evaluate_anchor_coverage(needed, present);
el runtime solo parsea el SPEC (derive_needed_anchors) y lista archivos (list_present_anchors).

Authority: HR#26 (test adversarial companion por script) + CLAUDE.md § Pre-render gate
(CP1 anchors → CP4 animation $) + feedback_per_clip_atomic_assembly (FileNotFoundError mid-batch).
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: pyyaml not installed", file=sys.stderr)
    sys.exit(2)

ANCHOR_EXTENSIONS = (".png", ".jpg", ".jpeg", ".webp")


# ─────────────────────────────────────────────────────────────────────────────
# PURE function — the decision. No filesystem, no SPEC parsing. Easy to test.
# ─────────────────────────────────────────────────────────────────────────────
def evaluate_anchor_coverage(needed, present):
    """Decide coverage from already-extracted data.

    needed:  iterable of anchor ids that MUST have a generated file.
    present: iterable of anchor ids that DO have a file on disk.
    Returns (ok: bool, missing: list[str] sorted) — ok iff every needed id is present.
    """
    needed_set = {n for n in needed if n}
    present_set = {p for p in present if p}
    missing = sorted(needed_set - present_set)
    return (len(missing) == 0, missing)


# ─────────────────────────────────────────────────────────────────────────────
# Runtime extraction — parse SPEC into the data the pure function consumes.
# ─────────────────────────────────────────────────────────────────────────────
def derive_needed_anchors(spec):
    """Return (needed: sorted list[str], reasons: dict[id] -> why) from a parsed SPEC.

    An anchor id is NEEDED if either:
      (a) declared in reference_anchors (characters/settings/props), OR
      (b) appears in >1 shot — derived from:
            - reference_anchors entry `appears_in_shots` (>1 entry), and/or
            - shot_list `anchor_id_required` values seen in ≥2 shots.
    Single-shot, undeclared appearances are intentionally NOT required.
    """
    reasons = {}

    # (a) + (b-via-appears_in_shots): top-level reference_anchors block (matadero dialect).
    ref = spec.get("reference_anchors") or {}
    if isinstance(ref, dict):
        for category in ("characters", "settings", "props"):
            for entry in ref.get(category) or []:
                if not isinstance(entry, dict):
                    continue
                aid = entry.get("id")
                if not aid:
                    continue
                reasons[aid] = f"declared in reference_anchors.{category}"
                appears = entry.get("appears_in_shots") or []
                if isinstance(appears, list) and len(appears) > 1:
                    reasons[aid] = (
                        f"declared in reference_anchors.{category} (appears in {len(appears)} shots)"
                    )

    # (b) shot_list anchor_id_required (sala-limpia / champions dialect): count appearances.
    appear_counts = {}
    for s in spec.get("shot_list") or []:
        if not isinstance(s, dict):
            continue
        req = s.get("anchor_id_required") or {}
        if isinstance(req, dict):
            ids = req.values()
        elif isinstance(req, list):
            ids = req
        else:
            ids = []
        for aid in ids:
            if aid:
                appear_counts[aid] = appear_counts.get(aid, 0) + 1
    for aid, count in appear_counts.items():
        if count > 1 and aid not in reasons:
            reasons[aid] = f"appears in {count} shots (anchor_id_required)"
        elif aid not in reasons:
            # single-shot AND not declared → not required (skip). But if it IS
            # declared elsewhere (anchor_image_id below), it stays out of here.
            pass

    return sorted(reasons), reasons


def list_present_anchors(anchors_dir):
    """Return the set of anchor ids (filename stems) present in anchors_dir.

    Stems are normalized for the common 'attempt'/'_hand'/'_audit' variants are NOT
    collapsed — we match by exact stem so a precise <id>.png is required (the i2v batch
    references the exact filename). Returns set[str]."""
    present = set()
    p = Path(anchors_dir)
    if not p.is_dir():
        return present
    for f in p.iterdir():
        if f.is_file() and f.suffix.lower() in ANCHOR_EXTENSIONS:
            present.add(f.stem)
    return present


def resolve_anchors_dir(project_dir, spec):
    """Where the SPEC expects anchor files. Canonical: <project>/assets/anchors.
    SPEC may override via reference_anchors.anchors_dir (forward-compat)."""
    ref = spec.get("reference_anchors") or {}
    override = ref.get("anchors_dir") if isinstance(ref, dict) else None
    if override:
        cand = Path(override)
        return cand if cand.is_absolute() else Path(project_dir) / override
    return Path(project_dir) / "assets" / "anchors"


def main():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--format", required=True, help="delivery/genre format (capability gate)")
    parser.add_argument("--spec", required=True)
    parser.add_argument(
        "--project-dir", required=True, help="project root (anchors expected in <project-dir>/assets/anchors)"
    )
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    spec_path = Path(args.spec)
    if not spec_path.exists():
        print(f"ERROR: SPEC not found: {spec_path}", file=sys.stderr)
        return 2

    with open(spec_path) as f:
        spec = yaml.safe_load(f) or {}

    caps = spec.get("video_capabilities")
    if caps is None:
        print(
            "ERROR: SPEC missing 'video_capabilities' block (Pattern 7 §1.6 mandatory). Bug #9.",
            file=sys.stderr,
        )
        return 2

    has_ai_clips = bool(caps.get("has_ai_generated_clips", False))

    if args.dry_run:
        print(
            f"format: {args.format}\nspec: {spec_path}\nhas_ai_generated_clips: {has_ai_clips}\n"
            f"branch: {'anchor_coverage_check' if has_ai_clips else 'not_applicable'}"
        )
        return 0

    if not has_ai_clips:
        print(
            json.dumps(
                {
                    "format": args.format,
                    "overall_status": "not_applicable",
                    "detail": "has_ai_generated_clips=false → no i2v batch to break on a missing anchor",
                },
                indent=2,
                ensure_ascii=False,
            )
        )
        return 0

    needed, reasons = derive_needed_anchors(spec)
    anchors_dir = resolve_anchors_dir(args.project_dir, spec)
    present = list_present_anchors(anchors_dir)

    ok, missing = evaluate_anchor_coverage(needed, present)

    report = {
        "format": args.format,
        "spec": str(spec_path),
        "anchors_dir": str(anchors_dir),
        "anchors_dir_exists": Path(anchors_dir).is_dir(),
        "overall_status": "pass" if ok else "fail",
        "overall_pass": ok,
        "needed_count": len(needed),
        "present_count": len(present),
        "missing": [{"anchor_id": m, "reason": reasons.get(m, "needed")} for m in missing],
        "needed": needed,
        "present": sorted(present),
    }
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
