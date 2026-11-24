# IMAGE-VARIETY.md — Variedad visual obligatoria

> Cualquier escena que se muestra >4s en un video con IA necesita 2-3 variantes de imagen. Reusar el mismo PNG produce slideshow feel — **especialmente** cuando se aplica motion (parallax/Ken Burns delata la repetición todavía más). Esta regla aplica a CUALQUIER formato de video con IA.
>
> **Complemento obligatorio**: `CHARACTER-CONSISTENCY.md`. Variedad de PLANOS pero MISMA identidad del personaje. Las variantes -a/-b/-c se generan con `--ref <anchor>` para que el personaje no mute entre tomas.

---

## La regla (origen: post-mortem bosque-abandonado v2, 2026-05-09)

Detectado por Gemini Video Analyzer: "PowerPoint narrado, no cine". 17 fotos fijas reutilizadas, mismo PNG hasta 10 veces. Cuando aplicas motion sobre esa reutilización, el ojo nota inmediatamente que es la misma imagen — y rompe la inmersión.

---

## Cuándo generar variantes

| Duración total de la escena en el video | Variantes mínimas |
|---|---|
| ≤ 4s | 1 (no requiere variantes) |
| 4–8s | 2 (`-a`, `-b`) |
| > 8s | 3 (`-a`, `-b`, `-c`) |

**Importante**: contar la duración total que la escena ocupa en el video, no la duración de cada caption individual. Si `forest-walk` aparece en 4 captions de 2-3s cada una sumando 10s totales, son 3 variantes.

---

## Cómo diseñar las variantes — CRÍTICO

> **Aprendizaje 2026-05-10 (mina-abandonada v1 test)**: Una versión más vieja de esta regla decía "cambiar ángulo/distancia/framing". Eso produce variantes **demasiado similares** que se siguen sintiendo como slideshow cuando se aplica motion. Gemini QA no lo detectó pero el usuario humano sí: "varias imágenes diferentes pero iguales".

**La regla correcta:** cambiar el **TIPO DE PLANO** (shot type), no solo el framing del mismo plano.

Mantén constantes: escenario, personajes, paleta de color, iluminación general.
Cambia: **qué muestra el plano** (sujeto, encuadre, lente, perspectiva).

### Catálogo de tipos de plano (elegir 2-3 distintos por escena)

| Tipo de plano | Qué muestra | Cuándo usarlo |
|---|---|---|
| **Wide POV** | El espacio completo, sujeto en el frame | Setup de escena |
| **Medium shot** | Sujeto al centro, contexto visible | Acción del sujeto |
| **Close-up rostro** | Cara del personaje, ojos en foco | Diálogo cripto / amenaza |
| **Close-up detalle** | Objeto / textura / mano / herida / inscripción | Tensión sostenida |
| **Plano lateral** | Sujeto de perfil, paralelo a la cámara | Movimiento / progresión |
| **Plano picado (high angle)** | Mirando hacia abajo | Vulnerabilidad / opresión |
| **Plano contra-picado (low angle)** | Mirando hacia arriba | Amenaza dominante |
| **POV detalle suelo/manos** | Lo que el espectador "ve" de sí mismo | Inmersión 1ra persona |
| **Plano ambiental sin sujeto** | Solo escenario | Mood / atmósfera |

### Ejemplo correcto vs incorrecto

#### ❌ MAL — variantes de la misma toma (lo que NO hay que hacer)

| Variante | Tipo de plano |
|---|---|
| `h3-walk-a` | Wide POV caminando, sujeto a 3 pasos |
| `h3-walk-b` | Wide POV caminando, sujeto a 5 pasos |
| `h3-walk-c` | Wide POV caminando, low angle |

Las 3 son la MISMA toma con variaciones de framing. Sigue siendo slideshow.

#### ✅ BIEN — tipos de plano distintos

| Variante | Tipo de plano |
|---|---|
| `h3-walk` | Wide POV caminando, sujeto a 3 pasos |
| `h3-beam-detail` | Close-up detalle: viga de madera agrietada con polvo cayendo |
| `h3-lamp-flicker` | Close-up detalle: lámpara de carbono parpadeando |

3 planos completamente distintos pero coherentes en escenario, personajes y mood. **Esto sí engancha al espectador.**

### Cuántos planos por escena (no variantes, planos)

| Duración total de la escena | Planos mínimos distintos |
|---|---|
| ≤ 4s | 1 |
| 4–8s | 2 (de tipos diferentes — ej: wide + detalle) |
| > 8s | 3 (de tipos diferentes — ej: wide + close-up rostro + detalle) |
| > 15s | 4-5 (escena rica — agregar lateral o low angle) |

### Patrón validado en videos virales (REFERENCE-ANALYSIS)

Los 3 videos de `@referent-a` usan **5 tipos de plano por hito**, no 5 variantes del mismo:

