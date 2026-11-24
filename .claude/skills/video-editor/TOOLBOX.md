# Videos Editor — TOOLBOX (la paleta)

> **Cómo leer este doc.** Esto es la **paleta de herramientas** disponibles para editar footage grabado, con su uso concreto. **NO es un procedimiento fijo.** No existe "el pipeline de edición": vos partís de lo que el user busca y **elegís + combinás** estas herramientas como mejor sirva al objetivo. Los comandos son ejemplos representativos para que sepas *cómo* opera cada herramienta — adaptá parámetros, encadená, salteá o reemplazá según el caso.
>
> **Convención de salida** (salvo que el user pida otra cosa): `.mp4` H.264 + AAC, `yuv420p`, dimensiones/fps consistentes. Re-encode con `-crf 18 -preset medium` da buena calidad/peso. Copias nuevas en carpeta de salida — nunca pisar originales.

---

## 0. Inspeccionar (siempre primero)

Para qué: entender el material antes de tocarlo (duración, resolución, fps, **rotación**, audio).

```bash
# Specs de video + audio
ffprobe -v error -select_streams v:0 \
  -show_entries stream=width,height,r_frame_rate -show_entries format=duration \
  -of default=noprint_wrappers=1 input.mp4
ffprobe -v error -select_streams a:0 -show_entries stream=codec_name,sample_rate,channels -of default=noprint_wrappers=1 input.mp4

# ⚠️ Rotación: footage de teléfono se almacena rotado. Chequealo SIEMPRE.
ffprobe -v error -select_streams v:0 -show_entries stream_side_data=rotation -of default=nk=1:nw=1 input.mp4

# Extraer un frame para VER el contenido (ffmpeg auto-rota → orientación de display real)
ffmpeg -v error -ss <seg> -i input.mp4 -frames:v 1 /tmp/peek.jpg -y
```

Si `rotation=-90` y stored es `1024×576`, el video **se ve `576×1024` vertical**. Trabajá en coordenadas de display (las del frame extraído).

---

## 1. Cortar / Trim

Para qué: quedarte con el segmento útil (un soundbite, sacar el arranque muerto, recortar el final).

```bash
# Corte preciso (re-encode, frame-accurate) del seg 5.2 al 18.7
ffmpeg -ss 5.2 -to 18.7 -i input.mp4 -c:v libx264 -crf 18 -preset medium -c:a aac -b:a 192k out.mp4

# Corte rápido sin re-encode (corta en keyframes, menos preciso)
ffmpeg -ss 5.2 -to 18.7 -i input.mp4 -c copy out.mp4
```

---

## 2. Concatenar

Para qué: unir varios clips en una pieza.

- **Mismo formato exacto** (res/fps/codec/timebase iguales) → concat demuxer con `-c copy` (rápido, sin pérdida).
- **Formatos distintos** (fps/res/codec dispares) → **concat filter** (re-encode; homogeneiza). Requiere misma **resolución** entre inputs.

```bash
# concat demuxer (homogéneos)
printf "file 'a.mp4'\nfile 'b.mp4'\n" > list.txt
ffmpeg -f concat -safe 0 -i list.txt -c copy out.mp4

# concat filter (heterogéneos; ej: pegar un clip de 30fps a uno de 31.58fps)
ffmpeg -i a.mp4 -i b.mp4 \
  -filter_complex "[0:v][0:a][1:v][1:a]concat=n=2:v=1:a=1[v][a]" \
  -map "[v]" -map "[a]" -c:v libx264 -crf 18 -preset medium -pix_fmt yuv420p -c:a aac -b:a 192k out.mp4
```

---

## 3. Cambiar velocidad

Para qué: acelerar partes lentas, ralentizar un momento, ajustar a una duración.

`setpts` mueve el video, `atempo` el audio — **deben quedar en sync** (factores inversos).

```bash
# 2x más rápido (video PTS ×0.5, audio tempo ×2)
ffmpeg -i in.mp4 -filter_complex "[0:v]setpts=0.5*PTS[v];[0:a]atempo=2.0[a]" -map "[v]" -map "[a]" out.mp4

# 0.5x cámara lenta (video PTS ×2, audio tempo ×0.5)
ffmpeg -i in.mp4 -filter_complex "[0:v]setpts=2.0*PTS[v];[0:a]atempo=0.5[a]" -map "[v]" -map "[a]" out.mp4
```

