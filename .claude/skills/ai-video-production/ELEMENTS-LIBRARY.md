# ELEMENTS-LIBRARY.md — Biblioteca híbrida de componentes UI

> Sistema híbrido: convención universal + implementaciones por estilo. Antes de hardcodear un countdown o loader en tu proyecto, **buscá en el catálogo**. Reutilizar componentes pre-renderizados = menos código, más consistencia, escala mejor.

---

## Filosofía híbrida

**Universal** (convención + JSON catálogo):
- Sistema de "elements" como concepto se aplica a CUALQUIER template
- `elements.json` en raíz cataloga todo
- Convenciones de naming, duración, aspect-ratio

**Por estilo** (implementaciones concretas):
- Cada estilo visual tiene su sub-biblioteca: `elements/horror-bw-crt/`, `elements/clean-modern/`, etc.
- Misma estructura: countdowns, loaders, lower-thirds
- Permite múltiples templates con identidades visuales distintas

---

## Estructura actual

```
AI video 1/
├── elements.json                ← Catálogo machine-readable (raíz)
├── countdown-pulse/             ← horror-bw-crt style
├── countdown-glitch/            ← horror-bw-crt style
├── countdown-slam/              ← horror-bw-crt style
├── loader-bar/                  ← horror-bw-crt style
├── loader-radial/               ← horror-bw-crt style
├── loader-segments/             ← horror-bw-crt style
├── lower-blackletter/           ← horror-bw-crt style
├── lower-typewriter/            ← horror-bw-crt style
├── lower-stamp/                 ← horror-bw-crt style
├── lower-handwritten/           ← horror-bw-crt style
└── lower-distressed/            ← horror-bw-crt style
```

**Estado actual**: todos los componentes son estilo `horror-bw-crt`. Cuando aparezca un template que requiera otro estilo, se creará una sub-biblioteca paralela.

**Próximo paso opcional**: reorganizar en `elements/horror-bw-crt/` para reflejar la sub-categorización por estilo. Por ahora flat OK porque solo hay un estilo.

---

## Catálogo actual — horror-bw-crt

### Countdowns

| ID | Path | Variant | Duración | Cuándo usar |
|---|---|---|---|---|
| `countdown-pulse` | `countdown-pulse/index.html` | SMPTE film-leader | 3.5s | Cuando querés look "cine clásico" |
| `countdown-glitch` | `countdown-glitch/index.html` | VHS static | 3.2s | Cuando querés look "VHS roto", más urgente |
| `countdown-slam` | `countdown-slam/index.html` | Impact | ~3s | Cuando querés impacto físico (slam down) |

**Para variedad entre videos**: pick random uno distinto al video anterior.

### Loaders

| ID | Path | Variant | Duración | Cuándo usar |
|---|---|---|---|---|
| `loader-bar` | `loader-bar/index.html` | Linear bar | 3.5s | Estándar, simple |
| `loader-radial` | `loader-radial/index.html` | Circle ring SVG | 3.5s | Cuando querés algo más circular/moderno |
| `loader-segments` | `loader-segments/index.html` | 12 segments | 3.5s | Cuando querés look "industrial" o tracking |

### Lower-thirds

| ID | Path | Variant | Font | Cuándo usar |
|---|---|---|---|---|
| `lower-blackletter` | `lower-blackletter/index.html` | Gothic medieval | UnifrakturMaguntia | Para introducir personajes/lugares dramáticos |
| `lower-typewriter` | `lower-typewriter/index.html` | Typewriter | Special Elite | Para "evidencia" / "investigación" |
| `lower-stamp` | `lower-stamp/index.html` | Impact stamp | Bebas Neue | Para reveals impactantes |
| `lower-handwritten` | `lower-handwritten/index.html` | Manuscript | Caveat | Para algo más personal/íntimo |
| `lower-distressed` | `lower-distressed/index.html` | Worn | (varía) | Para look "archivo viejo" |

---

## Cómo usar un elemento en tu proyecto

### Opción 1: Sub-composition via data-composition-src

```html
<div data-composition-src="countdown-pulse/index.html"
     data-start="11" 
     data-duration="3.5"
     data-track-index="50"></div>
```

HyperFrames carga el HTML standalone y lo monta dentro de tu composición principal.

### Opción 2: Copy del HTML + adaptar

Si necesitás modificar el countdown (cambiar números a "5-4-3-2-1" en lugar de "3-2-1"):

```bash
cp -r countdown-pulse my-project/countdown-custom
# Editar my-project/countdown-custom/index.html
```

---

## Selección random por video

Para variar la identidad visual entre videos del mismo formato:

```python
# Pseudocódigo
import random, json

elements = json.load(open('elements.json'))['elements']
countdowns = [e for e in elements if e['type'] == 'countdown']
loaders = [e for e in elements if e['type'] == 'loader']

# Excluir el del video anterior (chequear video-log.md)
last_countdown = "countdown-pulse"  # del video anterior
countdowns = [c for c in countdowns if c['id'] != last_countdown]

picked = random.choice(countdowns)
# Wire al index.html
```

---

