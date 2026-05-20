# HyperFrames — Complete Knowledge Base
> Source: https://hyperframes.heygen.com | https://hyperframes.mintlify.app
> Scraped: 2026-04-24

---

## 1. WHAT IS HYPERFRAMES

HyperFrames is an **open-source framework** (Apache 2.0) by HeyGen that lets AI agents and developers create videos by writing **HTML, CSS, and JavaScript**. The tagline is: *"Write HTML. Render video. Built for agents."*

- Converts HTML documents into deterministic, frame-by-frame MP4/MOV/WebM video output
- Uses GSAP, Lottie, CSS animations — no proprietary tools
- Agent-friendly: LLMs can generate the HTML directly
- Non-interactive CLI by default (all inputs via flags)
- Free at any scale, redistribution permitted

---

## 2. CORE CONCEPTS

### 2.1 Compositions

A **composition** is an HTML document that defines a video timeline. It is the fundamental building block.

**Required root element attributes:**
```html
<div data-composition-id="my-video" data-width="1920" data-height="1080">
```

**Clip types supported:**
- `<video>` — video clips
- `<img>` — static images (require explicit `data-duration`)
- `<audio>` — audio clips (invisible)
- `<div data-composition-id="...">` — nested compositions

**Two-layer architecture:**
1. **HTML primitives** — declarative structure: what plays, when, which track
2. **Scripts (GSAP)** — effects and animations (NEVER control playback or show/hide clips by timing)

**Variables:** Passed via `data-variable-values` as JSON; compositions must read and apply them manually.

**Nesting:**
- External file: `data-composition-src="path/to/file.html"` — recommended for reusable components
- Inline: embedded directly without template tags

---

### 2.2 Data Attributes

| Attribute | Description |
|-----------|-------------|
| `data-composition-id` | Unique identifier for the composition wrapper |
| `data-width` | Canvas width in pixels |
| `data-height` | Canvas height in pixels |
| `data-start` | Start time in seconds, or relative to another clip ID |
| `data-duration` | Required for images; optional for video/audio |
| `data-track-index` | Z-order and overlap prevention on same track |
| `data-media-start` | Trim point for video/audio playback start |
| `data-volume` | Audio volume 0–1 |
| `data-has-audio` | Flag for videos with audio tracks |
| `data-composition-src` | External HTML file path for nested compositions |
| `data-variable-values` | JSON data passed to nested compositions |

**Relative timing system:**
- `data-start="intro"` → start when clip with id="intro" ends
- `data-start="intro + 2"` → gap of 2s after intro ends
- `data-start="intro - 0.5"` → overlap 0.5s before intro ends
- Overlapping clips must be on different tracks
- References must resolve within the same composition (no cross-composition references)
- Circular references throw errors

---

### 2.3 Deterministic Rendering

Same composition always produces the same video. Uses a frame-by-frame seek-driven approach.

**Four rendering stages:**
1. **Frame Clock** — `time = frame / fps` (integer math, no wall-clock)
2. **Seek** — `seekFrame(frame)` positions all animations and DOM state
3. **Capture** — Chrome headless API captures pixel buffers atomically
4. **Encode** — FFmpeg converts frames to MP4, mixes audio

**Avoid for determinism:**
- `Date.now()`, `requestAnimationFrame`
- Unseeded randomness (`Math.random()`) — use seeded PRNGs instead
- Network fetches during rendering
- Variable fps or dimensions

**Docker mode** locks Chrome version, fonts, and FFmpeg for identical output across platforms.

---

### 2.4 Frame Adapters

Frame adapters bridge animation runtimes to the Hyperframes rendering engine.

**Required interface:**
- `getDurationFrames()` — returns a finite integer
- `seekFrame(frame)` — positions animation to exact frame (must be idempotent, support any seek order)
- Optional: `init()` and `destroy()`

**Rule:** The adapter never controls timing — the host drives all seeking.

**Current status:** API is v0 (experimental). First-party support: GSAP. Planned: CSS/WAAPI, Lottie, Three.js, SVG/Anime.

---

## 3. GSAP ANIMATION