1. **Wide del escenario** (setup, POV entrando)
2. **Close-up del personaje** (advertencia, diálogo cripto)
3. **Close-up del elemento de tensión** (objeto, monstruo, herida)
4. **Plano de la consecuencia mala** (twist malo)
5. **Plano de la consecuencia buena** (twist bueno / salida)

Cada uno responde a una FUNCIÓN narrativa distinta. **No hay variantes de "wide del escenario" repetidas** — hay UN wide y luego se va a otro tipo de plano.

### Cómo decidir el plan de planos para una escena nueva

Para cada escena del NARRATIVE.md, pregúntate:

1. ¿**Qué muestro primero**? (típicamente wide para establecer)
2. ¿**Qué necesita atención**? (un objeto, un rostro, un detalle) → close-up de eso
3. ¿**Qué emoción quiero**? (vulnerabilidad → picado, amenaza → contra-picado, claustrofobia → close-up apretado)
4. ¿**Hay un detalle que el espectador debería notar**? (una grieta, una sombra, una textura) → close-up detalle

Cada respuesta = un plano distinto = una imagen distinta a generar.

---

## Comando (paralelo)

Las generaciones se pueden lanzar en background simultáneamente. Gemini Nano Banana tolera 3-5 RPM concurrente:

```bash
# Variante principal
uv run ai-video image -p "[PROMPT_A]" -o assets/scene-a.png &

# Variantes B y C en paralelo
uv run ai-video image -p "[PROMPT_B_distinta_distancia]" -o assets/scene-b.png &
uv run ai-video image -p "[PROMPT_C_distinto_ángulo]"    -o assets/scene-c.png &
wait
```

Tiempo total: ~10-30s para 3 variantes (en paralelo).

---

## Naming + symlinks

### Naming canónico

```
assets/
  scene-a.png   ← variante principal (la "default")
  scene-b.png   ← segundo ángulo
  scene-c.png   ← tercer ángulo (si aplica)
```

### Symlinks de backward-compat

Si renombrás un asset existente (`scene.png → scene-a.png`) para empezar a usar variantes, **dejá un symlink** para no romper composiciones previas:

```bash
cd assets/
mv scene.png scene-a.png
ln -sf scene-a.png scene.png
```

Sin esto, cualquier `index.html` que referenciaba el nombre antiguo va a fallar con `media_missing_src` en el render.

---

## Wiring en `index.html`

Alternar variantes cada 2-3s dentro de la misma escena:

```html
<img id="scene-shot-1" src="assets/scene-a.png" class="scene-image clip"
     style="opacity:0;" data-start="19.0" data-duration="3.0" data-track-index="20" />
<img id="scene-shot-2" src="assets/scene-b.png" class="scene-image clip"
     style="opacity:0;" data-start="22.0" data-duration="3.0" data-track-index="21" />
<img id="scene-shot-3" src="assets/scene-c.png" class="scene-image clip"
     style="opacity:0;" data-start="25.0" data-duration="2.7" data-track-index="22" />
```

Cada variante toma un `data-track-index` distinto. Aplicar Ken Burns + parallax (ver `MOTION-LAYER.md`) a cada una por separado.

**Opcionalmente** usar las 3 variantes como capas de parallax dentro del mismo plano (cada una con `data-depth` distinto).

---

## Budget orientativo

| Cantidad | Costo en Gemini Nano Banana (paid tier) |
|---|---|
| 1 imagen | ~$0.04 |
| Video con 12-15 escenas y variantes (~20-25 imágenes totales) | ~$0.80-1.00 |
| Solo el "extra" de variantes (+5-8 imágenes) | ~$0.20-0.40 |

---

## Anti-patrones a evitar

- ❌ **Reusar la misma imagen para múltiples captions de la misma escena** — slideshow feel garantizado.
- ❌ **Generar variantes con escenarios distintos** — rompe continuidad ("¿estaba en bosque, ahora está en casa?")
- ❌ **Cambiar la iluminación o paleta entre variantes de la MISMA escena** — el ojo notará el cambio como un corte, no como motion.
- ❌ **Saltar la regla en escenas "pequeñas"** — incluso una escena de 5s reutilizada se siente como diapositiva si lleva motion.

---

## Cuándo está OK con 1 sola imagen

- Plano de ≤4s (incluyendo Ken Burns)
- Imagen tan icónica que la repetición es intencional (ej: misma cara en close-up usada solo 1 vez)
- Cliffhanger final donde el plano se sostiene como "still" emocional

---

## Workflow recomendado

1. **Durante la escritura del guion**: anotar duración estimada de cada escena en el video final
2. **Calcular variantes mínimas** por escena según la tabla
3. **Agregar las variantes al asset list** del proyecto (NARRATIVE.md o equivalente)
4. **Diseñar los 2-3 prompts** por escena cambiando solo ángulo/distancia/framing
5. **Generar en paralelo** (3-5 RPM)
6. **Wire en index.html** alternando cada 2-3s
7. **Aplicar motion** sobre cada variante por separado (parallax, Ken Burns, etc.)
