---
name: choice-format-core
description: INFRA / Capa A.5 — núcleo AGNÓSTICO de la familia de formatos CHOICE ("Elige a tu compañero"). Contiene SOLO la mecánica común a todos los géneros choice (hook dyad + name labels grandes + countdown 3-2-1 + loading bar + botones A/B + decisión→consecuencia + framing acción-condicional + counterfactual + cliffhanger + CTA loop + POV 1ª persona + español neutral + ~90s + rotación entre videos + decision-UI editorial pacing + UI safe zones + caption chunking + lip-sync). NUNCA activar sola — la HEREDAN `horror-choice-format` y `sport-choice-format`. Para la técnica UNIVERSAL apunta a `ai-video-production` (no la duplica). Para el sabor de género ver el skill de género (Capa B).
---

# choice-format-core — Capa A.5 (mecánica AGNÓSTICA del formato CHOICE)

> **⛔ NO es un skill de género y NUNCA se activa sola.** Es la capa neutral que define la mecánica común a TODOS los géneros choice. La heredan `horror-choice-format/` (terror) y `sport-choice-format/` (deportes). Cuando trabajés un video choice de un género concreto, activá el skill de ese género (Capa B) + `ai-video-production` + `video-director`; esos consultan core para "la mecánica choice".
>
> Contrato arquitectural completo + las 3 capas + lo que NO está acá → **`README.md`** de este directorio.

---

## Cuándo se consulta este skill

- El **arquitecto** de cualquier género choice diseña el esqueleto / decisiones / counterfactual / cliffhanger → consulta `CHOICE-MECHANIC.md`.
- El **ingeniero** de cualquier género choice ejecuta la UI de decisión / safe zones / caption chunking / lip-sync → consulta `INGENIERO-CHOICE-CORE.md` (y desde ahí apunta a `ai-video-production/` para la técnica universal).
- Los **tres roles** validan rotación entre videos antes de diseñar uno nuevo → consultan `ROTATION-RULES.md` + el video-log del género.

> Para CUALQUIER tarea de PRODUCCIÓN concreta (TTS, image, SFX, motion, captions, render, QA, mastering) la autoridad es `ai-video-production/` (Capa A). Core NO la duplica.

---

## La lente de lectura — 🟦 / 🟩 / 🟥

Todo en core (y en los skills de género que lo heredan) se expresa con este marco, NUNCA como regla binaria rígida:

- 🟦 **PRINCIPIO (mandatorio)** — invariante; romperlo colapsa la mecánica choice.
- 🟩 **VARIABILIDAD (libre)** — el espacio creativo del género/video.
- 🟥 **ANTI-PATTERN (evitar)** — patrón que rompe el formato.

---

## Documentos en core (orden de lectura)

| # | Doc | Qué contiene (agnóstico) |
|---|-----|--------------------------|
| 1 | **`README.md`** | Front door: contrato de capas (A universal / A.5 core / B género), por qué existe core, qué NO está acá, lineaje empírico. **Leer primero.** |
| 2 | **`CHOICE-MECHANIC.md`** | Autoridad CREATIVA agnóstica: filosofía (formato = generador no límite) · esqueleto canónico (hook dyad + name labels grandes + countdown 3-2-1 + loading bar + botones A/B → played path → counterfactual → cliffhanger) · distribución temporal por fase · el INVARIANTE (la opción de apariencia-favorable nunca decide con el viewer en el recorrido jugado) · recorridos secuenciales · decisión→consecuencia (✓ continúa el path / ✗ inserto corto dead-end) · framing acción-condicional (NO bare label "Si elegiste A") · counterfactual placement + cliffhanger + CTA verbal de loop · POV 1ª persona >80% · español neutral · oraciones cortas · ~90s · "orden hablado = orden de botones" · dilema-mechanics (duda real, ambas opciones defendibles, B no siempre correcta) · patterns abstractos (apariencia × verdad) · SPEC-AUDIT estructural. |
| 3 | **`INGENIERO-CHOICE-CORE.md`** | Autoridad TÉCNICA choice-específica: decision-UI editorial pacing (countdown 1s/dígito + pause beat + freeze/filter OPCIONAL + loading bar L→R) · UI safe zones (caption Y62 / loading Y52 / countdown Y46 / name labels Y11.5 monospaced + no-overlap + per-speaker Y-band) · caption chunking word-timed · lip-sync rule · "0 cuts en hook" · hook-continuity-no-zoom-cut. **+ tabla de técnica UNIVERSAL heredada → apunta a `ai-video-production/`** (LUFS, mix, render, HYBRID, MODEL-CAPABILITIES, etc. — NO duplicadas). |
| 4 | **`ROTATION-RULES.md`** | Regla agnóstica de rotación entre videos: no repetir pattern/rol/setting/jugada-clave en 2 videos consecutivos; consultar el video-log del género ANTES de diseñar. (Los video-logs viven en cada género, no acá.) |

---

## Relación con los skills de género (Capa B)

- `horror-choice-format/PAUTA-MASTER.md` → para la MECÁNICA choice apunta acá (`CHOICE-MECHANIC.md`); aporta el sabor horror (body horror, malo/bueno aparente, archetypes P1-P10, "Paz perdida", 8 canonical-scenes virales).
- `sport-choice-format/PAUTA-MASTER.md` → para la MECÁNICA choice apunta acá; aporta la LÓGICA deportiva (dos recorridos, asimetría por favorito, catálogo de fracaso, narración-no-juzga, política A/B).
- Si un doc de género y core discrepan sobre la MECÁNICA → **gana core**. Si discrepan sobre el SABOR de género → manda el skill de género.

---

## Estado

- **Versión:** v0 (creación 2026-06-01).
- **Origen:** extracción agnóstica desde `horror-choice-format/` (PAUTA-MASTER + INGENIERO-PAUTA-MASTER), generalizada a género-neutro, preservando el lineaje empírico (8 virales / 10 referentes F1).
- **No destructivo:** los docs de horror conservan su contenido de género + apuntan a core para lo agnóstico; nada se borró.
