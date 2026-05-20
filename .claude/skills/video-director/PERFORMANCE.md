# PERFORMANCE.md — Feedback loop de performance real

> Gemini mide calidad técnica. Instagram mide impacto. Sin este loop, podés tener 9.7/10 técnico y 2/10 en performance. Este doc cierra el gap.

---

## Propósito

Cerrar el ciclo entre **calidad técnica** (Gemini QA) y **performance real** (Instagram metrics). Sin esto:
- No sabés qué patterns funcionan en el mercado vs los que solo lucen bien técnicamente
- Las docs canónicas evolucionan en base a hipótesis, no evidencia
- Un anti-pattern real (que NO viraliza) puede convivir indefinidamente en las docs como "regla canónica"

Este sistema convierte cada video publicado en **data** que mejora el sistema entero.

---

## Filosofía del sistema

1. **Captura simple, análisis riguroso.** 5 min de captura, decisiones basadas en data acumulada.
2. **Patterns sobre opiniones.** Si vos creés que X funciona y los números muestran que no, ganan los números.
3. **Patience con N=1.** Un video bueno no valida un pattern. Tres sí. Cinco lo cementan.
4. **Bottom performers son tan valiosos como top.** Si algo no funcionó, identificá por qué.
5. **Cross-account = oro.** Un pattern que funciona en MÚLTIPLES nichos = regla universal.

---

## Estructura de archivos

```
.claude/skills/video-director/
  ├── PERFORMANCE.md                    ← Este doc (cómo funciona el sistema)
  ├── PATTERNS-LIBRARY.md               ← Catálogo vivo de patterns
  └── templates/
       └── video-performance-template.md ← Template a copiar por video

<proyecto-cuenta>/performance/           ← Capturas por cuenta (en cada repo de cuenta)
  ├── 2026-05-15-bosque-abandonado.md
  ├── 2026-05-20-mina-abandonada.md
  └── ...
```

**Importante**: las capturas por video viven con el proyecto/cuenta, no acá. Esta carpeta tiene SOLO el sistema, no la data.

---

## Cuándo capturar — T+48h

Una captura por video, 48h después de publicar.

**Por qué T+48h**:
- La mayoría del growth orgánico en Reels pasa en las primeras 24-48h
- Captura completa, no parcial
- Suficiente data para detectar éxito o flop
- Simple de mantener — una sesión por video

**Si un video tiene long tail (sigue creciendo a los 7d+)**: anotalo manualmente como nota al pie en su archivo. No es la regla, es excepción.

---

## Métricas mínimas — las 6 que importan

| Métrica | Por qué |
|---|---|
| **Views** | Reach del algoritmo |
| **Watch time avg / completion %** | Calidad del hook + retention. La métrica más predictiva. |
| **Likes** | Engagement pasivo |
| **Comments** | Engagement activo. Si pediste CTA en el video, contá cuántos responden. |
| **Saves** | Señal de valor percibido. Saves alto = "guardo para mostrar a alguien". |
| **Shares** | Viralidad real. Cada share es 1 nuevo viewer fuera de tu reach |

Profile visits es bonus si lo capturás. Demographics y reach vs impressions los ignoramos al inicio.

---

## Cómo se calcula "vs promedio de la cuenta"

Después de tener 5+ videos en una cuenta, comparás cada nuevo video contra el **rolling average de los últimos 10 videos** (o todos si hay <10).

| Resultado vs promedio | Etiqueta |
|---|---|
| **+50% o más** | Top performer ⭐ |
| **+20% a +50%** | Above average |
| **-20% a +20%** | Average |
| **-20% a -50%** | Below average |
| **-50% o más** | Bottom performer |

Esta clasificación define qué patterns merecen revisarse.

---

## El loop — qué hacer con cada captura

```
1. Captura métricas (5 min)
   ↓
2. Comparar vs promedio de la cuenta
   ↓
3. Anotar hipótesis (qué funcionó, qué no)
   ↓
4. Cada 10 videos → meta-review
   ↓
5. Promover patterns o actualizar anti-patterns
   ↓
6. Update docs canónicas (PATTERNS-LIBRARY, MOTION-LAYER, CAPTIONS, etc.)
```

---

## Meta-review (cada 10 videos)

Cada 10 videos publicados en una cuenta (o cuando acumulás 10 capturas entre todas las cuentas):

### Paso 1 — Tabular
Hacer una tabla con todos los 10 videos: score Gemini, performance class, top patterns detectados.

### Paso 2 — Identificar repetidores
Patterns que aparecen en 3+ top performers (de los 10) → **candidato a regla canónica**.
Patterns que aparecen en 3+ bottom performers → **candidato a anti-pattern**.

