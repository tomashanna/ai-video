# COLOR-GRADING.md — Two-LUT system (Narrative vs Choice/Liminal)

> Generado 2026-05-13 desde análisis de Gemini Vision sobre 35 keyframes + Gemini full-video sobre 7 referentes.
>
> **🎯 SCOPE:** Los 2 LUTs (LUT_NARRATIVE warm + LUT_CHOICE cool) son específicos de **F1 (Horror choice)**. Solo "vignette + crushed blacks + high contrast" son 🌐 universales. Ver `FORMAT-DETECTION.md` antes de aplicar. Otros formatos (F2 AI Mystery cool, F4 POV Synthwave oversaturated neon) tienen color grading OPUESTO.

## 🆕 Hallazgo crítico post Gemini full-video (2026-05-13 PM)

Gemini detectó que el color grading de F1 **NO es UN LUT por video**. Es **paleta dual psicológica** entre las dos opciones:
- **Opción peligrosa (Puerta 1, Bruno):** warm sickly amarillos/marrones podridos
- **Opción segura (Puerta 2, Pablo):** cool sterile / dorado nostalgia / azul-blanco

El **contraste psicológico** es lo que hace funcionar la narrativa visual. NO codificar UN LUT — codificar **dos LUTs opuestos** dentro del mismo video, uno por opción.

```css
/* Dentro del MISMO video horror-choice */
.option-dangerous {
  filter: contrast(1.18) saturate(0.80) sepia(0.12) hue-rotate(-15deg) brightness(0.92);
  /* warm sickly, podrido */
}
.option-safe {
  filter: contrast(1.15) saturate(0.95) brightness(1.05) hue-rotate(8deg);
  /* cool sterile / dorado nostalgia */
}
```

Esto sustituye mi codificación previa de "1 LUT por video". El LUT cambia escena a escena según la opción que se está mostrando.

---

## Decisión clave: NO hay UN color grade para horror

Los 7 referentes muestran **dos sistemas distintos de color grading**, no uno. La elección depende del **pattern narrativo**, no del genre.

| Sub-genre | Pattern típico | Color grade |
|-----------|----------------|-------------|
| Horror **narrativo** (mina, bosque, carretera) | Choice character-driven con archetypes humanos/criaturas | **LUT_NARRATIVE — warm/eerie** |
| Horror **choice puertas** (backrooms, doors) | Liminal space binary choice | **LUT_CHOICE — cool/cinematic** |
| Found footage natural | Visualización fenómeno extraño | LUT_NARRATIVE variante desaturada |

**Evidence:** ref-03/ref-06 (narrativo @referent-a) usan warm/eerie con crushed blacks. ref-04/ref-05 (puertas @referent-a) usan cool/cinematic con tintes verdosos.

---

## LUT_NARRATIVE — warm/eerie

**Para:** horror choice narrativo con archetypes humanos/criaturas (mina, bosque, carretera nocturna).

