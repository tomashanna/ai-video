# ANIMATION-LAYER.md — Replicate Kling para animar imágenes estáticas

> Última capa del pipeline antes del render final. Pasamos de imágenes generadas + GSAP motion → clips de video animados con Replicate Kling. Es la diferencia entre "Ken Burns sobre foto" y "escena viva". También es la fase más cara y la que más errores genera si no se planifica.

---

## Por qué importa

Una imagen estática con Ken Burns es buena. Una imagen animada con Kling es **cinemática**. Pero:
- Kling es caro (~$0.07/s, total $5-9 por video)
- Kling falla aleatoriamente (~15-20% de generaciones)
- Errores de timing (duration mismatch) producen frames congelados o loops visibles que arruinan engagement

Esta doc cubre cómo NO meter la pata en la fase final.

---

## 1. CUÁNDO ANIMAR vs DEJAR ESTÁTICO (decision tree)

### ⛔ PRE-GATE: regla de retención de los primeros 30s

**Scope**: 📱 **Vertical short-form ÚNICAMENTE** (Reels / TikTok / IG Reels / YouTube Shorts, ≤2min, 9:16). NO aplica a YouTube long-form, B2B horizontal commercial, ni cualquier delivery con retention curve distinta. Para detalle del scope ver `ai-video-production/RETENTION-RULES.md`.

**Regla**: Toda escena con `data-start < 30s` DEBE ser un clip Kling. Sin excepciones (en short-form).

| Condición | Acción |
|---|---|
| `data-start < 30s` | **Animar con Kling SIEMPRE** — wide, close-up, detail, lo que sea. Ni Ken Burns ni estática son aceptables. |
| `data-start ≥ 30s` | Aplicar decision tree normal (tabla abajo). |

**Por qué:** retención del espectador en los primeros 30s es crítica. Cualquier frame congelado o motion sutil tipo Ken Burns en esa ventana baja la curva de retención. Es la diferencia entre un Reel que termina en >70% retention vs <40%.

**Cómo se mide:** se mira el `data-start` del clip en el HTML. Si entra antes de t=30, animado. Si entra a partir de t=30.000, decision tree normal aplica. La duración de la escena no importa para esta regla — solo el momento de entrada.

**Implicación de costo:** si en los primeros 30s tenés 3-4 wide establishing shots que antes pensabas dejar Ken Burns, ahora son Kling. **+$1-2/video** sobre el budget base.

**Implicación operativa al planear shot list:** las primeras 4-5 imágenes del NARRATIVE.md ya quedan flagged como "Kling obligatorio" independiente del tipo de plano. Diseñalas para ser animables (un movimiento principal claro, sin texto pegado que rompa con micro-drift).

### Decision tree normal (aplica solo si `data-start ≥ 30s`)

| Tipo de plano | Animar con Kling | Solo Ken Burns |
|---|---|---|
| Close-up rostro con expresión clave | ✅ | – |
| Twist / consecuencia / impacto | ✅ | – |
| Cliffhanger / hero shot | ✅ | – |
| Plano con elementos vivos (humo, fuego, agua, partículas) | ✅ | – |
| Personaje haciendo gesto narrativamente importante | ✅ (con cuidado) | – |
| **Wide establishing shot** del escenario | – | ✅ |
| **Detail shot** de objeto (herramienta, cuaderno, libro) | – | ✅ |
| **POV ground / fallen** estático intencional | – | ✅ |
| **Plano del cliffhanger cálido** (cabaña, café) | A veces | ✅ default |
| Loading bar background | – | ✅ |

**Regla operativa**: animá 8-10 imágenes de las 15-20 típicas. El resto Ken Burns + variantes -a/-b/-c es suficiente. **Ajustá hacia arriba si la regla de los 30s mete más Kling al budget.**

**Costo orientativo**: 8-10 clips × tier 5s o 10s × $0.07/s + 1.5× retries = **$5-9 por video** (puede subir a $6-11 si la regla de los 30s fuerza Kling extra).

### ⭐ Cantidad óptima de imágenes (aprendizaje 2026-05-11 — mina-abandonada v8)

