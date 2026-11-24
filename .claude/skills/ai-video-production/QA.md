# QA.md — Validación de video con Gemini Video Analyzer

> Gate de calidad obligatorio antes de publicar. Skill local `video-analyzer` (`~/.claude/skills/video-analyzer/`) usa Gemini 3 Flash para analizar el video y devolver score 1-10. Sin score ≥ 9.0 no se publica.

---

## ⭐ Roadmap — QA hacia referent-based (incremental shift 2026-05-15)

**Current state**: Gemini holístico ≥9.7 + 4 referent-validated checks (Q17-Q20) + **Q21 referent-profile matching** (NUEVO 2026-05-15 — `ai-video audit-against-referent` con p25-p75 bands per metric).

**Direction**: phase out Gemini como rate-limiter primario. Migrar a `ai-video audit-against-referent` como vara primaria data-driven; Gemini como sanity check creativo solamente.

**Razón**: Gemini holístico ha mostrado scores históricamente inflados:
- pueblo-fantasma-desierto v2 (2026-05-13): Gemini 9.9 con video real 7/10 (24% cobertura narrativa + gaps de 40s + caminos rotos)
- isla-faro v1: 9.0+ con countdown tapando imagen + texto sobre rostros
- Pattern: Gemini puntúa "atmósfera + cinematografía" sobre incoherencia narrativa subyacente.

**Vara primaria futura** (cuando ai-video audit-against-referent madure y se valide en 3+ proyectos): match contra F1 canonical n=10 con p25-p75 bands per métrica. Critical metrics = pace WPM / LUFS / cuts/min / narration coverage. ≥85% de estos in range = pass.

**Vara actual (transitional, 2026-05-15)**: hard rule #1 = AMBAS gates requeridas (Gemini ≥9.7 + audit-against-referent ≥85%).

---

## Comando base

```bash
python3 ~/.claude/skills/video-analyzer/scripts/analyze_video.py \
  renders/draft.mp4 \
  --prompt "<TU_PROMPT_DE_QA>"
```

Output: reporte markdown con secciones (Top-Level Summary, Scene-by-Scene, Audio, Visual Details, Key Moments). El score lo pedís explícitamente en el prompt.

---

## Prompt UNIVERSAL (cualquier video con IA) — 14 dimensiones obligatorias

> **PRINCIPIO ANTI-ALUCINACIÓN (regla actualizada 2026-05-13 post pueblo-fantasma-desierto):** Gemini Video Analyzer aprobó un video con 9.9/10 que en realidad tenía 40s de outro casi sin narración + 24% de cobertura narrativa total + caminos narrativos rotos. Gemini mira "atmósfera + cinematografía" y da score alto si el ambient music + algún SFX tapan los gaps. **NUNCA confiar solo en el score holístico** — forzar siempre el inventario obligatorio de las dimensiones (11)-(14) abajo. Si CUALQUIER dimensión 11-14 reporta ausencias/gaps significativos → **score TOPE 8.0 sin importar la atmósfera**.

