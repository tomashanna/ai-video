# ARCHITECTURE.md — Las 3 capas del sistema

> **Este doc es el más importante para entender el sistema entero.** Define qué vive dónde, qué se reutiliza, qué se replica, qué se crea por proyecto. Sin esta separación clara, cada video reinventa la rueda y nada escala.

---

## TL;DR

```
┌───────────────────────────────────────────────────────────────┐
│  CAPA 1 — UNIVERSAL                                            │
│  Sirve para CUALQUIER template (horror, documental, edu…)      │
│  Vive en: video-director/ + ai-video-production/ + library/    │
│  NUNCA se replica. NUNCA se modifica por proyecto.             │
└───────────────────────┬───────────────────────────────────────┘
                        │
                        ▼
┌───────────────────────────────────────────────────────────────┐
│  CAPA 2 — TEMPLATE-ESPECÍFICO                                  │
│  Reglas perennes de UN formato (horror-choice, doc, edu…)      │
│  Vive en: <formato>-format/  (ej: horror-choice-format/)       │
│  Se REPLICA cuando se crea un template nuevo.                  │
└───────────────────────┬───────────────────────────────────────┘
                        │
                        ▼
┌───────────────────────────────────────────────────────────────┐
│  CAPA 3 — POR-VIDEO                                            │
│  Datos únicos de UN video específico                           │
│  Vive en: <proyecto>/  (ej: bosque-abandonado/)                │
│  Se CREA nuevo por cada video.                                 │
└───────────────────────────────────────────────────────────────┘
```

---

## CAPA 1 — UNIVERSAL

> Lo que vive acá NO cambia entre formatos. Es la infraestructura del director de video.

### 🌐 `video-director/` — identidad + workflow

| Archivo | Contenido | Cuándo se usa |
|---|---|---|
| `SKILL.md` | Identidad + quality bar + hard rules + diagrama de skills | Carga al inicio de TODA sesión de video |
| `PERSONALITY.md` | Voz, registros, cuándo discrepar | Aplicar en cualquier interacción |
| `WORKFLOW.md` | Loop maestro 5 pasos + flujos típicos | Cualquier tarea de video |
| `DECISION-FRAMEWORK.md` | Cuándo preguntar vs ejecutar | Decisiones de scope |
| `ANTI-PATTERNS.md` | Aprendizajes amargos universales | Antes de inventar algo |
| `META-BRAND.md` | TU identidad como creador (Toby Hanna) | Decisiones de portfolio multi-cuenta |
| `PERFORMANCE.md` | Sistema de feedback loop con métricas IG | Después de publicar cada video |
| `PATTERNS-LIBRARY.md` | Catálogo cross-account validados | Meta-review cada 10 videos |
| `HANDOFF-PROMPTS.md` | Template para delegar iteración a otra IA | Cuando se delega |
| `ARCHITECTURE.md` | Este doc | Antes de crear template/proyecto nuevo |
| `PROJECT-STRUCTURE.md` | Esqueleto de cada proyecto | Bootstrap de proyecto nuevo |
| `templates/video-performance-template.md` | Template captura métricas | T+48h por video |

### 🛠️ `ai-video-production/` — toolkit técnico

| Archivo | Contenido |
|---|---|
| `PIPELINE.md` | TTS, render, música, naming, GSAP base, symlinks |
| `MOTION-LAYER.md` | Ken Burns, parallax, flicker, vignette, glitch, glow, niebla |
| `IMAGE-VARIETY.md` | Variantes -a/-b/-c, tipos de plano |
| `CAPTIONS.md` | Whisper auto-sync + safe zone IG |
| `SFX-PIPELINE.md` | ElevenLabs SFX + mix volumes canónicos |
| `BOOTSTRAP.md` | Setup genérico de proyecto |
| `QA.md` | Gemini QA + interpretación feedback |
| `NARRATIVE-LED-EDITING.md` | Sistema 7 cortes con SFX específicos |
| `ELEMENTS-LIBRARY.md` | Sistema híbrido de componentes UI |
| `templates/scripts/*.py` | Scripts genéricos sin STYLE_SUFFIX |

