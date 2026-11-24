# DECISION-FRAMEWORK.md — Cuándo preguntar vs ejecutar

> El costo de pausar para confirmar es bajo. El costo de un cambio destructivo no deseado es muy alto. Pero también: preguntar todo destruye el flow. Esto define el límite.

---

## Eje principal: blast radius + reversibilidad

```
                  ALTO BLAST RADIUS
                          │
            (PREGUNTAR)   │   (PREGUNTAR + ESCALAR)
                          │
                          │
   IRREVERSIBLE ──────────┼────────── REVERSIBLE
                          │
                          │
            (DEPENDE)     │   (EJECUTAR)
                          │
                  BAJO BLAST RADIUS
```

**Cuadrante por defecto: ejecutar.**

---

## Matriz concreta — qué hacer sin preguntar

| Acción | Decisión |
|---|---|
| Leer cualquier archivo del proyecto | ✅ Ejecutar |
| Editar HTML / GSAP / CSS local | ✅ Ejecutar |
| Crear nuevo archivo en `assets/` o `scripts/` | ✅ Ejecutar |
| Ejecutar lint | ✅ Ejecutar |
| Medir duración con ffprobe | ✅ Ejecutar |
| Loop expansion con ffmpeg | ✅ Ejecutar |
| Aplicar atempo 2x a TTS | ✅ Ejecutar |
| Generar 1 imagen con `ai-video image` (~$0.04) | ✅ Ejecutar |
| Whisper sobre audios ya generados | ✅ Ejecutar (cero costo) |
| Update memory file | ✅ Ejecutar |
| Crear / completar TaskCreate | ✅ Ejecutar |

---

## Qué hacer con check rápido (1 frase de heads-up, después ejecutar)

| Acción | Heads-up requerido |
|---|---|
| Render draft de un video (~8-15 min) | "Lanzo render draft, ~10 min." |
| Generar 5+ imágenes (~$0.20) | "Genero 5 variantes, ~$0.20." |
| Generar batch de SFX (~$0.50-2) | "Batch de N SFX, ~$Xcred." |
| Boost de volumen masivo a audios | "Boost +10dB a los 12 narration files." |
| Refactor que toca >5 archivos | "Refactor toca 7 archivos, lo hago en bloque." |
| Eliminar archivos generados (regenerar) | "Borro los `-raw.mp3` viejos." |

---

## Qué requiere CONFIRMACIÓN explícita (esperar respuesta)

| Acción | Por qué preguntar |
|---|---|
| Borrar `assets/` o archivos grandes | Irreversible sin regenerar |
| Sobrescribir `index.html` con changes que el usuario no vio | Pérdida de trabajo |
| Generar 20+ imágenes (>$1) | Costo + tiempo significativo |
| Render high quality (~30-45 min) | Recursos + tiempo |
| Cambiar voice ID, STYLE_SUFFIX, paleta | Decisión creativa del usuario |
| Tirar abajo y rehacer un video | Scope decision |
| Cualquier acción destructiva en git (force push, reset --hard) | Pérdida de trabajo |
| Modificar skills (`.claude/skills/`) | Cambia futuras sesiones |
| Modificar memory (`~/.claude/projects/.../memory/`) | Cambia futuras sesiones |
| Publicar / subir a Instagram | Acción pública irreversible |
| Cambiar la narrativa / texto del guion | Decisión creativa |
| Re-render cuando el QA es decente y el usuario no pidió iterar | Tiempo |

---

## Decisiones creativas — siempre del usuario

NUNCA decides vos:
- Qué texto narra el video.
- Qué personajes hay.
- Qué dilema moral se plantea.
- Qué CTA final usar.
- Música elegida.
- Voz elegida.
- Estilo visual / paleta.
- Cuándo publicar.

Tu rol: ejecutar la visión con quality bar técnico.

---

## Heurística para casos no listados

Antes de actuar preguntate:

1. **¿Es reversible?** Si sí + barato → ejecutar.
2. **¿Cuánto cuesta deshacer?** Si <30s → ejecutar. Si >5min → preguntar.
3. **¿Lo está esperando el usuario?** Si pidió "renderiza todo" → ejecutar la cadena. Si fue ambiguo → confirmar.
4. **¿Afecta archivos / state fuera del proyecto?** Si sí (skills, memory, settings) → preguntar.
5. **¿Cuesta créditos / tiempo real?** Si >$1 o >15min → heads-up explícito.

---

## Cuándo escalar al usuario (mid-task)

Aún si vas a ejecutar, **informá** cuando:

- Encontrás un bug que no estaba en el scope original.
- Detectás que el usuario asume algo que técnicamente no funciona.
- El plan original ya no aplica (encontraste un blocker).
- El siguiente paso cuesta significativamente más de lo previsto.
- Descubrís un anti-pattern que está en otra parte del código.

Formato: 1 frase de descripción + qué hacés tú + qué necesitás del usuario (si algo).

---

## Cuándo usar AskUserQuestion vs pregunta libre

| Caso | Usar |
|---|---|
| Hay 2-4 opciones discretas mutuamente excluyentes | `AskUserQuestion` |
| Decisión creativa con multiple paths | `AskUserQuestion` |
| Confirmar approach técnico (A vs B vs C) | `AskUserQuestion` |
| Yes/no simple | Pregunta libre en el output |
| Detalle muy específico ("¿cuál es la URL?") | Pregunta libre |
| Necesitás OK para algo destructivo | Pregunta libre, una frase |

**Regla**: si vas a escribir 4+ líneas explicando la decisión, mejor `AskUserQuestion`.

---

## Plan mode (si está activado)

Si el usuario activa plan mode (Shift+Tab x2), NO ejecutás. Solo planeás.

Salida válida: `ExitPlanMode` con el plan completo. El usuario aprueba o ajusta.

---

## Casos límite reales (de proyectos previos)

### Caso 1: "Aplicá todos los fixes de Gemini"

Gemini sugirió 4 fixes. ¿Pregunto antes de aplicar cada uno?

**Decisión**: NO. El usuario delegó la ejecución. Apliclo todo, reportá después con score nuevo.

### Caso 2: "Mejorá la legibilidad"

Ambiguo. ¿Aumento font-size? ¿Stroke? ¿Cambio de color?

**Decisión**: PREGUNTAR. Tres approaches con trade-offs distintos. `AskUserQuestion`.

### Caso 3: "Renderizar"

Claro. Lanzo el comando documentado.

**Decisión**: EJECUTAR con heads-up de tiempo estimado.

### Caso 4: Encontrar el video v1.mp4 viejo (1 GB)

**Decisión**: NO BORRAR. El usuario quizás lo quiere de referencia. Si querés mencionarlo, mencionalo, pero no toques.

### Caso 5: Voice ID en TTS está mal (default vs correcto)

**Decisión**: FIX directo. Es un bug documentado en feedback_voice_audio.md. Aplicar y reportar.

### Caso 6: "Hacelo perfecto"

Hyperbólico. **Decisión**: traducir a "≥9.7 Gemini score" y proceder con quality bar. Si requiere muchas iteraciones, hacer scope-cut explícito.
