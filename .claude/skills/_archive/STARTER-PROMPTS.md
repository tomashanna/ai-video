# STARTER-PROMPTS.md — Prompts copy-paste para cada tipo de tarea

> Prompts pre-armados que FUERZAN al editor IA a leer las docs correctas antes de ejecutar. Copy-paste el que corresponde al inicio de cada sesión.

**Cómo se usa**: copiá el bloque entre `═══` y pegalo como primer mensaje de la sesión. Reemplazá `<placeholders>` con tus valores.

---

## 🎬 1. VIDEO NUEVO desde cero (horror-choice)

Usá este cuando arrancás un video nuevo del formato horror-choice (Berni vs Yonaiker, Hugo vs Santi, etc).

```
═══════════════════════════════════════════════════════════════════
Vamos a crear un video horror-choice nuevo desde cero.

ANTES de actuar, leé estos docs en orden:
1. <repo-root>/.claude/skills/video-director/SKILL.md
2. <repo-root>/.claude/skills/video-director/ARCHITECTURE.md
3. <repo-root>/.claude/skills/video-director/PROJECT-STRUCTURE.md
4. <repo-root>/.claude/skills/video-director/WORKFLOW.md
5. <repo-root>/.claude/skills/horror-choice-format/PAUTA.md
6. <repo-root>/.claude/skills/horror-choice-format/video-log.md
7. <repo-root>/.claude/skills/horror-choice-format/CREATIVE-BRIEF.md
8. <repo-root>/library/LIBRARY.md
9. <repo-root>/elements.json

DESPUÉS:
- Decime el plan completo del proyecto (slug, archetype propuesto,
  countdown + loader combo, personajes anchor).
- Verificá rotación contra video-log.md (NO repetir archetype ni componentes).
- NO ejecutes nada hasta que apruebe el plan.
═══════════════════════════════════════════════════════════════════
```

---

## 🎬 2. VIDEO NUEVO con template no-horror (formato distinto)

Usá este cuando creás el primer video de un formato nuevo (documental, educacional, etc).

```
═══════════════════════════════════════════════════════════════════
Vamos a crear un video del formato <NUEVO-FORMATO> (template no existe todavía).

ANTES de actuar, leé estos docs en orden:
1. <repo-root>/.claude/skills/video-director/SKILL.md
2. <repo-root>/.claude/skills/video-director/ARCHITECTURE.md
   (especialmente § "Cuando arrancás un TEMPLATE NUEVO")
3. <repo-root>/.claude/skills/video-director/PROJECT-STRUCTURE.md
4. <repo-root>/.claude/skills/horror-choice-format/SKILL.md
   (como REFERENCIA de cómo se estructura un format skill)
5. <repo-root>/library/LIBRARY.md

DESPUÉS:
- Decime el plan para crear el SKILL del formato nuevo
  (PATTERNS.md, VIDEO-PLAYBOOK.md, BRAND.md, etc).
- Aclará qué se reutiliza de Capa 1 universal vs qué hay que crear nuevo.
- NO ejecutes nada hasta que apruebe el plan.
═══════════════════════════════════════════════════════════════════
```

---

## 🔄 3. ITERAR un video existente (subir score Gemini)

Usá este cuando un video tiene score <9.5 y querés iterar.

```
═══════════════════════════════════════════════════════════════════
Iterar el video <PROYECTO> a v<N+1>. Score actual: <X.X/10>.

ANTES de actuar, leé:
1. <repo-root>/.claude/skills/video-director/SKILL.md
2. <repo-root>/.claude/skills/video-director/WORKFLOW.md
   (especialmente § Paso 5 ITERAR)
3. <repo-root>/.claude/skills/video-director/ANTI-PATTERNS.md
4. <repo-root>/.claude/skills/ai-video-production/QA.md
5. El render previo + reporte Gemini (si lo tenés)
6. <PROYECTO>/index.html para ver el state actual

Problemas identificados por Gemini (pegalos acá):
- (A) <problema A>
- (B) <problema B>

DESPUÉS:
- Mapea cada problema → doc del fix (per WORKFLOW § Paso 5 tabla)
- Decime los 2-3 fixes priorizados (mayor impacto primero)
- NO ejecutes nada hasta que apruebe el plan.
═══════════════════════════════════════════════════════════════════
```

