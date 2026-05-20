# BRAND.md — Brand de la cuenta IG horror-choice

> Define audience, voz del contenido, paleta visual, hashtags y reglas operativas DE LA CUENTA específica. **No de Toby** (eso está en `video-director/META-BRAND.md`). Es la identidad del canal de Instagram horror.

**Estado**: exploratorio. Muchas decisiones diferidas hasta validar con primera publicación + métricas.

---

## 1. Posicionamiento del canal

**Cuenta de Instagram con horror narrativo interactivo, formato "Elige a tu compañero" estilo `@referent-a`.**

- **Categoría**: Entertainment / Horror narrativo
- **Frecuencia target**: 2-3 reels/semana (mínimo para mantener viva la cuenta en el algoritmo)
- **Idioma**: Español neutro
- **Duración por reel**: 75-100s (formato vertical 1080×1920)

---

## 2. Audience persona

| Atributo | Definición |
|---|---|
| **Edad** | 18-30 (predominante), 30-40 (secundaria) |
| **Comportamiento** | Scrollers nocturnos, consumidores de horror narrativo, fans de creepypastas, leyendas urbanas |
| **Plataformas** | IG Reels principal, también TikTok (consumo cruzado) |
| **Triggers emocionales** | FOMO ("¿qué hubiera pasado si...?"), curiosidad mórbida, decisiones imposibles |
| **Behaviors clave** | Comentan respuestas a CTAs, taguean amigos, guardan para volver a ver |
| **Referentes culturales** | `@referent-a`, Black Mirror, Bandersnatch, creepypastas YouTube |

**Lo que les engancha**:
- Body horror específico (no genérico)
- Dilemas morales sin respuesta correcta obvia
- Twists que cambian la interpretación retrospectivamente
- Atmósfera vs jumpscares

**Lo que NO funciona**:
- Comedy puro
- Aspiracional / glamoroso
- Tutorial / educativo directo

---

## 3. Voz del contenido (la del narrador/personaje, NO la de Toby)

> Esta es la voz dentro de los videos. La voz de Toby en su perfil personal es otra (ver `META-BRAND.md`).

**Tono del narrador**:
- Frío, omnisciente, sin emoción explícita
- Habla en segunda persona implícita ("trabajas", "miras", "eliges")
- Frases cortas, nominales sin verbo ("Luz fría, pasillo vacío.")
- Promedio 5.4 palabras por oración
- 45% de las frases tienen 1-3 palabras

**Voice ID canónico**: `Tj9l48J9AJbry5yCP5eW` (con atempo 2.0)

**Vocabulario**:
- Body horror específico, NO "mueres"
- Imperativos crípticos ("No los mires a los ojos")
- Presente del indicativo SIEMPRE en consecuencias

Detalle completo en `SCRIPT-WRITING-GUIDE.md` y `PATTERNS.md`.

---

## 4. Visual identity (paleta + tipografía + filter)

### ⭐ Preset CSS filter canónico — "horror-deep" (validado v15)

**Scope**: 🎬 horror-choice format específicamente. Aplicar a TODOS los `.scene-image` del video.

```css
.scene-image {
  filter: contrast(1.28) saturate(0.35) brightness(0.74);
}
```

Estos son los valores canónicos validados en mina-abandonada v15-final (9.9/10 Gemini). NO modificar sin justificación documentada.

**Por qué estos valores específicos**:
- `contrast(1.28)`: realza la separación entre subjects oscuros (Hugo) y backgrounds (tunnel) sin "quemar" highlights
- `saturate(0.35)`: desatura para look lúgubre + integra IA-images con paletas distintas (Hugo gaunt vs Santi clean blue)
- `brightness(0.74)`: oscurece para mood horror sin perder detalle en sombras

**Override por escena**:
- ✅ Cliffhanger H6 con clase `.h6-img`: `filter: none` para activar warm tint (rama cálida)
- ❌ NO override en H1-H5 sin razón narrativa clara

