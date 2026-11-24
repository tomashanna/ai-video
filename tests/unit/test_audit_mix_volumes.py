#!/usr/bin/env python3
"""test_audit-mix-volumes.py — HR#26 companion test for audit-mix-volumes.py (HR#9b).

ANTI-THEATER: prueba que el validator CAZA el bug REAL (música mezclada FUERA de su
banda 0.05-0.18 — ej. 0.45 que tapa la narración; flash a 0.20 que no pega) y NO
molesta en el caso bueno (todos los roles dentro de banda) ni cuando el manifest no
declara volúmenes (HYBRID aplica defaults → informativo, no FAIL).

Cobertura:
  classify_role: por class del manifest, por nombre (flash/ambient/music/narration),
    por track-index 60-110 → sfx.
  PURE evaluate_mix_volumes:
    (a) música 0.45 (banda 0.05-0.18) → FAIL nombrando el track.
    (b) flash 0.20 (banda 0.55-0.65) → FAIL (no pega).
    (c) caso bueno: narración 1.0 / música 0.12 / sfx 0.28 / flash 0.60 / ambient 0.14 → PASS.
    (d) sin volumen declarado → no_volume_declared (no FAIL).
    (e) rol desconocido → warning (no FAIL).
    (f) límites: música 0.18 PASS, 0.181 FAIL; narración 1.0 PASS, 0.9 FAIL.
  Extractores runtime: manifest (class) + HTML (data-volume/track-index + JS volume:).
  CLI por subprocess: --format requerido; Bug#9; not_applicable; FAIL real; PASS.

Runnable: python3 test_audit-mix-volumes.py  → imprime "OK: ..." o sys.exit(1).
"""
import importlib.util
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[2] / "src/ai_video/audits/audit_mix_volumes.py"


