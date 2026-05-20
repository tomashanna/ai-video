# TEMPLATE-SPEC.md — Schema técnico del generador

> Especificación para el template parametrizable de Phase 4. Define qué es variable (slot del usuario) y qué es constante (constraint del formato). Para construirse con Hyperframes + GSAP siguiendo `PATTERNS.md`.

---

## ESTRUCTURA GENERAL

El template recibe un archivo `video-config.json` y produce un MP4 vertical 1080×1920 listo para Instagram Reels.

```
video-config.json
   ↓
[GENERATOR]
   ↓
1. Genera assets (images via Gemini, narración via ElevenLabs procesada, video animado via Kling para escenas seleccionadas)
2. Compone HTML con sub-compositions de Hyperframes
3. Aplica GSAP timelines con timing fijo basado en %
4. Renderiza MP4
   ↓
output.mp4
```

---

## SCHEMA DE INPUT — `video-config.json`

```json
{
  "meta": {
    "id": "video-001",
    "duration_seconds": 90,
    "fps": 30,
    "dimensions": {
      "width": 1080,
      "height": 1920
    }
  },
  "characters": {
    "bad_apparent": {
      "name": "MARTÍN",
      "image_prompt": "...",
      "image_path": "assets/martin.png",
      "video_clip_path": "assets/martin-loop.mp4",
      "dialogue": [
        "Inteligente.",
        "Ahora escucha."
      ]
    },
    "good_apparent": {
      "name": "TOBÍAS",
      "image_prompt": "...",
      "image_path": "assets/tobias.png",
      "video_clip_path": null
    }
  },
  "scenario": {
    "name": "Faro de Punta Negra",
    "ambient_description": "faro abandonado en costa rocosa, niebla densa",
    "color_palette": {
      "dominant": "#2A3540",
      "accent": "#8B4513",
      "warm_cliffhanger": "#E89D5E"
    }
  },
  "narrative": {
    "moral_dilemma_category": "curiosity_vs_obedience",
    "warning_text": "EL FARO LLEVA AÑOS APAGADO",
    "setup_text": "Si eliges a MARTÍN, estás en el faro de Punta Negra. Nivel 4, bombilla apagada. Martín mira al mar.",
    "choices": [
      {
        "index": 1,
        "question": "¿Quieres verlo?",
        "options": {
          "impulsive": "ENCIENDES LA LUZ",
          "stoic": "TE QUEDAS A OSCURAS"
        },
        "consequence_impulsive": "El haz atraviesa la niebla. Algo enorme levanta la cabeza del agua. Martín sonríe. El cristal tiembla. El faro cae. Te aplasta.",
        "consequence_stoic": "Martín asiente. 'Inteligente. Ahora escucha.'",
        "asset_impulsive_video": "assets/scene-light-attack.mp4",
        "asset_stoic_image": "assets/scene-darkness.png"
      },
      {
        "index": 2,
        "question": "Algo rasguña la puerta. ¿Le abres o esperas?",
        "options": {
          "impulsive": "ABRES LA PUERTA",
          "stoic": "ESPERAS"
        },
        "consequence_impulsive": "Algo largo y blanco te abraza. Te lleva al agua. No puedes gritar. El frío te entra por los ojos.",
        "consequence_stoic": "El rasguño para. Martín apaga su linterna. Amanece. Sales del faro. El mar está vacío.",
        "asset_impulsive_video": "assets/scene-door-open.mp4",
        "asset_stoic_image": "assets/scene-dawn.png"
      }
    ],
    "cliffhanger": {
      "action": "tomado té caliente",
      "natural_element": "las estrellas",
      "time_of_day": "amanecer",
      "asset_image": "assets/cliffhanger-tobias-warm.png"
    }
  },
  "audio": {
    "narration_path": "assets/narration.mp3",
    "music_path": "assets/drone-faro.mp3",
    "sfx": {
      "projector": "sfx/projector.wav",
      "riser_choice_1": "sfx/riser-1.wav",
      "riser_choice_2": "sfx/riser-2.wav",
      "twist_impact_1": "sfx/sub-bass-hit-1.wav",
      "twist_impact_2": "sfx/sub-bass-hit-2.wav",
      "glitch_pre_twist": "sfx/glitch.wav"
    }
  }
}
```

