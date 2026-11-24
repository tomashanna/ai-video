#!/usr/bin/env python3
"""test_audit-avu-sync-contract.py — HR#26 companion test for audit-avu-sync-contract.py (Q24/HR#25).

ANTI-THEATER: prueba que el validator CAZA el bug REAL (matadero iter 3-4 compose-time
fragility: shot ACOPLADO audio↔visual SIN AVU pre-rendered NI sync_contract → desync) y
NO molesta en los caminos buenos (AVU .mp4 en disco / sync_contract completo) ni en shots
no-acoplados (sin AVU/lip-sync/contract → regla no aplica).

Cobertura (CASO DISPARADOR del prompt):
  PURE evaluate_avu_sync_contract:
    (a) shot lip_sync coupled SIN AVU NI contract → FAIL nombrando el shot + razón compose-time.
    (b) shot coupled CON AVU .mp4 en disco → PASS.
    (c) shot coupled CON sync_contract completo → PASS.
    (d) shot NO-acoplado → regla no aplica (rule_applies False).
    (e) SPEC sin ningún shot acoplado → not_applicable.
    (mix) un shot bueno no enmascara a un shot acoplado roto.
  Runtime helpers: sync_contract_missing_fields; resolve_avu_on_disk (stat real);
    _atomic_clip_for_shot (lip-sync bundled); build_shot_record (detección de acople).
  CLI por subprocess con fixtures tempfile:
    --format requerido; Bug#9 video_capabilities ausente; not_applicable (sin acople / sin clips);
    FAIL real (lip_sync sin nada) → exit 1; PASS con AVU mp4 (tempfile); PASS con sync_contract.

Runnable: python3 test_audit-avu-sync-contract.py  → imprime "OK: ..." o sys.exit(1).
"""

import importlib.util
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[2] / "src/ai_video/audits/audit_avu_sync_contract.py"


def _load():
    spec = importlib.util.spec_from_file_location("avu_sync", SCRIPT)
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


# ───────────────────────── PURE FUNCTION (the heart of the bug) ─────────────────────────
print("[pure] evaluate_avu_sync_contract")

# (a) CASO DISPARADOR: shot lip_sync ACOPLADO sin AVU ni contract → FAIL nombrando el shot.
ok, summary = M.evaluate_avu_sync_contract(
    [
        {
            "shot_id": "shot_lipsync_naked",
            "coupled": True,
            "coupling_reasons": ["has_lip_sync_required=true"],
            "avu_present": False,
            "has_complete_sync_contract": False,
            "sync_contract_missing_fields": ["visual_start_s", "audio_start_s", "tolerance_s"],
        },
    ]
)
check(ok is False, "(a) lip_sync coupled SIN AVU NI contract → FAIL (matadero compose-fragility cazado)")
fails = [s for s in summary["shots"] if s["status"] == "fail"]
check([s["shot_id"] for s in fails] == ["shot_lipsync_naked"], "(a) FAIL nombra el shot ofensor")
check(any("compose-time fragility" in s["detail"] for s in fails), "(a) razón cita compose-time fragility")
check(summary["applicable"] is True and summary["coupled_shots"] == 1, "(a) applicable + 1 coupled shot")

# (b) shot coupled CON AVU .mp4 en disco → PASS.
ok, summary = M.evaluate_avu_sync_contract(
    [
        {
            "shot_id": "shot_countdown",
            "coupled": True,
            "coupling_reasons": ["avu_overlay_clip='countdown-3-2-1-film-leader-with-ticks.mp4'"],
            "avu_present": True,
            "has_complete_sync_contract": False,
            "avu_paths_checked": ["/x/countdown-3-2-1-film-leader-with-ticks.mp4"],
        },
    ]
)
check(ok is True, "(b) coupled CON AVU en disco → PASS")
check(
    any("AVU .mp4 en disco" in (s.get("satisfied_by") or []) for s in summary["shots"]),
    "(b) satisfied_by cita AVU .mp4 en disco",
)

# (c) shot coupled CON sync_contract completo → PASS.
ok, summary = M.evaluate_avu_sync_contract(
    [
        {
            "shot_id": "shot_framing",
            "coupled": True,
            "coupling_reasons": ["sync_contract declarado"],
            "avu_present": False,
            "has_complete_sync_contract": True,
        },
    ]
)
check(ok is True, "(c) coupled CON sync_contract completo → PASS")
check(
    any("sync_contract completo" in (s.get("satisfied_by") or []) for s in summary["shots"]),
    "(c) satisfied_by cita sync_contract completo",
)

