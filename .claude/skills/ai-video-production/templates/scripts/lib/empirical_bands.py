#!/usr/bin/env python3
"""lib/empirical_bands.py — punto ÚNICO de consulta de constantes empíricas per-formato.

BUG CLASS que cierra (Fase 0, clasificación 2026-06-04): constantes empíricas
duplicadas prosa↔script con drift real. Casos detectados en la auditoría:
  - Y48 (CLAUDE.md HR#4) vs Y52 (INGENIERO-CHOICE-CORE §2) para la loading bar,
    con F1-UI-SAFE-ZONES.json (bandas medidas n=10) existiendo SIN ningún
    script que lo lea — los valores estaban hardcodeados en build_clip_atomic.py.
  - cuts/min 2-7 (check-pacing.sh hardcodeado) vs 14-22 (PAUTA §23 / sport
    INGENIERO-PAUTA §0). ⚠️ NO es solo drift: F1 trae DOS counting methods
    (cuts_per_min curated ~2-7 vs cuts_per_min_raw ~7-11+). El consumidor DEBE
    elegir la key explícita; este lib NO decide por vos cuál es "la" métrica.

PRINCIPIO (v2 Fase 0): un número empírico vive en UN archivo machine-readable
(referent-analysis/<format>/F1-*.json). La prosa apunta, nunca repite. Los gates
consultan este lib con --format; NUNCA hardcodean el número.

PER-FORMAT ROUTING: las bandas son PARÁMETROS por formato, no constantes
globales. sport-choice es pre-empírico (sin F1 propio): load_* devuelve None y
el caller decide explícitamente si hereda otro formato (fallback_format=...) —
nunca un fallback silencioso (HR#19: canonical_validation_status explícito).

DISEÑO TESTEABLE: compute_band() es PURO (recibe lista de valores). Los load_*
resuelven filesystem. Band computation idéntica a audit-against-referent.py
(statistics.quantiles n=4 → p25/p75; n=20 → p5/p95; requiere ≥4 valores).

Authority: referent-analysis/<format>/F1-INGENIERO-MEASUREMENTS.json +
F1-UI-SAFE-ZONES.json + F1-UI-TIMING.json. HR#26 companion: test_empirical_bands.py.
"""
from __future__ import annotations

import json
import os
from pathlib import Path
from statistics import quantiles

# Element types presentes en F1-UI-SAFE-ZONES.json per_referent
UI_ELEMENT_TYPES = (
    "captions_narration",
    "character_name_labels",
    "warning_text",
    "watermark",
)

_MIN_VALUES_FOR_BAND = 4  # mismo umbral que audit-against-referent.compute_bands


def compute_band(values, tolerance: str = "p25-p75"):
    """PURO. Banda (lo, hi, n) desde una lista de valores numéricos.

    tolerance: 'p25-p75' (default, interquartile) | 'p5-p95'.
    Devuelve (None, None, n) si n < 4 (banda no confiable — mismo criterio que
    audit-against-referent.py).
    """
    vals = sorted(float(v) for v in values if v is not None)
    n = len(vals)
    if n < _MIN_VALUES_FOR_BAND:
        return None, None, n
    if tolerance == "p5-p95":
        q = quantiles(vals, n=20)
        return q[0], q[18], n
    q = quantiles(vals, n=4)
    return q[0], q[2], n


def find_referent_analysis_root(start: Path | None = None) -> Path | None:
    """Busca el dir referent-analysis/ subiendo desde `start` (default: este file).

    Funciona tanto desde templates/scripts/lib/ (repo) como desde
    <proyecto>/scripts/lib/ (copia bootstrap): referent-analysis/ vive en el
    root del repo en ambos casos. Override: env REFERENT_ANALYSIS_DIR.
    """
    env = os.environ.get("REFERENT_ANALYSIS_DIR")
    if env:
        p = Path(env)
        return p if p.is_dir() else None
    cur = (start or Path(__file__)).resolve()
    for parent in [cur] + list(cur.parents):
        cand = parent / "referent-analysis"
        if cand.is_dir():
            return cand
    return None


def _load_json(path: Path):
    try:
        with open(path) as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError):
        return None


def _format_dir(format_name: str, base: Path | None) -> Path | None:
    root = base or find_referent_analysis_root()
    if root is None:
        return None
    d = root / format_name
    return d if d.is_dir() else None


def load_measurements(format_name: str, base: Path | None = None,
                      fallback_format: str | None = None):
    """per_referent de F1-INGENIERO-MEASUREMENTS.json del formato, o None.

    Sin fallback silencioso: si el formato no tiene F1 propio devuelve None
    salvo fallback_format EXPLÍCITO (el caller declara la herencia, p.ej.
    sport-choice pre-empírico heredando horror-choice).
    """
    d = _format_dir(format_name, base)
    if d is not None:
        data = _load_json(d / "F1-INGENIERO-MEASUREMENTS.json")
        if data and "per_referent" in data:
            return data["per_referent"]
    if fallback_format and fallback_format != format_name:
        return load_measurements(fallback_format, base)
    return None


def load_ui_safe_zones(format_name: str, base: Path | None = None,
                       fallback_format: str | None = None):
    """per_referent de F1-UI-SAFE-ZONES.json del formato, o None (sin fallback silencioso)."""
    d = _format_dir(format_name, base)
    if d is not None:
        data = _load_json(d / "F1-UI-SAFE-ZONES.json")
        if data and "per_referent" in data:
            return data["per_referent"]
    if fallback_format and fallback_format != format_name:
        return load_ui_safe_zones(fallback_format, base)
    return None


def band(format_name: str, section: str, key: str, *,
         tolerance: str = "p25-p75", base: Path | None = None,
         fallback_format: str | None = None):
    """Banda (lo, hi, n) de una métrica F1-INGENIERO (ej. 'pacing','cuts_per_min').

    ⚠️ cuts: F1 trae 'cuts_per_min' (curated) Y 'cuts_per_min_raw' — elegí la key
    explícita según qué counting method audita tu gate.
    """
    per_ref = load_measurements(format_name, base, fallback_format)
    if per_ref is None:
        return None, None, 0
    values = []
    for ref in per_ref.values():
        try:
            v = ref[section][key]
        except (KeyError, TypeError):
            continue
        if v is not None:
            values.append(v)
    return compute_band(values, tolerance)


def ui_band(format_name: str, element: str, field: str = "y_pct", *,
            tolerance: str = "p25-p75", base: Path | None = None,
            fallback_format: str | None = None):
    """Banda (lo, hi, n) de un campo de UI safe zone (ej. 'captions_narration','y_pct').

    Maneja la variante '<field>_avg' que usan algunos elementos
    (character_name_labels guarda y_pct_avg + y_pct_range, no y_pct).
    """
    per_ref = load_ui_safe_zones(format_name, base, fallback_format)
    if per_ref is None:
        return None, None, 0
    values = []
    for ref in per_ref.values():
        el = ref.get(element)
        if not isinstance(el, dict):
            continue
        v = el.get(field, el.get(f"{field}_avg"))
        if v is not None:
            values.append(v)
    return compute_band(values, tolerance)