**Target ideal para Reels ~90-100s: 12-15 imágenes totales, NO 18-23.**

| Cantidad total | Promedio por imagen | Implicación |
|---|---|---|
| 23 imágenes | ~4.3s | Fragmentado. La mitad queda <3s = no-animable con Kling = filler Ken Burns. |
| **12-15 imágenes** ⭐ | **~6.7-8s** | **Cada imagen aguanta tier 5s o 10s. 10-12 animables sin esfuerzo.** |
| <10 imágenes | >10s | Riesgo de fatiga visual + necesidad de Kling tier 10s o 2 clips contiguos. |

**Por qué importa**: con 23 imágenes, ~12 quedan <3s o son detail puros — no se animan con Kling por límite técnico (drift de startup, costo, micro-drift artificial sobre detail). Resultado: 50% del video estático en background motion, 50% animado. Inconsistencia visual.

Con 12-15 imágenes:
- Cada una tiene ~6-8s en pantalla → aguanta tier Kling 5s o 10s con buffer
- 10-12 animables con Kling (~$6-8 budget)
- 2-3 estáticas SOLO para details o transiciones <2s muy puntuales
- Motion consistente en TODO el video

**Anti-pattern detectado en mina-abandonada v6→v7d**: para resolver "tomas POV repetidas" agregamos variantes -a/-b/-c hasta 23 imágenes. Resolvió repetición pero introdujo fragmentación. La solución correcta era **menos imágenes con shot types distintos** (close-up / wide / detail / POV diferenciados), no más variantes del mismo.

**Aplicación durante shot list (antes de generar imágenes)**:

| Tipo de plano | Cantidad target |
|---|---|
| Establishing wide (intro, exterior, valley) | 2-3 |
| Close-ups con expresión clave | 3-4 |
| POV con motion narrativo (descenso, escape) | 3-4 |
| Detail con narrativa puntual (objeto crítico) | 2-3 |
| **TOTAL** | **12-15** |

**Diseñá cada imagen para ser animable con Kling de entrada.** Si una imagen no sobrevive el decision tree (§ 1), no la generes.

---

## 2. DURATION MATCHING — el error #1 a evitar

### El problema

Imagen en pantalla X segundos. Kling animó Y segundos. Si Y < X, dos cosas pasan:
- **Frame congelado en los últimos X-Y segundos** → se nota muerto
- **O loop visible** si configuraste el `<video loop>` → se nota repetitivo

Engagement cae instantáneo. Pasó en elige-companero v1: imágenes de 7s animadas a 5s → 2s de "muerto" perceptibles.

### Kling tiene tiers fijos, no duración continua

Kling v2.0 en Replicate acepta `--duration` pero los tiers reales son **5s o 10s**. No podés pedir 7s.

### La fórmula

```
kling_duration = next_tier_above(scene_duration + 0.5s)
```

Aplicado:

| Duración scene | Pedir a Kling | Buffer que te queda | Costo (tier × $0.07/s) |
|---|---|---|---|
| ≤ 3s | NO usar Kling — Ken Burns suficiente | – | $0 |
| 3s–4s | Kling 5s | 1-2s (perfecto) | ~$0.35 |
| 5s–9s | **Kling 10s** | 1-5s ("gratis" — pagás el tier 10 igual) | ~$0.70 |
| > 10s | 2 clips Kling 10s + crossfade, **O** Kling 10s + Ken Burns sobre last frame extend | Variable | ~$1.40 o $0.70 |

**Regla de 1s de holgura**: siempre dejá al menos 1s de margen entre la duración del clip Kling y la duración de la imagen en pantalla. Cubre drift típico de TTS regen / caption shift / music edit.

### Las 3 estrategias cuando scene_duration > tier_máximo

1. **Hold last frame** (más barato): Kling 10s + GSAP extiende la imagen del último frame con Ken Burns sutil hasta el end. Funciona si los últimos 2-3s no necesitan motion específico.
2. **2 clips Kling contiguos** (más caro pero más motion): generar Kling 10s + Kling 10s con el último frame del primero como `start_image` del segundo. Crossfade 0.3s. Cuesta el doble pero da motion continuo.
3. **Loop atmosférico** (solo si el contenido es loopable): Kling 5s con prompt diseñado para loop invisible (ver § 4). Solo funciona si NO hay acción narrativa con start/end.