---

## CONSTANTES DEL TEMPLATE (no son variables)

Estas son fijas y se aplican igual a TODOS los videos. Hardcodeadas en el generator.

### Timing (en % de duración total)

```javascript
const TIMING = {
  presentation_hold: { start: 0.00, end: 0.17 },
  countdown: { start: 0.17, end: 0.21 },
  warning: { start: 0.21, end: 0.28 },
  scenario_setup: { start: 0.28, end: 0.37 },
  question_1: { start: 0.37, end: 0.40 },
  loading_bar_1: { start: 0.40, end: 0.40 + (2.5 / TOTAL_SECONDS) }, // 2.5s absolutos
  twist_1_consequence: { /* fills until 0.55 */ },
  branch_2_setup: { start: 0.55, end: 0.61 },
  question_2: { start: 0.61, end: 0.65 },
  loading_bar_2: { start: 0.65, end: 0.65 + (2.5 / TOTAL_SECONDS) },
  twist_2_climax: { /* until 0.78 */ },
  resolution: { start: 0.78, end: 0.92 },
  cliffhanger: { start: 0.92, end: 1.00 }
};
```

### Visual constants

```javascript
const VISUAL = {
  font_family: "VCR OSD Mono",
  font_color: "#FFFFFF",
  font_shadow: "2px 2px 0 #000000",
  font_transform: "uppercase",
  font_letter_spacing: "0.05em",
  font_size_name: "60px",
  font_size_caption: "80px",
  caption_position_bottom: "22%",
  
  ken_burns_zoom: { from: 1.0, to: 1.05, ease: "power2.inOut" },
  
  white_flash_frames: 3,
  glitch_pre_cut_frames: 10,
  
  grain_opacity: 0.08,
  vignette_opacity: 0.4,
  chromatic_aberration_offset: 1.5
};
```

### Audio constants

```javascript
const AUDIO = {
  narration_eq: {
    bass_boost: { freq: 100, gain: 4 },
    treble_cut: { freq: 12000, gain: -3 }
  },
  narration_compression: { ratio: 5, threshold: -18, makeup: 6 },
  narration_reverb: { type: "dark_room", decay: 0.5, predelay: 10 },
  
  ducking_amount_db: -6,
  loading_bar_duration_seconds: 2.5,
  
  master_lufs_target: -9.5
};
```

### Tipos de elemento por escena

| Escena | Tipo de asset | Razón |
|--------|---------------|-------|
| Presentación | Imagen estática + Ken Burns + parallax fog | Maximiza tiempo de hook con costo bajo |
| Countdown | Composición HTML/CSS animada | No requiere asset externo |
| Setup escenario | Imagen estática + Ken Burns | Texto narrativo es el foco |
| Twists violentos | Video clip (Kling 1.6) | Movimiento de personaje crítico |
| Resolución/Escape | Video clip o imagen + Ken Burns | Según presupuesto |
| Cliffhanger | Imagen estática + Ken Burns + warm grade | Estatismo refuerza la "paz" |

---

## VARIABLES (slots del usuario)

Solo estos 10 parámetros cambian entre videos:

| Slot | Tipo | Ejemplo | Constraint |
|------|------|---------|------------|
| `bad_apparent.name` | string | "MARTÍN" | 1-2 sílabas, mayúsculas, fácil pronunciación TTS |
| `good_apparent.name` | string | "TOBÍAS" | Idem |
| `bad_apparent.image_prompt` | string | "tall faceless..." | Seguir formato de prompts en `REFERENCE-ANALYSIS.md` |
| `good_apparent.image_prompt` | string | "small translucent..." | Idem |
| `scenario.name` | string | "Faro de Punta Negra" | Específico, con número/nivel cuando aplique |
| `narrative.moral_dilemma_category` | enum | "curiosity_vs_obedience" | De las 5 categorías válidas |
| `narrative.warning_text` | string (5-8 palabras) | "EL FARO LLEVA AÑOS APAGADO" | En presente, declarativo |
| `narrative.choices[*]` | array (2-3 items) | ver schema | Cada elección debe seguir regla de oro |
| `narrative.cliffhanger.action` | string | "tomado té caliente" | Acción de cuidado mutuo |
| `audio.narration_path` | path | "assets/narration.mp3" | Procesada con cadena de filtros AUDIO constants |