def _load():
    spec = importlib.util.spec_from_file_location("mix_vol", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _run(args):
    return subprocess.run([sys.executable, str(SCRIPT)] + args, capture_output=True, text=True)


M = _load()
failures = []


def check(cond, msg):
    if not cond:
        failures.append(msg)
        print(f"  FAIL: {msg}")
    else:
        print(f"  ok: {msg}")


# ───────────────────────── classify_role ─────────────────────────
print("[pure] classify_role")
check(M.classify_role(declared_role="music") == "music", "class=music → music")
check(M.classify_role(declared_role="sfx", name="footsteps") == "sfx", "class=sfx → sfx")
check(M.classify_role(declared_role="sfx", name="flash_electric_impact") == "flash",
      "class=sfx + name flash → flash (subtipo con banda propia)")
check(M.classify_role(name="hook_crescendo") == "music", "name crescendo → music")
check(M.classify_role(name="ambient_tunnel") == "ambient", "name ambient → ambient")
check(M.classify_role(name="drone_base") == "ambient", "name drone → ambient")
check(M.classify_role(name="flash_wet_impact") == "flash", "name flash → flash")
check(M.classify_role(name="narration_seg_01") == "narration", "name narration → narration")
check(M.classify_role(name="random_thud", track_index=72) == "sfx",
      "track-index 72 ∈ [60,110] → sfx")
check(M.classify_role(name="random_thud", track_index=12) is None,
      "track-index 12 fuera de banda SFX + nombre genérico → None")


# ───────────────────────── PURE evaluate_mix_volumes (the heart of the bug) ─────────────────────────
print("[pure] evaluate_mix_volumes")

# (a) música 0.45 fuera de banda 0.05-0.18 → FAIL (tapa la narración).
ok, reasons = M.evaluate_mix_volumes([
    {"id": "drone_base", "role": "music", "volume": 0.45},
])
check(ok is False, "(a) música 0.45 (banda 0.05-0.18) → FAIL")
fails = [r for r in reasons if r["status"] == "fail"]
check(fails and fails[0]["id"] == "drone_base", "(a) FAIL nombra el track ofensor (drone_base)")
check(any("FUERA de banda" in r["detail"] for r in fails), "(a) razón cita 'FUERA de banda'")

# (b) flash 0.20 (banda 0.55-0.65) → FAIL (no pega).
ok, _ = M.evaluate_mix_volumes([{"id": "flash_wet_impact", "role": "flash", "volume": 0.20}])
check(ok is False, "(b) flash 0.20 (banda 0.55-0.65) → FAIL (no pega)")

# (c) caso bueno: todos dentro de banda → PASS.
ok, reasons = M.evaluate_mix_volumes([
    {"id": "narr", "role": "narration", "volume": 1.0},
    {"id": "music", "role": "music", "volume": 0.12},
    {"id": "footsteps", "role": "sfx", "volume": 0.28},
    {"id": "flash", "role": "flash", "volume": 0.60},
    {"id": "ambient", "role": "ambient", "volume": 0.14},
])
check(ok is True, "(c) todos los roles dentro de banda → PASS")
check(all(r["status"] == "ok" for r in reasons), "(c) sin fails en caso bueno")

# (d) sin volumen declarado → no_volume_declared, no FAIL (HYBRID aplica defaults).
ok, reasons = M.evaluate_mix_volumes([{"id": "drone_base", "role": "music", "volume": None}])
check(ok is True, "(d) volumen None → PASS (pipeline aplica default canónico)")
check(reasons[0]["status"] == "no_volume_declared", "(d) status=no_volume_declared")

# (e) rol desconocido → warning, no FAIL.
ok, reasons = M.evaluate_mix_volumes([{"id": "mystery", "role": None, "volume": 0.99}])
check(ok is True, "(e) rol desconocido → PASS (warning, no FAIL)")
check(reasons[0]["status"] == "warning", "(e) status=warning para rol no clasificable")

# (f) límites de banda.
check(M.evaluate_mix_volumes([{"id": "m", "role": "music", "volume": 0.18}])[0] is True,
      "(f) música 0.18 (borde superior) → PASS")
check(M.evaluate_mix_volumes([{"id": "m", "role": "music", "volume": 0.181}])[0] is False,
      "(f) música 0.181 (apenas fuera) → FAIL")
check(M.evaluate_mix_volumes([{"id": "n", "role": "narration", "volume": 1.0}])[0] is True,
      "(f) narración 1.0 exacta → PASS")
check(M.evaluate_mix_volumes([{"id": "n", "role": "narration", "volume": 0.9}])[0] is False,
      "(f) narración 0.9 → FAIL (debe ser 1.0)")

# (mix) un track bueno no enmascara al malo.
ok, reasons = M.evaluate_mix_volumes([
    {"id": "good_music", "role": "music", "volume": 0.10},
    {"id": "bad_music", "role": "music", "volume": 0.50},
])
bad = [r["id"] for r in reasons if r["status"] == "fail"]
check(ok is False and bad == ["bad_music"], "(mix) un track bueno no enmascara al malo")


# ───────────────────────── extractores runtime ─────────────────────────
print("[runtime] extract_tracks_from_manifest + extract_tracks_from_html")

# manifest estilo ultimo-tren-carga: class sfx/music/ambient, SIN volume → todos no_volume_declared.
manifest = {"assets": [
    {"id": "drone_base", "class": "music"},
    {"id": "footsteps_wet_concrete", "class": "sfx"},
    {"id": "ambient_tunnel", "class": "ambient"},
    {"id": "flash_electric_impact", "class": "sfx"},  # name flash → flash
]}
tracks = M.extract_tracks_from_manifest(manifest)
roles = {t["id"]: t["role"] for t in tracks}
check(roles["drone_base"] == "music", "manifest: class music → music")
check(roles["footsteps_wet_concrete"] == "sfx", "manifest: class sfx → sfx")
check(roles["ambient_tunnel"] == "ambient", "manifest: class ambient → ambient")
check(roles["flash_electric_impact"] == "flash", "manifest: class sfx + name flash → flash")
check(all(t["volume"] is None for t in tracks), "manifest sin volume → todos volume None")

# manifest CON un volume fuera de banda → debe FAIL al evaluar.
manifest_bad = {"assets": [{"id": "loud_music", "class": "music", "volume": 0.45}]}
ok, _ = M.evaluate_mix_volumes(M.extract_tracks_from_manifest(manifest_bad))
check(ok is False, "manifest con volume 0.45 declarado en música → FAIL al evaluar")

# HTML: data-volume + data-track-index + JS volume:.
# Nota: 'drone' clasifica como ambient (correcto por heurística de nombre); usamos
# 'music_score.mp3' para el caso música-fuera-de-banda.
html = """
<audio id="narr" data-src="assets/tts/narr.mp3" data-volume="1.0" data-track-index="10"></audio>
<audio id="m1" src="assets/music/music_score.mp3" data-volume="0.45" data-track-index="40"></audio>
<audio id="fx1" src="assets/sfx/footsteps.mp3" volume="0.28" data-track-index="72"></audio>
<script> gsap.to(musicEl, { volume: 0.06, duration: 0.2 }); </script>
"""
htracks = M.extract_tracks_from_html(html)
by_name = {t["id"]: t for t in htracks}
check(by_name["narr.mp3"]["volume"] == 1.0 and by_name["narr.mp3"]["role"] == "narration",
      "HTML: narr data-volume 1.0 + nombre → narration")
check(by_name["music_score.mp3"]["volume"] == 0.45 and by_name["music_score.mp3"]["role"] == "music",
      "HTML: música 0.45 extraída (será FAIL)")
check(by_name["footsteps.mp3"]["role"] == "sfx",
      "HTML: footsteps track-index 72 → sfx")
ok, _ = M.evaluate_mix_volumes(htracks)
check(ok is False, "HTML con música 0.45 → FAIL al evaluar")


# ───────────────────────── CLI (subprocess + fixtures) ─────────────────────────
print("[cli] subprocess paths")
tmp = tempfile.mkdtemp()
try:
    proj = Path(tmp) / "proj"
    (proj / "assets").mkdir(parents=True)
    specs_dir = Path(tmp) / "creative-specs"
    specs_dir.mkdir()
    spec = specs_dir / "proj.yaml"

    def write_spec(*, has_sfx=True, has_music=True, has_tts=True, omit_caps=False):
        caps = "" if omit_caps else (
            "video_capabilities:\n"
            f"  has_sfx_layer: {str(has_sfx).lower()}\n"
            f"  has_layer_3_music: {str(has_music).lower()}\n"
            f"  has_tts_narration: {str(has_tts).lower()}\n"
            '  audio_mix_target: "lufs_-14"\n'
        )
        spec.write_text(f'schema_version: "v11.1"\n{caps}', encoding="utf-8")

    def write_manifest(items):
        (proj / "assets" / "audio-manifest.json").write_text(
            json.dumps({"assets": items}), encoding="utf-8")

    # --format requerido.
    write_spec()
    r = _run(["--spec", str(spec), "--dry-run"])
    check(r.returncode != 0 and "format" in r.stderr.lower(), "CLI: --format requerido")

    # Bug #9: video_capabilities ausente → exit 2.
    write_spec(omit_caps=True)
    r = _run(["--format", "horror-choice", "--spec", str(spec)])
    check(r.returncode == 2, "CLI: video_capabilities ausente → Bug#9 exit 2")

    # not_applicable: ninguna capability de audio → exit 0.
    write_spec(has_sfx=False, has_music=False, has_tts=False)
    # quitar audio_mix_target también:
    spec.write_text(
        'schema_version: "v11.1"\nvideo_capabilities:\n'
        '  has_sfx_layer: false\n  has_layer_3_music: false\n  has_tts_narration: false\n',
        encoding="utf-8")
    write_manifest([{"id": "x", "class": "music", "volume": 0.5}])
    r = _run(["--format", "horror-choice", "--spec", str(spec)])
    check(r.returncode == 0 and "not_applicable" in r.stdout.lower(),
          "CLI: sin capabilities de audio → not_applicable exit 0")

    # FAIL real: música 0.45 declarada en manifest.
    write_spec()
    write_manifest([
        {"id": "drone_base", "class": "music", "volume": 0.45},
        {"id": "footsteps", "class": "sfx", "volume": 0.28},
    ])
    r = _run(["--format", "horror-choice", "--spec", str(spec)])
    check(r.returncode == 1, "CLI: música 0.45 en manifest → exit 1 (FAIL)")
    payload = json.loads(r.stdout)
    check(payload["overall_pass"] is False and payload["fail_count"] >= 1,
          "CLI: report marca overall_pass false + fail_count≥1")

    # PASS: todos dentro de banda.
    write_manifest([
        {"id": "drone_base", "class": "music", "volume": 0.12},
        {"id": "footsteps", "class": "sfx", "volume": 0.28},
        {"id": "flash_x", "class": "sfx", "volume": 0.60},
    ])
    r = _run(["--format", "horror-choice", "--spec", str(spec)])
    payload = json.loads(r.stdout)
    check(r.returncode == 0 and payload["overall_pass"] is True,
          "CLI: todos dentro de banda → PASS exit 0")

    # PASS: manifest SIN volúmenes (HYBRID real) → no_volume_declared, no FAIL.
    write_manifest([
        {"id": "drone_base", "class": "music"},
        {"id": "footsteps", "class": "sfx"},
    ])
    r = _run(["--format", "horror-choice", "--spec", str(spec)])
    payload = json.loads(r.stdout)
    check(r.returncode == 0 and payload["overall_pass"] is True
          and payload["no_volume_declared_count"] == 2,
          "CLI: manifest sin volúmenes (HYBRID) → PASS, no_volume_declared=2")

    # cant_measure: ni manifest ni html → exit 2.
    (proj / "assets" / "audio-manifest.json").unlink()
    r = _run(["--format", "horror-choice", "--spec", str(spec)])
    check(r.returncode == 2 and "cant_measure" in r.stdout, "CLI: sin manifest ni html → exit 2 cant_measure")

    # --band override: subir banda de música a 0.05:0.50 hace pasar el 0.45.
    write_manifest([{"id": "drone_base", "class": "music", "volume": 0.45}])
    r = _run(["--format", "horror-choice", "--spec", str(spec), "--band", "music=0.05:0.50"])
    check(r.returncode == 0, "CLI: --band music=0.05:0.50 hace PASS al 0.45 (override funciona)")
finally:
    shutil.rmtree(tmp, ignore_errors=True)


# ───────────────────────── INTEGRATION: real SPEC must parse without crash ─────────────────────────
print("[integration] real ultimo-tren-carga SPEC + manifest parse")
real = Path(__file__).resolve().parents[2] / "examples/specs/ultimo-tren-carga.yaml"
if real.exists():
    r = _run(["--format", "horror-choice", "--spec", str(real)])
    check("Traceback" not in r.stderr, "real SPEC: no crash")
    check(r.returncode in (0, 1, 2), f"real SPEC: exit válido (got {r.returncode})")
else:
    print("  (skip: real SPEC not present)")


# ───────────────────────── verdict ─────────────────────────
if failures:
    print(f"\n{len(failures)} FAILURE(S):")
    for f in failures:
        print(f"  - {f}")
    sys.exit(1)
print("\nOK: audit-mix-volumes.py catches out-of-band mix (music 0.45 tapando narración / flash 0.20 sin pegar); clean cases + HYBRID-no-volume pass.")
