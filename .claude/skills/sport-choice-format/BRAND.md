# BRAND.md — Brand de la cuenta IG sport-choice (drama deportivo interactivo)

> Define audience, voz del contenido, paleta visual, hashtags y reglas operativas DE LA CUENTA específica del canal de Instagram sport-choice. Es el **firewall VISUAL del género**: garantiza que un video sport-choice salga **fútbol REAL broadcast** y NO horror disfrazado con un reskin de copy.
>
> ⚠️ **ESTE DOC HEREDA, NO DUPLICA.** El BRAND es la identidad VISUAL/de-cuenta sport. La MECÁNICA choice (estructura, invariante, counterfactual, cliffhanger) vive en `../choice-format-core/`. La técnica CSS universal (drop shadow, motion, mastering) vive en `ai-video-production/`. El género (BAN horror, REGLA DE AMBIENTE, SFX, LUTs) vive en las pautas sport. Este doc **apunta** a esas capas — no las re-litiga.
>
> **Estado**: v0 exploratorio + **PRE-EMPÍRICO**. Igual que el INGENIERO-PAUTA y la PAUTA-MASTER sport, sport-choice NO tiene render propio shippeado. Muchas decisiones (en especial el ⭐ preset CSS) son **propuestas razonadas a validar contra un render sport REAL** — NO medidas. Ver § 4 para el disclaimer explícito.

---

## 0. ⛔ EL FIREWALL DE GÉNERO (leer PRIMERO)

> Este BRAND existe porque el riesgo #1 del formato sport-choice es **salir horror disfrazado**: el template choice nació en horror, y horror tiene un look LÚGUBRE codificado a nivel CSS (`saturate(0.35) brightness(0.74)`). Si por inercia se hereda ese preset, un partido de fútbol se ve oscuro, desaturado y siniestro = horror con jugadores. Eso ES el bug que este doc previene.

### La regla del firewall (NO negociable)

🟦 **sport-choice = estadio BRILLANTE broadcast, cálido y saturado.** El look es el OPUESTO del lúgubre de horror.

🟥 **NUNCA aplicar el preset CSS de horror** (`contrast(1.28) saturate(0.35) brightness(0.74)`) ni ninguna variante desaturada/oscurecida a un `.scene-image` de sport. Si una imagen sport sale oscura/grisácea/siniestra → es un bug de género, reescribir.

🟥 **NUNCA color grade, SFX, música o paleta de horror** (cool_horror LUT, drones de terror, rojo-como-dread, vignette opresiva). El BAN completo de horror vive en `PAUTA-MASTER.md §0` — este BRAND es su contraparte VISUAL.

**Tabla del firewall (horror → sport, inversión 1:1):**

| Eje visual | horror-choice (lúgubre) | sport-choice (broadcast) |
|---|---|---|
| **Preset CSS base** | `saturate(0.35) brightness(0.74)` (desatura + oscurece) | `saturate(~1.20) brightness(~1.05)` (satura + ilumina) — § 4 |
| **Contraste** | `contrast(1.28)` (separar subjects oscuros) | `contrast(~1.10)` (broadcast limpio, NO crushed) |
| **Mood dominante** | lúgubre, frío, opresivo | brillante, vívido, eufórico/épico |
| **Color de tensión/dread** | rojo-como-amenaza | celeste/azul de estadio + dorado de gloria (rojo SOLO si es color de un equipo) |
| **LUT de error** | `cool_horror` (terror) | `cool_defeat` (gris-azul del fracaso DEPORTIVO, NO terror) |
| **Vignette** | opresiva fuerte | sutil / broadcast (no encierra; deja respirar el estadio) |
| **Géstalt** | "algo malo va a pasar" | "estoy en la final, las luces, el rugido" |

> Si en cualquier punto de la producción un frame sport evoca terror en vez de épica deportiva → está fuera de formato. Flaggear y reescribir, NO forzar.

---

## 1. Posicionamiento del canal

**Cuenta de Instagram con drama deportivo narrativo interactivo, formato "Elige a tu compañero" deportivo (variante sport del "Elige a tu compañero").**