```
Analiza en detalle:
(1) ¿La narración y los captions están sincronizados (sin desfase audible)?
(2) ¿El texto es legible en todos los fondos (incluyendo niebla, amanecer, fuego)?
(3) ¿Hay variedad visual o se reusa la misma imagen en múltiples momentos de una misma escena?
(4) ¿El video se siente vivo (motion en cada plano) o slideshow (fotos estáticas)?
(5) ¿El diseño sonoro va más allá de narración + música? (¿hay footsteps, breaths, impactos, ambient continuo?)
(6) ¿Hay momentos donde la imagen permanece estática >2s sin ningún tipo de motion?
(7) ¿Las transiciones se sienten intencionales o abruptas?
(8) ¿La mezcla de audio respeta jerarquía (narración manda, música apenas, SFX en su lugar)?
(9) ¿El video se siente cinematográfico o tipo "presentación con narración"?
(10) CONTINUIDAD NARRATIVA: ¿Hay alguna caption on-screen que contradice o duplica de manera redundante lo que el narrador dice en los siguientes 5 segundos? (Ej: caption dice "ELIGES A HUGO" pero narrador dice "Si elegiste a Hugo..." → debería decir "SI ELEGISTE A HUGO" para continuidad).
(11) INVENTARIO DE ELEMENTOS UI: lista CADA elemento de texto/UI que aparece en pantalla con su timestamp aprox (countdown, captions, labels, choice text, end CTA). Si no aparece un elemento que esperarías, dilo explícitamente — no asumas su presencia.

(12) INVENTARIO DE NARRACIÓN — OBLIGATORIO LISTAR TIMESTAMP A TIMESTAMP:
     Lista CADA bloque de narrador con start/end exacto y la frase aprox que dice.
     Ejemplo formato:
       0.2s-4.5s: "Elige a tu compañero. Para subir al pueblo."
       9.0s-13.5s: "Si elegiste a Enrique..."
       (...)
     Después responde:
     - ¿Hay GAPS >2s entre bloques narrativos consecutivos?
       Si sí, lista cada gap: "Entre 18.18s y 25.25s (7.07s sin narración)"
     - ¿La narración cubre <40% del video total? (suma duraciones / duración video)
     - ¿Los últimos >5s del video tienen narración o solo música/silencio?
     Si CUALQUIERA de los 3 puntos es "sí" → score TOPE 8.0.

(13) INVENTARIO DE MÚSICA — OBLIGATORIO:
     - ¿Hay música? ¿En qué segundos start-end?
     - ¿Cubre ≥85% del video?
     - ¿Hay segmentos >5s sin música cuando el formato la requiere?
     Si NO hay música o cobertura <50% → score TOPE 7.0.

(14) NARRATIVE CLOSURE — comprensión de trama:
     En 1 sola frase, contame qué pasó en el video (como si fueras un viewer común).
     Si NO podés contarlo en 1 frase → la trama está rota → score TOPE 7.5.
     Si la trama tiene gaps lógicos ("¿pero por qué eso era trampa?") → score TOPE 8.0.
     Si hay plot twist: ¿se entiende el twist sin contexto previo? ¿Imágenes acompañan? ¿Narración explica el link?

Dame un score 1-10 considerando las 14 dimensiones. **RECORDÁ: el score TOPE de 8.0 aplica si fallan (12), (13) o (14) — NO compenses con atmósfera buena.**
```

⚠️ **Por qué las dimensiones (10)-(14) son obligatorias** (acumulado 2026-05-11 + 2026-05-13):
- (10) Gemini lee captions y oye narrador pero NO valida continuidad automáticamente. El caption "ELIGES A HUGO" pasó 5 iteraciones sin que Gemini se quejara, hasta que el humano lo cazó porque conocía el guion.
- (11) **Gemini alucina presencia de elementos** que matchean el patrón del género. En un test real Gemini reportó "vi countdown 3-2-1" cuando los `<div class="countdown-num">` NO renderizaban (bug de timeline).
- (12) **Caso pueblo-fantasma-desierto v2 (2026-05-13)**: Gemini dio 9.9 a un video con 24% cobertura narrativa + gap de 40s sin narración al final + 4 gaps de 5-7s entre bloques de narrador. Audio ambient tapaba los silencios narrativos. Sin esta dimensión explícita, Gemini NO lo flagea. Cross-check técnico: `ai-video audit-audio` parsea el HTML directamente.
- (13) Mismo caso: música puede estar presente pero narración ausente. Forzar inventario separado de ambos.
- (14) **Caso isla-faro v1 y pueblo v2**: la trama no cierra pero Gemini da 9+ por atmósfera. La prueba del "viewer cuenta el video en 1 frase" expone la incoherencia.

Para formatos específicos, **agregar dimensiones adicionales** según el formato. Ejemplo: `horror-choice-format/PAUTA.md` § 2 extiende este prompt con 4 dimensiones específicas del formato (A/B comprensión, transición al cliffhanger, tamaño choice labels, CTA).

---

## Umbral de aprobación

| Score | Acción |
|---|---|
| **≥ 9.7** | APROBADO para publicar (vara del director, ver `video-director/SKILL.md`) |
| **9.0 – 9.6** | Iterar buscando ≥9.7. Si tras 3 iter no llega → ESCALAR al usuario |
| **7.0 – 8.9** | Iterar. Anotar feedback de Gemini y aplicar las reglas del formato + toolkit |
| **< 7.0** | Algo estructural está roto. Revisar diseño desde la raíz |

