# ANTI-PATTERNS.md — Lo que NUNCA hace el director

> Aprendizajes amargos de proyectos previos. Cada item costó tiempo, créditos, o calidad. Memorizalos.

---

## Workflow / iteration

### ❌ Parar en stop-point pre-animation con sub-9.7 esperando que la animación AI lo arregle

```
Score pre-animation: 9.3
Reporte: "Listo el stop point. Pendiente animation AI para llegar a 9.7."
```

**Por qué falla:** animation AI (Kling/Hailuo/Seedance/etc.) es animación image-to-video. NO arregla:
- Captions desincronizados o vagos
- Imágenes que no acompañan la narrativa
- Coherencia del plot twist (3 condiciones de § 6.5)
- Guion con gaps lógicos (info no establecida que se cobra después)
- Mix volumes mal balanceados
- Wiring HTML/GSAP roto (z-index, timing, opacity)

Animation AI **agrega motion** a imágenes que ya cuentan la historia bien. Si las imágenes/captions/guion están en 9.3, la animación las lleva quizás a 9.4-9.5 — NO a 9.7. El gap restante (0.2-0.4) se cierra con A→B→C (guion, assets, wiring), no con D (animation AI).

**Fix:** stop-point pre-animation DEBE estar en ≥9.7 con fixes NO-ANIMATION-AI (guion/captions/imágenes/wiring/mix — todo menos animar). Si <9.7, NO reportar al usuario — iterar dentro de 3 rounds aplicando:

1. **Fase A — Guion/captions**: rewrite frases que Gemini marcó vagas, eliminar redundancias caption↔narrador, comprimir intro si >10% del total.
2. **Fase B — Assets**: regenerar imágenes que confundan, agregar detail shots faltantes, generar setup elements del twist con timing 2.5-3.5s.
3. **Fase C — Wiring/mix**: dawn-birds u otros ambient missing, mix volumes canónicos, captions safe zone, opacity gaps.

Animation AI es Fase D (modelo según MODEL-BENCHMARK) — solo después de que A+B+C ya llevaron el video a ≥9.7. Animation AI cumple la hard rule "primeros 30s = animation AI obligatoria" + agrega +0.1-0.2 al score baseline.

**Aprendido en:** isla-faro v1 (2026-05-13). Agente productor reportó stop point con 9.3, asumiendo animation AI cerraría el gap. Usuario detectó: "Animation AI no fixea captions/imágenes/coherencia. Eso nunca puede pasar."

**Doc:** `ai-video-production/QA.md` § AUTONOMOUS LOOP — tabla actualizada.

---

## Retención (primeros 30s del Reel)

**Scope**: 📱 **Vertical short-form ÚNICAMENTE** (Reels/TikTok/IG Stories/YT Shorts). Todas las reglas de esta sección asumen retention dynamics agresivas de short-form. Para YouTube long-form, B2B commercial, etc., las reglas de retención son distintas — ver respectivos `formats/*.md`.

### ❌ Dejar escena estática o con solo Ken Burns en `data-start < 30s`

```html
<!-- MAL — wide establishing al inicio del Reel sin Kling -->
<img id="h1-establishing" src="..." data-start="0" data-duration="5"
     class="ken-burns-slow">
```

**Por qué falla:** la retención algorítmica de Instagram pesa MUCHO los primeros 30s. Ken Burns suave o estática en esa ventana se siente "diapositiva" para el espectador que está scrolleando rápido → mano va al swipe. La curva de retención cae del 70%+ al 40% sin que el resto del video pueda recuperarla.

**Fix:** todo `data-start < 30s` se anima con Kling, sin importar el tipo de plano. Es la única excepción a la regla "no animar wide/detail".

```html
<!-- BIEN — wide establishing inicial con Kling -->
<video id="h1-establishing" src="assets/h1-establishing.mp4"
       data-start="0" data-duration="5" autoplay muted playsinline></video>
```

**Costo implicado:** +$1-2 por video respecto a budget tradicional. Asumido — la retención lo paga.

**Doc:** `video-animation/ANIMATION-LAYER.md` § 1 PRE-GATE. Hard rule #6 (`video-director/SKILL.md`). Hard rule #9 (`video-animation/SKILL.md`).

---

## Captions / subtítulos

### ❌ Hand-timing captions

