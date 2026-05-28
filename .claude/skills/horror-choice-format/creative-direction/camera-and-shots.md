# camera-and-shots.md — Tipos de plano + motion direction + shot duration

> ⚠️ **DOC OPERACIONAL SECUNDARIO — NO ES AUTORIDAD CREATIVA.**
>
> La **autoridad creativa del formato horror-choice** vive en `horror-choice-format/PAUTA-MASTER.md` (8 videos virales canónicos).
>
> Este doc te ayuda a IMPLEMENTAR técnicamente lo que PAUTA-MASTER dicta. Si encontrás conflicto entre lo escrito acá y PAUTA-MASTER → **gana PAUTA-MASTER siempre**.
>
> Si llegaste a este doc sin leer PAUTA-MASTER primero, parar y leerla antes de seguir.

---


> El arquitecto define QUÉ planos quiere y QUÉ movimiento conceptual. El ingeniero decide cómo implementar (Ken Burns velocidad, parallax layers, GSAP timeline). Esta es DIRECCIÓN CINEMATOGRÁFICA.

---

## Los 6 tipos de plano usados en el formato

### 1. **WIDE shot (plano general)**
- **Cuándo:** establecer setting. Comunicar escala. Mostrar el dyad junto en el contexto.
- **Frecuencia:** 1 al inicio (H2 setup) + 1-2 en momentos de escala dramática
- **Duración recomendada:** 4-7s (necesita tiempo para que el viewer absorba el espacio)
- **Mood:** establishing, megalofobia, aislamiento
- **Validado en:** TODOS los 13 referentes lo usan al menos 1 vez

### 2. **MEDIUM shot (plano medio)**
- **Cuándo:** presentación de personajes. Diálogo. Acción corporal.
- **Frecuencia:** la mayoría del video (40-60%)
- **Duración:** 3-5s típico
- **Mood:** intimate, character-driven
- **Notas:** es el "default shot" del formato

### 3. **CLOSE-UP (primer plano)**
- **Cuándo:** momentos de tensión. Mirada fija del peligroso. Reacción.
- **Frecuencia:** 3-5 close-ups por video
- **Duración:** 2-3s (más corto = más intenso)
- **Mood:** tensión, dread, confrontación
- **Validado:** los referentes top tienen close-ups del peligroso mirando fijo a cámara

### 4. **EXTREME CLOSE-UP (primerísimo plano)**
- **Cuándo:** detalle anatómico uncanny (ojo único, dientes, mano deforme). Climax visual.
- **Frecuencia:** 1-2 por video, no más
- **Duración:** 1-2s (instantáneo punch)
- **Mood:** uncanny puro, jumpscare visual
- **Validado:** ref-03 ojo de Bruno, ref-12 boca de Teresa dientes afilados

### 5. **POV (first-person / point-of-view)**
- **Cuándo:** decisión física. Manos sosteniendo objeto. Mirada del personaje "vos".
- **Frecuencia:** 2-4 por video, asociados a decision points
- **Duración:** 2-4s
- **Mood:** inmersión, "estás ahí", agency
- **Validado:** todos los referentes usan POV en decision points (manos sosteniendo linterna, dedo activando botón, vista desde el coche)
- **Importante:** las manos en POV deben verse desde la perspectiva del usuario (manos saliendo del bottom del frame, no manos de personaje)

### 6. **DETAIL shot (plano detalle)**
- **Cuándo:** objetos críticos para la decisión. Medidor de gas, dinamita, botón de alarma, taza.
- **Frecuencia:** 1 por decision point típico
- **Duración:** 2-3s
- **Mood:** subraya el objeto = stake

---

## Camera movement (movimiento de cámara conceptual)

El arquitecto especifica QUÉ movimiento, el ingeniero implementa CÓMO.

### Movimientos validados

#### **Push-in (zoom forward lento)**
- Acerca cámara a sujeto gradualmente
- Usado en TODOS los planos > 2s
- Crea sensación de "te tira al interior"
- Variantes: push-in to face, push-in to detail, push-in to deep

#### **Pull-out (zoom backward lento)**
- Aleja cámara revelando contexto
- Usado en momentos de revelación de escala ("¿cuán grande es esto?")
- Validado en ref-04 (pull-out de puertas revelando pasillo decadente completo)

#### **Parallax 2.5D (layers moviéndose a velocidad distinta)**
- Background y foreground se mueven a distinta velocidad
- Crea sensación 3D en imagen estática AI
- Usado en TODOS los planos con sujeto + fondo
- **Validado como signature** del formato — los referentes top lo usan universalmente

#### **Slow rotation / orbit**
- Cámara orbita sutilmente alrededor del sujeto
- Más raro, usado en momentos contemplativos
- Validado en algunos planos de @referent-b

#### **Handheld shake sutil**
- Imitación de cámara en mano
- Acentúa "found footage" feel
- Usado en momentos de pánico/acción