**Umbral oficial del proyecto = 9.7/10 (FIJO, no negociable)**. Sub-9.7 NO se publica bajo ninguna circunstancia. La vara se subió de 9.5 → 9.7 el 2026-05-13 tras validar que es el piso necesario para one-shot quality reproducible. "Ship-pragmatic 9.2-9.5" quedó deprecada el 2026-05-12. Si tras 3 iteraciones seguís <9.7, ESCALAR al usuario (ver sección AUTONOMOUS LOOP).

---

## Cómo interpretar el feedback

Cada problema que Gemini menciona → comparar contra las reglas universales (V8-1/2/3) + reglas del formato específico:

| Problema Gemini detecta | Causa probable | Fix |
|---|---|---|
| "Se siente como presentación" | Falta motion | `MOTION-LAYER.md` — agregar parallax, flicker, vignette |
| "Misma imagen aparece varias veces" | Falta variantes | `IMAGE-VARIETY.md` — generar -b/-c |
| "Sonido pobre, solo música" | Falta capa SFX | `SFX-PIPELINE.md` — agregar footsteps, breaths, impactos |
| "Captions desincronizadas" | Hand-timing | `CAPTIONS.md` — regenerar con Whisper |
| "Texto ilegible en X frame" | Falta stroke | Agregar `-webkit-text-stroke` |
| "Transición abrupta" | Cuts secos donde debería haber motion | Whip cut con motion blur o glitch wipe |
| "Mezcla satura la voz" | Volúmenes mal calibrados | Revisar tabla mix de `SFX-PIPELINE.md` |

---

## Workflow recomendado

1. **Render draft** (calidad `draft`, ~8-15 min)
2. **Ejecutar QA** con prompt universal + dimensiones del formato
3. **Si score < 9.0**: leer el feedback detallado, identificar las dimensiones que fallaron, aplicar los fixes correspondientes, re-render
4. **Repetir hasta ≥ 9.0**
5. **Render final** (calidad `high`, ~30-45 min)
6. **Re-verificar specs** con ffprobe (h264 30fps, aac 48000)
7. **Subir**

---

## Notas sobre el video-analyzer skill

- Vive en `~/.claude/skills/video-analyzer/` (global, no project-local)
- Requiere `GEMINI_API_KEY` en environment
- Archivos ≤18MB suben inline; >18MB usan Files API con polling hasta 300s
- Modelo default: `gemini-3-flash-preview` (override con `--model`)
- Soporta `--fps` para sampling rate (útil en cortes muy rápidos)
- Retorna markdown plano, no JSON (el script extrae `response.text`)

---

## Cuándo el QA Gemini NO es suficiente

Casos donde necesitás complementar con `docs/FEEDBACK-LOOP.md` (QA manual sin ver el video):

- Verificar timings exactos de audio (Gemini puede confundir 24.5s con 25s)
- Validar que un asset específico aparece o no
- Inspeccionar frames específicos en detalle (slice con ffmpeg)
- Confirmar que SFX están en la mezcla aunque sean sutiles

Para estos casos usar el método del feedback loop: render → slice frames → read → diagnose.

### 🚨 Gemini ALUCINA presencia de elementos (regla descubierta 2026-05-11)

Patrón confirmado: cuando Gemini analiza un video del género que conoce (horror choice Reels), tiende a **reportar elementos que SE ESPERARÍAN** del género aunque no estén en el render concreto.

**Caso real**: render `intro-preview-v2.mp4` tenía un bug donde el countdown 3-2-1 NO renderizaba (timeline namespace incorrecto). Frame extraction a t=5.8, 6.2, 6.5 mostró fondo limpio sin números. Pero Gemini reportó: "Countdown 3-2-1 (0.33s c/u) — Muy frenético". Inventó tanto la presencia como el timing.

**Implicación**: Gemini QA solo no es suficiente para confirmar que un elemento **existe**. Solo es bueno para evaluar **calidad** de elementos que existen.

**Protocolo obligatorio frame extraction post-render**:
```bash
# Para cada elemento UI esperado, extraer frame al timestamp medio de su ventana
for t in 5.95 6.45 6.95 7.5 8.5; do
  ffmpeg -y -ss $t -i renders/X.mp4 -frames:v 1 -q:v 3 "/tmp/check-t${t}.jpg" -loglevel error
done
# Luego abrir cada JPG (Read tool) y verificar presencia
```

**Cuándo es crítico**: SIEMPRE para countdown, captions clave (cap-chose / cap-q), flash, loading bar. Si no aparece en el frame, ningún score de Gemini lo va a cazar.

