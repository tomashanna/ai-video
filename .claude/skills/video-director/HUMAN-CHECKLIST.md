# HUMAN-CHECKLIST.md — Gate humano post-Gemini

> Gemini Video Analyzer ≥9.7 es necesario pero NO suficiente. Hay un 5-10% de issues que Gemini no flagea pero el ojo humano sí. Este checklist captura ese gap.

---

## Por qué existe este checklist

**Evidencia:** mina-abandonada v7c sacó **9.5/10 Gemini**. El video tenía un flash de imagen <1s claramente visible al ojo humano (h4-pull a 0.15s entre fade-ins del black overlay). Gemini no lo flageó. El usuario sí.

Gemini puede ser permisivo con:
- Flashes <1s
- Continuidad sutil entre captions y visuales (caption hablando de rama A mientras imagen es de rama B)
- Pacing emotivo (un beat puede sentirse rápido al ojo humano pero Gemini lo aprueba)
- Asset orfan que se ve por error
- Sincronización fina audio-visual (un thud llegando 0.2s tarde)

Por eso: **después de Gemini ≥9.7, correr este checklist en 2 minutos** antes de declarar "listo para publicar".

---

## El checklist — 7 preguntas, sí/no, ~2 min

Mirá el video UNA VEZ de principio a fin, con auriculares. Marcá sí/no en cada uno:

### 1. ¿Aparece alguna imagen menos que parpadear?
Específicamente: alguna imagen que aparezca <1 segundo. Si la sentís como "flash que pasó y no entendí qué fue" — es un anti-pattern (ver `ANTI-PATTERNS.md` § Imágenes <1s). El audit script (`ai-video audit-narrative`) debería haberlo agarrado, pero el ojo humano detecta los casos sutiles.

**Si "sí" → identificá el timestamp y el id del `<img>`. Removelo del GSAP o extendé su duración.**

### 2. ¿Algún caption aparece "antes" o "después" de su imagen correspondiente?
Específicamente: ¿el caption habla de algo que la imagen activa contradice o aún no muestra?

Caso real: mina-abandonada v7 first iteration tuvo "CAES AL POZO" mostrándose sobre la imagen del pillar (rama buena), porque el black overlay desapareció antes que el caption cambiara.

**Si "sí" → el timing del black overlay / GSAP no está alineado con el caption-spec.json (Whisper). Re-alinear.**

### 3. ¿Algún momento donde el espectador se queda esperando >3s sin caption ni audio nuevo?
Específicamente: pantalla negra o imagen estática + silencio prolongado + nada nuevo pasando. El espectador scrollea.

**Si "sí" → o acortás el negro, o agregás un drone/SFX sostenido, o cambiás la imagen, o entra un caption.**

### 4. ¿La transición al cliffhanger se "anuncia" antes de que ocurra?
Específicamente: ¿hay un puente narrativo ("Y si hubieras elegido a...") que prepara al espectador antes del flash visual de transición?

**Si "no" → la transición se siente como glitch. Agregar el bridge caption inmediatamente antes del flash (V7-4 rule).**

### 5. ¿La música del cliffhanger se siente como un cambio real de mundo?
Específicamente: ¿el contraste de música (horror dark → warm calm) es notable, o pasa desapercibido?

**Si "no" → el cliffhanger pierde su impacto. Subir volumen de la música cálida, o agregar warm-whoosh SFX en la transición.**

### 6. ¿El CTA narrado al final invita a comentar específicamente?
Específicamente: ¿se escucha al narrador pidiendo "comentá A o B y por qué"? No solo texto en pantalla.

**Si "no" → falta CTA con voz (V7-5 rule). Generar TTS del CTA y wirearlo en los últimos 2.4s.**

### 7. ¿El último frame deja al espectador con curiosidad o queda en plano?
Específicamente: ¿el final genera "want to rewatch" o se siente como "ok, terminó"?

**Si "no genera curiosidad" → considerar:**
- Subir el contraste tonal del cliffhanger
- Agregar un caption sutil al final tipo "¿Qué habrías elegido?"
- Verificar que el cliffhanger NO resuelve la duda — la deja abierta

---

## Cómo reportar findings del checklist

Después de mirar el video, escribir al usuario en formato tabla:

```markdown
| # | Check | Resultado | Acción |
|---|-------|-----------|--------|
| 1 | Imagen <1s | ✓ Limpio | — |
| 2 | Caption-imagen sync | ✗ "CAES AL POZO" sobre pillar a 70.5s | Re-render con black hasta 71.9s |
| 3 | Espera >3s | ✓ Limpio | — |
| 4 | Bridge antes de cliffhanger | ✓ Limpio | — |
| 5 | Cambio de música mundo | ✓ Limpio | — |
| 6 | CTA narrado | ✗ Solo texto, no voz | Generar TTS, wire en últimos 2.4s |
| 7 | Curiosidad final | ✓ Limpio | — |
```

Si hay ≥1 ✗ → no se publica, se itera. Cada ✗ es un fix concreto.

---

## Cuándo NO correr este checklist

- Cuando Gemini dio <9.5 → primero llegar a Gemini 9.5, recién después human checklist.
- Cuando el render es un draft de prueba (no para publicar) → no gastar tiempo.
- Cuando es un re-render de un fix puntual que ya validaste antes → solo re-checkear el item que tocaste.

---

## Cuándo evolucionar este checklist

Cada vez que un bug llega a producción que ninguno de estos 7 checks hubiera atrapado → **agregar el check #8**. La lista crece solo con evidencia, no con teoría.

**Histórico de evolución:**
- 2026-05-10: creado con 7 checks basados en mina-abandonada v6→v7d session.

---

## Relación con otros gates

```
Gemini QA (≥9.7)  →  ai-video audit-narrative (0 errors)  →  HUMAN CHECKLIST (este)  →  PUBLICAR
   automático         automático                         humano (~2 min)
```

Los 3 son obligatorios. Cada uno cubre lo que los otros no.
