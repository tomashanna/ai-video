# VISUAL-STYLE.md — Estilo visual del formato horror-choice

> Preset CSS canónico, paleta y tipografía del formato. Extraído del antiguo brand doc;
> solo contiene decisiones técnicas de look (no estrategia de cuenta).

### ⭐ Preset CSS filter canónico — "horror-deep" (validado v15)

**Scope**: 🎬 horror-choice format específicamente. Aplicar a TODOS los `.scene-image` del video.

```css
.scene-image {
  filter: contrast(1.28) saturate(0.35) brightness(0.74);
}
```

Estos son los valores canónicos validados en mina-abandonada v15-final (9.9/10 Gemini). NO modificar sin justificación documentada.

**Por qué estos valores específicos**:
- `contrast(1.28)`: realza la separación entre subjects oscuros (Hugo) y backgrounds (tunnel) sin "quemar" highlights
- `saturate(0.35)`: desatura para look lúgubre + integra IA-images con paletas distintas (Hugo gaunt vs Santi clean blue)
- `brightness(0.74)`: oscurece para mood horror sin perder detalle en sombras

**Override por escena**:
- ✅ Cliffhanger H6 con clase `.h6-img`: `filter: none` para activar warm tint (rama cálida)
- ❌ NO override en H1-H5 sin razón narrativa clara

**Variante alternativa — "horror-claustrofóbico"**:
```css
.scene-image.deep-horror {
  filter: contrast(1.35) saturate(0.25) brightness(0.65);
}
```
Para sub-genre más oscuro / cuevas / espacios cerrados. NO probado todavía — usar con cuidado.

**Meta-rule referencia**: `ai-video-production/PIPELINE.md` § 2 "Meta-regla universal: cada formato define su preset CSS filter canónico"

### Paleta dominante

| Categoría | Color | Uso |
|---|---|---|
| Background | `#000000` puro / muy oscuro | Base |
| Foreground texto | `#ffffff` con stroke negro 2px | Captions principales |
| Color grade horror | filter horror-deep (ver arriba) | H1-H5 (rama horror) |
| Color grade cliffhanger | Cálido amarillo-naranja (warm-tint overlay) | H6 (rama "buena hipotética") |
| Acento cliffhanger | `#f0e040` (amarillo cálido) | CTA final, "¿qué hubieras elegido?" |
| Puente narrativo | `#f5d9a0` (dorado tenue) | "Y SI HUBIERAS ELEGIDO A..." |
| Bridge separador A→B | `#c8d8ff` (azul claro) | "SI [opción B]:" |

### Tipografía

| Uso | Font | Size | Stroke |
|---|---|---|---|
| Captions principales | Anton / Bebas Neue | 80px (68px si frase >8 palabras) | 2px |
| Choice labels A/B | Anton | 64px | 2px |
| Name labels HUGO/SANTI | Anton | 72px | 2.5px |
| Countdown | Anton | 400px | 4px |
| Caption Hugo whisper (italic) | Anton italic | 64px color #d8d8d8 | 1.5px |
| Lower thirds | Variable según elemento (ver templates/hyperframes/elements.json) | Variable | – |

**Drop shadow obligatorio en todos los textos**: ver receta canónica universal en `ai-video-production/ELEMENTS-LIBRARY.md` § "Receta universal — Drop shadow para texto sobre IA-generated images". 4 strokes diagonales + drop shadow + glow envelope.

---
