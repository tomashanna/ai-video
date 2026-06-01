# INGENIERO-PAUTA-MASTER.md — Autoridad TÉCNICA del INGENIERO para sport-choice × reel

> **AUTORIDAD TÉCNICA del formato sport-choice** (rol 🛠️ INGENIERO). Define CÓMO ejecutar técnicamente lo que la PAUTA-MASTER creativa dicta.
>
> ⚠️ **ESTE DOC HEREDA, NO DUPLICA.** sport-choice comparte 100% el pipeline técnico universal. Para CUALQUIER métrica técnica heredada (pace WPM, LUFS, mix de volúmenes, cuts/min, music BPM, captions, UI safe zones, decision-UI implementation, lip sync, HYBRID per-clip atomic, MODEL-CAPABILITIES, 8 gates), la autoridad es:
> - **`horror-choice-format/INGENIERO-PAUTA-MASTER.md`** (técnica del formato choice — derivada de mediciones F1 de 10 referentes) +
> - **`ai-video-production/`** (PIPELINE, CAPTIONS, SFX-PIPELINE, MOTION-LAYER, AUDIO-MASTERING, MODEL-CAPABILITIES-MATRIX, etc.).
>
> Este doc documenta SOLO lo sport-específico: la ⭐⭐ **REGLA DE AMBIENTE**, la paleta SFX fútbol, y la consistencia de kits/likeness. Todo lo demás se hereda.
>
> **Última actualización:** 2026-05-31 (creación)
> **Versión:** v0.1 (pre-empírico — fase de validación)

---

## 0. METODOLOGÍA — DE DÓNDE VIENEN ESTAS REGLAS

### Lo que se HEREDA (autoridad empírica F1 de horror-choice, NO re-medido)

| Métrica técnica | Valor heredado | Autoridad |
|-----------------|----------------|-----------|
| **Speaking rate** | 156-195 WPM (target ~165 WPM; David C2 = 157 WPM medido, atempo ×1.05) | horror INGENIERO-PAUTA § 1 |
| **Narration coverage** | ≥80% | horror INGENIERO-PAUTA § 1.3 |
| **LUFS integrated** | -14 ±0.5 (Instagram) | horror INGENIERO-PAUTA § 2.1 + `AUDIO-MASTERING.md` |
| **Mix de volúmenes** | narración 1.0 / música 0.05-0.18 / SFX 0.20-0.35 / flash 0.55-0.65 | CLAUDE.md HR#9 + `SFX-PIPELINE.md` |
| **Ducking / sidechain** | -6 dB target sobre música+ambient cuando narrador habla | horror INGENIERO-PAUTA § 2 + SPEC `layer_3.sidechain_target_db` |
| **Cuts/min** | banda 14-22 (modulado por sección — ver editing_targets del SPEC) | horror INGENIERO-PAUTA § 3 |
| **Music BPM** | según mood (ver § música sport abajo) | horror INGENIERO-PAUTA § 4 |
| **0 cuts en hook** | universal (hook = single shot O push-in continuo) | horror INGENIERO-PAUTA + feedback_hook_continuity_no_zoom_cut |
| **Captions** | Whisper word-timed progresivos, ≤2 líneas, chunk_caption_cues (NUNCA bloque estático que se trunca) | CLAUDE.md HR#3 + HR#30 + `CAPTIONS.md` |
| **UI safe zones** | caption Y62 / loading Y52 / countdown Y46 / name labels Y11.5 monospaced | CLAUDE.md HR#4 + horror INGENIERO-PAUTA § 7 |
| **Decision-UI editorial pacing** | countdown digit 1.0s, pause beat 0.9s median, loading Y52 ≥6% sep de countdown, NO ambient duck obligatorio, freeze/filter OPCIONAL | horror PAUTA-MASTER § 18 + horror INGENIERO-PAUTA § 7.10 |
| **Lip sync rule** | si `lip_sync_required: false` → NO clip con boca visible moviéndose | horror INGENIERO-PAUTA § 8.5 |
| **Ensamblado** | HYBRID per-clip atomic (captions burned per clip + Layer 3 continuo) | CLAUDE.md HR#23 + HR#25 + `PIPELINE.md § 13` + `build_clip_atomic.py` |
| **MODEL-CAPABILITIES** | Hailuo clip_max 5.9s, etc. — leer la MATRIX antes de producir | CLAUDE.md HR#28/#29 + `MODEL-CAPABILITIES-MATRIX.md` |
| **8 gates pre-render** | Gate 0 spec-completeness + lint + narrative + render-lock + frames + audio + continuity + qa-gate | CLAUDE.md § Pre-render gate |