- **Categoría**: Entertainment / Fútbol / Drama deportivo interactivo
- **Frecuencia target**: alta durante ventanas topical (Mundial / Champions) — 1 reel viral por partido marquee (ver `PAUTA-MASTER.md §1`: la máquina partido → reel). Fuera de ventana topical: 2-3 reels/semana.
- **Idioma**: Español neutro (tú/eliges/decides) — NUNCA voseo. (Hereda regla universal de cuenta.)
- **Duración por reel**: 86-100s (formato vertical 1080×1920)
- **Naturaleza topical**: el formato es una **máquina data-driven** atada a partidos reales (cracks marquee + favorito por cuotas). El timing importa: el reel sale mientras el partido es conversación.

---

## 2. Audience persona

| Atributo | Definición |
|---|---|
| **Edad** | 16-34 (predominante), fans de fútbol activos en social |
| **Comportamiento** | Scrollers de contenido futbolero, debaten jugadas, comparten memes de partidos, viven el topical (Mundial/Champions) |
| **Plataformas** | IG Reels principal, también TikTok (consumo cruzado), cross con Twitter/X futbolero |
| **Triggers emocionales** | Polémica de jugada ("¿la metía o no?"), tribalismo de equipo, FOMO del partido, gloria vs papelón, "¿qué hubieras hecho tú?" |
| **Behaviors clave** | Comentan su elección/bronca (A o B), taguean al amigo hincha rival, comparten el papelón/blooper, vuelven por el siguiente partido |
| **Referentes culturales** | Highlights broadcast (ESPN/DAZN), cuentas de memes de fútbol, FIFA/EAFC POV, debate de jugadas tipo "tú serías el 9" |

**Lo que les engancha**:
- Jugadas reales debatibles (duda genuina entre A y B)
- Tribalismo (eliges TU equipo, el rival es el obstáculo)
- El papelón/blooper compartible (≥1 por video — `PAUTA-MASTER.md §6`)
- La gloria épica: gol, copa, hinchada rugiendo, confeti
- Topical caliente: el partido del que todos hablan

**Lo que NO funciona**:
- Cualquier cosa que evoque horror/terror (es el firewall — § 0)
- Geografía confusa del partido (no se entiende dónde está el arco / quién es rival)
- Narración que editorializa ("ese jugador es malo") — el juicio lo pone el comentario del usuario (`PAUTA-MASTER.md §8`)
- Tutorial / educativo directo

---

## 3. Voz del contenido (la del relator/narrador)

> Esta es la voz dentro de los videos. Autoridad creativa completa → `PAUTA-MASTER.md §8` + `SCRIPT-WRITING-GUIDE.md`.

**Tono del relator**:
- **Play-by-play vivo, neutral de juicio** (relator deportivo que mete al viewer en la jugada) — NO el narrador frío omnisciente de horror.
- Habla en **segunda persona presente** ("eliges", "le das al desmarcado", "encaras al arquero").
- Oraciones cortas y claras. La épica emerge del **visual + rugido + música**, no de adjetivos en la narración.
- ✅ *"Uy… se la diste al lateral, enganchó y la perdió. Salen de contra. Gol."*
- 🟥 *"Ese jugador es malo, perdiste el partido."* (editorializar = prohibido)

**Voice ID canónico**: David C2 (mismo voice_id que usa el INGENIERO-PAUTA sport — narrador grave deportivo, español neutral). Ver `library/voices-catalog.json` + `INGENIERO-PAUTA-MASTER.md §4`.

**Vocabulario**:
- Léxico deportivo concreto (desmarcado, mano a mano, enganche, contra, achicar el ángulo, la clava)
- NUNCA léxico de horror (muerte, body horror, "te conviertes en…", monstruos)
- Presente del indicativo en consecuencias deportivas

Detalle completo en `SCRIPT-WRITING-GUIDE.md` + `PAUTA-MASTER.md §8`.

---

## 4. Visual identity (paleta + tipografía + filter)

### ⭐ Preset CSS filter canónico sport — "stadium-broadcast" (el FIREWALL VISUAL #1)

**Scope**: 🏟️ sport-choice format específicamente. Aplicar a TODOS los `.scene-image` del video EXCEPTO donde un LUT de sección override (ver abajo).

```css
.scene-image {
  /* sport-broadcast base — el OPUESTO del lúgubre de horror */
  filter: contrast(1.10) saturate(1.20) brightness(1.05);
}
```

