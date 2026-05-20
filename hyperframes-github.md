# HyperFrames — GitHub Repository Deep Dive
> Source: https://github.com/heygen-com/hyperframes
> Scraped: 2026-04-24 | Latest release: v0.4.22

---

## 1. REPOSITORY OVERVIEW

| Field | Value |
|-------|-------|
| Repo | heygen-com/hyperframes |
| Stars | 10,300+ |
| Forks | 856 |
| License | Apache 2.0 |
| Primary language | TypeScript (97.7%) |
| Runtime | Node.js ≥ 22 |
| Package manager | Bun (workspaces) |
| Module type | ES modules |
| Topics | html, typescript, video, ai, ffmpeg, animation, mcp, rendering, gsap, puppeteer |

---

## 2. REPOSITORY STRUCTURE

```
hyperframes/
├── .claude/                    # Claude AI integration config
├── .claude-plugin/             # Claude Code plugin manifest
├── .cursor-plugin/             # Cursor editor plugin
├── .codex-plugin/              # OpenAI Codex plugin
├── .github/                    # GitHub Actions workflows
├── assets/                     # Logo and icon assets
├── docs/                       # Documentation files
├── packages/
│   ├── cli/                    # hyperframes CLI tool
│   ├── core/                   # Types, parsers, runtime, linter
│   ├── engine/                 # Chrome BeginFrame capture engine
│   ├── producer/               # Full rendering pipeline
│   ├── studio/                 # Browser-based visual editor
│   ├── player/                 # Embeddable web component (3KB)
│   └── shader-transitions/     # WebGL shader transition effects
├── registry/
│   ├── blocks/                 # 39 ready-to-use block compositions
│   ├── components/             # 3 reusable snippet components
│   ├── examples/               # 8 starter templates
│   └── registry.json           # Registry manifest (53 items total)
├── skills/
│   ├── claude-design-hyperframes/  SKILL.md
│   ├── gsap/                       SKILL.md
│   ├── hyperframes/                SKILL.md
│   ├── hyperframes-cli/            SKILL.md
│   ├── hyperframes-registry/       SKILL.md
│   └── website-to-hyperframes/     SKILL.md
├── scripts/                    # Build and utility scripts
├── package.json                # Root monorepo config
├── bun.lock
└── LICENSE                     # Apache 2.0
```

---

## 3. PACKAGES

### 3.1 hyperframes (CLI) — `packages/cli`

**Source structure:**
```
src/
├── commands/
│   ├── add.ts           install blocks/components
│   ├── benchmark.ts     render performance measurement
│   ├── browser.ts       manage bundled Chrome
│   ├── capture.ts       extract website assets/screenshots
│   ├── catalog.ts       browse registry items
│   ├── compositions.ts  list project compositions
│   ├── doctor.ts        verify environment deps
│   ├── docs.ts          open documentation
│   ├── info.ts          version + environment info
│   ├── init.ts          scaffold new projects
│   ├── lint.ts          validate composition HTML
│   ├── play.ts          playback command
│   ├── preview.ts       launch studio with hot reload
│   ├── publish.ts       upload to hyperframes.dev
│   ├── render.ts        export to MP4/MOV/WebM
│   ├── skills.ts        install AI coding skills
│   ├── snapshot.ts      capture PNG frames
│   ├── telemetry.ts     telemetry management
│   ├── transcribe.ts    audio/video → word timestamps
│   ├── tts.ts           text-to-speech (Kokoro-82M)
│   ├── upgrade.ts       check for updates
│   └── validate.ts      WCAG contrast audit + structural check
├── browser/             Chrome management
├── capture/             Website capture utilities
├── docker/              Docker rendering support
├── docs/                CLI docs
├── registry/            Registry client
├── server/              Local file server
├── telemetry/           Analytics
├── templates/           Project templates
├── tts/                 TTS engine
├── ui/                  Terminal UI components
├── utils/               Helper functions
└── whisper/             OpenAI Whisper speech recognition
```

**Design philosophy:** All inputs via flags (non-interactive by default). Add `--human-friendly` for interactive prompts. Commands supporting `--json` output wrap with `_meta` envelope for agent version detection.

