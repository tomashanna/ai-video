# CHOICE-MECHANIC.md — La mecánica AGNÓSTICA del formato "Elige a tu compañero"

> **AUTORIDAD CREATIVA agnóstica de la familia CHOICE** (rol 🏛️ ARQUITECTO de cualquier género choice). Define la MECÁNICA común a todos los géneros choice — la estructura, el invariante, la dinámica de decisión, el framing y la lente de lectura. NO contiene sabor de género.
>
> **Heredan de este doc:** `horror-choice-format/PAUTA-MASTER.md` (sabor horror) y `sport-choice-format/PAUTA-MASTER.md` (lógica deportiva). Si un doc de género y este discrepan sobre la MECÁNICA → gana este doc. Si discrepan sobre el SABOR → manda el género.
>
> **Lineaje empírico:** la mecánica acá deriva del análisis de **8 videos virales canónicos** del formato "Elige a tu compañero" (vía `horror-choice-format/PAUTA-MASTER.md`, validada con compliance N/8). Lo que era ejemplo horror se generalizó a género-neutro; lo que es sabor horror se dejó en el skill de horror.
>
> **Última actualización:** 2026-06-01 (creación — extracción agnóstica).

---

## §0 — METODOLOGÍA (framework empírico genérico)

### Marco de lectura (anti reglas binarias)

Toda elección creativa se expresa como **🟦 PRINCIPIO (mandatorio) / 🟩 VARIABILIDAD (libre) / 🟥 ANTI-PATTERN (evitar)**, NUNCA como regla binaria rígida. Si algo acá suena a "regla rígida" sobre una elección creativa, es un bug de framing.

### Cómo se valida una regla de mecánica

- 🟦 Una regla es **PRINCIPIO** (invariante de la familia choice) solo si se cumple en la base empírica del género que la valida (en horror: 7/8 o más de los 8 virales canónicos). En esos casos la regla lleva la nota "validado N/8 (vía horror)".
- 🟩 Lo que varía libremente entre videos NO es regla — es el espacio creativo. No lo conviertas en regla rígida.
- 🟥 Lo que rompe el formato observado en los virales = anti-pattern; nunca hacerlo.
- Un género **pre-empírico** (p. ej. sport antes de tener sus propios virales) HEREDA los principios validados de la mecánica y valida su LÓGICA de género con sus propios videos. No tratar la lógica de género pre-empírica como "validada" antes de shippear.

> **El contenido CONCRETO de cada regla es de género** (settings, personajes, tipos de consecuencia, paleta, SFX). Acá vive la FORMA abstracta de la mecánica, no el relleno.

---

## §1 — FILOSOFÍA: la regla de oro

> 🟦 **El formato es el GENERADOR de creatividad, no el LÍMITE.** El espectador viene por la fórmula reconocible (dyad, countdown, dilema binario, consecuencia, counterfactual, cliffhanger/CTA). La creatividad vive en QUÉ poblamos esos slots, no en romperlos.
>
> **Si te encontrás queriendo romper el formato, el problema es tu historia, no el formato.**

Validado 8/8 (vía horror): ningún video viral rompe la estructura. Toda la variación vive en los slots.

> 🏛️ **Autoridad ESTRUCTURAL + invariante:** el esqueleto canónico (hook → played-path → counterfactual → cliffhanger) y el INVARIANTE (§2.2) son check auditable. Los 3 roles lo usan: el arquitecto diseña contra esto · el ingeniero ejecuta los specs de UI/efecto/sonido · el auditor compara el guion beat-por-beat.

---

## §2 — ESTRUCTURA TEMPORAL (el esqueleto agnóstico)

### Duración total

- 🟦 **Sweet spot:** **~80-100s** (rango observado 76-129s en los 8 virales horror; promedio ~97s). Fuera del rango cae la retención.
- 🟩 El género puede mover el sweet spot dentro de razón (sport default ~86-100s). No salir del rango sin justificación.

### 2.1 Esqueleto canónico (validado 5/5 refs auditados vía horror)