---

## 3. LOOP STRATEGY — cuándo y cómo loopear

### Cuándo SÍ se permite loop

- Contenido **estructuralmente loopable** sin start/end perceptible:
  - Niebla / humo / vapor flotando lento
  - Partículas suspendidas (polvo en la luz)
  - Llama de vela / lámpara titilando
  - Agua corriendo en background
  - Fuego de fogata
  - Estrellas titilando
- Plano que es esencialmente un **título atmosférico vivo** (ej: H1 horror-choice intro)

### Cuándo NUNCA loopear

- Personaje haciendo cualquier gesto con start/end (gira cabeza, parpadea, levanta mano)
- Cámara con push-in/pan completo (loop muestra el "snap back" al inicio)
- Cualquier acción narrativamente direccional (caminar, caer, abrir puerta)

### Prompts loop-safe (recetario)

| Tipo | Prompt template |
|---|---|
| Niebla entre personajes | `"Subtle fog drifting slowly horizontally between [subjects], characters perfectly still, no character motion, atmospheric only, camera locked, 5 seconds"` |
| Vela/lámpara titilando | `"Candle flame flickering subtly, almost imperceptible breeze, characters and background static, camera locked, looping atmospheric, 5 seconds"` |
| Polvo en la luz | `"Dust particles suspended in headlamp beam drifting slowly, subjects motionless, camera locked, atmospheric depth, 5 seconds"` |
| Fuego de fogata | `"Warm campfire flames flickering naturally, embers rising slowly, scene otherwise still, camera locked, looping warm atmosphere, 5 seconds"` |

### Verificar loop antes de integrar

Después de generar un clip Kling para loop:
1. Abrir el .mp4
2. Reproducirlo 3 veces seguidas mentalmente
3. ¿Notás dónde está el corte de loop? Si sí → regenerá con prompt más atmosférico
4. ¿Los primeros 0.3s coinciden con los últimos 0.3s? Si no → no es loopable

---

## 4. PROMPT ENGINEERING para Kling

### Fórmula validada (de PIPELINE.md § 9)

```
[SUJETO] + [VERBO DE MOVIMIENTO ESPECÍFICO] + [DIRECCIÓN/RESULTADO] + [CONTEXTO ATMOSFÉRICO]
```

### Lo que sí funciona

- **Movimiento de cámara > movimiento de sujeto** (más controlable y predecible)
- **Una acción principal por prompt** (Kling falla con múltiples acciones)
- **Movimientos lentos y deliberados** (rápidos quedan crudos)
- **Atmospheric loops** (más confiables que character animation)
- **Specificity en la dirección**: "leans forward" mejor que "moves"

### Anti-patterns Kling

| ❌ | Por qué falla | ✅ Alternativa |
|---|---|---|
| `[acción] toward camera` con violencia | Kling aplica acción sobre el sujeto, no hacia espectador | Describir experiencia del espectador: "foreleg descends into frame, fills screen" |
| Múltiples eventos simultáneos | Kling ignora la mayoría o los mezcla mal | Un solo movimiento principal por prompt |
| `camera shakes` como efecto | No lo interpreta como cámara | Omitir — editar en post con GSAP shake |
| Personajes hablando (boca abriendo) | Sale uncanny / desincronizado del audio | Animar gesto sutil (asentir, mirar) o solo atmósfera |
| Cara con expresión cambiando | Morphing visible | Foto fija con flicker exposure (CSS) en lugar de Kling |
| Acción de >5s en tier 5s | Se acelera artificialmente | Pedir tier 10s o simplificar acción |

---

## 5. PREPARACIÓN DE ASSETS pre-Kling

### Imagen base limpia

Kling necesita la imagen **sin filtros CSS aplicados**. Si tu CSS pone:

```css
.scene-image { filter: contrast(1.18) saturate(0.45) brightness(0.78); }
```

