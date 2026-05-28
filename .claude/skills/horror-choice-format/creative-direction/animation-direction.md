# animation-direction.md — Tier por shot + qué animar + cost optimization

> ⚠️ **DOC OPERACIONAL SECUNDARIO — NO ES AUTORIDAD CREATIVA.**
>
> La **autoridad creativa del formato horror-choice** vive en `horror-choice-format/PAUTA-MASTER.md` (8 videos virales canónicos).
>
> Este doc te ayuda a IMPLEMENTAR técnicamente lo que PAUTA-MASTER dicta. Si encontrás conflicto entre lo escrito acá y PAUTA-MASTER → **gana PAUTA-MASTER siempre**.
>
> Si llegaste a este doc sin leer PAUTA-MASTER primero, parar y leerla antes de seguir.

---


> El arquitecto define **qué shots se animan + con qué nivel de calidad + qué animan específicamente**. El ingeniero elige modelo específico según el tier (Kling 2.5 Turbo Pro vs Seedance vs Veo vs LTX, etc. — ver `video-director/MODEL-BENCHMARK.md` del ingeniero).

> **Insight clave del user:** todas las imágenes pueden animarse. Algunos shots NO son relevantes narrativamente → se animan con modelos baratos. Otros shots son hero → necesitan modelos premium. Esto es decisión CREATIVA, no técnica.

---

## Los 3 tiers de animación

Basados en el `MODEL-BENCHMARK.md` del ingeniero:

### Tier HERO ($0.07-0.40/s)
**Cuándo usar:** shots críticos narrativos — hook, climax, character reveals, counterfactual outro reveal.
**Ingeniero usará:** Kling 2.5 Turbo Pro / Seedance 2.0 / HappyHorse-1.0 / Veo 3.1
**Capacidades:** physics realistas + character consistency + camera control + audio nativo (si aplica)

### Tier STANDARD ($0.05-0.15/s)
**Cuándo usar:** shots narrativos pero no climácticos — setup descriptive, decision points (POV con manos), consequences mid-level.
**Ingeniero usará:** Hailuo 2.3 / Kling 1.6 Pro / Pika 2.5
**Capacidades:** movimiento creíble + character decent + más rápido de generar

### Tier DRAFT (GPU self-host)
**Cuándo usar:** shots atmospherics establishing + transition shots + B-roll ambient + cualquier shot que sea "fondo no protagonista".
**Ingeniero usará:** LTX-2.3 self-host / Wan 2.2 self-host
**Capacidades:** motion básico decente + costo casi cero (solo GPU)

### Alternative: Static + Ken Burns ($0)
**Cuándo usar:** shots que NO necesitan motion real — title cards, momentos puramente compositivos donde Ken Burns + parallax 2.5D simulan motion.
**Ingeniero usará:** CSS transforms + GSAP en HyperFrames
**Capacidades:** push-in lento + parallax básico — el ojo percibe motion sin clip Kling

---

## Criterios narrative-driven para asignar tier

### Asignar HERO si el shot...
- Es el HOOK (primeros 3s — make or break)
- Es el CLÍMAX (post-decisión 3 — momento más impactante)
- Es la PRIMERA APARICIÓN de un personaje recurrente (introducción icónica)
- Tiene VFX transformation crítico (Miro cambia color, Bruno parpadea ojo)
- Es el reveal del COUNTERFACTUAL OUTRO (catharsis visual)
- Necesita CHARACTER MOTION compleja (mirada hacia ti, sonrisa progresiva, gesture)

### Asignar STANDARD si el shot...
- Es un DECISION POINT (POV con manos + UI)
- Es una CONSEQUENCE intermedia (no climax)
- Es un SETUP describing del setting
- Tiene character motion simple (caminata, gesto básico)
- Es importante narrativamente pero NO hero

### Asignar DRAFT (cheap Kling tier) si el shot...
- Es ATMOSPHERIC establishing
- Es B-ROLL de background (ambient creature, polvo, niebla)
- Es TRANSITION shot entre hitos
- NO tiene character motion crítica
- Es CORTO (<3s) y no protagonista

### Asignar STATIC + KEN BURNS si el shot...
- Es UNA imagen con composition fuerte que NO necesita motion real
- Es un CAPTION-PRIMARY shot (la atención está en el texto, no en la imagen)
- Es un OBJECT detail shot que solo necesita slight zoom
- Es CORTÍSIMO (<2s) — Kling overkill

---

## Qué animar dentro de cada shot

Si el shot va a Kling/Seedance/Veo, el arquitecto especifica QUÉ MOVIMIENTO sucede DENTRO del clip.

### Categorías de motion intent

