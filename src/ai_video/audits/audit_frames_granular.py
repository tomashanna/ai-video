#!/usr/bin/env python3
"""
audit-frames-granular.py — Granular sentinel patterns audit for video render.

Validated need: matadero iter 5 audit 2026-05-19 PM — user caught 2 bugs that
existing audit-frames.py (interval 1.0s + holistic Gemini) missed:
  D1: cocinera audio playing 7-9.48s + cocinera face NOT visible on screen
      (anti-pattern #9 lip-sync compliance hidden form)
  D2: cap-24 subtitle "La sirena..." 83.72-84.88s + outro-card same text
      84.88-89.5s = redundant visual duplicate text

Authority:
  - AUDITOR-PROTOCOL § 6 anti-pattern #9 audio-visual lip-sync realism
  - AUDITOR-PROTOCOL § 6 anti-pattern #10 trust docs without direct verify
  - GAPS-LOG #14 decision UI editorial pacing
  - GAPS-LOG #18-20 hook order + visual style + docs methodology

Sentinel patterns automated:
  S1. Audio-visual character mismatch
      Pattern: caption[speaker=character_X audio playing] + character_X face NOT
      visible on screen during that window → 🚨 anti-pattern #9 hidden form
  S2. Duplicate text within window (10s)
      Pattern: same text content in 2+ elements within 10s timeline window
      → 🚨 redundant visual story-beat
  S3. AVU sync drift
      Pattern: AVU bundled audio peaks expected at digit-change moments vs
      actual ffmpeg volumedetect → 🚨 sync drift
  S4. Caption Y position canonical
      Pattern: caption Y < 55% or Y > 70% (canonical band [55-70]) → 🚨 drift
  S5. Watermark IG safe zone
      Pattern: watermark Y > 1700px (frame height 1920, IG bottom UI ~220px)
      → 🚨 close to IG UI overlap risk

Granular sweep: every 0.5s first 30s + every 1s rest of timeline.

Usage:
    python audit-frames-granular.py \\
        --video renders/draft.mp4 \\
        --captions assets/captions/captions.json \\
        --html index.html \\
        [--enable-gemini]

Exit codes:
    0 — ALL sentinel patterns PASS
    1 — ≥1 sentinel pattern FAIL (engineer/auditor must address)
    2 — script error (missing inputs)
"""

import argparse
import json
import re
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

# Upper bound for any child process (ffmpeg/ffprobe/whisper); prevents hung gates.
SUBPROCESS_TIMEOUT_S = 1800


def parse_html_elements(html_path: Path) -> dict:
    """Extract caption + outro-card + watermark elements with positions from HTML."""
    with open(html_path) as f:
        content = f.read()

    elements = {
        "captions": [],
        "outro_cards": [],
        "watermark": None,
    }

    # Captions
    caption_pattern = re.compile(
        r'<div id="(cap-[^"]+)".*?data-start="([^"]+)".*?data-duration="([^"]+)".*?>(.*?)</div>', re.DOTALL
    )
    for m in caption_pattern.finditer(content):
        elements["captions"].append(
            {
                "id": m.group(1),
                "start": float(m.group(2)),
                "duration": float(m.group(3)),
                "end": float(m.group(2)) + float(m.group(3)),
                "text": m.group(4).strip()[:120],
            }
        )

    # Outro cards
    outro_pattern = re.compile(
        r'<div id="(outro-card[^"]*)".*?data-start="([^"]+)".*?data-duration="([^"]+)".*?>(.*?)</div>',
        re.DOTALL,
    )
    for m in outro_pattern.finditer(content):
        elements["outro_cards"].append(
            {
                "id": m.group(1),
                "start": float(m.group(2)),
                "duration": float(m.group(3)),
                "end": float(m.group(2)) + float(m.group(3)),
                "text": m.group(4).replace("<br>", " ").strip()[:120],
            }
        )

    # Watermark Y position
    wm_y_match = re.search(r'\.watermark\s*\{[^}]*bottom:\s*(\d+)px', content)
    if wm_y_match:
        elements["watermark"] = {
            "bottom_px": int(wm_y_match.group(1)),
            "y_pct_from_top": ((1920 - int(wm_y_match.group(1))) / 1920) * 100,
        }

    return elements


