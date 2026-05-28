# aesthetic.md — Paleta dual + vignette + film grain + VFX transformations

> ⚠️ **DOC OPERACIONAL SECUNDARIO — NO ES AUTORIDAD CREATIVA.**
>
> La **autoridad creativa del formato horror-choice** vive en `horror-choice-format/PAUTA-MASTER.md` (8 videos virales canónicos).
>
> Este doc te ayuda a IMPLEMENTAR técnicamente lo que PAUTA-MASTER dicta. Si encontrás conflicto entre lo escrito acá y PAUTA-MASTER → **gana PAUTA-MASTER siempre**.
>
> Si llegaste a este doc sin leer PAUTA-MASTER primero, parar y leerla antes de seguir.

---


> El arquitecto define INTENT visual. El ingeniero implementa con CSS filters, LUTs, overlays. Esta es DIRECCIÓN ESTÉTICA, no técnica.

---

## La regla fundamental: PALETA DUAL PSICOLÓGICA

**13/13 referentes virales** usan paletas opuestas entre la rama del peligroso y la rama del seguro. No es un LUT por video — son DOS LUTs aplicados a escenas distintas dentro del MISMO video.

### Patrón validado

| Rama | Paleta típica | Mood |
|------|---------------|------|
| **Peligrosa (Bruno/Hugo/Axel/etc.)** | Cool / desaturada / podrida / sombras profundas | Amenaza, deterioro, peligro |
| **Segura (Pablo/Enzo/Mateo/etc.)** | Warm / cálida / dorada / acogedora | Alivio, calma, cozy |

### Variaciones por setting (catálogo aspirational)

| Setting | Peligrosa | Segura (counterfactual outro) |
|---------|-----------|-------------------------------|
| Mina | Grises + marrones + sombras negras + accent rojo (medidor, alarma) | Amanecer dorado + amber chimenea + verde naturaleza |
| Hotel | Verdes podridos + amarillos enfermizos + fluorescentes parpadeantes | Tonos cálidos hogareños + lámparas tungsten |
| Bosque | Azules oscuros + neblina gris + linterna fría | Naranjas de fogata + cielo amanecer |
| Carretera | Negro absoluto + faros amarillo punctual | Salón con chimenea + ámbar tungsten |
| Cockpit | Rojos+verdes paneles + azul oscuro exterior | Luz natural diurna + paisaje verde |
| Acuario | Azul cyan emisivo + sombras profundas | Cocina iluminada + café humeante |
| Industrial | Naranjas fuego + grises sucios + chispas | Oficina diurna ordinaria + luz natural |
| Tren | Sepias vintage + tonos fríos exteriores | (Generalmente outro es sepia recall de niñez/passado) |
| Pozo marino | Azul petróleo + gris granito + crushed blacks | (Counterfactual: superficie soleada) |
| Mall abandonado | Verdes podridos + plantas creciendo + decadencia | Parque acuático claro + agua tibia (ref-04 estilo) |

**Importante:** la paleta dual NO solo es estética — es PSICOLÓGICA. Comunica al viewer "esta opción es peligrosa, esa otra es segura" SIN palabras.

---

## Las 5 dimensiones de la dirección visual

### Dimensión 1 — Tone general (warm vs cool)
- **Warm** (rojos, naranjas, amarillos): cálido, hogareño, peligro orgánico (sangre), peligro fungal
- **Cool** (azules, cianes, verdes oscuros): clínico, distancia, alien, frío
- **Neutral desaturado** (grises, marrones): decadencia, abandono, polvo

### Dimensión 2 — Saturation
- **Oversaturated** (neones, primarios extremos): synthwave (ref-07), party (ref-13 EDM section)
- **Balanced**: realismo, found footage
- **Desaturated** (colores lavados): horror cinematográfico, post-apocalipsis

### Dimensión 3 — Contrast
- **High contrast** (sombras negras + luces brillantes): cinematográfico signature del formato
- **Crushed blacks** (negros aplastados): horror cinematográfico moderno
- **Medium contrast**: naturalistic
- **Low contrast**: nunca usar (look amateur)

### Dimensión 4 — Vignette
- **Pronunciada** (oscurece bordes claramente): claustrofobia + foco al centro
- **Moderada**: cinematográfico estándar
- **Sutil**: cuando el setting ya carga oscuridad
- **Nunca ausente** en este formato