```
1. HOOK            dyad "elige a tu compañero" (dos opciones presentadas SIMULTÁNEAMENTE)
                   + name labels GRANDES sobre cada opción (§2.5)
                   + countdown 3-2-1
2. RECORRIDO JUGADO   el de la opción ELEGIDA
   · setup           se establece el contexto del recorrido
   · DECISIÓN 1/2/3  →  consecuencia ✗ (dead-end corto)  /  consecuencia ✓ (continúa el path)
   · la última decisión cierra con RESOLUCIÓN del path
3. RECORRIDO COUNTERFACTUAL   el de la OTRA opción (la NO jugada): se muestra UNA vez —
                              al FINAL (default) o al INICIO (variante).
4. CLIFFHANGER / tagline loop (CTA verbal)
```

- 🟦 **Decisiones por video: 2-3 internas + la decisión inicial "elegir compañero" = 3-4 total.** Cada decisión SIEMPRE muestra ambas ramas (✗ dead-end + ✓ continúa).
- 🟦 **El hook SIEMPRE incluye el CTA narrado de elección** — la invocación verbal de agencia "Elige a tu compañero, [X] o [Y]" (con los dos nombres del dyad). NO es decorativo: **es LA mecánica del formato** — convierte al viewer de espectador en decisor desde el segundo 1, y nombra explícitamente las dos opciones que verá en pantalla. Un hook que solo muestra el dyad sin invocar la elección hablada rompe el contrato del formato. 🟩 El fraseo exacto del CTA es libre (y de género — ver §6 + el skill del género).
- 🟩 Qué decisiones, qué consecuencias y el orden del counterfactual (final = default / inicio = variante) varían por video.

### 2.2 ⛔ EL INVARIANTE (validado 5/5 refs vía horror) — el check más importante del SPEC-AUDIT

🟦 **La opción de apariencia-favorable (la opción NO jugada / la del counterfactual) NUNCA está presente en el RECORRIDO JUGADO tomando decisiones con el viewer.**

> Genéricamente: *la opción favorable-aparente* = en horror el **"bueno aparente"**; en sport el **rival / la otra estrella (el foil)**. El nombre del rol es de género; el invariante es agnóstico.

- Aparece SOLO en: el **hook** (dyad de presentación) + su **recorrido counterfactual** + opcional el **cliffhanger**.
- En el recorrido jugado, las tentaciones / órdenes / desafíos vienen de la **opción ELEGIDA** + del **instinto del viewer / el entorno** — NUNCA de la opción NO jugada estando presente y decidiendo.
- Los dos recorridos (jugado + counterfactual) son 🟦 **SECUENCIALES, jamás simultáneos**.

🟥 **VIOLACIÓN = error que retorna al arquitecto.** Si la opción rechazada sigue decidiendo con el viewer, colapsa la premisa "elegiste a X" + diluye el pattern a un genérico "dos personajes presentes". (Caso disparador vía horror V6: la opción rechazada tentando dentro del played path; el arquitecto y el auditor lo racionalizaron en vez de flaggearlo.)

### 2.3 Recorridos secuenciales (variabilidad libre)

El esqueleto + el invariante son fijos. 🟩 Varía (decisión creativa del arquitecto): **quién es cada rol del dyad** + el **pattern** (§15 + rotación → `ROTATION-RULES.md`) · **qué recorrido se muestra primero** (counterfactual al final = default / al inicio = variante) · **qué decisiones y consecuencias** · **setting / characters / paleta** (todo esto = sabor de género).

### 2.4 ⭐ SPEC-AUDIT — los ejes agnósticos que el auditor mira en CADA guion

El SPEC-AUDIT compara el guion **beat-por-beat contra el esqueleto** + chequea (parte agnóstica):

1. **Estructura** §2.1 (🔴 si falta un bloque del esqueleto)
2. **INVARIANTE** §2.2 (🔴 si la opción favorable-aparente está en shots de decisión/consecuencia del played path)
3. **Recorridos secuenciales** (🔴 si se mezclan)
4. **Pattern + rotación** (∈ patterns del género + ≠ último video → `ROTATION-RULES.md`)
5. **Name labels** §2.5 (grandes + visibles through-countdown)
6. **Framing acción-condicional** §3 (marca la rama sin bare label robótico)
7. **"Orden hablado = orden de botones"** §3
8. **Narración-fits-duration** (la narración a ~165 WPM entra en la duración del shot y dentro del clip_max del modelo i2v — autoridad técnica `ai-video-production/MODEL-CAPABILITIES-MATRIX.md`)