> ⚠️⚠️ **DISCLAIMER EXPLÍCITO — ESTOS VALORES SON v0, NO MEDIDOS.**
>
> A diferencia de horror (`saturate(0.35) brightness(0.74)`, **validado empíricamente en mina-abandonada v15-final, 9.9/10 Gemini**), estos valores sport son **una PROPUESTA razonada por orden de magnitud, NO una medición**. sport-choice todavía NO tiene un render propio shippeado contra el cual calibrar.
>
> **Regla "medir, no estimar":** estos números **DEBEN validarse contra el primer render sport REAL** (igual que horror se midió vs mina v15) antes de tratarlos como canónicos. Hasta entonces son el punto de partida del firewall, no la verdad final. Logueá la calibración en `video-log.md` cuando el primer video sport se mida.

**Por qué estos valores (razonamiento, NO medición):**
- `contrast(1.10)`: leve realce broadcast para separar jugadores del césped/fondo SIN crushear sombras ni "quemar" reflectores. Horror sube a 1.28 para separar subjects oscuros; sport no necesita tanto porque el estadio ya está iluminado.
- `saturate(1.20)`: **inversión directa del 0.35 de horror** — satura para que los kits, el césped verde brillante y el dorado de gloria salgan vívidos como un broadcast real. Desaturar acá = matar el género.
- `brightness(1.05)`: **inversión del 0.74 de horror** — ilumina ligeramente para el look de estadio con reflectores. Un estadio oscuro se lee como horror.

**Orden de magnitud aceptable (banda a calibrar):** contrast ~1.05-1.15 · saturate ~1.15-1.30 · brightness ~1.0-1.10. Quedarse dentro de la banda hasta tener medición; salir de ella requiere justificación documentada.

**Meta-rule referencia**: `ai-video-production/PIPELINE.md §2` "Meta-regla universal: cada formato define su preset CSS filter canónico". sport define el suyo acá — y es el inverso del de horror.

### Los 3 LUTs sport (intent de color por sección)

> Reskin de los grades de horror. **NUNCA `cool_horror` ni LUT de terror.** Autoridad del intent → `INGENIERO-PAUTA-MASTER.md §4`; acá se da el CSS concreto v0 (también a validar contra render).

| LUT | Cuándo | Intent | CSS concreto (v0, a validar) |
|---|---|---|---|
| **`warm_glory`** | Gol propio / copa / vuelta olímpica / cliffhanger de gloria | Cálido dorado de celebración | `filter: contrast(1.08) saturate(1.30) brightness(1.10) sepia(0.12) hue-rotate(-6deg)` (empuja a dorado-cálido) |
| **`cool_cinematic_stadium`** | Juego en tensión / decisiones / mano a mano | Frío cinematográfico de broadcast (tensión, NO terror) | `filter: contrast(1.12) saturate(1.10) brightness(1.0) hue-rotate(4deg)` (leve frío de broadcast nocturno) |
| **`cool_defeat`** | Error / burla / papelón / la jugada se cae | Gris-azul del fracaso DEPORTIVO (el frío de perder, NO el de horror) | `filter: contrast(1.05) saturate(0.78) brightness(0.92) hue-rotate(8deg)` (desatura HACIA frío deportivo — todavía MÁS brillante/saturado que el horror-deep; nunca llega al lúgubre) |

> ⚠️ Clave del firewall: incluso `cool_defeat` (el más frío/desaturado de sport) **se queda lejos del lúgubre de horror** (`saturate 0.78` vs el `0.35` de horror; `brightness 0.92` vs `0.74`). El fracaso deportivo es frío-decepcionado, no terror. Si `cool_defeat` empieza a verse como horror → bajar la mano, es un overshoot.

### Paleta dominante