`atempo` válido entre 0.5 y 2.0 por instancia → para más, encadená (`atempo=2.0,atempo=2.0` = 4x). Para ramps de velocidad variable se segmenta y reconcatena.

---

## 4. Reframe / Aspect ratio / Rotación

Para qué: pasar vertical↔horizontal, recortar a otro aspecto, fijar rotación.

```bash
# Vertical 9:16 → horizontal 16:9 con letterbox (sin recortar)
ffmpeg -i in.mp4 -vf "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2:black" out.mp4

# Horizontal → vertical 9:16 recortando al centro (crop)
ffmpeg -i in.mp4 -vf "crop=ih*9/16:ih,scale=1080:1920" out.mp4

# "Hornear" la rotación y limpiar metadata (si un player la ignora)
ffmpeg -i in.mp4 -vf "scale=iw:ih" -metadata:s:v:0 rotate=0 out.mp4
```


---

## 5. Captions (transcribir → **corregir** → quemar)

Para qué: subtítulos legibles sincronizados. **Whisper da timing + texto; vos corregís el texto antes de quemar.**

```bash
# (a) Transcribir con Whisper a SRT (español, líneas cortas, 2 líneas máx)
WH="$(command -v whisper)"   # openai-whisper CLI (uv sync --extra media)
"$WH" input.mp4 --model small --language es --task transcribe \
  --word_timestamps True --max_line_width 26 --max_line_count 2 \
  --output_format srt --output_dir srt --fp16 False
#   modelos cacheados típicos: tiny/base/small/large-v3.
#   ⚠️ large-v3 en CPU acá es inviable (lentísimo) → usá small y CORREGÍ el texto a mano.

# (b) Revisar y corregir el .srt (errores de palabra, puntuación, nombres). Guardar en srt_fixed/.

# (c) Quemar con estilo legible, PlayRes correcto (scripts bundled de este skill)
bash scripts/burn-captions.sh input.mp4 srt_fixed/sub.srt <W> <H> <fontsize> <marginV> out.mp4 [bold] [FontName]
#   Ej. vertical 576x1024 Georgia serif: ... 576 1024 38 130 out.mp4 0 Georgia
#   El script genera el .ass con PlayRes=WxH (fontsize/margen en px reales) y quema con libass.
```

Estilo legible (lo que hacen los scripts): blanco, **contorno + sombra** para contraste, **lower-third** que no tape caras, fuente acorde al pedido. Color/fuente/tamaño/posición son **parámetros** — elegilos según lo que el user busca.

> Sistema de clases/CSS para HyperFrames: `ai-video-production/CAPTIONS.md`.

---

## 6. Música + mezcla + mastering

Para qué: música de fondo que **no tape la voz**, niveles equilibrados, loudness de plataforma.

```bash
# Música con ducking automático bajo la voz (sidechaincompress)
ffmpeg -i video.mp4 -stream_loop -1 -i music.mp3 \
  -filter_complex "[1:a]volume=0.20[m];[m][0:a]sidechaincompress=threshold=0.04:ratio=8:attack=5:release=400[md];[0:a][md]amix=inputs=2:normalize=0[mix]" \
  -map 0:v -map "[mix]" -shortest -c:v copy -c:a aac -b:a 192k out.mp4

# Master final a -14 LUFS (Instagram) — 2-pass, validado
bash <ruta>/ai-video-production/templates/scripts/master-audio.sh out.mp4 final.mp4
```

**Niveles por capa (mezcla editorial canónica):** voz **−5 dB** · SFX **−10 dB** · música **−16 dB** (memoria `feedback_audio_mix_tiers_editorial`). La voz manda; lo demás vive debajo.

> Autoridad: `ai-video-production/AUDIO-MASTERING.md` (receta loudnorm 2-pass + tabla de mix).

---

## 7. SFX

Para qué: acentos sonoros (whoosh en cortes, impacto, ambiente).

- **Primero reusá** lo que ya hay: `library/sfx-catalog.json` + `transitions/<fmt>/audio-stings/`.
- Si falta, **generá con ElevenLabs** (cuesta → Plan-First):

```bash
.venv/bin/python scripts/sfx.py -t "<prompt en inglés, dry, single event>" -d 1.0 -i 0.5 -o assets/sfx/name.mp3
```

> Autoridad: `ai-video-production/SFX-PIPELINE.md` (prompts validados, loop para ambientes).

---

## 8. Transiciones

Para qué: conectar clips/beats con intención (corte seco, blend, flash, glitch…).