…entonces la imagen que mandás a Kling es el PNG raw (sin filter). El filter se aplica en HTML después.

### Formato

- **Aspect ratio**: 9:16 (vertical Reels)
- **Resolución mínima**: 1K (1024×1820 o similar) — más alto no aporta porque Kling output es 720p o 1080p
- **Formato**: PNG (no JPG — preserva detalle)
- **Sin texto/captions hardcoded** en la imagen (los captions van en HTML)

### Comando base

```bash
uv run ai-video video \
  -i assets/scene-source.png \
  -p "tu prompt aquí" \
  -o assets/scene.mp4 \
  --duration 5  # o 10
```

Modelo: `kwaivgi/kling-v2.0` | Parámetro de imagen: `start_image` (NO `image`) | cfg_scale: 0.5

---

## 6. INTEGRACIÓN HTML / HyperFrames

### Reemplazar `<img>` por `<video>`

Antes (estática):
```html
<img id="scene-1" src="assets/scene.png" class="scene-image clip"
     style="opacity:0;" data-start="19.0" data-duration="7.0" data-track-index="20" />
```

Después (animada):
```html
<video id="scene-1" src="assets/scene.mp4" class="scene-image clip"
       autoplay muted playsinline
       data-start="19.0" data-duration="7.0" data-track-index="20"
       style="opacity:0;"></video>
```

Si el clip Kling es 10s y la scene es 7s, **NO** poner `loop`. HyperFrames respeta `data-duration` y corta. El video corre los primeros 7s del Kling y se va.

Si querés loop intencional (caso atmospheric H1):
```html
<video id="scene-h1" src="assets/scene.mp4" class="scene-image clip"
       autoplay muted playsinline loop
       data-start="0" data-duration="7.0" data-track-index="0"
       style="opacity:1;"></video>
```

### GSAP — mismo que `<img>`

Los `tl.set("#scene-1", { opacity: 1 }, T)` siguen funcionando igual. Ken Burns con `scale` también, pero **cuidado**: el `scale` se aplica encima del motion de Kling. Por lo general con Kling NO hace falta Ken Burns adicional — el motion del clip es suficiente.

Excepción: si el motion de Kling es muy sutil (atmospheric), Ken Burns sobre el `<video>` da más vida sin sobrecargar.

### Track-index

Igual que las imágenes: rango 0-19. El video clip ocupa un track-index único, no comparte con otros.

### z-index y filter

`.scene-image` aplica:
- `z-index: 10`
- `filter: contrast(1.18) saturate(0.45) brightness(0.78)` (el horror grade)

Para `<video>` con clase `.scene-image`, el filter se aplica al video frame. Funciona igual que con `<img>`.

---

## 7. SINCRONIZACIÓN CON NARRADOR

Si el clip Kling tiene una acción narrativamente importante (ej: una mano cayendo, un personaje volteándose):

1. **El motion clave debe ocurrir cuando el narrador lo dice**
2. **NO antes** (spoiler visual)
3. **NO después** (se siente desincronizado)

### Cómo planearlo

1. Generás el TTS y medís duraciones
2. En el GSAP del video sabés exactamente cuándo arranca cada frase del narrador
3. Para un clip Kling con acción a los 2.5s (ej: la mano cae a los 2.5s del clip), `data-start` del `<video>` debe ser `T_frase_narrador - 2.5s`
4. Validación: extraer frames del render a los timestamps de las frases clave y confirmar que el visual matchea

### Anti-pattern

- Pedir a Kling un gesto genérico que no corresponde a ninguna frase del narrador
- Pedir múltiples gestos para que "alguno coincida con la narración" → el motion se ve random

---

## 8. COSTO + RETRIES + QUALITY VARIANCE

### Costo real Kling v2.0

- Tier 5s: ~$0.35/clip
- Tier 10s: ~$0.70/clip
- **15 imágenes** del video × 8-10 animadas = $4-7 base
- **Retries** (15-20% fail rate): ×1.5 = **$6-10 budget realista por video**

### Quality variance — Kling falla aleatoriamente

