#!/usr/bin/env python3
"""audit-style-markup.py — cierra Q19 (vignette) + Q20 (monospaced names) del pre-render-gate.

BUG REAL que cierra (caso disparador: grep manual del pre-render-gate Q19/Q20):
  El pre-render-gate exige en Q19 que el render tenga vignette aplicado y en Q20
  que los character name labels usen fuente monospaced (referent_validated_patterns
  2026-05-13: monospaced > proportional para nombres; drop-shadow > thick-stroke).
  Ambos chequeos vivían como GREP MANUAL ("¿ves el vignette? ¿la fuente parece
  mono?") — humano cansado dice "sí" sin mirar, y el name label sale en Arial
  (proportional) o el render queda plano sin vignette. Cero gate determinístico.

POR QUÉ NO LO CAZABA NADIE:
  audit-frames.py (Gemini Vision) razona sobre el FRAME renderizado y "no se queja"
  de una fuente proporcional ni de la falta de vignette — son señales sutiles que el
  scoring holístico no penaliza (mismo blind-spot que infló pueblo-v2 a 9.9). Y
  audit-spec-completeness.py cuenta EXISTENCIA de assets/UI, no su ESTILO. Nadie mira
  el markup (CSS/font) del index.html. Un check INGENUO de Q20 buscaría "monospace"
  en cualquier parte del HTML y pasaría aunque la fuente mono esté en un comentario o
  en un elemento que NO es el name label — por eso acá Q20 es una IMPLICACIÓN
  CONDICIONAL: solo exige mono SI hay name labels de personaje presentes (si no hay
  nombres en el HTML → la regla no aplica, no es un FAIL espurio).

REGLA:
  (Q19 vignette) index.html DEBE contener markup de vignette: regex
    (vignette | radial-gradient | box-shadow ... inset). Ausente → FAIL.
  (Q20 monospaced names) SI el HTML contiene name labels de personaje
    (class name-label/caption-name, id choice_button*, o texto matching los
    characters[].name del SPEC) → DEBE haber una fuente monospaced
    (VT323 | Space Mono | Courier | Menlo | Monaco | Consolas | monospace)
    asociada al/los label(s). Implicación condicional: sin name labels → Q20
    not_applicable (NO es FAIL).

Capability-gate: has_captions_baked false → not_applicable (exit 0). Sin overlay
  de UI/captions horneada no hay name-label-en-HTML que estilizar (el estilo se
  define en otro layer). video_capabilities ausente → Bug #9 (exit 2).
  Agnostic-by-design: --format REQUIRED.

DISEÑO TESTEABLE: lógica pura en evaluate_vignette(html_text) y
  evaluate_mono_names(html_text, character_names) — reciben el HTML y la lista de
  nombres ya extraídos; el wrapper runtime parsea SPEC (capabilities + characters)
  y lee el index.html del proyecto.

Exit: 0 PASS·not_applicable / 1 FAIL / 2 can't-measure (Bug #9 / SPEC|HTML ausente).
Authority: pre-render-gate Q19/Q20 + referent_validated_patterns (monospaced para
  names + vignette, 2026-05-13) + referent-analysis/REFERENT-PATTERNS.md. HR#26 companion test.
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

# Authority: pre-render-gate Q19 — markup de vignette aceptado. NO medido en F1
# (es presencia de markup, no una banda numérica). Override no aplica (booleano).
# - "vignette": class/id/comentario explícito.
# - "radial-gradient": técnica CSS canónica de vignette (oscurece bordes).
# - "box-shadow ... inset": vignette por sombra interior (la otra técnica canónica).
_VIGNETTE_PATTERNS = (
    re.compile(r"vignette", re.IGNORECASE),
    re.compile(r"radial-gradient", re.IGNORECASE),
    re.compile(r"box-shadow[^;{}]*\binset\b", re.IGNORECASE),
)

# Authority: referent_validated_patterns (2026-05-13) — character names en fuente
# monospaced (refuta proportional). Familia canónica de fuentes mono aceptadas.
# NO medido en F1 (presencia de font-family, no banda). Override via --mono-fonts.
_DEFAULT_MONO_FONTS = (
    "VT323", "Space Mono", "Courier", "Menlo", "Monaco",
    "Consolas", "Roboto Mono", "IBM Plex Mono", "monospace",
)

# Selectores/atributos que delatan un character name label en el HTML del formato
# choice (heredados del template: class name-label/caption-name + id choice_button*).
_NAME_LABEL_SELECTOR_RE = re.compile(
    r'(?:class|id)\s*=\s*["\'][^"\']*'
    r'(?:name[_-]?label|caption[_-]?name|choice[_-]?button)',
    re.IGNORECASE,
)


# ─────────────────────────── lógica pura (testeable) ───────────────────────────

def evaluate_vignette(html_text, *, patterns=_VIGNETTE_PATTERNS):
    """PURE. Q19 — ¿el HTML contiene markup de vignette?

    Devuelve (ok: bool, detail: dict). FAIL si NINGÚN patrón de vignette aparece.
    """
    matched = []
    for pat in patterns:
        m = pat.search(html_text or "")
        if m:
            matched.append(pat.pattern)
    ok = bool(matched)
    return ok, {
        "check": "Q19_vignette",
        "status": "ok" if ok else "fail",
        "patterns_matched": matched,
        "detail": (
            f"vignette markup presente (matched: {matched})" if ok else
            "NINGÚN markup de vignette (vignette|radial-gradient|box-shadow inset) "
            "en el HTML — render plano sin oscurecimiento de bordes (Q19 FAIL)"
        ),
    }


def _html_text_tokens(html_text):
    """Devuelve el texto visible (entre tags) en MAYÚSCULAS para matching robusto
    de nombres de personaje renderizados como label (DARIO, TOBIAS, IVÁN…)."""
    # quitar comentarios HTML para no matchear nombres mencionados en comentarios
    no_comments = re.sub(r"<!--.*?-->", " ", html_text or "", flags=re.DOTALL)
    # quitar contenido de <script>/<style> (no es texto renderizado)
    no_scripts = re.sub(r"<(script|style)\b.*?</\1>", " ", no_comments,
                        flags=re.DOTALL | re.IGNORECASE)
    inner = re.sub(r"<[^>]+>", " ", no_scripts)  # strip tags
    return inner.upper()


def detect_name_labels(html_text, character_names):
    """PURE. ¿Hay name labels de personaje en el HTML?

    Dos señales (OR): (1) selector canónico name-label/caption-name/choice_button;
    (2) el texto visible contiene alguno de los character_names del SPEC.
    Devuelve (present: bool, evidence: dict).
    """
    selector_hits = _NAME_LABEL_SELECTOR_RE.findall(html_text or "")
    visible = _html_text_tokens(html_text)
    name_hits = []
    for nm in (character_names or []):
        if not nm:
            continue
        # match palabra completa (los names son tokens en mayúsculas en el label)
        if re.search(rf"\b{re.escape(str(nm).strip().upper())}\b", visible):
            name_hits.append(str(nm).strip())
    present = bool(selector_hits) or bool(name_hits)
    return present, {
        "selector_hits": len(selector_hits),
        "name_text_hits": name_hits,
    }


def evaluate_mono_names(html_text, character_names, *, mono_fonts=_DEFAULT_MONO_FONTS):
    """PURE. Q20 — IMPLICACIÓN CONDICIONAL.

    Si NO hay name labels de personaje → not_applicable (NO FAIL).
    Si HAY name labels → DEBE existir una fuente monospaced en el HTML. FAIL si no.

    Nota: el chequeo de fuente busca cualquier mono-font en el markup. Razón: en el
    template choice los name labels comparten stylesheet/style inline con un único
    font-family; exigir co-localización exacta label↔font daría falsos negativos por
    el render por-clip-atomic (HR#25) donde el label se hornea pero el CSS de
    referencia queda en el index.html. La señal load-bearing es: "hay labels Y hay
    mono-font declarada". Si hay labels y CERO mono-font → la fuente es proporcional.
    """
    present, evidence = detect_name_labels(html_text, character_names)
    if not present:
        return True, {
            "check": "Q20_monospaced_names",
            "status": "not_applicable",
            "applies": False,
            "detail": ("HTML sin character name labels (ni selector name-label/"
                       "choice_button ni texto matching characters[].name) → Q20 no aplica"),
            "evidence": evidence,
        }

    mono_found = [f for f in mono_fonts
                  if re.search(rf"\b{re.escape(f)}\b", html_text or "", re.IGNORECASE)]
    ok = bool(mono_found)
    return ok, {
        "check": "Q20_monospaced_names",
        "status": "ok" if ok else "fail",
        "applies": True,
        "mono_fonts_found": mono_found,
        "evidence": evidence,
        "detail": (
            f"name labels presentes + fuente monospaced declarada ({mono_found}) ✓"
            if ok else
            "name labels de personaje PRESENTES pero NINGUNA fuente monospaced "
            f"({list(mono_fonts)}) en el HTML — los nombres salen en fuente proporcional "
            "(Q20 FAIL: referent_validated_patterns exige monospaced para names)"
        ),
    }


def evaluate_style_markup(html_text, character_names, *, mono_fonts=_DEFAULT_MONO_FONTS):
    """PURE. Combina Q19 + Q20. Devuelve (overall_ok, {q19, q20}).

    overall_ok = Q19 ok AND (Q20 ok OR Q20 not_applicable).
    """
    q19_ok, q19 = evaluate_vignette(html_text)
    q20_ok, q20 = evaluate_mono_names(html_text, character_names, mono_fonts=mono_fonts)
    overall_ok = q19_ok and q20_ok  # q20_ok ya es True cuando not_applicable
    return overall_ok, {"Q19_vignette": q19, "Q20_monospaced_names": q20}


# ─────────────────────────── wrapper runtime ───────────────────────────

def extract_character_names(spec):
    """Lee characters[].name (o .character_name / .name_label) del SPEC."""
    names = []
    for c in (spec.get("characters") or []):
        if not isinstance(c, dict):
            continue
        for k in ("name", "character_name", "name_label"):
            v = c.get(k)
            if isinstance(v, str) and v.strip():
                names.append(v.strip())
                break
    return names


def resolve_html_path(args, spec_path):
    """Resuelve el index.html: --html explícito o heurística <spec_dir>/../<stem>/<html>."""
    if args.html:
        return Path(args.html)
    guess = spec_path.parent.parent / spec_path.stem / "index.html"
    return guess


def main():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--format", required=True)
    parser.add_argument("--spec", required=True)
    parser.add_argument("--html", default=None,
                        help="index.html del proyecto. Default: <spec_dir>/../<spec_stem>/index.html")
    parser.add_argument("--mono-fonts", default=None,
                        help="CSV override de fuentes monospaced aceptadas (Q20).")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    mono_fonts = _DEFAULT_MONO_FONTS
    if args.mono_fonts:
        mono_fonts = tuple(f.strip() for f in args.mono_fonts.split(",") if f.strip())

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

    has_captions = bool(caps.get("has_captions_baked", False))
    character_names = extract_character_names(spec)

    if args.dry_run:
        print(f"format: {args.format}\nspec: {spec_path}\n"
              f"has_captions_baked: {has_captions}\n"
              f"character_names: {character_names}\n"
              f"branch: {'style_markup_check' if has_captions else 'not_applicable'}\n"
              f"mono_fonts: {list(mono_fonts)}")
        return 0

    if not has_captions:
        print(json.dumps({
            "format": args.format, "overall_status": "not_applicable",
            "detail": ("has_captions_baked=false → style markup check skipped "
                       "(sin overlay de UI/captions horneada que estilizar en HTML)"),
        }, indent=2, ensure_ascii=False))
        return 0

    html_path = resolve_html_path(args, spec_path)
    if not html_path.exists():
        print(f"ERROR: index.html not found: {html_path}. Bug #9 (can't measure markup).",
              file=sys.stderr)
        return 2

    html_text = html_path.read_text(encoding="utf-8")
    overall_ok, checks = evaluate_style_markup(html_text, character_names, mono_fonts=mono_fonts)

    fails = [c for c in checks.values() if c["status"] == "fail"]
    report = {
        "format": args.format,
        "spec": str(spec_path),
        "html": str(html_path),
        "character_names_from_spec": character_names,
        "mono_fonts_accepted": list(mono_fonts),
        "overall_status": "pass" if overall_ok else "fail",
        "overall_pass": overall_ok,
        "fail_checks": [c["check"] for c in fails],
        "checks": checks,
    }
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if overall_ok else 1


if __name__ == "__main__":
    sys.exit(main())
