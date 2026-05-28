# INTRO-FORMULA.md — Receta del intro de 9s

> **Scope**: 🎬 Horror-choice format × 📱 Reel/short-form (9:16)
>
> ⚠️ **AUDIT 2026-05-13 PM:** esta fórmula está validada en **mina-abandonada v15** (nuestra producción 9.9/10 Gemini) — pero **NO en los 8 videos canónicos virales** de `/videosref_elige_tu_compa/`. La autoridad creativa empírica es `PAUTA-MASTER.md`.
>
> **Estado de esta fórmula:**
> - ✅ **Reglas TÉCNICAS válidas como receta operacional**: timing 9s intro, captions Whisper-sync, white flash 0.25s, countdown 0.5s/número, labels mínimo 2.5s
> - ⚠️ **Nombres/arquetipos** (HUGO/SANTI/etc.) son de nuestra producción, NO de los 8 canónicos
> - ⚠️ **Duración total del video**: este doc asume 30-90s. PAUTA-MASTER § 2 documenta range empírico real 76-129s, sweet spot 80-100s
>
> Receta técnica vigente. Nombres + slots narrativos deben venir del catálogo `PAUTA-MASTER.md` §§ 7-13, no de aquí.

---

## Estructura macro (9s flat)

```
0.00-0.10  Frame 0: imagen atmospheric teaser (empty location + ominous element)
0.10-3.10  CAPTIÓN h1-narr Whisper-sync (3 frases progresivas)
0.00-3.00  KLING dolly: teaser → characters materialize (start_image + end_image)
3.10-3.20  Captioning gap (h1-stab SFX dispara)
3.20-5.70  Labels HUGO/SANTI visibles (2.5s)
4.71-5.70  CAPTIÓN cap-q "¿CON QUIÉN BAJARÍAS?" (1s)
5.70-7.20  Countdown 3-2-1 (0.5s c/u) + ticks
7.20-7.45  White flash (0.25s fade out)
7.45-9.00  Silence beat (NO cap-chose — el Whisper de h3-narr1 carry el bridge)
9.00       Cut a H3 (historia arranca)
```

---

## Assets requeridos

### 1. Imagen teaser (h1-teaser.png)

**Prompt template Gemini Nano Banana**:

```
Wide centered composition of an abandoned [SETTING] entrance at deep dusk/night. 
A [PORTAL TYPE: wooden-framed dark tunnel mouth / open doorway / cave mouth] in 
the center background, [ENVIRONMENTAL DETAIL: rusted mine cart rails / overgrown 
path / cracked stone steps] leading into pitch darkness. Thick heavy fog drifting 
horizontally across the entrance, partially obscuring the mouth. **Two dim warm 
[LIGHT SOURCE: carbide lamps / orange embers / pairs of eyes] glowing faintly 
deep inside.** Industrial debris and dark [vegetation/forest/structures] flanking 
the sides. No people, no characters, completely empty entrance. Cold blue twilight 
palette outside, faint amber glow inside. Cinematic ominous establishing shot.
```

**Variables a reemplazar por proyecto**:
- `[SETTING]`: mina abandonada / bosque / casa rural / mansion / faro / cueva / etc.
- `[PORTAL TYPE]`: el "umbral" simbólico (mina mouth, doorway, path entrance, etc.)
- `[ENVIRONMENTAL DETAIL]`: detalle del foreground (rails, path, steps, etc.)
- `[LIGHT SOURCE]`: los 2 puntos de luz ominosos que sugieren "algo vivo" adentro

**Comando**:
```bash
.venv/bin/python scripts/image.py \
  -p "..." \
  -o assets/h1-teaser.png \
  --size 1K --aspect 9:16
```

### 2. Imagen personajes (h1-characters.png)

Standard: 2 personajes (malo aparente + bueno aparente) en mismo escenario que el teaser pero ahora visibles en la entrada. Ver `horror-choice-format/PATTERNS.md` § 4 para prompts de personajes.

