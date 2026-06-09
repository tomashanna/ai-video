# A/B Video 1 — BRIEF CONGELADO (input idéntico a ambos brazos)

> **Este es el INPUT del experimento, no el SPEC.** Define el seed creativo + las
> constraints fijas (rotación + herencia V7). Lo que NO está acá (personajes, nombres,
> narración exacta, dilemas, shot direction de 7 dimensiones, los traps concretos) es
> **trabajo del arquitecto** — y es exactamente lo que el A/B compara entre v1 y v2.
>
> **Regla de pre-registro (AB-TEST-PROTOCOL §6)**: este brief NO se modifica una vez que
> arrancó el primer brazo. Si cambia, el experimento se invalida. Git lo deja verificable-
> idéntico en `AI video 1/` (v1) y `AI-video-1-v2/` (v2).

---

## Seed creativo

| Eje | Valor | Origen |
|---|---|---|
| **Género** | horror-choice | decisión A/B (video 1) |
| **Pattern** | **P3 — "Seguro era trampa"** (el *bueno aparente*, el que parecía la opción segura, es el peligro real — canónico ref-08 Pablo traidor) | rotación V8: descansado, último P3 hace 4 videos (cinema-abandonado) |
| **Apariencia dyad** | **Simétrica monstruosa (M/M)** — los DOS compañeros dan miedo; ninguno es el "amable obvio" | rotación V8: asimétrica (V7) + doble-monstruosa (V5) + doble-amable (V6) recién usadas → M/M descansada |
| **Setting** | **Criadero / granja avícola industrial nocturno** — galpón de engorde, hileras infinitas de jaulas con aves vivas hacinadas, cintas transportadoras de alimento, luz cenital parpadeante, turno 3 AM. Horror de la **confinación industrial de vida viva** (NO matanza/carcasas) | virgen (ningún setting de granja/ganadería usado); afín a la receta industrial de V7 |
| **Premisa P3** | Dos cuidadores entre las jaulas, ambos antinaturales. Elegís compañero; el que **parece seguir el procedimiento / te ofrece la salida** te lleva a la cinta de procesado. El que parecía la apuesta más segura era la trampa. | — |

## Constraints fijas (idénticas a ambos brazos)

- **Delivery**: reel vertical 9:16, 1080×1920, 30fps.
- **Duración**: target ~90-100s (V7 = 111s y no penalizó; banda 80-110s).
- **POV**: primera persona, manos del viewer visibles, nunca wide del protagonista.
- **Idioma**: español neutral (tú/eliges/decides — NUNCA voseo).
- **Estructura**: hook dyad → played path (2-3 decisiones internas con countdown + botones A)/B)) → counterfactual al final → cliffhanger "Paz perdida".
- **Invariante**: el bueno-aparente NUNCA decide en el camino jugado.

## Receta heredada de V7 (mejores métricas de la cuenta — usar como piso)

- **Hook**: kling 2.5 pro, interactivo (un personaje habla/actúa), con CTA narrado "Elige a tu compañero, X o Y".
- **Animación**: primeros 30s = AI obligatoria; clímax kling pro, resto hailuo std; perseguir execution-continuity (traslado POV físico real entre shots, cero teleport — fue el 10/10 de V7).
- **SFX**: densos + audibles, per-clase normalizado dBFS, licencia diegética (si se ve, suena), duck bajo voz. Reusar `library/sfx/general/` + generar lo del setting (cacareo/aleteo/jaulas/cinta/maquinaria).
- **Audio**: HR#31 voice-exclusivity (narrador y personaje NUNCA simultáneos), -14 LUFS, 48kHz.
- **Captions**: Whisper, caption-hide durante countdown, death-shots SIN caption.
- **UI**: countdown FILM LEADER ACADEMY, loading bar Y52, name labels Y11.5 monospaced.

## Watch-items (idénticos a ambos brazos — el rail los respalda)

1. **Distinctness vs matadero (#7)**: matadero = matanza, carcasas colgando, matarife + cocinera. Este = **aves VIVAS hacinadas + cuidadores**. Mantener `signature_staging` distinto; `audit-spec-narrative-coherence` hard-blocks ≥0.85 similarity, flag 0.75-0.84.
2. **M/M no es asimétrico**: ambos cuidadores deben dar miedo; resistir el default de hacer "uno amable + uno siniestro".
3. **P3 coherente**: el twist "el seguro era la trampa" debe cumplir las 3 condiciones (lógica clara + imágenes acompañan + narración explica el link).

---

## Cómo se corre (AB-TEST-PROTOCOL)

1. **Brazo v1 PRIMERO** (control): sesión FRESCA en `AI video 1/` → "diseñá el horror-choice de `AB-VIDEO-1-BRIEF.md`" → arquitecto (CLAUDE.md prescriptivo) diseña SPEC → flujo CP1-CP5 con gates de auditor → render.
2. **Brazo v2 después**: sesión FRESCA en `AI-video-1-v2/` → mismo prompt → arquitecto (router + `agents/ARCHITECT.md`) diseña SPEC → mismo flujo.
3. **NUNCA** la misma sesión/contexto sirve a ambos brazos (invalida, §6). Sesiones frescas, naive al experimento.
4. **Logging por CP** (§3.4): iteraciones, bugs por catcher (gate/auditor/Tomás), minutos de Tomás, costo, reglas inventadas.
5. Evaluación **A CIEGAS** de los 2 renders → regla de decisión §5.