```js
// MAL — timings escritos a ojo
tl.set("#h3-cap-1", { opacity: 1 }, 19.2);
tl.set("#h3-cap-1", { opacity: 0 }, 21.0);
tl.set("#h3-cap-2", { opacity: 1 }, 21.2);
```

**Por qué falla**: SIEMPRE se desincronizan. Tras regenerar audio cambian las duraciones y los timings quedan viejos. Y a ojo nunca aciertas el on/off por palabra.

**Fix**: `scripts/captions.py --spec captions-spec.json` (Whisper).

**Aprendido en**: bosque-abandonado v1 (captions desfasados, regeneración completa).

---

### ❌ Captions pegados al fondo (`bottom: 0`)

**Scope**: 📱 Vertical short-form (Reels/TikTok/IG Stories/YT Shorts). NO aplica a YouTube long-form ni B2B horizontal.

```css
.caption-wrap {
  bottom: 0;        /* MAL */
  height: 400px;
}
```

**Por qué falla**: la UI de Instagram (description, username, music sticker, like button) tapa los bottom ~400px del feed. El caption queda invisible o cortado.

**Fix**: 
```css
.caption-wrap {
  bottom: 540px;    /* canónico IG Reel */
  height: 280px;
}
```

Para otros formats vertical short-form ver `ai-video-production/formats/<format>.md` § UI Safe Zones (YT Short usa bottom 380px, IG Story usa center).

**Aprendido en**: bosque-abandonado v2 (Gemini detectó el problema en QA post-mortem).

---

### ❌ Loading bars en `bottom: 300-480px`

**Scope**: 📱 Vertical short-form.

**Por qué falla**: misma razón. Quedan en zona UI de IG.

**Fix**: `bottom: 700px` (mucho más arriba, fuera de toda UI).

---

### ❌ Mantener `opacity: 0` intermedios entre frases del mismo audio

```js
// MAL
tl.set("#cap-X", { opacity: 1, innerHTML: "FRASE 1" }, 1.0);
tl.set("#cap-X", { opacity: 0 }, 2.0);   /* gap visible 0.5s */
tl.set("#cap-X", { opacity: 1, innerHTML: "FRASE 2" }, 2.5);
tl.set("#cap-X", { opacity: 0 }, 3.5);
```

**Por qué falla**: produce gaps visibles 0.3-0.6s entre cada frase. El espectador percibe que "los captions fallan".

**Fix**: dejar UN solo `opacity: 0` al final del bloque. Entre frases, solo cambia `innerHTML`.

```js
// BIEN
tl.set("#cap-X", { opacity: 1, innerHTML: "FRASE 1" }, 1.0);
tl.set("#cap-X", { opacity: 1, innerHTML: "FRASE 2" }, 2.5);
tl.set("#cap-X", { opacity: 0 }, 3.5);
```

**Aprendido en**: mina-abandonada v3→v4 (2026-05-10).

---

### ❌ Caption text inconsistente con próxima frase del narrador

```html
<!-- Caption del intro -->
<div id="cap-chose">ELIGES A HUGO</div>
```
```
# Narrador h3-narr1 que arranca 0.2s después
"Si elegiste a Hugo... lleva treinta años en este pozo."
```

**Por qué falla**: el viewer escucha "Si elegiste" pero acaba de leer "ELIGES" (presente simple). Conflicto micro-perceptible que rompe inmersión. Además es redundante: si el narrador dice la frase completa "Si elegiste a Hugo", el caption estandalone es ruido.

**Fix**: el caption debe ser prefijo o continuación natural del narrador siguiente. En este caso: `"SI ELEGISTE A HUGO..."` para que el caption FLUYA hacia la próxima frase narrada (los Whisper captions de H3 luego completan "...lleva treinta años en este pozo.").

**Cómo detectarlo**: dimensión #10 del prompt Gemini QA (continuidad narrativa) + grep manual de NARRATIVE.md vs index.html para cada caption hardcoded.

**Aprendido en**: mina-abandonada intro v1-v5 (2026-05-11). Pasó 5 iteraciones de Gemini QA sin que lo flagee porque la prompt no incluía esa dimensión. El humano lo cazó.

---

## Imágenes

### ❌ Reusar la misma imagen para múltiples captions de una escena

