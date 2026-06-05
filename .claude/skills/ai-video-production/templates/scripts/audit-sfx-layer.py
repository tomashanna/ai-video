#!/usr/bin/env python3
"""audit-sfx-layer.py — HR#8: capa SFX dedicada obligatoria (track-index 60-110).

BUG REAL que cierra (caso disparador matadero CP5 gap #13): el ingeniero declaró
CP5 done con 0/10 SFX wired — había stems en disco (assets/sfx/) pero NINGUNO
conectado en el manifest/HTML, así que el render salió SIN capa SFX. Los audits
de calidad pasaban porque medían lo que existía, no el INVENTARIO contra SPEC.
HR#8 (CLAUDE.md): "Capa SFX dedicada obligatoria (track-index 60-110)". Sin gate,
"0 SFX wired" se cuela hasta el oído humano post-render.

POR QUÉ NO LO CAZABA NADIE:
  - `audit-render-audio-coverage.py` / `audit-audio.py` miden cobertura de
    NARRACIÓN + música; un video sin un solo SFX pasa esos coverage checks.
  - `audit-spec-completeness.py` (Gate 0) cuenta assets declarados en asset_list,
    pero el bug de matadero fue exactamente que existencia-en-disco ≠ wired: los
    SFX estaban generados pero NO conectados, y un check ingenuo de "¿hay mp3 en
    assets/sfx/?" daría PASS falso (había 10 archivos, 0 wired).
  Por eso este gate distingue WIRED (declarado en manifest/HTML, parte del mix)
  de ON-DISK (archivo presente pero huérfano), y exige ≥1 SFX WIRED.

REGLA:
  (a) path LEGACY HTML: ≥1 elemento <audio>/<video> con data-track-index en banda
      60-110, distinto de música/narración (clasificado por nombre/clase).
  (b) path HYBRID: ≥1 stem con class/role 'sfx' en el audio-manifest.json
      (per-clip), o archivos en assets/sfx/ DECLARADOS en el manifest/HTML — NO
      basta con estar en disco (ese fue exactamente el bug de matadero).
  FAIL si el video tiene capa SFX requerida (has_sfx_layer=true) pero 0 SFX wired,
  AUNQUE haya N archivos huérfanos en assets/sfx/ (se reportan como evidencia del
  gap: "N en disco, 0 wired").

Capability-gate: has_sfx_layer. false → not_applicable (exit 0). Agnostic-by-design:
--format REQUIRED. video_capabilities ausente → Bug #9 (exit 2).

DISEÑO TESTEABLE: lógica pura en evaluate_sfx_layer(wired_sfx, ondisk_sfx, min_sfx)
— recibe conteos/listas ya extraídos; NO toca filesystem. Wrappers runtime:
extract_wired_sfx_from_manifest() / extract_wired_sfx_from_html() / list_ondisk_sfx().

Exit: 0 PASS·not_applicable / 1 FAIL / 2 can't-measure (Bug #9 / SPEC ausente).
Authority: CLAUDE.md HR#8 + ai-video-production/SFX-PIPELINE.md §"Conectar en
index.html (track-index 60-110)" + GAPS-LOG matadero gap #13. HR#26 companion test:
test_audit-sfx-layer.py.
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

# track-index reservado a la capa SFX dedicada (HR#8). Authority: SFX-PIPELINE.md
# §"Conectar en index.html con data-track-index reservado 60-110". NO medido en F1
# (banda de diseño, no estadística de referentes) → constante de módulo overridable.
SFX_TRACK_INDEX_LO = 60
SFX_TRACK_INDEX_HI = 110
MIN_WIRED_SFX = 1  # HR#8: ≥1 SFX dedicado en el mix

# Extensiones de audio que cuentan como stem SFX en disco.
SFX_EXTS = (".mp3", ".wav", ".m4a", ".ogg", ".aac")

# Roles que NO son SFX (para excluir música/narración de la banda de track-index).
_NON_SFX_RE = re.compile(r"music|musica|música|narrat|narrac|voiceover|score|theme|crescendo|accent", re.IGNORECASE)
# Un id/clase explícitamente SFX.
_SFX_CLASS_RE = re.compile(r"^(?:sfx|sound_?effect|effect|fx)$", re.IGNORECASE)


def is_sfx_role(*, declared_class=None, name=""):
    """¿Este track es SFX? (no música/narración). True/False.

    SFX = class/role explícito 'sfx', O nombre que no matchea música/narración.
    flash_* cuenta como SFX (es un impacto, capa SFX dedicada)."""
    if declared_class is not None:
        c = str(declared_class).strip().lower()
        if _SFX_CLASS_RE.match(c) or c == "flash":
            return True
        if c in ("music", "musica", "música", "narration", "narracion", "narración",
                 "ambient", "ambience", "voice", "voiceover", "score"):
            # ambient lo tratamos aparte: NO es la capa SFX dedicada de eventos puntuales.
            return False
    if name and _NON_SFX_RE.search(name):
        return False
    # ambient por nombre tampoco cuenta como SFX dedicado de eventos.
    if name and re.search(r"ambient|drone|room.?tone", name, re.IGNORECASE):
        return False
    return bool(name) if declared_class is None else False


# ── Lógica PURA ────────────────────────────────────────────────────────────────
def evaluate_sfx_layer(wired_sfx, ondisk_sfx, *, min_sfx=MIN_WIRED_SFX):
    """PURE. wired_sfx = lista de ids SFX WIRED; ondisk_sfx = lista de archivos en disco.

    Devuelve (ok, reasons:list[dict]). FAIL si len(wired_sfx) < min_sfx, AUNQUE
    haya archivos huérfanos en disco (caso matadero gap #13). El conteo en disco
    se reporta como evidencia: "N en disco, 0 wired" deja claro el gap exacto.
    """
    n_wired = len(wired_sfx)
    n_disk = len(ondisk_sfx)
    reasons = []
    if n_wired >= min_sfx:
        reasons.append({
            "status": "ok", "wired_sfx_count": n_wired, "ondisk_sfx_count": n_disk,
            "detail": (f"{n_wired} SFX wired (≥{min_sfx} requerido por HR#8) ✓ "
                       f"[{n_disk} en disco]"),
            "wired_sample": wired_sfx[:10],
        })
        return True, reasons
    # FAIL — distinguir el sub-caso matadero (en disco pero no wired).
    if n_disk > 0:
        detail = (f"capa SFX dedicada obligatoria (HR#8) pero {n_wired} SFX WIRED — "
                  f"hay {n_disk} stem(s) en disco SIN conectar (caso matadero gap #13: "
                  f"existencia-en-disco ≠ wired; el render saldría sin capa SFX)")
    else:
        detail = (f"capa SFX dedicada obligatoria (HR#8) pero {n_wired} SFX wired y "
                  f"{n_disk} en disco — no se generó ni conectó ninguna capa SFX")
    reasons.append({
        "status": "fail", "wired_sfx_count": n_wired, "ondisk_sfx_count": n_disk,
        "detail": detail,
        "ondisk_sample": ondisk_sfx[:10],
    })
    return False, reasons


# ── Extractores runtime (filesystem) ────────────────────────────────────────────
def extract_wired_sfx_from_manifest(manifest):
    """De un audio-manifest.json (path HYBRID) → lista de ids con class/role SFX.

    Un stem está WIRED si aparece como item del manifest con class/role sfx (o flash).
    Música/narración/ambient se excluyen. Esto modela 'declarado en el mix per-clip'."""
    out = []
    items = manifest.get("assets") if isinstance(manifest, dict) else None
    if not isinstance(items, list):
        items = manifest if isinstance(manifest, list) else []
    for it in items:
        if not isinstance(it, dict):
            continue
        declared = it.get("class") or it.get("role") or it.get("layer")
        name = str(it.get("id") or it.get("name") or it.get("file") or "")
        if is_sfx_role(declared_class=declared, name=name):
            out.append(name or "?")
    return out


# Tags <audio>/<video> con data-track-index para el path LEGACY HTML.
_TAG_RE = re.compile(r"<(?:audio|video)\b[^>]*>", re.IGNORECASE)
_TRACK_IDX_RE = re.compile(r"data-track-index\s*=\s*[\"']?(\d+)", re.IGNORECASE)
_SRC_RE = re.compile(r"(?:data-src|src)\s*=\s*[\"']([^\"']+)[\"']", re.IGNORECASE)
_ID_RE = re.compile(r"\bid\s*=\s*[\"']([^\"']+)[\"']", re.IGNORECASE)
_CLASS_RE = re.compile(r"(?:data-role|data-layer|class)\s*=\s*[\"']([^\"']+)[\"']", re.IGNORECASE)


def extract_wired_sfx_from_html(html, *, lo=SFX_TRACK_INDEX_LO, hi=SFX_TRACK_INDEX_HI):
    """De un index.html (path LEGACY) → lista de ids SFX WIRED.

    SFX wired = tag <audio>/<video> con data-track-index ∈ [lo,hi] que NO sea
    música/narración por nombre/clase. Parseo por regex robusto (NO bs4)."""
    out = []
    for tag in _TAG_RE.findall(html):
        ti_m = _TRACK_IDX_RE.search(tag)
        if not ti_m:
            continue
        try:
            ti = int(ti_m.group(1))
        except ValueError:
            continue
        if not (lo <= ti <= hi):
            continue
        src_m = _SRC_RE.search(tag)
        id_m = _ID_RE.search(tag)
        class_m = _CLASS_RE.search(tag)
        name = (Path(src_m.group(1)).name if src_m else None) or (id_m.group(1) if id_m else "?")
        if is_sfx_role(declared_class=class_m.group(1) if class_m else None, name=name):
            out.append(f"{name}@track-{ti}")
    return out


def list_ondisk_sfx(sfx_dir):
    """Lista de nombres de archivo de audio en assets/sfx/ (evidencia de huérfanos)."""
    if not sfx_dir or not Path(sfx_dir).is_dir():
        return []
    return sorted(
        f.name for f in Path(sfx_dir).iterdir()
        if f.is_file() and f.suffix.lower() in SFX_EXTS)


def main():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--format", required=True, help="formato activo (agnostic-by-design)")
    parser.add_argument("--spec", required=True, help="creative-specs/<id>.yaml (capability gate)")
    parser.add_argument("--manifest", default=None,
                        help="audio-manifest.json (path HYBRID). Default: <project-dir>/assets/audio-manifest.json")
    parser.add_argument("--html", default=None, help="index.html (path LEGACY)")
    parser.add_argument("--sfx-dir", default=None,
                        help="dir de stems SFX. Default: <project-dir>/assets/sfx")
    parser.add_argument("--project-dir", default=None,
                        help="dir del proyecto. Default: <spec_dir>/../<spec_stem>")
    parser.add_argument("--min-sfx", type=int, default=MIN_WIRED_SFX)
    parser.add_argument("--track-lo", type=int, default=SFX_TRACK_INDEX_LO)
    parser.add_argument("--track-hi", type=int, default=SFX_TRACK_INDEX_HI)
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

    has_sfx = bool(caps.get("has_sfx_layer", False))

    project_dir = Path(args.project_dir) if args.project_dir else (spec_path.parent.parent / spec_path.stem)
    manifest_path = Path(args.manifest) if args.manifest else (project_dir / "assets" / "audio-manifest.json")
    html_path = Path(args.html) if args.html else (project_dir / "index.html")
    sfx_dir = Path(args.sfx_dir) if args.sfx_dir else (project_dir / "assets" / "sfx")

    if args.dry_run:
        print(f"format: {args.format}\nspec: {spec_path}\nhas_sfx_layer: {has_sfx}\n"
              f"branch: {'sfx_layer_check' if has_sfx else 'not_applicable'}\n"
              f"manifest: {manifest_path} (exists={manifest_path.exists()})\n"
              f"html: {html_path} (exists={html_path.exists()})\n"
              f"sfx_dir: {sfx_dir} (exists={Path(sfx_dir).is_dir()})\n"
              f"track-index band: [{args.track_lo}, {args.track_hi}], min_sfx: {args.min_sfx}")
        return 0

    if not has_sfx:
        print(json.dumps({
            "format": args.format, "overall_status": "not_applicable",
            "detail": "has_sfx_layer=false → SFX layer check skipped (este video no requiere capa SFX)",
        }, indent=2, ensure_ascii=False))
        return 0

    wired = []
    sources = []
    if manifest_path.exists():
        try:
            with open(manifest_path) as f:
                manifest = json.load(f)
            wired.extend(extract_wired_sfx_from_manifest(manifest))
            sources.append(str(manifest_path))
        except (OSError, json.JSONDecodeError) as e:
            print(f"WARNING: no se pudo parsear manifest {manifest_path}: {e}", file=sys.stderr)
    if html_path.exists():
        try:
            wired.extend(extract_wired_sfx_from_html(
                html_path.read_text(errors="ignore"), lo=args.track_lo, hi=args.track_hi))
            sources.append(str(html_path))
        except OSError as e:
            print(f"WARNING: no se pudo leer html {html_path}: {e}", file=sys.stderr)

    ondisk = list_ondisk_sfx(sfx_dir)

    if not sources:
        # Sin manifest NI html no podemos medir "wired"; pero SI hay disco, es el
        # gap matadero en su forma más cruda (archivos sin ninguna fuente de wiring).
        print(json.dumps({
            "format": args.format, "overall_status": "cant_measure",
            "ondisk_sfx_count": len(ondisk),
            "detail": (f"no se encontró ni manifest ({manifest_path}) ni html ({html_path}) — "
                       f"no hay fuente de wiring que auditar ({len(ondisk)} stem(s) en disco)"),
        }, indent=2, ensure_ascii=False))
        return 2

    ok, reasons = evaluate_sfx_layer(wired, ondisk, min_sfx=args.min_sfx)

    report = {
        "format": args.format, "spec": str(spec_path), "sources": sources,
        "sfx_dir": str(sfx_dir),
        "track_index_band": [args.track_lo, args.track_hi], "min_wired_sfx": args.min_sfx,
        "overall_status": "pass" if ok else "fail", "overall_pass": ok,
        "wired_sfx_count": len(wired), "ondisk_sfx_count": len(ondisk),
        "reasons": reasons,
    }
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
