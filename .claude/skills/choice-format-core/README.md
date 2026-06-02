# choice-format-core — Capa A.5 (núcleo AGNÓSTICO de la familia CHOICE)

> **Qué es esto:** la mecánica **agnóstica de género** del formato **CHOICE** ("Elige a tu compañero"). Es lo que es COMÚN a TODOS los géneros choice (horror, sport, y los que vengan). Vive en su propia capa, entre el toolkit técnico universal (`ai-video-production/`) y los skills de género (`horror-choice-format/`, `sport-choice-format/`).
>
> **NUNCA se activa sola.** No es un skill de género. No produce videos por sí misma. La **heredan** los skills de género.
>
> **Última actualización:** 2026-06-01 (creación — extracción agnóstica desde `horror-choice-format/` post directiva "lo agnóstico no puede vivir dentro de un template específico").

---

## ⛔ Por qué existe esta capa (el problema que resuelve)

Antes de esta capa, la mecánica agnóstica del formato choice (hook dyad + countdown 3-2-1 + loading bar + botones A/B + decisión→consecuencia + counterfactual + cliffhanger + CTA loop + framing acción-condicional + POV 1ª persona) vivía **DENTRO de `horror-choice-format/`**. Cuando nació `sport-choice-format/`, lo correcto habría sido que heredara la mecánica de una capa neutral; en cambio la heredaba de **horror** (un hermano heredando de otro hermano). Eso acopla sport a horror y arrastra sabor de género donde no corresponde.

**Fix arquitectural:** la mecánica agnóstica se extrae a `choice-format-core/` (Capa A.5). Tanto `horror-choice-format/` como `sport-choice-format/` (y futuros géneros choice) **heredan de core**, no entre sí.

```
                 ai-video-production/        ← Capa A: técnica UNIVERSAL (cualquier video AI)
                         ▲
                         │ (core APUNTA a A para técnica universal — NO la duplica)
                         │
                 choice-format-core/         ← Capa A.5: mecánica AGNÓSTICA de la familia CHOICE  ← ESTE DIRECTORIO
                    ▲             ▲
                    │             │
       horror-choice-format/   sport-choice-format/   ← Capa B: skills de GÉNERO (sabor concreto)
       (terror, body horror)   (fútbol, gloria/burla)
```

---

## 🧱 Las 3 capas (contrato arquitectural)

| Capa | Directorio | Dominio | Ejemplo de contenido |
|------|------------|---------|----------------------|
| **A — UNIVERSAL** | `ai-video-production/` | Técnica de CUALQUIER video AI | TTS, image gen, SFX, captions Whisper, render, HYBRID per-clip-atomic, MODEL-CAPABILITIES, mastering -14 LUFS, mix volumes, 8 gates, scripts, motion primitives |
| **A.5 — CORE CHOICE** *(este dir)* | `choice-format-core/` | Mecánica AGNÓSTICA de la familia choice (común horror + sport) | esqueleto hook→played-path→counterfactual→cliffhanger, decisión→consecuencia, framing acción-condicional, countdown/loading/botones A/B, POV 1ª persona, español neutral, ~90s, "orden hablado = orden de botones", decision-UI editorial pacing, UI safe zones choice, caption chunking, lip-sync rule, rotación entre videos |
| **B — GÉNERO** | `horror-choice-format/`, `sport-choice-format/` | Sabor concreto del género | horror: body horror, monstruos, malo/bueno aparente, archetypes P1-P10, cliffhanger "Paz perdida", SFX/voces de horror, 8 canonical-scenes virales · sport: dos recorridos, asimetría por favorito, catálogo de fracaso, narración-no-juzga, SFX fútbol, política A/B |

**Regla de oro:** modificar Capa A sirve a TODOS los videos AI. Modificar A.5 sirve a TODOS los géneros choice. Modificar B sirve solo a ese género. Si dudás dónde poner algo y es choice-pero-no-de-un-género-puntual → A.5. Si tiene sabor de un género → B.

---

## 🔭 La lente de lectura — 🟦 / 🟩 / 🟥

Toda elección creativa en core se expresa con este marco (NUNCA como regla binaria rígida):