```html
<img id="h3-walk-1" src="assets/h3-forest.png" data-start="19" />
<img id="h3-walk-2" src="assets/h3-forest.png" data-start="22" />  <!-- MAL -->
<img id="h3-walk-3" src="assets/h3-forest.png" data-start="25" />  <!-- MAL -->
```

**Por qué falla**: slideshow feel garantizado. Con motion (Ken Burns/parallax) el ojo nota la repetición incluso más.

**Fix**: generar variantes `-a`, `-b`, `-c` con TIPOS DE PLANO distintos (wide / close-up rostro / close-up detalle).

**Aprendido en**: bosque-abandonado v2 (Gemini: "PowerPoint narrado").

---

### ❌ Generar variantes que son la misma toma con framing distinto

```
h3-walk-a: wide POV caminando, sujeto a 3 pasos
h3-walk-b: wide POV caminando, sujeto a 5 pasos      ← MAL, misma toma
h3-walk-c: wide POV caminando, low angle             ← MAL, misma toma
```

**Por qué falla**: sigue sintiéndose slideshow. El ojo nota que "varias imágenes diferentes pero iguales".

**Fix**: cambiar el TIPO DE PLANO entre variantes (wide → close-up rostro → close-up detalle). Ver `IMAGE-VARIETY.md` catálogo.

**Aprendido en**: mina-abandonada v1 test.

---

### ❌ Generar cada escena del personaje SIN reference image (rompe consistencia visual)

```bash
# MAL — cada imagen de "Berni" es un Berni distinto
.venv/bin/python scripts/image.py -p "Berni caminando en bosque" -o h3-walk.png
.venv/bin/python scripts/image.py -p "Berni mirando al espectador" -o h3-look.png
.venv/bin/python scripts/image.py -p "Berni cerca de la mano" -o h3-hand.png
```

**Por qué falla**: Gemini genera 3 "Bernis" diferentes — caras distintas, edad fluctuante, ropa varía. El espectador percibe que es **otra persona** entre tomas → rompe la inmersión narrativa.

**Fix obligatorio**: workflow Anchor + Reference. Doc completo: `ai-video-production/CHARACTER-CONSISTENCY.md`.

```bash
# 1. PRIMERO: generar anchor del personaje (close-up frontal claro, sin --ref)
.venv/bin/python scripts/image.py \
  -p "Medium close-up of [PERSONAJE], facing camera, neutral expression, soft lighting." \
  -o assets/berni-anchor.png

# 2. DESPUÉS: cada escena con ese personaje pasa el anchor como --ref
.venv/bin/python scripts/image.py \
  -p "The character from the reference walking through dark forest. Same face, same age." \
  --ref assets/berni-anchor.png \
  -o assets/h3-walk.png
```

**Regla**: NUNCA generar escenas con personaje sin tener su anchor primero. NUNCA regenerar el anchor después de haber generado escenas (rompe todo).

**Aprendido**: problema clásico de generación con IA. Sin anchor + ref, el personaje "muta" entre tomas.

---

### ❌ Generar imágenes con gore / sangre / violencia explícita

Gemini Nano Banana rechaza prompts con:
- "blood", "sangre", "slashing motion", "razor-sharp edge"
- Acciones violentas hacia cámara

**Fix**: describir resultado visual, no acción. Ver `PIPELINE.md` § 2 tabla de bloqueos.

### ❌ Imágenes con visibilidad efectiva <1s (regla de oro)

Si una imagen aparece en pantalla **menos de 1 segundo**, NO VALE LA PENA. No hace sentido tenerla. El ojo no la procesa, solo registra un flash que distrae sin aportar narrativa.

**Causas típicas:**
1. `<img>` con `data-start` antes de que el GSAP la haga `opacity:1` mientras OTRO elemento (black overlay, otra imagen) la cubre antes de que se vea claro
2. Asset declarado para "soportar" un beat audio pero cubierto por black/flash el 95% de su tiempo
3. Split de una imagen en dos variantes que dejan a una de ellas <1s para meter más variedad (V8-1 mal aplicado)

**Caso real (mina-abandonada v7c):**
`h4-pull` (mano que jala) tenía `data-start=67.5` y `data-duration=2.2`. El black overlay entraba a 68.5s con fade 0.15s. Entre 68.5–68.65 (0.15s) h4-pull se veía a través del black fading. Resultado: flash visible <1s. **Fix:** removido del GSAP completamente — la narración auditiva ("Te jala") + caption blanco + thud SFX comunican el momento sin imagen explícita.