```javascript
// Required pattern
const tl = gsap.timeline({ paused: true }); // MUST be paused
tl.to(element, { opacity: 1, duration: 1 }, 1.5); // third arg = absolute position

// MUST register with composition ID
window.__timelines = window.__timelines || {};
window.__timelines["my-composition-id"] = tl;

// Extend timeline duration without animating elements:
tl.set({}, {}, 6); // forces timeline to reach 6 seconds
```

**Rules:**
- Always create timelines with `{ paused: true }`
- Register on `window.__timelines` using the exact `data-composition-id` as key
- Use the position parameter (third argument) for absolute timing
- Sub-compositions register their own timelines — framework auto-nests them
- Never manually play/pause/seek media elements
- Never animate `<video>` element dimensions directly (animate wrapper divs instead)
- Never create non-paused timelines

**Common mistake — video cuts off early:** Timeline is too short. Fix: `tl.set({}, {}, TARGET_DURATION)`

---

## 4. HTML SCHEMA REFERENCE

Every composition:
1. Root element needs `data-composition-id`, `data-width`, `data-height`
2. Timed elements need `data-start`, `data-duration` (for images), `data-track-index`, and `class="clip"`
3. GSAP timeline must be paused and registered on `window.__timelines`

**Clip requirements by type:**

| Type | `class="clip"` | `data-duration` | Notes |
|------|---------------|-----------------|-------|
| `<video>` | Required | Optional (defaults to source length) | Keep `muted`; audio in separate `<audio>` tag |
| `<img>` | Required | Required | |
| `<audio>` | Required | Optional | Invisible element |
| `<div data-composition-id>` | Required | Auto (GSAP timeline length) | |

---

## 5. CLI REFERENCE

```bash
npm install -g hyperframes
# or
npx hyperframes <command>
```

### Commands

| Command | Description |
|---------|-------------|
| `init` | Scaffold new project from example template |
| `add` | Install a block or component into existing project |
| `catalog` | Browse available registry items |
| `preview` | Live preview server with hot reload at localhost:3002 |
| `lint` | Check compositions for structural issues |
| `snapshot` | Capture key frames as PNG screenshots |
| `render` | Export to MP4/WebM/MOV |
| `capture` | Extract website assets, screenshots, fonts, design tokens |
| `publish` | Upload project, get stable hyperframes.dev URL |
| `transcribe` | Convert audio/video to word-level timestamps |
| `tts` | Generate speech locally (Kokoro-82M model) |
| `doctor` | Verify environment (Node.js, FFmpeg, Chrome, Docker) |
| `benchmark` | Benchmark render performance |
| `info` | Show system info for diagnostics |
| `skills` | Install AI coding skills for Claude Code, Gemini CLI, Cursor |

### Render options
```bash
npx hyperframes render \
  --output output.mp4 \
  --format mp4|mov|webm \
  --fps 24|30|60 \
  --quality draft|standard|high \
  --hdr               # HDR10 output (requires HDR sources + MP4)
  --workers N         # Chrome processes (default: half CPU cores, max 4)
```

**Quality presets:**
- `draft` — fast, lower quality (for iteration)
- `standard` — CRF 18, visually lossless at 1080p
- `high` — maximum quality

### Init examples
```bash
npx hyperframes init my-video --example blank
npx hyperframes init my-video --example warm-grain
npx hyperframes init my-video --example play-mode
npx hyperframes init my-video --example swiss-grid
npx hyperframes init my-video --example kinetic-type
npx hyperframes init my-video --example decision-tree
npx hyperframes init my-video --example product-promo
npx hyperframes init my-video --example nyt-graph
npx hyperframes init my-video --example vignelli    # portrait 1080×1920
```

### AI skill installation
```bash
npx skills add heygen-com/hyperframes
# Then use /hyperframes prefix in prompts
```

---

## 6. PACKAGES

| Package | Purpose |
|---------|---------|
| `@hyperframes/core` | Types, HTML parsing/generation, runtime, linter |
| `@hyperframes/engine` | Chrome BeginFrame capture engine (low-level) |
| `@hyperframes/producer` | Full HTML-to-video pipeline (Node.js programmatic use) |
| `@hyperframes/studio` | Browser-based visual editor (React components) |
| `@hyperframes/player` | Embeddable web component for playback (3KB gzipped) |
| `hyperframes` CLI | Command-line tool |

