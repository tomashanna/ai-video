"""``ai-video`` — single entry point for every tool in the toolkit.

    ai-video list                       # all tools with a one-line summary
    ai-video doctor                     # check binaries, optional deps and API keys
    ai-video validate-spec SPEC.yaml    # schema-validate a creative spec
    ai-video budget                     # show recorded paid-API spend
    ai-video <tool> [args...]           # e.g. ai-video audit-ui-safe-zones --help

Tools keep the names of the original standalone scripts (``audit-foo.py`` ->
``ai-video audit-foo``), and each is also runnable as ``python -m <module>``.
Modules are imported lazily so a tool with heavy optional dependencies (whisper,
google-genai, replicate) never slows down or breaks unrelated tools.
"""

from __future__ import annotations

import ast
import importlib
import importlib.util
import sys
from collections.abc import Sequence
from pathlib import Path

from ai_video.errors import AIVideoError

TOOLS: dict[str, str] = {
    # providers (paid APIs / local models)
    "tts": "ai_video.providers.tts",
    "sfx": "ai_video.providers.sfx",
    "image": "ai_video.providers.image",
    "video": "ai_video.providers.video",
    "veo3": "ai_video.providers.veo3",
    "captions": "ai_video.providers.captions",
    "gemini-midexec-vision": "ai_video.providers.gemini_midexec_vision",
    # build / assembly
    "build-clip-atomic": "ai_video.build.build_clip_atomic",
    "build-video-hybrid": "ai_video.build.build_video_hybrid",
    "build-avu-hook-transition": "ai_video.build.build_avu_hook_transition",
    "build-avu-outro-card": "ai_video.build.build_avu_outro_card",
    "apply-cross-clip-music": "ai_video.build.apply_cross_clip_music",
    "apply-effects-between-clips": "ai_video.build.apply_effects_between_clips",
    "apply-voice-preset": "ai_video.build.apply_voice_preset",
    "concat-clips-with-audio": "ai_video.build.concat_clips_with_audio",
    "orchestrator-cp-by-cp": "ai_video.build.orchestrator_cp_by_cp",
    "render-lock": "ai_video.build.render_lock",
    # research (referent measurement)
    "build-canonical-scenes": "ai_video.research.build_canonical_scenes",
    "extract-canonical-max-detail": "ai_video.research.extract_canonical_max_detail",
    "measure-canonical-decision-ui-pacing": "ai_video.research.measure_canonical_decision_ui_pacing",
    # spec
    "validate-spec": "ai_video.spec.validate",
    "migrate-spec-enums": "ai_video.spec.migrate_enums",
    # editor
    "make-ass": "ai_video.editor.make_ass",
    # audits / gates
    "audit-against-referent": "ai_video.audits.audit_against_referent",
    "audit-anchor-coverage": "ai_video.audits.audit_anchor_coverage",
    "audit-audio": "ai_video.audits.audit_audio",
    "audit-avu-sync-contract": "ai_video.audits.audit_avu_sync_contract",
    "audit-caption-temporal-coverage": "ai_video.audits.audit_caption_temporal_coverage",
    "audit-clip-timing-vs-audio": "ai_video.audits.audit_clip_timing_vs_audio",
    "audit-decision-ui-pacing": "ai_video.audits.audit_decision_ui_pacing",
    "audit-engineer-brief-vs-spec": "ai_video.audits.audit_engineer_brief_vs_spec",
    "audit-first30s-animation": "ai_video.audits.audit_first30s_animation",
    "audit-frames": "ai_video.audits.audit_frames",
    "audit-frames-granular": "ai_video.audits.audit_frames_granular",
    "audit-gemini-calibrated": "ai_video.audits.audit_gemini_calibrated",
    "audit-language-style": "ai_video.audits.audit_language_style",
    "audit-mix-volumes": "ai_video.audits.audit_mix_volumes",
    "audit-narrative": "ai_video.audits.audit_narrative",
    "audit-render-audio-coverage": "ai_video.audits.audit_render_audio_coverage",
    "audit-sfx-audibility": "ai_video.audits.audit_sfx_audibility",
    "audit-sfx-layer": "ai_video.audits.audit_sfx_layer",
    "audit-shot-spec-compliance": "ai_video.audits.audit_shot_spec_compliance",
    "audit-spec-completeness": "ai_video.audits.audit_spec_completeness",
    "audit-spec-declarations": "ai_video.audits.audit_spec_declarations",
    "audit-spec-genre-fidelity": "ai_video.audits.audit_spec_genre_fidelity",
    "audit-spec-lip-sync-marks": "ai_video.audits.audit_spec_lip_sync_marks",
    "audit-spec-narration-fits-duration": "ai_video.audits.audit_spec_narration_fits_duration",
    "audit-spec-narrative-coherence": "ai_video.audits.audit_spec_narrative_coherence",
    "audit-spec-structure-vs-canonical": "ai_video.audits.audit_spec_structure_vs_canonical",
    "audit-spec-voice-exclusivity": "ai_video.audits.audit_spec_voice_exclusivity",
    "audit-style-markup": "ai_video.audits.audit_style_markup",
    "audit-tts-vs-spec-duration": "ai_video.audits.audit_tts_vs_spec_duration",
    "audit-ui-safe-zones": "ai_video.audits.audit_ui_safe_zones",
    "audit-variant-coverage": "ai_video.audits.audit_variant_coverage",
    "audit-videolog-appended": "ai_video.audits.audit_videolog_appended",
    "continuity-check": "ai_video.audits.continuity_check",
    "qa-gate": "ai_video.audits.qa_gate",
    "quality-gate-per-clip": "ai_video.audits.quality_gate_per_clip",
    "sync-check": "ai_video.audits.sync_check",
}