| Categoría | Color | Uso |
|---|---|---|
| Background / letterbox | `#0a0e12` (negro broadcast suave, NO `#000000` puro de horror) | Base / barras |
| Foreground texto | `#ffffff` con drop shadow (ver receta universal) | Captions principales |
| **Color de gloria** | `#f5c542` (dorado cálido) | Celebración, gol, copa, cliffhanger de gloria, CTA |
| **Verde césped** | `#2fa84a` (verde estadio vívido) | Acentos, lower-thirds de jugada |
| **Celeste estadio** | `#4db8e8` (frío broadcast) | Bridges de sección tensión, "SI HUBIERAS ELEGIDO…" |
| **Gris-azul derrota** | `#7b8a99` (frío desaturado) | Bridge/acento del recorrido que falla (cool_defeat) |
| **Colores de equipo** | dinámicos por video (el kit propio + el kit rival) | name labels, choice labels A/B, kits |

> 🟥 **El rojo NO es "dread"** como en horror. En sport el rojo es legítimo SOLO si es el color real de un equipo (p.ej. kit del Arsenal). NUNCA usar rojo como señal de amenaza/peligro genérico.

### Tipografía

| Uso | Font | Size | Notas |
|---|---|---|---|
| Captions principales | Anton / Bebas Neue | 80px (68px si frase >8 palabras) | Hereda fonts de horror, **tono sport** (deportivo broadcast, no siniestro) |
| Choice labels A/B (equipos) | Anton | 64px | Color = color del equipo correspondiente |
| **Name labels jugadores** (SAKA / DEMBÉLÉ) | Anton | **76px+ (GRANDES)** | ⭐ Los name labels son GRANDES — el viewer debe leer al instante quién es cada crack. Monospaced safe-zone Y11.5 (hereda `choice-format-core` UI safe zones) |
| Countdown 3-2-1 | Anton | 400px | AVU universal (`ai-video-production/templates/avu-library/`) |
| Marcador / minuto (opcional broadcast) | Bebas Neue / monospaced | 40-52px | Lower-third estilo broadcast (minuto, marcador) si aplica |
| Lower thirds | Variable según elemento (ver `elements.json`) | Variable | – |

**Drop shadow obligatorio en todos los textos**: receta canónica universal en `ai-video-production/ELEMENTS-LIBRARY.md` § "Receta universal — Drop shadow para texto sobre IA-generated images" (4 strokes diagonales + drop shadow + glow envelope). **NO duplicar acá** — apuntar. (Hereda regla referent-validated: drop shadow > thick stroke.)

---

## 5. Copy + hashtags

### Caption del post (template)

```
¿Elegiste al compañero correcto? ⚽

[Línea hook reformulando la decisión clave del partido — ej: "¿Le dabas a Saka o encarabas tú?"]

¿A o B? Comenta tu jugada 👇

#futbol #eligetucompanero #aivideo #champions #footballreels #soccer
```

### Hashtags fijos por video (5-10)

| Hashtag | Razón |
|---|---|
| `#futbol` / `#football` | Categoría primaria |
| `#eligetucompanero` | Tag de marca del formato (consistente entre videos) |
| `#aivideo` | Discovery por AI creators / curiosos |
| `#soccer` | Alcance internacional |
| `#footballreels` | IG-native football tag |
| `#golazo` | Cross-discovery con community futbolera |
| `#futbolenespañol` | Idioma + género |

### Hashtags variables (3-5 por video según contenido)

- Torneo/ventana topical: `#mundial`, `#worldcup`, `#champions`, `#championsleague`, `#copaamerica`, etc.
- Equipos del cruce: `#arsenal`, `#psg`, etc. (los 2 equipos del dyad)
- Jugadores marquee del dyad: handle/apellido si trending (cuidando no diluir el feed)
- Jugada-clave: `#penal`, `#manoamano`, `#golazo`, `#blooper` según corresponda

### CTA narrado final (texto de voz)

Template variable (CTA loop reconocible cross-video — `PAUTA-MASTER.md §11`):
> "Elige bien a tu compañero. Y vuelve mañana."

Variantes para evitar repetición:
- "¿A quién le dabas tú? Comenta A o B y por qué."
- "¿La metías o la fallabas? Comenta tu jugada abajo."
- "Tú eras el 9. ¿A o B? Te leo en los comentarios."

> Watermark `@elige_tucompanero` persistente en el render (hereda regla universal de cuenta — NUNCA `@referent-a`, que es REFERENCE de horror only).

---

## 6. Frequency floor + posting strategy