### Paso 3 — Cross-check con score Gemini
- Si pattern es top performer Y Gemini lo calificaba alto → consistente, upgrade a regla canónica
- Si pattern es top performer Y Gemini lo calificaba bajo → **insight**, el sistema técnico no lo valoraba bien, ajustar prompt de Gemini QA
- Si pattern es bottom performer Y Gemini lo calificaba alto → **insight**, hay un gap entre técnica y mercado, investigar

### Paso 4 — Actualizar PATTERNS-LIBRARY.md
- Mover de "evaluación" a "validado" lo que cumple 3+
- Agregar nuevos anti-patterns
- Anotar cross-account confirmations

### Paso 5 — Cascade a docs canónicas (si aplica)
Si un pattern validado en `PATTERNS-LIBRARY` debería estar en:
- `ai-video-production/MOTION-LAYER.md`
- `ai-video-production/CAPTIONS.md`
- `ai-video-production/SFX-PIPELINE.md`
- `horror-choice-format/PATTERNS.md`
- `video-director/ANTI-PATTERNS.md`

→ Actualizar la doc canónica, citando el origen ("validated 2026-05 across 3 top performers: bosque-v2, mina-v3, X").

---

## Cómo se promueven patterns — los 3 niveles

### Nivel 1 — En evaluación (1-2 videos)
Cualquier pattern descubierto en un video. No accionable todavía. Solo se documenta para tracking.

### Nivel 2 — Validado (3+ videos top performers, misma cuenta)
Pattern confirmado en el contexto de UN nicho/formato. Va a:
- `PATTERNS-LIBRARY.md` § Validado format-specific
- Posiblemente al skill del formato (`horror-choice-format/PATTERNS.md`)

### Nivel 3 — Universal (3+ videos top performers, 2+ cuentas)
Pattern que funciona en MÚLTIPLES nichos. Es regla viral genuina. Va a:
- `PATTERNS-LIBRARY.md` § Universal
- Cascade a `ai-video-production/` docs (motion, captions, SFX, etc.) según aplique

---

## Bottom performers — qué hacés

**Política: dejar publicados, aprender en silencio.**

- NO ocultar / archivar (la cuenta debe verse natural, con altibajos)
- NO usar como contenido educativo público (todavía — eso es Fase 2 del meta-brand)
- SÍ identificar el pattern que falló:
  - ¿Hook débil?
  - ¿Tema sin demand?
  - ¿Timing mal?
  - ¿Calidad técnica baja (Gemini <9.0)?

Si el pattern negativo aparece 3 veces → upgrade a anti-pattern en `PATTERNS-LIBRARY.md` y propagación a `ANTI-PATTERNS.md` del video-director.

---

## Anti-patterns DE ESTE SISTEMA (cosas que NO hacés)

- ❌ **Capturar parcialmente** (solo views, sin saves/shares). Métricas a medias dan decisiones a medias.
- ❌ **Concluir patterns con N=1.** Un video viral NO valida un pattern. Esperá 3.
- ❌ **Comparar entre cuentas con audiences distintas.** Compará dentro de una cuenta (vs su promedio).
- ❌ **Borrar capturas viejas.** Toda la data acumulada es valiosa.
- ❌ **Decidir sin captura.** Si publicaste un video y no capturaste a T+48h, lo perdiste como data.
- ❌ **Ignorar bottom performers.** Son tan valiosos como top performers para identificar patterns negativos.
- ❌ **Actualizar docs canónicas con N<3.** Disciplina: 3+ casos o no se mueve.

---

## Ejemplo: ciclo completo de 1 video

### T+0 — Publicación
- Video: `bosque-abandonado v2`
- Score Gemini: 9.1/10
- Hipótesis pre-publicación: "SFX heartbeat y white flash con sub-bass deberían mantener retention en H2 (loading bar)"

### T+48h — Captura
Copiar template a `bosque-abandonado/performance/2026-05-15-bosque-abandonado-v2.md`. Llenar las 6 métricas + comentarios.

### T+50h — Análisis
- Views: 12,400 (sin promedio aún, es video #2)
- Saves: 89 → alta proporción vs likes
- Comments: 234 → muchos responden A o B (CTA funcionó)
- Hipótesis confirmada: ✓ retention en H2 buena (62% del audience pasa el 0:11-0:15)

Anotar en `PATTERNS-LIBRARY.md` § En evaluación:
> "White flash + SFX sub-bass en A/B → retention flat en transición. Validar en próximo video."

### T+30 días (después de 10 videos)
Meta-review. Si el pattern aparece en 3+ top performers → upgrade.

---

## Cuándo NO usar este sistema

- Videos de prueba / drafts no publicados (no hay métricas que capturar)
- Re-uploads del mismo video (la captura va al primer publish, no al re-upload)
- Stories vs Reels (este sistema es para Reels — Stories tienen métricas distintas)

---

## Última actualización

2026-05-10. Inicial. Sistema diseñado para empezar con captura manual + escalar después a API automation si la cantidad de videos lo justifica.
