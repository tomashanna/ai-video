# formats/youtube-long.md — YouTube Long-form

> Delivery format horizontal de YouTube. Retention curva totalmente distinta a short-form. Reglas heredadas se invierten en varios puntos.

---

## Specs técnicos

| Atributo | Valor |
|---|---|
| Aspect ratio | 16:9 |
| Resolución | 1920 × 1080 (FHD) o 3840 × 2160 (4K) |
| FPS | 24, 30, o 60 (depende del contenido) |
| Codec video | H.264 High profile o H.265 HEVC (4K) |
| Codec audio | AAC-LC stereo o 5.1 surround, 48000Hz |
| Bitrate video | 8-15 Mbps FHD, 35-45 Mbps 4K |
| Duración | 3-30min (sweet spot 8-15min para algoritmo) |
| Tamaño máx | 256 GB técnicamente |
| Container | MP4 |

---

## Reglas heredadas

### 🌐 Universal (TODAS aplican)
- `CAPTIONS.md` § Whisper-sync — sound-off viewers existen en YT (segundo monitor, biblioteca, etc.)
- `ELEMENTS-LIBRARY.md` § Drop shadow — texto sobre fondos variables
- `PIPELINE.md` § Preset filter — cada genre define su look
- `CHARACTER-CONSISTENCY.md` — anchors si hay personajes recurrentes

### 📱 Vertical short-form — **NO HEREDAR**
- ❌ `RETENTION-RULES.md` (completa) — retention dynamics distintas
- ❌ "Cero estáticas primeros 30s" — un long-form de 15min puede tener 3min de B-roll con motion sutil sin problema
- ❌ "Intro ≤10%" — un long-form de 15min con 90s de intro está OK

### 🖥️ Long-form (todas aplican — ver "Específico Long-form")

### 🎬 Format-specific
Ver sección abajo.

---

## Específico Long-form

### Retention curva distinta
**Scope**: 🖥️ Long-form

| Métrica | Short-form (Reels) | Long-form (YT) |
|---|---|---|
| Decision moment crítico | Segundos 1-3 | **Segundos 15-30** (skip ahead button) |
| Drop-off acelerado | 0-10s | 30s-2min |
| Re-watch frequency | Alta (loop auto) | Baja (≤1 viewing) |
| Caption importance | Crítica | Importante pero no crítica |
| Hook agresividad | Máxima | Moderada (público vino a YT explícitamente) |

### Estructura macro
**Scope**: 🖥️

```
0-15s     COLD OPEN / TEASER       (hook visual + audio + tease de payoff)
15-30s    INTRO + branding         (canal name, tema, value prop)
30s-mid   CONTENT BLOCKS           (3-5 blocks, cada uno con mini-payoff)
~80%      CLIMAX / KEY REVEAL      (el punto principal del video)
~90%      WRAP UP                  (recap + lesson learned)
~95-100%  CTA + OUTRO              (suscribe, próximo video, end screen)
```

### Chapter markers
**Scope**: 🖥️

YT permite chapter markers en la descripción. Para videos >5min, SIEMPRE incluir:

```
00:00 - Cold open
00:30 - Intro
01:45 - Block 1: [Title]
04:20 - Block 2: [Title]
...
```

Beneficios:
- Aumenta retention (viewers saltan al chapter que les interesa, pero terminan viendo más)
- SEO benefit (chapters indexan en search)
- Mejor UX en mobile (chips de chapters)

### Hook diferenciado del intro
**Scope**: 🖥️

Cold open (0-15s) y intro (15-30s) son **dos cosas distintas**:

- **Cold open**: prueba directa del payoff. Mostrar el momento más impactante PRIMERO, sin contexto.
- **Intro**: branding + setup del contexto. Acá va el "hola, soy X" si aplica.

**Anti-pattern**: empezar con "hola bienvenidos a mi canal" (intro) sin cold open → 50% bounce instantáneo.

### B-roll y voice-over
**Scope**: 🖥️

Mucho más uso de B-roll (imagen secundaria sobre voice-over) que en short-form. Reglas:
- B-roll cada 4-8s mínimo para mantener engagement visual
- B-roll debe ILUSTRAR lo que dice la voz (no ser decorativo random)
- Mix volumes: voice 1.0, ambient/music 0.10-0.15 (más bajo que short-form porque el viewer está enfocado)

### End screen (últimos 20s)
**Scope**: 🖥️ YT específicamente

YT permite end screens con:
- Suggest next video (autoplay candidate)
- Suggest playlist
- Subscribe button
- Channel link

Diseñar el video con los **últimos 20s pensados para end screen**:
- No información crítica en esos 20s (van a estar tapados)
- Visual atrás puede ser un loop o still atmospheric
- Audio outro a volumen bajo

### Captions: auto + burned-in selectivos
**Scope**: 🖥️

- YT auto-captions son aceptables (mejorar errores manualmente en YT Studio)
- Burned-in solo para EMPHASIS (key quotes, stats, names) — NO toda la narración
- Si el video se va a republicar en otras plataformas → considerar burned-in completo

---

## UI Safe zones — YouTube

```css
/* Para overlay text/elements en long-form */
.title-card {
  top: 80px;        /* debajo de search bar / mini player */
  left: 60px;
}
.lower-third {
  bottom: 120px;    /* arriba de progress bar + controls (cuando visibles) */
  left: 60px;
}
.end-screen-zone {
  /* últimos 20s — espacio para suggest cards */
  /* dejar bottom-right 600×340px libre para end screen elements */
}
```

---

## Anti-patterns específicos Long-form

### ❌ Aplicar PRE-GATE "cero estáticas primeros 30s"

**Por qué falla**: incompatible con long-form. Un cold open puede tener un cinemático estático con voice-over emocional.

**Fix**: ignorar PRE-GATE de short-form. Long-form puede usar motion CSS o Kling según narrativa, no por regla de retención.

### ❌ Intro de 2-3s sin establecer contexto

**Por qué falla**: viewer de YT vino con intención (search/recommendation). Cold open ultra-corto se siente clickbait.

**Fix**: cold open 8-15s con teaser de payoff. Intro 15-30s con setup.

### ❌ Render vertical 9:16 forzado a 16:9 con padding

**Por qué falla**: bandas negras laterales son señal de "video reutilizado de TikTok", el algoritmo de YT penaliza.

**Fix**: render nativo 16:9. Si la fuente es 9:16, re-componer (no padding).

### ❌ Caption-wrap en mismo lugar que short-form (bottom: 540px de 1920)

**Por qué falla**: en 16:9 1920×1080, "bottom: 540px" estaría fuera del frame. Coordenadas son distintas.

**Fix**: usar `lower-third` style — `bottom: 120px` para un canvas 1920×1080.

---

## QA específico Long-form

```
Dimensiones específicas YouTube Long:
- ¿Cold open en primeros 15s muestra el payoff sin spoiler completo?
- ¿Intro 15-30s establece contexto y branding?
- ¿Hay chapter markers cada 90-180s en la descripción?
- ¿Los últimos 20s están diseñados para end screen?
- ¿B-roll varía cada 4-8s mínimo?
- ¿CTA suggest next video / suscribe está al final?
- ¿Captions burned-in solo en emphasis (quotes/stats) o toda la narración?
```

---

## Casos producidos

(ninguno aún)

---

## Cross-references

- `DELIVERY-FORMATS.md` — catálogo padre
- `formats/reel.md` — comparar diferencias short vs long
- `formats/b2b-commercial.md` — formato hermano horizontal con reglas distintas