_BUILTINS = ("list", "doctor", "budget")


def module_file(module: str) -> Path | None:
    spec = importlib.util.find_spec(module)
    return Path(spec.origin) if spec and spec.origin else None


def summary(module: str) -> str:
    """First docstring line of a tool module, read via AST (no import side effects)."""
    path = module_file(module)
    if path is None:
        return ""
    try:
        doc = ast.get_docstring(ast.parse(path.read_text(encoding="utf-8"))) or ""
    except (OSError, SyntaxError):
        return ""
    for line in doc.splitlines():
        line = line.strip()
        if line:
            return line[:100]
    return ""


def run_tool(name: str, argv: Sequence[str]) -> int:
    module_name = TOOLS[name]
    try:
        module = importlib.import_module(module_name)
    except ModuleNotFoundError as exc:
        missing = exc.name or "a dependency"
        print(
            f"error: tool '{name}' needs the optional package '{missing}'. "
            f"Install extras with: uv sync --all-extras",
            file=sys.stderr,
        )
        return 2
    main = getattr(module, "main", None)
    if main is None:
        print(f"error: tool '{name}' has no main() entry point", file=sys.stderr)
        return 2
    old_argv = sys.argv
    sys.argv = [f"ai-video {name}", *argv]
    try:
        rc = main()
    except SystemExit as exc:  # argparse --help / errors, tools calling sys.exit
        code = exc.code
        return code if isinstance(code, int) else (0 if code is None else 1)
    except AIVideoError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    finally:
        sys.argv = old_argv
    return rc if isinstance(rc, int) else 0


def _cmd_list() -> int:
    width = max(len(n) for n in TOOLS)
    for name in sorted(TOOLS):
        print(f"  {name:<{width}}  {summary(TOOLS[name])}")
    return 0


def _cmd_budget() -> int:
    from ai_video.budget import default_guard

    g = default_guard()
    print(f"ledger:    {g.ledger}")
    print(f"spent:     ${g.spent():.2f}")
    print(f"limit:     ${g.limit_usd:.2f}")
    print(f"remaining: ${g.remaining():.2f}")
    return 0


def _cmd_doctor() -> int:
    from ai_video.config import get_settings
    from ai_video.proc import which

    ok = True
    print("binaries:")
    for b in ("ffmpeg", "ffprobe", "npx"):
        found = which(b)
        print(f"  {'ok ' if found else 'MISSING'} {b}")
        ok &= found is not None or b == "npx"
    print("optional python packages:")
    for pkg in ("yaml", "elevenlabs", "google.genai", "replicate", "whisper", "PIL", "cv2"):
        try:
            present = importlib.util.find_spec(pkg) is not None
        except ModuleNotFoundError:
            present = False
        print(f"  {'ok ' if present else '-- '} {pkg}")
    s = get_settings()
    print("credentials (values never printed):")
    for env, attr in (
        ("GEMINI_API_KEY", s.gemini_api_key),
        ("ELEVENLABS_API_KEY", s.elevenlabs_api_key),
        ("REPLICATE_API_TOKEN", s.replicate_api_token),
    ):
        print(f"  {'set' if attr else '---'} {env}")
    print(f"budget: ${s.budget_usd:.2f} (ledger {s.spend_ledger})")
    return 0 if ok else 1


def main(argv: Sequence[str] | None = None) -> int:
    from ai_video.log import configure_logging

    args = list(sys.argv[1:] if argv is None else argv)
    if not args or args[0] in ("-h", "--help", "help"):
        print(__doc__)
        return 0
    if args[0] in ("-V", "--version"):
        from ai_video import __version__

        print(__version__)
        return 0
    configure_logging()
    cmd, rest = args[0], args[1:]
    try:
        if cmd == "list":
            return _cmd_list()
        if cmd == "doctor":
            return _cmd_doctor()
        if cmd == "budget":
            return _cmd_budget()
        if cmd in TOOLS:
            return run_tool(cmd, rest)
    except AIVideoError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    print(f"error: unknown command '{cmd}'. Run 'ai-video list'.", file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())