Patrones de falla observados:
- Personaje se "derrite" o pierde forma
- Manos con dedos extra/raros
- Cámara hace movimiento inesperado
- Sujeto desaparece o aparece otro

### Protocolo de retries

1. **Pre-render check**: abrir cada clip Kling apenas se genera y revisarlo SOLO antes de integrarlo al HTML
2. **Budget por clip**: máximo 3 intentos. Si después de 3 no sale bien:
   - **Opción A**: aceptar el "mejor" intento y compensar con motion CSS encima
   - **Opción B**: dejar la imagen estática + Ken Burns y aceptar el trade-off
3. **NO descubrir el problema en el render final del video completo** — perdés 15 min de render para detectar 1 clip malo

### Anti-pattern

- Generar todos los 10 clips Kling en batch sin revisar uno por uno
- Descubrir fallas en el render final → re-render = re-gastar 15 min + retries Kling caros

---

## 9. AUDIO — Kling outputs silent video

Kling no genera audio. Esto es **bueno** porque:
- Tu capa de SFX/música/narración ya existente sigue funcionando intacta
- No hay conflicto entre audio del clip y audio del proyecto

Excepción rara: algunos modelos generan ambient suave. Si pasa:
```bash
# Re-extraer video sin audio
ffmpeg -i assets/scene.mp4 -an -c:v copy assets/scene-silent.mp4 -y
```

---

## 10. WORKFLOW completo (orden recomendado)

```
PRE-CONDICIÓN: video ya pasó Gemini QA ≥ 9.0 con imágenes estáticas + Ken Burns
                (no animar hasta que el "shape" del video esté validado)

1. Listar imágenes para Kling (8-10 de las 15-20)
   → Para cada una: tipo de plano + duración en scene + complejidad de acción

2. Diseñar prompt Kling para cada una
   → Aplicar prompts validados de PIPELINE.md § 9 o adaptar
   → Definir loopable vs no

3. Calcular tier por imagen (5s o 10s)
   → scene_duration + 0.5s buffer → next tier

4. Generar clips Kling en batch (paralelo si la API lo permite)
   → Costo: $5-9 esperado

5. Pre-render check de cada clip
   → 1 minuto por clip × 10 clips = 10 min de revisión
   → Reintentar los que fallen (budget 3 intentos por clip)

6. Reemplazar <img> por <video> en index.html
   → Cuidado con autoplay muted playsinline + sin loop (excepto loopables)

7. Render draft del video completo
   → 15-20 min HyperFrames

8. Gemini QA + 9ª categoría DIAGNOSIS CHECKLIST (duración animaciones)
   → Si algún clip se siente truncado o loopea visible → flag

9. Si todo OK → render final --quality high
```

---

## 11. CHECKLIST PRE-RENDER FINAL

Antes de declarar el video animado terminado:

- [ ] Cada `<video>` tiene `data-duration` ≤ duración del clip MP4
- [ ] Clips loopables (atmospheric only) NO tienen personajes con start/end de gesto
- [ ] Clips con acción narrativa están sincronizados con frase del narrador correspondiente
- [ ] Quality variance OK — ningún personaje "se derrite" en algún frame
- [ ] Filter CSS funciona sobre `<video>` igual que sobre `<img>`
- [ ] Audio del proyecto sigue intacto (Kling no introdujo audio raro)
- [ ] Render draft pasa Gemini QA ≥ 9.0

---

## 11.5. INTERPOLACIÓN start_image + end_image (Kling v2.5 turbo pro, 2026-05-11)

### Capability

Kling v2.5 turbo pro acepta **dos imágenes**: `start_image` (frame inicial) y `end_image` (frame final). El modelo interpola el motion entre ambas composiciones generando un plano continuo donde la composición A se transforma en la composición B.

```bash
uv run ai-video video \
  -i  assets/scene-start.png \
  -e  assets/scene-end.png \
  -p  "prompt de motion (qué cambia entre A y B)" \
  -o  assets/scene-morph.mp4 \
  --duration 5
```

Schema Replicate confirmado: `start_image` + `end_image` + `prompt` + `duration` (5|10) + `negative_prompt` (sin `cfg_scale`).

