# PAUTA — Documento maestro de producción

> **Si sos un agente que entra a este proyecto por primera vez: este es tu único punto de entrada.** Leelo entero antes de generar, renderizar o modificar nada. Te dice qué leer en qué orden, qué calidad debe tener el output, y qué errores ya cometimos para que no los repitas.

**Última actualización:** 2026-05-10 (post V7 + reglas V8 incorporadas)
**Render de referencia:** `renders/hito-completo-v7.mp4` (V7, 9.5/10) — pendiente V8 con motion + SFX dedicado

---

## 0. EN UN PÁRRAFO

Este proyecto produce Instagram Reels verticales (1080×1920, 30fps) en formato horror-choice estilo `@referent-a`. El espectador elige entre dos compañeros — uno monstruoso pero honesto (Cristóbal), uno aparentemente amable pero distractor (Yerald) — y vive consecuencias narrativas con elecciones internas (mirar/no mirar, comer/no comer). Stack técnico: HyperFrames + GSAP para composición, ElevenLabs para narración, Gemini para imágenes, Kling para animación de imágenes estáticas, Gemini Video Analyzer para QA final.

---

## 1. ORDEN DE LECTURA (no saltarse pasos)

| # | Archivo | Por qué leerlo |
|---|---------|----------------|
| 1 | `.claude/skills/horror-choice-format/PAUTA.md` (este) | Punto de entrada AL FORMATO. Define orden, criterios, reglas V7+V8 del formato horror-choice. |
| 2 | `<proyecto>/CLAUDE.md` | Gobernanza del proyecto (Plan-First rule, Phase 2 simplicity). Cada proyecto tiene su docs/OPERATING-MANUAL.md. |
| 3 | `.claude/skills/ai-video-production/BOOTSTRAP.md` | **Solo si arrancás proyecto nuevo desde cero.** Setup genérico: dir, venv, .env, scripts, smoke tests. |
| 4 | `.claude/skills/horror-choice-format/BOOTSTRAP-NEW-PROJECT.md` | Adaptación al formato: inputs FASE 0 horror-specific, templates específicos a copiar. |
| 5 | `.claude/skills/horror-choice-format/PATTERNS.md` | Reglas perennes del formato (timing %, personajes, dilemas, cliffhanger, choice mechanics). |
| 6 | `.claude/skills/horror-choice-format/PAUTA-MASTER.md [ex-CREATIVE-BRIEF deprecated]` | **Pauta narrativa.** QUÉ historia contar dentro del formato — slots de creatividad, 4 arquetipos de cliffhanger para rotar, 8 story seeds, template del brief, checklist pre-producción. Rellenar el template ANTES de generar assets. |
| 7 | `.claude/skills/horror-choice-format/SCRIPT-WRITING-GUIDE.md` | Cómo escribir el guion. Checklist V8 con plan de assets (variantes + SFX + motion). |
| 8 | `<proyecto>/NARRATIVE.md` | Guion implementado del proyecto. En nuevo proyecto, copiar de `templates/NARRATIVE-TEMPLATE.md`. |
| 9 | `<proyecto>/DESIGN.md` | Colores y tipografía específicos del video. |
| 10 | `.claude/skills/ai-video-production/PIPELINE.md` | Pipeline técnico GENERAL: TTS, image, render, music, GSAP base, symlinks. Reusable a cualquier formato. |
| 11 | `.claude/skills/ai-video-production/MOTION-LAYER.md` | Motion patterns GENERAL: Ken Burns + parallax + flicker + vignette + glitch + glow + niebla. |
| 12 | `.claude/skills/ai-video-production/SFX-PIPELINE.md` | SFX pipeline GENERAL: ai-video sfx + loop expansion >22s + mix volumes canónicos. |
| 13 | `.claude/skills/ai-video-production/IMAGE-VARIETY.md` | Regla V8-1 universal: variantes -a/-b/-c para escenas >4s. |
| 14 | `.claude/skills/ai-video-production/CAPTIONS.md` | Whisper auto-captions. |
| 15 | `.claude/skills/ai-video-production/QA.md` | Gemini Video Analyzer pattern + interpretación de feedback. |
| 16 | `.claude/skills/horror-choice-format/PRODUCTION-PIPELINE.md` | Detalles técnicos APLICADOS al formato horror (V7 rules CSS, Kling prompts horror). |
| 17 | `docs/FEEDBACK-LOOP.md` (raíz) | Método para verificar video sin poder verlo. General — complementa Gemini QA. |
| 17 | `<proyecto>/V6-VS-V7.md` | Historia de iteraciones del proyecto (V6→V7→V8). |
| 18 | `.claude/skills/horror-choice-format/VIDEO-PLAYBOOK.md` | Playbook secuencial fases 0→7 con templates HTML/GSAP por tipo de hito. |

