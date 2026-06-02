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
| **P3 — Seguro era trampa / lo fácil** | El camino fácil del foil vs el difícil del protagonista | **NATURAL para sport-choice** — la rama corta del foil ("lo fácil/seguro" del favorito) vs la rama jugable difícil |
| **P6 — Hedonismo eterno** | "Bueno" lleva a placer pero perdés el objetivo | (poco natural en sport) |
| **P9 — Peligroso te ayuda** | El amenazante te salva | (poco natural en sport) |

> **Nota:** P3 es el pattern natural del formato sport-choice (rama corta del foil = "lo fácil/seguro" del favorito, como counterfactual opening). Se declara P3 para satisfacer el enum canónico del validator. La rotación de pattern entre videos sport se evaluará cuando haya más videos; por ahora la rotación REAL importante es **liga/equipos + tipo de jugada-clave del clímax + posición del POV**.

---

## Tabla maestra

> Dimensiones tracked para rotación: **pattern** (enum choice), **liga / equipos** (no repetir enfrentamiento ni liga consecutiva), **jugada-clave del clímax** (no terminar siempre en mano a mano), **posición POV** (extremo / 9 / mediapunta / lateral), **countdown style**, **loader style**. Cada uno rota entre videos para evitar feed predecible.

| # | Fecha | Proyecto | Pattern | Liga / Equipos | Jugada-clave clímax | Posición POV | Countdown | Loader | Status |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 2026-05-31 | `champions-sport-choice` | **P3** — rama corta del foil (favorito PSG = "lo fácil") como counterfactual opening | **Champions League** — Arsenal (Saka #7) vs PSG (Dembélé #10), final en el Puskás Aréna | **Mano a mano con el arquero** (cruzar al palo lejano vs picar) | Extremo (banda → borde del área → mano a mano) | FILM LEADER ACADEMY AVU (heredado) | horizontal Y52 (heredado) | 🟡 **PENDING SHIP** (primer video del formato; SPEC validado `creative-specs/champions-sport-choice.yaml`) |

---

## Cross-video uniqueness fields (heredado del schema de horror-choice — validator cross-video)

> Igual que horror-choice, el validator `audit-spec-narrative-coherence.py` compara `location` + `signature_staging` cross-video (exact-match location → FAIL; semantic similarity de staging ≥0.85 → hard-block). Forward rows declaran estos fields al producirse.

| # | Proyecto | location | signature_staging | Confidence |
|---|----------|----------|-------------------|------------|
| 1 | `champions-sport-choice` | Final de la Champions en el Puskás Aréna de Budapest, minuto decisivo, POV de un jugador sobre el césped | POV de un jugador en el césped del Puskás en el minuto decisivo; a la izquierda Saka (kit rojo mangas blancas #7 Arsenal, sonrisa) y a la derecha Dembélé (kit azul franja roja #10 PSG, bigote), 67000 hinchas rugen, reflectores sobre líneas de cal, la jugada que reparte la orejona espera la decisión | HIGH (declarado al producir) |

---

## Rotación — alertas (actualizar con cada video)

### Pattern
- **Usado:** P3 (1 vez, #1 champions)
- **Próximo video:** P3 sigue siendo el natural para sport-choice; si se quiere variar, considerar P2 (acertar las jugadas = "sobrevivir la final"). Evaluar cuando haya más videos.

### Liga / equipos
- **Usado:** Champions League — Arsenal vs PSG (#1)
- **Próximo video DEBE NO repetir** este enfrentamiento ni la Champions consecutivamente. Opciones: Premier derby, LaLiga clásico, Mundial, Libertadores, etc.

### Jugada-clave del clímax
- **Usado:** mano a mano con el arquero (#1)
- **Próximo video DEBE rotar:** penal decisivo, tiro libre al ángulo, cabezazo en el último córner, gambeta al arquero, etc. (no terminar siempre en mano a mano).

### Posición del POV
- **Usado:** extremo (#1)
- **Próximo:** delantero centro (9), mediapunta (10), lateral que sube, incluso arquero (atajar el penal decisivo) — para variar el tipo de jugadas.

---

## Learnings (append 2-3 bullets por video al cerrar — feeds PAUTA-MASTER cuando haya patrón)

> Cuando un video se shippea, agregar acá los aprendizajes (qué funcionó, qué falló, qué ajustar). Estos bullets son la materia prima para promover la lógica deportiva de "diseño" (v0.1) a "empírico" (v1.0) en PAUTA-MASTER.

### #1 — champions-sport-choice (pending ship)
- _(Pendiente — completar al shippear: ¿la REGLA DE AMBIENTE produjo geografía clara? ¿la likeness descriptor-based de jugadores reales convergió en CP1? ¿el contexto explícito de equipo eliminó la confusión rival/compañero? ¿las consecuencias de error se leyeron como humillación deportiva sin caer en horror?)_