### 📦 `library/` — assets reutilizables

| Carpeta | Contenido |
|---|---|
| `library/LIBRARY.md` | Catálogo maestro de SFX/voces/música |
| `library/sfx-catalog.json` | Machine-readable de SFX |
| `library/voices-catalog.json` | Machine-readable de voice IDs |
| `library/sfx/` | 53+ SFX organizados por categoría |
| `library/voices/` | Referencias a voice IDs |
| `library/music/` | Música procesada lista para reutilizar |

### 📋 Raíz `AI video 1/`

| Archivo | Contenido |
|---|---|
| `FEEDBACK-LOOP.md` | Frame slicing + Read para validar video sin reproducir |
| `elements.json` | Catálogo machine-readable de componentes UI (countdown/loader/lower-third) |
| `.agents/skills/hyperframes*` | Skill oficial viva HyperFrames (API/CLI/registry, v0.6.69+). Reemplaza los scrapes `hyperframes-github.md`/`hyperframes-knowledge.md` (v0.4.22, DEPRECATED → `_archive-deprecated-docs/`) |

### 🌐 Skills globales `~/.claude/skills/`

| Skill | Propósito |
|---|---|
| `video-analyzer` | QA con Gemini Video Analyzer |
| `find-skills` | Discovery de skills externos |
| `hyperframes`, `hyperframes-cli` | API/CLI HyperFrames |
| `gsap`, `waapi`, `css-animations` | Motion APIs |

---

## CAPA 2 — TEMPLATE-ESPECÍFICO

> Esto se **REPLICA** cuando agregás un template nuevo. Hoy existe `horror-choice-format/`. Mañana puede aparecer `documental-format/`, `educacional-format/`, etc.

### 🎭 `<formato>-format/` — reglas del formato

Estructura canónica (todos los formatos deben tener):

| Archivo | Contenido | Obligatorio? |
|---|---|---|
| `SKILL.md` | Entry point del skill, descripción auto-trigger | ✅ |
| `PAUTA.md` | Orden de lectura + criterios de calidad del formato | ✅ |
| `PATTERNS.md` | Reglas perennes del formato (timing, audio, visual, lenguaje) | ✅ |
| `SCRIPT-WRITING-GUIDE.md` | Cómo escribir guion DEL FORMATO | ✅ |
| `VIDEO-PLAYBOOK.md` | Estructura de hitos + templates HTML/GSAP por hito | ✅ |
| `PAUTA-MASTER.md [ex-CREATIVE-BRIEF deprecated]` | Archetypes + story seeds + slots creativos | Opcional (formatos narrativos) |
| `REFERENCE-ANALYSIS.md` | Análisis de virales referentes del nicho | ✅ |
| `BOOTSTRAP-NEW-PROJECT.md` | Bootstrap aplicado al formato | ✅ |
| `PRODUCTION-PIPELINE.md` | Comandos aplicados (STYLE_SUFFIX, prompts) | ✅ |
| `BRAND.md` | Audience persona + voz + paleta + hashtags de la cuenta IG | ✅ |
| `video-log.md` | Registro de archetypes/temas usados por video (rotation log) | ✅ |
| `TEMPLATE-SPEC.md` | Phase 3 stuff (parametrización futura) | Opcional |

### 📋 `<formato>-format/templates/` — templates copiables

| Template | Contenido |
|---|---|
| `NARRATIVE-TEMPLATE.md` | Esqueleto del NARRATIVE.md por proyecto |
| `SFX-LIST-TEMPLATE.md` | Lista de SFX típicos del formato (referenciar library/) |
| `sfx-spec-TEMPLATE.json` | Spec batch SFX típico del formato |
| `hyperframes.json-TEMPLATE` | Config HyperFrames con valores del formato |
| `scripts/{captions,image,sfx,tts}.py` | Scripts CON STYLE_SUFFIX hardcoded del formato |