---

## 2. CRITERIO DE CALIDAD — CUÁNDO PUBLICAR

Después de cada render, ejecutar el QA de Gemini OBLIGATORIAMENTE:

```bash
python3 ~/.claude/skills/video-analyzer/scripts/analyze_video.py \
  renders/nombre.mp4 \
  --prompt "Analiza en detalle:
  (1) ¿Se entiende cuándo es outcome A vs B en cada elección?
  (2) ¿La transición a [BUENO_APARENTE] es clara?
  (3) ¿El texto es legible en todos los fondos?
  (4) ¿El tamaño del texto A/B es suficiente para móvil?
  (5) ¿Hay CTA al final?
  (6) ¿Hay variedad visual o se reusa la misma imagen en múltiples captions de una misma escena?
  (7) ¿El video se siente vivo (motion en cada plano) o slideshow (fotos estáticas con texto)?
  (8) ¿El diseño sonoro va más allá de narración + música? (¿hay footsteps, breaths, impactos, ambient continuo?)
  (9) ¿Hay momentos donde la imagen permanece estática >2s sin ningún tipo de motion?
  Dame un score 1-10 considerando estas 9 dimensiones."
```

**⛔ Vara de calidad = DUAL (canónica, NUNCA single-score):**
- (a) Gemini **calibrado ≥9.7** Y
- (b) **audit-against-referent ≥85%** métricas críticas (p25-p75 bands).
- AMBAS requeridas. (El umbral histórico ≥9.0 de abajo es legacy V7 y queda solo como referencia interpretativa de la severidad del feedback, NO como gate de publicación.)

| Score Gemini | Acción |
|-------|--------|
| **≥ 9.7 (calibrado) + referent ≥85%** | APROBADO para publicar (DUAL gate) |
| **9.0 – 9.6** | Iterar. Anotar cada feedback de Gemini en V6-VS-V7.md y aplicar reglas V7 — todavía NO publica (no llega a la vara DUAL) |
| **7.0 – 8.9** | Iterar. Algo de calidad falta; revisar feedback dimensión por dimensión |
| **< 7.0** | Revisar diseño desde la raíz, no solo timing — algo estructural está roto |

**Referencia histórica:**
- V6 → 7.0/10 (problemas: ramas A/B secuenciales, transición abrupta, texto pequeño, sin CTA)
- V7 → 9.5/10 (todos los problemas resueltos con las 6 reglas V7)
- bosque-abandonado v2 (proyecto hermano) → análisis Gemini detectó "síndrome de diapositivas": 17 fotos fijas reutilizadas + sound design pobre. Origen de las **reglas V8** abajo.

**No publicar nada por debajo de la vara DUAL (Gemini calibrado ≥9.7 + audit-against-referent ≥85%).** No tiene sentido subir un video viral imperfecto cuando una iteración de 15 min lo lleva a perfecto.

---

## 3. LAS 6 REGLAS V7 — LA CALIDAD MÍNIMA

Estas reglas son la diferencia entre 7/10 y 9.5/10. Aplicarlas DESDE EL PRIMER RENDER, no como pulido después.

Referencia técnica completa: `PRODUCTION-PIPELINE.md` sección 10.