### Dimensión 5 — Film grain / textura
- **Film grain visible** (8-12% típico): cinematográfico, dark academia, A24 horror
- **Clean digital**: liminal space (ref-05), backrooms
- **Bloom + glow** (en lugar de grain): synthwave, dreamcore (ref-07, ref-13)
- **Light leaks ocasionales**: transición orgánica

---

## Color isolation accent

**13 referentes lo usan.** Un color destaca DRAMÁTICAMENTE sobre la paleta dominante = guía la atención al peligro.

### Ejemplos validados

| Referente | Paleta dominante | Color accent | Para qué |
|-----------|------------------|---------------|----------|
| ref-03 mina | Grises + marrones | Rojo intenso | Medidor de gas + alarma + chispas taladro |
| ref-09 cockpit | Azul oscuro | Rojo paneles | Luces de advertencia |
| ref-08 acuario | Azul cyan | (no accent — la paleta YA contrasta dual) | - |
| ref-13 planta | Industrial gris | Azul Miro | El personaje místico destaca |
| ref-11 metro | Gris/naranja vagón | Verde+marrón Starbucks | El "símbolo de normalidad" en horror |

### Cuándo y cómo usar accent

- **1 accent color** por video (no más — confunde)
- Color de ALTA saturación sobre paleta desaturada
- Usado en OBJETOS críticos a la decisión (medidor, alarma, botón, dinamita)
- O usado en UN PERSONAJE para destacarlo (Miro azul sobre fábrica gris)
- Comunica: "esto importa"

---

## Lighting direction

(Heredado de `environments.md` — acá la dimensión estética específica)

### Hard light (sombras duras y definidas)
- Lámpara minera, faro de coche, foco fluorescente
- Crea sombras largas y dramáticas
- Mood: dramático, opresivo
- Usado en mayoría de scenes peligrosas

### Soft light (sombras difusas)
- Niebla difundiendo luz, lámpara con pantalla, dawn ambient
- Sombras suaves
- Mood: contemplativo, calmo
- Usado en counterfactual outros cozy

### Top-down dramatic
- Luz desde arriba (lámpara colgante, sol en horizonte)
- Crea sombras bajo cuencas oculares, barbillas
- Mood: criatura amenazante (acentúa rasgos uncanny)

### Sidelight (rim light)
- Luz lateral creando contorno luminoso
- Mood: mysterious, separating subject from background

### Backlit / silhouette
- Luz detrás del sujeto (figura recortada)
- Mood: misterio puro, identidad oculta

### Emissive lighting
- Luz emanada de objetos (paneles, neones, tanques acuario)
- Mood: tecnológico, mundo artificial

---

## VFX / transformaciones especiales (creativo, no técnico)

### Transformaciones de personaje (visuales narrativas)
Algunos videos usan transformaciones para reforzar pattern.
- **Cambio de color en personaje** (Miro: azul → verde paciencia → rojo ira en ref-13)
- **Aparición progresiva** (entidad alejándose se acerca lentamente en pasillo)
- **Desaparición / disolución** (personaje fade-out en momento dramático)
- **Distorsión facial** (uncanny extremo en climax)

### Efectos ambientales (atmósfera)
- **Niebla creciente** (build-up tensión)
- **Partículas de polvo en suspensión** (mina, edificio abandonado)
- **Chispas / fuegos artificiales orgánicos** (industrial, climax)
- **Luces parpadeantes** (fluorescentes, lámparas inestables)

### Glitches y morphings
- **Glitch effect** (cambio de estado de Miro)
- **Morph** (escena se transforma en otra sin cut físico)
- **Color shift abrupto** (drama tonal)

**Decisión creativa:** el arquitecto especifica QUÉ transformación. Ingeniero implementa con qué tool.

---

## Aesthetic por mood

### Uncanny puro (body horror)
- Cool desaturated dominante
- Vignette pronunciada
- Film grain visible 8-10%
- Hard light top-down
- Color accent rojo (peligro biológico)
- Crushed blacks profundos

### Surrealismo absurdo
- Variable según setting — más libertad cromática
- Pueden coexistir colores primarios (Bryan-capybara + neon party EDM)
- Vignette moderada
- Bloom OK en climax (no film grain necesariamente)

### Claustrofóbico liminal
- Warm sickly (amarillos enfermizos) o cool sterile
- Fluorescente parpadeante
- Vignette pronunciada
- Clean digital (sin grain) — backrooms aesthetic
- Color accent raro

### Cosmic horror megalofobia
- Cool desaturated extremo
- Crushed blacks máximos
- Film grain
- Wide composition (sujeto minúsculo vs escala)
- Mood: vacío, escala incomprensible