---

## 🎨 4. GENERAR ASSETS (imágenes + audio para un proyecto)

Usá este cuando ya tenés el script y necesitás producir los assets.

```
═══════════════════════════════════════════════════════════════════
Generar assets para <PROYECTO>. NARRATIVE.md ya está escrito.

ANTES de actuar, leé:
1. <repo-root>/.claude/skills/ai-video-production/PIPELINE.md
2. <repo-root>/.claude/skills/ai-video-production/IMAGE-VARIETY.md
3. <repo-root>/.claude/skills/ai-video-production/CHARACTER-CONSISTENCY.md
4. <repo-root>/.claude/skills/ai-video-production/SFX-PIPELINE.md
5. <repo-root>/library/LIBRARY.md
6. <PROYECTO>/NARRATIVE.md (asset list)

ORDEN OBLIGATORIO (NO saltarse):
1. Generar TODOS los anchors de personajes PRIMERO (sin --ref)
2. Generar TTS + atempo 2x
3. Generar escenas con personajes (CON --ref al anchor)
4. Generar escenas sin personajes (sin --ref)
5. SFX: buscar en library/ primero, generar solo lo faltante

DESPUÉS:
- Decime la lista exacta de comandos image.py + tts.py + sfx.py que vas a correr
- Confirmá que cada escena con personaje incluye --ref
- NO ejecutes hasta que apruebe.
═══════════════════════════════════════════════════════════════════
```

---

## 🎞️ 5. CONSTRUIR index.html (composición HTML/GSAP)

Usá este cuando ya tenés los assets y vas a armar la composición.

```
═══════════════════════════════════════════════════════════════════
Construir index.html para <PROYECTO>. Assets ya generados.

ANTES de actuar, leé:
1. <repo-root>/.claude/skills/video-director/SKILL.md
   (las 10 hard rules)
2. <repo-root>/.claude/skills/ai-video-production/PIPELINE.md § 3
3. <repo-root>/.claude/skills/ai-video-production/MOTION-LAYER.md
4. <repo-root>/.claude/skills/ai-video-production/NARRATIVE-LED-EDITING.md
5. <repo-root>/.claude/skills/ai-video-production/CAPTIONS.md
6. <repo-root>/.claude/skills/ai-video-production/ELEMENTS-LIBRARY.md
7. <repo-root>/.claude/skills/horror-choice-format/VIDEO-PLAYBOOK.md
   (solo si formato horror-choice — sino el VIDEO-PLAYBOOK del formato)
8. <repo-root>/elements.json
9. <repo-root>/.claude/skills/horror-choice-format/video-log.md
   (para no repetir countdown/loader)

ANTES DE WIRE:
- Pickear countdown + loader compatibles (chequear matriz ELEMENTS-LIBRARY § Regla 2.3)
- Confirmar que no repiten contra video anterior (video-log.md)
- Confirmar que se mantendrán durante TODO el video (intra-video consistency)

DESPUÉS:
- Decime el plan: components elegidos, motion layer, cortes NARRATIVE-LED-EDITING aplicados
- NO empieces a editar HTML hasta que apruebe.
═══════════════════════════════════════════════════════════════════
```

---

## 🔍 6. QA + Gemini analysis (post-render)

Usá este después de un render para evaluar y decidir si iterar.

```
═══════════════════════════════════════════════════════════════════
Analizar el render <PATH> con Gemini.

ANTES:
1. Leé <repo-root>/.claude/skills/ai-video-production/QA.md
2. Leé <repo-root>/FEEDBACK-LOOP.md
3. Identificá si el formato necesita prompt extendido
   (horror-choice → leé horror-choice-format/PAUTA.md § 2)

DESPUÉS:
- Construye el prompt de Gemini (universal + dimensiones del formato)
- Corré analyze_video.py
- Reportá honestamente: score real (no padding), dimensiones débiles, fixes priorizados
- Si score >= 9.5 → recomendá publicar
- Si score < 9.5 → recomendá iteración (usar prompt #3)
═══════════════════════════════════════════════════════════════════
```