---

## AUTONOMOUS ITERATION LOOP — el loop default sin human-in-the-loop

> Desde 2026-05-10 el director-de-video corre el loop completo **autónomamente** hasta llegar a la vara de calidad. El humano valida solo al final, no cada iteración intermedia.

### El loop

```
LOOP:
  1. Render draft
  2. Gemini QA con prompt extendido (9 dim universal + dim del formato)
  3. Diagnose con DIAGNOSIS CHECKLIST (8 categorías abajo)
  4. Si STOP CONDITION cumplida → break y reportar al humano
  5. Si no → aplicar fixes específicos por categoría que falló
  6. Volver a paso 1
```

El humano interviene **solo si**:
- Llega a la vara de calidad y la IA reporta "listo"
- El loop se escala por stop condition (ver abajo)

### DIAGNOSIS CHECKLIST — las 8 categorías a chequear cada iteración

Gemini Video Analyzer detecta algunas de estas pero no todas (aprendizaje 2026-05-10: Gemini falla en variedad visual real y cortes narrativos). Por eso este checklist mezcla análisis Gemini + análisis humano-style (extracción de frames + grep del HTML).

#### 1. Variedad visual
**Chequear**: ¿Escenas >4s sin variantes `-a/-b/-c`? ¿Mismo shot type repetido en escenas distintas (wide POV caminando × 6)? ¿Variantes que son la misma toma con framing distinto en lugar de tipos de plano diferentes?

**Cómo**:
```bash
# Listar todas las <img> con su data-start y data-duration
grep -E '<img.*data-start' <project>/index.html
# Si hay varias con data-duration > 4s y srcs muy parecidos → flag
```
Además: extraer frames a esos timestamps y comparar shot types visualmente.

**Fix doc**: `IMAGE-VARIETY.md` — regenerar como tipos de plano DIFERENTES, no variantes de la misma toma.

#### 2. Capa SFX completa
**Chequear**: ¿White flash sin audio? ¿Loading bar silenciosa (sin drone + sin tick)? ¿Countdown 3-2-1 sin tick.mp3? ¿Narración sin ambient debajo? ¿Twist sin impact thud? ¿Cliffhanger sin warm whoosh?

**Cómo**:
```bash
# Listar todos los <audio> y sus tracks
grep -E '<audio.*src=' <project>/index.html | grep -oE 'src="[^"]+"'
# Comparar contra los timestamps de flash, loading, twist, countdown
```

**Fix doc**: `SFX-PIPELINE.md` — generar los 7 SFX de corte canónicos si faltan + SFX por escena.

#### 3. Cortes narrativos (NARRATIVE-LED-EDITING)
**Chequear**: ¿Todos los cortes son white flash + corte directo (lineal)? ¿O usa la taxonomía completa de 7 tipos (negros + audio variado entre frases del narrador)?

**Cómo**: contar en el HTML cuántos `#black-overlay` opacity transitions hay vs cuántos `#flash-white`. Si el ratio es <1:1, falta black-cut variety. Además: leer el script del narrador (`NARRATIVE.md`) y mapear cada cambio de beat a un cut → confirmar que cada beat tiene su corte tipo correspondiente.

**Fix doc**: `NARRATIVE-LED-EDITING.md`.

#### 4. Captions
**Chequear**: 
- Overlaps entre elementos distintos (`cap-h3-n4` + `cap-h3-branch` visibles juntos)
- Gaps >0.3s sin texto entre frases del narrador
- Sync con audio (Whisper auto, no hand-timed)
- Legibilidad en fondos claros (text-stroke aplicado)

**Cómo**: extraer frames a los timestamps de transiciones entre elementos caption + leer.

**Fix doc**: `CAPTIONS.md` — eliminar `opacity:0` intermedios + hide explícito durante separadores V7-3 + h5-bridge.

#### 5. Motion
**Chequear**: ¿Ken Burns en TODO plano estático >2s? ¿Motion adicional (parallax/flicker/vignette/glitch/glow) donde el plano lo pida?

**Cómo**:
```bash
# Buscar imágenes sin tl.to({scale...}) asociado
grep -A2 '<img.*scene-image' <project>/index.html | grep -B1 'data-duration="[3-9]'
# Cruzar con el GSAP — debería haber tl.to scale para esa imagen
```

