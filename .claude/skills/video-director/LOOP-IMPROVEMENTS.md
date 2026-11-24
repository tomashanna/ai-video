# LOOP-IMPROVEMENTS.md — Histórico de mejoras al loop de producción

> Documento vivo. Cada mejora aquí nace de fricción real medida en una sesión de producción, no de teoría. Lo que se documenta acá ya existe como gate operativo en algún lado (script, doc, workflow). Este archivo captura el **por qué** para que un agente futuro entienda la razón histórica.

---

## Sesión 2026-05-10 — mina-abandonada v6 → v7d (8.5 → 10/10)

### Las 7 fricciones identificadas y su resolución

| # | Fricción | Costo en la sesión | Resolución | Doc/script |
|---|----------|-------------------|------------|------------|
| 1 | Render fail por CPU contention con otro agente | ~45 min (3 EPIPE consecutivos) | Lockfile global de renders | `ai-video render-lock` + `PIPELINE.md` § 11 |
| 2 | Imagen <1s no detectada automáticamente | 1 re-render (~12 min) | Lint extendido con check de visibilidad efectiva | `ai-video audit-narrative` + `AUDIT.md` |
| 3 | data-duration < GSAP opacity:0 timestamp | 1 re-render (~12 min) | Check `data_duration_too_short` en audit | mismo script |
| 4 | z-index black-overlay > caption-wrap | 1 re-render (~12 min) | Check `z_index_covers_captions` en audit | mismo script |
| 5 | Gemini QA permisivo con flash <1s | Detectado solo por humano | Gate humano post-Gemini de 7 checks | `HUMAN-CHECKLIST.md` |
| 6 | Captions Whisper desincronizados con beats del black overlay | 1 iteración extra | Documentado en anti-patterns | `ANTI-PATTERNS.md` |
| 7 | Assets huérfanos ($$$ desperdiciados) | ~$0.10 + entropy | Check `orphan_asset` en audit | mismo script |

**Total tiempo recuperado por sesión futura:** estimado ~45-60 min de las ~75 min totales que tomó esta sesión.

---

## Las 3 mejoras top de mayor impacto

### 🥇 1. `ai-video audit-narrative` — pre-render gate automatizado

**Sin esto:** cada bug estructural (visibilidad <1s, z-index conflict, data-duration mismatch) cuesta un re-render completo (~12 min) más diagnóstico (~5 min) más el escribir el fix (~3 min) ≈ 20 min por bug.

**Con esto:** el audit corre en <1s antes del render. Si falla, el agente ve el error con timestamp y fix sugerido, edita, y NO renderiza basura.

**ROI:** ~15-20 min por bug atrapado. En esta sesión hubiera atrapado 3 bugs = ~45 min ahorrados.

### 🥈 2. `ai-video render-lock` — coordinación entre agentes

**Sin esto:** cuando dos Claudes corren simultáneamente con tareas pesadas, FFmpeg pierde CPU y muere con SIGTERM. El mensaje de error NO sugiere "wait for the other agent" — sugiere bugs imaginarios.

**Con esto:** el agente ve el estado del lock antes de renderizar. Si está ocupado, `wait` automáticamente.

**ROI:** elimina los falsos diagnósticos. Las 3 fallas EPIPE de esta sesión hubieran sido 0.

### 🥉 3. `HUMAN-CHECKLIST.md` — gate humano post-Gemini

**Sin esto:** confiar en Gemini ≥9.7 como criterio único de "listo". Pero Gemini dio 9.5 al video v7c con un flash <1s claramente visible al ojo humano (caso histórico). Subir un video imperfecto a Instagram es peor que iterar 12 min más.

**Con esto:** 2 minutos de revisión humana scripted, con 7 preguntas concretas. Captura el 5-10% que Gemini no ve.

**ROI:** evita publicar videos con bugs sutiles. No hay reversa de un Reel ya subido.

---

## Filosofía de los gates

```
Gemini QA (≥9.7)  →  ai-video audit-narrative (0 errors)  →  ai-video audit-frames (≤2 issues)  →  ai-video qa-gate  →  HUMAN CHECKLIST  →  PUBLICAR
   semántico         estructural                          subjetivo
   automático        automático                           humano (~2 min)
```

Cada gate cubre lo que los otros NO:
- **Gemini** captura calidad narrativa, ritmo, atmosfera, edición general
- **Audit** captura issues estructurales/técnicos (visibility, z-index, durations)
- **Human checklist** captura issues subjetivos y de "feel" que ni Gemini ni audit ven

**Los 3 son obligatorios.** Skippear uno es un anti-pattern.

---

## Mejoras secundarias identificadas — pendientes de implementación

Documentadas acá como roadmap. Implementar solo cuando aparezca un bug real que las justifique.

| Mejora | Impacto | Esfuerzo | Trigger para implementar |
|---|---|---|---|
| Preview render selectivo (`--segment H4`) | Alto si HF lo soporta nativo | Depende de HyperFrames | Cuando una sesión tenga >5 iteraciones por proyecto |
| `record-version.sh` automatizado (diff entre versiones) | Medio | 1h | Cuando un proyecto pase de 10 versiones |
| Anti-patterns como lint rules (no solo doc) | Alto largo plazo | 2-3h | Cuando 3+ anti-patterns nuevos aparezcan |
| `caption-beats.json` post-Whisper (cruce caption vs GSAP) | Alto | 1-2h | Cuando aparezca el 2do bug "caption A sobre imagen B" |
| Asset usage report (más detallado que orphan check) | Bajo | 30 min | Cuando un proyecto tenga >50 assets |
| Mix-volume balance check (ffprobe + tabla) | Medio | 2h | Cuando un render tenga música tapando narración |

---

## Cómo agregar una mejora futura aquí

1. Identificar una fricción **real medida en una sesión** (no teoría)
2. Cuantificar el costo (minutos perdidos, créditos gastados, calidad perdida)
3. Proponer la resolución
4. Implementar la resolución (script, doc, o ambos)
5. Documentar acá:
   - Sesión donde se identificó
   - Costo medido
   - Resolución concreta
   - Doc/script donde vive ahora

---

## Reglas para evitar over-engineering del loop

1. **Nada de gates especulativos.** Cada gate solo nace de un bug real. Los gates falsos-positivos erosionan la confianza y se ignoran.
2. **Cada gate <2 min de costo.** Si tarda más, no se va a correr consistentemente.
3. **Cada gate da output accionable.** No "fail abstracto" — siempre con razón + fix sugerido.
4. **Los gates se ordenan por costo creciente.** Lo barato y automático primero (lint, audit), lo caro y manual después (human checklist).
5. **Documentar el "por qué".** Sin esto, el próximo agente borra el gate sin entender qué cubría.