> Los ejes de SONIDO/efecto/visual concretos (densidad de SFX, death-screams o rugidos, paleta, etc.) son **de género** — los mira el SPEC-AUDIT del skill de género, no este eje agnóstico. La parte agnóstica se enforza con los validators estructurales; el arquitecto los corre pre-emit, el auditor los re-corre. ✅ **Estado (2026-06-01)**: `audit-spec-structure-vs-canonical.py` está generalizado a la **familia choice** (`CHOICE_FAMILY = horror-choice, sport-choice`) → enforza este invariante para sport-choice también (resuelve la opción favorable-aparente por formato: bueno-aparente en horror / foil-rival en sport). `audit-spec-narrative-coherence.py` (gated `interactive_choice`) corre en paralelo. Los ejes de GÉNERO (SFX/LUT/narrador/no-horror) los cubre `sport-choice-format/NO-HORROR-GUARD.md` + `audit-spec-genre-fidelity.py`.

### 2.5 UI canon — name labels (creative intent)

🟦 Name labels **arriba de cada opción del dyad**, **letra GRANDE** (`fontsize_intent: large`). **Visibles desde el inicio de la intro Y DURANTE todo el countdown** — NO desaparecen al arrancar el countdown. Monospaced + drop-shadow.

Schema: `ui_active` name-label por opción con `timestamp_visible_s: [0, fin-del-countdown]` + `position` arriba de cada una. El "cómo" técnico → `INGENIERO-CHOICE-CORE.md § UI safe zones / name labels`.

---

## §3 — REGLAS DE LENGUAJE + DECISIÓN (subset agnóstico; el resto es de género)

> **Conservador:** este doc extrae SOLO las sub-reglas claramente agnósticas. Las sub-reglas de sabor (body horror específico, sonido-de-muerte sutil, épica de gol, etc.) se quedan en el skill de género.

### Lenguaje (agnóstico)

- 🟦 **Segunda persona presente:** "tú trabajas, miras, eliges / tú avanzas, pasas, decides" (no futuro).
- 🟦 **Español NEUTRAL** (tú / dices / eliges / decides). NUNCA voseo argentino (vos / decís / elegís). Audiencia internacional.
- 🟦 **Oraciones cortas y claras.** Pocas palabras que digan QUÉ pasa (acción) o den contexto.
- 🟦 **Narración CLARA, no estilizada.** El estilo (tenebroso en horror / épico en sport) emerge del **visual + SFX + música**, NO de la narración. Estilismo > claridad = bug del formato: si el viewer no entiende qué pasa en 1ª escucha sin caption → reescribir.
- 🟩 **Frases nominales sin verbo** reservadas al climax peak (no para setup/consecuencia, que siempre llevan sujeto+verbo+conexión causal).

### Framing acción-condicional — marcar la rama (agnóstico, corregido vs primary source)

> Esto NO es "Si elegiste X literal" (paráfrasis sintética) sino un PRINCIPIO con variabilidad.

- 🟦 **PRINCIPIO (mandatorio):** toda consecuencia marca a qué rama pertenece (sin esto el viewer se pierde). Un caption marcador-puente ("SI ELEGISTE B:") es válido, no el único compliance.
- 🟩 **VARIABILIDAD (libre — todas canónicas en primary source):** acción condicional *"Si la enciendes / Si esperas / Si te niegas / Si la das al desmarcado…"* (DOMINANTE) · choice-reference *"Si decides… / Si escogiste…"* · branch por nombre *"Si elegiste a [opción]…"*.
- 🟥 **ANTI-PATTERN:** bare label robótico *"Si elegiste A" / "Si elegiste B"* solo (0/8 — suena a formulario).
- Sin marcar la rama, el choice colapsa a un género genérico (caso disparador vía horror: cabina-14 V1).

### "Orden hablado = orden de botones" (agnóstico)

- 🟦 **A = la primera opción nombrada en la narración.** B = la segunda. El orden hablado SIEMPRE coincide con el orden de los botones. Romperlo confunde al viewer sobre qué votó.

### Estructura de decisión (agnóstico)

