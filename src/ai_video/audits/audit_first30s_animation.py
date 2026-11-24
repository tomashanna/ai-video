#!/usr/bin/env python3
"""audit-first30s-animation.py — HR#6 + HR#7 first-30s animation gate.

BUG REAL que cierra (caso disparador cabana-tormenta): el video shipeó la ventana
de retención (primeros 30s, incluido EL HOOK en data-start 0) como 23 <img> CSS
estáticos animados con Ken Burns — un "PowerPoint narrado" en vez de clips de
animación AI. cabina-14 fue el caso MIXTO (16 <video> + 7 <img>, varios <img> caen
<30s). HR#6 (CLAUDE.md) es categórica: los primeros 30s = animation AI obligatoria,
NUNCA Ken Burns ni estático. HR#7: el Ken Burns/estático es fallback ≤20% de los
shots y cada uno ≤2-3s.

POR QUÉ NO LO CAZABA NADIE:
  - El gate vivía como PROSA: HR#6/#7 en CLAUDE.md + pre-render-gate Q como checklist
    manual ("primeros 30s = animation AI planeada"). Nadie corría un número.
  - audit-spec-completeness.py cuenta EXISTENCIA de assets (¿el clip/PNG está en
    disco?) — un <img> estático en data-start 0 PASA completeness perfecto (el asset
    existe), pero VIOLA HR#6 (debía ser <video> clip animado).
  - Gemini holístico NO distingue de forma fiable un Ken Burns lento de un clip i2v
    real en 1 frame muestreado: ambos "se ven" como una imagen de la escena (caso
    pueblo-fantasma-desierto 9.9 holístico vs 7/10 real). Hace falta leer el TIPO de
    elemento (<video> vs <img>) / el model del manifest (i2v vs procedural/ken-burns),
    no juzgar el píxel.
  - Un check INGENUO contaría "¿hay AL MENOS un clip animado en los 30s?" y pasaría
    cabina-14 (tiene 16 <video>). Pero el hook estático sigue ahí. Acá exigimos que
    TODO shot que ARRANCA <30s sea animado AI — no que "haya alguno".

REGLA:
  (HR#6) Todo shot/elemento visual cuyo start < 30.0s DEBE ser un clip de animación
         AI: <video> en HTML legacy / model i2v-real (NO procedural, NO ken-burns) en
         el manifest HYBRID. Un <img> estático o un shot procedural:true que arranca
         <30s → FAIL.
  (HR#7) GLOBAL (todo el video): los shots Ken Burns/estáticos son fallback acotado —
         su share ≤20% del total de shots Y cada uno dura ≤3.0s. Share >20% o cualquier
         estático >3.0s → FAIL.

Capability-gate (gating EXACTO de HR#6 en CLAUDE.md): la regla aplica solo si
  has_ai_generated_clips=true AND format_type ∈ {interactive_choice, reel}. Si
  has_ai_generated_clips=false → not_applicable (exit 0). Si format_type fuera del set
  → not_applicable (exit 0). video_capabilities ausente → Bug #9 (exit 2).
  Agnostic-by-design: --format REQUIRED.

DISEÑO TESTEABLE: lógica pura en evaluate_first30s_hr6(shots,...) + evaluate_kenburns_hr7(shots,...)
  — reciben shots ya extraídos [{shot_id, start_s, is_animated, is_static_kenburns, duration_s}];
  los wrappers (parse_manifest_shots / parse_html_shots) resuelven filesystem.

Exit: 0 PASS/not_applicable · 1 FAIL · 2 can't-measure (Bug #9 / SPEC|input ausente).
Authority: CLAUDE.md HR#6 (animation_30s_rule.md) + HR#7 (MOTION-LAYER.md +
  <format>-format/INGENIERO-PAUTA-MASTER §5.6) + ai-video-production/animation_30s_rule.
  HR#26 companion test: test_audit-first30s-animation.py.
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

# ── Constantes con autoridad ─────────────────────────────────────────────────
# HR#6 ventana de retención. Authority: CLAUDE.md HR#6 + memoria animation_30s_rule
#   ("primeros 30s del Reel = clip animado AI, NO Ken Burns ni estático") — regla
#   model-agnostic universal short-form, NO medida en F1 (es un umbral de diseño,
#   no una banda empírica). Override via --window-s.
FIRST_WINDOW_S = 30.0
# HR#7 fallback acotado. Authority: CLAUDE.md HR#7 + MOTION-LAYER.md
#   ("Animation AI preferred; Ken Burns fallback ≤20%, max 2-3s") — NO medida en F1.
#   Override via --kenburns-max-share / --kenburns-max-dur-s.
KENBURNS_MAX_SHARE = 0.20  # ≤20% de los shots
KENBURNS_MAX_DUR_S = 3.0  # cada estático/Ken Burns ≤3.0s ("max 2-3s")

# Models que NO son animación AI (no-AI): el manifest los marca procedural:true.
# Cualquier nombre de model que matchee estos tokens = estático/Ken Burns (no-AI).
NON_AI_MODEL_TOKENS = ("procedural", "ken-burns", "ken_burns", "kenburns", "static", "still", "css", "none")


# ═══════════════════════════════════════════════════════════════════════════
# LÓGICA PURA (testeable sin filesystem)
# ═══════════════════════════════════════════════════════════════════════════


def evaluate_first30s_hr6(shots, *, window_s=FIRST_WINDOW_S):
    """PURE (HR#6). shots = [{shot_id, start_s, is_animated, ...}].

    Devuelve (ok, reasons). FAIL si ALGÚN shot que arranca start_s < window_s NO
    es animación AI (is_animated False). No basta con "haya algún clip animado":
    TODO shot dentro de la ventana debe serlo (caso cabana-tormenta hook estático
    en start 0). Shots con start_s >= window_s no los gatea HR#6.
    """
    reasons = []
    ok = True
    for s in shots:
        sid = s.get("shot_id", "?")
        try:
            start = float(s.get("start_s") if s.get("start_s") is not None else 1e9)
        except (TypeError, ValueError):
            start = 1e9
        is_anim = bool(s.get("is_animated"))
        if start >= window_s:
            reasons.append(
                {
                    "shot_id": sid,
                    "start_s": round(start, 2),
                    "is_animated": is_anim,
                    "status": "ok",
                    "rule_applies": False,
                    "detail": f"start {start:.1f}s ≥ {window_s:.0f}s → fuera de la ventana HR#6",
                }
            )
            continue
        if not is_anim:
            ok = False
            reasons.append(
                {
                    "shot_id": sid,
                    "start_s": round(start, 2),
                    "is_animated": is_anim,
                    "status": "fail",
                    "rule_applies": True,
                    "detail": (
                        f"shot '{sid}' arranca a {start:.1f}s (<{window_s:.0f}s) y NO es "
                        f"animación AI (estático/Ken Burns/procedural) — HR#6 exige clip "
                        f"animado AI en TODA la ventana de retención (riesgo PowerPoint-narrado)"
                    ),
                }
            )
        else:
            reasons.append(
                {
                    "shot_id": sid,
                    "start_s": round(start, 2),
                    "is_animated": is_anim,
                    "status": "ok",
                    "rule_applies": True,
                    "detail": f"start {start:.1f}s (<{window_s:.0f}s) con clip animado AI ✓",
                }
            )
    return ok, reasons


def evaluate_kenburns_hr7(shots, *, max_share=KENBURNS_MAX_SHARE, max_dur_s=KENBURNS_MAX_DUR_S):
    """PURE (HR#7). GLOBAL sobre todos los shots.

    Devuelve (ok, summary, per_shot_reasons). FAIL si:
      (a) share de estáticos/Ken Burns > max_share, O
      (b) algún estático/Ken Burns dura > max_dur_s.
    is_static_kenburns marca el shot como no-AI (procedural/img/ken-burns).
    """
    total = len(shots)
    static_shots = [s for s in shots if bool(s.get("is_static_kenburns"))]
    n_static = len(static_shots)
    share = (n_static / total) if total else 0.0

    per_shot = []
    over_dur = []
    for s in static_shots:
        sid = s.get("shot_id", "?")
        try:
            dur = float(s.get("duration_s") if s.get("duration_s") is not None else 0.0)
        except (TypeError, ValueError):
            dur = 0.0
        too_long = dur > max_dur_s
        if too_long:
            over_dur.append(sid)
        per_shot.append(
            {
                "shot_id": sid,
                "duration_s": round(dur, 2),
                "status": "fail" if too_long else "ok",
                "detail": (
                    f"estático/Ken Burns '{sid}' dura {dur:.1f}s "
                    + (
                        f"> {max_dur_s:.0f}s — HR#7 exige ≤{max_dur_s:.0f}s c/u"
                        if too_long
                        else f"≤{max_dur_s:.0f}s ✓"
                    )
                ),
            }
        )

    share_ok = share <= max_share + 1e-9
    dur_ok = len(over_dur) == 0
    ok = share_ok and dur_ok
    summary = {
        "total_shots": total,
        "static_kenburns_shots": n_static,
        "static_share": round(share, 4),
        "max_share": max_share,
        "share_ok": share_ok,
        "max_dur_s": max_dur_s,
        "over_duration_shots": over_dur,
        "duration_ok": dur_ok,
        "detail": (
            f"share Ken Burns/estático {share * 100:.0f}% > {max_share * 100:.0f}% — "
            f"HR#7 lo limita a fallback ({n_static}/{total} shots)"
            if not share_ok
            else f"share Ken Burns/estático {share * 100:.0f}% ≤ {max_share * 100:.0f}% ✓ ({n_static}/{total})"
        ),
    }
    return ok, summary, per_shot


# ═══════════════════════════════════════════════════════════════════════════
# WRAPPERS DE EXTRACCIÓN (filesystem)
# ═══════════════════════════════════════════════════════════════════════════


def _model_is_non_ai(model, procedural):
    """True si el shot del manifest NO es animación AI (no-AI / estático / Ken Burns)."""
    if procedural is True:
        return True
    m = (str(model) if model is not None else "").strip().lower()
    if not m:
        return True  # sin model declarado → no es un clip AI confiable
    return any(tok in m for tok in NON_AI_MODEL_TOKENS)


def parse_manifest_shots(manifest, spec):
    """HYBRID per-clip. Cruza el manifest CP4 (model/procedural/clip_duration_s por
    shot) con el SPEC shot_list (duration_intent_s acumulado → start_s de cada shot).

    El start_s de un shot = suma de duration_intent_s de los shots ANTERIORES en el
    orden del shot_list del SPEC (mismo orden que el manifest). Devuelve la lista de
    dicts puros para evaluate_*.
    """
    spec_shots = spec.get("shot_list") or []
    # Mapa shot_id → duration_intent_s (del SPEC, autoridad de timing-intent).
    spec_dur = {}
    spec_order = []
    for s in spec_shots:
        if not isinstance(s, dict):
            continue
        sid = str(s.get("shot_id", "")).strip()
        if not sid:
            continue
        spec_order.append(sid)
        try:
            spec_dur[sid] = (
                float(s.get("duration_intent_s")) if s.get("duration_intent_s") is not None else None
            )
        except (TypeError, ValueError):
            spec_dur[sid] = None

    manifest_shots = manifest.get("shots") or []
    # Orden de acumulación: el del manifest (es el orden de ensamble real).
    cumulative = 0.0
    out = []
    for ms in manifest_shots:
        if not isinstance(ms, dict):
            continue
        sid = str(ms.get("shot_id", "")).strip() or "?"
        model = ms.get("model")
        procedural = ms.get("procedural")
        non_ai = _model_is_non_ai(model, procedural)

        # duración del shot: SPEC duration_intent_s (intent canónico) si existe,
        # si no clip_duration_s del manifest.
        dur = spec_dur.get(sid)
        if dur is None:
            cd = ms.get("clip_duration_s")
            try:
                dur = float(cd) if cd is not None else 0.0
            except (TypeError, ValueError):
                dur = 0.0

        start = cumulative
        cumulative += dur or 0.0
        out.append(
            {
                "shot_id": sid,
                "start_s": start,
                "duration_s": dur or 0.0,
                "model": model,
                "is_animated": not non_ai,
                "is_static_kenburns": non_ai,
            }
        )
    return out


# Regex robusto (NADA de bs4/lxml — idéntico idiom a audit-narrative.py).
_TAG_RE = re.compile(r'<(video|img)\b[^>]*>', re.IGNORECASE)


def _attr(tag, name):
    m = re.search(rf'{name}\s*=\s*"([^"]*)"', tag, re.IGNORECASE)
    return m.group(1) if m else None


def parse_html_shots(html_content):
    """HTML legacy. Cada elemento visual con data-start: <video> = clip animado AI,
    <img> = estático/Ken Burns CSS. start_s = data-start; duration_s = data-duration.

    Solo elementos con data-start Y data-duration parseables (la capa de clips). Los
    overlays UI (countdown/loading divs) no son <video>/<img> y no entran acá.
    """
    out = []
    for m in _TAG_RE.finditer(html_content):
        tag = m.group(0)
        kind = m.group(1).lower()
        eid = _attr(tag, "id") or "?"
        ds = _attr(tag, "data-start")
        dd = _attr(tag, "data-duration")
        if ds is None or dd is None:
            continue
        try:
            start = float(ds)
            dur = float(dd)
        except ValueError:
            continue
        is_video = kind == "video"
        out.append(
            {
                "shot_id": eid,
                "start_s": start,
                "duration_s": dur,
                "tag": kind,
                "is_animated": is_video,  # <video> = clip animado AI
                "is_static_kenburns": (not is_video),  # <img> = estático / Ken Burns CSS
            }
        )
    return out


# ═══════════════════════════════════════════════════════════════════════════
# RUNTIME
# ═══════════════════════════════════════════════════════════════════════════


def _load_yaml(path: Path):
    with open(path) as f:
        return yaml.safe_load(f) or {}


def _detect_mode(args):
    if args.mode != "auto":
        return args.mode
    if args.manifest:
        return "manifest"
    if args.html:
        return "html"
    return "auto"


def main():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "--format", required=True, help="agnostic-by-design (horror-choice / sport-choice / ...)"
    )
    parser.add_argument(
        "--mode",
        choices=["auto", "manifest", "html"],
        default="auto",
        help="auto-detecta por --manifest/--html, o forzá el modo",
    )
    parser.add_argument(
        "--spec",
        help="CREATIVE-SPEC.yaml (video_capabilities + shot_list). REQUERIDO en modo manifest y para la capability-gate.",
    )
    parser.add_argument("--manifest", help="cp4-manifest*.yaml (HYBRID per-clip)")
    parser.add_argument("--html", help="index.html (legacy)")
    parser.add_argument("--window-s", type=float, default=FIRST_WINDOW_S)
    parser.add_argument("--kenburns-max-share", type=float, default=KENBURNS_MAX_SHARE)
    parser.add_argument("--kenburns-max-dur-s", type=float, default=KENBURNS_MAX_DUR_S)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    mode = _detect_mode(args)
    if mode == "auto":
        print("ERROR: no input — pasá --manifest (HYBRID) o --html (legacy), o --mode.", file=sys.stderr)
        return 2

    # ── Capability gate (necesita el SPEC) ──────────────────────────────────
    # En modo HTML el SPEC es opcional para extraer shots (el HTML es autónomo) pero
    # SÍ requerido para la capability-gate. Si no hay SPEC en modo HTML, exigimos uno
    # (la capability-gate de HR#6 vive en el SPEC — no se puede saltear).
    if not args.spec:
        print(
            "ERROR: --spec requerido (capability-gate HR#6 vive en video_capabilities del SPEC).",
            file=sys.stderr,
        )
        return 2
    spec_path = Path(args.spec)
    if not spec_path.exists():
        print(f"ERROR: SPEC not found: {spec_path}", file=sys.stderr)
        return 2
    spec = _load_yaml(spec_path)

    caps = spec.get("video_capabilities")
    if caps is None:
        print(
            "ERROR: SPEC missing 'video_capabilities' block (Pattern 7 §1.6 mandatory). Bug #9.",
            file=sys.stderr,
        )
        return 2

    has_clips = bool(caps.get("has_ai_generated_clips", False))
    fmt_type = str(caps.get("format_type", "")).strip()
    GATED_FORMAT_TYPES = {"interactive_choice", "reel"}

    if args.dry_run:
        print(
            f"format: {args.format}\nmode: {mode}\nspec: {spec_path}\n"
            f"has_ai_generated_clips: {has_clips}\nformat_type: {fmt_type}\n"
            f"window_s: {args.window_s}\nkenburns_max_share: {args.kenburns_max_share}\n"
            f"kenburns_max_dur_s: {args.kenburns_max_dur_s}\n"
            f"branch: {'first30s_animation_check' if (has_clips and fmt_type in GATED_FORMAT_TYPES) else 'not_applicable'}"
        )
        return 0

    if not has_clips:
        print(
            json.dumps(
                {
                    "format": args.format,
                    "mode": mode,
                    "overall_status": "not_applicable",
                    "detail": "has_ai_generated_clips=false → first-30s animation gate skipped (no AI clips).",
                },
                indent=2,
                ensure_ascii=False,
            )
        )
        return 0
    if fmt_type not in GATED_FORMAT_TYPES:
        print(
            json.dumps(
                {
                    "format": args.format,
                    "mode": mode,
                    "overall_status": "not_applicable",
                    "detail": (
                        f"format_type='{fmt_type}' ∉ {sorted(GATED_FORMAT_TYPES)} → "
                        f"HR#6 first-30s rule no aplica (gating exacto de CLAUDE.md)."
                    ),
                },
                indent=2,
                ensure_ascii=False,
            )
        )
        return 0

    # ── Extracción de shots según modo ──────────────────────────────────────
    if mode == "manifest":
        if not args.manifest:
            print("ERROR: --manifest requerido en modo manifest.", file=sys.stderr)
            return 2
        man_path = Path(args.manifest)
        if not man_path.exists():
            print(f"ERROR: manifest not found: {man_path}", file=sys.stderr)
            return 2
        manifest = _load_yaml(man_path)
        shots = parse_manifest_shots(manifest, spec)
        input_ref = str(man_path)
    else:  # html
        if not args.html:
            print("ERROR: --html requerido en modo html.", file=sys.stderr)
            return 2
        html_path = Path(args.html)
        if not html_path.exists():
            print(f"ERROR: html not found: {html_path}", file=sys.stderr)
            return 2
        shots = parse_html_shots(html_path.read_text(encoding="utf-8", errors="ignore"))
        input_ref = str(html_path)

    if not shots:
        print(
            "ERROR: 0 shots extraídos del input — no se puede medir (input vacío/no parseable). Bug #9.",
            file=sys.stderr,
        )
        return 2

    # ── Evaluación pura ─────────────────────────────────────────────────────
    ok6, reasons6 = evaluate_first30s_hr6(shots, window_s=args.window_s)
    ok7, summary7, per_shot7 = evaluate_kenburns_hr7(
        shots, max_share=args.kenburns_max_share, max_dur_s=args.kenburns_max_dur_s
    )

    overall_ok = ok6 and ok7
    report = {
        "format": args.format,
        "mode": mode,
        "spec": str(spec_path),
        "input": input_ref,
        "window_s": args.window_s,
        "overall_status": "pass" if overall_ok else "fail",
        "overall_pass": overall_ok,
        "shots_extracted": len(shots),
        "hr6_first30s_animation": {
            "pass": ok6,
            "shots_in_window": sum(1 for r in reasons6 if r["rule_applies"]),
            "fail_shots": [r for r in reasons6 if r["status"] == "fail"],
            "shots": reasons6,
        },
        "hr7_kenburns_fallback": {
            "pass": ok7,
            "summary": summary7,
            "static_shots": per_shot7,
        },
    }
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if overall_ok else 1


if __name__ == "__main__":
    sys.exit(main())