**Modo topical (Mundial/Champions)**: cadencia ALTA — 1 reel viral por partido marquee, montándose en la ola del partido. El timing es la ventaja competitiva (sacar el reel mientras el partido es conversación).
**Modo base (fuera de ventana topical)**: 2-3 reels/semana mínimo para mantener la cuenta viva en el algoritmo.

**Mejor horario** (estimado, ajustar con data real):
- **Inmediatamente post-partido** (la ventana caliente del topical es prioridad #1 sobre cualquier horario fijo)
- Fuera de topical: tardes/noches de días de fútbol (entre semana Champions, fines de semana liga)

**Rotación entre videos**: cada video DEBE rotar liga/equipos + jugada-clave del clímax + posición POV + modo de fracaso + política A/B (ver `PAUTA-MASTER.md §12` + `../choice-format-core/ROTATION-RULES.md` + `video-log.md`). Consultar `video-log.md` ANTES de diseñar.

---

## 7. Política de riesgo A/B (real-topical)

> Específica de sport (no aplica a horror). Autoridad completa → `PAUTA-MASTER.md §9`.

- **DEFAULT A**: la estrella nombrada queda en la GLORIA; el fallo cae en VOS (POV ficticio) o en un compañero genérico. Real + topical + seguro + escalable.
- 🟧 **B SELECTIVO (solo primeros videos, dosificado)**: la estrella nombrada puede fallar para boost de viralidad temprana. **Riesgo asumido conscientemente** (derechos de imagen + portrayal negativo + synthetic-media policy IG/TikTok) → declarado por video en el SPEC (`risk_policy: A|B`) + logueado en `video-log.md`. No es default; se apaga al escalar.

**Disclosure AI**: igual que horror, disclosure honesto de que es AI-generated (puede ser sutil en bio/highlight).

---

## 8. Reglas operativas

### Lo que SIEMPRE hacés en esta cuenta
- ✅ Aplicar el **preset sport-broadcast** (cálido/saturado/brillante) a los `.scene-image` — NUNCA el lúgubre de horror (§ 0 + § 4)
- ✅ Geografía de estadio clara en cada frame (**REGLA DE AMBIENTE** — `INGENIERO-PAUTA-MASTER.md §1`)
- ✅ Aplicar quality bar dual (Gemini ≥9.7 + audit-against-referent ≥85% — referente = bandas técnicas heredadas F1 hasta tener referentes sport propios)
- ✅ Rotar liga/equipos/jugada/política A/B (NO repetir cruce ni liga consecutiva)
- ✅ Name labels GRANDES de los 2 cracks (el viewer lee al instante quién es quién)
- ✅ Captions safe zone IG (hereda `choice-format-core`)
- ✅ Watermark `@elige_tucompanero` + disclosure honesto AI
- ✅ Capturar performance T+48h después de cada post

### Lo que NUNCA hacés en esta cuenta (el firewall, operativo)
- ❌ Aplicar el preset CSS lúgubre de horror (`saturate 0.35 / brightness 0.74`) ni ningún grade desaturado/oscurecido siniestro
- ❌ Usar `cool_horror` LUT, drones de terror, gritos/susurros de horror, o rojo-como-dread (§ 0 — el BAN completo en `PAUTA-MASTER.md §0`)
- ❌ Geografía de partido confusa (arco invisible, kits ambiguos, no se sabe quién es rival)
- ❌ Narración que editorializa el juicio ("ese jugador es malo") — el juicio lo pone el comentario del usuario
- ❌ Repetir cruce/liga/jugada-clave en videos consecutivos
- ❌ Comprar followers / engagement
- ❌ Esconder que es AI-generated
- ❌ Publicar contenido off-format (la cuenta es sport-choice 100%)
- ❌ Bajar quality bar por velocidad (ni siquiera en topical caliente)

---

## 9. Métricas de éxito de la cuenta

### Validación (primeros 3 meses)

| Métrica | Target |
|---|---|
| Followers | 1K en 3 meses (orgánico, boosteado por ventanas topical) |
| Avg views por reel | 5K (más en partido marquee caliente) |
| Avg completion rate | 60%+ |
| **Shares rate** | 6%+ de views (alto para sport — el papelón/polémica se comparte) |
| Engagement rate | 8%+ (likes + comments + saves + shares / views — el debate A/B mueve comentarios) |

### Escala (6-12 meses)

| Métrica | Target |
|---|---|
| Followers | 10K |
| Avg views | 25K+ (topical alto durante torneos) |
| Comentarios A/B por reel | 50+ (señal de polémica orgánica sana) |

> ⚠️ Métricas v0 estimadas. Recalibrar con data real de los primeros videos topical.

---

## 10. Decisiones diferidas

| Decisión | Status | Criterio para resolver |
|---|---|---|
| **Handle de la cuenta IG sport** | DIFERIDA | ¿cuenta propia separada de horror, o `@elige_tucompanero` compartido? Antes del primer post |
| **Foto de perfil + bio** | DIFERIDA | Antes del primer post |
| **⭐ Preset CSS sport calibrado** | DIFERIDA (v0 propuesto en § 4) | **Medir contra primer render sport REAL** + loguear en `video-log.md` (igual que horror se midió vs mina v15) |
| **Los 3 LUTs CSS concretos** | DIFERIDA (v0 propuesto en § 4) | Validar contra render sport real |
| **Política A/B de arranque** | DIFERIDA | Decidir cuántos videos iniciales corren modo B antes de apagarlo (`PAUTA-MASTER.md §9`) |
| **Cross-posting a TikTok** | DIFERIDA | Una vez IG validado, replicar TikTok como secondary |

---

## 11. Cómo usa este doc el video-director (ingeniero)

Cuando producís un video sport-choice para esta cuenta:

1. **Antes de generar cualquier `.scene-image`**: aplicar el preset sport-broadcast de § 4 (NUNCA el de horror). Chequear el firewall § 0.
2. Antes de generar prompts de imagen: cruzar con la **REGLA DE AMBIENTE** (`INGENIERO-PAUTA-MASTER.md §1`) — la geografía del partido manda.
3. Antes de escribir captions del post: usar template de § 5.
4. Antes de aplicar grades por sección: usar los 3 LUTs de § 4 (warm_glory / cool_cinematic_stadium / cool_defeat) — NUNCA cool_horror.
5. Antes de publicar: validar contra § 8 (lo que SÍ / NO se hace, incluido el firewall operativo).
6. Después de publicar: capturar performance per § 9 + **medir el grade real y calibrar el preset v0** + actualizar `video-log.md`.

---

## 12. Relación con otros documentos

| Capa | Doc | Qué aporta |
|---|---|---|
| **A.5 (mecánica agnóstica)** | `../choice-format-core/CHOICE-MECHANIC.md` + `INGENIERO-CHOICE-CORE.md` | La mecánica choice (hook dyad, countdown, loading, botones A/B, counterfactual, cliffhanger, UI safe zones, caption chunking) — el BRAND NO la duplica |
| **B (género — creativo)** | `PAUTA-MASTER.md` | Autoridad creativa sport: BAN horror (§0), elección=compañero, dos recorridos, narración-no-juzga, política A/B |
| **B (género — técnico)** | `INGENIERO-PAUTA-MASTER.md` | REGLA DE AMBIENTE, paleta SFX fútbol, LUTs intent, consistencia de kits/likeness |
| **A (técnica universal)** | `ai-video-production/` (PIPELINE, CAPTIONS, MOTION-LAYER, AUDIO-MASTERING, COLOR-GRADING, ELEMENTS-LIBRARY) | La técnica CSS universal (drop shadow, motion, mastering, color grading mecánica) — el BRAND **apunta, no duplica** |
| **Este doc (B — brand/visual)** | `BRAND.md` (sport) | Firewall VISUAL: preset CSS sport, paleta, tipografía, voz de cuenta, hashtags, reglas operativas de la cuenta IG sport |

---

## Última actualización

2026-06-01. Creación v0. Brand de la cuenta IG sport-choice como **firewall VISUAL del género** (espejo INVERSO de `horror-choice-format/BRAND.md`). Preset CSS sport-broadcast (cálido/saturado/brillante) + 3 LUTs sport + paleta + tipografía propuestos como **v0 razonado, NO medido** — a validar contra el primer render sport real (igual que horror se midió vs mina v15). Hereda mecánica de `choice-format-core`, técnica universal de `ai-video-production`, y género de las pautas sport.