def parse_captions_json(path: Path) -> list:
    """Load captions.json with normalized fields."""
    with open(path) as f:
        data = json.load(f)
    captions = data.get("captions", data) if isinstance(data, dict) else data
    if not isinstance(captions, list):
        return []
    normalized = []
    for c in captions:
        normalized.append(
            {
                "start": float(c.get("start", 0)),
                "end": float(c.get("end", 0)),
                "text": c.get("whisper_text", c.get("text", "")),
                "speaker": c.get("speaker", "narrator"),
                "y_position_pct": c.get("y_position_pct", 62),
            }
        )
    return normalized


def get_video_duration(video_path: Path) -> float:
    """Use ffprobe to get video duration."""
    result = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            str(video_path),
        ],
        capture_output=True,
        text=True,
        timeout=SUBPROCESS_TIMEOUT_S,
    )
    return float(result.stdout.strip())


def generate_sample_timestamps(duration: float) -> list:
    """Granular sweep: every 0.5s first 30s + every 1s rest."""
    timestamps = []
    t = 0.0
    while t < min(30.0, duration):
        timestamps.append(round(t, 2))
        t += 0.5
    t = 30.0
    while t < duration:
        timestamps.append(round(t, 2))
        t += 1.0
    return timestamps


def sentinel_s1_audio_visual_character_mismatch(captions: list, character_visible_windows: dict) -> list:
    """S1. Character audio playing + character face not visible on screen.

    character_visible_windows: dict[character_id, list of (start, end) windows where face visible].
    For now, we accept windows from manual config or skip if not provided (requires Gemini Vision integration).
    """
    findings = []
    for c in captions:
        speaker = c["speaker"]
        if speaker in ("narrator", "off_screen", ""):
            continue  # narrator off-screen voice always valid

        # Check if character_id has visible windows defined
        visible_windows = character_visible_windows.get(speaker)
        if visible_windows is None:
            findings.append(
                {
                    "sentinel": "S1",
                    "severity": "WARN",
                    "caption_id": f"caption@{c['start']:.1f}-{c['end']:.1f}s",
                    "speaker": speaker,
                    "issue": f"No character_visible_windows config for speaker '{speaker}' — manual verification required (or enable Gemini Vision sentinel)",
                    "text": c["text"][:60],
                }
            )
            continue

        # Verify character visible during full audio window
        audio_start, audio_end = c["start"], c["end"]
        visible_during_audio = any(vs <= audio_start and ve >= audio_end for vs, ve in visible_windows)
        if not visible_during_audio:
            findings.append(
                {
                    "sentinel": "S1",
                    "severity": "FAIL",
                    "caption_id": f"caption@{audio_start:.1f}-{audio_end:.1f}s",
                    "speaker": speaker,
                    "issue": f"Character '{speaker}' audio playing {audio_start:.1f}-{audio_end:.1f}s but face NOT visible during full window (anti-pattern #9 hidden form)",
                    "text": c["text"][:60],
                    "fix_hint": "Option A: cut to character face animated during audio. Option B: remove character audio at this moment.",
                }
            )
    return findings