### 3. Kling clip h1-approach (5s tier)

**Receta exacta**:
```bash
.venv/bin/python scripts/video.py \
  -i assets/h1-teaser.png \
  -e assets/h1-characters.png \
  -p "Slow steady camera dolly forward toward an abandoned [SETTING] entrance over [DETAIL]. Thick fog gradually clears as we approach. Two [character archetypes] gradually materialize from the darkness at the [SETTING] entrance: [MALO] (left) [description], [BUENO] (right) [description]. They emerge into view as if always there but only revealed by the approach. Ominous atmospheric reveal." \
  -o assets/h1-approach.mp4 \
  --duration 5
```

Replicate model: `kwaivgi/kling-v2.5-turbo-pro` (default tras 2026-05-11).

### 4. Extender clip Kling a 9s (ffmpeg tpad)

```bash
ffmpeg -y -i assets/h1-approach.mp4 \
  -vf "tpad=stop_mode=clone:stop_duration=4" \
  -an assets/h1-approach-9s.mp4
```

Resultado: 9s. Primeros 5s = motion (dolly + materialize). Últimos 4s = hold del último frame (personajes estáticos en la entrada).

### 5. TTS h1-narr

**Template**:
```
"Elige a tu compañero. Para bajar a [LOCATION CON ARTÍCULO] esta noche. [BUENO]... o [MALO]."
```

**Comando**:
```bash
python3 scripts/tts.py \
  -t "Elige a tu compañero. Para bajar a la mina esta noche. Hugo... o Santi." \
  -o assets/h1-narr-raw.mp3
ffmpeg -y -i assets/h1-narr-raw.mp3 -filter:a "atempo=2.0" assets/h1-narr-2x.mp3
```

Duración esperada post-atempo: 4.5-5.0s (depende de length del nombre).

### 6. Whisper sobre h1-narr-2x.mp3

```bash
python3 -c "
import whisper
m = whisper.load_model('base')
r = m.transcribe('assets/h1-narr-2x.mp3', language='es', word_timestamps=True, verbose=False)
for seg in r['segments']:
    for w in seg.get('words', []):
        print(f'{w[\"start\"]:.2f}-{w[\"end\"]:.2f}  {w[\"word\"]}')
"
```

Usar el output para generar 3 frases progresivas para `#cap-h1-narr`.

---

## HTML completo del intro (copy-paste, slots marcados con `[SLOT]`)