**Fix doc**: `MOTION-LAYER.md`.

#### 6. POV continuity (solo para formatos con branching)
**Chequear**: En el cut a rama mala, ¿la cámara muestra al espectador siendo la víctima (primera persona — mano hacia cámara, POV ground, etc.) o lo muestra como observador externo (tercera persona — ves el monstruo emerger, ves el túnel girar)?

**Cómo**: extraer frame al timestamp del twist malo (típicamente 38.5s en H3, 65s en H4) y evaluar: ¿qué ve la cámara? ¿Es lo que VOS vivís o lo que LE pasa a alguien?

**Fix doc**: `NARRATIVE-LED-EDITING.md` + `IMAGE-VARIETY.md` — regenerar la imagen del twist malo con POV primera persona.

#### 7. Mix volumes
**Chequear**: Narración 1.0, música 0.05-0.18, SFX 0.20-0.35, flash impacts 0.55-0.65, ambient 0.10-0.18.

**Cómo**:
```bash
grep -oE 'data-volume="[^"]+"' <project>/index.html | sort -u
# Si hay valores fuera de los rangos canónicos → flag
```

**Fix doc**: `SFX-PIPELINE.md`.

#### 8. Specs IG
**Chequear**: H.264 + AAC + 1080×1920 + 30fps + ≤650 MB.

**Cómo**:
```bash
ffprobe -v quiet -print_format json -show_streams <render>.mp4 | \
  python3 -c "import json,sys; [print(s['codec_name'], s.get('r_frame_rate',''), s.get('sample_rate',''), s.get('width',''), s.get('height','')) for s in json.load(sys.stdin)['streams']]"
ls -lh <render>.mp4
```

**Fix**: re-render con flags correctos. Si tamaño excede 650 MB usar `--quality draft` para iteraciones intermedias.

#### 9. Duración animaciones (solo aplica si hay clips Kling)
**Chequear**:
- ¿Cada `<video>` Kling tiene duración del clip ≥ `data-duration` del video en HTML?
- ¿Algún clip loopea visiblemente (contenido no loopable: personaje con gesto, cámara con push-in completo)?
- ¿Los gestos narrativos de Kling están sincronizados con la frase correspondiente del narrador?
- ¿Hay 1s de buffer entre duración del clip Kling y data-duration?

**Cómo**:
```bash
# Listar todos los <video> con sus data-durations
grep -E '<video.*data-duration' <project>/index.html
# Para cada uno, medir duración del MP4 fuente
for clip in <project>/assets/*.mp4; do
  echo "$clip: $(ffprobe -v quiet -show_entries format=duration -of csv=p=0 "$clip")"
done
# Cruzar: data-duration debe ser ≤ duración del clip
```

Además: extraer frames a los timestamps del último segundo de cada clip para confirmar que NO hay frame congelado ni loop visible.

**Fix doc**: `ANIMATION-LAYER.md` — usar tier correcto (5s o 10s con +1s buffer), elegir contenido loopable para clips cortos, sincronizar gestos con narrador.

#### 10. Continuidad narrativa caption ↔ narrador (nuevo 2026-05-11)
**Chequear**: ¿Algún caption on-screen contradice o duplica de manera redundante lo que el narrador dice en los siguientes 5s? Caso típico: caption del intro dice "ELIGES A HUGO" pero el narrador de H3 que arranca a continuación dice "Si elegiste a Hugo..." — debería ser "SI ELEGISTE A HUGO..." en la caption para continuidad sin redundancia.

**Cómo**:
```bash
# Para cada caption del HTML, listar el siguiente bloque de narración por timestamp
grep -E 'id="cap-[^"]+"' <project>/index.html | head
# Comparar el texto de cap-chose con el primer renglón del narrador siguiente
grep -A1 "### h[0-9].*narr1" <project>/NARRATIVE.md
```
Si el texto de la caption NO es prefijo o continuación natural del narrador → fix.

**Fix doc**: `video-director/ANTI-PATTERNS.md` § Captions — "Caption text inconsistente con próxima frase del narrador".

#### 11. Inventario de elementos UI (verificación anti-alucinación)
**Chequear**: cada elemento UI/texto que debería aparecer (countdown numbers, labels, captions, flash, loading bar, end CTA) está realmente en el render.