#### **Subtle motion** (HERO o STANDARD)
- Personaje respira / pecho sube y baja
- Ojo único parpadea cada 8-12s
- Sonrisa progresiva (de cara neutral a sonrisa lenta)
- Cabeza gira ligeramente (5-10 grados)
- Mano se mueve hacia algo (slow reach)
- Mirada cambia de un punto a otro

#### **Action motion** (HERO predominantemente)
- Caminata (full body walking)
- Empuje físico (uno empuja al otro)
- Caída (POV o wide del cuerpo cayendo)
- Activación de objeto (mano press button, switch, etc.)
- Explosión / flash (visual impact)
- Transformación física (cambio de color, deformación)

#### **Ambient motion** (DRAFT o STANDARD)
- Polvo en suspensión flotando
- Niebla baja moviéndose lento
- Luces parpadeando intermitente
- Agua goteando
- Vapor de respiración
- Crujidos visibles de madera (slight movement)

#### **Camera motion within clip** (HERO si es signature)
- Push-in deep into eye / object
- Pull-out reveal scale (megalofobia)
- Slow orbit alrededor del subject
- Dolly forward (POV walking)
- Whip pan (transition entre objetos)
- Crash zoom (impact dramático)

### Cómo describir motion al ingeniero

```yaml
animation:
  tier: HERO
  motion_intent: |
    Bruno está estático general. Lo que se anima:
    - Su ojo único parpadea LENTAMENTE 1 vez (0.5s closing, 0.5s opening) a t=1.5s del clip
    - Su pecho sube y baja sutilmente respirando
    - Polvo en suspensión flota lento alrededor
    - Vapor leve de su respiración visible en exhale
    - Cabeza permanece estática (NO turn, NO tilt)

  duration_clip_seconds: 5  # tier Kling 5s
  motion_speed: slow_ominous  # not fast action

  what_NOT_to_animate:
    - "Cuerpo de Bruno (mantenerlo estático)"
    - "Background (parallax sí, pero no movimiento orgánico de objetos del fondo)"
    - "Casco de Bruno (estático, mantener tape rojo en posición fija)"
```

---

## Loop length intent

Kling y modelos similares generan clips de duración fija:

- **5s clips** — predomínant en H-choice (sweet spot)
- **10s clips** — para shots que necesitan más action o más respiración
- **15-20s clips** — raramente en H-choice, solo para tomas largas con motion compleja

### Criterios para loop length

| Duración intent | Cuándo |
|------------------|--------|
| 3-5s | Default — most shots |
| 5-10s | Hero shots, character reveals, climácticos |
| 10-15s | Acción compleja con desarrollo (caminata + acción) |
| 15-20s | Solo si NECESITA continuous motion sin cut (raro) |

---

## Transiciones entre shots

El arquitecto especifica el tipo de transición entre cada par de shots consecutivos.

### Tipos de transición

| Tipo | Cuándo usar | Effect emocional |
|------|-------------|------------------|
| **Hard cut** | Default 90% de las transiciones | Limpieza, ritmo, decisión |
| **Fade to black** | Final de un hito (separa H3 → H4) | Pausa narrativa, breathing |
| **Fade to white** | Death moment / flash impact | Trauma sensorial |
| **Light leak** | Transición "respiración" entre actos | Suave + orgánico |
| **Whip pan** | High energy moments | Velocidad + urgencia |
| **Crossfade** | Outro cozy / transición tonal | Suavidad + warmth |
| **Glitch / morph** | Transformación de estado (Miro color shift) | Surrealismo + AI uncanny |
| **Push-through** | Cámara atraviesa elemento (boca → otro mundo) | Inmersión + dimensional shift |

### Especificación en SPEC

```yaml
transitions:
  - from_shot: shot_setup_wide_mina
    to_shot: shot_dp1_pov_linterna
    type: hard_cut
    intent: "Clean ritmico, no overlap"

  - from_shot: shot_cons1_caida_pov
    to_shot: shot_dp2_setup
    type: fade_to_black
    duration: 0.5s
    intent: "Separar acto 1 de acto 2, breathing momento"

  - from_shot: shot_climax_taladro
    to_shot: shot_outro_pablo_cozy
    type: fade_to_white_then_warm_dissolve
    duration: 1.0s
    intent: "Trauma sensorial → catharsis tonal radical"
```

---

## Audio-reactive animations (cuando aplica)

Algunos shots tienen animación SYNC con audio events. Decisión creativa del arquitecto.

### Patrones validados

**Scale pop sync con SFX impact:**
- A 0:14, sub-bass impact → imagen scale 1.0 → 1.05 → 1.0 en 0.3s
- A 0:28, white flash impact → frame entero flash blanco brief 0.1s

**Visual pulse sync con beat musical:**
- Si música tiene beat marcado, slight brightness pulse cada beat (subtle)