### @hyperframes/core entry points
```js
import { ... } from '@hyperframes/core'           // types, parsers, generators
import { ... } from '@hyperframes/core/lint'       // composition linter
import { ... } from '@hyperframes/core/compiler'   // timing/HTML compiler, bundler
import { ... } from '@hyperframes/core/runtime'    // IIFE runtime for browser
```

### @hyperframes/producer (programmatic rendering)
```typescript
import { createRenderJob, executeRenderJob } from '@hyperframes/producer';

const job = createRenderJob({
  input: './my-video/index.html',
  output: './output.mp4',
  fps: 30,
  quality: 'standard',
});
await executeRenderJob(job);
```

### @hyperframes/player (embedding)
```html
<!-- Web component -->
<hf-player src="./my-video/index.html" controls autoplay muted loop></hf-player>
```
- Mirrors native `<video>` API: `play()`, `pause()`, `seek()`, `currentTime`, `duration`
- Events: `ready`, `timeupdate`, `play`, `pause`, `ended`, `error`
- Default dimensions: 1920×1080

---

## 7. RENDERING MODES

### Local Mode
- Uses bundled Chromium + system FFmpeg
- Fast startup, GPU acceleration support
- Output may vary across platforms

### Docker Mode
```bash
npx hyperframes render --docker
```
- Identical output on every platform
- Locks Chrome, fonts, FFmpeg versions
- No GPU acceleration, slower startup
- Recommended for CI/CD and teams

### GPU Acceleration
- NVIDIA NVENC
- macOS VideoToolbox
- Linux VAAPI

### Transparent Video
- MOV + ProRes 4444 — industry standard, works in CapCut, Final Cut Pro, Premiere Pro, DaVinci Resolve, After Effects
- WebM VP9 alpha — technically supported but most video editors ignore the alpha channel

### HDR Rendering
- Requires `--hdr` flag + MP4 format + H.265 encoder
- Source must have BT.2020 primaries + PQ (smpte2084) or HLG (arib-std-b67) transfer
- 16-bit PNG is the only supported HDR still image format
- Mixed SDR/HDR compositions work (SDR converts from sRGB to BT.2020)

---

## 8. WORKFLOW

### Standard workflow
```
npx hyperframes init my-video
→ Edit compositions/index.html
→ npx hyperframes preview        # hot reload at localhost:3002
→ npx hyperframes lint            # validate structure
→ npx hyperframes render --output output.mp4
```

### AI agent workflow (recommended)
```
npx skills add heygen-com/hyperframes
→ Open project in Claude Code
→ Prompt with /hyperframes prefix
→ npx hyperframes preview
→ Iterate with targeted edits
→ npx hyperframes render
```

### Website-to-video pipeline
```
npx hyperframes capture <URL>    # capture screenshots, fonts, design tokens
→ 7-step automated pipeline:
  1. Capture  — screenshots, design tokens, fonts, assets
  2. Design   — brand reference document
  3. Script   — narration with structure
  4. Storyboard — beat-by-beat creative direction
  5. VO + Timing — audio with timestamps
  6. Build    — animated HTML compositions
  7. Validate — visual verification snapshots
```
Adding a Gemini API key enables AI vision analysis (~$0.04 for 40 images on paid plan).

---

## 9. PERFORMANCE & COMMON MISTAKES

### Critical mistakes (linter cannot catch these)
1. **Animating `<video>` dimensions** — breaks frame rendering; animate wrapper div instead
2. **Script-based media control** (`play()`, `pause()`, `currentTime`) — breaks sync; framework owns playback
3. **Timeline too short** — video cuts off early; use `tl.set({}, {}, DURATION)` to extend
4. **Missing `class="clip"`** — elements not visible (linter catches this)
5. **Oversized images** — resize to max 2× canvas dimensions
6. **Heavy `backdrop-filter: blur()` stacks** — limit to 2–3 layers with lower radii
7. **`--hdr` flag misuse** — it detects, not forces HDR; requires proper source metadata

