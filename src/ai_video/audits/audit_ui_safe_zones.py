#!/usr/bin/env python3
"""audit-ui-safe-zones.py — HR#4 UI safe-zones gate (Y-position empírico).

BUG REAL que cierra (caso disparador drift 2026-06-04): la posición vertical de
la loading bar quedó codificada como **Y48** en CLAUDE.md HR#4 pero **Y52** en
INGENIERO-CHOICE-CORE §2 — drift de 4pp en la fuente de autoridad. Peor: el
F1-UI-SAFE-ZONES.json (bandas medidas n=10 referentes virales) EXISTÍA y NINGÚN
script lo leía — caption Y62 estaba HARDCODEADO en build_clip_atomic.py. HR#4 era
`prose_only`: nadie verificaba que un overlay del index.html cayera DENTRO de la
banda empírica, ni que loading bar y countdown no se solaparan.

POR QUÉ NO LO CAZABA NADIE:
  - `audit-frames.py` (Gemini Vision) ve "hay un caption" / "hay overlap" de forma
    holística y subjetiva — NO mide y_pct contra una banda p25-p75 determinística.
  - `audit-spec-completeness.py` cuenta EXISTENCIA del overlay (¿está wired el
    countdown / loading bar?) pero NO razona sobre su POSICIÓN vertical.
  - Las constantes vivían en prosa duplicada (CLAUDE.md vs INGENIERO-CHOICE-CORE)
    con drift real, y en código hardcodeado — sin un gate que leyera F1 como
    única fuente, cualquiera de los tres valores podía shipear.
  Un check INGENUO compararía la y_pct contra un número hardcodeado (justo el
  antipatrón). Acá la banda de los 4 elementos F1 (captions_narration /
  character_name_labels / warning_text / watermark) se LEE de F1 vía
  lib/empirical_bands.ui_band() — la prosa apunta, nunca repite. Loading bar y
  countdown NO tienen banda confiable en F1 (n=1) → defaults de módulo con
  autoridad INGENIERO-CHOICE-CORE §2, overridables por CLI.

REGLA:
  Por cada overlay del index.html cuya y_pct (centro del elemento, origen
  top-left, sobre 1080x1920) se pueda extraer y clasificar:
    - elemento con banda (F1 o default) → y_pct DEBE caer en [lo-tol, hi+tol]
      (tolerancia ±2pp configurable). Fuera de banda → FAIL.
    - loading bar y countdown ambos presentes → |y_loading - y_countdown| ≥ 6pp
      (INGENIERO-CHOICE-CORE §2: "≥6% sep de countdown Y46"). Solape → FAIL.
  Elemento AUSENTE del HTML → not-checked / skipped (NO FAIL): puede ser path
  HYBRID sin ese overlay (captions BURNED per clip, sin div estructural, etc.).

Capability-gate (HR#4): format_type ∈ {interactive_choice, reel} OR resolución
vertical 1080x1920. Si NO aplica → not_applicable (exit 0).
video_capabilities ausente → Bug #9 (exit 2). Agnostic-by-design: --format REQUIRED.

DISEÑO TESTEABLE: lógica pura en evaluate_safe_zones(elements, bands) — recibe
overlays ya extraídos [{element_type, y_pct, raw}] + bandas resueltas; el wrapper
runtime parsea SPEC (capabilities) + HTML (regex robusto, sin bs4/lxml) + resuelve
bandas vía lib/empirical_bands.py.

Exit: 0 PASS / not_applicable · 1 FAIL · 2 can't-measure (Bug #9 / SPEC|HTML ausente).
Authority: CLAUDE.md HR#4 + choice-format-core/INGENIERO-CHOICE-CORE §2 +
referent-analysis/<format>/F1-UI-SAFE-ZONES.json. HR#26 companion test.
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

# Permite importar lib/empirical_bands.py tanto desde templates/scripts/ (repo)
# como desde <proyecto>/scripts/ (copia bootstrap) — mismo patrón que qa-gate.py.
from ai_video.core import empirical_bands as eb

# ── Frame canónico Reel vertical ──────────────────────────────────────────────
FRAME_W = 1080
FRAME_H = 1920

# ── Tolerancia + separación ───────────────────────────────────────────────────
DEFAULT_TOLERANCE_PP = 2.0  # ±2pp sobre la banda p25-p75 (configurable --tolerance)
MIN_SEPARATION_PP = 6.0  # loading bar vs countdown — INGENIERO-CHOICE-CORE §2

# ── Defaults NO medidos en F1 (n=1, banda no confiable) ───────────────────────
# Authority: choice-format-core/INGENIERO-CHOICE-CORE §2 — NO medida en F1;
# override via --loading-band / --countdown-y.
DEFAULT_LOADING_BAND = (44.0, 52.0)  # §2: "44-52% baseline / 52% en decision shots"
DEFAULT_COUNTDOWN_Y = 46.0  # §2: countdown_y_pct = 46

# Capability gate HR#4: estos format_type disparan la regla de safe zones.
SAFE_ZONE_FORMAT_TYPES = {"interactive_choice", "reel"}

# Elementos con banda empírica en F1-UI-SAFE-ZONES.json que SÍ enforce-amos.
# ⚠️ watermark EXCLUIDO a propósito del enforce: la banda F1 (Y75-84%) mide el
# watermark IG-NATIVO de la pantalla grabada del referente ("overlaps IG-native
# bottom UI region", note explícita en F1) — NO un target de diseño. Nuestro
# watermark canónico @elige_tucompanero va arriba (Y4, INGENIERO-CHOICE-CORE +
# memoria feedback_watermark_handle). Enforcar la banda F1 daría falso-positivo en
# todos nuestros renders. Se REPORTA (report-only), nunca FAIL.
F1_ELEMENTS = (
    "captions_narration",
    "character_name_labels",
    "warning_text",
)
# Elementos que se clasifican y reportan pero NO se validan contra banda:
#   watermark      → banda F1 es artefacto screen-recording (ver arriba).
#   choice_buttons → sin banda F1 confiable (n=1) + colocación bottom-anchored
#                    variable per-video; se reporta su y_pct pero no se enforce.
REPORT_ONLY_ELEMENTS = ("watermark", "choice_buttons")

# Clasificación id/class → element_type. Orden = prioridad (más específico primero).
# Se evalúa contra el texto combinado de id+class (lowercased).
# ⚠️ choice_button ≠ character_name_labels: los botones A/B viven abajo (Y~12-25%
# desde el fondo, bottom-anchored) y NO tienen banda F1 propia (n=1) → report-only.
# Los name labels de personaje viven ARRIBA (Y~11-33%, banda F1 n=8). Lumparlos
# daría falso-positivo (botón abajo evaluado contra banda de name-label arriba).
ELEMENT_KEYWORDS = [
    ("loading_bar", ("loading_bar", "loading-bar", "loadingbar", "loader")),
    ("countdown", ("countdown",)),
    (
        "choice_buttons",
        ("choice_button", "choice-button", "choicebutton", "btn-a", "btn-b", "button-a", "button-b"),
    ),
    (
        "character_name_labels",
        ("name-label", "name_label", "namelabel", "char-name", "char_name", "speaker-name", "speaker_name"),
    ),
    ("warning_text", ("warning", "danger-text", "alert-text")),
    ("watermark", ("watermark", "handle")),
    (
        "captions_narration",
        ("caption-wrap", "caption_wrap", "captionwrap", "caption", "subtitle", "narration-caption"),
    ),
]


# ════════════════════════════════════════════════════════════════════════════
# LÓGICA PURA — testeable sin filesystem
# ════════════════════════════════════════════════════════════════════════════


def classify_element(ident: str, classes: str) -> str | None:
    """element_type desde id + class (keyword match). None si no clasifica."""
    hay = f"{ident or ''} {classes or ''}".lower()
    for etype, kws in ELEMENT_KEYWORDS:
        if any(kw in hay for kw in kws):
            return etype
    return None


def style_to_y_pct(style: str, frame_h: int = FRAME_H) -> float | None:
    """Centro vertical (y_pct, origen top-left) desde un inline style.

    Soporta:
      - top:<px|%>  → ancla superior.   bottom:<px|%>  → ancla inferior.
      - height:<px|%> para hallar el centro de la caja.
      - transform: translateY(-50%) / translate(x,-50%) → la caja está
        centrada sobre el ancla (patrón canónico HYBRID loading bar).
    Devuelve None si no hay top/bottom parseable (no podemos ubicarlo).
    """
    if not style:
        return None
    s = style.lower()

    def _len_to_px(val: str, unit: str) -> float | None:
        try:
            num = float(val)
        except ValueError:
            return None
        if unit == "%":
            return num / 100.0 * frame_h
        return num  # px

    def _grab(prop: str) -> float | None:
        m = re.search(rf"(?:^|[;{{\s]){prop}\s*:\s*(-?\d+(?:\.\d+)?)\s*(px|%)", s)
        if not m:
            return None
        return _len_to_px(m.group(1), m.group(2))

    top_px = _grab("top")
    bottom_px = _grab("bottom")
    height_px = _grab("height")

    # translateY centrado sobre el ancla (translateY(-50%) o translate(_, -50%))
    centered = bool(
        re.search(r"transform\s*:[^;]*translatey\s*\(\s*-\s*50%\s*\)", s)
        or re.search(r"transform\s*:[^;]*translate\s*\([^,]+,\s*-\s*50%\s*\)", s)
    )

    if top_px is not None:
        if centered:
            return top_px / frame_h * 100.0
        # ancla superior: centro = top + height/2 (height/2=0 si no se conoce)
        center = top_px + (height_px or 0.0) / 2.0
        return center / frame_h * 100.0

    if bottom_px is not None:
        # bottom desde el borde inferior. box_bottom_y = frame_h - bottom_px.
        box_bottom_y = frame_h - bottom_px
        if centered:
            return box_bottom_y / frame_h * 100.0
        # ancla inferior: centro = box_bottom_y - height/2
        center = box_bottom_y - (height_px or 0.0) / 2.0
        return center / frame_h * 100.0

    return None


def evaluate_safe_zones(
    elements,
    bands,
    *,
    tolerance_pp=DEFAULT_TOLERANCE_PP,
    min_sep_pp=MIN_SEPARATION_PP,
    report_only=REPORT_ONLY_ELEMENTS,
):
    """PURO. Valida overlays contra bandas + separación loading/countdown.

    elements = [{element_type, y_pct, raw}] (overlays ya extraídos y clasificados).
    bands    = {element_type: (lo, hi, source)} — banda p25-p75 + string de autoridad.
               Un element_type sin entrada en `bands` → reportado como
               band_unknown (skipped, no FAIL).
    report_only = element_types que se reportan pero NUNCA fallan (ej. watermark,
               cuya banda F1 es un artefacto de screen-recording, no un target).

    Devuelve (ok: bool, reasons: list[dict]). FAIL si:
      - una y_pct cae fuera de [lo-tol, hi+tol] (excepto report_only), o
      - loading bar y countdown presentes con |Δy| < min_sep_pp.
    """
    reasons = []
    ok = True
    # mapa element_type → y_pcts observadas (para separación)
    by_type: dict[str, list[float]] = {}

    for e in elements:
        etype = e.get("element_type")
        raw = e.get("raw", "")
        y = e.get("y_pct")
        if y is None:
            reasons.append(
                {
                    "element_type": etype,
                    "y_pct": None,
                    "status": "skipped",
                    "detail": f"'{raw}' sin posición vertical parseable → not-checked",
                }
            )
            continue
        by_type.setdefault(etype, []).append(y)

        if etype in report_only:
            reasons.append(
                {
                    "element_type": etype,
                    "y_pct": round(y, 1),
                    "status": "skipped",
                    "detail": (
                        f"'{raw}' y_pct={y:.1f} — '{etype}' es report-only "
                        f"(banda F1 = artefacto screen-recording, no enforce) → not-checked"
                    ),
                }
            )
            continue

        band = bands.get(etype)
        if band is None:
            reasons.append(
                {
                    "element_type": etype,
                    "y_pct": round(y, 1),
                    "status": "skipped",
                    "detail": f"'{raw}' y_pct={y:.1f} — sin banda de autoridad para '{etype}' → not-checked",
                }
            )
            continue
        lo, hi, src = band
        if lo is None or hi is None:
            reasons.append(
                {
                    "element_type": etype,
                    "y_pct": round(y, 1),
                    "status": "skipped",
                    "detail": (f"'{raw}' y_pct={y:.1f} — banda '{etype}' no confiable ({src}) → not-checked"),
                }
            )
            continue
        lo_t, hi_t = lo - tolerance_pp, hi + tolerance_pp
        if lo_t <= y <= hi_t:
            reasons.append(
                {
                    "element_type": etype,
                    "y_pct": round(y, 1),
                    "status": "ok",
                    "band": [round(lo, 1), round(hi, 1)],
                    "tolerance_pp": tolerance_pp,
                    "detail": f"'{raw}' y_pct={y:.1f} ∈ banda [{lo:.1f},{hi:.1f}]±{tolerance_pp}pp ({src}) ✓",
                }
            )
        else:
            ok = False
            reasons.append(
                {
                    "element_type": etype,
                    "y_pct": round(y, 1),
                    "status": "fail",
                    "band": [round(lo, 1), round(hi, 1)],
                    "tolerance_pp": tolerance_pp,
                    "detail": (
                        f"'{raw}' y_pct={y:.1f} FUERA de banda safe-zone "
                        f"[{lo:.1f},{hi:.1f}]±{tolerance_pp}pp ({src}) — HR#4"
                    ),
                }
            )

    # Separación loading bar vs countdown (si ambos presentes con y_pct conocida)
    loads = by_type.get("loading_bar", [])
    counts = by_type.get("countdown", [])
    if loads and counts:
        worst = None
        for yl in loads:
            for yc in counts:
                sep = abs(yl - yc)
                if worst is None or sep < worst[0]:
                    worst = (sep, yl, yc)
        sep, yl, yc = worst
        if sep < min_sep_pp:
            ok = False
            reasons.append(
                {
                    "element_type": "loading_bar↔countdown",
                    "y_pct": None,
                    "status": "fail",
                    "detail": (
                        f"loading bar Y{yl:.1f} solapa countdown Y{yc:.1f} "
                        f"(sep {sep:.1f}pp < {min_sep_pp}pp mínimo — INGENIERO-CHOICE-CORE §2)"
                    ),
                }
            )
        else:
            reasons.append(
                {
                    "element_type": "loading_bar↔countdown",
                    "y_pct": None,
                    "status": "ok",
                    "detail": f"loading bar Y{yl:.1f} vs countdown Y{yc:.1f}: sep {sep:.1f}pp ≥ {min_sep_pp}pp ✓",
                }
            )

    return ok, reasons


# ════════════════════════════════════════════════════════════════════════════
# WRAPPER RUNTIME — parsea SPEC + HTML + resuelve bandas
# ════════════════════════════════════════════════════════════════════════════

# regex robusto: cualquier <tag ...> con un style="..."; extrae id, class, style.
_TAG_RE = re.compile(r"<(?:div|span|p|section)\b([^>]*)>", re.IGNORECASE)
_ATTR_RE = lambda name: re.compile(rf'{name}\s*=\s*"([^"]*)"', re.IGNORECASE)
_ID_RE = _ATTR_RE("id")
_CLASS_RE = _ATTR_RE("class")
_STYLE_RE = _ATTR_RE("style")


def parse_html_overlays(html_text: str, frame_h: int = FRAME_H):
    """Extrae overlays clasificables con y_pct desde el index.html (regex)."""
    elements = []
    for m in _TAG_RE.finditer(html_text):
        attrs = m.group(1)
        idm = _ID_RE.search(attrs)
        cm = _CLASS_RE.search(attrs)
        sm = _STYLE_RE.search(attrs)
        ident = idm.group(1) if idm else ""
        classes = cm.group(1) if cm else ""
        style = sm.group(1) if sm else ""
        etype = classify_element(ident, classes)
        if etype is None:
            continue
        y = style_to_y_pct(style, frame_h)
        elements.append(
            {
                "element_type": etype,
                "y_pct": y,
                "raw": (ident or classes or "?").strip()[:48],
            }
        )
    return elements


def resolve_bands(
    format_name,
    *,
    fallback_format=None,
    loading_band=DEFAULT_LOADING_BAND,
    countdown_y=DEFAULT_COUNTDOWN_Y,
    band_base=None,
):
    """bands = {element_type: (lo, hi, source_str)}.

    F1 elements → lib/empirical_bands.ui_band(). loading_bar/countdown →
    defaults de módulo (autoridad INGENIERO-CHOICE-CORE §2, overridables CLI).
    """
    bands = {}
    for el in F1_ELEMENTS:
        lo, hi, n = eb.ui_band(format_name, el, "y_pct", fallback_format=fallback_format, base=band_base)
        if lo is None:
            bands[el] = (None, None, f"F1:{format_name} n={n} (<4, banda no confiable)")
        else:
            bands[el] = (lo, hi, f"F1:{format_name} p25-p75 n={n}")
    # loading bar: banda directa (no es centro de un punto medido)
    bands["loading_bar"] = (
        loading_band[0],
        loading_band[1],
        "INGENIERO-CHOICE-CORE §2 (no F1; --loading-band)",
    )
    # countdown: punto único Y46 → banda simétrica ±tol manejada en evaluate
    bands["countdown"] = (countdown_y, countdown_y, "INGENIERO-CHOICE-CORE §2 (no F1; --countdown-y)")
    return bands


def main():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--format", required=True, help="formato (agnostic-by-design)")
    parser.add_argument("--spec", required=True, help="creative-specs/<id>.yaml (capabilities)")
    parser.add_argument("--html", required=True, help="<proyecto>/index.html (HyperFrames composition)")
    parser.add_argument(
        "--fallback-format",
        default=None,
        help="formato del que heredar F1 si el activo es pre-empírico (ej. horror-choice)",
    )
    parser.add_argument(
        "--tolerance",
        type=float,
        default=DEFAULT_TOLERANCE_PP,
        help=f"tolerancia ±pp sobre la banda (default {DEFAULT_TOLERANCE_PP})",
    )
    parser.add_argument(
        "--min-separation",
        type=float,
        default=MIN_SEPARATION_PP,
        help=f"separación mínima loading↔countdown pp (default {MIN_SEPARATION_PP})",
    )
    parser.add_argument(
        "--loading-band",
        default=None,
        help='override banda loading bar "lo,hi" (default 44,52 — INGENIERO-CHOICE-CORE §2)',
    )
    parser.add_argument(
        "--countdown-y",
        type=float,
        default=DEFAULT_COUNTDOWN_Y,
        help=f"override countdown y_pct (default {DEFAULT_COUNTDOWN_Y})",
    )
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    spec_path = Path(args.spec)
    if not spec_path.exists():
        print(f"ERROR: SPEC not found: {spec_path}", file=sys.stderr)
        return 2
    html_path = Path(args.html)
    if not html_path.exists():
        print(f"ERROR: HTML not found: {html_path}", file=sys.stderr)
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

    fmt_type = caps.get("format_type")
    resolution = str(caps.get("output_resolution", "")).lower().replace(" ", "")
    is_vertical = resolution in ("1080x1920", "1080×1920")
    rule_applies = (fmt_type in SAFE_ZONE_FORMAT_TYPES) or is_vertical

    loading_band = DEFAULT_LOADING_BAND
    if args.loading_band:
        try:
            lo, hi = (float(x) for x in args.loading_band.split(","))
            loading_band = (lo, hi)
        except ValueError:
            print(f"ERROR: --loading-band debe ser 'lo,hi' (got {args.loading_band!r})", file=sys.stderr)
            return 2

    if args.dry_run:
        print(
            f"format: {args.format}\nspec: {spec_path}\nhtml: {html_path}\n"
            f"format_type: {fmt_type}\noutput_resolution: {resolution}\n"
            f"rule_applies (HR#4): {rule_applies}\n"
            f"tolerance_pp: {args.tolerance}\nmin_separation_pp: {args.min_separation}\n"
            f"loading_band: {loading_band}\ncountdown_y: {args.countdown_y}"
        )
        return 0

    if not rule_applies:
        print(
            json.dumps(
                {
                    "format": args.format,
                    "overall_status": "not_applicable",
                    "detail": (
                        f"format_type={fmt_type!r} ∉ {sorted(SAFE_ZONE_FORMAT_TYPES)} y "
                        f"resolución={resolution!r} no es vertical 1080x1920 → HR#4 UI safe zones no aplica"
                    ),
                },
                indent=2,
                ensure_ascii=False,
            )
        )
        return 0

    bands = resolve_bands(
        args.format,
        fallback_format=args.fallback_format,
        loading_band=loading_band,
        countdown_y=args.countdown_y,
    )

    html_text = html_path.read_text(encoding="utf-8", errors="replace")
    elements = parse_html_overlays(html_text)

    ok, reasons = evaluate_safe_zones(
        elements, bands, tolerance_pp=args.tolerance, min_sep_pp=args.min_separation
    )

    fails = [r for r in reasons if r["status"] == "fail"]
    checked = [r for r in reasons if r["status"] in ("ok", "fail")]
    skipped = [r for r in reasons if r["status"] == "skipped"]
    report = {
        "format": args.format,
        "spec": str(spec_path),
        "html": str(html_path),
        "rule_applies": rule_applies,
        "tolerance_pp": args.tolerance,
        "min_separation_pp": args.min_separation,
        "bands_resolved": {k: {"lo": v[0], "hi": v[1], "source": v[2]} for k, v in bands.items()},
        "overall_status": "pass" if ok else "fail",
        "overall_pass": ok,
        "overlays_found": len(elements),
        "checked": len(checked),
        "fails": len(fails),
        "skipped": len(skipped),
        "fail_elements": fails,
        "elements": reasons,
    }
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