**Cómo auditar:** script en producción

```python
# Para cada <img>:
# 1. Calcular data_end = data-start + data-duration
# 2. Encontrar GSAP show (primer opacity:1) y hide (primer opacity:0 posterior)
# 3. effective_visible = min(hide, data_end) - max(show, data_start)
# 4. Flaggear si effective_visible < 1.0
```

**Fix general:** si la imagen no contribuye visualmente porque está cubierta por black/flash/otra imagen, REMOVERLA. No "soporta" nada. El audio + caption ya hacen el trabajo.

**Excepción:** ÚNICA imagen que puede ser <1s es el `flash-white` mismo (3-5 frames @ 30fps = 0.1–0.17s) — ese es un cut intencional, no una imagen narrativa.

---

## Motion / animación

### ❌ Plano estático >2s sin Ken Burns

```html
<img class="scene-image clip" data-start="19" data-duration="6" />
<!-- sin tl.to() de scale -->
```

**Por qué falla**: Gemini lo detecta como "PowerPoint con narración".

**Fix**: SIEMPRE Ken Burns mínimo:
```js
tl.to("#mi-imagen", { scale: 1.04, duration: 6, ease: "sine.inOut" }, 19);
```

---

### ❌ `filter: blur()` animado con GSAP

**Por qué falla**: mata performance GPU, el render se enlentece 5-10x o se cuelga.

**Fix**: blur estático (CSS), o usar `transform: scale + opacity` para el efecto sin blur dinámico.

---

### ❌ `fromTo` para elemento que empieza invisible

```js
// MAL — produce flash al inicio porque fromTo setea el frame 1
tl.fromTo("#mi-img", { opacity: 0 }, { opacity: 1, duration: 0.5 }, 36.6);
```

**Por qué falla**: HyperFrames pre-renderiza el primer frame antes del play. El elemento aparece visible en t=0.

**Fix**: ancla en t=0 + set después:
```js
tl.set("#mi-img", { opacity: 0 }, 0);           // ancla
tl.set("#mi-img", { opacity: 1 }, 36.6);         // reveal
```

---

### ❌ White flash sin hard-kill posterior

```js
// MAL — al hacer seek, el flash reaparece
tl.set("#flash-white", { opacity: 1 }, T);
tl.to( "#flash-white", { opacity: 0, duration: 0.1 }, T + 0.001);
```

**Fix**: agregar hard-kill:
```js
tl.set("#flash-white", { opacity: 0 }, T + 0.2);  // obligatorio
```

---

## Audio / SFX / música

### ❌ Música procesada con `-ss` antes de `-af` con afade

```bash
# MAL — produce silencio total
ffmpeg -ss 17 -i music-raw.mp3 -t 5.2 -af "afade=t=in:st=0:d=0.2" music.mp3
```

**Fix**: 2 pasos.
```bash
# 1. trim
ffmpeg -y -i music-raw.mp3 -ss 17 -t 5.2 music-clip.mp3
# 2. fades
ffmpeg -y -i music-clip.mp3 -af "afade=t=in:st=0:d=0.2,afade=t=out:st=5.0:d=0.2" music-final.mp3
```

**Aprendido en**: PIPELINE.md § 6.

---

### ❌ Música / SFX que dura menos que la sección que debe cubrir

Ejemplo: `music-dawn.mp3` dura 6.1s, pero la sección H6 dura 18s.

**Por qué falla**: el audio termina y queda silencio.

**Fix**: pre-loop con ffmpeg.
```bash
ffmpeg -y -stream_loop -1 -i music-dawn.mp3 -t 23 music-dawn-loop.mp3
```

Usar siempre el `-loop.mp3`, nunca el original corto.

---

### ❌ Capa SFX ausente (solo música + narración + ticks)

**Por qué falla**: Gemini detecta "sonido pobre". El video se siente plano.

**Fix**: integrar capa SFX completa per `SFX-PIPELINE.md`. Footsteps, breaths, whispers, impacts, ambient continuo.

**Aprendido en**: bosque-abandonado v1→v2 (de 8.8 a 9.2 con sound design 9/10 → 10/10).

---

### ❌ Volúmenes que tapan la narración