**Color shift sync con drone music swell:**
- En crescendo musical pre-climax, lighting becomes more red gradually

### Especificación

```yaml
audio_reactive_moments:
  - shot_id: shot_dp1_pov_linterna
    sync_event: "white flash SFX a t=0:20"
    animation_intent: "Frame entero flash white 0.1s + scale 1.0 → 1.05 → 1.0"
    purpose: "Visual punch sync con audio impact"

  - shot_id: shot_climax_taladro
    sync_event: "sub-bass impact a t=1:15"
    animation_intent: "Scale pop 1.0 → 1.05 + slight shake camera + flash partial"
    purpose: "Climax visual impact synced"
```

---

## Cost optimization strategy

### Budget tier por video

El arquitecto en el SPEC define el budget tier objetivo:

```yaml
budget_optimization:
  total_budget_target: $5_USD  # ejemplo
  duration_target: 60s  # cortos para abaratar
  hero_shots_count: 4  # los 4 más críticos premium
  standard_shots_count: 6  # los siguientes 6 standard
  draft_shots_count: 8  # atmospherics + transitions
  static_shots_count: 4  # captions/details que no necesitan Kling
```

**Distribución típica para video 60s con budget $5:**
- 4 shots HERO Kling 2.5 Turbo Pro × 5s × $0.07 = $1.40
- 6 shots STANDARD Hailuo × 5s × ~$0.05 = $1.50
- 8 shots DRAFT LTX self-host × 5s × $0 (GPU only) = $0
- 4 shots STATIC + Ken Burns × $0 = $0
- **Total animación: ~$3** (resto para image gen + TTS + SFX)

**Distribución para video 90s con budget $10:**
- 6 shots HERO × 5s × $0.07 = $2.10
- 10 shots STANDARD × 5s × $0.05 = $2.50
- 8 shots DRAFT × 5s × $0 = $0
- 4 shots STATIC × $0 = $0
- **Total animación: ~$4.60**

### Tier priorización si budget se agota

Si el budget es limitado y debes reducir, priorizar (en este orden):

1. **MANTENER siempre HERO** en: hook (primer shot), climax (post H5), counterfactual reveal (primer outro shot)
2. **Reducir STANDARD a DRAFT** primero — son shots que NO son protagonistas
3. **Aumentar STATIC + Ken Burns** — los shots de detail/object work bien estáticos con zoom

### Cuándo NO recortar budget

- Personaje uncanny aparece por primera vez → SIEMPRE HERO (la primera impresión define recognition cross-video)
- Decision point que define el video → al menos STANDARD
- Counterfactual outro reveal → SIEMPRE HERO (catharsis falla si se siente cheap)

---

## Output al SPEC — animation per shot