---

## 📊 7. PERFORMANCE CAPTURE (T+48h después de publicar)

Usá este 48h después de publicar un video.

```
═══════════════════════════════════════════════════════════════════
Capturar performance del video <PROYECTO> publicado el <FECHA>.

ANTES:
1. Leé <repo-root>/.claude/skills/video-director/PERFORMANCE.md
2. Leé <repo-root>/.claude/skills/video-director/templates/video-performance-template.md
3. Leé las últimas 3 capturas previas para comparar (si existen)

YO TE PASO LAS MÉTRICAS:
- Views: ___
- Watch time avg: ___
- Likes: ___
- Comments: ___
- Saves: ___
- Shares: ___
- Profile visits: ___ (opcional)

DESPUÉS:
- Copiá el template a <PROYECTO>/performance/YYYY-MM-DD-<slug>.md
- Llenalo con las métricas
- Si la cuenta tiene 5+ videos → calculá vs rolling avg
- Identificá hipótesis: qué funcionó, qué no, patterns nuevos
- Si llegamos a múltiplo de 10 videos → propone meta-review
- Actualizá video-log.md del formato con score + status publicado
═══════════════════════════════════════════════════════════════════
```

---

## 🧠 8. META-REVIEW (cada 10 videos)

Usá este después de publicar N múltiplo de 10 videos para meta-revisar patterns.

```
═══════════════════════════════════════════════════════════════════
Meta-review de los últimos 10 videos publicados.

ANTES:
1. Leé <repo-root>/.claude/skills/video-director/PERFORMANCE.md § Meta-review
2. Leé <repo-root>/.claude/skills/video-director/PATTERNS-LIBRARY.md
3. Leé las 10 capturas en <PROYECTO-cuenta>/performance/

DESPUÉS:
- Tabla con los 10 videos: score Gemini + performance class (top/avg/bottom)
- Identificá patterns que aparecen 3+ veces en top performers
- Identificá patterns que aparecen 3+ veces en bottom performers
- Promové patterns que cumplan criterio (3+ confirmaciones)
- Actualizá PATTERNS-LIBRARY.md
- Cascade a docs canónicas si aplica (MOTION-LAYER, CAPTIONS, SFX, etc.)
═══════════════════════════════════════════════════════════════════
```

---

## 🤝 9. HAND-OFF a otra IA / sesión paralela

Usá este cuando querés delegar una iteración específica.

```
═══════════════════════════════════════════════════════════════════
Necesito un prompt de hand-off para delegar la iteración v<N> de <PROYECTO>
a otra sesión / IA.

ANTES:
1. Leé <repo-root>/.claude/skills/video-director/HANDOFF-PROMPTS.md

DESPUÉS:
- Generá el prompt completo siguiendo el template canónico de 8 secciones
- Incluí paths absolutos, comandos copy-pasteables, validación
- Mostrame el prompt completo para que lo copy-paste
═══════════════════════════════════════════════════════════════════
```

---

## 🎞️ 11. ANIMAR un video existente con Replicate Kling

Usá este cuando ya tenés un render con imágenes estáticas + Ken Burns (Gemini ≥9.0) y querés elevarlo a cinematic con Kling.

