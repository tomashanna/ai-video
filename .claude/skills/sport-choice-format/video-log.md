# video-log.md — Registro de producción del formato sport-choice

> Una fila por video producido. Antes de empezar un nuevo brief: leer las últimas 3 filas. **El próximo video DEBE rotar respecto a los anteriores en: liga/equipos, tipo de jugada-clave del clímax, posición del POV, y pattern estructural** (ver PAUTA-MASTER § 10 + § rotación).

**Última actualización**: 2026-05-31 (creación del formato)

---

## ⚠️ ESTADO METODOLÓGICO

sport-choice es un **formato NUEVO** (creado 2026-05-31). A diferencia de horror-choice (8 referentes virales propios), sport-choice **aún no tiene referentes virales propios**. La rotación, por ahora, se ajusta a mano sobre nuestros propios videos. Cuando haya ≥3 videos shipped, se derivarán bandas + reglas de rotación empíricas (igual que horror-choice las derivó de sus 8 virales).

**Pattern numbering canonical** (la FORMA abstracta apariencia×verdad del enum choice vive en `../choice-format-core/CHOICE-MECHANIC.md § 7`; el catálogo concreto P1-P10 con contenido y el enum exacto usado por el validator `audit-spec-narrative-coherence.py` se heredan de `horror-choice-format/PAUTA-MASTER.md` — sport reusa esa numeración hasta tener catálogo propio):

| Pattern | Significado | Aplicación a sport-choice |
|---------|-------------|----------------------------|
| **P1 — Verdad visible** | El obvio peligroso ES peligroso | (poco natural en sport — no hay "peligroso") |
| **P2 — Supervivencia si manejás bien** | Sobrevivible con decisiones correctas | acertar las 3 jugadas = "sobrevivir" la final → campeón |
| **P3 — Seguro era trampa / lo fácil** | El camino fácil del foil vs el difícil del protagonista | **NATURAL para sport-choice** — el recorrido del favorito ("lo fácil/seguro", ~2 compuertas) vs el del no-favorito (más difícil, ~3 compuertas) |
| **P6 — Hedonismo eterno** | "Bueno" lleva a placer pero perdés el objetivo | (poco natural en sport) |
| **P9 — Peligroso te ayuda** | El amenazante te salva | (poco natural en sport) |

> **Nota:** P3 es el pattern natural del formato sport-choice (el recorrido del favorito = "lo fácil/seguro" con ~2 compuertas, contrastado con el del no-favorito; el orden de los dos recorridos es libre — NO un "counterfactual opening fijo", ver `PAUTA-MASTER.md § 4` + § 10.A). Se declara P3 para satisfacer el enum canónico del validator. La rotación de pattern entre videos sport se evaluará cuando haya más videos; por ahora la rotación REAL importante es **liga/equipos + tipo de jugada-clave del clímax + posición del POV**.

---

## Tabla maestra

> Dimensiones tracked para rotación: **pattern** (enum choice), **liga / equipos** (no repetir enfrentamiento ni liga consecutiva), **jugada-clave del clímax** (no terminar siempre en mano a mano), **posición POV** (extremo / 9 / mediapunta / lateral), **countdown style**, **loader style**. Cada uno rota entre videos para evitar feed predecible.

| # | Fecha | Proyecto | Pattern | Liga / Equipos | Jugada-clave clímax | Posición POV | Countdown | Loader | Status |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 2026-05-31 | `champions-sport-choice` | **P3** — recorrido del favorito (PSG = "lo fácil") vs no-favorito | **Champions League** — Arsenal (Saka #7) vs PSG (Dembélé #10), final en el Puskás Aréna | **Mano a mano con el arquero** (cruzar al palo lejano vs picar) | Extremo (banda → borde del área → mano a mano) | FILM LEADER ACADEMY AVU (heredado) | horizontal Y52 (heredado) | ❌ **NOT SHIPPED** (intento topical fallido — ver Learnings #1; construido sobre la estructura v0.1 deprecada. NO usar como autoridad, HR#19) |

---

## Cross-video uniqueness fields (heredado del schema de horror-choice — validator cross-video)

> Igual que horror-choice, el validator `audit-spec-narrative-coherence.py` compara `location` + `signature_staging` cross-video (exact-match location → FAIL; semantic similarity de staging ≥0.85 → hard-block). Forward rows declaran estos fields al producirse.

