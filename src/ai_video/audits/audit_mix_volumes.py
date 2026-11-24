#!/usr/bin/env python3
"""audit-mix-volumes.py — HR#9b: bandas de volumen por elemento del mix.

BUG REAL que cierra (HR#9 hoy prose_only): la regla "narración 1.0 / música
0.05-0.18 / SFX 0.20-0.35 / flash 0.55-0.65 / ambient 0.10-0.18" vivía SOLO en
prosa (SFX-PIPELINE.md §"Mix volumes" + CLAUDE.md HR#9). Sin gate, nada chequea
que un `volume=` declarado en el HTML o en el manifest caiga dentro de su banda.
El caso clásico: música puesta a 0.5 (debería 0.05-0.18) que TAPA la narración,
o un flash a 0.20 que no pega. Gemini holístico no mide amplitudes declaradas;
el oído humano lo caza tarde (post-render) — este gate lo caza determinísticamente
sobre los volúmenes que el pipeline DECLARA, antes de renderizar.

POR QUÉ NO LO CAZABA NADIE:
  - `audit-spec-completeness.py` cuenta EXISTENCIA de assets (¿el stem está wired?),
    NO el VOLUMEN al que se mezcla.
  - `audit-render-audio-coverage.py` / `audit-audio.py` miden COBERTURA temporal
    (¿hay narración el ≥X% del tiempo?, ¿gaps?), NO la AMPLITUD relativa por rol.
  - El QA Gemini holístico puntúa "atmósfera" y se infla; una música 3x fuera de
    banda baja el score recién cuando ya tapó la voz en el render final.
  Ningún check previo razona "este track es rol=música y su volumen declarado 0.45
  está fuera de la banda canónica 0.05-0.18".

REGLA (por track clasificado):
  Clasificar cada track por ROL (narración/música/sfx/flash/ambient) — por campo
  del manifest (`class`/`role`), por nombre de archivo (heurística flash/ambient),
  o por track-index (60-110 → capa SFX). Validar el volumen DECLARADO contra la
  banda canónica del rol:
      narración 1.0 (exacto, tol 0.0) · música 0.05-0.18 · SFX 0.20-0.35 ·
      flash 0.55-0.65 · ambient 0.10-0.18
  FAIL si un track clasificado declara un volumen FUERA de su banda.
  Track SIN volumen declarado → no se puede medir su amplitud → se reporta como
  "no_volume_declared" (informativo, NO falla: el pipeline aplica defaults canónicos
  vía build_clip_atomic.py — ver MIX_*_DEFAULT, todos dentro de banda).
  Track NO clasificable (rol desconocido) → warning, NO FAIL.

Capability-gate: has_sfx_layer / audio_mix_target. Si NINGUNA capability de audio
está presente (sin mix que auditar) → not_applicable (exit 0).
video_capabilities ausente → Bug #9 (exit 2). Agnostic-by-design: --format REQUIRED.

DISEÑO TESTEABLE: lógica pura en evaluate_mix_volumes(tracks, bands) — recibe
tracks ya extraídos [{id, role, volume}] + bandas; NO toca filesystem. Wrappers
runtime: extract_tracks_from_manifest() + extract_tracks_from_html() parsean
manifest/HTML.

Constantes con autoridad: las bandas de mix NO están en F1 (no medidas en n=10;
son límites de diseño de SFX-PIPELINE.md). → constantes de módulo con comentario
"Authority: SFX-PIPELINE.md §Mix volumes — NO medida en F1; override via --band".

Exit: 0 PASS·not_applicable / 1 FAIL / 2 can't-measure (Bug #9 / SPEC ausente).
Authority: ai-video-production/SFX-PIPELINE.md §"Mix volumes" + CLAUDE.md HR#9.
HR#26 companion test: test_audit-mix-volumes.py.
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

# ── Bandas canónicas (lo, hi) por rol ──────────────────────────────────────────
# Authority: ai-video-production/SFX-PIPELINE.md §"Mix volumes" + CLAUDE.md HR#9.
# NO medida en F1 (no es estadística de referentes n=10 sino límite de diseño de
# sound mix); por eso son constantes de módulo overridables vía --band rol=lo:hi.
CANONICAL_BANDS = {
    "narration": (1.0, 1.0),  # siempre 1.0 — nada compite con la voz
    "music": (0.05, 0.18),  # apenas perceptible
    "sfx": (0.20, 0.35),  # eventos puntuales (footsteps/breaths/body falls)
    "flash": (0.55, 0.65),  # impactos que tienen que pegar (white flash + sub-bass)
    "ambient": (0.10, 0.18),  # capa continua profunda (wind/fire loop)
}

# track-index reservado para la capa SFX dedicada (HR#8 / SFX-PIPELINE.md §"Conectar en index.html").
SFX_TRACK_INDEX_LO = 60
SFX_TRACK_INDEX_HI = 110

# Tolerancia de igualdad para banda de ancho 0 (narración == 1.0).
VOL_EPS = 1e-6

# Heurística de rol por nombre de archivo / id.
_FLASH_RE = re.compile(r"flash", re.IGNORECASE)
_AMBIENT_RE = re.compile(r"ambient|drone|wind|fire.?crackle|rain|room.?tone", re.IGNORECASE)
_MUSIC_RE = re.compile(r"music|crescendo|accent|score|theme|tango|radio", re.IGNORECASE)
_NARRATION_RE = re.compile(
    r"narrat|narrac|\bnarr\b|narr[_\-.]|voiceover|\bvo\b|tts|dialog|dialogo|diálogo|voice", re.IGNORECASE
)


def classify_role(*, declared_role=None, name="", track_index=None):
    """Devuelve un rol canónico (narration/music/sfx/flash/ambient) o None.

    Precedencia: (1) rol declarado explícito en el manifest/HTML, (2) heurística de
    nombre (flash > ambient > music > narration), (3) track-index en banda SFX → sfx.
    flash gana a sfx porque 'flash_*' es un subtipo de SFX con banda propia más alta.
    """
    if declared_role:
        r = str(declared_role).strip().lower()
        # normalizar sinónimos
        if r in ("narration", "narracion", "narración", "voice", "voiceover", "vo", "dialog", "dialogue"):
            return "narration"
        if r in ("music", "musica", "música", "score"):
            return "music"
        if r in ("ambient", "ambience", "ambiente", "atmos"):
            return "ambient"
        if r in ("flash", "flash_impact", "impact_flash"):
            return "flash"
        if r in ("sfx", "sound_effect", "effect", "fx"):
            # sub-clasificar flash dentro de sfx por nombre
            return "flash" if name and _FLASH_RE.search(name) else "sfx"
        # rol declarado desconocido → seguir a heurística
    if name:
        if _FLASH_RE.search(name):
            return "flash"
        if _AMBIENT_RE.search(name):
            return "ambient"
        if _NARRATION_RE.search(name):
            return "narration"
        if _MUSIC_RE.search(name):
            return "music"
    if track_index is not None:
        try:
            ti = int(track_index)
        except (TypeError, ValueError):
            ti = None
        if ti is not None and SFX_TRACK_INDEX_LO <= ti <= SFX_TRACK_INDEX_HI:
            return "sfx"
    return None


# ── Lógica PURA ────────────────────────────────────────────────────────────────
def evaluate_mix_volumes(tracks, *, bands=None, eps=VOL_EPS):
    """PURE. tracks = [{id, role, volume}, ...] (role ya clasificado; volume puede ser None).

    Devuelve (ok: bool, reasons: list[dict]). FAIL si un track con rol conocido +
    volumen declarado cae FUERA de su banda. Track sin volumen → informativo (no
    falla: pipeline aplica defaults canónicos). Track sin rol → warning (no falla).
    """
    bands = bands or CANONICAL_BANDS
    reasons = []
    ok = True
    for t in tracks:
        tid = t.get("id", "?")
        role = t.get("role")
        vol = t.get("volume")
        if role is None or role not in bands:
            reasons.append(
                {
                    "id": tid,
                    "role": role,
                    "volume": vol,
                    "status": "warning",
                    "detail": (
                        f"track '{tid}' no clasificable a un rol canónico "
                        f"(rol={role!r}) — no se valida banda (warning, no FAIL)"
                    ),
                }
            )
            continue
        lo, hi = bands[role]
        if vol is None:
            reasons.append(
                {
                    "id": tid,
                    "role": role,
                    "volume": None,
                    "status": "no_volume_declared",
                    "band": [lo, hi],
                    "detail": (
                        f"track '{tid}' (rol={role}) sin volumen declarado — "
                        f"pipeline aplica default canónico dentro de [{lo}, {hi}] "
                        f"(informativo, no FAIL)"
                    ),
                }
            )
            continue
        try:
            v = float(vol)
        except (TypeError, ValueError):
            reasons.append(
                {
                    "id": tid,
                    "role": role,
                    "volume": vol,
                    "status": "warning",
                    "detail": f"track '{tid}' volumen no numérico {vol!r} (warning, no FAIL)",
                }
            )
            continue
        in_band = (lo - eps) <= v <= (hi + eps)
        if in_band:
            reasons.append(
                {
                    "id": tid,
                    "role": role,
                    "volume": round(v, 4),
                    "band": [lo, hi],
                    "status": "ok",
                    "detail": f"track '{tid}' (rol={role}) volumen {v:g} ∈ [{lo}, {hi}] ✓",
                }
            )
        else:
            ok = False
            reasons.append(
                {
                    "id": tid,
                    "role": role,
                    "volume": round(v, 4),
                    "band": [lo, hi],
                    "status": "fail",
                    "detail": (
                        f"track '{tid}' (rol={role}) volumen {v:g} FUERA de banda "
                        f"canónica [{lo}, {hi}] — HR#9: {role} debe mezclarse en "
                        f"ese rango (SFX-PIPELINE.md §Mix volumes)"
                    ),
                }
            )
    return ok, reasons


# ── Extractores runtime (filesystem) ────────────────────────────────────────────
def extract_tracks_from_manifest(manifest):
    """De un audio-manifest.json (path HYBRID) → [{id, role, volume}].

    Clasifica por `class`/`role` del item; volumen desde `volume`/`mix_volume`/`gain`
    si está declarado (este manifest del HYBRID típicamente NO lo trae — el pipeline
    aplica defaults — y eso es esperado: el gate reporta no_volume_declared).
    """
    tracks = []
    items = manifest.get("assets") if isinstance(manifest, dict) else None
    if not isinstance(items, list):
        items = manifest if isinstance(manifest, list) else []
    for it in items:
        if not isinstance(it, dict):
            continue
        declared_role = it.get("class") or it.get("role") or it.get("layer")
        name = str(it.get("id") or it.get("name") or it.get("file") or "")
        ti = it.get("track_index", it.get("track-index"))
        role = classify_role(declared_role=declared_role, name=name, track_index=ti)
        vol = None
        for k in ("volume", "mix_volume", "gain", "data-volume"):
            if it.get(k) is not None:
                vol = it.get(k)
                break
        tracks.append({"id": name or "?", "role": role, "volume": vol})
    return tracks


# Regex para <audio>/<video> con data-volume / volume + opcional data-track-index.
_TAG_RE = re.compile(r"<(?:audio|video)\b[^>]*>", re.IGNORECASE)
_VOL_ATTR_RE = re.compile(r"(?:data-volume|volume)\s*=\s*[\"']?([0-9]*\.?[0-9]+)", re.IGNORECASE)
_TRACK_IDX_RE = re.compile(r"data-track-index\s*=\s*[\"']?(\d+)", re.IGNORECASE)
_SRC_RE = re.compile(r"(?:data-src|src)\s*=\s*[\"']([^\"']+)[\"']", re.IGNORECASE)
_ID_RE = re.compile(r"\bid\s*=\s*[\"']([^\"']+)[\"']", re.IGNORECASE)
_ROLE_ATTR_RE = re.compile(r"(?:data-role|data-layer|class)\s*=\s*[\"']([^\"']+)[\"']", re.IGNORECASE)
# GSAP / JS: volume: 0.18 — capturamos el número + intentamos un nombre cercano.
_JS_VOL_RE = re.compile(r"volume\s*:\s*([0-9]*\.?[0-9]+)", re.IGNORECASE)


def extract_tracks_from_html(html):
    """De un index.html (path LEGACY) → [{id, role, volume}].

    Parseo por regex robusto (NO bs4): tags <audio>/<video> con data-volume/volume,
    + setVolume/volume: en JS/GSAP. Clasifica por src/id/class + track-index.
    """
    tracks = []
    seen = set()
    for tag in _TAG_RE.findall(html):
        vol_m = _VOL_ATTR_RE.search(tag)
        src_m = _SRC_RE.search(tag)
        id_m = _ID_RE.search(tag)
        ti_m = _TRACK_IDX_RE.search(tag)
        role_m = _ROLE_ATTR_RE.search(tag)
        name = (Path(src_m.group(1)).name if src_m else None) or (id_m.group(1) if id_m else "?")
        ti = ti_m.group(1) if ti_m else None
        role = classify_role(declared_role=role_m.group(1) if role_m else None, name=name, track_index=ti)
        vol = float(vol_m.group(1)) if vol_m else None
        key = (name, ti, vol)
        if key in seen:
            continue
        seen.add(key)
        tracks.append({"id": name, "role": role, "volume": vol})
    # JS/GSAP volume: directives sin tag asociado (ej. gsap.to(musicEl,{volume:0.06})).
    # Contexto SOLO de la sentencia actual (corta en ; { o newline) para no robar el
    # filename de un <audio> previo. Inferimos el rol del nombre de la VARIABLE target
    # (musicEl/ambientEl/narrEl) o de un .mp3 dentro de la MISMA sentencia.
    for m in _JS_VOL_RE.finditer(html):
        start = max(0, m.start() - 120)
        ctx = html[start : m.start()]
        # acotar al statement actual: lo que sigue al último ; { ( o salto de línea.
        ctx = re.split(r"[;{(\n]", ctx)[-1]
        var_m = re.search(r"([A-Za-z_]\w*?(?:El|Audio|Element))\b", ctx)
        mp3_m = re.search(r"['\"]([\w\-./]+\.mp3)['\"]", ctx, re.IGNORECASE)
        if mp3_m:
            name = Path(mp3_m.group(1)).name
        elif var_m:
            name = var_m.group(1)
        else:
            name = "js_volume_directive"
        role = classify_role(name=name)
        vol = float(m.group(1))
        key = (name, None, vol)
        if key in seen:
            continue
        seen.add(key)
        tracks.append({"id": name, "role": role, "volume": vol})
    return tracks


def parse_band_overrides(override_list):
    """--band narration=1.0:1.0 → dict de overrides. Devuelve dict {role:(lo,hi)}."""
    out = dict(CANONICAL_BANDS)
    for ov in override_list or []:
        try:
            role, rng = ov.split("=", 1)
            lo, hi = rng.split(":", 1)
            out[role.strip().lower()] = (float(lo), float(hi))
        except (ValueError, AttributeError):
            print(f"WARNING: --band override mal formado, ignorado: {ov!r}", file=sys.stderr)
    return out


def main():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--format", required=True, help="formato activo (agnostic-by-design)")
    parser.add_argument("--spec", required=True, help="creative-specs/<id>.yaml (capability gate)")
    parser.add_argument(
        "--manifest",
        default=None,
        help="audio-manifest.json (path HYBRID). Default: <project-dir>/assets/audio-manifest.json",
    )
    parser.add_argument("--html", default=None, help="index.html (path LEGACY)")
    parser.add_argument(
        "--project-dir",
        default=None,
        help="dir del proyecto (para autolocalizar manifest/html). Default: <spec_dir>/../<spec_stem>",
    )
    parser.add_argument(
        "--band",
        action="append",
        default=[],
        help="override de banda: rol=lo:hi (ej. music=0.05:0.20). Repetible.",
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

    has_sfx = bool(caps.get("has_sfx_layer", False))
    has_music = bool(caps.get("has_layer_3_music", False))
    has_tts = bool(caps.get("has_tts_narration", False))
    has_mix_target = bool(caps.get("audio_mix_target"))
    has_any_audio = has_sfx or has_music or has_tts or has_mix_target

    bands = parse_band_overrides(args.band)

    # Resolver project-dir (heurística hermano del spec).
    project_dir = Path(args.project_dir) if args.project_dir else (spec_path.parent.parent / spec_path.stem)
    manifest_path = Path(args.manifest) if args.manifest else (project_dir / "assets" / "audio-manifest.json")
    html_path = Path(args.html) if args.html else (project_dir / "index.html")

    if args.dry_run:
        print(
            f"format: {args.format}\nspec: {spec_path}\nhas_any_audio: {has_any_audio}\n"
            f"branch: {'mix_volume_check' if has_any_audio else 'not_applicable'}\n"
            f"manifest: {manifest_path} (exists={manifest_path.exists()})\n"
            f"html: {html_path} (exists={html_path.exists()})\nbands: {bands}"
        )
        return 0

    if not has_any_audio:
        print(
            json.dumps(
                {
                    "format": args.format,
                    "overall_status": "not_applicable",
                    "detail": (
                        "ninguna capability de audio presente (has_sfx_layer / has_layer_3_music / "
                        "has_tts_narration / audio_mix_target) → no hay mix que auditar"
                    ),
                },
                indent=2,
                ensure_ascii=False,
            )
        )
        return 0

    tracks = []
    sources = []
    if manifest_path.exists():
        try:
            with open(manifest_path) as f:
                manifest = json.load(f)
            tracks.extend(extract_tracks_from_manifest(manifest))
            sources.append(str(manifest_path))
        except (OSError, json.JSONDecodeError) as e:
            print(f"WARNING: no se pudo parsear manifest {manifest_path}: {e}", file=sys.stderr)
    if html_path.exists():
        try:
            tracks.extend(extract_tracks_from_html(html_path.read_text(errors="ignore")))
            sources.append(str(html_path))
        except OSError as e:
            print(f"WARNING: no se pudo leer html {html_path}: {e}", file=sys.stderr)

    if not sources:
        print(
            json.dumps(
                {
                    "format": args.format,
                    "overall_status": "cant_measure",
                    "detail": (
                        f"no se encontró ni manifest ({manifest_path}) ni html ({html_path}) — "
                        f"sin fuente de volúmenes declarados que auditar"
                    ),
                },
                indent=2,
                ensure_ascii=False,
            )
        )
        return 2

    ok, reasons = evaluate_mix_volumes(tracks, bands=bands)

    fails = [r for r in reasons if r["status"] == "fail"]
    warnings = [r for r in reasons if r["status"] == "warning"]
    no_vol = [r for r in reasons if r["status"] == "no_volume_declared"]
    report = {
        "format": args.format,
        "spec": str(spec_path),
        "sources": sources,
        "bands": {k: list(v) for k, v in bands.items()},
        "overall_status": "pass" if ok else "fail",
        "overall_pass": ok,
        "tracks_checked": len(tracks),
        "fail_count": len(fails),
        "warning_count": len(warnings),
        "no_volume_declared_count": len(no_vol),
        "fail_tracks": fails,
        "tracks": reasons,
    }
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
