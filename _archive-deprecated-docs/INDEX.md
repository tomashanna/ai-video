# INDEX — Front door del directorio AI Video 1

> Tabla rápida trigger → doc. Si tu tarea no aparece acá, consultá `CLAUDE.md` § Mapa de docs autoritativos (autoridad canónica).

---

## 🎯 Por dónde empezar según tarea

| Tarea | Skills a activar | Docs primarias (leer ANTES de planear) |
|---|---|---|
| **⭐ Video nuevo (cualquier genre × cualquier format)** | video-director + ai-video-production + skill del genre | **PRIMERO**: `ai-video-production/DELIVERY-FORMATS.md` (matriz + catálogo), después `formats/<delivery>.md` + `<genre>-format/PAUTA.md`. Si short-form: `+ RETENTION-RULES.md`. |
| **Video nuevo horror-choice × reel** (combo validado v15 9.9/10) | video-director + ai-video-production + horror-choice-format | `formats/reel.md`, `horror-choice-format/PAUTA.md`, `horror-choice-format/INTRO-FORMULA-V15.md`, ⭐ `horror-choice-format/PAUTA-MASTER.md` (autoridad empírica — PAUTA-MASTER.md [ex-CREATIVE-BRIEF deprecated] deprecated), `RETENTION-RULES.md`, `library/LIBRARY.md` |
| **Crear template nuevo de genre (no-horror)** | video-director + ai-video-production | `video-director/ARCHITECTURE.md` § "Cuando arrancás un TEMPLATE NUEVO", `ai-video-production/DELIVERY-FORMATS.md` |
| **Iterar video existente** | video-director + ai-video-production (+ formato si aplica) | `video-director/WORKFLOW.md` § Paso 5, `ai-video-production/QA.md`, `video-director/ANTI-PATTERNS.md` |
| **Generar assets (TTS + imágenes + SFX)** | ai-video-production (+ formato) | `ai-video-production/PIPELINE.md`, `IMAGE-VARIETY.md`, `CHARACTER-CONSISTENCY.md`, `library/LIBRARY.md` |
| **Construir index.html (composición)** | ai-video-production (+ formato) | `MOTION-LAYER.md`, `NARRATIVE-LED-EDITING.md`, `CAPTIONS.md`, `ELEMENTS-LIBRARY.md`, `elements.json` |
| **Animar con Kling/Replicate** | video-animation | `video-animation/SKILL.md`, `video-animation/ANIMATION-LAYER.md` |
| **QA con Gemini** | ai-video-production | `ai-video-production/QA.md`, `FEEDBACK-LOOP.md`, `video-director/HUMAN-CHECKLIST.md` |
| **Render con HyperFrames** | hyperframes + hyperframes-cli + ai-video-production | `ai-video-production/PIPELINE.md` § 5+11, `ai-video-production/AUDIT.md` |
| **Performance capture (T+48h)** | video-director | `video-director/PERFORMANCE.md`, `video-director/templates/video-performance-template.md` |
| **Debug / problema técnico** | (consultar primero) | `video-director/ANTI-PATTERNS.md`, `CLAUDE.md` § Mapa de docs autoritativos |

---

## 🗺️ Triggers semánticos → skill

| Si la tarea menciona… | Activá |
|---|---|
| "video", "render", "captions", "SFX", "narración", "TTS", "Gemini" (sin más contexto) | video-director + ai-video-production |
| "horror", "hito", "H1-H6", "choice", "dilema", "twist", "cliffhanger", "compañero", "referent-a" | + horror-choice-format |
| "animar", "Kling", "Replicate", "image-to-video", "convertir imágenes en clips" | + video-animation |
| "hyperframes lint/render/init/preview/transcribe/tts" | + hyperframes + hyperframes-cli |
| "GSAP", "timeline", "tl.to", "easing", "stagger", "yoyo" | + gsap |
| "captura web", "URL a video", "promo de sitio web" | + website-to-hyperframes |

---

## 📁 Mapa físico del directorio

```
AI video 1/
├── CLAUDE.md                          ← auto-load context al inicio
├── INDEX.md                           ← este archivo
├── FEEDBACK-LOOP.md                   ← validación visual sin reproducir
├── NARRATION-RULES.md                 ← reglas TTS
├── hyperframes-knowledge.md           ← refs API
├── hyperframes-github.md              ← refs repo
├── elements.json                      ← catálogo countdown/loader/lower-third
├── skills-lock.json                   ← versiones skills
│
├── .claude/skills/                    ← CAPA 1 + CAPA 2 (skills)
│   ├── video-director/                ← META — identidad, workflow, quality bar
│   ├── ai-video-production/           ← TÉCNICO — TTS, motion, SFX, captions, QA
│   ├── video-animation/               ← Kling / Replicate
│   └── horror-choice-format/          ← FORMATO horror-choice
│
├── library/                           ← CAPA 1 — assets reutilizables
│   ├── LIBRARY.md
│   ├── voices-catalog.json
│   ├── sfx-catalog.json
│   ├── sfx/  music/  voices/
│
├── countdown-{pulse,glitch,slam}/     ← componentes UI universales
├── loader-{bar,radial,segments}/      ← componentes UI universales
├── lower-{typewriter,handwritten,...}/← componentes UI universales
│
├── .agents/skills/                    ← skills HyperFrames externas
│   └── (hyperframes, hyperframes-cli, gsap, ...)
│
└── <proyecto>/                        ← CAPA 3 — un directorio por video
    ├── elige-companero/
    ├── bosque-abandonado/
    ├── mina-abandonada/
    └── compare-cuts/
```

---

## ⚡ Atajos para llegar rápido

| Quiero saber… | Archivo |
|---|---|
| Las 3 capas del sistema | `.claude/skills/video-director/ARCHITECTURE.md` |
| Workflow maestro 5 pasos | `.claude/skills/video-director/WORKFLOW.md` |
| Hard rules globales | `.claude/skills/video-director/SKILL.md` § Hard rules |
| Voice ID + atempo | `library/voices-catalog.json` + `library/LIBRARY.md` § Voice IDs |
| Anti-patterns conocidos | `.claude/skills/video-director/ANTI-PATTERNS.md` |
| Bootstrap proyecto nuevo | `.claude/skills/ai-video-production/BOOTSTRAP.md` |
| Mapa autoritativo trigger→doc | `CLAUDE.md` § Mapa de docs autoritativos |
| Starter prompts copy-paste | `.claude/skills/video-director/STARTER-PROMPTS.md` |
| Bugs sutiles HyperFrames | `.claude/skills/ai-video-production/HYPERFRAMES-GOTCHAS.md` |

---

## 🚫 Si dudás dónde vive algo

Regla rápida:
- **Sirve a CUALQUIER video futuro?** → CAPA 1 (`video-director/` o `ai-video-production/` o `library/`)
- **Sirve solo a UN formato?** → CAPA 2 (`<formato>-format/`)
- **Sirve solo a UN video?** → CAPA 3 (`<proyecto>/`)

Detalle: `.claude/skills/video-director/ARCHITECTURE.md`.

---

## 🔄 Última actualización

2026-05-11. Inicial. Reemplaza el mapa trigger→doc anterior (descontinuado 2026-05-16, reemplazado por `CLAUDE.md` § Mapa de docs autoritativos).