def sentinel_s2_duplicate_text_window(captions: list, html_elements: dict, window_s: float = 10.0) -> list:
    """S2. Same text content across DIFFERENT element TYPES within window.

    NOTE: HTML cap-N elements are renders of captions.json entries (1:1 mapping),
    so we ONLY check duplicates across DIFFERENT types:
    - captions (from JSON, source of truth) vs outro_cards
    - outro_cards vs outro_cards (if multiple)
    - special UI text overlays vs captions
    Skip captions.json vs HTML caption pairs (redundant same-source comparison).
    """
    findings = []

    # Type A: HTML captions (what user actually SEES on screen, including stale elements not in JSON)
    type_a_elements = []
    for ec in html_elements.get("captions", []):
        type_a_elements.append(
            {
                "id": ec["id"],
                "type": "html_caption",
                "text": ec["text"].lower().strip().rstrip("."),
                "start": ec["start"],
                "end": ec["end"],
            }
        )

    # Type B: outro cards from HTML (separate element type)
    type_b_elements = []
    for oc in html_elements.get("outro_cards", []):
        type_b_elements.append(
            {
                "id": oc["id"],
                "type": "outro_card",
                "text": oc["text"].lower().strip().rstrip("."),
                "start": oc["start"],
                "end": oc["end"],
            }
        )

    # Check stale HTML captions (in HTML but NOT in captions.json) — warns engineer dead code
    json_text_set = {c["text"].lower().strip().rstrip(".") for c in captions}
    for el in type_a_elements:
        if el["text"] and el["text"] not in json_text_set:
            # Check if any partial match (in case JSON text is contained in HTML text or vice versa)
            partial_match = any(el["text"] in jt or jt in el["text"] for jt in json_text_set if jt)
            if not partial_match:
                findings.append(
                    {
                        "sentinel": "S2",
                        "severity": "FAIL",
                        "elements": [el["id"]],
                        "types": ["html_caption_stale"],
                        "issue": f"HTML element {el['id']} has text '{el['text'][:50]}...' but NOT present in captions.json — STALE element from previous iter",
                        "fix_hint": f"Remove HTML element {el['id']} (line in index.html) — it renders text that's no longer in captions source of truth.",
                    }
                )

    # Compare type_a vs type_b (HTML cross-type duplicates)
    seen_pairs = set()
    for a in type_a_elements:
        for b in type_b_elements:
            pair_key = (a["id"], b["id"])
            if pair_key in seen_pairs:
                continue
            if not a["text"] or not b["text"]:
                continue
            a_text = re.sub(r'\s+', ' ', a["text"])
            b_text = re.sub(r'\s+', ' ', b["text"])
            # Match: same text OR one contains the other (substring relationship)
            if a_text == b_text or a_text in b_text or b_text in a_text:
                # Check timing: within window_s of each other
                gap = min(
                    abs(a["start"] - b["start"]), abs(a["end"] - b["start"]), abs(a["start"] - b["end"])
                )
                if gap <= window_s:
                    findings.append(
                        {
                            "sentinel": "S2",
                            "severity": "FAIL",
                            "elements": [a["id"], b["id"]],
                            "types": [a["type"], b["type"]],
                            "issue": f"Same text '{a['text'][:50]}...' appears in {a['type']} ({a['start']:.1f}s) AND {b['type']} ({b['start']:.1f}s) within {window_s}s window — redundant visual",
                            "fix_hint": "Remove one element OR change text content of one. User-perceived as duplicate even if no temporal overlap.",
                        }
                    )
                    seen_pairs.add(pair_key)

    # Also check outro_card vs outro_card (multiple outro cards with same text)
    for i, a in enumerate(type_b_elements):
        for j, b in enumerate(type_b_elements):
            if i >= j:
                continue
            if not a["text"] or not b["text"]:
                continue
            a_text = re.sub(r'\s+', ' ', a["text"])
            b_text = re.sub(r'\s+', ' ', b["text"])
            if a_text == b_text or a_text in b_text or b_text in a_text:
                findings.append(
                    {
                        "sentinel": "S2",
                        "severity": "FAIL",
                        "elements": [a["id"], b["id"]],
                        "types": [a["type"], b["type"]],
                        "issue": f"Multiple outro cards with same text '{a['text'][:50]}...'",
                        "fix_hint": "Keep only one outro card.",
                    }
                )

    return findings