```
═══════════════════════════════════════════════════════════════════
Animar el video <PROYECTO> v<N> con Replicate Kling.

PRE-CONDICIÓN: el render base ya pasó Gemini QA ≥ 9.0 con estáticas + Ken Burns.
Si NO está validado todavía, primero usar prompt #6 (QA).

ANTES de actuar, leé en orden:
1. <repo-root>/.claude/skills/video-animation/SKILL.md
2. <repo-root>/.claude/skills/video-animation/ANIMATION-LAYER.md
   (lee las 12 secciones — es el doc maestro)
3. <PROYECTO>/index.html (state actual del HTML)
4. <PROYECTO>/NARRATIVE.md (timing + asset list)

DESPUÉS:
1. Verificá setup técnico:
   - REPLICATE_API_TOKEN en <PROYECTO>/.env
   - scripts/video.py presente (sino: cp de elige-companero/scripts/video.py)
   - replicate package en el venv

2. Listá las imágenes del proyecto, clasificalas con decision tree (ANIMATION-LAYER § 1):
   ✅ Animar con Kling (close-ups, twists, cliffhangers, partículas, gestos)
   ❌ Dejar estático (wide establishing, detail shots, POV fallen)

3. Para cada imagen a animar, calculá:
   - scene_duration en el video
   - kling_tier (5s o 10s — siempre next_tier_above(scene + 0.5s))
   - prompt Kling (un movimiento principal por prompt)
   - loopable: sí/no

4. Decime el plan completo en tabla:
   | imagen | scene_dur | tier | prompt | loopable | costo |
   
   Con costo total estimado.

5. NO ejecutes nada hasta que apruebe el plan (cada clip cuesta créditos).

6. Ejecución (cuando apruebes):
   - Generar clips en batch
   - Pre-render check de cada uno ANTES de wire HTML
   - Retries hasta 3 por clip
   - Reemplazar <img> por <video> en index.html
   - Render draft del video animado
   - Gemini QA + reportá score

CRÍTICO:
- NO animar todo (8-10 de 12-15 imágenes es óptimo)
- NO animar antes de validar el "shape" del video con Gemini
- NO loop con personajes haciendo gestos
- NO descubrir fallas en el render final — pre-render check obligatorio
═══════════════════════════════════════════════════════════════════
```

---

## 🔧 10. DEBUG / problema técnico específico

Usá este cuando algo falla y querés diagnóstico.

```
═══════════════════════════════════════════════════════════════════
Diagnóstico de problema: <DESCRIPCIÓN-CORTA>

Sintoma observado:
<lo-que-pasó>

ANTES:
1. Leé <repo-root>/.claude/skills/video-director/ANTI-PATTERNS.md
   (chequear si es un anti-pattern conocido)
2. Leé `<repo-root>/CLAUDE.md` § Mapa de docs autoritativos
   (chequear qué doc cubre el área del problema)
3. Leé la doc relevante del área

DESPUÉS:
- Identificá causa raíz (no asumir, diagnosticar con datos)
- Proponé fix concreto + cómo se evita en el futuro
- Si el aprendizaje es nuevo → proponé update de ANTI-PATTERNS.md
═══════════════════════════════════════════════════════════════════
```

---

## Cuándo usar cuál — tabla rápida

| Situación | Prompt # |
|---|---|
| Empiezo un video horror-choice nuevo | #1 |
| Empiezo un formato nuevo (no horror) | #2 |
| Tengo render con score <9.5, hay que iterar | #3 |
| Tengo script listo, falta generar assets | #4 |
| Tengo assets, falta armar el HTML | #5 |
| Acabo de renderizar, hay que QA | #6 |
| Publiqué hace 48h, hora de capturar métricas | #7 |
| Llegué a 10/20/30 videos publicados | #8 |
| Quiero delegar a otra sesión | #9 |
| Algo falla y no sé por qué | #10 |
| Quiero animar un video con Kling/Replicate | #11 |

---

## Tips para usar los prompts

1. **Copy-paste exacto**, no edites mucho. El sistema espera ciertos paths.
2. **Reemplazá `<placeholders>`** con valores reales antes de mandar.
3. **No omitas las lecturas obligatorias**. Si saco la línea "leé X.md", pierdo el contexto necesario.
4. **Esperá el plan antes de aprobar.** No digas "dale" sin leer lo que propongo.
5. **Si propongo algo que rompe las reglas** (ej: hardcodear countdown sin chequear video-log), corrégime.

---

## Mantenimiento

Cuando crees una nueva doc importante o agregues un workflow:
1. Agregar un prompt nuevo acá si vale la pena
2. Update la tabla de "cuándo usar cuál"
3. Mencionarlo en `CLAUDE.md` § Mapa de docs autoritativos

---

## Última actualización

2026-05-11. Inicial. 10 prompts copy-paste para los workflows críticos. Forzar lectura de docs ANTES de actuar = sistema funciona en sesiones largas sin perder coherencia.