---

### 3.2 @hyperframes/core — `packages/core`

**Source structure:**
```
src/
├── adapters/
│   ├── gsap.ts          GSAP frame adapter
│   ├── gsap.test.ts
│   ├── types.ts         adapter interface definitions
│   └── index.ts
├── compiler/            timing resolution + HTML compiler + bundler
├── generators/          HTML generation from CompositionSpec
├── inline-scripts/      browser-injected scripts
├── lint/                composition linter
├── parsers/             HTML → TypeScript objects
├── registry/            registry client
├── runtime/             pre-built IIFE runtime for browser
├── studio-api/          Studio interface APIs
├── templates/           HTML templates
├── text/                text processing utilities
├── core.types.ts        ALL core TypeScript types (see below)
├── index.ts
└── index.test.ts
```

**Entry points:**
```js
import { ... } from '@hyperframes/core'           // types, parsers, generators
import { ... } from '@hyperframes/core/lint'       // linter
import { ... } from '@hyperframes/core/compiler'   // timing/HTML compiler, bundler
import { ... } from '@hyperframes/core/runtime'    // IIFE runtime for browser
```

---

### 3.3 @hyperframes/engine — `packages/engine`

**What it does:** Seekable HTML-page-to-video capture engine using Chrome's `HeadlessExperimental.beginFrame` API.

**8 main services:**
- `browserManager` — manages headless Chrome instances
- `frameCapture` — seeking, screenshots, buffer lifecycle
- `screenshotService` — Chrome DevTools Protocol capture
- `chunkEncoder` — buffered FFmpeg encoding
- `streamingEncoder` — real-time FFmpeg encoding
- `audioMixer` — process + combine audio tracks from HTML `<audio>` elements
- `videoFrameExtractor` — pull frames from video elements for composition
- `parallelCoordinator` — distribute frame ranges across workers
- `fileServer` — serve local HTML via Hono

**Seek protocol (window.__hf):**
```typescript
interface HfProtocol {
  duration: number;
  seek(time: number): void;
  media?: HfMediaElement[];
  transitions?: HfTransitionMeta[];
}

interface HfMediaElement {
  elementId: string;
  src: string;
  startTime: number;
  endTime: number;
  mediaOffset?: number;
  volume?: number;
  hasAudio?: boolean;
}

interface HfTransitionMeta {
  time: number;
  duration: number;
  shader: string;
  ease: string;
  fromScene: string;
  toScene: string;
}

// Global window augmentation
declare global {
  interface Window {
    __hf?: HfProtocol;
  }
}
```

**Capture types:**
```typescript
interface CaptureOptions {
  width: number;
  height: number;
  fps: number;
  format?: "jpeg" | "png";
  quality?: number;
  deviceScaleFactor?: number;
  skipReadinessVideoIds?: readonly string[];
}

interface CaptureResult {
  frameIndex: number;
  time: number;
  path: string;
  captureTimeMs: number;
}

interface CapturePerfSummary {
  frames: number;
  avgTotalMs: number;
  avgSeekMs: number;
  avgBeforeCaptureMs: number;
  avgScreenshotMs: number;
}
```

---

### 3.4 @hyperframes/producer — `packages/producer`

**Full rendering pipeline** — combines engine + FFmpeg:
```
1. Spin up local file server
2. Open HTML in headless Chrome
3. Capture frames via BeginFrame API
4. Process through FFmpeg (GPU acceleration auto-detected)
5. Extract + mix audio from HTML <audio> elements
```

**Programmatic API:**
```typescript
import { createRenderJob, executeRenderJob } from '@hyperframes/producer';

const job = createRenderJob({
  input: './my-video/index.html',
  output: './output.mp4',
  fps: 30,              // 24 | 30 | 60
  quality: 'standard',  // draft | standard | high
  width: 1920,
  height: 1080,
});
await executeRenderJob(job);  // supports progress callbacks + cancellation
```

**Also supports:** HTTP server mode (POST `/render`), Docker deterministic rendering, GPU acceleration (NVIDIA NVENC / macOS VideoToolbox / Linux VAAPI), HDR output, transparent video (WebM VP9, MOV ProRes 4444).