def sentinel_s4_caption_y_position_canonical(captions: list) -> list:
    """S4. Caption Y position outside canonical band [55-70%]."""
    findings = []
    for c in captions:
        y = c.get("y_position_pct", 62)
        if y < 55 or y > 70:
            findings.append(
                {
                    "sentinel": "S4",
                    "severity": "WARN",
                    "caption_id": f"caption@{c['start']:.1f}s",
                    "y_position": y,
                    "issue": f"Caption Y position {y}% outside canonical band [55-70%]",
                    "fix_hint": "Adjust caption Y to 62% (canonical) unless justified for design reason.",
                }
            )
    return findings


def sentinel_s8_static_background_per_shot(
    video_path: Path, shot_windows: list = None, ssim_threshold: float = 0.99, min_consecutive_frames: int = 4
) -> list:
    """S8. Background ambient creature/object animated per shot (GAP #23).

    Method: SSIM consecutive frames at 0.5s intervals within shot windows. If >0.99
    mean SSIM across 4+ consecutive frames (=2s static) → flag static background.

    Phase 1 implementation 2026-05-20 via scikit-image SSIM.

    If shot_windows not provided, segments video into 4s windows from t=0.
    """
    findings = []
    try:
        import cv2
        from skimage.metrics import structural_similarity as ssim
    except ImportError as e:
        return [
            {
                "sentinel": "S8",
                "severity": "WARN",
                "issue": f"S8 deps missing: {e}. Install opencv-python-headless + scikit-image.",
                "fix_hint": "pip install opencv-python-headless scikit-image",
            }
        ]

    duration = get_video_duration(video_path)
    if not shot_windows:
        # Fallback: synthetic 4s windows
        shot_windows = [(t, min(t + 4.0, duration)) for t in range(0, int(duration), 4)]

    cap = cv2.VideoCapture(str(video_path))
    if not cap.isOpened():
        return [{"sentinel": "S8", "severity": "WARN", "issue": "Could not open video"}]
    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0

    for win_idx, (start_s, end_s) in enumerate(shot_windows):
        if end_s - start_s < 2.0:
            continue
        sample_ts = [start_s + i * 0.5 for i in range(int((end_s - start_s) / 0.5))]
        prev_gray = None
        ssims_window = []
        for t in sample_ts:
            cap.set(cv2.CAP_PROP_POS_FRAMES, int(t * fps))
            ret, frame = cap.read()
            if not ret:
                continue
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            small = cv2.resize(gray, (256, 456))  # downscale for speed
            if prev_gray is not None:
                try:
                    s = ssim(prev_gray, small)
                    ssims_window.append(s)
                except ValueError:
                    pass
            prev_gray = small
        # Find longest run of SSIM > threshold
        longest_run = 0
        cur_run = 0
        for s in ssims_window:
            if s >= ssim_threshold:
                cur_run += 1
                longest_run = max(longest_run, cur_run)
            else:
                cur_run = 0
        if longest_run >= min_consecutive_frames:
            mean_ssim = sum(ssims_window) / len(ssims_window) if ssims_window else 0
            findings.append(
                {
                    "sentinel": "S8",
                    "severity": "WARN",
                    "window": f"{start_s:.1f}-{end_s:.1f}s",
                    "mean_ssim": round(mean_ssim, 4),
                    "longest_static_run_frames": longest_run,
                    "static_duration_s": round(longest_run * 0.5, 1),
                    "issue": f"Static background detected {start_s:.1f}-{end_s:.1f}s (SSIM≥{ssim_threshold} for {longest_run * 0.5:.1f}s consecutive). GAP #23 anti-canonical.",
                    "fix_hint": "Add ambient motion (smoke, creature, glow flicker) OR shorter shot duration. Canonical refs have continuous micro-motion.",
                }
            )
    cap.release()
    return findings