### V7-1. Stroke negro en todos los captions
```css
.caption { -webkit-text-stroke: 1.5px rgba(0,0,0,0.7); }
```
Sin esto el texto blanco se pierde en niebla, amanecer o fuego.

### V7-2. Choice labels A/B en 64px (no 48px) + stroke
```css
.choice-label { font-size: 64px; -webkit-text-stroke: 2px rgba(0,0,0,0.8); }
```
A 48px el pulgar tapa la elección en móvil.

### V7-3. Separador de rama A→B en cada elección interna
Entre outcome A y outcome B: pulso oscuro suave + caption "SI [opción B]:" en azul claro `#c8d8ff` por 1.2s. Sin esto, las ramas se perciben como secuenciales en vez de alternativas.

### V7-4. Puente narrativo antes del cliffhanger
1.5s antes del flash que abre la rama buena, caption en dorado `#f5d9a0`: "Y SI HUBIERAS ELEGIDO A [BUENO_APARENTE]..." Sin esto, el cambio de tono se siente como glitch.

### V7-5. CTA de engagement al final — TEXTO + VOZ DEL NARRADOR

**DOS capas obligatorias en los últimos 2.4s del video:**

- **Visual:** caption "¿SOBREVIVISTE? 💬 COMENTA A o B" en 60px
- **Audio:** narración del MISMO voice ID que el narrador del video (voz canónica — ver `assets/library/voices-catalog.json`; default `2gPFXx8pN3Avh27Dw5Ma`, narrador V5 `K3TeN3ZVK8WnOeJ0NYqZ`. ⛔ `Tj9l48J9AJbry5yCP5eW` DEPRECATED) preguntando directamente al espectador. Plantilla:
  > "Y tú... ¿qué habrías elegido? Comenta A o B abajo, y dinos por qué."

**Por qué la voz es obligatoria:** el texto solo invita a comentar "A" o "B" (1 carácter, bajo peso algorítmico). La voz pide "y por qué" → comentarios largos → mejor distribución en el feed.

**Implementación:** generar `assets/cta-narration.mp3` con `ai-video tts`. (⛔ `atempo 2.0`/2x DEPRECATED — el pipeline real cappea velocidad a ≥0.90 y NO ralentiza la voz; ver `INGENIERO-PAUTA-MASTER.md` § 1.6.) Track-index libre en la franja de narración del Hito 6.

### V7-6. Gemini QA gate antes de aprobar
Vara DUAL obligatoria antes de publicar (AMBAS): Gemini calibrado **≥9.7** + `audit-against-referent` **≥85%** (ver § 2 + `quality_standards`). Sin excepciones. (El ≥9.0 histórico = legacy V7, NO gate de publicación.) **Prompt extendido en sección 2** evalúa también motion y sound design.

### V7-7. Instagram safe zones (REGLA INVIOLABLE)

Instagram superpone su UI sobre el frame al reproducir. Cualquier texto en zona reservada se ve **tapado o cortado al subir el video**. Esto no es opcional ni estético — es técnico.

**CSS obligatorio:**
```css
.name-label       { top: 300px; }                    /* labels superiores */
.caption-wrap     { bottom: 540px; height: 280px; }  /* captions principales + CTA */
.loading-bar-wrap { bottom: 700px; }                 /* opciones A/B durante elección */
```

**Zonas reservadas (NO poner texto acá):**
- **Top:** y = 0–270 (botón X, audio info, sound mute)
- **Bottom:** y = 1380–1920 (caption del post, profile pic, audio, follow)
- **Right:** x = 840–1080 (like, comment, share, save, "...")

**Zona segura para texto crítico:** X 60–840, Y 270–1380.

Especificación completa en `DESIGN.md` sección "Instagram Safe Zones". Detectado en V7 draft (texto en zona insegura) y resuelto en V7 final.

---

## 3.7 LAS 3 REGLAS V8 — DE "REEL CON NARRACIÓN" A "CORTO CINEMATOGRÁFICO"