```yaml
animation_direction:
  total_shots_estimated: 24

  tier_distribution:
    hero: 6   # hook, climax, character intros, outro reveal
    standard: 10  # decision points, consequences
    draft: 6  # establishing, transitions, ambient
    static_ken_burns: 2  # detail shots

  shots_animation:
    # SHOT-BY-SHOT DETAIL

    - shot_id: shot_hook_close_up_bruno
      tier: HERO
      duration_clip: 5s
      motion_intent: |
        Bruno static general. Animar:
        - Ojo único parpadea LENTAMENTE 1 vez a t=2s (0.5s close + 0.5s open)
        - Pecho sube/baja respirando sutil
        - Polvo en suspensión flota lento alrededor
        - Vapor leve respiración en exhale
      motion_speed: slow_ominous
      what_not_to_animate:
        - "Cabeza (estática, no turn)"
        - "Cuerpo (estático)"
        - "Background (parallax sí, motion orgánico no)"
      audio_reactive: false

    - shot_id: shot_setup_wide_mina
      tier: DRAFT
      duration_clip: 5s
      motion_intent: |
        Camera slow push-in 5% hacia el centro del túnel.
        Polvo en suspensión flota.
        Lámparas colgantes parpadean intermitente.
        Sin character motion (Bruno y Pablo estáticos al fondo).
      audio_reactive: false

    - shot_id: shot_dp1_pov_linterna
      tier: STANDARD
      duration_clip: 4s
      motion_intent: |
        POV first-person. Manos visibles bottom frame.
        Dedo se mueve LIGERAMENTE hacia el botón de la linterna (subtle reach).
        Bruno al fondo estático con leve respiración.
        Polvo flota.
      audio_reactive: true
      audio_reactive_event: "SFX countdown tick — visual pulse leve sync con cada tick"

    - shot_id: shot_cons1_caida_pov
      tier: HERO
      duration_clip: 5s
      motion_intent: |
        POV cayendo. Manos extendidas hacia arriba.
        Cámara rotates slowly cayendo.
        Vista del pozo subiendo arriba de cámara.
        Sound design importantísima — esto es climácticos visual.
      audio_reactive: true
      audio_reactive_event: "Sub-bass thud a final del clip — scale 1.05 + black overlay"

    - shot_id: shot_climax_taladro
      tier: HERO
      duration_clip: 5s
      motion_intent: |
        Extreme close-up taladro en acción.
        Chispas saltando en arc (visualizar como flashes blancos rápidos cada 0.3s).
        Cilindro del taladro vibra ligeramente (motion industrial).
        Sin face visible — pure terror del objeto.
      audio_reactive: true
      audio_reactive_event: "Sub-bass impact + grito cortado — scale + flash"

    - shot_id: shot_outro_pablo_cozy
      tier: HERO
      duration_clip: 5s
      motion_intent: |
        Medium shot warm cozy. Pablo y vos sentados.
        Pablo sonríe progresivo (cara neutral → sonrisa cálida en 2s).
        Sus manos sirven pan (subtle gesture).
        Tus manos sostienen cartas, slight shuffle.
        Llama de vela parpadea.
      audio_reactive: false

    # ... (resto de shots)

  transitions:
    - from: shot_hook_close_up_bruno
      to: shot_setup_wide_mina
      type: hard_cut
    - from: shot_setup_wide_mina
      to: shot_setup_bruno_apaga
      type: hard_cut
    - from: shot_dp1_pov_linterna
      to: shot_cons1_linterna_enciende
      type: white_flash
      duration: 0.2s
      intent: "Decision tomada — flash signature"
    - from: shot_cons1_caida_pov
      to: shot_dp2_setup
      type: fade_to_black
      duration: 0.5s
    - from: shot_climax_taladro
      to: shot_outro_pablo_cozy
      type: fade_to_white_then_warm_dissolve
      duration: 1.0s
      intent: "Trauma sensorial → catharsis radical"

  budget_strategy:
    total_target_animation_cost: ~$5
    hero_priority_shots: ["shot_hook_close_up_bruno", "shot_cons1_caida_pov", "shot_climax_taladro", "shot_outro_pablo_cozy"]
    cost_estimate_breakdown:
      hero_total: ~$2.10 (6 shots × 5s × $0.07)
      standard_total: ~$2.50 (10 shots × 5s × $0.05)
      draft_total: $0 (self-host)
      static_total: $0
```

---

## Anti-patterns en animation direction

❌ **Animar TODOS los shots con HERO tier** → exceso de costo + tiempo. No todo shot lo necesita.
❌ **Static todos los shots** → "slideshow + Ken Burns" feel. Necesitás Kling en hero shots.
❌ **Motion intent vague** ("se anima Bruno") → ingeniero infiere = drift creativo
❌ **No especificar WHAT NOT to animate** → ingeniero anima de más (background, cuerpo, etc.) → uncanny mecánico
❌ **Loop length wrong** (15s clip de hook descripción) → desperdicio
❌ **Audio-reactive sin sync con SFX** → puro adorno visual sin function
❌ **Transitions sin intent** (todo hard cut) → falta variedad emocional
❌ **Glitch effects en cada cut** → pierde fuerza
❌ **Whip pan en escenas calmas** → disonancia tonal
❌ **Tier choice por costo sin considerar narrative importance** → hero shots con tier draft = fail

---

## Validación final de animation direction

- [ ] ¿Cada shot tiene tier asignado (HERO / STANDARD / DRAFT / STATIC)?
- [ ] ¿Motion intent describe QUÉ se anima Y qué NO se anima?
- [ ] ¿Loop length intent definido (default 5s)?
- [ ] ¿Hero shots son los narrativos críticos (hook + climax + outro reveal + character intros)?
- [ ] ¿Audio-reactive moments marcados explícitamente?
- [ ] ¿Transitions entre cada par de shots especificadas?
- [ ] ¿Budget total estimado y dentro del target?
- [ ] ¿Hero priority list claro para fallback de presupuesto?

Si ❌ en cualquiera → ajustar antes de SPEC.

---

## Cómo se enchufa con todo lo demás

```
SCRIPT (timeline backbone)
   ↓
   synced_to_visual → SHOT IMAGES (image-direction.md)
   ↓
   per-shot animation: tier + motion_intent + transitions
   ↓
   ANIMATIONS (este doc)
   ↓
   El ingeniero elige modelo específico según tier (Kling 2.5 Turbo Pro, Seedance, etc.)
   ↓
   El video se anima coherentemente con script + images + captions + audio
```

**El arquitecto da intent. El ingeniero ejecuta con el modelo apropiado del benchmark.**