---

## PIPELINE DE GENERACIÓN

```bash
# 1. Validar config
node validate-config.js video-config.json
# → verifica que dilema está en categorías válidas, timings cuadran, etc.

# 2. Generar assets faltantes
node generate-assets.js video-config.json
# → corre image.py para imágenes que no existan
# → corre tts.py + audio-postprocess.sh para narración
# → opcionalmente corre video.py (Kling) para clips animados

# 3. Compilar HTML
node compile-template.js video-config.json
# → genera index.html con sub-compositions
# → calcula timings basados en duration_seconds + porcentajes fijos
# → inserta paths de assets

# 4. Lint y validate
npx hyperframes lint
npx hyperframes validate

# 5. Render
npx hyperframes render -q standard -o output/video-001.mp4

# 6. Audio post-pro final (mastering, ducking, LUFS)
ffmpeg -i output/video-001.mp4 -af "..." output/video-001-master.mp4
```

---

## ESTRUCTURA DE ARCHIVOS DEL TEMPLATE

```
template/
├── compile-template.js          # Orquestador
├── generate-assets.js
├── validate-config.js
├── lib/
│   ├── timing.js                 # Cálculos de % a segundos
│   ├── audio-postprocess.js      # Cadena de filtros narración
│   └── prompts/
│       ├── image-prompt.template # Template para Gemini
│       └── narration.template    # Template TTS pre-procesado
├── compositions/
│   ├── master.html.template      # Composición raíz con todos los slots
│   ├── presentation.html         # Sub-comp de presentación
│   ├── countdown.html            # Sub-comp del 3-2-1
│   ├── loading-bar.html          # Sub-comp interactiva
│   ├── twist-impact.html         # Sub-comp con white flash + glitch
│   └── cliffhanger.html          # Sub-comp warm
├── assets-shared/
│   ├── fonts/VCR_OSD_MONO.ttf
│   ├── overlays/grain-loop.mp4
│   ├── overlays/vignette.png
│   └── sfx/                      # SFX que son constantes (proyector, etc.)
└── examples/
    └── video-001-config.json     # Ejemplo lleno
```

---

## VALIDACIONES OBLIGATORIAS DEL CONFIG

`validate-config.js` debe rechazar:

- ❌ Duración fuera del rango 80-110 segundos
- ❌ Menos de 2 o más de 3 elecciones interactivas
- ❌ Categoría de dilema fuera de las 5 válidas
- ❌ Cliffhanger sin elemento sensorial cálido
- ❌ Nombres con tildes/eñes que conflictúen con TTS
- ❌ Image prompts genéricos (sin specs técnicos)
- ❌ Audio narration sin procesamiento (sin EQ + compresión + reverb aplicados)

---

## TODO LIST PARA PHASE 4

Cuando se llegue al punto de implementar este template:

- [ ] Implementar `validate-config.js` con todas las reglas de arriba
- [ ] Crear las 6 sub-compositions HTML reusables
- [ ] Escribir `audio-postprocess.sh` con la cadena ffmpeg de EQ + compresión + reverb + ducking
- [ ] Construir `compile-template.js` que tome el config y produzca HTML compilado
- [ ] Crear 3 ejemplos llenos de `video-config.json` (uno por tipo de escenario probado)
- [ ] Documentar cómo agregar un nuevo escenario al template
- [ ] Setup de CI: cada nuevo config debe pasar lint + validate antes de render
