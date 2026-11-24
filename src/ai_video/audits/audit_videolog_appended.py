#!/usr/bin/env python3
"""audit-videolog-appended.py — Q15 del pre-render-gate: learnings appended a video-log.md.

BUG REAL que cierra (caso disparador estructural — el Q15 que hoy es acto MANUAL
auto-reportado): el pre-render-gate Q15 pide "video-log.md learnings appended" y la
rotación HR#14 pide "NO repetir el mismo pattern 2 videos consecutivos". Ambos hoy se
verifican a OJO y se auto-reportan ("sí, ya appendié los learnings") — exactamente el
tipo de Y/N humano que se saltea bajo presión de ship. El propio horror-choice
video-log.md tiene un "⚠️ Nota rotación (gap de log)" admitiendo que entre #7 y #8 se
produjeron 3 videos (cinema/cerro/parque) que NO se loguearon: el log se desincroniza
silenciosamente. El POST-MORTEM standalone ya se deprecó por write-only (nadie lo lee);
el video-log es lo que SÍ se propaga (alimenta la rotación del próximo brief). Este gate
verifica PRESENCIA ESTRUCTURAL de la entry del proyecto en el log, no su calidad.

POR QUÉ NO LO CAZABA NADIE:
  Ningún gate lee el video-log.md. audit-spec-* miran el SPEC; audit-frames/-audio miran
  el render; qa-gate mira el score. El video-log es prosa markdown de un skill (Capa B),
  fuera del scope de todo gate existente. El único "checador" era la línea del
  pre-render-gate que el agente respondía de memoria. Resultado: entries omitidas
  (gap-of-log auto-admitido) + riesgo de repetir pattern sin que nadie corra la
  comparación con la entry anterior (isla-faro #6 repitió P6 de cabana #5 → anti-pattern
  shipeado). La CALIDAD de los learnings es juicio humano (NO la evaluamos); la PRESENCIA
  estructural (entry existe + menciona pattern + ≥2 bullets [+ score]) es mecánica → gate.

REGLA (sobre <format>-format/video-log.md, dado --project-id):
  (a) EXISTE una sección/entry cuyo título O body matchea el project-id (substring
      case-insensitive, slug-normalizado — `champions-sport-choice`, `matadero-banquete`,
      backticks/V-suffix tolerados).
  (b) la entry MENCIONA el pattern usado (token Pn — P1/P2/P3/P6/P9/P10… — o "pattern"
      explícito en el body de la entry).
  (c) la entry contiene ≥2 bullets de learnings (líneas que empiezan con `-`, `*` o `•`
      dentro del span de la entry). MIN_LEARNINGS_BULLETS override por CLI.
  (d) [si --require-scores] la entry menciona un score (X.X/10, "Gemini 9.x", "10.0/10").
  Cualquiera de (a)-(d) que falte → FAIL nombrando QUÉ falta.

  --check-rotation (opcional, HR#14): el pattern de la entry MÁS RECIENTE (la última fila
  de la "Tabla maestra" con # mayor) ≠ pattern de la ANTERIOR. Dos entries consecutivas con
  el mismo pattern → FAIL (feed predecible). Independiente de --project-id.

Capability-gate (Pattern 7): --format REQUERIDO (agnostic-by-design). El carrier de
capabilities es el SPEC del proyecto (--spec). video_capabilities ausente → Bug #9 (exit 2).
La capability relevante es maintains_video_log (las familias choice mantienen video-log.md);
si el formato NO es de la familia choice Y la capability no está declarada → not_applicable
(exit 0): un formato sin video-log no tiene Q15 que verificar.

DISEÑO TESTEABLE: lógica PURA en evaluate_videolog_entry(entry_text, ...) +
evaluate_rotation(patterns) — reciben texto/listas ya extraídos, sin filesystem. El wrapper
runtime lee el .md, parte el log en entries (split_log_entries) y extrae la tabla maestra
(parse_master_table_patterns).

Bandas empíricas: NINGUNA aplica — la regla es ESTRUCTURAL (presencia de campos + rotación
HR#14), no una banda medida en F1. MIN_LEARNINGS_BULLETS = 2 es constante de módulo.
Authority: CLAUDE.md § Pre-render gate Q15 ("video-log.md learnings appended") + HR#14
(rotación pattern) — NO medida en F1. Override CLI --min-bullets.

Exit: 0 PASS·not_applicable / 1 FAIL / 2 can't-measure (Bug #9 / SPEC|log ausente / pyyaml).
Authority: CLAUDE.md HR#14 + § Pre-render gate Q15 + <format>-format/video-log.md (schema
"Cómo agregar entrada" + "Learnings"). HR#26 companion test: test_audit-videolog-appended.py.
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

# ── Constantes con autoridad ────────────────────────────────────────────────────────────────
# NO medidas en F1 (reglas estructurales del log, no bandas empíricas del render) →
# constantes de módulo. Authority: CLAUDE.md § Pre-render gate Q15 + HR#14.
MIN_LEARNINGS_BULLETS = 2   # Q15: "append learnings (2-3 bullets)". Override via --min-bullets.

# Familia choice (mantienen video-log.md — capability-gate del Q15).
CHOICE_FAMILY = ("horror-choice", "sport-choice")

# Tokens de pattern del enum canónico choice (PAUTA-MASTER P1/P2/P3/P6/P9 + taxonomía vieja P4/P5/P10).
PATTERN_TOKEN_RE = re.compile(r"\bP(?:1|2|3|4|5|6|7|8|9|10)\b")
# Bullet de learnings: línea que empieza (tras indent opcional) con -, * o •. Excluye "---" (HR).
BULLET_RE = re.compile(r"^\s*(?:[-*]|•)\s+(?!-)\S")
# Score: X.X/10, "10.0/10", "Gemini 9.x", "9.7". Capturamos las formas del log real.
SCORE_RE = re.compile(r"\b(?:\d{1,2}\.\d/10|\d{1,2}/10|gemini\s+\d{1,2}(?:\.\d)?)\b", re.IGNORECASE)


def slug_normalize(s: str) -> str:
    """Normaliza para match tolerante: lower, sin backticks, espacios/_ → -, colapsa --, strip."""
    s = (s or "").lower().replace("`", "")
    s = re.sub(r"[\s_]+", "-", s.strip())
    s = re.sub(r"-{2,}", "-", s).strip("-")
    return s


# ════════════════════════════════════════════════════════════════════════════════════════════
# LÓGICA PURA — testeables sin filesystem
# ════════════════════════════════════════════════════════════════════════════════════════════

def project_matches(entry_text: str, project_id: str) -> bool:
    """¿La entry (texto) menciona el project-id? Substring slug-normalizado, case-insensitive.

    Tolera backticks, V-suffix, _/espacios. 'matadero-banquete' matchea
    '`matadero-banquete` v1 SHIP'. Match bidireccional defensivo (project-id contenido en
    el texto, que es el caso real)."""
    if not project_id:
        return False
    return slug_normalize(project_id) in slug_normalize(entry_text)


def extract_pattern_tokens(text: str):
    """Tokens de pattern (P1..P10) hallados en el texto, en orden de aparición, dedup-ordenado."""
    seen = []
    for m in PATTERN_TOKEN_RE.finditer(text or ""):
        tok = m.group(0)
        if tok not in seen:
            seen.append(tok)
    return seen


def count_bullets(text: str) -> int:
    """Nº de líneas-bullet (- / * / •) en el texto. Excluye separadores '---'."""
    return sum(1 for line in (text or "").splitlines() if BULLET_RE.match(line))


def mentions_score(text: str) -> bool:
    """¿El texto menciona un score (X.X/10, N/10, Gemini 9.x)?"""
    return bool(SCORE_RE.search(text or ""))


def evaluate_videolog_entry(entry_text, project_id, *, require_scores=False,
                            min_bullets=MIN_LEARNINGS_BULLETS, entry_found=True):
    """PURO. Evalúa el bloque de texto asociado al project-id contra (a)-(d).

    entry_text   = texto agregado de la(s) sección(es)/fila(s) que matchean el project-id
                   ('' si no se halló ninguna).
    entry_found  = el runtime ya determinó si hubo match (separa "no existe" de "existe vacío").
    Devuelve dict {overall_pass, checks:[{check,status,detail}], ...}."""
    checks = []

    # (a) existencia — la determina el runtime (gather_project_text); entry_text es el
    # texto agregado de los bloques que matchearon. Confiamos en entry_found.
    exists = bool(entry_found)
    checks.append({
        "check": "a_entry_exists", "status": "pass" if exists else "fail",
        "detail": (f"entry para project-id '{project_id}' hallada en el video-log ✓" if exists
                   else f"NO existe entry para project-id '{project_id}' en el video-log "
                        f"(Q15 — learnings NUNCA appended)"),
    })
    if not exists:
        # Sin entry, (b)/(c)/(d) no se pueden evaluar — reportamos pero el overall ya falla.
        for name, det in (("b_mentions_pattern", "sin entry"),
                          ("c_min_bullets", "sin entry"),
                          ("d_mentions_score", "sin entry")):
            checks.append({"check": name, "status": "fail", "detail": f"no evaluable: {det}"})
        return {"overall_pass": False, "checks": checks,
                "pattern_tokens": [], "bullet_count": 0}

    # (b) menciona pattern
    patterns = extract_pattern_tokens(entry_text)
    has_pattern = bool(patterns) or "pattern" in (entry_text or "").lower()
    checks.append({
        "check": "b_mentions_pattern", "status": "pass" if has_pattern else "fail",
        "detail": (f"entry menciona pattern: {patterns or 'token \"pattern\"'} ✓" if has_pattern
                   else "entry NO menciona el pattern usado (Pn o 'pattern') — rotación HR#14 "
                        "no se puede trackear sin pattern declarado"),
    })

    # (c) ≥ min_bullets learnings
    n_bullets = count_bullets(entry_text)
    enough = n_bullets >= min_bullets
    checks.append({
        "check": "c_min_bullets", "status": "pass" if enough else "fail",
        "detail": (f"{n_bullets} bullet(s) de learnings ≥ {min_bullets} ✓" if enough
                   else f"solo {n_bullets} bullet(s) de learnings < {min_bullets} exigidos "
                        f"(Q15: 'append learnings 2-3 bullets')"),
        "bullet_count": n_bullets,
    })

    # (d) score [opcional]
    if require_scores:
        has_score = mentions_score(entry_text)
        checks.append({
            "check": "d_mentions_score", "status": "pass" if has_score else "fail",
            "detail": ("entry menciona un score (X.X/10 / Gemini 9.x) ✓" if has_score
                       else "entry NO menciona score y --require-scores está activo"),
        })

    overall = all(c["status"] == "pass" for c in checks)
    return {"overall_pass": overall, "checks": checks,
            "pattern_tokens": patterns, "bullet_count": n_bullets}


def evaluate_rotation(recent_patterns):
    """PURO. HR#14: el pattern de la entry más reciente ≠ el de la anterior.

    recent_patterns = lista de patterns en orden CRONOLÓGICO (más antiguo → más nuevo),
    ya extraída de la tabla maestra (cada fila = un pattern, p.ej. ['P10','P6','P4',...]).
    Devuelve dict {overall_pass, detail, last, prev}. <2 entries → not_applicable (no hay
    par consecutivo que comparar)."""
    pats = [p for p in recent_patterns if p]
    if len(pats) < 2:
        return {"overall_pass": True, "status": "not_applicable",
                "detail": f"solo {len(pats)} entry con pattern → no hay par consecutivo (HR#14 N/A)",
                "last": pats[-1] if pats else None, "prev": None}
    last, prev = pats[-1], pats[-2]
    ok = last != prev
    return {
        "overall_pass": ok, "status": "pass" if ok else "fail",
        "last": last, "prev": prev,
        "detail": (f"rotación OK: última entry '{last}' ≠ anterior '{prev}' ✓" if ok
                   else f"VIOLA HR#14: última entry '{last}' == anterior '{prev}' "
                        f"(mismo pattern 2 videos consecutivos = feed predecible)"),
    }


# ════════════════════════════════════════════════════════════════════════════════════════════
# EXTRACCIÓN — runtime (lee el .md y arma las estructuras puras)
# ════════════════════════════════════════════════════════════════════════════════════════════

def split_log_entries(md_text: str):
    """Parte el video-log.md en bloques candidatos a 'entry' por heading (##/###/####).

    Devuelve [(heading_text, block_text), ...] donde block_text incluye el heading y todo
    hasta el siguiente heading de igual o mayor jerarquía. Además, cada FILA de la 'Tabla
    maestra' (| N | fecha | proyecto | ...) se trata como una mini-entry adicional (el log
    real codifica learnings tanto en filas de tabla como en secciones ###)."""
    blocks = []
    lines = md_text.splitlines()
    # Headings → bloques.
    heading_idx = [(i, len(m.group(1)))
                   for i, line in enumerate(lines)
                   for m in [re.match(r"^(#{2,4})\s+(.*)$", line)] if m]
    for k, (start, _level) in enumerate(heading_idx):
        end = heading_idx[k + 1][0] if k + 1 < len(heading_idx) else len(lines)
        block = "\n".join(lines[start:end])
        heading = lines[start].lstrip("#").strip()
        blocks.append((heading, block))
    # Filas de tabla maestra → mini-entries (heading = contenido de la fila).
    for line in lines:
        if re.match(r"^\|\s*\d+\s*\|", line):
            blocks.append((line.strip(), line.strip()))
    return blocks


def gather_project_text(md_text: str, project_id: str):
    """Texto agregado de los bloques que pertenecen al project-id.

    Devuelve (found: bool, text: str). Concatena la(s) fila(s) de tabla (pattern + score) +
    la sección ### de learnings (bullets) del MISMO proyecto. Para evitar over-matching, una
    sección con heading (##/###/####) cuenta SOLO si su PROPIO heading menciona el project-id
    (p.ej. '### matadero-banquete v1 SHIP …'); las filas de tabla cuentan por su body (es donde
    vive el slug). Así no se arrastra la sección-contenedor '## Tabla maestra' / '## Cross-video
    uniqueness' — que contiene TODOS los slugs — a cada proyecto."""
    parts = []
    for heading, block in split_log_entries(md_text):
        is_table_row = bool(re.match(r"^\|\s*\d+\s*\|", heading))
        if is_table_row:
            if project_matches(block, project_id):
                parts.append(block)
        elif project_matches(heading, project_id):
            parts.append(block)
    return (len(parts) > 0, "\n".join(parts))


def parse_master_table_patterns(md_text: str):
    """Extrae los patterns de la 'Tabla maestra' en orden CRONOLÓGICO (por # de fila).

    Las filas tienen forma `| N | fecha | proyecto | Pattern | ...`. Devuelve lista
    [(num, pattern_token_or_None), ...] ordenada por num ascendente. El pattern es el primer
    token Pn hallado en la fila (la columna Pattern). Filas sin Pn → pattern None (se filtran
    en evaluate_rotation)."""
    rows = []
    for line in md_text.splitlines():
        m = re.match(r"^\|\s*(\d+)\s*\|(.*)$", line)
        if not m:
            continue
        num = int(m.group(1))
        toks = extract_pattern_tokens(m.group(2))
        rows.append((num, toks[0] if toks else None))
    rows.sort(key=lambda r: r[0])
    return rows


def resolve_videolog_path(fmt: str, explicit: str | None) -> Path | None:
    """Path al video-log.md. --video-log explícito gana; si no, deriva del --format:
    <repo>/.claude/skills/<format>-format/video-log.md."""
    if explicit:
        return Path(explicit)
    from ai_video.errors import ConfigError
    from ai_video.paths import skills_dir

    try:
        return skills_dir() / f"{fmt}-format" / "video-log.md"
    except ConfigError:
        return None


# ════════════════════════════════════════════════════════════════════════════════════════════
# RUNTIME
# ════════════════════════════════════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--format", required=True,
                        help="formato (agnostic-by-design — gatea Q15 por familia choice + deriva el log)")
    parser.add_argument("--spec", required=True,
                        help="CREATIVE-SPEC.yaml del proyecto (carrier de video_capabilities — Bug #9)")
    parser.add_argument("--project-id", required=True,
                        help="slug del proyecto a buscar en el video-log (ej. matadero-banquete)")
    parser.add_argument("--video-log", default=None,
                        help="path al video-log.md (default: <skills>/<format>-format/video-log.md)")
    parser.add_argument("--require-scores", action="store_true",
                        help="exige que la entry mencione un score (check d)")
    parser.add_argument("--check-rotation", action="store_true",
                        help="HR#14: pattern de la entry más reciente ≠ anterior (tabla maestra)")
    parser.add_argument("--min-bullets", type=int, default=MIN_LEARNINGS_BULLETS,
                        help=f"override del mínimo de bullets de learnings (default {MIN_LEARNINGS_BULLETS})")
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

    # Capability: maintains_video_log declarada O familia choice (las que mantienen log).
    maintains_log = caps.get("maintains_video_log")
    in_family = args.format in CHOICE_FAMILY
    applies = bool(maintains_log) if maintains_log is not None else in_family

    log_path = resolve_videolog_path(args.format, args.video_log)

    if args.dry_run:
        print(f"format: {args.format}\nspec: {spec_path}\nproject_id: {args.project_id}\n"
              f"video_log: {log_path}\nmaintains_video_log: {maintains_log} | in_family: {in_family}\n"
              f"branch: {'videolog_check' if applies else 'not_applicable'}\n"
              f"require_scores: {args.require_scores} | check_rotation: {args.check_rotation} | "
              f"min_bullets: {args.min_bullets}")
        return 0

    if not applies:
        print(json.dumps({
            "format": args.format, "project_id": args.project_id,
            "overall_status": "not_applicable",
            "detail": ("formato fuera de la familia choice Y maintains_video_log no declarado → "
                       "no mantiene video-log.md (Q15 no aplica)"),
        }, indent=2, ensure_ascii=False))
        return 0

    if log_path is None or not log_path.exists():
        print(f"ERROR: video-log.md not found: {log_path}", file=sys.stderr)
        return 2

    md_text = log_path.read_text(encoding="utf-8")
    found, entry_text = gather_project_text(md_text, args.project_id)

    entry_result = evaluate_videolog_entry(
        entry_text, args.project_id, require_scores=args.require_scores,
        min_bullets=args.min_bullets, entry_found=found)

    checks = list(entry_result["checks"])
    overall = entry_result["overall_pass"]

    rotation = None
    if args.check_rotation:
        rows = parse_master_table_patterns(md_text)
        patterns_chrono = [p for _num, p in rows]
        rotation = evaluate_rotation(patterns_chrono)
        if rotation["status"] != "not_applicable" and not rotation["overall_pass"]:
            overall = False

    report = {
        "format": args.format, "spec": str(spec_path),
        "video_log": str(log_path), "project_id": args.project_id,
        "min_bullets": args.min_bullets, "require_scores": args.require_scores,
        "overall_status": "pass" if overall else "fail",
        "overall_pass": overall,
        "entry_found": found,
        "pattern_tokens": entry_result["pattern_tokens"],
        "bullet_count": entry_result["bullet_count"],
        "checks": checks,
    }
    if rotation is not None:
        report["rotation"] = rotation
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if overall else 1


if __name__ == "__main__":
    sys.exit(main())