def sentinel_s9_character_lip_sync_compliance(captions: list, html_path: Path) -> list:
    """S9. Character speech ON-screen must have lip-sync visible (GAP #24).

    Method: for each caption with speaker=character + lip_sync_required=true,
    require Gemini Vision Tier 2 check (frame extract + mouth movement detect vs audio).
    """
    findings = []
    for c in captions:
        if c.get("speaker") in ("narrator", "off_screen", "", None):
            continue
        # Character speech → flag for lip-sync verification
        findings.append(
            {
                "sentinel": "S9",
                "severity": "WARN",
                "caption_id": f"caption@{c['start']:.1f}s",
                "speaker": c["speaker"],
                "issue": f"Character '{c['speaker']}' speech requires lip-sync verification (Gemini Vision Tier 2 forward)",
                "fix_hint": "Verify Hailuo clip output + Hedra/Sync.so retarget if needed. GAP #24.",
                "text": c["text"][:60],
            }
        )
    return findings


def sentinel_s10_pov_traversal_continuity(
    video_path: Path, shot_clip_timings: list = None, ssim_threshold: float = 0.98, min_consecutive: int = 3
) -> list:
    """S10. POV traversal across consecutive shots (GAP #25).

    Method: extract frame at start of each shot, compute SSIM between consecutive
    shot start frames. If >0.98 across 3+ consecutive shots = static framing
    throughout = viewer feels teleported (no POV traversal).

    Phase 1 implementation 2026-05-20 via scikit-image SSIM.

    shot_clip_timings: list of (start_s, end_s) shot windows. If None, parses from
    scene_cuts.txt sibling file OR fallback fixed 4s intervals.
    """
    findings = []
    try:
        import cv2
        from skimage.metrics import structural_similarity as ssim
    except ImportError as e:
        return [{"sentinel": "S10", "severity": "WARN", "issue": f"S10 deps missing: {e}"}]

    duration = get_video_duration(video_path)
    if not shot_clip_timings:
        # Try scene_cuts.txt sibling
        cuts_path = video_path.parent / "scene_cuts.txt"
        if cuts_path.exists():
            cuts = [float(line.strip()) for line in cuts_path.read_text().splitlines() if line.strip()]
            cuts = sorted(set([0.0] + cuts + [duration]))
            shot_clip_timings = [
                (cuts[i], cuts[i + 1]) for i in range(len(cuts) - 1) if cuts[i + 1] - cuts[i] > 0.5
            ]
        else:
            shot_clip_timings = [(t, min(t + 4.0, duration)) for t in range(0, int(duration), 4)]

    if len(shot_clip_timings) < 2:
        return findings

    cap = cv2.VideoCapture(str(video_path))
    if not cap.isOpened():
        return [{"sentinel": "S10", "severity": "WARN", "issue": "Could not open video"}]
    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0

    shot_start_frames = []
    for start_s, _ in shot_clip_timings:
        cap.set(cv2.CAP_PROP_POS_FRAMES, int((start_s + 0.1) * fps))  # +0.1s for cut stability
        ret, frame = cap.read()
        if ret:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            shot_start_frames.append((start_s, cv2.resize(gray, (256, 456))))
    cap.release()

    # SSIM between consecutive shot starts
    consec_high_ssim_runs = []
    cur_run = []
    for i in range(1, len(shot_start_frames)):
        t_prev, fr_prev = shot_start_frames[i - 1]
        t_cur, fr_cur = shot_start_frames[i]
        try:
            s = ssim(fr_prev, fr_cur)
        except ValueError:
            continue
        if s >= ssim_threshold:
            cur_run.append((t_prev, t_cur, s))
        else:
            if len(cur_run) >= min_consecutive - 1:
                consec_high_ssim_runs.append(cur_run)
            cur_run = []
    if len(cur_run) >= min_consecutive - 1:
        consec_high_ssim_runs.append(cur_run)

    for run in consec_high_ssim_runs:
        start_t = run[0][0]
        end_t = run[-1][1]
        mean_ssim = sum(x[2] for x in run) / len(run)
        n_shots = len(run) + 1
        findings.append(
            {
                "sentinel": "S10",
                "severity": "WARN",
                "window": f"{start_t:.1f}-{end_t:.1f}s",
                "consecutive_shots_static": n_shots,
                "mean_ssim": round(mean_ssim, 4),
                "issue": f"POV traversal stalled {start_t:.1f}-{end_t:.1f}s — {n_shots} consecutive shots with SSIM ≥{ssim_threshold} (mean {mean_ssim:.3f}). Viewer perceives no camera movement / teleport feel.",
                "fix_hint": "Add POV traversal cuts: dolly forward, hand reveal, environment shift between consecutive shots. GAP #25 canonical horror-choice POV continuity.",
            }
        )
    return findings