> **Regla #1 del ingeniero (heredada):** NUNCA usar nuestras propias producciones como autoridad técnica. La autoridad de la mecánica son los referentes F1 (vía horror INGENIERO-PAUTA). Para la capa sport (REGLA DE AMBIENTE, SFX fútbol), la autoridad es ESTE doc + se valida con cada video.

### Lo que es SPORT-ESPECÍFICO (este doc)

1. ⭐⭐ **REGLA DE AMBIENTE** (§ 1) — el orden visual del partido en cada prompt de imagen/animación. **La regla técnica central del formato.**
2. **Paleta SFX fútbol** (§ 2) — qué sonidos pueblan la capa SFX.
3. **Consistencia de identidad** (§ 3) — kits propio vs rival, likeness descriptor-based.
4. **Música deportiva** (§ 4) — el mood musical reskineado.

---

## 1. ⭐⭐ REGLA DE AMBIENTE — el orden visual del partido (LA REGLA TÉCNICA CENTRAL)

> **Como TODO pasa en la cancha, el riesgo #1 del formato es que el viewer no entienda QUÉ está pasando en el partido en cada frame** (dónde está el arco, quién es compañero, quién rival, dónde está el balón). La REGLA DE AMBIENTE elimina ese riesgo: cada prompt de imagen/animación UBICA la escena ANTES de la acción, en un orden fijo.

### La regla (NO negociable)

**Cada `visual_intent` de cada shot DEBE construirse en este ORDEN exacto:**

```
(1) CÁMARA POV 1ª persona del jugador
     ↓
(2) ZONA del campo  (círculo central / banda / borde del área / mano a mano / medio campo)
     ↓
(3) GEOGRAFÍA clara:
       - arco + red (¿dónde está la portería?)
       - compañeros (kit PROPIO)
       - rivales (kit OPUESTO)
       - arquero (kit DISTINTO a ambos)
       - balón (¿dónde está?)
       - líneas de cal (referencia espacial)
     ↓
(4) ESTADIO lleno + reflectores + césped
     ↓
(5) la ACCIÓN / animación  (lo que pasa en este shot)
```

**Calidad de imagen:** premium, foto-real broadcast, lente 85mm, profundidad de campo. Debe entenderse **CLARÍSIMO qué pasa en el partido** en cada frame.

**Por qué este orden:** ubicar primero (POV → zona → geografía → estadio) ancla al viewer espacialmente; recién entonces la acción tiene contexto. Si la acción va primero (o sin geografía), el viewer ve "alguien patea algo en algún lado" — confuso. La geografía DEBE preceder a la acción.

### Ejemplo completo #1 — shot del HOOK (dyad)

```
Cámara POV en primera persona de un jugador, parado en el CÍRCULO CENTRAL del
estadio [Puskás Aréna]. Geografía: a la izquierda Saka (kit ROJO mangas blancas,
dorsal 7, piel marrón, rapado, barba corta, sonrisa amplia) pide el balón con la
mano abierta; a la derecha Dembélé (kit AZUL marino franja roja central, dorsal 10,
piel oscura, rapado, bigote, serio); líneas de cal del círculo central bajo los pies;
balón blanco oficial en el suelo. Estadio Champions LLENO desenfocado al fondo,
reflectores cayendo sobre el césped verde brillante. Acción: micro-bob de cámara,
los dos jugadores miran al viewer esperando la elección. Foto-real broadcast, 85mm,
profundidad de campo.
```

(Orden verificable: POV ✓ → zona [círculo central] ✓ → geografía [Saka kit rojo izq / Dembélé kit azul der / líneas / balón] ✓ → estadio [lleno + reflectores + césped] ✓ → acción [micro-bob, miran al viewer] ✓.)

### Ejemplo completo #2 — shot de DECISIÓN (D3 clímax mano a mano)

```
Cámara POV en primera persona del jugador, en el MANO A MANO dentro del área rival.
Geografía: el arquero del rival (kit verde fosforescente distinto a ambos equipos)
adelantado achicando el ángulo a pocos metros; la portería con red detrás de él;
líneas de cal del área grande y el punto de penal a un lado; tu compañero Saka
(kit rojo mangas blancas #7) desmarcado al borde del área izquierdo; balón blanco
controlado a tus pies. Estadio LLENO rugiendo, reflectores y luz fría de tensión
sobre el césped. Acción: el viewer encara al arquero con el balón dominado, decidiendo
el remate; el arquero se agranda. Foto-real broadcast, 85mm, profundidad de campo
shallow sobre el balón y el arquero.
```