```html
<!-- ============ INTRO HORROR-CHOICE 9s — v15 FORMULA ============ -->

<!-- Música y ambient -->
<audio id="music-horror" class="clip" src="assets/music-horror.mp3"
  data-start="0" data-duration="9" data-track-index="50" data-volume="0.13"></audio>
<audio id="ambient-mine" class="clip" src="assets/sfx/ambient-mine-loop.mp3"
  data-start="0" data-duration="9" data-track-index="60" data-volume="0.10"></audio>

<!-- ÚNICO video del intro: dolly + materialize + hold (sin cuts internos) -->
<video id="h1-approach" src="assets/h1-approach-9s.mp4"
  class="scene-image clip" autoplay muted playsinline
  style="opacity:1;"
  data-start="0" data-duration="9" data-track-index="0"></video>

<!-- Overlays atmósfera -->
<div class="cold-tint"></div>
<div class="ambient-grain"></div>
<div class="vignette"></div>

<!-- Labels personajes — drop shadow universal recipe -->
<div id="label-hugo"  class="name-label clip"
  data-start="3.2" data-duration="2.5" data-track-index="2">[MALO_NAME]</div>
<div id="label-santi" class="name-label clip"
  data-start="3.2" data-duration="2.5" data-track-index="3">[BUENO_NAME]</div>

<!-- Captions (Whisper-sync para h1-narr + cap-q estático) -->
<div class="caption-wrap">
  <div id="cap-h1-narr" class="caption caption-abs" style="opacity:0;"></div>
  <div id="cap-q"       class="caption caption-abs" style="opacity:0;">¿CON QUIÉN [VERBO BAJARÍAS/ENTRARÍAS/IRÍAS]?</div>
</div>

<!-- Audio principal -->
<audio id="h1-narr" class="clip" src="assets/h1-narr-2x.mp3"
  data-start="0" data-duration="[H1_NARR_DURATION]" data-track-index="40" data-volume="1.0"></audio>
<audio id="h1-cave-drone" class="clip" src="assets/sfx/h1-cave-drone.mp3"
  data-start="0" data-duration="3" data-track-index="62" data-volume="0.25"></audio>
<audio id="h1-stab" class="clip" src="assets/sfx/h1-name-stab.mp3"
  data-start="3.2" data-duration="0.5" data-track-index="63" data-volume="0.55"></audio>

<!-- Countdown 5.7-7.2 (0.5s c/u) -->
<div id="cnt-3" class="countdown-num clip"
  data-start="5.7" data-duration="0.5" data-track-index="4">3</div>
<div id="cnt-2" class="countdown-num clip"
  data-start="6.2" data-duration="0.5" data-track-index="5">2</div>
<div id="cnt-1" class="countdown-num clip"
  data-start="6.7" data-duration="0.5" data-track-index="6">1</div>

<audio id="tick-h2-3" class="clip" src="assets/sfx/tick.mp3"
  data-start="5.7" data-duration="0.1" data-track-index="100" data-volume="0.7"></audio>
<audio id="tick-h2-2" class="clip" src="assets/sfx/tick.mp3"
  data-start="6.2" data-duration="0.1" data-track-index="101" data-volume="0.7"></audio>
<audio id="tick-h2-1" class="clip" src="assets/sfx/tick.mp3"
  data-start="6.7" data-duration="0.1" data-track-index="102" data-volume="0.7"></audio>

<audio id="h2-flash" class="clip" src="assets/sfx/h2-flash-impact.mp3"
  data-start="7.2" data-duration="0.5" data-track-index="65" data-volume="0.6"></audio>

<div id="flash-white"></div>
```

## GSAP del intro (copy-paste, slots marcados con `[T_]`)

```js
const tl = gsap.timeline({ paused: true });

/* Video único — scale push Ken Burns sobre 9s */
tl.fromTo("#h1-approach", { scale: 1.0 }, { scale: 1.05, duration: 9.0, ease: "sine.inOut" }, 0);

/* H1 narrador captions (Whisper-sync) — sound-off retention hook */
tl.set("#cap-h1-narr", { opacity: 1, innerHTML: "ELIGE A TU COMPAÑERO" }, [T_FRASE_1]);
tl.set("#cap-h1-narr", { opacity: 1, innerHTML: "PARA BAJAR A [LOCATION]" }, [T_FRASE_2]);
tl.set("#cap-h1-narr", { opacity: 1, innerHTML: "ESTA NOCHE..." }, [T_FRASE_3]);
tl.set("#cap-h1-narr", { opacity: 0 }, 3.10);

/* Labels v12 timing — 2.5s */
tl.set("#label-hugo",  { opacity: 1 }, 3.2);  tl.set("#label-hugo",  { opacity: 0 }, 5.7);
tl.set("#label-santi", { opacity: 1 }, 3.2);  tl.set("#label-santi", { opacity: 0 }, 5.7);

/* Question caption */
tl.set("#cap-q", { opacity: 1 }, 4.7);
tl.set("#cap-q", { opacity: 0 }, 5.7);

/* Countdown 0.5s c/u */
tl.set("#cnt-3", { opacity: 1 }, 5.7);  tl.set("#cnt-3", { opacity: 0 }, 6.2);
tl.set("#cnt-2", { opacity: 1 }, 6.2);  tl.set("#cnt-2", { opacity: 0 }, 6.7);
tl.set("#cnt-1", { opacity: 1 }, 6.7);  tl.set("#cnt-1", { opacity: 0 }, 7.2);

/* Flash 7.2-7.45 (250ms fade-out) */
tl.set("#flash-white", { opacity: 1 }, 7.2);
tl.to( "#flash-white", { opacity: 0, duration: 0.25, ease: "power2.out" }, 7.201);
tl.set("#flash-white", { opacity: 0 }, 7.45);

/* 7.45-9.0: silence beat — NO cap-chose, el cap-h3-n1 Whisper @ 9.2 carry el bridge */

/* HyperFrames timeline registration (CRÍTICO) */
window.__timelines = window.__timelines || {};
window.__timelines.main = tl;
```