## Cuándo crear estilo nuevo

Cuando aparezca un template que requiera identidad visual distinta:

### Ejemplo: si lanzás `cooking-format/` con cuenta IG cálida estilo "abuelita cocinando"

```
1. Crear: elements/clean-warm/
2. Generar versiones de countdowns/loaders/lower-thirds en ese estilo
3. Actualizar elements.json con sub-categoría:
   {
     "style_libraries": {
       "horror-bw-crt": { "elements": [...] },
       "clean-warm": { "elements": [...] }
     }
   }
4. cooking-format/PATTERNS.md referencia explícitamente "use elements/clean-warm/*"
```

---

## Sistema de tags en elements.json

`elements.json` tagga cada elemento para discovery. Útil para queries:

```python
# "Dame todos los countdowns horror"
countdowns_horror = [e for e in elements 
                     if 'countdown' in e['tags'] 
                     and 'horror' in e['tags']]
```

Tags actuales: `countdown`, `loader`, `lower-third`, `horror`, `bw`, `crt`, `glitch`, `vhs`, `flicker`, `medieval`, `typewriter`, `stamp`...

---

## Reglas de uso — CRÍTICAS

### Regla 1: Consistencia INTRA-video (no negociable)

**El countdown elegido se usa en TODOS los countdowns del video. El loader elegido se usa en TODOS los loaders del video.**

Si un video horror-choice tiene 3 countdowns (H2 + H3 + H4) y 3 loaders (H2 + H3 + H4):
- ✅ CORRECTO: countdown-glitch para H2, H3, H4 + loader-bar para H2, H3, H4
- ❌ MAL: countdown-glitch H2, countdown-slam H3, countdown-pulse H4

**Por qué**: el espectador interpreta el countdown como "símbolo del momento de elección". Si cambia entre dilemas, rompe la convención visual. Sentido: el formato te enseña su lenguaje y vos lo respetás durante el video.

### Regla 2: Compatibility check antes de wire (no negociable)

Antes de elegir `countdown + loader`, **verificar 3 dimensiones de compatibilidad**:

#### 2.1 — Timing (no se sobrelapen)

Patrón canónico horror-choice: `countdown 3s → flash → loader 2.5-3s → flash → resultado`.
**Son SECUENCIALES, NO simultáneos.**

| Elemento | Duración estándar |
|---|---|
| countdown-pulse | 3.5s |
| countdown-glitch | 3.2s |
| countdown-slam | 3.0s |
| loader-bar | 3.5s |
| loader-radial | 3.5s |
| loader-segments | 3.5s |

Verificar que `data-start` del loader = `data-start` del countdown + duración del countdown (sin overlap).

#### 2.2 — Posición (no choquen visualmente)

Patrón canónico:
- **Countdown**: top 50% (center vertical)
- **Loader**: bottom 700px (safe zone)

Si elegís un countdown que NO está center (algún variante futuro top-aligned) y un loader que sube por encima del bottom 700px → choque visual.

Por ahora todos los countdowns son center y todos los loaders son bottom-aligned → no hay choque entre los 11 actuales. Pero **verificar al agregar nuevos componentes**.

#### 2.3 — Estética (los estilos deben calzar)

Matriz de compatibilidad estética validada:

| Countdown ↓ / Loader → | `loader-bar` | `loader-radial` | `loader-segments` |
|---|---|---|---|
| `countdown-pulse` (SMPTE film) | ✅ Perfecto | ✅ Bueno | ⚠️ Choca (industrial vs film) |
| `countdown-glitch` (VHS) | ⚠️ Choca (VHS vs clean linear) | ✅ Bueno | ✅ Perfecto |
| `countdown-slam` (impact) | ✅ Bueno | ⚠️ Choca (impact vs ring smooth) | ✅ Perfecto |

**Combos top-tier (recomendados)**:
1. `pulse` + `bar` — clásico cine
2. `glitch` + `segments` — VHS industrial paranoia
3. `slam` + `segments` — impacto + tracking urgente

**Combos a evitar**:
- `pulse` + `segments` — film clásico vs industrial = identidad confusa
- `glitch` + `bar` — VHS roto vs linear limpio = identidad confusa
- `slam` + `radial` — impacto duro vs anillo smooth = identidad confusa

### Regla 3: Variedad ENTRE videos

Pickear distinto al video anterior. Doc: `<formato>/video-log.md`.

### Regla 4: No editar los originales

Si necesitás variación, copy + adapt en tu proyecto.

### Regla 5: Actualizar elements.json al agregar componente nuevo

Sin esto, el sistema no encuentra tu nuevo componente.

---

## Cuándo NO usar elements pre-renderizados

- Cuando el video requiere countdown/loader CON contenido específico (ej: countdown que dice "TIMER PARA DETONACIÓN" — no genérico)
- Cuando el estilo del template no coincide con ningún estilo de la biblioteca
- Cuando el video es tan corto que no compensa la overhead de sub-composition

En esos casos: hardcodear en `index.html` o crear sub-composition propia en `<proyecto>/compositions/`.

---

## Próximas acciones sugeridas