#### **Whip (transición motion-blur)**
- Movimiento muy rápido lateral entre shots
- Decisión creativa: cuándo el ritmo lo pide

### Regla universal: **CERO frames estáticos**

Si un shot dura más de 1.5s, DEBE tener motion. Push-in lento es mínimo. Sin motion → "slideshow de fotos" feeling. Validado en 13/13 referentes top.

---

## Shot duration patterns

### Distribución típica de shots en 90s

| Tipo de plano | Cantidad | Duración cada uno | Total |
|---------------|----------|-------------------|-------|
| Wide (establishing) | 2-3 | 5-7s | 12-18s |
| Medium (predominante) | 12-18 | 3-4s | 40-60s |
| Close-up (tensión) | 3-5 | 2-3s | 8-12s |
| Extreme close-up | 1-2 | 1-2s | 2-4s |
| POV (decisión) | 3-4 | 3-4s | 10-14s |
| Detail (objeto) | 2-3 | 2-3s | 5-8s |

**Total aprox:** 22-30 planos por video. Pacing felt de 1.5-2s por plano experiencial.

### Distribución por hito

| Hito | Tipos predominantes |
|------|--------------------|
| H1 Hook 0-3s | Close-up + extreme close-up + medium dual |
| H2 Setup 3-15s | Wide establishing + medium con name labels |
| H3 Decisión 1 | Medium + POV (manos) + countdown UI |
| Consecuencia 1 | Mix: close-up reacciones + medium acción + detail objetos |
| H4 Decisión 2 | POV + medium + detail |
| Consecuencia 2 | Mix con stakes mayores |
| H5 Decisión 3 | POV + close-up tensión + extreme close-up climax |
| Climax | Extreme close-up + impact visual |
| H6 Outro | Medium cozy + warm tones + slow push-in |

---

## Reglas de variedad

### Regla 1 — Mínimo 5 tipos distintos por video
**Validado:** los referentes top usan 5-7 tipos. Los videos mediocres usan 2-3 (todos medium o todos POV) — fatigue visual.

### Regla 2 — Cambio de tipo cada 2-3 shots consecutivos
- ❌ 4 medium shots seguidos = monotonía
- ✅ Medium → close-up → POV → medium → detail → wide

### Regla 3 — POV asociado a decision points
- Cada decision point (H3, H4, H5) DEBE tener al menos 1 shot POV con UI elements visibles
- Comunica "vos estás eligiendo"

### Regla 4 — Wide al inicio + outro
- 1 wide en H2 establece setting
- 1 wide cozy en H6 contrasta con horror anterior

### Regla 5 — Extreme close-up en clímax
- 1 extreme close-up en el momento más impactante (post-H5)
- Sostiene 1-2s para máximo punch

---

## Specific shot lists por escena

### Plantilla escena "mina abandonada — decision point 1"

| # | Tipo | Duración | Contenido |
|---|------|----------|-----------|
| 1 | Medium | 4s | Bruno mira a vos, lámpara apagada, expresión ambigua |
| 2 | POV | 3s | Tus manos en bolsillo, linterna visible, dedo en botón |
| 3 | Close-up | 2s | Ojo único de Bruno, espera tu decisión |
| 4 | Detail | 2s | UI countdown circular 3-2-1 sobreimpresa |
| 5 | POV | 3s | Tu mano apretando el botón (decisión A) o tu mano relajándose (decisión B) |

### Plantilla escena "hotel — descubrimiento entidad"

| # | Tipo | Duración | Contenido |
|---|------|----------|-----------|
| 1 | Wide | 5s | Pasillo hotel infinito vacío con luces parpadeando |
| 2 | Medium | 3s | Personaje al fondo del pasillo, lejos |
| 3 | POV | 3s | Vos avanzando hacia él |
| 4 | Close-up | 2s | Su rostro va apareciendo, demasiado alto |
| 5 | Extreme close-up | 1.5s | Ojos completamente negros |

### Plantilla escena "carretera — coche detenido"

| # | Tipo | Duración | Contenido |
|---|------|----------|-----------|
| 1 | Wide | 4s | Coche detenido en medio de carretera nocturna, faros encendidos |
| 2 | Medium | 3s | Vos en asiento del copiloto, Axel al volante mirando fijo |
| 3 | POV | 3s | Tus manos en el regazo, móvil tentador |
| 4 | Close-up | 2s | Sonrisa de Axel apareciendo lentamente |
| 5 | Detail | 2s | UI countdown + botones "Mantener silencio" / "Encender luz" |

---

## Camera direction por mood

### Si el mood es uncanny puro
- Close-ups del archetype peligroso predominan
- Extreme close-ups en detail anatómico uncanny (ojo único, dientes)
- Push-ins lentos hacia el rostro

### Si el mood es surrealismo absurdo
- Wide shots mostrando absurdidad espacial
- Slow orbit alrededor de criaturas (déjà la weirdness work)
- Composiciones simétricas frontales