---

## CAPA 3 — POR-VIDEO

> Esto se **CREA NUEVO** cada vez que arrancás un video. Vive en `<proyecto>/`.

Estructura canónica de cada proyecto. Detalle completo en `PROJECT-STRUCTURE.md`.

| Archivo / carpeta | Origen | Único o copy? |
|---|---|---|
| `CLAUDE.md` | Copy adaptado del proyecto previo del mismo formato | Replica |
| `DESIGN.md` | Copy del previo del mismo formato | Replica con ajustes |
| `NARRATIVE.md` | Copy de `<formato>/templates/NARRATIVE-TEMPLATE.md` | Esqueleto replicado, contenido único |
| `creative-brief-vN.md` | Llenando template de PAUTA-MASTER.md [ex-CREATIVE-BRIEF deprecated] | Único |
| `V6-VS-V7.md` (o `vN.md`) | Vacío al inicio | Único |
| `AGENTS.md` | Copy del previo | Replica |
| `hyperframes.json` | Copy de template | Replica con ajustes |
| `meta.json` | Generado por `hyperframes init` | Único |
| `index.html` | Construido con HTML/GSAP | Único |
| `assets/` | TTS + imágenes + SFX generados PARA este video | Único |
| `scripts/` | Copy de `<formato>/templates/scripts/` | Replica |
| `renders/` | MP4s draft + final | Único |
| `performance/` | Capturas T+48h por video | Único |
| `.env` | API keys | Replica |

---

## Reglas de propagación

### Cuando arrancás un VIDEO NUEVO dentro del mismo template

```
1. CAPA 1 (video-director/, ai-video-production/, library/) → REUTILIZAR tal cual (skills cargados)
2. CAPA 2 (formato/) → REUTILIZAR tal cual
3. Buscar en library/ los SFX/música/voces necesarios → COPIAR a tu proyecto
4. Buscar en elements.json los componentes UI → wire via data-composition-src
5. CAPA 3 → CREAR carpeta nueva <proyecto-N>/
   - Copy CLAUDE/DESIGN/AGENTS/hyperframes.json del proyecto previo del mismo formato
   - Copy scripts/ del formato
   - Generar NARRATIVE.md llenando template
   - Llenar creative-brief-vN.md (slot-based)
   - Generar assets SOLO de lo que no esté en library/
6. Actualizar <formato>-format/video-log.md con archetype/tema usado
7. Después de Gemini ≥9.7 y publicación: capturar performance a T+48h
8. Cada 10 videos: meta-review → actualizar PATTERNS-LIBRARY.md
```

### Cuando arrancás un TEMPLATE NUEVO (ej: documental-format)

```
1. CAPA 1 → REUTILIZAR tal cual
2. <formato-actual>/ → IGNORAR (es de otro formato)
3. CREAR NUEVO skill: <nuevo-formato>-format/ con TODA la estructura canónica de Capa 2
   - SKILL.md, PAUTA.md, PATTERNS.md (reglas perennes DEL NUEVO formato)
   - SCRIPT-WRITING-GUIDE.md (estilo de guion del nuevo formato)
   - VIDEO-PLAYBOOK.md (estructura de hitos del nuevo formato)
   - PAUTA-MASTER.md si aplica (archetypes empíricos del formato)
   - REFERENCE-ANALYSIS.md (análisis de virales del nuevo nicho)
   - BOOTSTRAP-NEW-PROJECT.md, PRODUCTION-PIPELINE.md (con STYLE_SUFFIX propio)
   - BRAND.md (audience nueva cuenta IG)
   - video-log.md (vacío)
   - templates/ (NARRATIVE, SFX, scripts con STYLE_SUFFIX nuevo)
4. Si el visual del template requiere estilo distinto → crear `elements/<estilo-nuevo>/`
   en raíz + actualizar elements.json. Si no → reutilizar elements existentes.
5. Si el formato requiere SFX nuevos → generarlos en proyecto piloto, después promover a library/
6. Primer <proyecto> del nuevo formato → Capa 3 normal
```