---

### 3.5 @hyperframes/studio — `packages/studio`

**Browser-based visual editor.** Launched via `npx hyperframes preview` (no direct install needed for standard use).

**React components:**
```js
import {
  StudioApp,          // complete app wrapper
  NLELayout,          // non-linear editor layout
  NLEPreview,
  Player,
  PlayerControls,
  Timeline,
  PreviewPanel,
  SourceEditor,
  PropertyPanel,
  FileTree,
  CompositionBreadcrumb,
} from '@hyperframes/studio'

import {
  useTimelinePlayer,   // playback control
  usePlayerStore,      // player state
  useCodeEditor,       // source editing
  useElementPicker,    // preview element selection
} from '@hyperframes/studio'
```

**Architecture:** iframe-isolated preview via `postMessage`, timeline parsing through `@hyperframes/core`, Vite-based HMR.

**Drag-and-drop:** Assets can be dragged from sidebar to timeline (added in v0.4.18).

---

### 3.6 @hyperframes/player — `packages/player`

**3KB gzipped web component** for embedding compositions.

```html
<!-- Via CDN -->
<script type="module" src="https://cdn.jsdelivr.net/npm/@hyperframes/player"></script>
<hf-player src="./my-video/index.html" controls autoplay muted loop
           width="1920" height="1080"></hf-player>
```

```typescript
// JavaScript API — mirrors native <video>
player.play()
player.pause()
player.seek(2.5)
player.currentTime   // getter
player.duration      // getter
player.paused        // getter

// Events
player.addEventListener('ready', ...)
player.addEventListener('timeupdate', ...)
player.addEventListener('play', ...)
player.addEventListener('pause', ...)
player.addEventListener('ended', ...)
player.addEventListener('error', ...)

// Advanced: access composition DOM/runtime
player.iframeElement  // for editors/recorders
```

**Mobile audio:** Automatically handles iOS Safari's iframe audio block by extracting timed media to parent-frame copies.

**Responsive:** Compositions scale to fit container while maintaining aspect ratio.

---

### 3.7 @hyperframes/shader-transitions — `packages/shader-transitions`

**GPU-accelerated scene-to-scene transitions using WebGL fragment shaders, driven by GSAP timelines.**

- Captures scenes to WebGL textures
- Crossfades between them using shader effects
- Fallback: hard cut if WebGL unavailable
- License: MIT (separate from Apache 2.0 main repo)

**14 shader effects available:**
chromatic-radial-split, cinematic-zoom, cross-warp-morph, domain-warp-dissolve, flash-through-white, glitch, gravitational-lens, light-leak, ridged-burn, ripple-waves, sdf-iris, swirl-vortex, thermal-distortion, whip-pan

**Distribution:** ESM, CJS, IIFE with TypeScript definitions.

**Aspect ratio support:** Any aspect ratio (landscape, portrait, square) — added in v0.4.20.

---

## 4. CORE TypeScript TYPES (core.types.ts)