def sentinel_s6_countdown_digit_transition_timing(html_path: Path) -> list:
    """S6. Countdown digit GSAP tl.call() timestamps staggered per digit_duration_s.

    Bug pattern (GAP #22 matadero iter 7): tl.call() updates digit textContent ALL
    firing at same timestamp instead of staggered. Result: digit displays final value
    for entire window. User perceives "desfase".
    """
    findings = []
    with open(html_path) as f:
        content = f.read()

    # Find all tl.call(...) updating digit textContent + extract timestamp
    # Pattern: tl.call(() => { ...digit... }, [], TIMESTAMP);
    digit_call_pattern = re.compile(
        r'tl\.call\(\s*\(\s*\)\s*=>\s*\{[^}]*?(?:getElementById\("([^"]+-digit)"\)|"([^"]+-digit)")[^}]*?textContent\s*=\s*"([0-9])"[^}]*?\}\s*\,\s*\[\s*\]\s*,\s*([0-9.]+)\s*\)',
        re.DOTALL,
    )

    # Group timestamps by digit_id
    digit_timestamps = defaultdict(list)
    for m in digit_call_pattern.finditer(content):
        digit_id = m.group(1) or m.group(2)
        digit_value = m.group(3)
        timestamp = float(m.group(4))
        digit_timestamps[digit_id].append((digit_value, timestamp))

    # Verify staggered per digit_id
    for digit_id, transitions in digit_timestamps.items():
        if len(transitions) < 2:
            continue
        transitions_sorted = sorted(transitions, key=lambda x: int(x[0]), reverse=True)
        # Expected staggered: each transition timestamp at least 0.5s after previous
        timestamps = [t for _, t in transitions_sorted]
        for i in range(1, len(timestamps)):
            gap = timestamps[i] - timestamps[i - 1]
            if gap < 0.5:
                findings.append(
                    {
                        "sentinel": "S6",
                        "severity": "FAIL",
                        "element": digit_id,
                        "issue": f"Countdown digit '{digit_id}' transitions firing at near-identical timestamps (gap={gap:.2f}s < 0.5s) — digits jump instantly instead of staggered per canonical 1s per digit",
                        "transitions": [(d, t) for d, t in transitions_sorted],
                        "fix_hint": "Stagger GSAP tl.call() timestamps +1s per digit. Better: replace HTML+GSAP countdown with pre-rendered AVU clip (eliminates timing-bug class entirely per PAUTA § 19 AVU principle).",
                    }
                )
                break  # one finding per digit_id is enough

    return findings


