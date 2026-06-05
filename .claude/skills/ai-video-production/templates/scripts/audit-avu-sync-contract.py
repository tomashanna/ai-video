#!/usr/bin/env python3
"""audit-avu-sync-contract.py — HR#25 / Q24 AVU + sync_contract gate (compose-time fragility).

BUG REAL que cierra (caso disparador matadero iter 3-4): los elementos audio-visual
ACOPLADOS (countdown 3-2-1 con su tick, freeze-de-decisión con su sting, diálogo
lip-sync, hook-transition flash+whoosh, outro card + drone) se ARMABAN a compose-time
con GSAP timing + data-start CSS + wiring del mix de audio. Ese acople tiene MÚLTIPLES
puntos de falla (race conditions del timeline, data-start vs segmento de audio, etc.) →
en matadero iter 3-4 el countdown/diálogo se DESINCRONIZABA al componer. El principio
AVU (PAUTA § 19 + INGENIERO-PAUTA § 7.11): un elemento acoplado debe ser O un .mp4
pre-renderizado con el audio YA bundleado (1 solo punto de falla = bullet-proof) O,
si su texto/audio varía per-video y no es AVU-able, un sync_contract EXPLÍCITO declarado
en el SPEC (visual_start_s + audio_start_s + tolerance_s) que se valide pre-render.

POR QUÉ NO LO CAZABA NADIE:
  Q24 del pre-render-gate es HOY un check MANUAL (Y/N humano) — exactamente el tipo de
  verificación que el ojo se saltea bajo presión: hay que cruzar, shot por shot, qué
  shots tienen audio+visual acoplados contra si cada uno tiene su AVU .mp4 EN DISCO o su
  sync_contract COMPLETO. Los otros gates no lo ven: audit-spec-completeness cuenta
  EXISTENCIA de assets pero no razona sobre el ACOPLE audio-visual; audit-clip-timing
  mide A/V drift del render YA armado (tarde — el daño ya está); Gemini holístico ve el
  frame, no el contrato de sync del SPEC. El acople es metadata del SPEC + presencia de
  .mp4, no algo perceptible en 1 frame.

REGLA (por shot del shot_list con audio+visual ACOPLADOS):
  Un shot está ACOPLADO si declara CUALQUIERA de (campos reales del schema v11):
    · audio_visual_atomic_units (lista — § 7.11.4 canonical), O
    · avu_overlay_clip no-null (se overlaya un AVU pre-rendered sobre el shot), O
    · has_lip_sync_required: true (diálogo de personaje lip-sync = audio↔visual acoplado), O
    · sync_contract presente (bloque explícito).
  Shot ACOPLADO PASA si CUALQUIERA:
    (a) AVU pre-rendered .mp4 EXISTE en disco — el path declarado (avu_overlay_clip /
        audio_visual_atomic_units[].asset_path) resuelto contra la avu-library O el
        proyecto; para lip-sync el satisfier es el clip atomic .mp4 (audio bundleado
        Layer 1) en clips-atomic/. Se verifica con stat (HR#19 — MEASURE, no asumir).
    (b) sync_contract EXPLÍCITO COMPLETO: visual_start_s + audio_start_s + tolerance_s
        (o el bloque contract de un audio_visual_atomic_units[].type == sync_contract).
  FAIL si shot acoplado SIN (a) ni (b).
  Shot NO-acoplado → la regla no aplica (PASS).
  SPEC sin NINGÚN shot acoplado → not_applicable (exit 0).

Capability-gate (Pattern 7): has_ai_generated_clips false → not_applicable (exit 0) — sin
clips AI generados no hay compose-time fragility del acople AVU que prevenir.
video_capabilities ausente → Bug #9 (exit 2). Agnostic-by-design: --format REQUERIDO.

DISEÑO TESTEABLE: lógica PURA en evaluate_avu_sync_contract(shots) — recibe shots ya
extraídos [{shot_id, coupled, coupling_reasons, avu_present, has_complete_sync_contract}];
el wrapper runtime parsea el SPEC, resuelve los paths de AVU contra disco (stat) y arma
esas estructuras. La función pura no toca filesystem.

Banda empírica: N/A — la tolerance_s del sync_contract NO es una banda medida en F1, es
un campo de CONTRATO que el arquitecto declara. Authority del valor de referencia =
INGENIERO-PAUTA § 7.11.4 (ejemplo tolerance_s 0.1) — NO medida en F1. El gate NO impone un
valor de tolerance, solo exige que los 3 campos del contrato ESTÉN presentes (override del
set de campos requeridos vía --require-contract-fields).

Exit: 0 PASS·not_applicable / 1 FAIL / 2 can't-measure (Bug #9 / SPEC ausente / pyyaml).
Authority: pre-render-gate/SKILL.md Q24 + horror-choice-format/INGENIERO-PAUTA-MASTER § 7.11
  (AVU library + sync_contract § 7.11.4) + PAUTA-MASTER § 19 AVU principle + CLAUDE.md HR#25.
  HR#26 companion test: test_audit-avu-sync-contract.py.
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
# Campos requeridos del sync_contract. NO medidos en F1 (son un CONTRATO declarativo, no una
# banda empírica del render). Authority: INGENIERO-PAUTA § 7.11.4. Override vía CLI.
REQUIRED_SYNC_CONTRACT_FIELDS = ("visual_start_s", "audio_start_s", "tolerance_s")

# Dir canónico de la AVU library compartida (NIVEL 2 universal — § 7.11.1). avu_overlay_clip y
# audio_visual_atomic_units[].asset_path resuelven acá cuando son basenames de la library.
AVU_LIBRARY_DIRNAME = "avu-library"

# Tokens que NO cuentan como AVU real (placeholders del SPEC). avu_overlay_clip: null / "" → no AVU.
AVU_NULL_TOKENS = ("", "null", "none", "~")


def gate(name, status, detail, **extra):
    """Resultado de un check: status ∈ pass | fail | not_applicable."""
    d = {"check": name, "status": status, "detail": detail}
    d.update(extra)
    return d


# ════════════════════════════════════════════════════════════════════════════════════════════
# LÓGICA PURA — testeable sin filesystem
# ════════════════════════════════════════════════════════════════════════════════════════════

def evaluate_avu_sync_contract(shots):
    """PURE. shots = [{shot_id, coupled, coupling_reasons,
                       avu_present, avu_paths_checked, has_complete_sync_contract,
                       sync_contract_missing_fields}].

    Devuelve (ok, summary). Un shot ACOPLADO pasa si avu_present O
    has_complete_sync_contract. FAIL si acoplado sin ninguna de las dos
    (compose-time fragility risk — matadero iter 3-4).

    Si NINGÚN shot está acoplado → not_applicable (ok=True, applicable=False)."""
    coupled = [s for s in shots if s.get("coupled")]
    reasons = []
    ok = True

    if not coupled:
        return True, {
            "applicable": False,
            "coupled_shots": 0,
            "shots": [{
                "shot_id": s.get("shot_id", "?"), "coupled": False, "status": "ok",
                "rule_applies": False,
                "detail": "shot sin audio+visual acoplados → regla AVU/sync_contract no aplica",
            } for s in shots],
        }

    for s in shots:
        sid = s.get("shot_id", "?")
        if not s.get("coupled"):
            reasons.append({
                "shot_id": sid, "coupled": False, "status": "ok", "rule_applies": False,
                "detail": "shot sin audio+visual acoplados → regla no aplica",
            })
            continue

        coupling = s.get("coupling_reasons") or []
        avu_present = bool(s.get("avu_present"))
        contract_ok = bool(s.get("has_complete_sync_contract"))

        if avu_present or contract_ok:
            satisfier = []
            if avu_present:
                satisfier.append("AVU .mp4 en disco")
            if contract_ok:
                satisfier.append("sync_contract completo")
            reasons.append({
                "shot_id": sid, "coupled": True, "status": "ok", "rule_applies": True,
                "coupling_reasons": coupling,
                "satisfied_by": satisfier,
                "avu_paths_checked": s.get("avu_paths_checked") or [],
                "detail": f"shot acoplado ({', '.join(coupling)}) satisfecho por: {' + '.join(satisfier)} ✓",
            })
        else:
            ok = False
            missing = s.get("sync_contract_missing_fields") or list(REQUIRED_SYNC_CONTRACT_FIELDS)
            reasons.append({
                "shot_id": sid, "coupled": True, "status": "fail", "rule_applies": True,
                "coupling_reasons": coupling,
                "avu_present": False,
                "avu_paths_checked": s.get("avu_paths_checked") or [],
                "sync_contract_missing_fields": missing,
                "detail": (
                    f"shot '{sid}' tiene audio+visual ACOPLADOS ({', '.join(coupling)}) pero NO tiene "
                    f"(a) AVU pre-rendered .mp4 en disco NI (b) sync_contract completo "
                    f"(faltan {missing}) — Q24/HR#25 compose-time fragility (matadero iter 3-4): "
                    f"buildear el AVU .mp4 (audio bundleado) O declarar sync_contract explícito"),
            })

    return ok, {
        "applicable": True,
        "coupled_shots": len(coupled),
        "shots": reasons,
    }


def sync_contract_missing_fields(contract, *, required=REQUIRED_SYNC_CONTRACT_FIELDS):
    """PURE. contract = dict (o None). Devuelve la lista de campos requeridos AUSENTES
    o None-valued. contract None/no-dict → todos faltan."""
    if not isinstance(contract, dict):
        return list(required)
    return [f for f in required if contract.get(f) is None]


# ════════════════════════════════════════════════════════════════════════════════════════════
# EXTRACCIÓN — runtime (parsea el SPEC + resuelve AVU paths contra disco)
# ════════════════════════════════════════════════════════════════════════════════════════════

def extract_shots(spec):
    """shot_list[] → solo dicts con shot_id."""
    return [s for s in (spec.get("shot_list") or []) if isinstance(s, dict) and s.get("shot_id")]


def _is_null_avu(value):
    """avu_overlay_clip null / "" / "null" → no es un AVU real."""
    if value is None:
        return True
    return str(value).strip().lower() in AVU_NULL_TOKENS


def find_avu_library_dir(spec_path):
    """Localiza .../ai-video-production/templates/avu-library/ subiendo desde el script
    (vivimos en .../templates/scripts/) con fallback a buscar desde el spec. Devuelve Path o None."""
    here = Path(__file__).resolve().parent          # .../templates/scripts/
    cand = here.parent / AVU_LIBRARY_DIRNAME         # .../templates/avu-library/
    if cand.is_dir():
        return cand
    # Fallback: subir desde el spec buscando ai-video-production/templates/avu-library
    for parent in [spec_path.resolve()] + list(spec_path.resolve().parents):
        guess = parent / ".claude" / "skills" / "ai-video-production" / "templates" / AVU_LIBRARY_DIRNAME
        if guess.is_dir():
            return guess
    return None


def resolve_avu_on_disk(avu_ref, *, avu_library_dir, project_dir, clips_atomic_dir):
    """Resuelve una referencia a AVU (.mp4) contra disco. Devuelve (present: bool, checked: [paths]).

    avu_ref puede ser:
      · path absoluto / relativo al proyecto → se prueba tal cual + relativo a project_dir
      · basename de la avu-library (ej. countdown-3-2-1-film-leader-with-ticks.mp4) → avu_library_dir
    Se prueba cada candidato con stat (HR#19 MEASURE)."""
    checked = []
    if _is_null_avu(avu_ref):
        return False, checked
    ref = str(avu_ref).strip()
    candidates = []
    p = Path(ref)
    if p.is_absolute():
        candidates.append(p)
    else:
        # relativo al proyecto (avu_overlay_clip suele venir como path tipo "ai-video-production/.../x.mp4")
        if project_dir:
            candidates.append(Path(project_dir) / ref)
        # basename contra la library compartida
        if avu_library_dir:
            candidates.append(Path(avu_library_dir) / Path(ref).name)
        # basename contra clips-atomic del proyecto (lip-sync bundled)
        if clips_atomic_dir:
            candidates.append(Path(clips_atomic_dir) / Path(ref).name)
    for c in candidates:
        checked.append(str(c))
        try:
            if c.is_file() and c.stat().st_size > 0:
                return True, checked
        except OSError:
            continue
    return False, checked


def _atomic_clip_for_shot(shot_id, clips_atomic_dir):
    """Para shots con lip-sync el audio (diálogo) va bundleado en el clip atomic .mp4 (Layer 1).
    Busca shot_<id>_*_atomic.mp4 (o shot_<id>_atomic.mp4) en clips-atomic/. (present, [checked])."""
    if not clips_atomic_dir or not Path(clips_atomic_dir).is_dir():
        return False, []
    checked = []
    d = Path(clips_atomic_dir)
    # naming: shot_NN_<descriptor>_atomic.mp4  (también shot_NN_atomic.mp4)
    matches = sorted(d.glob(f"{shot_id}_*atomic.mp4")) + sorted(d.glob(f"{shot_id}_atomic.mp4"))
    for m in matches:
        checked.append(str(m))
        try:
            if m.is_file() and m.stat().st_size > 0:
                return True, checked
        except OSError:
            continue
    if not checked:
        checked.append(str(d / f"{shot_id}_*atomic.mp4"))
    return False, checked


def build_shot_record(shot, *, avu_library_dir, project_dir, clips_atomic_dir,
                      required_fields=REQUIRED_SYNC_CONTRACT_FIELDS):
    """Arma el dict de un shot para la lógica pura: detecta acople + resuelve AVU/contract."""
    sid = shot.get("shot_id", "?")
    coupling_reasons = []

    # 1. audio_visual_atomic_units (lista canonical § 7.11.4)
    avus = shot.get("audio_visual_atomic_units")
    avu_list = avus if isinstance(avus, list) else []
    if avu_list:
        coupling_reasons.append("audio_visual_atomic_units declarado")

    # 2. avu_overlay_clip no-null
    overlay = shot.get("avu_overlay_clip")
    if not _is_null_avu(overlay):
        coupling_reasons.append(f"avu_overlay_clip='{str(overlay).strip()}'")

    # 3. lip-sync (diálogo de personaje acoplado a su visual)
    lip = bool(shot.get("has_lip_sync_required")) or bool(shot.get("lip_sync_required"))
    if lip:
        coupling_reasons.append("has_lip_sync_required=true")

    # 4. sync_contract top-level del shot
    top_contract = shot.get("sync_contract")
    if isinstance(top_contract, dict):
        coupling_reasons.append("sync_contract declarado")

    coupled = bool(coupling_reasons)

    # ── (a) AVU .mp4 en disco ──
    avu_present = False
    avu_paths_checked = []
    # 2-resolve: avu_overlay_clip
    if not _is_null_avu(overlay):
        present, checked = resolve_avu_on_disk(
            overlay, avu_library_dir=avu_library_dir, project_dir=project_dir,
            clips_atomic_dir=clips_atomic_dir)
        avu_paths_checked += checked
        avu_present = avu_present or present
    # 1-resolve: audio_visual_atomic_units[].asset_path (los de type pre_rendered_avu)
    for u in avu_list:
        if not isinstance(u, dict):
            continue
        ap = u.get("asset_path")
        if ap:
            present, checked = resolve_avu_on_disk(
                ap, avu_library_dir=avu_library_dir, project_dir=project_dir,
                clips_atomic_dir=clips_atomic_dir)
            avu_paths_checked += checked
            avu_present = avu_present or present
    # lip-sync: el audio del diálogo va bundleado en el clip atomic .mp4 (Layer 1 HYBRID)
    if lip and not avu_present:
        present, checked = _atomic_clip_for_shot(sid, clips_atomic_dir)
        avu_paths_checked += checked
        avu_present = avu_present or present

    # ── (b) sync_contract completo ──
    contracts = []
    if isinstance(top_contract, dict):
        contracts.append(top_contract)
    for u in avu_list:
        if isinstance(u, dict) and str(u.get("type", "")).strip() == "sync_contract":
            c = u.get("contract")
            if isinstance(c, dict):
                contracts.append(c)
            else:
                contracts.append({})  # declarado type sync_contract pero sin contract → incompleto
    has_complete = (
        any(not sync_contract_missing_fields(c, required=required_fields) for c in contracts)
        if contracts else False)
    # campos faltantes del "mejor" contrato (el de menos faltantes) para el reporte
    if contracts:
        missing = min((sync_contract_missing_fields(c, required=required_fields) for c in contracts), key=len)
    else:
        missing = list(required_fields)

    return {
        "shot_id": sid,
        "coupled": coupled,
        "coupling_reasons": coupling_reasons,
        "avu_present": avu_present,
        "avu_paths_checked": avu_paths_checked,
        "has_complete_sync_contract": has_complete,
        "sync_contract_missing_fields": missing,
    }


# ════════════════════════════════════════════════════════════════════════════════════════════
# RUNTIME
# ════════════════════════════════════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--format", required=True,
                        help="formato del SPEC (agnostic-by-design)")
    parser.add_argument("--spec", required=True, help="path al CREATIVE-SPEC.yaml")
    parser.add_argument("--project-dir", default=None,
                        help="dir del proyecto (assets/). Default: <spec_dir>/../<spec_stem>/ si existe.")
    parser.add_argument("--avu-library-dir", default=None,
                        help="dir de la avu-library compartida. Default: autolocalizada desde el script/spec.")
    parser.add_argument("--require-contract-fields", default=",".join(REQUIRED_SYNC_CONTRACT_FIELDS),
                        help=f"campos requeridos del sync_contract (default: {','.join(REQUIRED_SYNC_CONTRACT_FIELDS)})")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    required_fields = tuple(
        f.strip() for f in args.require_contract_fields.split(",") if f.strip()
    ) or REQUIRED_SYNC_CONTRACT_FIELDS

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

    has_clips = bool(caps.get("has_ai_generated_clips", False))

    # Resolución de dirs.
    project_dir = args.project_dir
    if project_dir is None:
        guess = spec_path.parent.parent / spec_path.stem
        if guess.is_dir():
            project_dir = str(guess)
    avu_library_dir = args.avu_library_dir or (
        str(find_avu_library_dir(spec_path)) if find_avu_library_dir(spec_path) else None)
    clips_atomic_dir = None
    if project_dir:
        cand = Path(project_dir) / "assets" / "clips-atomic"
        if cand.is_dir():
            clips_atomic_dir = str(cand)

    if args.dry_run:
        print(f"format: {args.format}\nspec: {spec_path}\nhas_ai_generated_clips: {has_clips}\n"
              f"branch: {'avu_sync_check' if has_clips else 'not_applicable'}\n"
              f"project_dir: {project_dir}\navu_library_dir: {avu_library_dir}\n"
              f"clips_atomic_dir: {clips_atomic_dir}\n"
              f"required_contract_fields: {list(required_fields)}")
        return 0

    if not has_clips:
        print(json.dumps({
            "format": args.format, "overall_status": "not_applicable",
            "detail": "has_ai_generated_clips=false → AVU/sync_contract check skipped "
                      "(sin clips AI no hay compose-time fragility del acople que prevenir)",
        }, indent=2, ensure_ascii=False))
        return 0

    shots = extract_shots(spec)
    records = [build_shot_record(
        s, avu_library_dir=avu_library_dir, project_dir=project_dir,
        clips_atomic_dir=clips_atomic_dir, required_fields=required_fields) for s in shots]

    ok, summary = evaluate_avu_sync_contract(records)

    if not summary["applicable"]:
        print(json.dumps({
            "format": args.format, "spec": str(spec_path),
            "overall_status": "not_applicable",
            "detail": "ningún shot tiene audio+visual acoplados (sin AVU/lip-sync/sync_contract) → "
                      "Q24/HR#25 no aplica a este SPEC",
            "shots_checked": len(records),
        }, indent=2, ensure_ascii=False))
        return 0

    fails = [r for r in summary["shots"] if r["status"] == "fail"]
    report = {
        "format": args.format, "spec": str(spec_path),
        "project_dir": project_dir,
        "avu_library_dir": avu_library_dir,
        "clips_atomic_dir": clips_atomic_dir,
        "required_contract_fields": list(required_fields),
        "overall_status": "pass" if ok else "fail",
        "overall_pass": ok,
        "shots_checked": len(records),
        "coupled_shots": summary["coupled_shots"],
        "fail_count": len(fails),
        "fail_shots": fails,
        "shots": summary["shots"],
    }
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