### Synthwave / dreamcore
- Oversaturated neones (cyan + magenta + crimson + verde ácido)
- Motion blur direccional
- Bloom + glow
- NO film grain
- Black crush extremo (ref-07 estilo)

---

## Counterfactual outro aesthetic

El outro DEBE contrastar tonalmente con el horror anterior. Esta es la catharsis visual.

### Cambios típicos en outro
- Cool → Warm (azules → naranjas/dorados)
- Desaturated → Saturated (colores vivos)
- Vignette pronunciada → vignette sutil o ausente
- Hard light → soft light (chimenea, dawn)
- Crushed blacks → balanced shadows
- Color accent dramático → ausencia de accent (todo cálido uniforme)
- Cuts rápidos → push-in lento contemplativo

**Validado:** los referentes top tienen este contraste MARCADO. Los mediocres mantienen mismo grading = score D4 cae.

---

## Output al SPEC

```yaml
aesthetic:
  general_visual_direction:
    tone: cool_desaturated_decadente
    saturation: desaturated_with_red_accent
    contrast: high_crushed_blacks
    vignette: pronunciada
    film_grain: visible_8_to_10_percent
    lighting_style: hard_light_top_down_lamparas_casco

  dual_palette:
    dangerous_route:
      dominant_colors: ["#3a2418 marrón mina", "#1a1a1a negro sombras", "#5a5045 gris polvo"]
      accent_color: "#cc0000 rojo medidor/alarma/chispas"
      mood: "amenazante, opresivo, claustrofóbico"
      lighting: "single source top-down (lámparas casco)"

    safe_route_outro:
      dominant_colors: ["#d4a056 ámbar tungsten chimenea", "#7a5a3a marrón cálido madera", "#3a4a6a azul cielo amanecer"]
      accent_color: "ninguno — todo cálido uniforme"
      mood: "cozy, hogareño, alivio"
      lighting: "soft light multiple sources (chimenea + lámpara + ventana al amanecer)"

  vfx_transformations:
    - description: "Bruno parpadea su ojo único cada 8-12s — único acto físico no humano"
      timing: "throughout"
      purpose: "mantener uncanny dread"
    - description: "Luz roja del medidor PULSA con sub-bass impact al aparecer"
      timing: "0:25 (decision point 1)"
      purpose: "audio-visual sync impact"
    - description: "Chispas del taladro como flashes blancos rápidos en clímax"
      timing: "1:15 (clímax)"
      purpose: "horror visceral visual"

  outro_aesthetic_shift:
    visual_change_description: |
      Cambio abrupto post-clímax:
      - Cool desaturated → warm saturated
      - Crushed blacks → balanced
      - Vignette pronunciada → sutil
      - Hard light → soft (chimenea + dawn)
      - El viewer SIENTE el alivio en la imagen
    audio_change_pointer: "ver audio-direction.md → cambio drone → folk acoustic"

  color_isolation_strategy:
    accent_color: "#cc0000 rojo"
    objects_with_accent:
      - "Medidor de gas (decision point 2)"
      - "Botón de alarma de emergencia (decision point 3)"
      - "Chispas del taladro (clímax)"
    purpose: "guiar atención del viewer a peligros específicos"
```

---

## Anti-patterns en aesthetic

❌ **UN LUT para todo el video** — pierde paleta dual psicológica, gap D4
❌ **Cool tones para horror narrativo** sin justificación — @referent-a usa WARM/EERIE para uncanny puro
❌ **Saturación alta general** — look "kids YouTube"
❌ **Sin vignette** — look TV vieja
❌ **Sin contrast** — look amateur documental
❌ **Color accent en cada objeto** — confunde, pierde fuerza
❌ **Outro con misma paleta que horror** — falta catharsis visual
❌ **Film grain en synthwave** — incoherente con aesthetic neon
❌ **Bloom en horror cinematográfico clásico** — incoherente

---

## Validación final de aesthetic

- [ ] ¿Paleta dual definida (peligrosa vs segura)?
- [ ] ¿Vignette especificada con intensidad?
- [ ] ¿Film grain o bloom según mood?
- [ ] ¿Lighting direction definida (no neutral plana)?
- [ ] ¿Color isolation accent identificado y limitado a objetos críticos?
- [ ] ¿Outro tiene shift visual marcado vs horror?
- [ ] ¿VFX transformations especificadas si pattern las requiere?

Si ❌ en cualquiera → ajustar antes de SPEC.