### Si el mood es claustrofóbico liminal
- POV predominante (estás encerrado)
- Push-in al infinity (pasillo nunca termina)
- Pull-out raro pero impactante (cuando lo usa)

### Si el mood es cosmic horror
- Wide con escala humana minúscula vs entidad/setting masivo
- Slow push-in que NO llega (sensación de "más grande aún")
- Pull-out revelando lo imposible

### Si el mood es journey horror (tren, coche)
- Medium estable dentro del vehículo
- Detail de ventanas mostrando paisaje pasando
- POV ocasional con manos visible

---

## Composition / framing rules

### Regla de tercios — usar
- Setting: respetar tercios para "natural feel"
- Sujetos: en intersecciones de tercios

### Romper regla de tercios — cuándo
- **Simetría bilateral perfecta** en horror (dos puertas, dos personajes enfrentados)
- **Sujeto centrado extremo** para creep factor (Bruno mirando directo cámara)
- **Composición desbalanceada** para tensión

### POV framing
- Manos visibles entran desde bottom del frame (no laterales)
- Cámara a altura humana realista (no aérea)
- Sujetos en POV están a distancia "arms length" o más

### Lighting framing (cómo se enmarca la luz)
- Top-down dramatic (lámpara minera) crea sombras bajo cuencas oculares
- Sidelight crea contraste extremo (carretera con faros)
- Rim light backlit (figura recortada contra fondo) para mystery

---

## Cuts y transiciones (conceptual)

### Hard cut — default
- 95% de las transiciones son hard cuts
- Limpieza > fancy transitions
- "Edit invisible" feel

### Fade to black — cuando
- Final de un hito (separa H3 de H4)
- Death moment (post-clímax)
- Outro (transición a counterfactual)

### Fade to white — raro pero impactante
- Flash de revelation
- Death con white flash (sensorial trauma)

### Light leak — opcional
- Transición "respiración" entre actos
- Decisión creativa, no rule

### Whip pan
- Solo en high energy moments
- Validado en @referent-b con EDM section

### Glitch / morph
- Transformación de personaje (Miro cambiando color)
- Setting shift drástico

---

## Output al SPEC

```yaml
camera_and_shots:
  total_shots_estimated: 24
  pacing_intent: "felt cadence ~20 events/min, cero frames estáticos"

  shot_distribution:
    wide: 2  # H2 establishing + H6 outro cozy
    medium: 14  # predominant
    close_up: 4  # tensión
    extreme_close_up: 2  # clímax + setup uncanny
    pov: 3  # uno por decision point
    detail: 3  # objetos críticos

  movement_intent:
    - "Push-in lento en todos los shots > 2s"
    - "Parallax 2.5D en todos los shots con sujeto + background"
    - "Hard cuts predominantes, 1-2 fade to black entre hitos"
    - "1 extreme close-up sostenido en clímax"

  shot_list_critical:
    - id: hook_close_up_bruno
      timestamp: 0-3s
      type: close-up
      content: "Bruno cíclope ojo fijo en cámara, casco minero, penumbra"
      motion: "slow push-in to eye"

    - id: setup_wide_mina
      timestamp: 3-7s
      type: wide
      content: "Pasillo mina, túnel profundo, luces de cascos al fondo"
      motion: "slight parallax 2.5D, pull-back revelando profundidad"

    - id: dp1_pov_linterna
      timestamp: 17-20s
      type: pov
      content: "Tus manos sosteniendo linterna, dedo cerca botón. UI countdown 3-2-1 sobreimpreso"
      motion: "leve handheld shake"

    # ... (resto de shots)
```

---

## Anti-patterns en camera & shots

❌ **Solo medium shots todo el video** — fatigue visual, score D3 cae
❌ **Frames estáticos > 1.5s sin motion** — sensación slideshow
❌ **POV en escenas sin decision** — pierde semántica (POV = "tus manos eligen")
❌ **Extreme close-up al inicio antes de establishing wide** — viewer desorientado
❌ **Pull-out lento de >5s** — pierde momentum
❌ **Cambios de tipo MUY frecuentes** (1 shot por segundo) — agotador
❌ **Camera shake en escenas calmas** — disonancia
❌ **Manos en POV con apariencia de personaje (mangas largas, anillos visibles)** — rompe inmersión, deben ser "tus" manos genéricas

---

## Validación final de camera & shots

- [ ] ¿5+ tipos de plano distintos en el video?
- [ ] ¿Distribución dentro de los rangos validados?
- [ ] ¿Cada decision point tiene POV asociado?
- [ ] ¿1 wide en setup + 1 wide en outro?
- [ ] ¿Extreme close-up en clímax?
- [ ] ¿Motion en TODOS los shots > 1.5s?
- [ ] ¿Composition coherente con mood?

Si ❌ en cualquiera → ajustar antes de SPEC.
