#!/usr/bin/env python3
"""
audit-narrative.py — Pre-render narrative + structural audit.

Catches issues that `hyperframes lint` does NOT detect:
  1. Images with effective visibility < 1.0s (anti-pattern: flashes that
     distract without aporting narrative)
  2. data-duration mismatched with GSAP opacity timing — image fades out
     visually because data-duration ended even though GSAP still says
     opacity:1
  3. z-index conflicts where black-overlay (or any high-z element) covers
     caption-wrap unintentionally
  4. Asset orphans — files in assets/ not referenced by any HTML tag

Usage:
    python scripts/audit-narrative.py [path/to/index.html]
    # Default: ./index.html

Exits 0 if all checks pass, 1 if any check fails.

Each finding prints: severity (ERROR/WARN), check name, element id, evidence.

Aprendizajes amargos que originaron este script:
  - mina-abandonada v7c: h4-pull flasheaba 0.15s entre fades del black overlay
  - mina-abandonada v7b: h4-hand desaparecía a los 67.5s porque data-duration=2.5
    aunque GSAP lo mantenía opacity:1 hasta 68.65
  - mina-abandonada v7 first: black-overlay z-index 94 tapaba caption-wrap (70)

Documentado en: .claude/skills/video-director/ANTI-PATTERNS.md
"""
import re
import sys
from pathlib import Path
from collections import defaultdict

MIN_VISIBLE_SECONDS = 1.0
CAPTION_WRAP_Z_INDEX = 70  # estándar en todos los proyectos


def parse_html(html_path: Path) -> str:
    return html_path.read_text(encoding="utf-8")


def extract_imgs(content: str):
    """Returns list of dicts: {id, src, data_start, data_duration, data_end, starts_visible}.

    starts_visible: True if no inline `opacity: 0` in the style attribute.
    Elements that start visible don't need an explicit GSAP opacity:1 event.
    """
    out = []
    for m in re.finditer(r'<img\b[^>]*>', content):
        tag = m.group(0)
        get = lambda attr: (re.search(rf'{attr}="([^"]*)"', tag) or [None, None])[1]
        eid = get("id")
        src = get("src")
        ds = get("data-start")
        dd = get("data-duration")
        if not (eid and ds and dd):
            continue
        try:
            ds_f = float(ds)
            dd_f = float(dd)
        except ValueError:
            continue
        style = get("style") or ""
        # If inline style explicitly sets opacity:0, element starts hidden.
        starts_visible = "opacity:0" not in style.replace(" ", "")
        out.append({
            "id": eid,
            "src": src,
            "data_start": ds_f,
            "data_duration": dd_f,
            "data_end": ds_f + dd_f,
            "starts_visible": starts_visible,
        })
    return out


def extract_gsap_opacity_events(content: str):
    """
    Returns dict: {element_id: [(time, opacity_value), ...]} sorted by time.
    Parses both tl.set and tl.to calls for opacity changes.
    """
    events = defaultdict(list)
    # tl.set("#id", { opacity: N, ... }, T) or tl.to(...)
    pat = re.compile(
        r'tl\.(set|to)\(\s*"#([\w\-]+)"\s*,\s*\{[^}]*?opacity:\s*([\d.]+)[^}]*\}\s*,\s*([\d.]+)\s*\)'
    )
    for m in pat.finditer(content):
        _, eid, op, t = m.groups()
        events[eid].append((float(t), float(op)))
    for eid in events:
        events[eid].sort()
    return events


def extract_css_z_index(content: str):
    """Returns dict: {selector_or_id: z_index_value}."""
    out = {}
    # Match rules like  #foo { ... z-index: N ... } or .bar { ... z-index: N }
    rule_pat = re.compile(r'([#.\w-]+)\s*\{([^}]*)\}', re.DOTALL)
    z_pat = re.compile(r'z-index\s*:\s*(\d+)')
    for m in rule_pat.finditer(content):
        sel = m.group(1).strip()
        body = m.group(2)
        zm = z_pat.search(body)
        if zm:
            out[sel] = int(zm.group(1))
    return out


def get_effective_visibility(img, gsap_events):
    """
    Compute effective visibility window for an image.
    Returns (eff_start, eff_end, eff_visible_seconds, reason).

    Logic:
    - If element starts_visible (no inline opacity:0):
        show = data_start (visible from the moment it enters the timeline)
        hide = first GSAP opacity:0 time (or data_end)
    - If element starts hidden (inline opacity:0):
        show = first GSAP opacity:1 time → if none, never visible
        hide = first GSAP opacity:0 time after show (or data_end)
    """
    events = gsap_events.get(img["id"], [])
    show_events = [t for t, o in events if o == 1.0]
    hide_events = [t for t, o in events if o == 0.0]

    if img["starts_visible"]:
        show = img["data_start"]
    else:
        if not show_events:
            return (None, None, 0.0, "inline opacity:0 + no GSAP opacity:1 — element never shown")
        show = show_events[0]

    hide_candidates = [t for t in hide_events if t > show]
    hide = hide_candidates[0] if hide_candidates else img["data_end"]

    eff_start = max(show, img["data_start"])
    eff_end = min(hide, img["data_end"])
    eff_seconds = max(0.0, eff_end - eff_start)

    reason = None
    if hide > img["data_end"]:
        reason = (f"GSAP opacity:0 at {hide:.2f}s but data-duration ends at "
                  f"{img['data_end']:.2f}s — image disappears early because "
                  f"data-duration too short")
    return (eff_start, eff_end, eff_seconds, reason)


