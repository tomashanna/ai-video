"""ai_video — toolkit for producing short AI-generated vertical videos.

The package groups:

* ``ai_video.providers`` — thin, hardened clients for paid generative APIs
  (ElevenLabs TTS/SFX, Gemini image/vision/Veo, Replicate/Kling) plus local Whisper.
* ``ai_video.build`` — per-clip atomic assembly, concat, transitions, music, orchestration.
* ``ai_video.audits`` — deterministic quality gates over specs and renders.
* ``ai_video.spec`` — creative-spec schema and validation.
* ``ai_video.core`` — pure helpers (empirical bands, similarity, state machine).

Every tool is exposed through the ``ai-video`` CLI (see ``ai_video.cli``).
"""

__version__ = "0.2.0"