```typescript
// Execution and canvas
export type ExecutionMode = "planning" | "design" | "execution" | null;
export type Orientation = "16:9" | "9:16";
export type CanvasResolution = "landscape" | "portrait";

export const CANVAS_DIMENSIONS = {
  landscape: { width: 1920, height: 1080 },
  portrait:  { width: 1080, height: 1920 },
} as const;

// Timeline elements
export type TimelineElementType = "video" | "image" | "text" | "audio" | "composition";
export type MediaElementType    = "video" | "image" | "audio";

export interface TimelineElementBase {
  id: string; type: TimelineElementType; name: string;
  startTime: number; duration: number; zIndex: number;
  x?: number; y?: number; scale?: number; opacity?: number;
}

export interface TimelineMediaElement extends TimelineElementBase {
  type: MediaElementType;
  src: string;
  mediaStartTime?: number; sourceDuration?: number; isAroll?: boolean;
  sourceWidth?: number; sourceHeight?: number;
  volume?: number; hasAudio?: boolean;
}

export interface TimelineTextElement extends TimelineElementBase {
  type: "text"; content: string; color?: string;
  fontSize?: number; textShadow?: boolean; fontFamily?: string; fontWeight?: number;
  textOutline?: boolean; textOutlineColor?: string; textOutlineWidth?: number;
  textHighlight?: boolean; textHighlightColor?: string;
  textHighlightPadding?: number; textHighlightRadius?: number;
}

export interface TimelineCompositionElement extends TimelineElementBase {
  type: "composition"; src: string; compositionId: string;
  scale?: number; sourceDuration?: number;
  variableValues?: Record<string, string | number | boolean>;
  sourceWidth?: number; sourceHeight?: number;
}

// Composition variables
export type CompositionVariableType = "string" | "number" | "color" | "boolean" | "enum";

export interface CompositionSpec {
  id: string;
  duration: number;
  variables: CompositionVariable[];
}

// Variable types: StringVariable, NumberVariable, ColorVariable, BooleanVariable, EnumVariable
// EnumVariable has: options: { value: string; label: string }[]

// Player API (full interface)
export interface PlayerAPI {
  play(): void; pause(): void; seek(time: number): void;
  getTime(): number; getDuration(): number; isPlaying(): boolean;
  getMainTimeline(): unknown;
  getElementBounds(elementId: string): void;
  getElementsAtPoint(x: number, y: number): void;
  setElementPosition(elementId: string, x: number, y: number): void;
  previewElementPosition(elementId: string, x: number, y: number): void;
  setElementKeyframes(elementId: string, keyframes: Keyframe[] | null): void;
  setElementScale(elementId: string, scale: number): void;
  setElementFontSize(elementId: string, fontSize: number): void;
  setElementTextContent(elementId: string, content: string): void;
  setElementTextColor(elementId: string, color: string): void;
  setElementTextShadow(elementId: string, enabled: boolean): void;
  setElementTextFontWeight(elementId: string, weight: number): void;
  setElementTextFontFamily(elementId: string, fontFamily: string): void;
  setElementTextOutline(elementId: string, enabled: boolean, color?: string, width?: number): void;
  setElementTextHighlight(elementId: string, enabled: boolean, color?: string, padding?: number, radius?: number): void;
  setElementVolume(elementId: string, volume: number): void;
  setStageZoom(scale: number, focusX: number, focusY: number): void;
  getStageZoom(): { scale: number; focusX: number; focusY: number };
  setStageZoomKeyframes(keyframes: StageZoomKeyframe[] | null): void;
  getStageZoomKeyframes(): StageZoomKeyframe[];
  addElement(data: AddElementData): boolean;
  removeElement(elementId: string): boolean;
  updateElementTiming(elementId: string, start?: number, end?: number): boolean;
  setElementTiming(elementId: string, startTime: number, duration: number, mediaStartTime?: number): void;
  updateElementSrc(elementId: string, src: string): boolean;
  updateElementLayer(elementId: string, zIndex: number): boolean;
  updateElementBasePosition(elementId: string, x?: number, y?: number, scale?: number): boolean;
  markTimelineDirty(): void; isTimelineDirty(): boolean;
  rebuildTimeline(): void; ensureTimeline(): void;
  enableRenderMode(): void; disableRenderMode(): void;
  renderSeek(time: number): void;
  getElementVisibility(elementId: string): { visible: boolean; opacity?: number };
  getVisibleElements(): Array<{ id: string; tagName: string; start: number; end: number }>;
  getRenderState(): { time: number; duration: number; isPlaying: boolean; renderMode: boolean; timelineDirty: boolean };
}

// Constants
export const TIMELINE_COLORS: Record<TimelineElementType, string> = {
  video: "#ec4899", image: "#3b82f6", text: "#06b6d4",
  audio: "#10b981", composition: "#f97316",
};

export const DEFAULT_DURATIONS: Record<TimelineElementType, number> = {
  video: 5, image: 5, text: 2, audio: 5, composition: 5,
};

// Type guards: isStringVariable, isNumberVariable, isColorVariable,
//              isBooleanVariable, isEnumVariable,
//              isTextElement, isMediaElement, isCompositionElement,
//              getDefaultStageZoom
```

---

## 5. AI SKILLS

All skills are installed via: `npx skills add heygen-com/hyperframes`

### 5.1 `hyperframes` skill — Composition authoring