### Performance tips
- `backdrop-filter: blur()` is the most expensive CSS property — limit stacking
- `filter: blur()` and `drop-shadow()` are expensive on large elements
- Shadows on animated elements cause re-rasterization each frame
- Image bitmap cost: `width × height × 4` bytes in memory
- Diagnose with Chrome DevTools Performance tab (main thread: composite layers, paint, image decoding)
- Use `--quality draft` during development
- Run `npx hyperframes benchmark` to measure render speed

### Debugging checklist
1. Run `npx hyperframes lint`
2. Check `window.__timelines` registration in browser console
3. Check browser console for errors
4. Hard-refresh preview browser
5. Run `npx hyperframes doctor` for environment issues

---

## 10. PROMPTING GUIDE (for AI agents)

### Setup
```bash
npx skills add heygen-com/hyperframes
# Use /hyperframes prefix in all prompts
```

### Effective vocabulary

| Intent | Say this |
|--------|----------|
| Smooth easing | "smooth" → `power2.out` |
| Bouncy motion | "bouncy" → `back.out` |
| Energetic caption | "Hype" tone → heavy fonts 72–96px + scale-pop animation |
| Calm transition | "calm" → blur crossfade |
| Medium transition | "medium" → push slide |
| High-energy transition | "high" → zoom through |
| Audio-reactive | Bass→scale, treble→glow, amplitude→opacity |

### Cold start prompt structure
- Duration + aspect ratio + mood + key elements
- Example: *"Create a 10-second product intro with fade-in title over dark background"*

### Warm start (from URL/doc)
- Provide URL or document + video concept
- Example: *"Summarize this PDF into a 45-second pitch video"*

### Iteration pattern
- Use targeted edits: *"Make the title 2× bigger"* — not full re-prompts

### Critical rules for agents
1. Register all timelines on `window.__timelines`
2. Keep `<video>` elements `muted` (audio in separate `<audio>` tags)
3. Never use `Math.random()` — use seeded PRNGs
4. Add entrance animations to every scene
5. Include transitions between scenes

---

## 11. STUDIO (Visual Editor)

Launch with: `npx hyperframes preview`

**Features:**
- Live preview matching render output exactly
- Visual timeline with clip structure
- Timeline editing: move (updates `data-start`), reposition rows (updates `data-track-index`), trim endpoints
- Source code editor
- Hot reload without restart
- iframe-isolated preview via postMessage

**Timeline editing constraints:**
- Media clips: move, row-change, shorten, trim beginning
- Motion/div clips: move, right-trim only (no front-trim)
- No split, slip, or ripple editing
- Z-order: row position + inline `z-index`

**Studio packages (for custom integration):**
```js
import { StudioApp, Player, Timeline, NLELayout } from '@hyperframes/studio'
import { useTimelinePlayer, usePlayerStore, useCodeEditor, useElementPicker } from '@hyperframes/studio'
```

---

## 12. CLAUDE DESIGN INTEGRATION

1. Download `SKILL.md` from HyperFrames docs
2. Attach to a Claude Design chat
3. Describe your video concept (+ brand assets, colors, screenshots)
4. Claude Design generates: `index.html`, `preview.html`, `README.md`, `DESIGN.md`
5. Download ZIP → refine in Claude Code with `/hyperframes` skill

**What Claude Design produces:** Valid first draft with brand identity, scene content, layout, animations, transitions — passes linting on first download.

**Limitations:** In-pane preview scrubbing is unreliable; use local preview. Cannot run linting directly.

---

## 13. HYPERFRAMES VS REMOTION

| | HyperFrames | Remotion |
|--|-------------|----------|
| Authoring | HTML + CSS + JS | React (TSX) |
| Animation | GSAP, Anime.js, CSS (seekable) | Per-frame React rendering |
| Agent-native | Yes — LLMs write HTML naturally | Harder — React abstractions |
| Visual editing | Direct DOM editing | Code-to-visual round-trip |
| HDR support | Yes | No |
| Distributed rendering | No | Yes (Remotion Lambda) |
| License | Apache 2.0 — free at any scale | Custom commercial — per-render fees above team threshold |
| Open source | Yes | Partially |

