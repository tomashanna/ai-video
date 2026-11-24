#!/usr/bin/env python3
"""audit-language-style.py — gate determinístico de 4 preferencias permanentes del creator.

Convierte a código 4 reglas de estilo/idioma que hoy viven SOLO como prosa en memorias
(prose_only). Las 4 tienen un bug SHIPPED real como caso disparador. Un solo gate, 4 checks
seleccionables con --checks (voseo / cliche / names / handle).

BUG REAL que cierra (4 casos disparadores, todos shipped):
  (1) voseo  — matadero post-ship 2026-05-20: el video shipeó con voseo argentino
       ("elegís", "te convertís") cuando el canónico es Spanish NEUTRAL (tú/eliges/decides).
       Audiencia international Instagram. Authority: memoria feedback_spanish_neutral.
  (2) cliche — matadero post-ship 2026-05-20: narración con frases horror overused
       ("cena que nunca acaba", "bucle eterno"). Authority: feedback_anti_cliche_horror.
  (3) names  — cinema-abandonado iter1 2026-05-20: characters con nombres = oficio
       ("Proyector", "Acomodador") en vez de nombres reales inventados (Bruno/Pablo/Hugo).
       Los 8/8 refs canónicos usan real first names. Authority: feedback_character_real_names.
  (4) handle — el handle PROPIO canónico es @elige_tucompanero; @referent-a es
       REFERENCE-only (NUNCA como watermark/channel propio). Authority: feedback_watermark_handle.

POR QUÉ NO LO CAZABA NADIE:
  Ningún gate determinístico inspecciona el TEXTO ESPAÑOL del SPEC. audit-spec-completeness
  cuenta inventario de assets; audit-frames mira píxeles; Gemini holístico puntúa atmósfera
  y NO reporta confiablemente "esto es voseo" ni "este nombre es un oficio" — son reglas
  LÉXICAS categóricas (lista cerrada de palabras/frases), exactamente lo que un LLM-judge
  pasa por alto y un check de lexicón con word-boundary caza siempre. Estas 4 reglas vivían
  en memorias prose_only sin enforcement → re-aparecen video tras video.

REGLA:
  (1) voseo  — lexicón voseo con word-boundary {vos, decís, elegís, tenés, querés, podés,
       sabés, mirá, andá, escuchá, agarrá, sos, acordate, fijate} en narration_script[].text_canonical
       + shot_list[].dialog_text + captions (ui_overlay_elements[].text de tipo caption/warning).
       Falso-positivo evitado: 'vosotros' NO es voseo (word-boundary lo excluye); 'sos' standalone
       SÍ es voseo ('sos un' incluido); el canónico = tú/dices/eliges.
  (2) cliche — blacklist case-insensitive de frases overused (CLICHE_PHRASES, extensible por
       módulo / --extra-cliche) sobre los mismos textos.
  (3) names  — characters[].name (+ star_name si existe) NO debe ser sustantivo de OFICIO
       (JOB_NAME_BLACKLIST). El campo de DESCRIPCIÓN (visual_signature/role) PUEDE mencionar
       el oficio (válido) — SOLO el NAME field falla.
  (4) handle — si el SPEC declara channel/watermark (project.channel / channel_signature.
       watermark_handle / meta.watermark / + HTML watermark), debe ser @elige_tucompanero.
       FAIL si aparece @referent-a como handle PROPIO en esos campos. Mención en
       comentarios/why_relevant/references como REFERENCE NO falla (solo campos de handle propio).

Capability-gate: este gate es UNIVERSAL (estilo/idioma aplica a todo SPEC con texto). NO se
  desactiva por capability — corre siempre que haya video_capabilities. video_capabilities
  ausente → Bug #9 (exit 2): un SPEC sin el bloque Pattern 7 §1.6 está mal formado.
  --format REQUERIDO (agnostic-by-design).

DISEÑO TESTEABLE: lógica PURA en evaluate_voseo / evaluate_cliche / evaluate_names /
  evaluate_handle — reciben datos YA extraídos (listas de textos / nombres / handles), sin
  filesystem. El wrapper runtime parsea el SPEC (yaml) + el HTML (regex) y los alimenta.

Exit: 0 PASS / not_applicable · 1 FAIL · 2 can't-measure (Bug #9 / SPEC ausente / pyyaml).
Authority: memorias feedback_spanish_neutral + feedback_anti_cliche_horror +
  feedback_character_real_names + feedback_watermark_handle + CLAUDE.md MEMORY index.
  NO medidas en F1 (reglas léxicas categóricas, no bandas numéricas) → constantes de módulo.
  HR#26 companion test: test_audit-language-style.py.
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

ALL_CHECKS = ("voseo", "cliche", "names", "handle")

# ── (1) Lexicón VOSEO argentino ──────────────────────────────────────────────
# Authority: feedback_spanish_neutral — NO medido en F1 (regla léxica categórica).
# Canónico = Spanish neutral (tú/dices/eliges). Cada entrada se matchea con word-boundary
# (\b...\b) case-insensitive → 'vosotros' NO matchea 'vos'; 'sos un' SÍ matchea 'sos'.
VOSEO_LEXICON = (
    "vos",
    "decís",
    "elegís",
    "tenés",
    "querés",
    "podés",
    "sabés",
    "mirá",
    "andá",
    "escuchá",
    "agarrá",
    "sos",
    "acordate",
    "fijate",
)

# ── (2) Blacklist CLICHÉS horror overused ────────────────────────────────────
# Authority: feedback_anti_cliche_horror — NO medido en F1. Lista extensible por módulo
# (append acá) o por --extra-cliche en runtime. Match case-insensitive de la frase.
CLICHE_PHRASES = (
    "te conviertes en cena",
    "cena que nunca acaba",
    "bucle eterno",
    "nunca encuentras la salida",
    "la oscuridad te consume",
    "demasiado tarde para escapar",
)

# ── (3) Blacklist NOMBRES = oficio ───────────────────────────────────────────
# Authority: feedback_character_real_names — NO medido en F1. SOLO aplica al NAME field;
# el oficio mencionado en visual_signature/role/description es VÁLIDO. Match word-boundary
# case-insensitive sobre el name completo (un name de UNA palabra que sea oficio falla;
# "Bruno" con description "matarife del pueblo" pasa).
JOB_NAME_BLACKLIST = (
    "Proyector",
    "Acomodador",
    "Matarife",
    "Cocinera",
    "Guardavías",
    "Vigilante",
    "Maquinista",
    "Operario",
    "Sereno",
    "Portero",
    "Enfermera",
    "Doctor",
    "Conserje",
)

# ── (4) Handles ──────────────────────────────────────────────────────────────
# Authority: feedback_watermark_handle — NO medido en F1.
CANONICAL_HANDLE = "@elige_tucompanero"
FORBIDDEN_OWN_HANDLE = "@referent-a"  # reference-only — NUNCA handle propio


# ═══════════════════════════════════════════════════════════════
# LÓGICA PURA (testeable sin filesystem)
# ═══════════════════════════════════════════════════════════════


def _voseo_pattern(lexicon=VOSEO_LEXICON):
    # word-boundary case-insensitive; re.UNICODE para que el boundary respete acentos.
    # El grupo (?:...) es OBLIGATORIO: sin él el lookbehind solo bindea al 1er alternante
    # y el lookahead al último (bug 'vosotros' matchea 'vos'). Con grupo, los boundaries
    # envuelven CADA alternante → 'vosotros' NO matchea 'vos'.
    alt = "|".join(re.escape(w) for w in lexicon)
    return re.compile(rf"(?<![\w])(?:{alt})(?![\w])", re.IGNORECASE | re.UNICODE)


def evaluate_voseo(texts, *, lexicon=VOSEO_LEXICON):
    """PURO. texts = [{source, text}, ...]. Devuelve (ok, findings).

    FAIL si alguna palabra del lexicón voseo aparece con word-boundary. 'vosotros'
    NO matchea (boundary derecho); 'sos un compañero' SÍ matchea 'sos'.
    """
    pat = _voseo_pattern(lexicon)
    findings = []
    for item in texts:
        text = item.get("text") or ""
        src = item.get("source", "?")
        hits = sorted({m.group(0).lower() for m in pat.finditer(text)})
        if hits:
            findings.append(
                {
                    "source": src,
                    "status": "fail",
                    "hits": hits,
                    "detail": (
                        f"voseo detectado {hits} en '{src}' — el canónico es Spanish "
                        f"neutral (tú/dices/eliges). Texto: «{text[:90]}»"
                    ),
                }
            )
    return (len(findings) == 0), findings


def evaluate_cliche(texts, *, phrases=CLICHE_PHRASES):
    """PURO. FAIL si alguna frase de la blacklist aparece (case-insensitive)."""
    lowered = [p.lower() for p in phrases]
    findings = []
    for item in texts:
        text = item.get("text") or ""
        src = item.get("source", "?")
        low = text.lower()
        hits = [phrases[i] for i, p in enumerate(lowered) if p in low]
        if hits:
            findings.append(
                {
                    "source": src,
                    "status": "fail",
                    "hits": hits,
                    "detail": (
                        f"cliché(s) overused {hits} en '{src}' — escribir original/"
                        f"concreto/sensorial. Texto: «{text[:90]}»"
                    ),
                }
            )
    return (len(findings) == 0), findings


def evaluate_names(names, *, blacklist=JOB_NAME_BLACKLIST):
    """PURO. names = [{source, name}, ...]. FAIL si el NAME field ES (word-boundary,
    case-insensitive) un sustantivo de oficio de la blacklist. La descripción del personaje
    que mencione el oficio NO se pasa acá → no falla (caso 'Bruno' + desc 'matarife')."""
    alt = "|".join(re.escape(w) for w in blacklist)
    # grupo (?:...) obligatorio (mismo motivo que _voseo_pattern): los boundaries deben
    # envolver CADA alternante, no solo el 1er/último.
    pat = re.compile(rf"(?<![\w])(?:{alt})(?![\w])", re.IGNORECASE | re.UNICODE)
    findings = []
    for item in names:
        name = (item.get("name") or "").strip()
        src = item.get("source", "?")
        if not name:
            continue
        m = pat.search(name)
        if m:
            findings.append(
                {
                    "source": src,
                    "status": "fail",
                    "name": name,
                    "hit": m.group(0),
                    "detail": (
                        f"character name '{name}' ({src}) ES un oficio ('{m.group(0)}') — "
                        f"usar nombre REAL inventado (Bruno/Pablo/Hugo). El oficio va en "
                        f"la descripción, NUNCA en el name field."
                    ),
                }
            )
    return (len(findings) == 0), findings


def evaluate_handle(handles, *, canonical=CANONICAL_HANDLE, forbidden=FORBIDDEN_OWN_HANDLE):
    """PURO. handles = [{source, handle}, ...]. FAIL si algún campo de handle PROPIO
    contiene el forbidden (@referent-a) o NO es el canónico (@elige_tucompanero).
    Solo se alimentan acá campos de handle propio (channel/watermark) — menciones como
    reference en comentarios/why_relevant NO llegan a esta función."""
    findings = []
    fnorm = forbidden.lstrip("@").lower()
    cnorm = canonical.lstrip("@").lower()
    for item in handles:
        raw = (item.get("handle") or "").strip()
        src = item.get("source", "?")
        if not raw:
            continue
        norm = raw.lstrip("@").lower()
        if norm == fnorm:
            findings.append(
                {
                    "source": src,
                    "status": "fail",
                    "handle": raw,
                    "detail": (
                        f"handle PROPIO '{raw}' en '{src}' es {forbidden} — reference-only, "
                        f"NUNCA handle propio. Canónico = {canonical}."
                    ),
                }
            )
        elif norm != cnorm:
            findings.append(
                {
                    "source": src,
                    "status": "fail",
                    "handle": raw,
                    "detail": (f"handle PROPIO '{raw}' en '{src}' ≠ canónico {canonical}."),
                }
            )
    return (len(findings) == 0), findings


# ═══════════════════════════════════════════════════════════════
# EXTRACCIÓN (runtime — parsea SPEC + HTML, alimenta la lógica pura)
# ═══════════════════════════════════════════════════════════════

# Tipos de ui_overlay_element que SON caption de texto narrativo (no UI cromo).
_CAPTION_ELEMENT_HINTS = ("caption", "warning", "narration", "subtitle")
# Tipos que NO son caption (no chequear su .text por estilo): name labels, countdown,
# watermark, botones, loaders. (El watermark se chequea aparte en collect_handles.)
_NON_CAPTION_ELEMENT_HINTS = (
    "name_label",
    "countdown",
    "watermark",
    "button",
    "loading",
    "loader",
    "cta",
    "logo",
)


def _is_caption_element(element_id: str) -> bool:
    eid = (element_id or "").lower()
    if any(h in eid for h in _NON_CAPTION_ELEMENT_HINTS):
        return False
    return any(h in eid for h in _CAPTION_ELEMENT_HINTS)


def collect_texts(spec: dict) -> list:
    """Junta TODOS los textos español del SPEC que deben respetar idioma/estilo:
    narration_script[].text_canonical, shot_list[].dialog_text + narration_in_this_shot,
    y captions (ui_overlay_elements[].text de tipo caption/warning)."""
    out = []
    for seg in spec.get("narration_script") or []:
        if not isinstance(seg, dict):
            continue
        t = seg.get("text_canonical") or seg.get("text")
        if t:
            sid = seg.get("segment_id") or seg.get("shot_id_anchor") or "?"
            out.append({"source": f"narration_script[{sid}].text_canonical", "text": t})

    for shot in spec.get("shot_list") or []:
        if not isinstance(shot, dict):
            continue
        sid = shot.get("shot_id", "?")
        dt = shot.get("dialog_text")
        if dt:
            out.append({"source": f"shot_list[{sid}].dialog_text", "text": dt})
        nt = shot.get("narration_in_this_shot")
        if nt:
            out.append({"source": f"shot_list[{sid}].narration_in_this_shot", "text": nt})
        for el in shot.get("ui_overlay_elements") or []:
            if not isinstance(el, dict):
                continue
            eid = el.get("element_id", "")
            txt = el.get("text")
            if txt and _is_caption_element(eid):
                out.append({"source": f"shot_list[{sid}].{eid}.text", "text": txt})
    return out


def collect_names(spec: dict) -> list:
    """characters[].name (+ star_name si existe en el char block del formato sport)."""
    out = []
    for ch in spec.get("characters") or []:
        if not isinstance(ch, dict):
            continue
        cid = ch.get("character_id", "?")
        name = ch.get("name")
        if name:
            out.append({"source": f"characters[{cid}].name", "name": name})
        star = ch.get("star_name")
        if star:
            out.append({"source": f"characters[{cid}].star_name", "name": star})
    return out


def collect_handles(spec: dict, html_text: str | None = None) -> list:
    """Campos de handle PROPIO: project.channel, channel_signature.watermark_handle,
    meta.watermark, + watermark en ui_overlay_elements + watermarks en el HTML.
    NO recoge menciones en comentarios/why_relevant (reference-only)."""
    out = []
    proj = spec.get("project")
    if isinstance(proj, dict) and proj.get("channel"):
        out.append({"source": "project.channel", "handle": proj["channel"]})
    cs = spec.get("channel_signature")
    if isinstance(cs, dict) and cs.get("watermark_handle"):
        out.append({"source": "channel_signature.watermark_handle", "handle": cs["watermark_handle"]})
    meta = spec.get("meta")
    if isinstance(meta, dict) and meta.get("watermark"):
        out.append({"source": "meta.watermark", "handle": meta["watermark"]})

    # watermark text dentro de ui_overlay_elements (handle PROPIO renderizado en pantalla)
    for shot in spec.get("shot_list") or []:
        if not isinstance(shot, dict):
            continue
        sid = shot.get("shot_id", "?")
        for el in shot.get("ui_overlay_elements") or []:
            if not isinstance(el, dict):
                continue
            eid = (el.get("element_id") or "").lower()
            txt = el.get("text")
            if txt and "watermark" in eid and "@" in str(txt):
                out.append({"source": f"shot_list[{sid}].{eid}.text", "handle": txt})

    # HTML watermark (regex robusto — busca @handle en atributos/text de elementos
    # con clase/id/data que mencione watermark; fallback: cualquier @handle del set conocido).
    if html_text:
        for m in re.finditer(r'(@elige_tucompanero|@referent-a)', html_text):
            # contexto: ¿está cerca de la palabra "watermark"? Si sí, es handle propio renderizado.
            start = max(0, m.start() - 120)
            ctx = html_text[start : m.start()].lower()
            if "watermark" in ctx:
                out.append({"source": "html.watermark", "handle": m.group(1)})
    return out


# ═══════════════════════════════════════════════════════════════
# WRAPPER
# ═══════════════════════════════════════════════════════════════

CHECK_DISPATCH = {
    "voseo": ("collect_texts", "evaluate_voseo"),
    "cliche": ("collect_texts", "evaluate_cliche"),
    "names": ("collect_names", "evaluate_names"),
    "handle": ("collect_handles", "evaluate_handle"),
}


def run_checks(spec, html_text, checks, *, extra_cliche=()):
    """Orquesta los checks pedidos sobre datos extraídos. Devuelve (overall_ok, report_checks)."""
    report = {}
    overall_ok = True

    texts = collect_texts(spec)
    names = collect_names(spec)
    handles = collect_handles(spec, html_text)

    for chk in checks:
        if chk == "voseo":
            ok, findings = evaluate_voseo(texts)
            report[chk] = {
                "status": "pass" if ok else "fail",
                "inputs_checked": len(texts),
                "findings": findings,
            }
        elif chk == "cliche":
            phrases = tuple(CLICHE_PHRASES) + tuple(extra_cliche)
            ok, findings = evaluate_cliche(texts, phrases=phrases)
            report[chk] = {
                "status": "pass" if ok else "fail",
                "inputs_checked": len(texts),
                "findings": findings,
            }
        elif chk == "names":
            ok, findings = evaluate_names(names)
            report[chk] = {
                "status": "pass" if ok else "fail",
                "inputs_checked": len(names),
                "findings": findings,
            }
        elif chk == "handle":
            ok, findings = evaluate_handle(handles)
            report[chk] = {
                "status": "pass" if ok else "fail",
                "inputs_checked": len(handles),
                "findings": findings,
            }
        else:
            continue
        overall_ok = overall_ok and ok
    return overall_ok, report


def main():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--format", required=True, help="agnostic-by-design (horror-choice/sport-choice/…)")
    parser.add_argument("--spec", required=True)
    parser.add_argument("--html", default=None, help="index.html opcional (chequea watermark renderizado)")
    parser.add_argument(
        "--checks", default="all", help="csv de {voseo,cliche,names,handle} o 'all' (default)"
    )
    parser.add_argument(
        "--extra-cliche", action="append", default=[], help="frase extra a blacklistear (extensible runtime)"
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

    if args.checks.strip().lower() == "all":
        checks = list(ALL_CHECKS)
    else:
        checks = [c.strip().lower() for c in args.checks.split(",") if c.strip()]
        bad = [c for c in checks if c not in ALL_CHECKS]
        if bad:
            print(f"ERROR: unknown check(s) {bad}; valid: {ALL_CHECKS}", file=sys.stderr)
            return 2

    if args.dry_run:
        print(
            f"format: {args.format}\nspec: {spec_path}\nchecks: {checks}\n"
            f"branch: language_style_check (universal — siempre aplica)"
        )
        return 0

    html_text = None
    if args.html:
        hp = Path(args.html)
        if hp.exists():
            html_text = hp.read_text(encoding="utf-8", errors="replace")

    overall_ok, check_report = run_checks(spec, html_text, checks, extra_cliche=args.extra_cliche)

    total_findings = sum(len(c["findings"]) for c in check_report.values())
    report = {
        "format": args.format,
        "spec": str(spec_path),
        "checks_run": checks,
        "overall_status": "pass" if overall_ok else "fail",
        "overall_pass": overall_ok,
        "total_findings": total_findings,
        "checks": check_report,
    }
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if overall_ok else 1


if __name__ == "__main__":
    sys.exit(main())