(Orden: POV ✓ → zona [mano a mano en el área] ✓ → geografía [arquero kit verde + portería + líneas + Saka kit rojo + balón] ✓ → estadio [lleno + reflectores] ✓ → acción [encara, el arquero se agranda] ✓.)

### Checklist por shot (el ingeniero valida ANTES de generar)

- [ ] ¿El prompt empieza con la cámara POV 1ª persona?
- [ ] ¿Está nombrada la ZONA del campo explícitamente?
- [ ] ¿Está la GEOGRAFÍA completa: arco, kit propio, kit rival, arquero (si aplica), balón, líneas?
- [ ] ¿Está el ESTADIO (lleno + reflectores + césped)?
- [ ] ¿La ACCIÓN va AL FINAL, no al principio?
- [ ] ¿Los kits son inequívocos (color propio vs opuesto vs arquero)?
- [ ] ¿Queda CLARÍSIMO qué pasa en el partido con solo leer el prompt?
- [ ] ¿Cierra con "foto-real broadcast, 85mm, profundidad de campo"?

Si ❌ en cualquiera → reescribir el prompt antes de generar (no dejar que el modelo improvise la geografía).

### Anti-patterns de la REGLA DE AMBIENTE

❌ **Acción primero, geografía después** ("le pega al balón… en un estadio") → el modelo no sabe dónde está el arco.
❌ **Geografía incompleta** (falta el arco, o no se sabe quién es compañero/rival) → frame ambiguo.
❌ **Kits no especificados o ambiguos** → el viewer no distingue aliado de obstáculo.
❌ **"Estadio" genérico sin lleno/reflectores/césped** → se ve vacío y falso, no broadcast.
❌ **POV no establecido** → el modelo genera tercera persona (rompe HR de POV 1ª persona).
❌ **Falta el balón** → jugada sin balón = sin sentido futbolístico.

---

## 2. PALETA SFX FÚTBOL

> Reemplaza la paleta de horror (drones, susurros, gritos). Heredá la MECÁNICA de SFX (`SFX-PIPELINE.md`: capa dedicada track-index 60-110, foley por acción visible, ducking) pero con SONIDOS DEPORTIVOS. Los presets de voz de horror en `effects-library/voice-effects/` NO se usan.

### Catálogo SFX sport-choice

| Categoría | SFX | Cuándo |
|-----------|-----|--------|
| **Ambiente base (continuo)** | **Rugido de hinchada** (packed stadium crowd roar) | Cross-clip continuo casi todo el video — la final NO calla nunca |
| **Ambiente base** | **Cánticos lejanos de ultras** + eco de estadio cerrado | Capa continua bajo el rugido |
| **Eventos de juego** | **Silbato** del árbitro | Inicio/falta/penal |
| **Eventos de juego** | **Golpe al balón** (boot-strike) | Cada vez que se patea/pasa |
| **Eventos de juego** | **Red inflándose** (net ripple) | GOL |
| **Eventos de juego** | **Atajada / manotazo** (goalkeeper save) | El arquero saca/ataja |
| **GLORIA (acierto)** | **Explosión de celebración** de la hinchada | Gol propio / campeón |
| **GLORIA** | **Confeti** (rustle) + cánticos eufóricos | Vuelta olímpica / levantar la copa |
| **GLORIA** | **Pings de redes positivos** (opcional) | Si se muestra el furor en redes |
| **BURLA (error)** | ⭐ **Abucheos / "uy" decepcionado** de la hinchada | Cada error → la jugada se cae |
| **BURLA** | ⭐ **Pings de redes / notificaciones** (meme alert) | "Eres la burla" — el furor de memes en su contra |
| **BURLA** | **Silbidos** de la hinchada | Humillación sostenida |
| **UI** | Tick del countdown 3-2-1 (film leader academy) + beep tick del loading bar | Cada decisión (se hereda el AVU countdown de horror) |

### Regla absoluta de la paleta

> ⛔ **NUNCA gritos de horror, drones de terror, sub-bass de jumpscare, ni susurros uncanny.** El audio de sport-choice es 100% diegético-deportivo + música de tensión deportiva. Si un SFX evoca terror, está fuera de formato.