# (d) shot NO-acoplado → regla no aplica.
ok, summary = M.evaluate_avu_sync_contract(
    [
        {"shot_id": "shot_plain", "coupled": False, "coupling_reasons": []},
        {
            "shot_id": "shot_coupled_ok",
            "coupled": True,
            "coupling_reasons": ["has_lip_sync_required=true"],
            "avu_present": True,
            "has_complete_sync_contract": False,
        },
    ]
)
check(ok is True, "(d) no-acoplado + acoplado-ok → PASS")
rec_plain = next(s for s in summary["shots"] if s["shot_id"] == "shot_plain")
check(rec_plain["rule_applies"] is False, "(d) shot no-acoplado: rule_applies=False")

# (e) SPEC sin NINGÚN shot acoplado → not_applicable.
ok, summary = M.evaluate_avu_sync_contract(
    [
        {"shot_id": "s1", "coupled": False, "coupling_reasons": []},
        {"shot_id": "s2", "coupled": False, "coupling_reasons": []},
    ]
)
check(
    ok is True and summary["applicable"] is False,
    "(e) ningún shot acoplado → not_applicable (applicable=False)",
)

# (mix) un shot bueno no enmascara al acoplado roto.
ok, summary = M.evaluate_avu_sync_contract(
    [
        {
            "shot_id": "good",
            "coupled": True,
            "coupling_reasons": ["avu_overlay_clip='x.mp4'"],
            "avu_present": True,
            "has_complete_sync_contract": False,
        },
        {
            "shot_id": "bad",
            "coupled": True,
            "coupling_reasons": ["has_lip_sync_required=true"],
            "avu_present": False,
            "has_complete_sync_contract": False,
        },
    ]
)
fail_ids = [s["shot_id"] for s in summary["shots"] if s["status"] == "fail"]
check(ok is False and fail_ids == ["bad"], "(mix) un shot bueno no enmascara al acoplado roto")


# ───────────────────────── RUNTIME HELPERS ─────────────────────────
print("[runtime] sync_contract_missing_fields + resolve_avu_on_disk + build_shot_record")

check(
    M.sync_contract_missing_fields({"visual_start_s": 2.0, "audio_start_s": 2.0, "tolerance_s": 0.1}) == [],
    "sync_contract completo → sin campos faltantes",
)
check(
    M.sync_contract_missing_fields({"visual_start_s": 2.0}) == ["audio_start_s", "tolerance_s"],
    "sync_contract incompleto → lista los faltantes",
)
check(
    M.sync_contract_missing_fields(None) == list(M.REQUIRED_SYNC_CONTRACT_FIELDS),
    "sync_contract None → todos faltan",
)
check(
    M.sync_contract_missing_fields({"visual_start_s": 2.0, "audio_start_s": None, "tolerance_s": 0.1})
    == ["audio_start_s"],
    "campo None-valued cuenta como faltante",
)

