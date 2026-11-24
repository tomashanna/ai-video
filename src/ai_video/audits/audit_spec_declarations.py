#!/usr/bin/env python3
"""audit-spec-declarations.py — gate parametrizado de 4 campos del SPEC (Q26/Q27/Q28/Q22b).

UN solo script que consolida 4 checks de DECLARACIÓN de campos del CREATIVE-SPEC que
hoy viven como manual_checklist (clasificación 2026-06-04: "un solo script parametrizado
cubriría Q26/Q27/Q28/Q22b"). Cada check activable/desactivable por flag (--checks).

BUG REAL que cierra (casos disparadores):
  · Q26 (caso matadero post-ship 2026-05-20, GAP #23): el video shipeó con setting MUERTO —
    carnes colgando estáticas, paredes, equipo sin UN solo elemento de background animado.
    Los refs canónicos 100% tienen AL MENOS UNA criatura/objeto de background en movimiento
    (ref-03 tiburón, ref-01 haz de luz, ref-08 glow de Miro, ref-10 fuego del horno). El SPEC
    debe DECLARAR per shot un setting_ambient_creature_or_object no-vacío.
  · Q27 (GAP #26): shots con atmospheric_motions_count <3 (o lista que NO matchea el count
    declarado) → background pobre + drift count↔list. El SPEC debe declarar ≥3 motions Y que
    la lista TENGA exactamente esos N elementos (no count=4 con lista de 2).
  · Q28 (GAP #25): SPEC con TODOS los shots static (pov_traversal/motion_type static) → el
    "PowerPoint narrado" en movimiento de cámara: cero traversal, cero recorrido. La regla es
    ALL-STATIC (no per-shot): un freeze de decisión static es legítimo, un SPEC entero static no.
  · Q22b (HR#19 — "NEVER ESTIMATE, ALWAYS MEASURE"): el SPEC declara métricas de pacing
    (WPM/cuts) tomadas de NUESTRAS PROPIAS producciones (canonical_validation_status:
    deprecated_our_prod_only) como si fueran autoridad → score inflado (caso pueblo-v2 Gemini
    9.9 vs 7/10 real). canonical_validation_status DEBE ser explícito y ∈ {pending_video_measurement,
    validated_via_perceptual_test, validated_via_video_measurement}; deprecated_our_prod_only = FAIL.

POR QUÉ NO LO CAZABA NADIE:
  audit-spec-completeness.py cuenta EXISTENCIA de assets y audit-spec-structure-vs-canonical.py
  mide la ESTRUCTURA de la familia choice — ninguno razona sobre la PRESENCIA + el CONTENIDO de
  estos 4 campos declarativos por shot. Vivían como Y/N de un checklist humano (manual_checklist),
  que es exactamente el tipo de chequeo que el ojo se saltea bajo presión de tiempo (los 31 shots
  del SPEC se revisan a mano = nadie verifica count==list en cada uno). Gemini holístico tampoco
  los ve: son metadata del SPEC, no del render.

REGLA (por shot del shot_list, salvo Q28 que es all-static y Q22b que es del bloque de pacing):
  · Q26: setting_ambient_creature_or_object presente y no-vacío en CADA shot (GAP #23).
  · Q27: visual_action_match.atmospheric_motions_count ≥3  Y  len(atmospheric_motions_list)==count
         en CADA shot (GAP #26).
  · Q28: pov_traversal (o motion_type fallback) NO puede ser static en TODOS los shots — FAIL solo
         si el SPEC ENTERO es static (GAP #25). Per-shot static es legítimo.
  · Q22b: canonical_validation_status del bloque de pacing presente y ∈ {pending_video_measurement,
          validated_via_perceptual_test, validated_via_video_measurement}; FAIL si
          deprecated_our_prod_only o ausente (HR#19).

Capability-gate (Pattern 7): Q26 gatea por familia choice — --format ∈ CHOICE_FAMILY O el campo
setting_ambient_creature_or_object presente en ≥1 shot (señal de que el SPEC lo usa). Si ni una ni
otra → Q26 not_applicable. Los otros 3 checks aplican a cualquier SPEC con shot_list.
video_capabilities ausente → Bug #9 (exit 2). Agnostic-by-design: --format REQUERIDO.

DISEÑO TESTEABLE: lógica PURA en evaluate_q26/q27/q28/q22b(...) que reciben datos ya extraídos
(listas de shots {shot_id, ...} o el dict de pacing) — testeables sin filesystem. El wrapper runtime
parsea el SPEC y arma esas estructuras.

Exit: 0 PASS·not_applicable / 1 FAIL / 2 can't-measure (Bug #9 / SPEC ausente / pyyaml ausente).
Authority: creative-director/master-flow-v2/GAPS-LOG.md GAP #23/#25/#26 + CLAUDE.md HR#19
  (NEVER ESTIMATE, ALWAYS MEASURE) + ai-video-production SPEC schema v9+ (setting_ambient per shot).
  HR#26 companion test: test_audit-spec-declarations.py.
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

# ── Constantes con autoridad ──────────────────────────────────────────────────────────────────
# NO medidas en F1 (son reglas estructurales del SPEC, no bandas empíricas del render) →
# constantes de módulo. Authority: GAPS-LOG.md GAP #26 + CLAUDE.md HR#19.
MIN_ATMOSPHERIC_MOTIONS = 3   # GAP #26: ≥3 atmospheric motions por shot. Override via --min-motions.

# HR#19 — estados de validación canónica VÁLIDOS. deprecated_our_prod_only es el ANTI-PATTERN.
VALID_CANONICAL_VALIDATION_STATUS = (
    "pending_video_measurement",
    "validated_via_perceptual_test",
    "validated_via_video_measurement",
)
DEPRECATED_VALIDATION_STATUS = "deprecated_our_prod_only"

# Familia choice (Q26 gatea por esto — alineado a audit-spec-structure-vs-canonical.py).
CHOICE_FAMILY = ("horror-choice", "sport-choice")

# Tokens que cuentan como "static" para Q28 (pov_traversal / motion_type). All-static = FAIL.
# static_with_micro_bob ES static (micro-bob no es traversal). "static" exacto también.
STATIC_TOKENS = ("static", "static_with_micro_bob", "freeze", "frozen", "none")

ALL_CHECKS = ("q26", "q27", "q28", "q22b")


def gate(name, status, detail, **extra):
    """Resultado de un check: status ∈ pass | fail | not_applicable."""
    d = {"check": name, "status": status, "detail": detail}
    d.update(extra)
    return d


# ════════════════════════════════════════════════════════════════════════════════════════════
# LÓGICA PURA — testeables sin filesystem
# ════════════════════════════════════════════════════════════════════════════════════════════

def evaluate_q26(shots, *, format_in_family, field_present_in_any):
    """Q26 PURO. shots = [{shot_id, ambient}]. ambient = string (o None) por shot.

    Capability-gate: si NO es familia choice Y el campo no aparece en ningún shot →
    not_applicable. Si aplica: FAIL si algún shot tiene ambient vacío/ausente (GAP #23)."""
    if not format_in_family and not field_present_in_any:
        return gate("q26_setting_ambient_creature_or_object", "not_applicable",
                    "formato fuera de la familia choice Y setting_ambient_creature_or_object ausente "
                    "en todos los shots → el SPEC no usa este campo (GAP #23 no aplica)")
    offenders = []
    for s in shots:
        amb = s.get("ambient")
        if amb is None or not str(amb).strip():
            offenders.append(s.get("shot_id", "?"))
    if offenders:
        return gate("q26_setting_ambient_creature_or_object", "fail",
                    (f"{len(offenders)}/{len(shots)} shot(s) sin setting_ambient_creature_or_object "
                     f"no-vacío (GAP #23 — setting MUERTO: refs canónicos 100% tienen ≥1 elemento de "
                     f"background animado por shot): {offenders}"),
                    offender_shots=offenders)
    return gate("q26_setting_ambient_creature_or_object", "pass",
                f"{len(shots)}/{len(shots)} shots declaran un setting_ambient_creature_or_object no-vacío ✓")


def evaluate_q27(shots, *, min_motions=MIN_ATMOSPHERIC_MOTIONS):
    """Q27 PURO. shots = [{shot_id, motions_count, motions_list_len}].

    FAIL si algún shot tiene count < min_motions O len(list) != count (GAP #26)."""
    offenders = []
    for s in shots:
        sid = s.get("shot_id", "?")
        count = s.get("motions_count")
        list_len = s.get("motions_list_len")
        problems = []
        try:
            count_i = int(count)
        except (TypeError, ValueError):
            count_i = None
        if count_i is None:
            problems.append("atmospheric_motions_count ausente/no-numérico")
        elif count_i < min_motions:
            problems.append(f"count {count_i} < min {min_motions}")
        if list_len is None:
            problems.append("atmospheric_motions_list ausente")
        elif count_i is not None and list_len != count_i:
            problems.append(f"len(list)={list_len} != count={count_i} (drift count↔list)")
        if problems:
            offenders.append({"shot_id": sid, "problems": problems})
    if offenders:
        return gate("q27_atmospheric_motions", "fail",
                    (f"{len(offenders)}/{len(shots)} shot(s) violan GAP #26 (≥{min_motions} motions Y "
                     f"len(list)==count): {[o['shot_id'] for o in offenders]}"),
                    offender_shots=offenders, min_motions=min_motions)
    return gate("q27_atmospheric_motions", "pass",
                f"{len(shots)}/{len(shots)} shots con ≥{min_motions} atmospheric motions Y len(list)==count ✓",
                min_motions=min_motions)


def evaluate_q28(shots):
    """Q28 PURO. shots = [{shot_id, traversal}]. traversal = string normalizado (lower).

    FAIL solo si TODOS los shots son static (GAP #25 — el check es all-static, NO per-shot).
    Un freeze static aislado es legítimo; un SPEC entero sin traversal no lo es."""
    if not shots:
        return gate("q28_not_all_static", "not_applicable",
                    "shot_list vacío → no hay traversal que evaluar")
    non_static = []
    static = []
    for s in shots:
        t = str(s.get("traversal") or "").strip().lower()
        if t and t not in STATIC_TOKENS:
            non_static.append(s.get("shot_id", "?"))
        else:
            static.append(s.get("shot_id", "?"))
    if not non_static:
        return gate("q28_not_all_static", "fail",
                    (f"TODOS los {len(shots)} shots son static (pov_traversal/motion_type ∈ "
                     f"{STATIC_TOKENS}) — GAP #25: cero traversal en todo el SPEC = PowerPoint narrado "
                     f"sin recorrido"),
                    static_shots=static)
    return gate("q28_not_all_static", "pass",
                (f"{len(non_static)}/{len(shots)} shot(s) con traversal real (no all-static) ✓ — "
                 f"ej: {non_static[:5]}"),
                non_static_count=len(non_static), static_count=len(static))


def evaluate_q22b(status_value, *, field_found):
    """Q22b PURO. status_value = string del canonical_validation_status (o None si no se halló).

    FAIL si deprecated_our_prod_only o ausente (HR#19 — no estimación de nuestras prod como
    autoridad). PASS si ∈ VALID_CANONICAL_VALIDATION_STATUS."""
    if not field_found or status_value is None:
        return gate("q22b_canonical_validation_status", "fail",
                    ("canonical_validation_status AUSENTE en el bloque de pacing (narrative_pacing / "
                     "editing_targets / pacing top-level) — HR#19 exige declararlo explícito ∈ "
                     f"{list(VALID_CANONICAL_VALIDATION_STATUS)}; sin él, las métricas de pacing no "
                     "tienen procedencia validada (riesgo de tratar nuestras prod como autoridad)"),
                    field_found=field_found)
    val = str(status_value).strip()
    if val == DEPRECATED_VALIDATION_STATUS:
        return gate("q22b_canonical_validation_status", "fail",
                    (f"canonical_validation_status = '{DEPRECATED_VALIDATION_STATUS}' — HR#19 PROHÍBE "
                     "usar nuestras propias producciones como autoridad técnica (caso pueblo-v2: "
                     "Gemini 9.9 vs 7/10 real). Re-medir contra referentes o test perceptual."),
                    value=val)
    if val in VALID_CANONICAL_VALIDATION_STATUS:
        return gate("q22b_canonical_validation_status", "pass",
                    f"canonical_validation_status = '{val}' ∈ válidos ✓", value=val)
    return gate("q22b_canonical_validation_status", "fail",
                (f"canonical_validation_status = '{val}' NO ∈ {list(VALID_CANONICAL_VALIDATION_STATUS)} "
                 "(valor desconocido — HR#19)"),
                value=val)


# ════════════════════════════════════════════════════════════════════════════════════════════
# EXTRACCIÓN — runtime (parsea el SPEC y arma las estructuras puras)
# ════════════════════════════════════════════════════════════════════════════════════════════

def extract_shots(spec):
    """shot_list[] → solo los dicts con shot_id (filtra basura). Devuelve [dict, ...]."""
    out = []
    for s in spec.get("shot_list") or []:
        if isinstance(s, dict) and s.get("shot_id"):
            out.append(s)
    return out


def shot_ambient(shot):
    """setting_ambient_creature_or_object del shot (string o None)."""
    return shot.get("setting_ambient_creature_or_object")


def shot_motions(shot):
    """(count, list_len) de visual_action_match.atmospheric_motions_*. list_len=None si no es lista."""
    vam = shot.get("visual_action_match") or {}
    if not isinstance(vam, dict):
        vam = {}
    count = vam.get("atmospheric_motions_count")
    lst = vam.get("atmospheric_motions_list")
    list_len = len(lst) if isinstance(lst, (list, tuple)) else None
    return count, list_len


def shot_traversal(shot):
    """pov_traversal del shot, fallback a motion_type. String o ''."""
    return shot.get("pov_traversal") or shot.get("motion_type") or ""


def find_canonical_validation_status(spec):
    """Busca canonical_validation_status en los bloques de pacing plausibles, en orden:
    narrative_pacing → editing_targets → pacing → top-level del SPEC.

    Devuelve (value, found_bool, where). El SPEC v11 lo aloja donde viva el pacing; no inventamos
    un path único — probamos los candidatos reales y reportamos dónde (o que no está)."""
    candidates = ("narrative_pacing", "editing_targets", "pacing")
    for key in candidates:
        block = spec.get(key)
        if isinstance(block, dict) and "canonical_validation_status" in block:
            return block.get("canonical_validation_status"), True, key
    if "canonical_validation_status" in spec:
        return spec.get("canonical_validation_status"), True, "<top-level>"
    return None, False, None


# ════════════════════════════════════════════════════════════════════════════════════════════
# RUNTIME
# ════════════════════════════════════════════════════════════════════════════════════════════

def parse_checks(raw):
    """--checks q26,q27 → ('q26','q27'). 'all' → ALL_CHECKS. Valida nombres."""
    if not raw or raw.strip().lower() == "all":
        return ALL_CHECKS
    picked = tuple(c.strip().lower() for c in raw.split(",") if c.strip())
    bad = [c for c in picked if c not in ALL_CHECKS]
    if bad:
        raise ValueError(f"checks desconocidos: {bad} (válidos: {list(ALL_CHECKS)} | all)")
    return picked


def run_checks(spec, fmt, checks, *, min_motions=MIN_ATMOSPHERIC_MOTIONS):
    """Corre los checks pedidos contra un SPEC ya parseado. Devuelve lista de gate-dicts.

    Semi-puro: recibe el spec dict (no filesystem). Usado por el runtime y los tests."""
    shots = extract_shots(spec)
    results = []

    if "q26" in checks:
        ambient_shots = [{"shot_id": s.get("shot_id"), "ambient": shot_ambient(s)} for s in shots]
        field_present_in_any = any(
            sh["ambient"] is not None and str(sh["ambient"]).strip() for sh in ambient_shots
        ) or any("setting_ambient_creature_or_object" in s for s in shots)
        format_in_family = fmt in CHOICE_FAMILY
        results.append(evaluate_q26(
            ambient_shots, format_in_family=format_in_family,
            field_present_in_any=field_present_in_any))

    if "q27" in checks:
        motion_shots = []
        for s in shots:
            count, list_len = shot_motions(s)
            motion_shots.append({
                "shot_id": s.get("shot_id"), "motions_count": count, "motions_list_len": list_len})
        results.append(evaluate_q27(motion_shots, min_motions=min_motions))

    if "q28" in checks:
        trav_shots = [{"shot_id": s.get("shot_id"), "traversal": shot_traversal(s)} for s in shots]
        results.append(evaluate_q28(trav_shots))

    if "q22b" in checks:
        value, found, where = find_canonical_validation_status(spec)
        res = evaluate_q22b(value, field_found=found)
        res["pacing_block_searched"] = where if where else "none (narrative_pacing/editing_targets/pacing/top-level)"
        results.append(res)

    return results


def main():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--format", required=True,
                        help="formato del SPEC (agnostic-by-design — gatea Q26 por familia choice)")
    parser.add_argument("--spec", required=True, help="path al CREATIVE-SPEC.yaml")
    parser.add_argument("--checks", default="all",
                        help="checks a correr, coma-separados: q26,q27,q28,q22b (default: all)")
    parser.add_argument("--min-motions", type=int, default=MIN_ATMOSPHERIC_MOTIONS,
                        help=f"override del mínimo de atmospheric motions de Q27 (default {MIN_ATMOSPHERIC_MOTIONS})")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    try:
        checks = parse_checks(args.checks)
    except ValueError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 2

    spec_path = Path(args.spec)
    if not spec_path.exists():
        print(f"ERROR: SPEC not found: {spec_path}", file=sys.stderr)
        return 2

    with open(spec_path) as f:
        spec = yaml.safe_load(f) or {}

    caps = spec.get("video_capabilities")
    if caps is None:
        print("ERROR: SPEC missing 'video_capabilities' block (Pattern 7 §1.6 mandatory). Bug #9.",
              file=sys.stderr)
        return 2

    if args.dry_run:
        print(f"format: {args.format}\nspec: {spec_path}\nchecks: {list(checks)}\n"
              f"min_motions: {args.min_motions}\nshots: {len(extract_shots(spec))}")
        return 0

    results = run_checks(spec, args.format, checks, min_motions=args.min_motions)

    fails = [r for r in results if r["status"] == "fail"]
    overall_ok = not fails
    report = {
        "format": args.format, "spec": str(spec_path),
        "checks_run": list(checks),
        "overall_status": "pass" if overall_ok else "fail",
        "overall_pass": overall_ok,
        "fail_count": len(fails),
        "checks": results,
    }
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if overall_ok else 1


if __name__ == "__main__":
    sys.exit(main())