1. **Generar samples de cada elemento** — render de 3-5s para preview rápido sin abrir el HTML.
2. **Crear `elements/<estilo-nuevo>/`** cuando aparezca segundo template con identidad visual distinta.
3. **Considerar más variantes**: countdown-typed (números aparecen letra por letra), loader-skull (loader con esqueleto en horror), etc.
4. **Sistema de selección random** integrado en el video-director — pickeo automático al iniciar proyecto.

---

## ⭐ Receta universal — Drop shadow para texto sobre IA-generated images

**Scope**: 🌐 **Universal** — aplica a CUALQUIER video con texto overlay sobre imágenes generadas por IA, cualquier formato, cualquier duración.

### El problema

Imágenes generadas por IA tienen **iluminación impredecible** entre tomas. Un caption blanco que se ve perfectamente sobre una escena oscura se vuelve INVISIBLE sobre la siguiente escena con cielo claro o niebla blanca. Single text-shadow no alcanza.

Esto pasa en TODOS los formatos:
- Horror Reel (oscuridad → flash blanco)
- Tutorial corporate (slides oscuros → screenshots blancos)
- Documental (interior oscuro → exterior soleado)
- Testimonial (background varía por toma)

### La receta canónica

```css
.text-overlay-canonical {
  /* multi-direction stroke (8-way) */
  -webkit-text-stroke: 2px rgba(0,0,0,0.85);

  /* drop shadow combo — 4 strokes diagonales + glow + outer shadow */
  text-shadow:
    -3px -3px 0 rgba(0,0,0,1),     /* top-left stroke */
    3px -3px 0 rgba(0,0,0,1),      /* top-right stroke */
    -3px 3px 0 rgba(0,0,0,1),      /* bottom-left stroke */
    3px 3px 0 rgba(0,0,0,1),       /* bottom-right stroke */
    0 6px 16px rgba(0,0,0,1),      /* outer drop shadow */
    0 0 40px rgba(0,0,0,0.95);     /* outer glow envelope */
}
```

### Por qué funciona

| Layer | Función |
|---|---|
| `-webkit-text-stroke 2px black` | Outline básico que separa letra del fondo |
| 4 strokes diagonales ±3px | Refuerza el outline en TODAS las direcciones (cubre escena clara, oscura, mid-tone) |
| `0 6px 16px black` | Drop shadow que separa visualmente del background |
| `0 0 40px rgba(0,0,0,0.95)` | Glow envelope — oscurece sutilmente el área alrededor del texto |

Resultado: el texto queda con un "halo oscuro" pequeño que **funciona sobre cualquier fondo** (blanco, negro, mid-tone, niebla, fire).

### Validado en

- **mina-abandonada v15**: labels HUGO/SANTI legibles sobre dolly-mine (cielo nocturno claro arriba + entrada negra abajo). Sin esto, "SANTI" desaparecía sobre los troncos del fondo.
- **(esperar otros proyectos para validar en B2B / tutorial / etc.)**

### Casos de uso típicos

```css
/* Captions principales (font-size 80px) */
.caption {
  font-size: 80px;
  color: #ffffff;
  -webkit-text-stroke: 2px rgba(0,0,0,0.85);
  text-shadow:
    -3px -3px 0 rgba(0,0,0,1), 3px -3px 0 rgba(0,0,0,1),
    -3px 3px 0 rgba(0,0,0,1), 3px 3px 0 rgba(0,0,0,1),
    0 6px 16px rgba(0,0,0,1),
    0 0 40px rgba(0,0,0,0.95);
}

/* Labels de personajes (font-size 60-72px) */
.name-label {
  font-size: 72px;
  color: #ffffff;
  -webkit-text-stroke: 2.5px rgba(0,0,0,1);  /* más grueso por menor size */
  text-shadow: /* misma receta */;
}

/* Countdown / number callouts (font-size 200-400px) */
.countdown-num {
  font-size: 400px;
  color: #ffffff;
  -webkit-text-stroke: 4px rgba(0,0,0,0.6);  /* más grueso aún */
  text-shadow:
    0 4px 12px rgba(0,0,0,0.9),
    0 0 80px rgba(255,255,255,0.12);  /* glow blanco para impacto */
}
```

### Anti-patterns

❌ **Single `text-shadow: 2px 2px 4px black`** — funciona en fondos uniformes, FALLA en imágenes IA con luz variable.

❌ **Background rectangle (`background: rgba(0,0,0,0.7); padding: 8px`)** — funciona pero se ve "PowerPoint", no premium. Aceptable en B2B lower-thirds pero NO en captions principales.

❌ **Text-stroke sin drop shadow** — texto queda "plano", no se separa del background visualmente.

❌ **Solo glow (`text-shadow: 0 0 40px black`)** — borra los bordes de letra, se siente impreciso.

---

## Última actualización

2026-05-11. Agregada receta universal drop shadow text legibility (Scope: 🌐 Universal). Validado en mina-abandonada v15 (9.9/10 Gemini).

2026-05-10. Inicial. Documenta el sistema híbrido de componentes UI. 11 elementos catalogados (estilo horror-bw-crt).