> Aprendidas del post-mortem de `bosque-abandonado/renders/v2-final.mp4` (2026-05-09): el video pasaba todas las reglas V7 pero Gemini lo describió como "presentación de PowerPoint" — 17 fotos estáticas, mismo PNG reutilizado 10×, sin SFX granular más allá de música ambient + ticks.
>
> Aplicar V8 desde el primer render, igual que V7. Implementación técnica completa en `PRODUCTION-PIPELINE.md` secciones 2.5, 3.5, 12 y 13. Reglas perennes del formato en `PATTERNS.md` secciones 2, 3, 10 y 11.

### V8-1. Variantes de imagen obligatorias (regla de variedad)

Cualquier escena que se muestra >4s en el video DEBE tener **2–3 variantes** de imagen con sufijos `-a`, `-b`, `-c`. Reutilizar el mismo PNG en múltiples captions de la misma escena produce sensación de slideshow, **especialmente cuando se le aplica motion** (parallax y Ken Burns delatan la repetición todavía más).

Las variantes deben cambiar ángulo / distancia / pose / framing — no escenario. Budget: +5–8 imágenes por video (~$0.20–0.40 en Gemini).

**Implementación**: `PRODUCTION-PIPELINE.md` § 2.5. **Regla perenne**: `PATTERNS.md` § 3.

### V8-2. Capa de sound design dedicada

Cada escena necesita SFX granulares más allá de narración + música + ticks de countdown: footsteps en cada plano de caminata, breaths/whispers en momentos de tensión, impactos en cada white flash, ambient continuo (wind/dawn) por debajo de todo el video.

**Motor único:** ElevenLabs Sound Effects API vía `ai-video sfx` con `sfx-spec.json` batch. Para ambient loops >22s, generar 22s con `loop:true` y expandir con ffmpeg `stream_loop` — patrón en `PRODUCTION-PIPELINE.md` § 12.5.
**Fallback opcional:** Freesound solo si un asset puntual sale notoriamente uncanny y no se arregla iterando el prompt. **No es parte del workflow estándar.** Decisión 2026-05-10 validada en bosque-abandonado v3.

**Mix volumes** → tabla canónica completa en `../ai-video-production/SFX-PIPELINE.md § Mix volumes` (narración 1.0 / música 0.05–0.18 / SFX 0.20–0.35 / flash 0.55–0.65 / ambient continuo 0.10–0.18 / clinks 0.25–0.35). No dupliques la tabla acá. Reservar `data-track-index` 60–110 para SFX en `index.html`.

**Implementación**: `PRODUCTION-PIPELINE.md` § 12 (ElevenLabs) y § 13 (Freesound). **Regla perenne**: `PATTERNS.md` § 2.

### V8-3. Motion mínimo en todo plano

Ningún plano queda estático >2s sin algún tipo de motion. **Ken Burns es el piso, no el techo.**

Stack de motion (aplicar lo que corresponda por escena):
- **Ken Burns global** (`scale 1.0 → 1.04`, `ease: sine.inOut`) — obligatorio en todo plano estático
- **Parallax 3 capas** (fondo lento, medio, primer plano rápido) en planos con profundidad
- **Flicker de exposición** (`filter: brightness` 0.9↔1.1 a 0.8–2Hz) en luces y rostros tensos
- **Handheld shake sutil** (translate ±2px @ 6Hz) en close-ups de horror
- **Vignette pulsante** (radial-gradient animado) en momentos de tensión sostenida
- **Glitch frame** (1–2 frames de displacement) antes/durante twists
- **Glow pulsante** (brightness + box-shadow animado) en fuentes de luz
- **Niebla/partículas/chispas** overlay con `mix-blend-mode: screen` en exteriores

Tier de prioridad por escena: Ken Burns siempre. Parallax + flicker + vignette donde aporten al género. Glitch + shake solo en twists.

**Implementación**: `PRODUCTION-PIPELINE.md` § 3.5. **Regla perenne**: `PATTERNS.md` § 10.

---

## 4. WORKFLOW COMPLETO DE PRODUCCIÓN