**Variante alternativa — "horror-claustrofóbico"**:
```css
.scene-image.deep-horror {
  filter: contrast(1.35) saturate(0.25) brightness(0.65);
}
```
Para sub-genre más oscuro / cuevas / espacios cerrados. NO probado todavía — usar con cuidado.

**Meta-rule referencia**: `ai-video-production/PIPELINE.md` § 2 "Meta-regla universal: cada formato define su preset CSS filter canónico"

### Paleta dominante

| Categoría | Color | Uso |
|---|---|---|
| Background | `#000000` puro / muy oscuro | Base |
| Foreground texto | `#ffffff` con stroke negro 2px | Captions principales |
| Color grade horror | filter horror-deep (ver arriba) | H1-H5 (rama horror) |
| Color grade cliffhanger | Cálido amarillo-naranja (warm-tint overlay) | H6 (rama "buena hipotética") |
| Acento cliffhanger | `#f0e040` (amarillo cálido) | CTA final, "¿qué hubieras elegido?" |
| Puente narrativo | `#f5d9a0` (dorado tenue) | "Y SI HUBIERAS ELEGIDO A..." |
| Bridge separador A→B | `#c8d8ff` (azul claro) | "SI [opción B]:" |

### Tipografía

| Uso | Font | Size | Stroke |
|---|---|---|---|
| Captions principales | Anton / Bebas Neue | 80px (68px si frase >8 palabras) | 2px |
| Choice labels A/B | Anton | 64px | 2px |
| Name labels HUGO/SANTI | Anton | 72px | 2.5px |
| Countdown | Anton | 400px | 4px |
| Caption Hugo whisper (italic) | Anton italic | 64px color #d8d8d8 | 1.5px |
| Lower thirds | Variable según elemento (ver elements.json) | Variable | – |

**Drop shadow obligatorio en todos los textos**: ver receta canónica universal en `ai-video-production/ELEMENTS-LIBRARY.md` § "Receta universal — Drop shadow para texto sobre IA-generated images". 4 strokes diagonales + drop shadow + glow envelope.

---

## 5. Copy + hashtags

### Caption del post (template)

```
¿Elegiste al compañero correcto?

[Línea hook reformulando la pregunta del video]

A o B? Comenta abajo 👇

#horror #elegirtucamino #aivideo #horrorenespañol #creepystories #darkstories
```

### Hashtags fijos por video (5-10)

| Hashtag | Razón |
|---|---|
| `#horror` | Categoría primaria |
| `#elegirtucamino` | Tag de marca del formato (consistente entre videos) |
| `#aivideo` | Discovery por AI creators / curiosos |
| `#horrorenespañol` | Idioma + género |
| `#creepystories` | Cross-discovery con creepypasta community |
| `#darkstories` | Cross-discovery |
| `#instahorror` | IG-native horror tag |
| `#cuentos` | Para audiencia latam |
| `#viralhorror` | (Bajo prioridad pero amplio) |

### Hashtags variables (3-5 por video según contenido)

- Escenario: `#bosque`, `#mina`, `#hospitalabandonado`, `#fabrica`, `#metro`, etc.
- Mood: `#fantasma`, `#monstruo`, `#aliens` según corresponda
- Specific: si hay tag emergente del trending, agregarlo (cuidando no diluir el feed)

### CTA narrado final (texto de voz)

Template variable:
> "Y tú... ¿qué habrías elegido? Comenta A o B abajo, y dinos por qué."

Variantes para evitar repetición:
- "¿Cuál habrías elegido tú? Comentá y decime tu razón."
- "A o B — ¿cuál elegís? Comentá abajo."
- "¿Sobreviviste? Comentá A o B y por qué."

---

## 6. Frequency floor + posting strategy

