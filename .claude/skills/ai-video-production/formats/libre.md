# formats/libre.md — Custom / Parametrizable

> Delivery format **NO canónico**. Plantilla parametrizable para proyectos one-off o experimentales que no caben en los formats existentes.

---

## Cuándo usar `libre`

✅ **Usar libre cuando**:
- One-off para un cliente específico con specs únicos
- Test de un formato nuevo antes de canonicalizarlo
- Combinación de requirements que no matchean ningún format existente
- Proyecto experimental (educacional, art piece, NFT video, etc.)

❌ **NO usar libre cuando**:
- El proyecto encaja en `reel.md`, `youtube-short.md`, `youtube-long.md`, `b2b-commercial.md`, o `instagram-story.md` → usar el format específico
- Vas a producir ≥3 proyectos con specs similares → **canonicalizar** creando un nuevo format en lugar de usar libre múltiples veces

---

## Parámetros que define el proyecto

Al iniciar un proyecto `libre`, declarar TODOS los siguientes en el bootstrap:

```yaml
# libre-config.yaml (sugerido en project root)

delivery:
  aspect_ratio: "16:9"          # 9:16 | 16:9 | 1:1 | 4:5 | custom
  resolution: "1920x1080"        # cualquier resolución técnicamente válida
  fps: 30                        # 24 | 30 | 60 | 120
  duration_seconds: 45           # cualquier duración
  max_file_size_mb: 50           # depende de destination

codecs:
  video: "h264_high_l40_yuv420p" # default
  audio: "aac_lc_48khz_stereo"   # default

destination:
  platform: "linkedin_feed"      # str descriptiva, NO impacta render
  ui_safe_zones:                 # define manualmente según destination
    top: 80
    bottom: 120
    left: 60
    right: 60

retention_strategy:
  is_short_form: true            # determina si hereda RETENTION-RULES.md
  hook_max_seconds: 3            # según platform
  intro_max_percent: 10          # según platform

audio_strategy:
  sound_off_default: true        # determina si Whisper captions son CRÍTICO
  music_licensing: "epidemic_sound" # source explícito

branding:
  color_grade_preset: "naturalista" # name of preset
  filter_css: "contrast(1.05) saturate(0.95) brightness(1.0)"
  font_family: "Inter, sans-serif"

genre:
  primary: "testimonial"         # genre principal
  subgenre: null                 # opcional

constraints:
  must_include:
    - "client logo at 00:00-00:03"
    - "URL at end"
  must_avoid:
    - "horror filter"
    - "AI-generated faces"
```

---

## Reglas heredadas

`libre.md` no hereda reglas por default. Las hereda **explícitamente** según los parámetros declarados:

| Parámetro libre | Hereda |
|---|---|
| `is_short_form: true` | `RETENTION-RULES.md` (completa) |
| `sound_off_default: true` | `CAPTIONS.md` § Whisper hard rule (universal pero crítico) |
| `aspect_ratio: 9:16` | `formats/reel.md` § UI safe zones (referencia) |
| `aspect_ratio: 16:9, duration > 180s` | `formats/youtube-long.md` § B-roll patterns |
| (always) | `ELEMENTS-LIBRARY.md`, `CHARACTER-CONSISTENCY.md`, `ANIMATION-LAYER.md` |

---

## Workflow al iniciar proyecto `libre`

### Paso 1: declarar params
Crear `libre-config.yaml` con todos los parámetros del proyecto.

### Paso 2: identificar herencia
Para cada param, listar qué doc hereda. Ejemplo:
```
is_short_form: true → hereda RETENTION-RULES.md
sound_off_default: true → hereda CAPTIONS.md § Whisper
duration_seconds: 45 → cap intro a 4.5s
aspect_ratio: 16:9 → cap zone bottom 80px
```

### Paso 3: definir genre
Si el genre matchea un skill existente (horror-choice, futuro tutorial, etc.) → herda sus reglas narrativas.
Si no, declarar reglas custom inline en el proyecto.

### Paso 4: bootstrap como any otro proyecto
```bash
mkdir -p mi-proyecto-libre/{assets,scripts,renders}
# copy templates de ai-video-production/templates/
# editar libre-config.yaml
```

### Paso 5: QA adaptado
El prompt Gemini debe incluir las reglas heredadas + las custom del proyecto.

---

## Cuándo canonicalizar (convertir libre en format propio)

Si producís ≥3 proyectos libres con specs SIMILARES, es momento de canonicalizar:

1. Identificar el patrón común
2. Crear `formats/<nuevo-format>.md` con esas specs
3. Migrar proyectos pasados (referenciar)
4. Actualizar `DELIVERY-FORMATS.md` catálogo

Ejemplo: si haces 3 podcast clips con specs idénticos (1:1, 60-90s, audiograma) → canonicalizar como `formats/podcast-clip.md`.

---

## Anti-patterns específicos libre

### ❌ Usar libre para "evitar" elegir un format específico

**Por qué falla**: si el proyecto encaja en reel/youtube-short/etc., usar el format específico te da reglas heredadas automáticamente. libre te obliga a declararlas manualmente.

**Fix**: confirmar primero si encaja en formats existentes. Solo usar libre si NO encaja.

### ❌ Usar libre sin declarar `libre-config.yaml`

**Por qué falla**: sin params declarados, el agente no sabe qué reglas heredar. Cualquier decisión se vuelve ad-hoc.

**Fix**: SIEMPRE crear `libre-config.yaml` con todos los params en el bootstrap.

### ❌ Usar libre múltiples veces con specs idénticos

**Por qué falla**: estás reinventando rules cada vez. Si pasa 3+ veces, debería ser un format canónico.

**Fix**: ver "Cuándo canonicalizar" arriba.

---

## QA específico libre

```
Dimensiones específicas libre:
- ¿libre-config.yaml está completo y todos los params declarados?
- ¿Las reglas heredadas son consistentes con los params (ej: is_short_form=true → ¿se aplicó PRE-GATE)?
- ¿El render matchea exactamente el aspect/duration/codec declarados?
- ¿Las constraints `must_include` y `must_avoid` se respetan?
- ¿Si este es el 3er proyecto libre con specs similares, hay un plan de canonicalización?
```

---

## Casos producidos

(ninguno aún — libre por definición es ad-hoc)

---

## Cross-references

- `DELIVERY-FORMATS.md` — catálogo padre
- Todos los `formats/*.md` — para referenciar cuando un libre converge