def check_visibility(imgs, gsap_events):
    """Flag images with effective visibility < MIN_VISIBLE_SECONDS."""
    findings = []
    for img in imgs:
        eff_start, eff_end, eff_seconds, reason = get_effective_visibility(img, gsap_events)
        if eff_seconds < MIN_VISIBLE_SECONDS:
            sev = "ERROR" if eff_seconds < 0.5 else "WARN"
            extra = f" — {reason}" if reason else ""
            findings.append(
                (sev, "visibility_under_1s",
                 f"#{img['id']} effective visibility = {eff_seconds:.2f}s "
                 f"(data-start={img['data_start']}, data-end={img['data_end']}, "
                 f"eff window=[{eff_start},{eff_end}]){extra}")
            )
    return findings


def check_duration_vs_gsap(imgs, gsap_events):
    """Flag images where GSAP opacity:0 is AFTER data-end (image cut off by data-duration)."""
    findings = []
    for img in imgs:
        events = gsap_events.get(img["id"], [])
        hide_events = [t for t, o in events if o == 0.0]
        if not hide_events:
            continue
        last_hide = max(hide_events)
        if last_hide > img["data_end"] + 0.01:
            findings.append(
                ("WARN", "data_duration_too_short",
                 f"#{img['id']} GSAP keeps opacity:1 until {last_hide:.2f}s but "
                 f"data-duration ends at {img['data_end']:.2f}s "
                 f"(diff = {last_hide - img['data_end']:.2f}s). "
                 f"Fix: data-duration={last_hide - img['data_start'] + 0.05:.2f}")
            )
    return findings


def check_z_index_conflicts(z_indices):
    """Flag overlay elements that may cover caption-wrap."""
    findings = []
    caption_z = z_indices.get(".caption-wrap", CAPTION_WRAP_Z_INDEX)
    risky = {
        "#black-overlay": "black overlay must be BELOW caption-wrap so captions remain visible on black",
        "#fade-out": "fade-out is canonical at z>caption-wrap, only an issue if used during caption display",
    }
    for sel, note in risky.items():
        z = z_indices.get(sel)
        if z is None:
            continue
        if z > caption_z:
            sev = "WARN" if sel == "#fade-out" else "ERROR"
            findings.append(
                (sev, "z_index_covers_captions",
                 f"{sel} z-index={z} > caption-wrap z-index={caption_z}. {note}")
            )
    return findings


def check_orphan_assets(html_dir: Path, content: str):
    """Flag assets/*.png or *.mp3 in filesystem not referenced anywhere in HTML.

    Skips known intermediate / library files that are expected to exist but not
    necessarily wired:
      - `*-raw.mp3` — pre-atempo TTS intermediates
      - `assets/sfx/cuts/*` — library of canonical cut SFX (reusable, not all used per video)
      - `*.json`, `*.txt`, `*.md` — config/spec files
    """
    findings = []
    assets_dir = html_dir / "assets"
    if not assets_dir.exists():
        return findings

    SKIP_SUFFIX_PATTERNS = ("-raw.mp3",)
    SKIP_PATH_FRAGMENTS = ("/sfx/cuts/", "/cuts/")

    for asset in assets_dir.rglob("*"):
        if not asset.is_file():
            continue
        if asset.suffix.lower() not in {".png", ".jpg", ".jpeg", ".mp3", ".wav", ".mp4"}:
            continue
        rel = asset.relative_to(html_dir).as_posix()
        # Skip known intermediates / libraries
        if any(rel.endswith(s) for s in SKIP_SUFFIX_PATTERNS):
            continue
        if any(frag in rel for frag in SKIP_PATH_FRAGMENTS):
            continue
        if rel in content or asset.name in content:
            continue
        findings.append(
            ("WARN", "orphan_asset",
             f"{rel} exists in filesystem but is not referenced in HTML")
        )
    return findings


def main():
    html_path = Path(sys.argv[1] if len(sys.argv) > 1 else "index.html").resolve()
    if not html_path.exists():
        print(f"audit-narrative: file not found: {html_path}", file=sys.stderr)
        sys.exit(2)

    content = parse_html(html_path)
    imgs = extract_imgs(content)
    gsap_events = extract_gsap_opacity_events(content)
    z_indices = extract_css_z_index(content)

    findings = []
    findings += check_visibility(imgs, gsap_events)
    findings += check_duration_vs_gsap(imgs, gsap_events)
    findings += check_z_index_conflicts(z_indices)
    findings += check_orphan_assets(html_path.parent, content)

    if not findings:
        print(f"audit-narrative: {len(imgs)} <img> tags, {len(gsap_events)} GSAP-controlled elements")
        print("✓ All checks pass")
        sys.exit(0)

    errors = [f for f in findings if f[0] == "ERROR"]
    warns = [f for f in findings if f[0] == "WARN"]

    for sev, check, msg in findings:
        print(f"[{sev}] {check}: {msg}")

    print()
    print(f"audit-narrative: {len(errors)} error(s), {len(warns)} warning(s)")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