**Mínimo**: 2 reels/semana. Bajo eso, IG penaliza la cuenta.
**Ideal**: 3 reels/semana al alcanzar 5K followers.
**Maximum**: 5 reels/semana (saturas tu propia audiencia).

**Mejor horario** (estimado, ajustar con data real):
- Martes 20:00-22:00 (peak engagement horror audience)
- Jueves 21:00-23:00
- Domingo 20:00-22:00

**Variación de archetype**: cada video DEBE usar archetype diferente al anterior (ver `PAUTA-MASTER.md` § 13 + `video-log.md`).

---

## 7. Cross-link con Toby (META-BRAND)

⚠️ **DIFERIDO**: hasta tener handle personal definido.

Una vez decidido, esta cuenta:
- Linkea en bio a perfil personal de Toby
- Menciona "@toby<handle>" en algún highlight (NO en todos los videos — soft-touch)
- Hashtag de marca personal (definir) en cada caption del post

---

## 8. Reglas operativas

### Lo que SIEMPRE hacés en esta cuenta
- ✅ Aplicar quality bar ≥9.7 Gemini (per `video-director/SKILL.md`)
- ✅ Rotar archetype de cliffhanger
- ✅ Captions safe zone IG
- ✅ Disclosure honesto que es AI-generated (puede ser sutil en algún highlight o bio)
- ✅ Capturar performance T+48h después de cada post

### Lo que NUNCA hacés en esta cuenta
- ❌ Repetir mismo archetype dos videos seguidos
- ❌ Reciclar mismo monstruo ("malo aparente") entre videos (que sea siempre uno nuevo)
- ❌ Comprar followers / engagement
- ❌ Esconder que es AI-generated
- ❌ Publicar contenido off-format (la cuenta es horror-choice 100%)
- ❌ Bajar quality bar por velocidad

---

## 9. Métricas de éxito de la cuenta

### Validación (primeros 3 meses)

| Métrica | Target |
|---|---|
| Followers | 1K en 3 meses (orgánico) |
| Avg views por reel | 5K |
| Avg completion rate | 60%+ |
| Saves rate | 5%+ de views (alto para horror) |
| Engagement rate | 7%+ (likes + comments + saves / views) |

### Escala (6-12 meses)

| Métrica | Target |
|---|---|
| Followers | 10K |
| Avg views | 20K+ |
| Inbound DMs preguntando "cómo lo hacés" | 30+ (señal de demand offer Toby) |
| Cross-reference a perfil personal | Detectable en analytics |

Trigger para Fase 2 de META-BRAND (monetización): cuenta llega a 10K + 30 inbounds.

---

## 10. Decisiones diferidas

| Decisión | Status | Criterio para resolver |
|---|---|---|
| **Handle de la cuenta IG** | DIFERIDA | Antes de primer post |
| **Foto de perfil** | DIFERIDA | Antes de primer post |
| **Bio del perfil** | DIFERIDA | Antes de primer post (debe linkear a Toby personal) |
| **Highlights iniciales** | DIFERIDA | Después de primeros 5 reels |
| **Disclosure AI explícito** | DIFERIDA | Decidir sutileza vs explicit (depende de IG policy update 2026) |
| **¿Spinoffs / series internas?** | DIFERIDA | Después de 20+ videos producidos |
| **Cross-posting a TikTok** | DIFERIDA | Una vez IG validado, replicar TikTok como secondary |

---

## 11. Cómo usa este doc el video-director

Cuando producís un video para esta cuenta:

1. Antes de generar assets: chequear voz, paleta, tipografía acá.
2. Antes de escribir captions del post: usar template de § 5.
3. Antes de publicar: validar contra § 8 (lo que SÍ / NO se hace en esta cuenta).
4. Después de publicar: capturar performance per § 9 + actualizar `video-log.md`.

---

## Última actualización

2026-05-10. Inicial. Brand de la cuenta IG horror-choice (handle pendiente). Refleja decisiones tomadas + decisiones diferidas con criterios de resolución.