### Look target
- Tono general: warm con ocres/marrones/sienas
- Sombras: crushed blacks profundos (#000-#0A0A0A)
- Contraste: alto (acentúa cuencas oculares, barbillas)
- Saturación: desaturada general, con un acento de color (rojo sangre, naranja fuego, amarillo lámpara) que cuts through
- Vignette: 0.4-0.5 strength, soft falloff
- Film grain: 8-12% intensity (cinematic/dark academia)
- Iluminación target: top-down dramatic (lámpara desde arriba)

### CSS implementation

```css
.scene-narrative {
  filter:
    contrast(1.15)
    saturate(0.85)
    brightness(0.95)
    sepia(0.08)
    hue-rotate(-10deg);
}
```

### Vignette overlay (universal)

```html
<div id="vignette-overlay"></div>

<style>
#vignette-overlay {
  position: fixed;
  inset: 0;
  pointer-events: none;
  z-index: 90;
  box-shadow:
    inset 0 0 100px rgba(0,0,0,0.3),
    inset 0 0 250px rgba(0,0,0,0.5);
  background: radial-gradient(
    ellipse at center,
    transparent 40%,
    rgba(0,0,0,0.3) 80%,
    rgba(0,0,0,0.5) 100%
  );
}
</style>
```

### Film grain overlay (universal para narrative)

```html
<div id="grain-overlay"></div>

<style>
#grain-overlay {
  position: fixed;
  inset: 0;
  pointer-events: none;
  z-index: 91;
  opacity: 0.12;
  mix-blend-mode: overlay;
  background-image: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" width="200" height="200"><filter id="noise"><feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" stitchTiles="stitch"/></filter><rect width="100%" height="100%" filter="url(%23noise)"/></svg>');
  animation: grain 0.25s steps(1) infinite;
}

@keyframes grain {
  0%   { transform: translate(0, 0); }
  25%  { transform: translate(-3px, 2px); }
  50%  { transform: translate(3px, -2px); }
  75%  { transform: translate(-2px, -3px); }
  100% { transform: translate(2px, 3px); }
}
</style>
```

### Color balance fino (Gemini Vision target)

| Tonal range | Shift |
|-------------|-------|
| Shadows | +5 R, -5 B (warm shadows) |
| Midtones | +3 R, +2 G (sienna midtones) |
| Highlights | -2 R, +5 B (cool highlights for contrast) |

Aplicable via SVG filter chain o post-process en ffmpeg:
```bash
ffmpeg -i input.mp4 -vf "curves=preset=increase_contrast,colorbalance=rs=0.05:bs=-0.05:gm=0.02" output.mp4
```

---

## LUT_CHOICE — cool/cinematic (Liminal space)

**Para:** horror choice de puertas/binary visual decisions (backrooms, doors, "elige una puerta").

### Look target
- Tono general: cool con tintes verdosos/cian
- Contraste complementario: rojo + azul agresivo (puerta A vs puerta B)
- Saturación: media-alta en primarios, desaturada en neutros
- Vignette: 0.5 strength (más pronunciada que narrative)
- Film grain: 0% (ref-05) o 5% gritty (ref-04)
- Filter look: clean digital (Liminal Space) o cinematic gritty
- Iluminación target: top-down centered light (lámpara plafón)

### CSS implementation

```css
.scene-choice {
  filter:
    contrast(1.20)
    saturate(0.95)
    brightness(1.0)
    hue-rotate(5deg);
}

/* Variante con tinte verdoso explícito */
.scene-choice-greenish {
  filter:
    contrast(1.20)
    saturate(0.90)
    hue-rotate(8deg);
}
```

### Vignette más pronunciada

```css
#vignette-overlay.choice-variant {
  box-shadow:
    inset 0 0 80px rgba(0,0,0,0.4),
    inset 0 0 220px rgba(0,0,0,0.7);
}
```

### Sin film grain (Liminal Space)

Para ref-05 style (puerta roja vs puerta azul), NO usar film grain. El look es **clean digital**, casi surrealista. El grain rompe la sensación de "espacio fabricado".

---

## Cuándo aplicar cada LUT (decision tree)

```
¿El video es horror choice?
├── Sí
│   ├── ¿Archetypes humanos/criaturas con nombres? (Bruno/Pablo, Axel/Enzo)
│   │   └── LUT_NARRATIVE (warm/eerie)
│   └── ¿Binary visual choice (2 puertas, 2 caminos, 2 objetos)?
│       └── LUT_CHOICE (cool/cinematic)
└── No
    └── LUT_NARRATIVE variante (warm/eerie default)
```

---

## Universal rules (independent of LUT)

### Crushed blacks — siempre

```css
.scene-any {
  filter: brightness(1.0) contrast(1.15);
  /* Implícito: las sombras se aplastan via contrast */
}
```

Para crushed más explícito:
```css
.scene-any {
  filter: brightness(0.95) contrast(1.2);
}
```

### Vignette — siempre (cualquier LUT)

7/7 referentes lo usan. Es **obligatorio** en pre-render-gate Q19.

### High contrast — siempre

7/7 referentes. Bajo contraste = look amateur/document. Alto contraste = cinematic.

---

## Anti-patterns

❌ **Aplicar cool/blue grade a horror narrativo:** look "icy" frío, mata la sensación eerie/uncanny. @referent-a NUNCA hace esto en narrativo.

❌ **Saturación alta general:** look "vibrante" → contradice horror. La saturación selectiva (un color cuts through) es OK; saturación global NO.

❌ **Sin vignette:** rompe el "feel" cinematic. Aún en LUT clean digital de ref-05 hay vignette moderada.

❌ **Film grain >20%:** look "TV old" exagerado. Sweet spot 8-12%.

❌ **LUT estática durante todo el video:** considera shift sutil de LUT en climax (e.g., más contraste, más crush) para enfatizar.

---

## Validación con Gemini Vision

Cada render debe pasar Gemini Vision check:

```python
# Prompt fragment for Gemini QA on color grading
COLOR_QA_PROMPT = """
Evaluá el color grading del frame:
1. ¿Vignette visible y moderada-pronunciada? Y/N
2. ¿Crushed blacks (sombras profundas <#0A0A0A)? Y/N
3. ¿High contrast (relación sombras-luces marcada)? Y/N
4. ¿Coherente con LUT declarado? (NARRATIVE warm/eerie vs CHOICE cool/cinematic)
5. ¿Film grain presente si es NARRATIVE? Y/N
"""
```

---

## Integración con pre-render-gate

**Q19. ¿Vignette aplicado en composición?** (Universal en 7/7 referentes)
```bash
# Check que index.html tiene #vignette-overlay
grep -q "vignette-overlay" index.html && echo "✓" || echo "✗"
```

**Q19.5. ¿LUT correcto aplicado según pattern?**
- Pattern narrative → `scene-narrative` class en escenas
- Pattern choice puertas → `scene-choice` class en escenas

---

## Casos disparadores

- **pueblo-fantasma-desierto v2:** color grading inconsistente entre escenas, sin LUT declarado. El usuario percibió "color inconsistente" en review humano. Codificar 2 LUTs hace el output reproducible.
- **mina-abandonada v15:** funcionó con un look warm/eerie por accidente (Nano Banana generó imágenes con esa paleta). Codificar el LUT hace replicable.

---

## Pendiente investigar (Sesión 2)

- LUT dinámico que shift sutilmente durante decision points (más contraste, más crush)
- Color grade reactivo a audio (volumen narración → contrast lift)
- LUT específico para climax/resolution
