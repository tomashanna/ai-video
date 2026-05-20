# DELIVERY-FORMATS.md — Catálogo de formatos de entrega

> Todo proyecto de video se define por DOS ejes ortogonales:
> - **GENRE / TEMA**: qué cuenta el video (horror-choice, tutorial, testimonial, brand-story, etc.)
> - **DELIVERY FORMAT**: cómo se entrega (reel, youtube-short, youtube-long, b2b-commercial, instagram-story, libre)
>
> Este doc es el catálogo del segundo eje. Cada delivery format vive en `formats/<nombre>.md` y define las reglas técnicas que NO dependen de qué cuenta el video.

---

## Convención de scope tags

Toda regla en `ai-video-production/` o sub-skills debe llevar un scope tag explícito:

| Tag | Significa | Ejemplo |
|---|---|---|
| 🌐 **Universal** | Aplica a CUALQUIER video, cualquier formato, cualquier duración | "Toda narración requiere Whisper-sync caption" |
| 📱 **Vertical short-form** | Aplica solo a Reels / TikTok / IG Stories / YT Shorts (≤2min, 9:16, mobile) | "Hook en primeros 2-3s" |
| 🖥️ **Long-form** | Aplica solo a YouTube long / web content (>2min, 16:9) | "Chapter markers cada 90s" |
| 🏢 **B2B / Corporativo** | Aplica solo a contenido profesional / sales / LinkedIn | "Logo + lower-third en cada plano" |
| 🎬 **Format-specific** | Aplica solo a un genre o delivery específico | "H1-H6 estructura horror-choice" |

Cuando una doc cubre reglas mixtas, cada sección lleva su propio scope tag.

---

## Catálogo de delivery formats

| Format | Doc | Aspect | Duración | Plataformas |
|---|---|---|---|---|
| **Reel** | [`formats/reel.md`](formats/reel.md) | 9:16 1080×1920 | 30-90s | Instagram Reels, TikTok, IG Reels |
| **YouTube Short** | [`formats/youtube-short.md`](formats/youtube-short.md) | 9:16 1080×1920 | ≤60s | YouTube Shorts |
| **YouTube Long** | [`formats/youtube-long.md`](formats/youtube-long.md) | 16:9 1920×1080 | 3-30min | YouTube long-form |
| **B2B Commercial** | [`formats/b2b-commercial.md`](formats/b2b-commercial.md) | 16:9 o 1:1 | 30s-2min | LinkedIn, web, sales decks, email |
| **Instagram Story** | [`formats/instagram-story.md`](formats/instagram-story.md) | 9:16 1080×1920 | ≤15s/segmento | Instagram Stories |
| **Libre** | [`formats/libre.md`](formats/libre.md) | Parametrizable | Parametrizable | Custom one-off |

---

## Matriz GENRE × DELIVERY FORMAT

Cada celda representa un combo válido. ⭐ marca proyectos ya producidos.

| GENRE \ FORMAT | Reel | YT Short | YT Long | B2B | IG Story | Libre |
|---|---|---|---|---|---|---|
| **horror-choice** | ⭐ v15 final | ✓ apto | ✗ no fit | ✗ no fit | ✓ apto (mini) | ✓ |
| **tutorial** (futuro) | ✓ corto | ✓ | ✓ profundo | ✓ explainer | ✓ | ✓ |
| **testimonial** (futuro) | ✓ teaser | ✓ | ✓ historia completa | ⭐ customer story | ✗ | ✓ |
| **brand-story** (futuro) | ✓ | ✓ | ✓ documental | ⭐ B2B | ✓ | ✓ |
| **comedy/sketch** (futuro) | ✓ | ✓ | ✗ different rules | ✗ no fit | ✓ | ✓ |
| **news/breaking** (futuro) | ✓ | ✓ | ✗ different rules | ✗ no fit | ✓ | ✓ |

---

## Cómo combinar GENRE + DELIVERY al iniciar proyecto

```bash
# Al hacer bootstrap, declarar ambos ejes:
"Bootstrap video: 
  genre   = horror-choice
  format  = reel
  setting = mina abandonada"
```

El agente entonces lee 3 capas de skills en orden:

1. **`ai-video-production/SKILL.md`** + reglas universales (CAPTIONS, ELEMENTS-LIBRARY, PIPELINE, etc.)
2. **`formats/<delivery>.md`** — reglas técnicas del delivery (specs, retention, UI safe zones)
3. **`<genre>-format/SKILL.md`** — reglas narrativas del genre (estructura, beats, personajes)

Combina los 3 y produce el `index.html` + assets.

---

## Reglas por inheritance

Cada delivery format declara qué reglas universales **hereda** y qué reglas heredadas **overridea**:

```markdown
## Heredance (en cada formats/X.md)

### Hereda 🌐 Universal:
- CAPTIONS.md § Whisper-sync hard rule
- ELEMENTS-LIBRARY.md § Drop shadow text legibility
- PIPELINE.md § Preset filter principle
- CHARACTER-CONSISTENCY.md § Bootstrap gate

### Hereda 📱 Vertical short-form (si aplica):
- RETENTION-RULES.md (completa)
- ANIMATION-LAYER.md § PRE-GATE cero estáticas

### Específico de este delivery:
- (rules unique to this format)

### Override (si difiere de un default heredado):
- (excepciones explícitas)
```

---

## Cuándo agregar un nuevo delivery format

Crear `formats/X.md` solo si:
- ✅ El delivery es **estructuralmente distinto** (aspect, duration range, platform UI) — no solo "otro video corto"
- ✅ Va a producir **≥3 proyectos** en el futuro (sino mejor usar `libre.md`)
- ✅ Tiene reglas técnicas que **no caben** en un format existente

Ejemplos válidos para agregar en futuro:
- `formats/podcast-clip.md` (1:1 o 9:16, 60-90s, podcast cuts con audiograma)
- `formats/connected-tv.md` (16:9 4K, 15-30s, CTV/Smart TV ads)
- `formats/twitter-x-native.md` (1:1 16:9, ≤2:20min, autoplay muted)

Ejemplos NO válidos (usar `libre.md`):
- One-off custom para un cliente
- Test de formato experimental

---

## Estado actual (2026-05-11)

- Catálogo: 6 formats canónicos definidos
- Proyectos producidos: 1 combo (horror-choice × reel — mina-abandonada v15-final 9.9/10)
- Próximo formato genre a definir: TBD (tutorial, testimonial, o brand-story según prioridad de negocio)

---

## Cross-references

- `SKILL.md` § Documentos — link a este catálogo
- `BOOTSTRAP.md` — paso 0 declara genre + format
- `QA.md` — el prompt Gemini debe adaptarse al delivery format
- Cada `formats/X.md` — detalle de un format específico