| # | Proyecto | location | signature_staging | Confidence |
|---|----------|----------|-------------------|------------|
| 1 | `champions-sport-choice` | Final de la Champions en el Puskás Aréna de Budapest, minuto decisivo, POV de un jugador sobre el césped | POV de un jugador en el césped del Puskás en el minuto decisivo; a la izquierda Saka (kit rojo mangas blancas #7 Arsenal, sonrisa) y a la derecha Dembélé (kit azul franja roja #10 PSG, bigote), 67000 hinchas rugen, reflectores sobre líneas de cal, la jugada que reparte la orejona espera la decisión | ❌ NOT SHIPPED (intento fallido — no cuenta como video producido) |

---

## Rotación — alertas (actualizar con cada video)

> ⚠️ **0 videos SHIPPED.** Lo de abajo es lo que se INTENTÓ en el champions fallido (NO shipped). El primer video que sí se shippee parte sin restricción de rotación real — pero conviene evitar repetir tal cual la superficie del intento fallido.

### Pattern
- **Intentado (NO shipped):** P3 (#1 champions)
- **Próximo video:** P3 sigue siendo el natural para sport-choice; si se quiere variar, considerar P2 (acertar las jugadas = "sobrevivir la final"). Evaluar cuando haya videos shipped.

### Liga / equipos
- **Intentado (NO shipped):** Champions League — Arsenal vs PSG (#1)
- **Próximo video:** evitar repetir tal cual ese enfrentamiento/competición del intento fallido. Opciones: Premier derby, LaLiga clásico, Mundial, Libertadores, etc.

### Jugada-clave del clímax
- **Intentado (NO shipped):** mano a mano con el arquero (#1)
- **Próximo video:** rotar — penal decisivo, tiro libre al ángulo, cabezazo en el último córner, gambeta al arquero, etc. (no terminar siempre en mano a mano).

### Posición del POV
- **Intentado (NO shipped):** extremo (#1)
- **Próximo:** delantero centro (9), mediapunta (10), lateral que sube, incluso arquero (atajar el penal decisivo) — para variar el tipo de jugadas (catálogo de jugadas-compuerta por posición → `PAUTA-MASTER.md § 10.B`).

---

## Learnings (append 2-3 bullets por video al cerrar — feeds PAUTA-MASTER cuando haya patrón)

> Cuando un video se shippea, agregar acá los aprendizajes (qué funcionó, qué falló, qué ajustar). Estos bullets son la materia prima para promover la lógica deportiva de "diseño" (v0.1) a "empírico" (v1.0) en PAUTA-MASTER.

### #1 — champions-sport-choice (❌ NOT SHIPPED — intento topical fallido)
- **Concepto rival/compañero roto en la estructura v0.1:** la estrella foil aparecía como rival DENTRO del played path (su anchor reusado para los obstáculos, shots 05/06/07/12/17/19) → el viewer no sabía quién era su compañero y quién el rival. Fix v0: el foil vive SOLO en su propio recorrido `counterfactual_*` + hook + cliffhanger; los rivales del played path son `rival_npc` genérico (PAUTA § 4 tagging + INGENIERO-PAUTA § 3 5 anchors).
- **Teleport-continuity entre shots mató la inmersión:** los cortes saltaban de posición sin continuidad física, rompiendo la sensación de "un plano continuo" que es el factor X del formato. Fix v0: EXECUTION CONTINUITY (PAUTA § 2) — cada recorrido se vive como UN plano continuo; el único corte no-continuo permitido es el PIVOTE marcado entre recorridos (PAUTA § 10.A).
- **Los docs de enseñanza quedaron en v0.1 tras el rebuild de la PAUTA a v0:** SCRIPT-WRITING-GUIDE + creative-direction/* seguían enseñando "rama corta del foil = counterfactual opening fijo que spoileaba". El upgrade 2026-06-03 (v0.2 operativa) los realineó a la estructura dos-recorridos + orden libre + asimetría por favorito.
- **La estructura debe estar lista ANTES de producir** (no diseñar el formato durante un topical day-of): el champions se intentó montar mientras el formato todavía no tenía la capa operativa. La v0.2 agrega § 10.A (guion beat-a-beat) + § 10.B (catálogo de jugadas-compuerta por posición) + § 10.C (plantilla de cadena causal) precisamente para que el próximo topical arranque con la estructura aceitada.