```html
<audio src="music.mp3" data-volume="0.4">      <!-- MAL: tapa la voz -->
<audio src="sfx-flash.mp3" data-volume="1.0">  <!-- MAL: ensordece -->
```

**Fix**: mix volumes canónicos (SFX-PIPELINE.md tabla):
- Narración 1.0
- Música 0.05-0.18
- SFX puntuales 0.20-0.35
- Flash impacts 0.55-0.65
- Ambient continuo 0.10-0.18

---

### ❌ Usar raw TTS sin atempo 2x

Voz `Tj9l48J9AJbry5yCP5eW` es lenta por naturaleza. A 1x produce 162s de narración para un video de 90s.

**Fix**: SIEMPRE `ffmpeg -i raw.mp3 -filter:a "atempo=2.0" out.mp3` después de TTS.

---

### ❌ Boost de volumen >+10dB en narración

Lleva el peak a >0dBFS → clipping audible.

**Fix**: medir con `ffmpeg -af volumedetect` antes. Subir hasta peak max ~-3dBFS, no más.

---

## Render

### ❌ Dos renders en paralelo

```bash
npx hyperframes render -o renders/v1.mp4 &
npx hyperframes render -c index-v2.html -o renders/v2.mp4 &  # MAL
```

**Por qué falla**: ambos procesos compiten por CPU. FFmpeg recibe SIGTERM (exit 255).

**Fix**: secuencial siempre. Esperar uno + después el siguiente.

**Aprendido en**: bosque-abandonado v2 (render falló al 75% por contention con elige-companero).

---

### ❌ Render sin lint previo

**Por qué falla**: errores reales (id duplicado, asset missing) detienen el render a mitad de camino, perdiendo 5-10 min de captura de frames.

**Fix**: `npx hyperframes lint` antes de cada render. Warnings de multi-root son ignorables; errores reales NO.

---

### ❌ Declarar terminado sin Gemini QA

**Por qué falla**: vos no tenés ojos. El video puede tener problemas invisibles desde la HTML/code.

**Fix**: `python3 ~/.claude/skills/video-analyzer/scripts/analyze_video.py` antes de declarar listo. Score ≥9.7 o iterar.

**Aprendido en**: intro mina-abandonada 2026-05-11 — entregué v1 diciendo "listo, ritmo OK" sin haber pasado por Gemini ni abierto el .mp4. Usuario abrió, score real 6/10, perdimos 4 iteraciones extras corrigiendo.

---

### ❌ Declarar terminado sin frame extraction propia

**Por qué falla**: complementa al fix anterior. Gemini **alucina presencia de elementos** que matchean el patrón esperado del género. Reportó "countdown 3-2-1 visible" cuando los `<div class="countdown-num">` literalmente no renderizaban (bug de timeline). Score Gemini solo no detecta esto.

**Fix**: después de Gemini QA, extraer frames a los timestamps de elementos UI clave (countdown, captions, flash, end CTA) y verificar con `Read` el JPG.

```bash
for t in <timestamps de elementos UI esperados>; do
  ffmpeg -y -ss $t -i renders/X.mp4 -frames:v 1 -q:v 3 "/tmp/check-t${t}.jpg" -loglevel error
done
```

**Aprendido en**: intro mina-abandonada 2026-05-11 — iter v2→v3 Gemini reportó countdown OK pero frame extraction reveló que NO existía en el render (namespace de timeline incorrecto).

---

### ❌ Iterar timing sin abrir el render

**Por qué falla**: cambios "obvios" (mover 0.3s, ajustar opacity) pueden romper otra cosa silenciosamente. Si no abrís el output cada iteración perdés el rastro de qué se rompió.

**Fix**: cada render → 30s de frame extraction antes de seguir tocando.

**Aprendido en**: intro mina-abandonada 2026-05-11 — iteré 3 renders cambiando timings sin abrir el output. El render v3 estaba completamente roto (countdown + cap-chose invisibles) y solo lo descubrí al iterar al v4.

---

## Workflow / proceso

### ❌ Inventar pattern cuando hay doc

Ejemplo: agregar `caption-warm` class custom cuando ya existe `text-stroke 1.5px` canónico.

**Por qué falla**: divergencia de la doc, próxima sesión nadie va a saber por qué existe esa class.

**Fix**: leer el doc canónico del tema (`CLAUDE.md` § Mapa de docs autoritativos te dice cuál) ANTES de inventar. Si el pattern no existe Y lo necesitás, agrégalo al doc canónico al mismo tiempo que lo implementás.