_tmp = tempfile.mkdtemp()
try:
    libdir = Path(_tmp) / "avu-library"
    libdir.mkdir()
    (libdir / "countdown-3-2-1-film-leader-with-ticks.mp4").write_bytes(b"x" * 100)
    # basename resuelto contra la library
    present, checked = M.resolve_avu_on_disk(
        "countdown-3-2-1-film-leader-with-ticks.mp4",
        avu_library_dir=str(libdir),
        project_dir=None,
        clips_atomic_dir=None,
    )
    check(present is True, "resolve_avu_on_disk: basename existente en library → present")
    present, _ = M.resolve_avu_on_disk(
        "decision-freeze-with-tick-3-2-1.mp4",
        avu_library_dir=str(libdir),
        project_dir=None,
        clips_atomic_dir=None,
    )
    check(present is False, "resolve_avu_on_disk: AVU ausente → not present (stat real, no asume)")
    # null tokens → no AVU
    present, checked = M.resolve_avu_on_disk(
        None, avu_library_dir=str(libdir), project_dir=None, clips_atomic_dir=None
    )
    check(present is False and checked == [], "resolve_avu_on_disk: null → no AVU, sin paths")

    # _atomic_clip_for_shot: lip-sync dialog bundled en clips-atomic/
    atomic = Path(_tmp) / "clips-atomic"
    atomic.mkdir()
    (atomic / "shot_05_dario_rule_atomic.mp4").write_bytes(b"x" * 100)
    present, checked = M._atomic_clip_for_shot("shot_05", str(atomic))
    check(present is True, "_atomic_clip_for_shot: shot_05_*_atomic.mp4 existe → present (lip-sync bundled)")
    present, _ = M._atomic_clip_for_shot("shot_99", str(atomic))
    check(present is False, "_atomic_clip_for_shot: shot sin atomic → not present")

    # build_shot_record: lip_sync coupled, atomic clip presente → coupled + avu_present (satisfecho).
    rec = M.build_shot_record(
        {"shot_id": "shot_05", "has_lip_sync_required": True},
        avu_library_dir=str(libdir),
        project_dir=None,
        clips_atomic_dir=str(atomic),
    )
    check(
        rec["coupled"] is True and rec["avu_present"] is True,
        "build_shot_record: lip_sync + atomic clip → coupled & avu_present",
    )

    # build_shot_record: lip_sync SIN atomic clip y SIN contract → coupled pero NO satisfecho (FAIL-able).
    rec = M.build_shot_record(
        {"shot_id": "shot_xx", "has_lip_sync_required": True},
        avu_library_dir=str(libdir),
        project_dir=None,
        clips_atomic_dir=str(atomic),
    )
    check(
        rec["coupled"] is True and rec["avu_present"] is False and rec["has_complete_sync_contract"] is False,
        "build_shot_record: lip_sync naked → coupled, sin AVU, sin contract (el bug)",
    )

    # build_shot_record: sync_contract top-level completo → coupled + contract ok.
    rec = M.build_shot_record(
        {
            "shot_id": "shot_c",
            "sync_contract": {"visual_start_s": 2.0, "audio_start_s": 2.0, "tolerance_s": 0.1},
        },
        avu_library_dir=str(libdir),
        project_dir=None,
        clips_atomic_dir=None,
    )
    check(
        rec["coupled"] is True and rec["has_complete_sync_contract"] is True,
        "build_shot_record: sync_contract completo → coupled & contract ok",
    )

    # build_shot_record: audio_visual_atomic_units type sync_contract con contract incompleto → coupled, contract NO ok.
    rec = M.build_shot_record(
        {
            "shot_id": "shot_avu",
            "audio_visual_atomic_units": [
                {"id": "framing", "type": "sync_contract", "contract": {"visual_start_s": 2.0}}
            ],
        },
        avu_library_dir=str(libdir),
        project_dir=None,
        clips_atomic_dir=None,
    )
    check(
        rec["coupled"] is True and rec["has_complete_sync_contract"] is False,
        "build_shot_record: AVU-units sync_contract incompleto → coupled, contract NO ok",
    )

    # build_shot_record: shot plano (sin nada) → no coupled.
    rec = M.build_shot_record(
        {"shot_id": "shot_plain", "has_lip_sync_required": False, "avu_overlay_clip": None},
        avu_library_dir=str(libdir),
        project_dir=None,
        clips_atomic_dir=None,
    )
    check(rec["coupled"] is False, "build_shot_record: shot sin acople → not coupled")
finally:
    shutil.rmtree(_tmp, ignore_errors=True)