```
┌─────────────────────────────────────────────────────────┐
│  FASE 0 — INPUTS  (10 min)                               │
│  Recolectar: nombre malo, nombre bueno, escenario,       │
│  dilema 1, dilema 2. VIDEO-PLAYBOOK.md Fase 0.            │
└──────────────────────┬───────────────────────────────────┘
                       ▼
┌─────────────────────────────────────────────────────────┐
│  FASE 0.5 — CREATIVE BRIEF  (20 min) ⭐ NUEVO            │
│  Rellenar el CREATIVE-PROMPT-TEMPLATE de                 │
│  PAUTA-MASTER.md (Slots A-H) con TODOS los slots.              │
│  Elegir cliffhanger archetype DIFERENTE al del video     │
│  anterior (ver video-log.md). Pasar los 24 puntos del    │
│  checklist pre-producción § 6 antes de tocar APIs.       │
└──────────────────────┬───────────────────────────────────┘
                       ▼
┌─────────────────────────────────────────────────────────┐
│  FASE 1 — SCRIPT  (30 min)                               │
│  Escribir narración siguiendo SCRIPT-WRITING-GUIDE.md    │
│  + slots del Creative Brief de la Fase 0.5.              │
│  Incluir CTA narrado al final (V7-5).                    │
│  Checklist de validación obligatorio antes de TTS.       │
└──────────────────────┬───────────────────────────────────┘
                       ▼
┌─────────────────────────────────────────────────────────┐
│  FASE 2 — ASSETS  (1.5-2 horas)                          │
│  TTS (ElevenLabs voz canónica — voices-catalog.json;     │
│   ⛔ NO Tj9l48J9 ni atempo 2x, ver INGENIERO-PAUTA §1.6)  │
│  Imágenes + VARIANTES -a/-b/-c (V8-1) — regla obligatoria│
│  SFX dedicado vía ai-video sfx + sfx-spec.json (V8-2)  │
│  Ambient loops >22s: EL loop:true + ffmpeg stream_loop   │
│  Video animado (Kling, prompts validados)                │
│  Música (Pixabay, procesar en 2 pasos — no -ss + -af)    │
└──────────────────────┬───────────────────────────────────┘
                       ▼
┌─────────────────────────────────────────────────────────┐
│  FASE 3 — COMPOSITION + MOTION  (45-90 min)              │
│  Editar index.html aplicando las 6 reglas V7 desde el    │
│  primer momento + motion layer V8-3 (Ken Burns global,   │
│  parallax, flicker, vignette pulse donde aplique).       │
│  Conectar capa SFX (track-index 60-110).                 │
│  Anclar en t=0 todo lo invisible.                        │
│  Crear symlink assets → "assets v1" antes del render.    │
└──────────────────────┬───────────────────────────────────┘
                       ▼
┌─────────────────────────────────────────────────────────┐
│  FASE 4 — RENDER DRAFT  (8-15 min)                       │
│  npx hyperframes render --output renders/draft.mp4       │
│  Si falla con EPIPE o Target closed: reintentar.         │
└──────────────────────┬───────────────────────────────────┘
                       ▼
┌─────────────────────────────────────────────────────────┐
│  FASE 5 — QA GEMINI  (3 min)                             │
│  /video-analyzer renders/draft.mp4 con prompt completo.  │
│  Score ≥ 9.7 → ir a Fase 6.                              │
│  Score < 9.7 → volver a Fase 3 con feedback de Gemini.   │
└──────────────────────┬───────────────────────────────────┘
                       ▼
┌─────────────────────────────────────────────────────────┐
│  FASE 6 — RENDER FINAL  (~30 min)                        │
│  Re-render en --quality high para el upload.             │
│  Actualizar V6-VS-V7.md con la versión nueva.            │
└─────────────────────────────────────────────────────────┘
```

---

## 5. ERRORES PASADOS — NO REPETIR

### 5.1 Render sin assets
Los assets están en `assets v1/` pero el HTML referencia `assets/`. Sin symlink el render produce videos silenciosos / sin imágenes.

```bash
cd "/ruta/al/proyecto"
ln -sf "assets v1" assets
```