**Cómo**: extraer frames a los timestamps de ventana media de cada elemento esperado y verificar con Read. No confiar en el reporte Gemini para presencia de elementos.

**Fix**: si elemento faltante → revisar timeline registration (`window.__timelines.main`), z-index, opacity inline, data-duration, conflicto con otro elemento del mismo track-index.

### STOP CONDITIONS — cuándo cortar el loop

| Condición | Acción |
|---|---|
| **Gemini ≥ 9.7** + 8 categorías green | ✅ STOP — declarar terminado, reportar al humano |
| **Gemini < 9.7 en stop point pre-animation** | ⛔ **NO REPORTAR todavía. Iterar con fixes NO-ANIMATION-AI** (guion, captions, imágenes, wiring, mix) hasta ≥9.7. Recién después ir a animación AI (Kling/Hailuo/Seedance/etc. según MODEL-BENCHMARK) para cumplir hard rule primeros 30s. Animation AI NO rescata score bajo — solo agrega +0.1-0.2 sobre baseline validado. |
| **Gemini < 9.7** después de **3 iteraciones de fixes no-animation-AI** | 🚨 ESCALAR al usuario con análisis dimensión-por-dimensión + opciones de fix. NO publicar. |
| **Gemini < 7.0** en cualquier iteración | 🚨 ESCALAR — algo estructural está roto, no es iteración. Reportar gap específico |
| Mejora **<0.1** entre 2 iteraciones consecutivas (sin llegar a 9.7) | 🚨 ESCALAR — diminishing returns, decisión humana sobre seguir o aceptar |

**Regla 2026-05-13 — vara FIJA 9.7**: sub-9.7 NO se publica bajo ninguna circunstancia. La vara se subió de 9.5 → 9.7 tras validar que es el piso necesario para one-shot quality reproducible. "Ship-pragmatic 9.2-9.5" (2026-05-10) y "vara 9.5" (2026-05-12) quedaron deprecadas. Si tras 3 iter seguís <9.7, escalá al usuario con propuesta concreta de fix. El usuario decide.

### Cómo reportar al humano al final del loop

Al cortar el loop (por cualquier stop condition), generar un reporte conciso con esta estructura:

```
═══════════════════════════════════════
LOOP TERMINADO — <proyecto> v<N>
═══════════════════════════════════════

Score Gemini final: <X.X>/10  (vs vara 9.7)
Iteraciones corridas: <N>/3
Razón del stop: <ship-9.7 | escalate-stuck-sub-9.7 | escalate-structural | escalate-diminishing-returns>

Diagnosis checklist final:
   1. Variedad visual:           ✅/⚠️/❌ <nota corta>
   2. Capa SFX:                  ✅/⚠️/❌
   3. Cortes narrativos:         ✅/⚠️/❌
   4. Captions:                  ✅/⚠️/❌
   5. Motion:                    ✅/⚠️/❌
   6. POV continuity:            ✅/⚠️/❌ (n/a si no hay branching)
   7. Mix volumes:               ✅/⚠️/❌
   8. Specs IG:                  ✅/⚠️/❌
   9. Duración animaciones:      ✅/⚠️/❌ (n/a si no hay Kling)
  10. Continuidad cap↔narrador:  ✅/⚠️/❌
  11. Inventario UI verificado:  ✅/⚠️/❌ (frame extraction obligatoria)

Render final: <path>
Specs: h264 30fps aac48k 1080×1920 <size MB>

Próxima acción sugerida: <publicar | re-iterar con humano | regenerar asset X>
```

### Anti-patterns del loop autónomo

- ❌ **Saltarse el diagnosis checklist** — Gemini score solo no basta. Las 8 categorías son la red de seguridad.
- ❌ **Iterar >3 veces sin cambiar estrategia** — si después de 3 intentos sigue trabado, hay que escalar al humano, no insistir.
- ❌ **Aceptar score <9.7 silenciosamente o publicar sub-9.7** — vara fija 9.7 (subida desde 9.5 el 2026-05-13). Siempre reportar honesto, escalar al usuario si no llega tras 3 iter.
- ❌ **Aplicar fixes sin diagnose** — si Gemini dice "captions desincronizadas" y vos sin investigar regenerás imágenes, perdés el tiro. Cada fix debe responder a una categoría específica del checklist que falló.
- ❌ **Reportar "listo" sin completar el reporte final** — el humano necesita ver el checklist + razón del stop para confiar.