- 🟦 **PRINCIPIO (mandatorio)** — invariante del formato. Romperlo colapsa la mecánica choice.
- 🟩 **VARIABILIDAD (libre)** — el espacio creativo del género/video. Acá vive la creatividad.
- 🟥 **ANTI-PATTERN (evitar)** — patrón que rompe el formato; nunca hacerlo.

Si algo en core suena a "regla rígida" sobre una decisión creativa, es un bug de framing.

---

## 📄 Documentos en core

| Doc | Rol | Lo lee… |
|-----|-----|---------|
| `README.md` *(este)* | Front door + contrato de capas | quien orienta el sistema |
| `SKILL.md` | Índice del core + orden de lectura | arquitecto / ingeniero / auditor de cualquier género choice |
| `CHOICE-MECHANIC.md` | Autoridad CREATIVA agnóstica (esqueleto, invariante, decisión→consecuencia, framing acción-condicional, counterfactual, cliffhanger, CTA, POV, dilema-mechanics, patterns abstractos) | 🏛️ ARQUITECTO de cualquier género choice |
| `INGENIERO-CHOICE-CORE.md` | Autoridad TÉCNICA choice-específica (decision-UI editorial pacing, UI safe zones, caption chunking, lip-sync, 0-cuts-en-hook) **+ tabla de técnica universal heredada → apunta a `ai-video-production/`** | 🛠️ INGENIERO de cualquier género choice |
| `ROTATION-RULES.md` | Regla agnóstica de rotación entre videos (no repetir pattern/rol/setting/jugada-clave consecutivos; consultar el video-log del género) | los 3 roles antes de diseñar un video nuevo |

---

## ⛔ Lo que NO está acá (y por qué)

| NO está en core | Vive en… | Por qué |
|-----------------|----------|---------|
| **Técnica universal** (LUFS -14, mix volumes, render, HYBRID per-clip atomic, MODEL-CAPABILITIES, cost cap, TDD, Whisper sync mechanism, motion primitives, mastering, 8 gates) | `ai-video-production/` (Capa A) | Ya es agnóstica y universal. **Core NO la duplica — la APUNTA** (ver `INGENIERO-CHOICE-CORE.md § tabla heredada-universal`). Duplicarla crearía una tercera copia que se desincroniza. |
| **Sabor de horror** (body horror, monstruos uncanny, malo/bueno aparente con contenido horror, archetypes P1-P10 horror, "Paz perdida", SFX/voces de horror, 8 canonical-scenes virales, BRAND/TASTE-LOG/video-log de horror, INTRO-FORMULA con sabor horror) | `horror-choice-format/` (Capa B) | Es contenido de un género. Core captura la FORMA abstracta (p. ej. "apariencia × verdad"), no el CONTENIDO horror. |
| **Sabor de sport** (dos recorridos, asimetría por favorito, catálogo de fracaso, fallo-de-jugador, narración-no-juzga, REGLA DE AMBIENTE, SFX fútbol, política A/B) | `sport-choice-format/` (Capa B) | Es contenido del género deportes. |
| **El registro de videos producidos** (video-log de horror, video-log de sport) | el skill de cada género | Cada género mantiene su propia bitácora de rotación. Core solo define la REGLA de rotación, no el log. |

---

## 🔗 Lineaje empírico (de dónde sale el contenido agnóstico)

El contenido creativo agnóstico de core deriva de la autoridad empírica de `horror-choice-format/PAUTA-MASTER.md` (8 videos virales canónicos del formato "Elige a tu compañero"). El contenido técnico choice-específico deriva de `horror-choice-format/INGENIERO-PAUTA-MASTER.md` (mediciones F1 de 10 referentes). Core **preserva esa atribución** en cada métrica, de modo que el origen empírico no se pierde al generalizar. Sport-choice es pre-empírico: hereda la mecánica validada de core y valida su LÓGICA deportiva con sus propios videos.

> **Importante:** core es la **versión canónica agnóstica**. Las secciones equivalentes en `horror-choice-format/` quedan como la **aplicación a horror** + apuntan a core para lo agnóstico. Si core y un doc de género discrepan sobre la MECÁNICA, gana core.