- 🟦 **3-4 decisiones binarias** total (1 inicial "elegir compañero" + 2-3 internas).
- 🟦 **Cada decisión** tiene countdown 3-2-1 + barra de carga (loading bar).
- 🟦 **Hard cut** entre escenas (text on-screen NUNCA anima — hard cut only).
- 🟦 **Loading bar** entre decisiones (timing técnico → `INGENIERO-CHOICE-CORE.md`).

### Producción (agnóstico)

- 🟦 **POV (primera persona) ≥80% de los shots** — ENFORCEMENT obligatorio. El arquitecto cuenta shots POV vs non-POV en el SPEC y reporta el ratio en self-audit. El viewer ES el protagonista; nunca shots en 3ª persona donde el viewer se ve "a sí mismo".
- 🟦 **CTA narrado al final** (tagline loop reconocible cross-video).
- 🟦 **Watermark del creator** visible toda la duración.
- 🟦 **Caption del Reel** con pregunta directa ("¿A quién elegirías?") + hashtags.
- 🟦 **Lip-sync intent marcado por shot** (`lip_sync_required: true|false`): `true` si un personaje habla on-screen; `false` si solo hay narración voiceover. Si `false` → el ingeniero NO usa clip con boca visible moviéndose (regla técnica → `INGENIERO-CHOICE-CORE.md § lip-sync`). Caso disparador vía horror: personaje "habla" en clip animado mientras solo habla el narrador → disonancia.

---

## §4 — DECISIÓN → CONSECUENCIA (la dinámica de elección)

### La mecánica agnóstica

- 🟦 **✓ = continúa** el recorrido/jugada (sigue el plano hacia el desenlace del path).
- 🟦 **✗ = inserto corto dead-end** — la consecuencia negativa se muestra brevemente; luego el video sigue por el camino correcto.
- 🟦 Cada decisión SIEMPRE muestra ambas ramas.

### Transición narrativa explícita entre ramas (agnóstico)

- 🟦 **Después de cada decisión binaria debe haber transición narrativa explícita** entre la rama mostrada y el avance del path — NO solo el cliffhanger final. Si se muestra la consecuencia ✗, antes de avanzar al siguiente beat debe haber 1 línea o cue explícito ("Si hubieras elegido B / Vuelves al momento / Otra realidad") — sin esto el viewer queda perdido sobre cómo se pasó del dead-end al avance.
- Caso disparador vía horror (maikol-crucero): rama no-elegida no presentada → viewer confundido sobre cómo se vuelve al punto de decisión.

### La dinámica de control / desafío que testean los dilemas (Slot D agnóstico)

> El CONTENIDO de la dinámica es de género (la "regla del malo" en horror; la zona/jugada en sport). La FORMA es agnóstica.

- 🟦 **Hay una dinámica** — la opción elegida o el entorno siempre exige/desafía algo.
- 🟦 **Conecta con los dilemas** — cada dilema testea esa dinámica.
- 🟦 **No es moralmente obvia** — no es "no mates / no robes". El test correcto: **¿la decisión genera DUDA real?** Si la respuesta es obvia, el dilema está mal diseñado.
- 🟦 **Consecuencia inmediata si se rompe** (concreta y visualizable — el TIPO de consecuencia es de género).

---

## §5 — DILEMA-MECHANICS (Slot E agnóstico)

### Número de dilemas

- 🟦 **3-4 decisiones total** (1 inicial + 2-3 internas). Promedio observado ~3.4 (vía horror). NO solo 2.

### Estructura de cada dilema (validada 8/8 vía horror)

```
1. SETUP (1-2 oraciones) — qué se ofrece / qué se ve / qué pasa
2. PREGUNTA — "Ahora decide. A. [opción 1]  B. [opción 2]"  (orden hablado = orden de botones, §3)
3. COUNTDOWN — 3-2-1
4. LOADING BAR — barra mientras el viewer "elige"
5. CONSECUENCIA ✗ — dead-end corto (TIPO de consecuencia = de género)
6. CONSECUENCIA ✓ — apertura al siguiente dilema / avance del path
```

### Reglas de los dilemas (agnóstico)