---

## Audio mix volumes (canónicos v15)

| Audio | data-volume | Track |
|---|---|---|
| h1-narr | 1.0 | 40 |
| music-horror | 0.13 | 50 |
| ambient-mine | 0.10 | 60 |
| h1-cave-drone | 0.25 | 62 |
| h1-stab | 0.55 | 63 |
| h2-flash | 0.60 | 65 |
| tick × 3 | 0.70 | 100-102 |

---

## Reglas a NO romper

1. ❌ **NO meter cap-chose ("SI ELEGISTE A [MALO]...") en el intro**. El Whisper de cap-h3-n1 a los 9.2s ya dice "SI ELEGISTE A [MALO]," → poner caption en intro es redundante.

2. ❌ **NO cortar h1-approach a la mitad** (ej: 0-3s) para insertar otro clip. Validado en v13/v14 que rompe el dolly. Single clip = single dolly continuo.

3. ❌ **NO countdown <0.5s por número**. Validado en v13 que 0.33s es "atropellado". 0.5s es el sweet spot.

4. ❌ **NO labels visibles <2s**. v13 los tuvo 1.5s y el usuario detectó que desaparecen muy rápido.

5. ❌ **NO usar mismo voice ID para Hugo whisper hook + narrador omnisciente** (si se implementa hook). Validado que se confunde. Si se quiere hook → diferente voice ID + pitch shift.

---

## Costo estimado (intro completo)

| Asset | Costo |
|---|---|
| h1-teaser.png (Gemini Nano Banana) | ~$0.04 |
| h1-characters.png (Gemini) | ~$0.04 |
| h1-approach.mp4 (Kling v2.5 turbo pro tier 5s) | ~$0.30 |
| h1-narr TTS (ElevenLabs) | ~$0.05 |
| Whisper (local) | $0 |
| **TOTAL intro** | **~$0.43** |

---

## QA específico del intro

Antes de declarar el intro listo, validar (frame extraction):
- t=0.5s: visual atmospheric + caption visible
- t=2.0s: dolly en progreso + caption "PARA BAJAR..."
- t=3.5s: personajes materializados + labels HUGO/SANTI visibles
- t=5.0s: cap-q "¿CON QUIÉN..." visible
- t=6.0s: countdown "2" visible
- t=7.3s: post-flash, characters sostenidos
- t=8.5s: silencio visual, characters estáticos (preparando bridge a H3)

Cualquier frame con NEGRO o sin elemento esperado → bug. Revisar GSAP namespace, tpad extend, captions opacity.

---

## Casos producidos siguiendo esta fórmula

| Proyecto | Setting | Variables | Score |
|---|---|---|---|
| ⭐ mina-abandonada v15-final | mina abandonada | malo=Hugo, bueno=Santi, verb=BAJARÍAS, location=la mina | 9.9/10 |

---

## Cross-references

- `PATTERNS.md` § 1 — estructura temporal general del formato
- `PATTERNS.md` § 10.5 — Opción D: Teaser materialization (técnica visual)
- `BRAND.md` — preset filter CSS canónico (`contrast 1.28 saturate 0.35 brightness 0.74`)
- `ai-video-production/CAPTIONS.md` — Whisper-sync hard rule
- `ai-video-production/RETENTION-RULES.md` — reglas de retención short-form
- `video-animation/ANIMATION-LAYER.md` § 11.5 — técnica Kling start_image + end_image
