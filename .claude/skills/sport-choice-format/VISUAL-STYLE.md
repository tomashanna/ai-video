# VISUAL-STYLE.md — Estilo visual del formato sport-choice

> Firewall visual de género + preset CSS canónico, paleta y tipografía del formato.
> Solo contiene decisiones técnicas de look (no estrategia de cuenta).

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
| Countdown 3-2-1 | Anton | 400px | AVU universal (`assets/avu/`) |
| Marcador / minuto (opcional broadcast) | Bebas Neue / monospaced | 40-52px | Lower-third estilo broadcast (minuto, marcador) si aplica |
| Lower thirds | Variable según elemento (ver `templates/hyperframes/elements.json`) | Variable | – |

**Drop shadow obligatorio en todos los textos**: receta canónica universal en `ai-video-production/ELEMENTS-LIBRARY.md` § "Receta universal — Drop shadow para texto sobre IA-generated images" (4 strokes diagonales + drop shadow + glow envelope). **NO duplicar acá** — apuntar. (Hereda regla referent-validated: drop shadow > thick stroke.)

---