### Cuando descubrís un pattern NUEVO en producción

```
1. ¿Es universal o específico del formato?
   - Específico → va a <formato>-format/PATTERNS.md o doc relevante
   - Universal → ¿lo viste en 2+ formatos?
     - Si → va a CAPA 1 (ai-video-production/ o video-director/)
     - Si no → todavía está en evaluación, va a video-director/PATTERNS-LIBRARY.md § "en evaluación"
2. ¿Es un SFX/asset reutilizable?
   - Si → copiar a library/ + actualizar LIBRARY.md + sfx-catalog.json
3. ¿Es un anti-pattern descubierto?
   - Universal → video-director/ANTI-PATTERNS.md
   - Format-specific → <formato>-format/ correspondiente
```

---

## Cómo invocar las 3 capas al iniciar un video

### Sesión nueva: el video-director skill se auto-carga
- Identidad + workflow + quality bar
- META-BRAND para context estratégico
- `CLAUDE.md` § Mapa de docs autoritativos para saber qué leer por tema

### Skill del formato se auto-carga si la tarea menciona keywords del formato
- horror-choice-format si el usuario menciona "hito", "choice", "horror"
- documental-format si menciona "documental", "investigación", etc.

### Librería se invoca explícitamente desde WORKFLOW.md
- Antes de generar SFX → leer library/LIBRARY.md primero
- Antes de pick countdown/loader → leer elements.json

### Skills técnicas se cargan automáticamente
- hyperframes, hyperframes-cli, gsap cuando se tocan archivos relevantes

---

## Decisiones arquitectónicas (con criterio de cambio)

| Decisión | Estado actual | Cambiar si… |
|---|---|---|
| Element library híbrida (universal + por estilo) | ✅ Implementado | Aparece 3+ estilos distintos → más sub-folders |
| Voice IDs en library central | ✅ Implementado | Más de 10 voces validadas → categorizar por nicho |
| Video-log con el formato | ✅ Implementado | Aparezca 2+ cuentas IG del mismo formato → mover a per-cuenta |
| Brand de cuenta con el formato | ✅ Implementado | Aparezca 2+ cuentas IG del mismo formato → crear carpeta per-cuenta |
| 1 cuenta IG = 1 formato | ✅ Asumido | Si querés mezclar formatos en una cuenta → revisar estrategia |
| CAPA 1 (universal) no se modifica por proyecto | ✅ Inviolable | Nunca cambiar |
| CAPA 2 (formato) se modifica solo cuando aparece pattern validado | ✅ Implementado | Sigue así |
| CAPA 3 (proyecto) se descarta cuando se borra proyecto | ✅ Implementado | Backup en git si hay riesgo |

---

## Anti-patterns de arquitectura

- ❌ **Hacer modificaciones a CAPA 1 desde un proyecto específico.** Si necesitás cambiar algo universal, evalualo desde el lente de "¿esto sirve a TODOS los videos futuros?"
- ❌ **Hardcodear assets de horror en `ai-video-production/`.** Eso pertenece a `horror-choice-format/`.
- ❌ **Crear un nuevo skill por proyecto.** Los proyectos NO son skills. El formato sí.
- ❌ **Duplicar templates entre formato y proyecto.** El proyecto referencia el template, no lo duplica con cambios.
- ❌ **Modificar la library con un asset que solo sirve al proyecto actual.** Promover a library solo después de validar reutilidad.
- ❌ **Olvidar agregar al sfx-catalog.json cuando agregás archivos.** El JSON es la fuente de verdad machine-readable.