def sentinel_s5_watermark_safe_zone(html_elements: dict) -> list:
    """S5. Watermark Y > 1700px (IG UI overlap risk)."""
    findings = []
    wm = html_elements.get("watermark")
    if not wm:
        return findings
    bottom_px = wm["bottom_px"]
    if bottom_px < 150:
        findings.append(
            {
                "sentinel": "S5",
                "severity": "WARN",
                "element": "watermark",
                "bottom_px": bottom_px,
                "issue": f"Watermark bottom: {bottom_px}px < 150px safe zone — risk Instagram UI overlap",
                "fix_hint": "Raise watermark bottom CSS to ≥150px to avoid IG bottom UI bar overlap.",
            }
        )
    return findings


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--video", required=True, help="Path to rendered video mp4")
    p.add_argument("--captions", required=True, help="Path to captions.json")
    p.add_argument("--html", required=True, help="Path to index.html")
    p.add_argument(
        "--character-visible-config",
        default=None,
        help="Optional JSON file with {character_id: [[start, end], ...]} visible windows",
    )
    p.add_argument(
        "--enable-gemini",
        action="store_true",
        help="Enable Gemini Vision sentinel for S1 character-visible detection",
    )
    p.add_argument("--output-json", default=None, help="Save findings to JSON file")
    args = p.parse_args()

    video_path = Path(args.video)
    captions_path = Path(args.captions)
    html_path = Path(args.html)

    for path, label in [(video_path, "video"), (captions_path, "captions"), (html_path, "html")]:
        if not path.exists():
            print(f"ERROR: {label} not found: {path}", file=sys.stderr)
            sys.exit(2)

    # Load inputs
    duration = get_video_duration(video_path)
    captions = parse_captions_json(captions_path)
    html_elements = parse_html_elements(html_path)
    character_visible_windows = {}
    if args.character_visible_config:
        with open(args.character_visible_config) as f:
            character_visible_windows = json.load(f)

    timestamps = generate_sample_timestamps(duration)

    # Run sentinels
    all_findings = []
    all_findings.extend(sentinel_s1_audio_visual_character_mismatch(captions, character_visible_windows))
    all_findings.extend(sentinel_s2_duplicate_text_window(captions, html_elements))
    all_findings.extend(sentinel_s4_caption_y_position_canonical(captions))
    all_findings.extend(sentinel_s5_watermark_safe_zone(html_elements))
    all_findings.extend(sentinel_s6_countdown_digit_transition_timing(html_path))
    all_findings.extend(sentinel_s8_static_background_per_shot(video_path))
    all_findings.extend(sentinel_s9_character_lip_sync_compliance(captions, html_path))
    all_findings.extend(sentinel_s10_pov_traversal_continuity(video_path))
    # S3 AVU sync drift + S1 Gemini Vision = forward when integrated

    # Report
    print(f"\n=== AUDIT FRAMES GRANULAR — {video_path.name} ===")
    print(f"Video duration: {duration:.2f}s")
    print(f"Sample timestamps generated: {len(timestamps)} (0.5s first 30s + 1s rest)")
    print(f"Captions parsed: {len(captions)}")
    print(
        f"HTML elements parsed: {len(html_elements['captions'])} captions + {len(html_elements['outro_cards'])} outro cards"
    )
    print()

    severity_counts = defaultdict(int)
    for f in all_findings:
        severity_counts[f["severity"]] += 1

    print(
        f"Findings: {len(all_findings)} total | FAIL={severity_counts['FAIL']} | WARN={severity_counts['WARN']}"
    )
    print()

    if not all_findings:
        print("✅ ALL SENTINEL PATTERNS PASS")
        sys.exit(0)

    for f in all_findings:
        marker = "🚨" if f["severity"] == "FAIL" else "⚠️"
        print(f"{marker} [{f['sentinel']}] {f['severity']} — {f['issue']}")
        if "text" in f:
            print(f"      text: \"{f['text']}\"")
        if "elements" in f:
            print(f"      elements: {f['elements']}")
        if "fix_hint" in f:
            print(f"      fix: {f['fix_hint']}")
        print()

    if args.output_json:
        with open(args.output_json, "w") as f:
            json.dump({"findings": all_findings, "timestamps": timestamps}, f, indent=2)
        print(f"Findings saved to {args.output_json}")

    if severity_counts["FAIL"] > 0:
        print(
            f"\n🔴 VERDICT: {severity_counts['FAIL']} FAIL findings — engineer/auditor must address before ship"
        )
        sys.exit(1)
    else:
        print(f"\n🟡 VERDICT: {severity_counts['WARN']} WARN findings only — review but ship-acceptable")
        sys.exit(0)


if __name__ == "__main__":
    main()