### Capas de audio (heredadas, reskineadas al estadio)

| Capa | horror | sport-choice |
|------|--------|--------------|
| Música (Layer 3 drone) | dark ambient drone | drone subharmónico de tensión deportiva sostenida (sports-thriller bed) |
| Voiceover | narrador grave | narrador grave deportivo, español neutral (mismo voice_id David C2) |
| Ambient continuo (Layer 2) | hum/viento del setting | **rugido de estadio lleno** + cánticos + eco (cobertura 99-100%, cero dead zones) |
| SFX puntuales (Layer 1 clip-scoped) | foley horror + impactos | foley deportivo (boot-strike, red, atajada) + abucheos/confeti/pings |
| Accent (clímax) | string stabs | rising strings + low pulse en D3 (mano a mano) + remate |

(Detalle creativo de las 4 capas → `creative-direction/audio-direction.md`. Detalle técnico de la mecánica SFX → `ai-video-production/SFX-PIPELINE.md`.)

---

## 3. CONSISTENCIA DE IDENTIDAD — kits + likeness (riesgo CP1)

> Lo equivalente a "character consistency" de horror, pero centrado en KITS DE EQUIPO + likeness de jugadores reales.

### Kit propio vs rival — siempre legible

- **El kit del jugador elegido = TU equipo (tu kit).** Aparece en el POV (tus mangas), en tu compañero, y define "los míos".
- **Los rivales visten el kit OPUESTO** (color contrastante). Son obstáculos (lateral, defensores).
- **El arquero rival viste un kit DISTINTO a ambos** (regla real del fútbol — guante + color diferenciado). Esto evita confusión en el mano a mano.
- En cada shot, el ingeniero verifica que los 3 kits (propio / rival de campo / arquero) sean visualmente inequívocos. El kit es la señal que le dice al viewer quién es aliado y quién obstáculo.

**Anchors de kit:** generar UNA reference image por jugador (anchor) con su kit exacto (color, mangas, dorsal) y reusarla en todos los shots de ese jugador (IP-Adapter / reference mode). El dorsal y el patrón del kit son la "visual signature" — NUNCA varían cross-shot.

### Likeness de jugadores reales = descriptor-based (REGLA CRÍTICA)

- ⛔ **NUNCA poner el nombre de la celebridad literal en el prompt de imagen.** Los modelos t2i no reproducen personas reales nombradas de forma confiable (producen caras genéricas o fallan).
- ✅ Describir por **RASGOS FOTO-REALES reconocibles**: posición + tono de piel + corte de pelo + vello facial + gesto característico + **kit con dorsal**. Ejemplo: "extremo del Arsenal, piel marrón, rapado, barba corta, sonrisa amplia, kit rojo mangas blancas dorsal 7".
- **Iterar en CP1** hasta likeness aceptable. Este es el **riesgo de producción #1** del formato — presupuestar iteraciones de CP1 (anchor generation) para los jugadores reales.
- Si la likeness no converge a un nivel aceptable tras iteración razonable, escalar al arquitecto (puede decidir jugador ficticio o ajustar el descriptor).

### Lip sync (heredado, aplicado al protagonista)

- El **jugador protagonista PUEDE hablar on-screen** (p.ej. pidiendo el balón / "Confía en ti, la metes" / "Te lo dije, hermano"). En esos shots `lip_sync_required: true`.
- Aplica la **lip sync rule heredada** (horror INGENIERO-PAUTA § 8.5): si `lip_sync_required: false`, NO usar clips con boca visible moviéndose (crea disonancia). El ingeniero itera tools (Hedra primary, ver MODEL-BENCHMARK) hasta resultado aceptable.

---

## 4. MÚSICA DEPORTIVA (mood reskineado)

> Hereda la mecánica de música de horror INGENIERO-PAUTA § 4 (3 capas mandatorias, BPM por mood, evolución, ducking). Reskin del MOOD:

| Sección | Mood musical sport-choice | Ejemplo de prompt ElevenLabs |
|---------|---------------------------|------------------------------|
| Hook + juego en tensión | Drone subharmónico de **tensión deportiva sostenida** (sports-thriller bed) | "low subharmonic drone, sustained deep bass tension, no melody, dark cinematic sports-thriller bed, faint orchestral swell undertone" |
| Rama corta gloriosa + resolución + outro (acierto) | **Celebración triunfal cálida** | "triumphant stadium celebration ambience, distant euphoric crowd cheering warm, confetti rustle, victory tone, uplifting, no horror" |
| Clímax D3 (mano a mano) | **Tensión rising** | "rising dark cinematic strings tension, pounding low pulse building, climax buildup, no resolution" |
| Outro sostenido | Hum bajo + swell triunfal (loop cue) | "sustained low hum gradual fade blended with faint triumphant swell, cliffhanger atmospheric, loop cue" |

**Contraste musical clave:** el drone de tensión (juego) → celebración cálida (gol/gloria). Igual que horror contrasta drone → folk cozy, sport-choice contrasta tensión → triunfo. El error/burla va con paleta fría desaturada (gris-azul del fracaso, NO rojo de horror) + abucheos.

**LUTs (intent de color, ejecuta el ingeniero):**
- `warm_glory` = celebración / gol / copa (cálido dorado)
- `cool_cinematic_stadium` = juego en tensión (frío cinematográfico de broadcast)
- `cool_defeat` = error / burla (frío desaturado gris-azul — el frío del fracaso deportivo, NO horror rojo)

(Sin `cool_horror` ni ninguna LUT de terror.)

---

## 5. GATES + VALIDACIÓN (heredados)

Se heredan los **8 gates pre-render** (CLAUDE.md § Pre-render gate) + el dual quality bar (Gemini ≥9.7 + audit-against-referent ≥85%). Notas sport-específicas para los gates:

- **Gate 4 (audit-frames Gemini Vision):** verificar adicionalmente que en cada frame se entienda la geografía del partido (arco visible, kits distinguibles, balón ubicable) — la REGLA DE AMBIENTE se valida acá visualmente.
- **Gate 5 (audit-audio):** verificar que el rugido de estadio cubra ≥99% (cero dead zones) y que los abucheos/celebración estén presentes en los beats de error/gloria.
- **Gate 6 (continuity-check):** verificar que la cadena de lógica deportiva cierre (elección → equipo → jugadas → resultado) sin saltos, y que el orden hablado = orden de botones.
- **audit-against-referent:** ⚠️ sport-choice aún NO tiene referentes virales propios para el ≥85% de métricas críticas. Hasta tenerlos, este audit se corre contra las **bandas técnicas heredadas de F1** (las de la mecánica: LUFS, cuts/min, UI safe zones, pace) — que SÍ aplican. Las métricas de CONTENIDO deportivo (qué % son shots de jugada, etc.) se derivarán empíricamente con nuestros primeros videos. Documentar honestamente en el handoff que la referencia es la mecánica F1, no referentes sport.

---

## 6. RELACIÓN CON OTROS DOCUMENTOS

### Hereda (autoridad técnica, NO re-litiga)

- ✓ `horror-choice-format/INGENIERO-PAUTA-MASTER.md` — TODA la técnica de la mecánica choice (pace, LUFS, mix, cuts, BPM, captions, UI safe zones, decision-UI, lip sync, silencios).
- ✓ `ai-video-production/` — PIPELINE, SFX-PIPELINE, CAPTIONS, MOTION-LAYER, AUDIO-MASTERING, COLOR-GRADING, PACING-MARKERS, MODEL-CAPABILITIES-MATRIX, build_clip_atomic.py, los 8 gates.
- ✓ `video-director/MODEL-BENCHMARK.md` — selección de modelo (imagen + animation + lip sync).

### Aporta (lo sport-específico)

- ✓ REGLA DE AMBIENTE (§ 1) — el orden visual del partido.
- ✓ Paleta SFX fútbol (§ 2).
- ✓ Consistencia de kits + likeness descriptor-based (§ 3).
- ✓ Música/LUTs deportivos (§ 4).

### No toca

- Decisiones creativas (qué jugadas, qué equipos, la lógica narrativa) — son del arquitecto (PAUTA-MASTER).

---

## 7. ESTADO + PRÓXIMOS PASOS

- **Versión:** v0.1 (pre-empírico, fase de validación)
- **Para promover a v1.0 empírico:** medir nuestros primeros videos sport-choice (F1-style: cuts/min, LUFS, coverage, % shots de jugada, claridad de geografía) + escribir bandas técnicas deportivas propias. Hasta entonces, la técnica de la mecánica se hereda de F1 (válida) + la capa sport (AMBIENTE, SFX, kits) se ajusta con cada video logueado en `video-log.md`.