### Cuándo es ideal usar

| Caso | Por qué funciona |
|---|---|
| **Personajes "apareciendo" en escena** (intro reveals) | Empty scene → scene-with-characters. Reemplaza un cut por una aparición orgánica. |
| **Cámara dolly + cambio de contenido** | Forward push se mantiene continuo mientras el contenido del frame se transforma. |
| **Transformación atmosférica** (día → noche, niebla densa → niebla disipada) | El motion es la transformación misma. |
| **Reveal de detalle oculto** (objeto que se va materializando) | Empty composition → composition con objeto. |

### Cuándo NO usar

- **Composiciones radicalmente distintas** (interior → exterior, primera persona → tercera persona). Kling no puede interpolar coherentemente cambios de cámara/escenario.
- **Motion temporal grande** (escena nocturna → escena diurna 10s). Mejor 2 clips contiguos con crossfade.
- **Personajes con gestos específicos** entre start y end. El motion intermedio puede salir uncanny (lips, dedos).

### Receta validada — characters materializing en intro

**Caso real** (mina-abandonada intro v4, 2026-05-11):
- `start_image`: `h1-teaser.png` — mine entrance vacía + niebla + 2 luces ominosas dentro
- `end_image`: `h1-characters.png` — same mine entrance + Hugo (izquierda) + Santi (derecha)
- Prompt: `"Slow steady camera dolly forward toward an abandoned coal mine entrance over rusted mine cart rails. Thick fog gradually clears as we approach. Two miner figures gradually materialize from the darkness at the mine entrance: HUGO (left) gaunt veteran with carbide lamp helmet and pickaxe, SANTI (right) young miner with LED helmet and notebook. They emerge into view as if always there but only revealed by the approach. Ominous atmospheric reveal."`
- Duration: 5s
- Resultado: t=0 = teaser exacto, t=2s personajes empiezan a emerger desde sombras, t=3s personajes sólidos, t=4-5s = end_image exacto. Score Gemini de la intro entera 9.7/10.

### Anti-patterns

- ❌ **end_image con composición completamente distinta a start_image** — Kling no puede interpolar cambios de cámara o escenario radicales
- ❌ **Prompt vago** ("characters appear") — funciona mejor describiendo el motion DE LA CÁMARA + qué cambia entre A y B
- ❌ **Tier 5s para morph complejo** (3+ personajes apareciendo) — usar tier 10s
- ❌ **No verificar el lastframe** — extraer frame en t=duration-0.1s y confirmar que matchea end_image. Si no matchea → mejorar prompt o regenerar.

### Costo

Mismo precio que un Kling normal (tier 5s o 10s). El `end_image` no agrega costo. Es la herramienta más eficiente para "scene reveals" sin requerir 2 clips + crossfade manual.

---

## 12. ANTI-PATTERNS críticos (resumen)

- ❌ **Animation duration < image-on-screen duration** — frame congelado o loop visible. Aprendizaje elige-companero v1.
- ❌ **Loop con contenido no-loopable** — gestos de personajes, push-ins de cámara
- ❌ **Múltiples acciones en un prompt Kling** — falla previsible
- ❌ **Aplicar filter CSS antes de Kling** — Kling necesita PNG limpio
- ❌ **Descubrir fallas Kling en el render final** — gastar 15 min de render para detectar 1 clip malo
- ❌ **Animar TODO** — caro, innecesario, y los "wide establishing shots" no ganan nada con Kling

---

## Validado en

- **elige-companero v1** — 9 prompts Kling exitosos; learning clave (duration mismatch → match tier 5s/10s) ya codificado en §2/§12 + SKILL.md.

---

## Aplicación a otros formatos (general)

Esta doc aplica a CUALQUIER formato de video con IA. Para formatos específicos, hay overrides:

| Formato | Override animación |
|---|---|
| **horror-choice-format** | H1 (presentación personajes) **siempre Kling tier 5s loopable atmospheric** — niebla/velas/partículas, sin character motion. Ver `horror-choice-format/PATTERNS.md` § animación. |
| **documental** (futuro) | – |
| **educacional** (futuro) | – |