---

## 14. CATALOG — UI / SOCIAL OVERLAY BLOCKS

All blocks install via: `npx hyperframes add <name>`
All integrate as: `<div data-composition-id="NAME" data-composition-src="compositions/NAME.html" data-start="0" data-duration="N" data-track-index="1" data-width="W" data-height="H"></div>`

| Block | Description | Dimensions | Duration | Tags |
|-------|-------------|------------|----------|------|
| `app-showcase` | Three floating smartphone screens (fitness app) | 1920×1080 | 5.5s | showcase, 3d |
| `instagram-follow` | Animated Instagram follow overlay with profile card and follow button | 1080×1920 | 4.5s | social, overlay, instagram |
| `logo-outro` | Cinematic logo reveal: piece-by-piece assembly, glow bloom, tagline fade-in, URL pill | 1920×1080 | 6s | branding, outro |
| `macos-notification` | Animated macOS notification banner with app icon and message | 1920×1080 | 5s | social, overlay, notification |
| `reddit-post` | Animated Reddit post card overlay with upvote/comment elements | 1920×1080 | 5s | social, overlay, reddit |
| `spotify-card` | Animated Spotify now-playing card with album art and progress bar | 1080×1920 | 5s | social, overlay |
| `tiktok-follow` | Animated TikTok follow overlay with profile card and follow button | 1080×1920 | 4.5s | social, overlay |
| `x-post` | Animated X/Twitter post card with engagement metrics | 1920×1080 | 5s | social, overlay |
| `yt-lower-third` | Animated YouTube subscribe lower third with avatar and channel info | 1920×1080 | 4.5s | social, overlay, youtube |
| `data-chart` | Animated bar + line chart with staggered reveal, NYT-style typography, value labels | 1920×1080 | 15s | data, chart |
| `flowchart` | Animated decision tree with SVG connectors, sticky-note nodes, cursor interaction, typing correction | 1920×1080 | 12s | data, interactive |
| `ui-3d-reveal` | Perspective 3D reveal animation for UI elements | 1920×1080 | 13s | 3d, ui |

---

## 15. CATALOG — SHADER TRANSITION BLOCKS

All shader transitions: 1920×1080, 4 seconds, tags: `transition shader`

| Block | Description | Install |
|-------|-------------|---------|
| `chromatic-radial-split` | Chromatic aberration with radial split animation | `npx hyperframes add chromatic-radial-split` |
| `cinematic-zoom` | Dramatic zoom blur transition | `npx hyperframes add cinematic-zoom` |
| `cross-warp-morph` | Cross-warped morphing animation | `npx hyperframes add cross-warp-morph` |
| `domain-warp-dissolve` | Fractal noise domain warping | `npx hyperframes add domain-warp-dissolve` |
| `flash-through-white` | White flash crossfade | `npx hyperframes add flash-through-white` |
| `glitch` | Digital glitch artifacts | `npx hyperframes add glitch` |
| `gravitational-lens` | Gravitational lensing distortion | `npx hyperframes add gravitational-lens` |
| `light-leak` | Cinematic light leak overlay | `npx hyperframes add light-leak` |
| `ridged-burn` | Ridged turbulence burn effect | `npx hyperframes add ridged-burn` |
| `ripple-waves` | Concentric ripple wave distortion | `npx hyperframes add ripple-waves` |
| `sdf-iris` | Signed distance field iris reveal | `npx hyperframes add sdf-iris` |
| `swirl-vortex` | Swirling vortex distortion | `npx hyperframes add swirl-vortex` |
| `thermal-distortion` | Heat haze thermal distortion | `npx hyperframes add thermal-distortion` |
| `whip-pan` | Rapid camera pan movement effect | `npx hyperframes add whip-pan` |

---

## 16. CATALOG — TRANSITION SHOWCASE BLOCKS

All showcases: 1920×1080, tags: `transition showcase`