### 5.2 Render falla con EPIPE / Target closed
Crash transitorio de Chrome. **Reintentar el mismo comando.** No tocar el código.

### 5.3 Audio silencioso después de procesar música
Si usás `-ss antes de -i` + `-af` en el mismo comando ffmpeg, el output sale silencioso. Siempre en 2 pasos: primero extraer, después aplicar fades. Ver `PRODUCTION-PIPELINE.md` sección 8.

### 5.4 Voz TTS suena a IA
> ⛔ **DEPRECATED.** Este caso describía el viejo flujo `atempo=2.0` (`-2x.mp3`), que ya NO es el pipeline real: hoy la voz NO se ralentiza/duplica, se cappea velocidad a ≥0.90. Ver `INGENIERO-PAUTA-MASTER.md` § 1.6 para el manejo canónico de pace TTS. (Conservado como nota histórica del por-qué se dejó de usar el `-raw.mp3` crudo.)

### 5.5 Flash visible al inicio de un elemento
Falta la ancla `tl.set(el, {opacity:0, scale:1.0}, 0)` en t=0. Sin ella HyperFrames hace pre-render del estado visible. Nunca usar `fromTo` para estados iniciales.

### 5.6 Gemini rechaza el prompt de imagen
Describir el resultado visual, no la acción violenta. "Una pierna con exoesqueleto quitinoso visible" pasa; "una pierna siendo cortada con sangre" no. Tabla completa en `PRODUCTION-PIPELINE.md` sección 2.

### 5.7 Kling aplica la acción sobre el sujeto en lugar del espectador
Para movimientos hacia el espectador, describir la experiencia del espectador, no la del sujeto. "Foreleg descends into frame, fills screen, cuts to black" funciona. "Mantis swings foreleg at viewer" no.

### 5.8 Captions cortados fuera de pantalla
Default `white-space: nowrap` rompe frases largas. Siempre `white-space: normal` + `width: 960px`.

### 5.9 Ramas A/B percibidas como secuenciales
Sin separador V7-3, el espectador no distingue "si elegís A pasa esto" de "si elegís B pasa lo otro". Detectado por Gemini en V6.

### 5.10 Transición abrupta al cliffhanger
Sin puente V7-4, el cambio de tono de horror a paz se percibe como glitch. Detectado por Gemini en V6.

### 5.11 Imágenes reusadas hacen slideshow
En bosque-abandonado v2, `h3-forest-walk.png` se referenciaba 10× en el HTML para 4 captions distintas de la misma escena. Gemini lo detectó como "PowerPoint narrado". Aplicar **V8-1**: cualquier escena >4s necesita 2-3 variantes con sufijos `-a`/`-b`/`-c`. Generar las variantes ANTES de aplicar motion — el parallax y Ken Burns delatan la repetición todavía más.

### 5.12 Video sin SFX dedicados se siente plano
Solo música ambient + ticks de countdown + narración **no es sound design**. El video se siente "narrador con música", no cine. Aplicar **V8-2**: capa SFX granular por escena (footsteps, breaths, impactos, ambient continuo). Motor: `ai-video sfx` con `sfx-spec.json`. Auxiliar: Freesound para lo que ElevenLabs no genera bien.

### 5.13 Symlinks para variantes de imagen (backward-compat)
Cuando renombrás un asset existente para soportar variantes (`nombre.png → nombre-a.png`), dejá un symlink desde el nombre original al nuevo `-a` para no romper renders previos de la composición:

```bash
cd assets/
ln -sf nombre-a.png nombre.png
```

Distinto del symlink elige-style de § 5.1 (folder completo `assets → assets v1`). Este es por archivo individual y solo aplica cuando agregás variantes a una composición que ya rendereó al menos una vez.