**Workflow:**
1. Check for `DESIGN.md` or `visual-style.md` in the project
2. If user names a style, consult `visual-styles.md` for 8 named presets
3. If neither exists, ask about mood, light/dark, and brand direction
4. Generate minimal `DESIGN.md` with color palette + typography
5. Build layout first (hero frame), write static HTML+CSS
6. Animate *into* positions using `gsap.from()` for entrances
7. Reserve `gsap.to()` for exits only on final scenes

**Non-negotiable rules:**
- No randomness or time-based logic (deterministic)
- Every timeline must be in `window.__timelines["<id>"]`
- No `repeat: -1` — calculate exact repeat counts
- Build timelines synchronously (never inside `async`/`setTimeout`/Promises)
- Multi-scene: transitions between every scene; non-final scenes use entrance animations only (no exits)
- Video: `muted playsinline`; audio always in separate `<audio>` element
- No animation conflicts: same property on same element from multiple timelines is forbidden

**Sub-compositions:** Wrap in `<template>` + load via `data-composition-src` for reusable components. Standalone files go directly in `<body>` without `<template>`.

**Validation:** Run `npx hyperframes lint` + `npx hyperframes validate` before delivery. Validate runs WCAG contrast audits automatically.

---

### 5.2 `hyperframes-cli` skill — CLI usage

Complete documentation of all commands. Covers:
- 9 init templates (warm-grain, kinetic-type, product-promo, etc.)
- Lint validates: missing `data-composition-id`, overlapping tracks, unregistered timelines
- Render: quality levels, fps, GPU, Docker mode
- TTS: multiple voices, Kokoro-82M model
- Transcribe: MP3, MP4, subtitle formats

---

### 5.3 `gsap` skill — Animation reference

**Core GSAP methods:**
```js
gsap.to(target, vars)       // animate toward values
gsap.from(target, vars)     // entrance from values
gsap.fromTo(target, from, to)  // explicit start + end
gsap.set(target, vars)      // immediate, no animation
```

**Key properties:** `duration`, `delay`, easing (`"power1.out"`, `"elastic.out(1, 0.3)"`), `stagger`

**Transform aliases:** `x`, `y`, `z`, `scale`, `rotation`, `autoAlpha` (opacity + visibility)

**Timeline positioning:**
```js
tl.to(el, vars, 1.5)      // absolute: at 1.5s
tl.to(el, vars, "+=0.5")  // relative: 0.5s after previous ends
tl.to(el, vars, "<")       // same start as previous
tl.to(el, vars, ">")       // after previous ends
```

**Performance:** Animate transforms + opacity (compositor). Avoid width/height. Use `gsap.quickTo()` for frequent updates (event handlers).

---

### 5.4 `website-to-hyperframes` skill — URL-to-video pipeline

**Triggers:** user provides URL + requests video ("capture this site", "turn this into a video", "make a promo")

**7-step workflow:**

| Step | Artifact |
|------|---------|
| 1. Capture & Understand | site data summary: name, colors, fonts, assets, vibe |
| 2. Write DESIGN.md | 6-section brand reference (~90 lines) |
| 3. Write SCRIPT | narration with scene durations tied to dialogue |
| 4. Write STORYBOARD | beat-by-beat creative direction (mood, camera, animations, assets) |
| 5. Generate VO + Map Timing | TTS audio → transcribe → sync to beats |
| 6. Build Compositions | construct each scene; self-review |
| 7. Validate & Deliver | lint + validate + snapshot + preview → MP4 |

**Supported video types:**

| Type | Duration | Beats |
|------|----------|-------|
| Social ad | 10–15s | 3–4 |
| Product demo | 30–60s | 5–8 |
| Feature announcement | 15–30s | 3–5 |

**Supported formats:** Landscape (1920×1080), Portrait (1080×1920), Square (1080×1080)

---

### 5.5 `hyperframes-registry` skill — Block/component installation

**Blocks vs. Components:**
- **Blocks**: standalone sub-compositions (own dimensions, duration, timeline) → `data-composition-src`
- **Components**: effect snippets (no own dimensions) → paste directly into host composition