**Consultá primero el catálogo:** `transitions/catalog.json` (15 transiciones: universal + por formato). Cada una trae su recipe + sting de audio.

```bash
# Cross-fade 0.5s entre dos clips, con offset = (duración clip A − 0.5)
ffmpeg -i a.mp4 -i b.mp4 \
  -filter_complex "[0:v][1:v]xfade=transition=fade:duration=0.5:offset=19.5[v];[0:a][1:a]acrossfade=d=0.5[a]" \
  -map "[v]" -map "[a]" -c:v libx264 -crf 18 -c:a aac out.mp4
#   transition= fade | fadeblack | fadewhite | wipeleft | slideup | hlslice (glitch) | circleopen ...
```

> Catálogo + helper multi-clip: `transitions/README.md` + `ai-video-production/templates/scripts/apply-effects-between-clips.py`. Default de ritmo: el hard-cut es el workhorse; reservá flash/glitch para momentos puntuales.

---

## 9. Texto / Lower-thirds / Títulos

Para qué: nombre+rol del que habla, título de sección, kicker, CTA.

```bash
# Lower-third de texto con caja (drawtext) entre seg 1 y 6
ffmpeg -i in.mp4 -vf "drawtext=fontfile='/System/Library/Fonts/Supplemental/Georgia.ttf':\
text='Nombre — Rol':fontcolor=white:fontsize=42:box=1:boxcolor=black@0.5:boxborderw=16:\
x=60:y=h-180:enable='between(t,1,6)'" -c:a copy out.mp4
```

Para overlays más ricos (animados, branding, logos) está la vía HyperFrames/GSAP, o renderizar un PNG con alpha y superponer con `overlay`. 


---

## 10. Color / LUTs

Para qué: darle carácter (cálido/cinematográfico, brillante/creator, frío).

**Consultá `filters/catalog.json`** (LUTs `.cube` disponibles: `wildebeast` warm, `gazelle` bright, …).

```bash
# Aplicar un LUT
ffmpeg -i in.mp4 -vf "lut3d=filters/luts/wildebeast.cube" out.mp4

# LUT a intensidad parcial (blend 50%)
ffmpeg -i in.mp4 -vf "split[a][b];[b]lut3d=filters/luts/gazelle.cube[g];[a][g]blend=all_expr='A*0.5+B*0.5'" out.mp4

# Ajustes finos sin LUT
ffmpeg -i in.mp4 -vf "eq=contrast=1.1:saturation=1.05:brightness=0.02" out.mp4
```

> Autoridad: `ai-video-production/COLOR-GRADING.md`.

---

## 11. Ritmo (pacing)

Para qué: chequear que el montaje no sea ni plano ni epiléptico.

```bash
bash <ruta>/ai-video-production/templates/scripts/check-pacing.sh out.mp4
# detecta hard cuts/min (banda de referencia short-form: 2-7 cuts/min "duros")
```

> Autoridad: `ai-video-production/PACING-MARKERS.md`.

---

## 12. QA + Entrega

Antes de declarar listo:

```bash
# Frames de verificación (ver captions, overlays, color en distintos puntos)
ffmpeg -v error -ss <t> -i final.mp4 -frames:v 1 /tmp/verify.jpg -y

# Duración / dimensiones / codec (confirmar mp4 estándar)
ffprobe -v error -show_entries format=duration -of default=nk=1:nw=1 final.mp4
ffprobe -v error -select_streams v:0 -show_entries stream=width,height,codec_name -of csv=p=0 final.mp4

# LUFS final (debe dar ≈ -14 ±0.5)
ffmpeg -i final.mp4 -af loudnorm=I=-14:TP=-1:LRA=11:print_format=summary -f null - 2>&1 | grep -i "Input Integrated"
```

Entregá copias nuevas en una carpeta clara, decí **dónde quedaron**, reportá **qué hiciste**, y **flageá lo incierto** (ej: líneas de caption que no pudiste verificar contra el audio — el user sabe qué se dijo).

---

## Scripts de QA reutilizables (opcionales)

En `ai-video-production/templates/scripts/` hay validadores que podés correr sobre el render: `audit-mix-volumes.py`, `audit-caption-temporal-coverage.py`, `audit-sfx-audibility.py`, `audit-clip-timing-vs-audio.py`, `qa-gate.py`. Usalos cuando el trabajo lo amerite (no son obligatorios para un caption job chico).
