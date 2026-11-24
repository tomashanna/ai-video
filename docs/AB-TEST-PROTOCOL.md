# A/B Test — v1 prescriptivo vs v2 identitario (protocolo PRE-REGISTRADO)

> **Qué se testea.** La capa de PROMPTS de los 3 agentes — única variable. v1 = corpus
> prescriptivo actual (docs/OPERATING-MANUAL.md 34KB + lectura obligatoria + reglas explícitas).
> v2 = prompts identitarios (~1 página por rol: quién sos + valores + heurísticas +
> límites + punteros) + docs/OPERATING-MANUAL.md router slim.
>
> **Qué NO se testea (idéntico en ambos brazos).** Los rails: gates determinísticos
> (8 canónicos + validators Fase 0 wave 1+2), lib/empirical_bands, F1 JSONs, library,
> referentes canónicos, SPEC schema v11, flujo CP1-CP5 con gates de auditor, checkpoints
> humanos, HUMAN-CHECKLIST. Si un rail cambia durante el experimento → cherry-pick a
> ambos brazos ANTES del siguiente video.
>
> **Regla de pre-registro.** Este doc se committea ANTES de correr el primer video del
> experimento. La regla de decisión (§5) NO se modifica después de ver resultados.

---

## 1. Hipótesis

**H1**: los agentes identitarios (v2) producen calidad ≥ v1 con MENOS fricción
(iteraciones, tiempo de Tomás, escaladas evitables), porque el juicio generaliza donde
las reglas memorizadas fallan, y los rails cazan lo mecánico en ambos brazos.

**H0 (nula)**: sin los prompts prescriptivos, v2 comete errores de clase CONOCIDA que
los gates no cubren (el 26% juicio-irreducible), degradando calidad o aumentando
iteraciones.

## 2. Mecánica de los brazos

| | v1 (control) | v2 (tratamiento) |
|---|---|---|
| Working dir | `` (main) | worktree `~/AI-video-1-v2/` (branch `v2-identity`) |
| System prompt | docs/OPERATING-MANUAL.md prescriptivo actual | docs/OPERATING-MANUAL.md router slim → `agents/{ARCHITECT,ENGINEER,AUDITOR}.md` |
| Skills/docs | Lectura obligatoria § 0.3 (13 items) | Consulta on-demand vía punteros de identidad |
| Rails | idénticos | idénticos |
| Memoria auto-inyectada | la del path v1 (existente) | la del path v2 (arranca limpia — control más puro) |
| `.env` / API keys | existente | copiar manualmente al worktree (gitignored) |

El directorio determina el cerebro: abrir el terminal del rol en el working dir del
brazo correspondiente. **NUNCA mezclar** (un rol de v2 leyendo docs con un agente
arrancado en v1 contamina el brazo).

## 3. Protocolo por video

1. **Mismo brief**: Tomás define UN brief (tema/género/delivery) y lo entrega idéntico
   a ambos brazos. Mínimo **2 videos por brazo** (n=1 es anécdota); ideal 3.
2. **Orden alternado** para matar el efecto aprendizaje: video A → v1 primero;
   video B → v2 primero. (El segundo brazo de cada video NO debe ver outputs del primero.)
3. **Flujo completo en cada brazo**: arquitecto → SPEC → auditor → CP1-CP5 con gates →
   pre-render-gate → render final. Mismos budget caps ($9/video).
4. **Logging obligatorio durante la corrida** (por brazo, en una tabla simple por video):
   - iteraciones por CP (conteo)
   - bugs por catcher: ¿lo cazó un GATE (exit 1), el AUDITOR (finding), o TOMÁS (post-hoc)?
   - escaladas (¿cuántas, evitables?)
   - minutos de Tomás (interacción real)
   - costo API total (Replicate + ElevenLabs + Gemini + Claude)
   - veces que el agente citó autoridad inexistente o inventó una regla (proxy de drift)
5. **Evaluación A CIEGAS**: los renders finales se renombran (`render-X.mp4`,
   `render-Y.mp4` — un tercero o un script baraja) y Tomás los puntúa perceptual 1-10
   SIN saber qué brazo produjo cuál. Recién después se desbloquea el mapping.
6. Calibrated v4 corre sobre ambos (no es ciego pero es determinístico).

## 4. Métricas (primarias y secundarias)

| Métrica | Tipo | Gana quien… |
|---|---|---|
| Perceptual de Tomás (ciego) | PRIMARIA calidad | ≥ del otro brazo (empate vale) |
| Regresiones de clase conocida (fixtures/gates en FAIL final) | PRIMARIA seguridad | tenga CERO |
| Iteraciones totales hasta ship | PRIMARIA fricción | menos |
| Minutos de Tomás | PRIMARIA fricción | menos |
| Calibrated v4 | secundaria | informativo |
| Costo API | secundaria | menos |
| Bugs cazados por gate vs auditor vs Tomás | secundaria diagnóstico | (más temprano = mejor sistema) |
| Reglas inventadas / autoridad mal citada | secundaria drift | menos |

## 5. Regla de decisión (FIJADA — no se toca post-resultados)

**ADOPTAR v2** si en el agregado de los videos del experimento:
1. Perceptual ciego de v2 ≥ v1 (promedio, tolerancia -0.2), **Y**
2. v2 tiene 0 regresiones de clase conocida (todos los gates/fixtures verdes al ship), **Y**
3. v2 reduce fricción (iteraciones O minutos de Tomás, al menos una de las dos, sin
   empeorar la otra >20%).

**MANTENER v1** si v2 pierde en perceptual por >0.2 promedio O tiene ≥1 regresión de
clase conocida.

**HÍBRIDO** (resultado más probable): si v2 gana en unos roles y pierde en otros →
adoptar identidad por-rol donde ganó (p.ej. ingeniero identitario + arquitecto
prescriptivo) y re-testear el rol perdedor tras iterar su identity file.

En cualquier resultado: los rails construidos en Fase 0 quedan (sirven a ambos).

## 6. Qué invalidaría el experimento (abortar y re-correr)

- Un rail divergió entre brazos a mitad de un video (gate distinto, lib distinta).
- El mismo terminal/contexto sirvió a ambos brazos en el mismo video.
- La evaluación no fue ciega (Tomás supo el mapping antes de puntuar).
- El brief cambió entre brazos ("aprovechá y agregale X" a uno solo).

## 7. Estado

- [ ] Fase 0 wave 1 shipped (7 gates + lib) ✅ 2026-06-04
- [x] Fase 0 wave 2 shipped (decision-UI + AVU + videolog + invariantes health-check) ✅ 2026-06-04
- [x] Branch `v2-identity` + worktree creado ✅
- [x] `agents/ARCHITECT.md` + `ENGINEER.md` + `AUDITOR.md` escritos (destilación 2026-06-04) ✅ 2026-06-04
- [x] docs/OPERATING-MANUAL.md router slim en v2 ✅
- [x] `.env` copiado al worktree ✅
- [ ] Video 1 del experimento: brief definido → corrido en ambos brazos → evaluado ciego
- [ ] Video 2 (orden invertido)
- [ ] Decisión per §5