### 5.14 Texto tapado por la UI de Instagram
En V7 draft, names estaban en `top:180px` y captions en `bottom:0 height:400px`. Al subir a Instagram quedaban tapados — names bajo el botón X + audio info; captions bajo el caption del post + profile pic + audio. Aplicar **V7-7**: `.name-label { top: 300px }`, `.caption-wrap { bottom: 540px; height: 280px }`, `.loading-bar-wrap { bottom: 700px }`. Verificación visual obligatoria: extraer un frame con captions y confirmar que el texto vive en y=270–1380 (la franja central 14%–72%).

---

## 6. APIS Y COSTOS

| API | Uso | Costo aproximado por video |
|-----|-----|---------------------------|
| ElevenLabs TTS | Narración (10-15 generaciones × 5-10s c/u) | ~$0.30 |
| ElevenLabs Sound Effects | SFX dedicado V8-2 (~30-35 SFX incluyendo ambient loops) | ~$5-10 |
| Gemini (Google AI Studio) | Imágenes + variantes V8-1 (15-20 generaciones) | Free tier |
| Gemini (Video Analyzer) | QA post-render (1-3 análisis) | Free tier |
| Replicate (Kling) | Video animado (8-12 clips × 5s c/u) | ~$3 |
| Pixabay | Música royalty-free | Free |
| Freesound | Fallback opcional (solo si EL falla puntualmente) | Free |

**Plan-First rule (docs/OPERATING-MANUAL.md):** antes de cualquier llamada a API, proponer un plan y esperar confirmación explícita del usuario. Incluso si la API es gratis — porque consume créditos y tiempo.

API keys: `.env` en raíz del proyecto. Verificar `GEMINI_API_KEY`, `ELEVENLABS_API_KEY`, `REPLICATE_API_TOKEN`.

---

## 7. ESTADO ACTUAL DEL PROYECTO

> **Movido.** El estado vivo del proyecto (sprints en flight, video shipped, próximos pasos) vive en `memory/active_session_state.md` + `horror-choice-format/video-log.md`. El planning Phase 2/3 + `TEMPLATE-SPEC.md` quedó archivado (no se usa el path de parameterización descrito acá).

---

## 8. CHECKLIST FINAL ANTES DE PUBLICAR

- [ ] Render generado en `renders/nombre.mp4`
- [ ] Symlink `assets → assets v1` existe (+ symlinks de variantes si aplican, § 5.13)
- [ ] Las 6 reglas V7 aplicadas (verificar en index.html)
- [ ] Las 3 reglas V8 aplicadas:
  - [ ] V8-1: cada escena >4s tiene ≥2 variantes de imagen
  - [ ] V8-2: capa SFX dedicada conectada (track-index 60-110, mix volumes correctos)
  - [ ] V8-3: ningún plano estático >2s sin Ken Burns como mínimo
- [ ] Vara DUAL cumplida: Gemini calibrado ≥9.7 + `audit-against-referent` ≥85% (prompt extendido § 2, 9 dimensiones)
- [ ] V6-VS-V7.md actualizado con la versión nueva y el score
- [ ] Lint ejecutado: `npx hyperframes lint` sin errores nuevos
- [ ] Render en --quality high (no draft) para upload final
- [ ] `CREDITS.md` actualizado si se usaron assets Freesound CC-BY
- [ ] Caption del post preparado: "¿Elegiste al compañero correcto?" + hashtags relevantes

---

## 9. CONTACTO Y REFERENCIAS

**Proyecto:** elige-companero
**Inspiración:** `@referent-a` (3 videos virales analizados en `REFERENCE-ANALYSIS.md`)
**Stack:**
- HyperFrames (composition + render)
- GSAP 3.14.2 (animaciones)
- ElevenLabs (TTS)
- Google Gemini (imágenes + video analysis)
- Replicate Kling v2.0 (animación de imágenes)
- Pixabay (música royalty-free)
- `~/.claude/skills/video-analyzer/` (skill local de QA con Gemini)

**Voice ID del narrador horror:** ver `assets/library/voices-catalog.json` (default `2gPFXx8pN3Avh27Dw5Ma`; narrador V5 `K3TeN3ZVK8WnOeJ0NYqZ`). ⛔ `Tj9l48J9AJbry5yCP5eW` DEPRECATED — NO usar.