- 🟦 **Duda real:** ambas opciones defendibles. Si una es obvia, no hay dilema (refuta "la ganadora SIEMPRE va contra el impulso" — NO es universal; lo universal es la DUDA).
- 🟦 **Variedad de categorías:** los dilemas dentro de un video deben ser de categorías diferentes (no todos del mismo tipo). Validado 8/8 vía horror.
- 🟥 **"B" no siempre correcta** — rotar qué opción paga entre videos.
- 🟩 **Ratio debatible:** ~1 de cada 3-4 decisiones deliberadamente debatible (fuel de comentarios / engagement).

> Las **categorías concretas** de dilema (curiosidad/obediencia, sumisión/resistencia en horror; regate/pase/definición en sport) son de género — ver el skill de género.

---

## §6 — COUNTERFACTUAL + CLIFFHANGER + CTA LOOP (Slot G — solo la ESTRUCTURA)

> ⛔ **Acá vive SOLO la estructura agnóstica.** Los **elementos sensoriales del cliffhanger son género-específicos** (en horror: café / pan / cartas / chimenea cozy = "Paz perdida"; en sport: gloria / trofeo / hinchada) — ver el skill de género.

### El counterfactual (estructura agnóstica)

- 🟦 **TODO video choice tiene un counterfactual** tipo "Si hubieras elegido X, habrías…": muestra el recorrido de la opción NO jugada. Validado 8/8 vía horror.
- 🟦 La opción favorable-aparente debe aparecer visualmente en **≥2 shots ANTES del cliffhanger** (hook + counterfactual mínimo) — no puede aparecer por primera vez en el outro, o no carga emocionalmente.

### Counterfactual placement (agnóstico — emotional framing es el diferenciador)

El diferenciador NO es el timestamp sino el **emotional framing**:

| Placement | Framing | Efecto | Recomendado |
|-----------|---------|--------|-------------|
| **BEFORE choice resolves** (counterfactual antes de cerrar el path principal) | `stakes_lift` | sube la tensión, contrasta los paths | ✅ **CANÓNICO preferido** |
| **Recorrido favorable AL FINAL** (alivio/contraste tras el path jugado) | `relief_contrast` | release emocional / contraste | ✅ variante canónica |
| **Parallel alternation** (cortar entre paths beat a beat) | — | mantiene tensión en ambos | ✅ variante aceptable |
| **AFTER both paths como "explicación retrospectiva"** | `retrospective_closure` | redundante (el viewer ya vio) | ⚠️ **CONDICIONAL anti-pattern** — funciona solo si se enmarca como alivio/contraste, falla si se enmarca como explicación redundante |

> SPEC schema: `narrative_structure.counterfactual_placement` ∈ `before_choice_resolves | twin_ending_good_alternate | good_path_at_end | parallel_alternation` (evitar `after_both_paths_retrospective`) + `emotional_framing` ∈ `stakes_lift | relief_contrast`.

### Estructura del outro (agnóstico)

```
1. Voz: "Si hubieras elegido a [opción no jugada]…"
2. Visual del recorrido no jugado (contraste tonal vs el path jugado — el TONO es de género)
3. Detalle específico (1-2 elementos — los elementos son de género)
4. Cierre con imagen final
5. Tagline + CTA loop: tagline reconocible cross-video → loop al próximo video
```

- 🟦 **CTA loop = tagline reconocible cross-video** + watermark persistente. (La frase concreta es de género — "Elige a tu compañero para…" / "Elige bien a tu compañero. Y vuelve mañana.")
- 🟦 **El cierre SIEMPRE repite el CTA de elección.** El video abre invocando la agencia (hook §2.1) y cierra repitiéndola — el bookend "Elige a tu compañero" es lo que hace al formato loopear (re-arma la decisión para el próximo video). Apertura sin cierre = se pierde el loop; cierre sin apertura = el viewer no entró como decisor. 🟩 fraseo libre / de género.

---

## §7 — PATTERNS NARRATIVOS (la FORMA abstracta; el CONTENIDO es de género)

> ⛔ El **contenido de cada pattern es género-específico** (en horror los archetypes P1-P10 con contenido de terror; en sport las configuraciones deportivas). Acá vive la FORMA abstracta como configuraciones de **apariencia × verdad**.

Un pattern choice es una configuración de **lo que cada opción APARENTA × lo que RESULTA ser**:

| Forma abstracta (apariencia × verdad) | Definición agnóstica |
|----------------------------------------|----------------------|
| **Verdad visible** | lo que aparenta peligroso/desfavorable ES desfavorable |
| **Supervivencia si manejás bien** | lo desfavorable-aparente puede sobrevivirse con decisiones correctas |
| **Lo amenazante te ayuda** | lo que parece amenazante es lo que te salva |
| **Lo seguro era trampa** | la opción favorable-aparente era el verdadero riesgo |
| **Hedonismo/atajo eterno** | la opción "buena" te lleva a placer/atajo pero perdés el objetivo |

- 🟦 El video declara qué configuración usa.
- 🟥 No repetir la misma configuración en 2 videos consecutivos → `ROTATION-RULES.md`.
- 🟩 El **relleno** de cada configuración (qué es cada opción, qué consecuencia, qué outcome) es 100% de género.

> Cada género mantiene su propio catálogo concreto de patterns (horror: P1-P10 con contenido de terror; sport: configuraciones deportivas). Este doc define solo la lente abstracta.

---

## §8 — CHECKLIST DE CALIDAD (subset agnóstico)

> **Conservador:** solo los ítems claramente agnósticos. Los ítems de personajes / consecuencia-de-género / paleta viven en el checklist del skill de género.

### Estructura
- [ ] Esqueleto §2.1 completo (hook dyad → played path → counterfactual → cliffhanger)
- [ ] INVARIANTE §2.2 respetado (la opción favorable-aparente NO decide en el played path)
- [ ] Recorridos secuenciales (no simultáneos)
- [ ] 3-4 decisiones (1 inicial + 2-3 internas), cada una de categoría diferente
- [ ] Cada decisión: countdown 3-2-1 + loading bar + ambas ramas (✗ dead-end + ✓ avance)
- [ ] Counterfactual presente + placement con emotional framing válido (§6)
- [ ] Duración ~80-100s

### Decisión / lenguaje
- [ ] Cada dilema genera DUDA real (ambas opciones defendibles)
- [ ] Framing acción-condicional marca la rama (sin bare label robótico)
- [ ] "Orden hablado = orden de botones"
- [ ] Segunda persona presente + español neutral + oraciones cortas claras
- [ ] Narración clara (el estilo emerge del visual/SFX/música, no del relato)

### Producción
- [ ] POV >80% de los shots
- [ ] Hard cuts entre escenas; text on-screen no anima
- [ ] `lip_sync_required` marcado por shot
- [ ] Watermark persistente + CTA loop tagline + caption del Reel con pregunta + hashtags
- [ ] Pattern rotado vs último video (→ `ROTATION-RULES.md` + video-log del género)

---

## §9 — Decision-UI editorial pacing (creative intent — cross-link)

El momento de decisión NO es "UI suelto sobre un clip". Es un **micro-evento editorial estructurado** (pause beat → countdown 3-2-1 → loading bar L→R, con freeze-frame y filter overlay OPCIONALES). Esto es creative intent agnóstico; el **timing técnico exacto + implementación** → `INGENIERO-CHOICE-CORE.md § decision-UI editorial pacing`.

🟥 **Anti-pattern:** countdown con timing flotante + clip en movimiento + loading bar pegado al countdown sin separación → "elementos UI puestos sueltos sobre video". La estructura editorial colapsa.

---

## §10 — RELACIÓN CON OTROS DOCS

- **Técnica universal** (LUFS, mix, render, HYBRID, MODEL-CAPABILITIES, motion, mastering, 8 gates) → `ai-video-production/` (Capa A). Este doc NO la toca.
- **Técnica choice-específica** (decision-UI pacing, UI safe zones, caption chunking, lip-sync, 0-cuts-en-hook) → `INGENIERO-CHOICE-CORE.md` (Capa A.5).
- **Rotación entre videos** → `ROTATION-RULES.md` (Capa A.5).
- **Sabor de género** (settings, personajes, tipos de consecuencia, paleta, SFX, patterns concretos, elementos del cliffhanger) → `horror-choice-format/PAUTA-MASTER.md` o `sport-choice-format/PAUTA-MASTER.md` (Capa B).