---

### ❌ Aplicar 5 fixes y después renderizar

**Por qué falla**: si baja el score, no sabés cuál fix causó la regresión.

**Fix**: 2-3 fixes coordinados por iteración. Render. Medir. Siguiente iteración.

---

### ❌ Reportar score con padding

"Score 8.8, casi 9, vamos muy bien" → MAL.

**Fix**: "Score 8.8/10. Bajo el umbral. Iteramos."

---

### ❌ Inventar contenido (texto, nombres, hechos) sin chequear

Whisper transcribe "BERNI" como "VER NI" → no podés dejar "VER NI" en los captions.

**Fix**: revisar manualmente correcciones de nombres propios y términos específicos del proyecto.

---

### ❌ No releer una doc tras >50 mensajes

El contexto se pierde. Una regla que leíste al inicio puede haberse olvidado.

**Fix**: si la sesión es larga, releer rápido la doc relevante antes de la tarea.

---

### ❌ Construir micro-composición HTML "desde cero" copy-pasteando CSS

```html
<!-- MAL: arrancar intro-preview.html con copia parcial del CSS + script propio -->
<script>
  const tl = gsap.timeline({ paused: true });
  // ...
  window.__hyperframes_timeline__ = tl;  /* MAL: namespace inventado */
  tl.play(0);                            /* MAL: HyperFrames controla play */
</script>
```

**Por qué falla**: HyperFrames busca `window.__timelines.main` (no `__hyperframes_timeline__`). Sin ese registry **ningún `tl.set/tl.to` se ejecuta** y los elementos quedan en su style inline (opacity:0). El render se ve "normal" pero faltan todos los elementos animados — silencio total, sin error.

**Fix**: para micro-composiciones partir de un `cp index.html intro-preview.html` y stripear lo no-relevante, NO copy-pastear CSS de a piezas. El boilerplate del `<script>` SIEMPRE termina con:
```js
      window.__timelines = window.__timelines || {};
      window.__timelines.main = tl;
```

**Aprendido en**: intro mina-abandonada 2026-05-11 — invertí 3 renders + Gemini QAs antes de descubrir el namespace correcto. Ver `ai-video-production/HYPERFRAMES-GOTCHAS.md`.

---

### ❌ Validar micro-composición SIN testear el join point con la composición principal

**Por qué falla**: un intro standalone de 9s puede puntuar 9.7/10 en Gemini QA pero el segundo 9→10 al unirse con H3 puede ser un desastre (caption choca con caption-h3-n1, narrador suena cortado, música se solapa).

**Fix**: después de validar la micro-composición standalone, hacer un render combinado de [últimos 3s de micro] + [primeros 5s de la composición principal] y QA específicamente el join point antes de integrar.

**Aprendido en**: intro mina-abandonada 2026-05-11 — el intro v6 puntuó 9.7/10 standalone pero el caption "SI ELEGISTE A HUGO..." del intro se solapaba con cap-h3-n1 (misma frase del narrador). El usuario lo vio antes que yo.

---

## Git / archivos

### ❌ `rm -rf` sobre assets del proyecto

**Por qué falla**: los assets generados costaron créditos (Gemini, EL). Regenerar es caro.

**Fix**: nunca `rm` sin confirmar. Usar `mv` a `.trash/` si necesitás "borrar" pero recuperable.

---

### ❌ Sobrescribir `index.html` con cambios masivos sin backup

**Fix**: si vas a hacer un refactor grande, `cp index.html index-vN.html.bak` antes.

---

### ❌ Modificar skills `.claude/skills/` sin avisar al usuario

**Por qué falla**: los skills viven entre sesiones. Un cambio te afecta a vos en el futuro.

**Fix**: avisar al usuario antes de tocar skills. Documentar el cambio con fecha.

---

## Memoria / contexto

### ❌ Asumir que el usuario recuerda lo que dijiste hace 50 mensajes

No lo recuerda. Si referenciás algo viejo, recapitulá brevemente.

---

### ❌ No actualizar `MEMORY.md` cuando aprendiste algo

Cosas que valen ir a memoria:
- Voice ID correcto del proyecto.
- Specs IG del año.
- Reglas del formato.
- Bugs específicos descubiertos.