| Block | Description | Duration | Install |
|-------|-------------|----------|---------|
| `transitions-3d` | 3D perspective flip and rotate transitions | 11s | `npx hyperframes add transitions-3d` |
| `transitions-blur` | Blur-based transitions | 20s | `npx hyperframes add transitions-blur` |
| `transitions-cover` | Cover/uncover slide transitions | 21s | `npx hyperframes add transitions-cover` |
| `transitions-destruction` | Destructive break-apart transitions | 14s | `npx hyperframes add transitions-destruction` |
| `transitions-dissolve` | Dissolve and fade transitions | 24s | `npx hyperframes add transitions-dissolve` |
| `transitions-distortion` | Warp and distortion-based transitions | 21s | `npx hyperframes add transitions-distortion` |
| `transitions-grid` | Grid-based tile transitions | 11s | `npx hyperframes add transitions-grid` |
| `transitions-light` | Light-based glow and flash transitions | 21s | `npx hyperframes add transitions-light` |
| `transitions-mechanical` | Mechanical shutter and iris transitions | 15s | `npx hyperframes add transitions-mechanical` |
| `transitions-other` | Miscellaneous creative transitions | 20s | `npx hyperframes add transitions-other` |
| `transitions-push` | Push and slide transitions | 24s | `npx hyperframes add transitions-push` |
| `transitions-radial` | Radial wipe and reveal transitions | 20s | `npx hyperframes add transitions-radial` |
| `transitions-scale` | Scale and zoom transitions | 15s | `npx hyperframes add transitions-scale` |

---

## 17. CATALOG — COMPONENTS (Snippets)

Components are snippets integrated directly into compositions (not standalone compositions).
Install: `npx hyperframes add <name>` → file placed in `compositions/components/`

| Component | Description | Tags |
|-----------|-------------|------|
| `grain-overlay` | Animated film grain texture overlay using CSS keyframes — adds warmth and analog character | texture, grain, overlay, film |
| `grid-pixelate-wipe` | Transition: screen dissolves into grid of pixelated squares that fade in staggered timing | transition, wipe, grid, pixelate |
| `shimmer-sweep` | Animated light sweep across text/elements using CSS gradient mask — AI accents and premium reveals | text, shimmer, highlight, effect |

---

## 18. PROJECT CONFIGURATION

`hyperframes.json` — project config file:
```json
{
  "registry": "https://hyperframes.dev/r",
  "paths": {
    "compositions": "./compositions",
    "assets": "./assets",
    "blocks": "./compositions/blocks",
    "components": "./compositions/components"
  }
}
```

---

## 19. PREREQUISITES

- Node.js 22+
- FFmpeg (for encoding)
- Chrome/Chromium (bundled or system)
- Docker (optional, for deterministic rendering)

Check environment: `npx hyperframes doctor`

---

## 20. QUICK REFERENCE — MINIMAL VALID COMPOSITION

```html
<!DOCTYPE html>
<html>
<head>
  <style>
    body { margin: 0; background: #000; }
    .clip { position: absolute; }
  </style>
</head>
<body>
  <div id="root" data-composition-id="my-video" data-width="1920" data-height="1080">

    <img class="clip" src="assets/hero.jpg"
         data-start="0" data-duration="3" data-track-index="0"
         style="width:100%; height:100%; object-fit:cover;" />

    <div class="clip" id="title"
         data-start="0.5" data-duration="2.5" data-track-index="1"
         style="color:white; font-size:72px; top:40%; left:10%;">
      Hello World
    </div>

  </div>

  <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js"></script>
  <script>
    const tl = gsap.timeline({ paused: true });
    tl.from('#title', { opacity: 0, y: 30, duration: 0.5 }, 0.5);
    tl.set({}, {}, 3); // ensure full duration

    window.__timelines = window.__timelines || {};
    window.__timelines['my-video'] = tl;
  </script>
</body>
</html>
```

---

## 21. LINKS

| Resource | URL |
|----------|-----|
| Main site | https://hyperframes.heygen.com |
| Documentation | https://hyperframes.mintlify.app |
| Full docs index | https://hyperframes.mintlify.app/llms.txt |
| GitHub | https://github.com/heygen-com/hyperframes |
| Catalog (web) | https://hyperframes.heygen.com/catalog/blocks |
| Skill file (Claude Design) | Download SKILL.md from docs site |