# ───────────────────────── CLI (subprocess + fixtures) ─────────────────────────
print("[cli] subprocess paths (CASO DISPARADOR end-to-end)")
tmp = tempfile.mkdtemp()
try:
    spec = Path(tmp) / "spec.yaml"

    def write_spec(body, *, has_clips=True, omit_caps=False):
        caps = (
            ""
            if omit_caps
            else (
                "video_capabilities:\n"
                f"  has_ai_generated_clips: {str(has_clips).lower()}\n"
                '  format_type: "interactive_choice"\n'
            )
        )
        spec.write_text(f'schema_version: "v11.2"\n{caps}{body}', encoding="utf-8")

    # --format requerido.
    write_spec("shot_list: []\n")
    r = _run(["--spec", str(spec), "--dry-run"])
    check(r.returncode != 0 and "format" in r.stderr.lower(), "CLI: --format requerido (exit≠0)")

    # Bug #9: video_capabilities ausente → exit 2.
    write_spec("shot_list: []\n", omit_caps=True)
    r = _run(["--format", "horror-choice", "--spec", str(spec)])
    check(r.returncode == 2, "CLI: video_capabilities ausente → Bug#9 exit 2")

    # not_applicable: has_ai_generated_clips=false → exit 0.
    write_spec("shot_list:\n  - shot_id: shot_01\n    has_lip_sync_required: true\n", has_clips=False)
    r = _run(["--format", "horror-choice", "--spec", str(spec)])
    check(
        r.returncode == 0 and "not_applicable" in r.stdout.lower(),
        "CLI: has_ai_generated_clips=false → not_applicable exit 0",
    )

    # not_applicable: ningún shot acoplado (con clips AI) → exit 0.
    write_spec(
        "shot_list:\n  - shot_id: shot_02\n    has_lip_sync_required: false\n    avu_overlay_clip: null\n"
    )
    r = _run(["--format", "horror-choice", "--spec", str(spec)])
    check(
        r.returncode == 0 and "not_applicable" in r.stdout.lower(),
        "CLI: ningún shot acoplado → not_applicable exit 0",
    )

    # CASO DISPARADOR — FAIL: shot lip_sync_required:true SIN AVU NI contract.
    # avu_overlay_clip apunta a un AVU INEXISTENTE en disco + clips-atomic vacío.
    write_spec(
        "shot_list:\n  - shot_id: shot_05\n    has_lip_sync_required: true\n    avu_overlay_clip: null\n"
    )
    r = _run(
        [
            "--format",
            "horror-choice",
            "--spec",
            str(spec),
            "--project-dir",
            str(Path(tmp) / "noproj"),
            "--avu-library-dir",
            str(Path(tmp) / "nolib"),
        ]
    )
    check(r.returncode == 1, "CLI: lip_sync sin AVU ni contract → exit 1 (FAIL — CASO DISPARADOR)")
    check("shot_05" in r.stdout and '"fail"' in r.stdout, "CLI: FAIL nombra shot_05")

    # PASS con AVU .mp4 (tempfile): avu_overlay_clip resuelve a un mp4 existente en la library.
    libdir = Path(tmp) / "avu-library"
    libdir.mkdir(exist_ok=True)
    (libdir / "countdown-3-2-1-film-leader-with-ticks.mp4").write_bytes(b"x" * 100)
    write_spec(
        "shot_list:\n"
        "  - shot_id: shot_01b\n"
        "    has_lip_sync_required: false\n"
        "    avu_overlay_clip: countdown-3-2-1-film-leader-with-ticks.mp4\n"
    )
    r = _run(["--format", "horror-choice", "--spec", str(spec), "--avu-library-dir", str(libdir)])
    payload = json.loads(r.stdout)
    check(
        r.returncode == 0 and payload["overall_pass"] is True,
        "CLI: avu_overlay_clip → AVU mp4 en disco → PASS exit 0",
    )

    # PASS con sync_contract completo declarado en el shot.
    write_spec(
        "shot_list:\n"
        "  - shot_id: shot_06\n"
        "    has_lip_sync_required: true\n"
        "    sync_contract:\n"
        "      visual_start_s: 25.5\n"
        "      audio_start_s: 25.5\n"
        "      tolerance_s: 0.1\n"
    )
    r = _run(
        [
            "--format",
            "horror-choice",
            "--spec",
            str(spec),
            "--project-dir",
            str(Path(tmp) / "noproj"),
            "--avu-library-dir",
            str(Path(tmp) / "nolib"),
        ]
    )
    payload = json.loads(r.stdout)
    check(r.returncode == 0 and payload["overall_pass"] is True, "CLI: sync_contract completo → PASS exit 0")

    # PASS con audio_visual_atomic_units type sync_contract completo (forma canonical § 7.11.4).
    write_spec(
        "shot_list:\n"
        "  - shot_id: shot_06b\n"
        "    audio_visual_atomic_units:\n"
        "      - id: narrator_framing\n"
        "        type: sync_contract\n"
        "        contract:\n"
        "          visual_start_s: 2.0\n"
        "          audio_start_s: 2.0\n"
        "          tolerance_s: 0.1\n"
    )
    r = _run(
        [
            "--format",
            "horror-choice",
            "--spec",
            str(spec),
            "--project-dir",
            str(Path(tmp) / "noproj"),
            "--avu-library-dir",
            str(Path(tmp) / "nolib"),
        ]
    )
    payload = json.loads(r.stdout)
    check(
        r.returncode == 0 and payload["overall_pass"] is True,
        "CLI: audio_visual_atomic_units sync_contract completo → PASS exit 0",
    )
finally:
    shutil.rmtree(tmp, ignore_errors=True)


# ───────────────────────── INTEGRATION: real SPEC must parse without crash ─────────────────────────
print("[integration] real ultimo-tren-carga SPEC parses")
real = Path(__file__).resolve().parents[2] / "examples/specs/ultimo-tren-carga.yaml"
if real.exists():
    r = _run(["--format", "horror-choice", "--spec", str(real)])
    check("Traceback" not in r.stderr, "real SPEC: no crash")
    check(r.returncode in (0, 1), f"real SPEC: exit 0/1 (got {r.returncode})")
else:
    print("  (skip: real SPEC not present)")


# ───────────────────────── verdict ─────────────────────────
if failures:
    print(f"\n{len(failures)} FAILURE(S):")
    for f in failures:
        print(f"  - {f}")
    sys.exit(1)
print(
    "\nOK: audit-avu-sync-contract.py catches matadero compose-time fragility "
    "(coupled shot sin AVU ni sync_contract); AVU-mp4 / sync_contract / no-coupled cases pass."
)
