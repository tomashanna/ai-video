# ROTATION-RULES.md — Rotación entre videos (mecánica AGNÓSTICA del formato CHOICE)

> **AUTORIDAD agnóstica de la rotación cross-video** de la familia choice. Define LA REGLA de rotación común a todos los géneros choice. **Heredan de este doc:** `horror-choice-format/` y `sport-choice-format/`.
>
> ⛔ **Este doc define solo LA REGLA.** El **registro** de videos producidos (el video-log) vive en cada género — `horror-choice-format/video-log.md` y `sport-choice-format/video-log.md` son autoritativos para el ESTADO de rotación de su género (CLAUDE.md HR#14). Core no hospeda ni mueve esos logs.
>
> **Última actualización:** 2026-06-01 (creación — extracción agnóstica).

---

## §1 — LA REGLA (CLAUDE.md HR#14, agnóstica)

🟦 **No repetir el mismo PATTERN narrativo en 2 videos consecutivos.** El pattern (la configuración "apariencia × verdad" — ver `CHOICE-MECHANIC.md §7`) debe rotar entre videos.

🟦 **No repetir, en videos consecutivos:**
- el **pattern** narrativo (configuración apariencia × verdad)
- el **rol** del personaje/dyad recurrente (si reusás una identidad, invertí o cambiá su rol)
- el **setting** (cambiar de escenario mantiene fresh el feed)
- el **beat clave del clímax** (la jugada/decisión culminante)

🟦 **Consultar el video-log del género ANTES de diseñar** un video nuevo. Es paso obligatorio del flujo del arquitecto + verificación del auditor.

> Genéricamente: lo que rota es **pattern + rol + setting + beat-clave**. El CONTENIDO de cada eje es de género (en horror: setting de terror, body horror, personaje recurrente; en sport: liga/equipos/cruce, jugada-clave del clímax, posición del POV, modo de fracaso, política A/B). El EJE de rotación es agnóstico.

---

## §2 — POR QUÉ ROTAR

- **Frescura del feed:** repetir setting/pattern hace que los videos del creator se sientan iguales → cae el engagement de la cuenta.
- **Re-watch + misterio:** reusar una identidad con rol invertido crea "universo del creator" + drive de re-watch ("¿esta opción era buena o mala realmente?").
- **Evitar que el viewer aprenda la respuesta:** si la opción ganadora es siempre la misma (p. ej. "B siempre paga"), el viewer deja de dudar → muere la mecánica de decisión. Rotar qué opción paga (`CHOICE-MECHANIC.md §5`).

---

## §3 — CÓMO SE APLICA (los 3 roles)

| Rol | Acción de rotación |
|-----|--------------------|
| 🏛️ **Arquitecto** | Antes de elegir el pattern del video nuevo, abre el `video-log.md` del género + verifica que pattern/rol/setting/beat-clave ≠ los del último video. Declara el pattern elegido en el SPEC. |
| 🔍 **Auditor** | En el SPEC-AUDIT (CP2), verifica que el pattern ∈ los patterns del género AND ≠ el del último video logueado. 🟡/🔴 si repite. |
| 🛠️ **Ingeniero** | Tras shippear, **appendea** los learnings del video al `video-log.md` del género (pattern usado, setting, rol, beat-clave) para que la próxima rotación tenga estado. |

---

## §4 — EL VIDEO-LOG VIVE EN CADA GÉNERO (no acá)

- `horror-choice-format/video-log.md` — autoritativo para la rotación de horror (settings de terror, patterns P1-P10, personajes recurrentes).
- `sport-choice-format/video-log.md` — autoritativo para la rotación de sport (ligas/equipos/cruces, jugadas-clave, modos de fracaso, política A/B). Hasta ≥3 videos shipped, rotación a mano.
- Un género nuevo de la familia choice crea su propio `video-log.md` y aplica ESTA regla.

> Core NO centraliza los logs (cada género tiene estado de rotación distinto y vocabulario propio). Core centraliza solo la REGLA que todos enforzan.

---

## §5 — RELACIÓN CON OTROS DOCS

- **La configuración "apariencia × verdad" que rota** → `CHOICE-MECHANIC.md §7` (patterns abstractos).
- **El catálogo concreto de patterns + el video-log** → el skill de género (Capa B).
- **La regla canónica HR#14** → CLAUDE.md § Hard rules globales.
