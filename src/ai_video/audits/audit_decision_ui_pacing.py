#!/usr/bin/env python3
"""audit-decision-ui-pacing.py — Q22a pre-render-gate: valida el decision-UI editorial pacing del PROYECTO ACTUAL contra las bandas canónicas medidas.

BUG REAL que cierra (Q22a — decision-UI editorial pacing, hoy MANUAL):
  El pre-render-gate Q22 ("decision UI editorial moment correcto") se chequea a OJO.
  Un SPEC puede declarar un countdown de 0.4s/dígito (ilegible, se pierde el beat de tensión)
  o de 2.5s/dígito (mata el ritmo del Reel) y nadie lo caza: los 3 freezes de decisión se
  revisan a mano bajo presión de tiempo. La pauta de pacing del decision-UI YA está MEDIDA
  empíricamente desde los 8 refs canónicos (aggregate-canonical-bands.json: countdown digit
  duration, pause beat narración→countdown, WPM por rol de segmento, freeze%), pero NINGÚN
  script comparaba el SPEC contra esas bandas — vivía como Y/N de un checklist humano.

POR QUÉ NO LO CAZABA NADIE:
  · audit-spec-completeness.py cuenta EXISTENCIA de elementos UI (¿está declarado el countdown?)
    pero NO razona sobre su DURACIÓN/TIMING contra una banda empírica.
  · audit-ui-safe-zones.py valida la POSICIÓN (Y%) de los overlays, no su PACING temporal.
  · audit-spec-narration-fits-duration.py valida que la narración QUEPA en el clip, no su WPM
    contra la banda canónica POR ROL de segmento (decision_question vs hook vs cliffhanger).
  · Gemini holístico NO ve metadata del SPEC (timestamp_visible_s, ui_active) — solo el render.
  El timing del decision-UI es exactamente el tipo de número que el ojo aprueba por "se ve bien"
  sin medir, y que drifteó silenciosamente en producciones previas (countdown 0.7 broadcast vs
  1.0 perceptual vs 0.5 medido — GAP #16 user-validated).

REGLA (por DECISION SHOT — identificable en el SPEC: shots con ui_active countdown/loading,
  o avu_overlay_clip de countdown/freeze-decision, o section_id de decisión):
  Para cada decision shot, medir desde el SPEC + manifest los parámetros MEDIBLES del timing
  declarado y validarlos contra la banda [p25, p75] del aggregate JSON:
    · countdown_digit_duration_s  = span del countdown ui_active / n_dígitos ("3-2-1" → 3).
    · countdown_pause_beat_s      = countdown_start_abs − narración_question_end_abs (separación
                                    temporal narración→countdown). ⚠️ Measurement-grade SOLO si la
                                    narración (timestamp_intent_s absoluto) y el countdown (ui_active
                                    shot-relativo, ubicado por cumulative duration_intent_s) viven en
                                    el MISMO clock en ese shot. Si los dos relojes del SPEC divergen
                                    (>1s) → cross-clock NO confiable → report-only (NO se inventa el
                                    número; gate de pause-beat measurement-grade = forward render).
    · per_segment_wpm (decision_question / decision_setup) = words/dur*60 del narration_in_this_shot,
                                    clasificado por rol (mismo clasificador heurístico que el measure
                                    script) y validado contra per_segment_wpm_bands[rol].
  Banda con n_samples ≥ 4 (MIN_VALUES_FOR_BAND, mismo umbral que lib/empirical_bands +
    audit-against-referent) → fuera de [p25,p75] = FAIL. Banda con n_samples < 4 (p.ej.
    countdown_digit_duration n=1) → REPORT-ONLY (banda débil), NUNCA falla.
  Parámetros que requieren el RENDER (no medibles del SPEC: ambient_duck_db medido por RMS de
    audio; freeze SSIM real; loading-bar fill medido frame-a-frame) → SKIPPED/FORWARD, listados
    explícitamente en el output, NO inventados. (El freeze DECLARADO en el SPEC —pov_traversal
    static/freeze + LUT _freeze_filter + avu freeze clip— se reporta como contexto report-only,
    no como medición del render.)

Capability-gate (Pattern 7): format_type ∈ {interactive_choice, reel} O has_layer_4_ui true →
  aplica. Si no → not_applicable (exit 0): sin capa UI de decisión no hay decision-UI que validar.
  video_capabilities ausente → Bug #9 (exit 2). Agnostic-by-design: --format REQUERIDO.

DISEÑO TESTEABLE: lógica PURA en evaluate_decision_ui_pacing(decision_shots, bands) — recibe los
  shots ya extraídos [{shot_id, countdown_digit_duration_s, countdown_pause_beat_s, wpm_checks,...}]
  + el dict de bandas; testeable sin filesystem. El wrapper runtime parsea SPEC + arma esas
  estructuras + carga el aggregate JSON.

Exit: 0 PASS·not_applicable / 1 FAIL (algún param medible fuera de banda fuerte) / 2 can't-measure
  (Bug #9 / SPEC ausente / pyyaml ausente / bandas JSON ausente sin override).
Authority: referent-analysis/horror-choice/empirical-decision-ui-pacing/aggregate-canonical-bands.json
  (medido n=8 refs, schema v1) + measure-canonical-decision-ui-pacing.py (genera las bandas) +
  pre-render-gate Q22 + choice-format-core/INGENIERO-CHOICE-CORE § 2 (decision-UI pacing) +
  CLAUDE.md HR#19 (NEVER ESTIMATE, ALWAYS MEASURE). HR#26 companion: test_audit-decision-ui-pacing.py.
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

# ── Constantes con autoridad ──────────────────────────────────────────────────────────────────
# Umbral de banda CONFIABLE: idéntico a lib/empirical_bands._MIN_VALUES_FOR_BAND y a
# audit-against-referent.compute_bands. n_samples < 4 → banda débil → report-only (NO falla).
MIN_VALUES_FOR_BAND = 4

# Path canónico del aggregate JSON medido (n=8 refs). Override: --bands-json.
# Authority: measure-canonical-decision-ui-pacing.py OUT_DIR (horror-choice namespaced).
DEFAULT_BANDS_RELPATH = "data/referent-analysis/horror-choice/empirical-decision-ui-pacing/aggregate-canonical-bands.json"

# Capability-gate: capas que activan el check.
UI_FORMAT_TYPES = ("interactive_choice", "reel")

# Familia choice — sección de decisión por section_id (señal de decision shot).
DECISION_SECTION_RE = re.compile(r"^decision(?:_\d+)?(?:_climax)?$", re.IGNORECASE)

# ui_active element_id / font que marcan un overlay de decisión.
COUNTDOWN_ID_RE = re.compile(r"countdown", re.IGNORECASE)
LOADING_ID_RE = re.compile(r"load(?:ing|er)?_?bar|loading", re.IGNORECASE)
COUNTDOWN_FONT_RE = re.compile(r"film.?leader|academy", re.IGNORECASE)
LOADING_FONT_RE = re.compile(r"loading", re.IGNORECASE)

# avu_overlay_clip que marca un beat de decisión/countdown.
AVU_DECISION_RE = re.compile(r"countdown|decision.?freeze|3-?2-?1|tick", re.IGNORECASE)

# Tokens de freeze/near-frozen declarados (CONTEXTO report-only — NO medición del render).
FREEZE_TOKENS = ("static", "static_with_micro_bob", "freeze", "frozen", "near_frozen")

# Rol → patrón regex (mismo clasificador heurístico que measure-canonical-decision-ui-pacing.py
# ROLE_PATTERNS). Solo validamos los roles tied a decision shots (decision_question/decision_setup);
# el resto se clasifica para reporte pero no gatea.
ROLE_PATTERNS = {
    "hook_framing": [r"\b(?:escoge|elige|decid[íi]).*\bcompañer", r"\b(matarife|cocinera|ó o)\b"],
    "setup_establishing": [r"\bplanta el", r"\b(turno|cámara|gancho|despiese)", r"\bsi (?:elegiste|escogiste)\b"],
    "decision_setup": [r"\b(empieza a|empieza|aparece|se voltea|se acerca|empezás)\b"],
    "decision_question": [r"\bdecid[íi]s?\b", r"\bahora decides?\b", r"\b(?:miras|mirás|salís|seguís|te incomoda|prefieres|atrapas|esperas|corres|quedas)\b\?"],
    "consequence_narration": [r"\bsi (?:miras|mirás|seguís|salís|esper|te quieres|sabes|te incomoda|pisas|corres|atrapas)", r"\b(?:envía|enoja|sonríe|deja de|empieza a|abre la)\b"],
    "cliffhanger": [r"\b(?:nunca|sirena|seis|saliste|vive tu|aprendiste|loop|eterno|para siempre|baila)\b"],
    "climax_staccato": [r"^\s*(?:la (?:olla|sirena)|cena|nunca|fin|ya)\b"],
}

# Roles cuya banda WPM gatea para decision shots (los otros se reportan, no fallan).
GATING_WPM_ROLES = ("decision_question", "decision_setup")

# Parámetros del aggregate JSON que requieren el RENDER (no medibles del SPEC) → forward.
RENDER_ONLY_PARAMS = (
    ("ambient_duck_db_during_countdown", "RMS de audio del render (librosa) — el SPEC no declara dB de ducking medido"),
    ("freeze_frame", "SSIM frame-a-frame del render — el SPEC solo DECLARA freeze (pov_traversal/LUT), no lo mide"),
    ("loading_bar_fill_duration_s", "fill width frame-a-frame del render — NO está en el aggregate JSON (Phase 2) y el SPEC solo declara el span de visibilidad"),
)


def gate(name, status, detail, **extra):
    """Resultado de un check de un param: status ∈ pass | fail | report_only | not_applicable."""
    d = {"param": name, "status": status, "detail": detail}
    d.update(extra)
    return d


def classify_segment(text):
    """Clasificador de rol heurístico (alineado a measure-canonical-decision-ui-pacing.ROLE_PATTERNS)."""
    t = (text or "").lower().strip()
    for role, patterns in ROLE_PATTERNS.items():
        for pat in patterns:
            if re.search(pat, t):
                return role
    return "unclassified"


# ════════════════════════════════════════════════════════════════════════════════════════════
# LÓGICA PURA — testeable sin filesystem
# ════════════════════════════════════════════════════════════════════════════════════════════

def _band_for(bands, *path):
    """Navega bands['params'][path...] y devuelve (p25, p75, n_samples) o (None, None, 0)."""
    node = (bands or {}).get("params", {})
    for p in path:
        if not isinstance(node, dict):
            return None, None, 0
        node = node.get(p)
    if not isinstance(node, dict):
        return None, None, 0
    n = node.get("n_samples", 0) or 0
    return node.get("p25"), node.get("p75"), n


def _check_against_band(param_name, value, p25, p75, n_samples, *, unit="s", role=None):
    """PURO. Compara un valor medido contra [p25, p75].

    n_samples < MIN_VALUES_FOR_BAND → report_only (banda débil, NUNCA falla).
    value None → report_only (no medible en este shot). Dentro de banda → pass; fuera → fail.
    """
    label = f"{param_name}" + (f"[{role}]" if role else "")
    if value is None:
        return gate(label, "report_only",
                    f"{label} no medible desde el SPEC en este contexto (sin valor declarado)",
                    value=None, role=role)
    v = round(float(value), 3)
    if p25 is None or p75 is None or n_samples < MIN_VALUES_FOR_BAND:
        return gate(label, "report_only",
                    (f"{label} = {v}{unit} — banda DÉBIL (n_samples={n_samples} < {MIN_VALUES_FOR_BAND}) "
                     f"→ report-only, no falla (banda medida: p25={p25} p75={p75})"),
                    value=v, p25=p25, p75=p75, n_samples=n_samples, role=role)
    lo, hi = float(p25), float(p75)
    if lo <= v <= hi:
        return gate(label, "pass",
                    f"{label} = {v}{unit} ∈ banda [{lo}, {hi}]{unit} (n={n_samples}) ✓",
                    value=v, p25=lo, p75=hi, n_samples=n_samples, role=role)
    return gate(label, "fail",
                (f"{label} = {v}{unit} FUERA de banda canónica [{lo}, {hi}]{unit} (n={n_samples}) — "
                 f"decision-UI pacing diverge del medido en los 8 refs (Q22a)"),
                value=v, p25=lo, p75=hi, n_samples=n_samples, role=role)


def evaluate_decision_ui_pacing(decision_shots, bands):
    """PURO. decision_shots = [{shot_id, countdown_digit_duration_s, countdown_pause_beat_s,
       wpm_checks:[{role, wpm}], freeze_declared, loading_visible_s}, ...]. bands = aggregate dict.

    Devuelve (ok, results) donde results es lista de dicts por shot. ok=False si ALGÚN param
    medible cae fuera de una banda FUERTE (n≥4). Bandas débiles / params render-only NO fallan.
    """
    cd_p25, cd_p75, cd_n = _band_for(bands, "countdown_digit_duration_s", )
    pb_p25, pb_p75, pb_n = _band_for(bands, "countdown_pause_beat_s")

    results = []
    ok = True
    for s in decision_shots:
        sid = s.get("shot_id", "?")
        checks = []

        # 1. countdown digit duration (banda n=1 en el JSON canónico → report-only)
        checks.append(_check_against_band(
            "countdown_digit_duration_s", s.get("countdown_digit_duration_s"),
            cd_p25, cd_p75, cd_n))

        # 2. pause beat narración→countdown (banda n=14 → fuerte). SOLO se mide si narración y
        #    countdown viven en el MISMO clock (mismo shot, anclas consistentes). Si las dos
        #    referencias de timeline del SPEC (cumulative-duration vs narration-absolute) divergen
        #    en el decision shot → cross-clock no confiable → report-only (NO inventamos el número).
        pb_val = s.get("countdown_pause_beat_s")
        if pb_val is not None and s.get("pause_beat_clock_consistent"):
            checks.append(_check_against_band(
                "countdown_pause_beat_s", pb_val, pb_p25, pb_p75, pb_n))
        elif pb_val is not None:
            checks.append(gate(
                "countdown_pause_beat_s", "report_only",
                (f"countdown_pause_beat_s ≈ {pb_val}s NO confiable: el SPEC tiene dos relojes de "
                 f"timeline (cumulative duration_intent_s vs narration timestamp_intent_s absoluto) "
                 f"que divergen en este decision shot → restar countdown_start(rel)−narración_end(abs) "
                 f"mezcla clocks. Medición de pause-beat measurement-grade = forward (render o SPEC "
                 f"con un único clock declarado)"),
                value=pb_val, p25=pb_p25, p75=pb_p75, n_samples=pb_n))
        else:
            checks.append(_check_against_band(
                "countdown_pause_beat_s", None, pb_p25, pb_p75, pb_n))

        # 3. WPM por rol del segmento de decisión (gatea solo decision_question/decision_setup)
        for wc in s.get("wpm_checks") or []:
            role = wc.get("role")
            if role not in GATING_WPM_ROLES:
                # rol no-gating: reportar sin gatear
                checks.append(gate(
                    f"per_segment_wpm[{role}]", "report_only",
                    f"segmento clasificado como '{role}' (no gating en decision shot) — wpm={wc.get('wpm')}",
                    value=wc.get("wpm"), role=role))
                continue
            r_p25, r_p75, r_n = _band_for(bands, "per_segment_wpm_bands", role)
            checks.append(_check_against_band(
                "per_segment_wpm", wc.get("wpm"), r_p25, r_p75, r_n, unit=" wpm", role=role))

        # 4. freeze DECLARADO (contexto report-only — NO medición del render)
        if "freeze_declared" in s:
            fz = s.get("freeze_declared")
            checks.append(gate(
                "freeze_declared_context", "report_only",
                ("freeze/near-frozen DECLARADO en el SPEC (pov_traversal/LUT/avu) — contexto, NO "
                 "medición del render (freeze SSIM real = gate de render, forward)")
                if fz else
                "freeze NO declarado en este decision shot (¿decision moment sin freeze? — revisar a ojo)",
                value=bool(fz)))

        # 5. loading bar span declarado (sin banda en el aggregate JSON → report-only)
        if s.get("loading_visible_s") is not None:
            checks.append(gate(
                "loading_bar_visible_span_s", "report_only",
                (f"loading bar visible {s['loading_visible_s']}s declarado — SIN banda canónica en el "
                 f"aggregate JSON (loading_bar_fill_duration_s = Phase 2, no medido) → report-only"),
                value=s["loading_visible_s"]))

        shot_fail = [c for c in checks if c["status"] == "fail"]
        if shot_fail:
            ok = False
        results.append({
            "shot_id": sid,
            "status": "fail" if shot_fail else "pass",
            "checks": checks,
        })
    return ok, results


# ════════════════════════════════════════════════════════════════════════════════════════════
# EXTRACCIÓN — runtime (parsea el SPEC + arma las estructuras puras)
# ════════════════════════════════════════════════════════════════════════════════════════════

def _ui_active(shot):
    ui = shot.get("ui_active")
    return ui if isinstance(ui, list) else []


def _is_decision_shot(shot):
    """Decision shot si: section_id de decisión, O ui_active con countdown/loading, O avu de decisión."""
    sec = str(shot.get("section_id") or "")
    if DECISION_SECTION_RE.match(sec):
        return True
    for el in _ui_active(shot):
        if not isinstance(el, dict):
            continue
        eid = str(el.get("element_id") or "")
        font = str(el.get("font") or "")
        if COUNTDOWN_ID_RE.search(eid) or LOADING_ID_RE.search(eid) or \
           COUNTDOWN_FONT_RE.search(font) or LOADING_FONT_RE.search(font):
            return True
    avu = str(shot.get("avu_overlay_clip") or "")
    if avu and AVU_DECISION_RE.search(avu):
        return True
    return False


def _span(el):
    """timestamp_visible_s [start,end] → (start, end) floats o (None, None)."""
    ts = el.get("timestamp_visible_s")
    if isinstance(ts, (list, tuple)) and len(ts) == 2:
        try:
            return float(ts[0]), float(ts[1])
        except (TypeError, ValueError):
            return None, None
    return None, None


def _count_digits(text):
    """Cuenta dígitos en un text de countdown ('3-2-1' → 3, '3 2 1 0' → 4). Default 3 si no hay."""
    digits = re.findall(r"\d", str(text or ""))
    return len(digits) if digits else 3


def extract_countdown_digit_duration(shot):
    """countdown span / n_dígitos. Prefiere ui_active countdown; fallback ninguno → None."""
    for el in _ui_active(shot):
        if not isinstance(el, dict):
            continue
        eid = str(el.get("element_id") or "")
        font = str(el.get("font") or "")
        if COUNTDOWN_ID_RE.search(eid) or COUNTDOWN_FONT_RE.search(font):
            start, end = _span(el)
            if start is not None and end is not None and end > start:
                n = _count_digits(el.get("text"))
                if n > 0:
                    return (end - start) / n, {"span": [start, end], "n_digits": n}
    return None, None


def extract_loading_visible_s(shot):
    """span de visibilidad de la loading bar (NO el fill medido — eso es del render)."""
    for el in _ui_active(shot):
        if not isinstance(el, dict):
            continue
        eid = str(el.get("element_id") or "")
        font = str(el.get("font") or "")
        if LOADING_ID_RE.search(eid) or LOADING_FONT_RE.search(font):
            start, end = _span(el)
            if start is not None and end is not None and end > start:
                return round(end - start, 3)
    return None


def _countdown_start_abs(shot, shot_start_abs):
    """Timestamp ABSOLUTO de inicio del countdown = shot_start_abs + countdown ui_active start."""
    for el in _ui_active(shot):
        if not isinstance(el, dict):
            continue
        eid = str(el.get("element_id") or "")
        font = str(el.get("font") or "")
        if COUNTDOWN_ID_RE.search(eid) or COUNTDOWN_FONT_RE.search(font):
            start, _end = _span(el)
            if start is not None and shot_start_abs is not None:
                return shot_start_abs + start
    return None


def build_shot_start_abs_map(spec):
    """Mapa shot_id → timestamp ABSOLUTO de inicio en el timeline, acumulando duration_intent_s
    en orden de shot_list. Es la mejor aproximación del timeline desde el SPEC (los timestamps de
    narration_script son intent absolutos pero no todos los shots tienen narración)."""
    out = {}
    t = 0.0
    for s in spec.get("shot_list") or []:
        if not isinstance(s, dict):
            continue
        sid = s.get("shot_id")
        if sid is None:
            continue
        out[sid] = t
        try:
            d = float(s.get("duration_intent_s") or 0.0)
        except (TypeError, ValueError):
            d = 0.0
        t += d
    return out


def build_narration_abs_index(spec):
    """Índice de los segmentos NARRATOR con timestamp_intent_s absoluto: shot_id → (start_abs, end_abs).

    start_abs = mínimo de los starts del shot, end_abs = máximo de los ends. Usado para (a) el
    pause-beat (fin narración → inicio countdown) y (b) la verificación de clock-consistency (el
    narration-absolute clock vs el cumulative-duration clock — si divergen, pause-beat NO es
    confiable). Preferimos el timestamp_intent_s absoluto (intent canónico de timeline del arquitecto)."""
    per_shot = {}
    for seg in spec.get("narration_script") or []:
        if not isinstance(seg, dict):
            continue
        if str(seg.get("speaker") or "") != "narrator":
            continue
        sid = seg.get("shot_id_anchor")
        ts = seg.get("timestamp_intent_s")
        if sid and isinstance(ts, (list, tuple)) and len(ts) == 2:
            try:
                start, end = float(ts[0]), float(ts[1])
            except (TypeError, ValueError):
                continue
            cur = per_shot.get(sid)
            if cur is None:
                per_shot[sid] = (start, end)
            else:
                per_shot[sid] = (min(cur[0], start), max(cur[1], end))
    return per_shot


def shot_narration_wpm_checks(shot):
    """wpm_checks del narration_in_this_shot del shot, clasificado por rol.

    wpm = words / duration_intent_s * 60. Si no hay narración o dur → []."""
    text = shot.get("narration_in_this_shot")
    if not text or not str(text).strip():
        return []
    try:
        dur = float(shot.get("duration_intent_s") or 0.0)
    except (TypeError, ValueError):
        dur = 0.0
    if dur <= 0:
        return []
    words = len(str(text).split())
    wpm = words / dur * 60.0
    role = classify_segment(text)
    return [{"role": role, "wpm": round(wpm, 1), "words": words, "dur_s": dur}]


def shot_freeze_declared(shot):
    """¿El SPEC DECLARA freeze/near-frozen para este shot? (contexto report-only, NO render)."""
    trav = str(shot.get("pov_traversal") or shot.get("motion_type") or "").strip().lower()
    if trav in FREEZE_TOKENS:
        return True
    lut = str(shot.get("visual_style_lut") or "").lower()
    if "freeze" in lut:
        return True
    avu = str(shot.get("avu_overlay_clip") or "").lower()
    if "freeze" in avu:
        return True
    return False


# Tolerancia (s) entre el cumulative-duration clock y el narration-absolute clock en el decision
# shot para considerar el pause-beat measurement-grade (mismo clock). Más allá → cross-clock → report-only.
PAUSE_BEAT_CLOCK_TOLERANCE_S = 1.0


def extract_decision_shots(spec):
    """shot_list → estructuras puras para evaluate_decision_ui_pacing (solo decision shots).

    pause_beat = countdown_start_abs − narración_end_abs del MISMO decision shot. PERO el SPEC tiene
    DOS relojes: el cumulative-duration (suma de duration_intent_s, que ubica el countdown shot-rel)
    y el narration-absolute (timestamp_intent_s de narration_script). Si en el decision shot esos
    dos relojes divergen > PAUSE_BEAT_CLOCK_TOLERANCE_S, restar uno contra otro mezcla clocks y el
    pause-beat NO es confiable → se marca pause_beat_clock_consistent=False (evaluate lo degrada a
    report-only, NO inventa la medición). Si la narración vive en un shot previo (decision shot solo
    UI) → pause_beat None (report-only)."""
    shot_start_abs = build_shot_start_abs_map(spec)
    narration_abs = build_narration_abs_index(spec)
    out = []
    for s in spec.get("shot_list") or []:
        if not isinstance(s, dict) or not s.get("shot_id"):
            continue
        if not _is_decision_shot(s):
            continue
        sid = s["shot_id"]
        digit_dur, _meta = extract_countdown_digit_duration(s)

        # pause beat: countdown_start_abs − narración_end_abs del decision shot
        pause_beat = None
        clock_consistent = False
        cum_start = shot_start_abs.get(sid)
        cd_start_abs = _countdown_start_abs(s, cum_start)
        nar = narration_abs.get(sid)
        if cd_start_abs is not None and nar is not None:
            nar_start_abs, nar_end_abs = nar
            pause_beat = round(cd_start_abs - nar_end_abs, 3)
            # clock-consistency: ¿el cumulative-duration start del shot coincide con el narration
            # absolute start del mismo shot? (ambos ubican el MISMO instante en su propio reloj)
            if cum_start is not None:
                clock_consistent = abs(cum_start - nar_start_abs) <= PAUSE_BEAT_CLOCK_TOLERANCE_S

        out.append({
            "shot_id": sid,
            "countdown_digit_duration_s": (round(digit_dur, 3) if digit_dur is not None else None),
            "countdown_pause_beat_s": pause_beat,
            "pause_beat_clock_consistent": clock_consistent,
            "wpm_checks": shot_narration_wpm_checks(s),
            "freeze_declared": shot_freeze_declared(s),
            "loading_visible_s": extract_loading_visible_s(s),
        })
    return out


# ════════════════════════════════════════════════════════════════════════════════════════════
# RUNTIME
# ════════════════════════════════════════════════════════════════════════════════════════════

def find_bands_json(start, override):
    """Resuelve el aggregate JSON: --bands-json explícito > path canónico subiendo desde start."""
    if override:
        p = Path(override)
        return p if p.exists() else None
    from ai_video.errors import ConfigError
    from ai_video.paths import repo_root

    try:
        canonical = repo_root() / DEFAULT_BANDS_RELPATH
        if canonical.exists():
            return canonical
    except ConfigError:
        pass
    cur = Path(start).resolve()
    for parent in [cur] + list(cur.parents):
        cand = parent / DEFAULT_BANDS_RELPATH
        if cand.exists():
            return cand
    return None


def main():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--format", required=True,
                        help="formato del SPEC (agnostic-by-design — el path de bandas usa horror-choice namespaced)")
    parser.add_argument("--spec", required=True, help="path al CREATIVE-SPEC.yaml")
    parser.add_argument("--bands-json", default=None,
                        help=f"override del aggregate JSON (default: sube buscando {DEFAULT_BANDS_RELPATH})")
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
        print("ERROR: SPEC missing 'video_capabilities' block (Pattern 7 §1.6 mandatory). Bug #9.",
              file=sys.stderr)
        return 2

    fmt_type = str(caps.get("format_type") or "")
    has_ui = bool(caps.get("has_layer_4_ui", False))
    applies = (fmt_type in UI_FORMAT_TYPES) or has_ui

    if args.dry_run:
        print(f"format: {args.format}\nspec: {spec_path}\nformat_type: {fmt_type}\n"
              f"has_layer_4_ui: {has_ui}\nbranch: {'decision_ui_pacing_check' if applies else 'not_applicable'}\n"
              f"decision_shots: {len(extract_decision_shots(spec))}")
        return 0

    if not applies:
        print(json.dumps({
            "format": args.format, "overall_status": "not_applicable",
            "detail": (f"format_type='{fmt_type}' ∉ {list(UI_FORMAT_TYPES)} y has_layer_4_ui=false → "
                       "sin capa UI de decisión que validar (Q22a no aplica)"),
        }, indent=2, ensure_ascii=False))
        return 0

    bands_path = find_bands_json(spec_path, args.bands_json)
    if bands_path is None:
        print("ERROR: aggregate-canonical-bands.json no encontrado (ni --bands-json ni el path "
              f"canónico {DEFAULT_BANDS_RELPATH}). Sin bandas medidas no se puede validar. "
              "Correr measure-canonical-decision-ui-pacing.py primero.", file=sys.stderr)
        return 2
    try:
        with open(bands_path) as f:
            bands = json.load(f)
    except (OSError, json.JSONDecodeError) as e:
        print(f"ERROR: no se pudo leer/parsear bands JSON {bands_path}: {e}", file=sys.stderr)
        return 2

    decision_shots = extract_decision_shots(spec)
    ok, results = evaluate_decision_ui_pacing(decision_shots, bands)

    # Params del render no medibles del SPEC → forward explícito (NO inventados).
    forward = [{"param": p, "status": "skipped_forward", "detail": why} for p, why in RENDER_ONLY_PARAMS]

    fail_shots = [r for r in results if r["status"] == "fail"]
    report = {
        "format": args.format,
        "spec": str(spec_path),
        "bands_json": str(bands_path),
        "bands_source_refs": bands.get("source_refs"),
        "min_values_for_band": MIN_VALUES_FOR_BAND,
        "overall_status": "pass" if ok else "fail",
        "overall_pass": ok,
        "decision_shots_found": len(decision_shots),
        "fail_shot_count": len(fail_shots),
        "shots": results,
        "render_only_params_forward": forward,
    }
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