**Integration:**
- Blocks: `<div data-composition-src="..." data-composition-id="..." data-start="..." data-track-index="...">`
- Components: manually extract and merge 3 parts (HTML elements, CSS styles, JS code) into host

---

### 5.6 `claude-design-hyperframes` skill — Claude Design integration

**What Claude Design produces:** Valid first draft ZIP containing `index.html`, `preview.html`, `README.md`, `DESIGN.md`.

**Claude Design handles:** brand identity, scene layout, content hierarchy, entrance animations, mid-scene motion, shader transition placement (2–3 per video max), structural validity.

**Claude Code handles:** animation polish, timing refinement, production QA.

**Banned behaviors (Claude Design won't do):**
- Call `copy_starter_component` or use React/Babel
- Use SVG filter data URLs (breaks Safari + shader transitions)
- Create exit animations before shader transitions (shader IS the exit)
- Touch script loading order, timeline initialization, `.scene-content` wrapper
- Use banned typefaces: Inter, Roboto, Open Sans, Playfair Display, Fraunces

---

## 6. REGISTRY

**Total items: 53**
- 8 examples
- 3 components
- 42 blocks

**Registry manifest fields per item:** name, type, title, description, tags, dimensions, duration, files[]

### Blocks (39 folders in registry/blocks/):
app-showcase, chromatic-radial-split, cinematic-zoom, cross-warp-morph, data-chart, domain-warp-dissolve, flash-through-white, flowchart, glitch, gravitational-lens, instagram-follow, light-leak, logo-outro, macos-notification, reddit-post, ridged-burn, ripple-waves, sdf-iris, spotify-card, swirl-vortex, thermal-distortion, tiktok-follow, transitions-3d, transitions-blur, transitions-cover, transitions-destruction, transitions-dissolve, transitions-distortion, transitions-grid, transitions-light, transitions-mechanical, transitions-other, transitions-push, transitions-radial, transitions-scale, ui-3d-reveal, whip-pan, x-post, yt-lower-third

### Components (3):
grain-overlay, shimmer-sweep, grid-pixelate-wipe

### Examples (8 folders in registry/examples/):
decision-tree, kinetic-type, nyt-graph, play-mode, product-promo, swiss-grid, vignelli, warm-grain

---

## 7. EXAMPLE TEMPLATES — KEY STRUCTURE PATTERNS

### warm-grain (Landscape, cream aesthetic)
```html
<!-- Root composition: 1920×1080 -->
<div data-composition-id="warm-grain" data-width="1920" data-height="1080">
  <!-- A-Roll video (scales + repositions through 5 moments over 17s) -->
  <video class="clip" data-start="0" data-track-index="0" muted playsinline src="__VIDEO_SRC__">
  <!-- Nested compositions loaded via data-composition-src -->
  <div class="clip" data-composition-src="compositions/intro.html" ...>
  <div class="clip" data-composition-src="compositions/graphics.html" ...>
  <div class="clip" data-composition-src="compositions/captions.html" ...>
  <!-- Grain overlay: CSS keyframe animated noise texture -->
</div>
<!-- GSAP timeline: 5 distinct video framing moments via power2.inOut -->
<!-- Placeholder variables: __VIDEO_SRC__, __VIDEO_DURATION__ -->
```

### product-promo (Landscape, multi-scene)
```html
<!-- 5 sequential scenes: logo-intro → 3×canvas → logo-outro -->
<!-- Captions track overlaid: 3 messages fade in/out via GSAP -->
<!-- Typography: Inter font family -->
<!-- GSAP blur + scale transitions between scenes -->
<!-- Duration: ~20s total -->
```

---

## 8. RECENT RELEASES (last 10)

| Version | Date | Key Changes |
|---------|------|-------------|
| v0.4.22 | Apr 24, 2026 | (latest) |
| v0.4.21 | Apr 24, 2026 | Extraction-phase instrumentation, segment-scope HDR preflight, content-addressed extraction cache, fixed GSAP boundary exits + template-wrapped sub-composition media offsets |
| v0.4.20 | Apr 24, 2026 | Support any aspect ratio (vertical, square) for shader transitions |
| v0.4.19 | Apr 24, 2026 | SKILL.md download experience fixes |
| v0.4.18 | Apr 24, 2026 | Enhanced shader-transition capture robustness, drag-and-drop asset support in studio, template-first rewrite of design-skill |
| v0.4.17 | Apr 23, 2026 | Cursor + Claude Code plugin manifests, Claude Design entry point, streaming encoder lifecycle testing, hardened studio timeline editing |
| v0.4.16 | Apr 23, 2026 | Windows FFmpeg CI (BtbN), matrix3d transform handling, H.265 NVENC preset mapping, HDR + shader regression tests |
| v0.4.15 | Apr 23, 2026 | `hyperframes publish` feature (public URL sharing), HDR with dynamic SDR→HDR transfer, `--crf` + `--video-bitrate` CLI overrides |
| v0.4.15-alpha.1 | Apr 23, 2026 | Pre-release publish feature |
| v0.4.14 | Apr 23, 2026 | Performance metrics telemetry bridge, player optimizations (adoptedStyleSheets, MutationObserver), synchronous seek() API, HDR regression tests |

---

## 9. OPEN ISSUES (ACTIVE AS OF APR 24, 2026)

| # | Title | Type |
|---|-------|------|
| #440 | Cross-branch compatibility — clean scan | investigation |
| #418 | Dependency Dashboard (Renovate bot) | maintenance |
| #410 | Improve auto worker handling / guidance for WebGL-heavy compositions | enhancement |
| #408 | Codex install command fails with "invalid marketplace file" | bug |
| #407 | Install failed at the first hurdle | bug |
| #350 | Cloudflare Workers / Cloudflare Browser Run support | enhancement |
| #340 | Support for Reusable Components and Global Design Systems | feature request |
| #337 | How to connect ElevenLabs for TTS | question |

---

## 10. MONOREPO BUILD SYSTEM

```json
{
  "type": "module",
  "workspaces": ["packages/*"],
  "scripts": {
    "dev": "bun run studio",
    "build": "build all packages (CLI last)",
    "test": "bun run --filter '*' test",
    "lint": "oxlint",
    "format": "oxfmt",
    "unused": "knip"
  }
}
```

- **Runtime:** Bun
- **TypeScript:** 5.0
- **Linting:** oxlint
- **Formatting:** oxfmt
- **Unused code detection:** knip
- **Git hooks:** Lefthook
- **Commit style:** Conventional commits (commitlint)
- **Test runner:** Bun built-in

---

## 11. AI PLATFORM INTEGRATIONS

| Platform | Integration file |
|----------|-----------------|
| Claude Code | `.claude-plugin/` + skills system |
| Cursor | `.cursor-plugin/` |
| OpenAI Codex | `.codex-plugin/` |
| Claude Design | `skills/claude-design-hyperframes/SKILL.md` |

Install skill for any platform: `npx skills add heygen-com/hyperframes`
Then use `/hyperframes` prefix in prompts.

---

## 12. KEY ARCHITECTURAL DECISIONS

1. **HTML as source of truth** — not React, not proprietary DSL. LLMs write HTML naturally.
2. **Seek-driven rendering** — `seekFrame(N)` instead of real-time playback. Deterministic.
3. **window.__timelines** — all GSAP timelines registered here; framework drives them.
4. **window.__hf** — seek protocol exposed by compositions; engine calls `__hf.seek(time)`.
5. **Frame Adapter pattern** — any animation runtime that can answer "what does frame N look like?" integrates cleanly.
6. **Two layers** — HTML attributes declare *structure/timing*, GSAP declares *animation*. Scripts never control clip visibility or media playback.
7. **Sub-compositions via `<template>`** — loaded, parsed, mounted by runtime; no manual DOM wiring needed.
8. **Shader transitions as blocks** — WebGL textures capture scene before + after; fragment shader crossfades them; the shader IS the exit animation.

---

## 13. CONTRIBUTING

- PRs welcome (Apache 2.0)
- Requires Git LFS for full clone (test baselines are binary)
- Conventional commits required
- Test with: `bun run --filter '*' test`
- `npx hyperframes doctor` to verify local environment

GitHub: https://github.com/heygen-com/hyperframes
