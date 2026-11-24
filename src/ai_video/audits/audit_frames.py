#!/usr/bin/env python3
"""
audit-frames.py — Frame-by-frame visual QA con Gemini Vision.

Detecta issues NO detectados por Gemini Video Analyzer holístico:
- Frames negros / vacíos
- UI overlaps (countdown tapa imagen)
- Texto cortado, mal posicionado, fuera de safe zone IG
- Character drift visible entre frames consecutivos
- Composición rota
- Captions overlap entre sí

Razón: Gemini QA holístico da score 9.5 a un video con countdown tapando
imagen (caso isla-faro v1) porque el frame específico es minoría. Este
script audita FRAME por FRAME para detectar issues localizados.

Usage:
  python audit-frames.py --video renders/v1.mp4 --interval 0.5
    → Extrae frames cada 0.5s, audita cada uno con Gemini Vision
    → Reporta issues con timestamp + tipo
    → Exit 1 si encuentra >max-issues frames problemáticos

Integration con el flow del agente productor:
  Después del render draft, ANTES de declarar stop point pre-Kling:
    subprocess.run([
        "python", "scripts/audit-frames.py",
        "--video", "renders/draft.mp4",
        "--interval", "0.5",
        "--max-issues", "2"
    ], check=True)
"""

import argparse
import json
import os
import subprocess
import sys
import tempfile

try:
    import google.genai as genai  # noqa: F401  (availability check)
except ImportError:
    print("ERROR: missing deps. Run: uv sync --extra providers")
    sys.exit(2)

from ai_video.errors import ConfigError
from ai_video.providers.clients import gemini_client

# Upper bound for any child process (ffmpeg/ffprobe/whisper); prevents hung gates.
SUBPROCESS_TIMEOUT_S = 1800


AUDIT_PROMPT = """Examina este frame de un video horror-choice (1080×1920, vertical Reel para Instagram).

Buscá issues VISUALES específicos. Reportá SOLO si encontrás:

1. Frame negro o casi negro (>80% pixels black) sin razón narrativa clara
2. UI overlap: countdown/loader/labels tapando imagen principal
3. Texto cortado, mal posicionado, fuera de safe zone IG (captions bottom <540px, top >1700px)
4. Character drift visible (mismo personaje con cara distinta vs frames adyacentes)
5. Composición rota (objetos cortados feo, encuadre desbalanceado, sujeto principal off-frame)
6. Captions overlap entre sí (dos captions en el mismo frame que no deberían coexistir)
7. Asset cortado prematuramente (imagen desaparece antes de que termine el caption sincronizado)

Formato de respuesta:
- Si NO hay issues: responde exactamente "OK"
- Si hay issues: lista cada uno en 1 línea, formato:
    ISSUE: <tipo>: <detalle específico>
  Ejemplo: ISSUE: ui-overlap: countdown digit cubre rostro del personaje en centro de frame
"""


def extract_frames(video_path: str, interval: float, output_dir: str) -> list:
    """Extract frames every N seconds. Returns list of (timestamp, path)."""
    os.makedirs(output_dir, exist_ok=True)

    # Get duration via ffprobe
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "csv=p=0", video_path],
        capture_output=True, text=True, check=True
    , timeout=SUBPROCESS_TIMEOUT_S)
    duration = float(result.stdout.strip())

    frames = []
    t = 0.0
    # Stop with margin to avoid ffmpeg failing silently on end-of-stream
    while t < duration - 0.1:
        out = os.path.join(output_dir, f"frame_{t:06.2f}.png")
        subprocess.run(
            ["ffmpeg", "-y", "-ss", str(t), "-i", video_path,
             "-frames:v", "1", "-q:v", "2", out],
            capture_output=True, check=False
        , timeout=SUBPROCESS_TIMEOUT_S)
        if os.path.exists(out) and os.path.getsize(out) > 1000:
            frames.append((t, out))
        t += interval

    return frames


def audit_frame(frame_path: str, client) -> list:
    """Send frame to Gemini Vision. Return list of issues found."""
    with open(frame_path, "rb") as f:
        image_bytes = f.read()

    response = client.models.generate_content(
        model="gemini-3.1-flash-lite",
        contents=[{
            "role": "user",
            "parts": [
                {"text": AUDIT_PROMPT},
                {"inline_data": {"mime_type": "image/png", "data": image_bytes}}
            ]
        }]
    )

    text = response.text.strip()
    if text == "OK" or text.upper().startswith("OK"):
        return []

    issues = []
    for line in text.split("\n"):
        line = line.strip()
        if line.startswith("ISSUE:"):
            issues.append(line[6:].strip())  # strip "ISSUE: " prefix

    return issues


def main():
    parser = argparse.ArgumentParser(
        description="Frame-by-frame visual QA con Gemini Vision."
    )
    parser.add_argument("--video", required=True, help="Path to mp4")
    parser.add_argument(
        "--interval", type=float, default=0.5,
        help="Seconds between frame extractions (default 0.5)"
    )
    parser.add_argument(
        "--max-issues", type=int, default=2,
        help="Fail if more than N frames have issues (default 2)"
    )
    parser.add_argument(
        "--output", type=str, default=None,
        help="Optional path to save JSON report"
    )

    args = parser.parse_args()

    if not os.path.exists(args.video):
        print(f"ERROR: video not found: {args.video}")
        return 2

    try:
        client = gemini_client()
    except ConfigError as exc:
        print(f"ERROR: {exc}")
        return 2

    print(f"📹 Auditing {args.video}")
    print(f"   Interval: {args.interval}s | Max issues threshold: {args.max_issues}")
    print()

    with tempfile.TemporaryDirectory() as tmpdir:
        frames = extract_frames(args.video, args.interval, tmpdir)
        print(f"   Extracted {len(frames)} frames")
        print()

        all_issues = {}
        errors = []
        for t, path in frames:
            try:
                issues = audit_frame(path, client)
                if issues:
                    all_issues[t] = issues
                    for issue in issues:
                        print(f"   ⚠️ t={t:6.2f}s: {issue}")
            except Exception as e:
                errors.append((t, str(e)))
                print(f"   ❗ t={t:6.2f}s: AUDIT_ERROR — {e}")
                continue

    print()
    print("=" * 60)
    print(f"Total frames audited: {len(frames)}")
    print(f"Frames with issues:   {len(all_issues)}")
    print(f"Total issues:         {sum(len(v) for v in all_issues.values())}")

    if args.output:
        report = {
            "video": args.video,
            "frames_audited": len(frames),
            "frames_with_issues": len(all_issues),
            "issues_by_timestamp": {str(t): issues for t, issues in all_issues.items()}
        }
        with open(args.output, "w") as f:
            json.dump(report, f, indent=2)
        print(f"Report saved: {args.output}")

    print()
    if len(all_issues) > args.max_issues:
        print(f"❌ FRAME AUDIT FAILED — {len(all_issues)} frames with issues (max {args.max_issues})")
        print("   Fixear issues antes de stop point pre-Kling.")
        return 1

    print(f"✅ FRAME AUDIT PASSED — {len(all_issues)} frames ≤ max {args.max_issues}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
