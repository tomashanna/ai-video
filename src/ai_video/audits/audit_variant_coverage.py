#!/usr/bin/env python3
"""audit-variant-coverage.py — HR#5 duration-driven image variety gate.

BUG REAL que cierra (caso disparador bosque-v2): el video shipeó "PowerPoint
narrado" — UN solo PNG reusado para una escena de ~11s on-screen. HR#5 exige
≥2 variantes de TIPO de plano distinto en cualquier shot con >4s on-screen
(IMAGE-VARIETY.md § "Cuándo generar variantes": ≤4s → 1, 4-8s → 2, >8s → 3).

POR QUÉ NO LO CAZABA NADIE:
  `audit-spec-completeness.py` cuenta EXISTENCIA de assets (¿el PNG está en disco
  / declarado en asset_list?) pero NO razona sobre DURACIÓN on-screen por shot. Un
  shot de 11s con 1 PNG pasa "completeness" perfecto.
  Un check INGENUO contaría variantes "por caption" — y como cada caption dura
  2-3s, 4 captions del mismo shot parecen "compliant" (≤4s c/u) aunque sumen 11s
  con UN solo plano. IMAGE-VARIETY.md § 23 lo dice explícito: contar la duración
  TOTAL que la escena ocupa, NO la de cada caption. Por eso acá contamos POR SHOT
  (su duración on-screen agregada), nunca per-caption.

REGLA (por shot del shot_list):
  onscreen_s = (timestamp_intent_s[1]-[0]) si existe, si no duration_intent_s.
  n_variants  = max(declarado en SPEC: image_variants/n_variants/variant_count,
                    contado en assets/: shot_NN.png[base=1] + shot_NN-a/-b/-c.png).
  onscreen_s > 4.0  AND  n_variants < 2  →  FAIL (riesgo PowerPoint-narrado),
  nombrando el shot + su duración + variantes encontradas.
  onscreen_s ≤ 4.0  → regla NO aplica (PASS aunque tenga 1 variante).

Capability-gate: has_ai_generated_clips false → not_applicable (exit 0). Sin
clips AI generados no hay "PowerPoint" que prevenir.
video_capabilities ausente → Bug #9 (exit 2). Agnostic-by-design: --format REQUIRED.

DISEÑO TESTEABLE: lógica pura en evaluate_variant_coverage(shots) — recibe shots
ya extraídos [{shot_id, onscreen_s, n_variants}]; el wrapper runtime parsea SPEC +
cuenta variantes en disco.

Exit: 0 PASS / not_applicable · 1 FAIL · 2 can't-measure (Bug #9 / SPEC ausente).
Authority: HARD-RULES.md HR#5 + ai-video-production/IMAGE-VARIETY.md. HR#26 companion test.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: pyyaml not installed", file=sys.stderr)
    sys.exit(2)

ONSCREEN_THRESHOLD_S = 4.0  # HR#5 / IMAGE-VARIETY.md: >4s on-screen → ≥2 variantes
MIN_VARIANTS = 2  # variantes de TIPO de plano distinto


def evaluate_variant_coverage(shots, *, threshold_s=ONSCREEN_THRESHOLD_S, min_variants=MIN_VARIANTS):
    """PURE. shots = [{shot_id, onscreen_s, n_variants}, ...].

    Devuelve (ok: bool, reasons: list[dict]). FAIL si algún shot con
    onscreen_s > threshold_s tiene n_variants < min_variants (PowerPoint-narrado).
    Cuenta POR SHOT (la duración on-screen agregada del shot) — NO per-caption,
    que es como un check ingenuo se vería falsamente compliant.
    """
    reasons = []
    ok = True
    for s in shots:
        sid = s.get("shot_id", "?")
        try:
            onscreen = float(s.get("onscreen_s") or 0.0)
        except (TypeError, ValueError):
            onscreen = 0.0
        try:
            n = int(s.get("n_variants") or 0)
        except (TypeError, ValueError):
            n = 0
        if onscreen <= threshold_s:
            reasons.append(
                {
                    "shot_id": sid,
                    "onscreen_s": round(onscreen, 2),
                    "n_variants": n,
                    "status": "ok",
                    "rule_applies": False,
                    "detail": f"on-screen {onscreen:.1f}s ≤ {threshold_s}s → variantes no requeridas",
                }
            )
            continue
        if n < min_variants:
            ok = False
            reasons.append(
                {
                    "shot_id": sid,
                    "onscreen_s": round(onscreen, 2),
                    "n_variants": n,
                    "status": "fail",
                    "rule_applies": True,
                    "detail": (
                        f"shot '{sid}' on-screen {onscreen:.1f}s > {threshold_s}s con SOLO {n} "
                        f"variante(s) — HR#5 exige ≥{min_variants} TIPOS de plano distintos "
                        f"(riesgo PowerPoint-narrado: 1 PNG reusado en escena larga)"
                    ),
                }
            )
        else:
            reasons.append(
                {
                    "shot_id": sid,
                    "onscreen_s": round(onscreen, 2),
                    "n_variants": n,
                    "status": "ok",
                    "rule_applies": True,
                    "detail": f"on-screen {onscreen:.1f}s > {threshold_s}s con {n} variantes ✓",
                }
            )
    return ok, reasons


def shot_onscreen_seconds(shot):
    """Extrae duración on-screen de un shot del SPEC. Prefiere timestamp_intent_s
    [start,end] (end-start); fallback a duration_intent_s. Devuelve float o 0.0."""
    ts = shot.get("timestamp_intent_s")
    if isinstance(ts, (list, tuple)) and len(ts) == 2:
        try:
            return max(0.0, float(ts[1]) - float(ts[0]))
        except (TypeError, ValueError):
            pass
    d = shot.get("duration_intent_s")
    try:
        return float(d) if d is not None else 0.0
    except (TypeError, ValueError):
        return 0.0


def count_variants(shot, assets_dir):
    """n_variants = max(declarado-en-SPEC, contado-en-disco).

    SPEC: campos image_variants (lista o int) / n_variants / variant_count.
    Disco: base shot_NN.{png,jpg,jpeg,webp} cuenta como variante 1; sufijos
    -a/-b/-c suman. Si NO hay base pero SÍ sufijos, cada sufijo cuenta."""
    sid = str(shot.get("shot_id", "")).strip()
    declared = 0
    iv = shot.get("image_variants")
    if isinstance(iv, list):
        declared = len(iv)
    elif isinstance(iv, int):
        declared = iv
    for k in ("n_variants", "variant_count"):
        v = shot.get(k)
        if isinstance(v, int):
            declared = max(declared, v)

    on_disk = 0
    if sid and assets_dir and Path(assets_dir).is_dir():
        exts = ("png", "jpg", "jpeg", "webp")
        base_re = re.compile(rf"^{re.escape(sid)}\.(?:{'|'.join(exts)})$", re.IGNORECASE)
        var_re = re.compile(rf"^{re.escape(sid)}-[a-z]\.(?:{'|'.join(exts)})$", re.IGNORECASE)
        base = sum(1 for f in Path(assets_dir).iterdir() if base_re.match(f.name))
        variants = sum(1 for f in Path(assets_dir).iterdir() if var_re.match(f.name))
        # base cuenta como variante 1 (es un plano); sufijos son planos adicionales.
        on_disk = base + variants
    return max(declared, on_disk)


def main():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--format", required=True)
    parser.add_argument("--spec", required=True)
    parser.add_argument(
        "--assets-dir",
        default=None,
        help="dir con clips/imágenes (-a/-b/-c). Default: <spec_dir>/../<project>/assets/clips si existe.",
    )
    parser.add_argument("--threshold-s", type=float, default=ONSCREEN_THRESHOLD_S)
    parser.add_argument("--min-variants", type=int, default=MIN_VARIANTS)
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

    has_clips = bool(caps.get("has_ai_generated_clips", False))
    if args.dry_run:
        print(
            f"format: {args.format}\nspec: {spec_path}\nhas_ai_generated_clips: {has_clips}\n"
            f"branch: {'variant_coverage_check' if has_clips else 'not_applicable'}\n"
            f"threshold_s: {args.threshold_s}, min_variants: {args.min_variants}"
        )
        return 0

    if not has_clips:
        print(
            json.dumps(
                {
                    "format": args.format,
                    "overall_status": "not_applicable",
                    "detail": "has_ai_generated_clips=false → variant coverage check skipped (no AI clips to vary)",
                },
                indent=2,
                ensure_ascii=False,
            )
        )
        return 0

    assets_dir = args.assets_dir
    if assets_dir is None:
        # Heurística: assets/clips del proyecto hermano del spec (no obligatorio — si no existe, se cuenta SPEC).
        guess = spec_path.parent.parent / spec_path.stem / "assets" / "clips"
        if guess.is_dir():
            assets_dir = str(guess)

    shot_list = spec.get("shot_list") or []
    shots = []
    for s in shot_list:
        if not isinstance(s, dict):
            continue
        shots.append(
            {
                "shot_id": s.get("shot_id", "?"),
                "onscreen_s": shot_onscreen_seconds(s),
                "n_variants": count_variants(s, assets_dir),
            }
        )

    ok, reasons = evaluate_variant_coverage(
        shots, threshold_s=args.threshold_s, min_variants=args.min_variants
    )

    fails = [r for r in reasons if r["status"] == "fail"]
    report = {
        "format": args.format,
        "spec": str(spec_path),
        "assets_dir": assets_dir,
        "threshold_s": args.threshold_s,
        "min_variants": args.min_variants,
        "overall_status": "pass" if ok else "fail",
        "overall_pass": ok,
        "shots_checked": len(shots),
        "rule_applied_to": sum(1 for r in reasons if r["rule_applies"]),
        "fail_shots": fails,
        "shots": reasons,
    }
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
