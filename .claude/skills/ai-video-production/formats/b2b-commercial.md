# formats/b2b-commercial.md — B2B Commercial / Sales / LinkedIn

> Delivery format profesional/corporativo. Reglas distintas a contenido viral. Métricas distintas (conversión, no views).

---

## Specs técnicos

| Atributo | Valor |
|---|---|
| Aspect ratio | 16:9 (default) o 1:1 (LinkedIn feed nativo) o 9:16 (LinkedIn Stories) |
| Resolución | 1920×1080 (16:9), 1080×1080 (1:1), 1080×1920 (9:16) |
| FPS | 30 (default), 24 si tono cinematic |
| Codec video | H.264 High profile, yuv420p |
| Codec audio | AAC-LC stereo, 48000Hz |
| Bitrate video | 6-10 Mbps (target premium look, no compresión visible) |
| Duración | 30s-2min (sweet spot 45-90s) |
| Tamaño máx | <100 MB (algunos clientes/CRMs limitan a 50 MB) |
| Container | MP4 |

---

## Reglas heredadas

### 🌐 Universal (TODAS aplican)
- `CAPTIONS.md` § Whisper-sync — **CRÍTICO** en B2B (LinkedIn autoplay muted por default; 80%+ ve sin audio)
- `ELEMENTS-LIBRARY.md` § Drop shadow
- `PIPELINE.md` § Preset filter — preset distinto (corporativo limpio)
- `CHARACTER-CONSISTENCY.md` — si hay portavoces recurrentes

### 📱 Vertical short-form — **HEREDAR SELECTIVAMENTE**
- ✅ Hook en primeros 3-5s (LinkedIn scroll rápido)
- ❌ "Cero estáticas primeros 30s" — B2B puede usar still corporate shots
- ❌ UI safe zones IG/TikTok — LinkedIn tiene UI distinta

### 🏢 B2B / Corporativo (todas aplican — ver "Específico B2B")

### 🎬 Format-specific
Ver sección abajo.

---

## Específico B2B Commercial

### Tono y look
**Scope**: 🏢 B2B

| Aspecto | Valor B2B |
|---|---|
| Color grade | Naturalista, contrast 1.05-1.10, saturate 0.90-1.0, brightness 1.0-1.05 |
| Música | Corporate uplifting, motivational, **NO horror/comedy**. Volumen 0.10-0.15 |
| Voz | Profesional, clara, **idealmente humano real** (no AI TTS si presupuesto permite) |
| Captions | Inglés/español formal — NO slang, NO mayúsculas dramáticas innecesarias |
| Movimiento de cámara | Estable, deliberado. NO shaky cam, NO whip pans |
| Logos | Logo del cliente visible en al menos 1 momento (intro o outro) |

### Estructura típica (45-90s)

```
0-5s    HOOK / PAIN POINT             ("¿Tu equipo pierde 10h/semana en X?")
5-15s   PROBLEM AGITATION             (consecuencias del pain point)
15-30s  SOLUTION INTRO                (qué hace tu producto/servicio)
30-50s  VALUE DEMO                    (cómo funciona, capturas reales)
50-70s  PROOF / SOCIAL                (logos clientes, métricas, testimonial)
70-85s  CTA                           ("Agenda demo", "Descarga whitepaper")
85-90s  BRANDING WRAP                 (logo + URL)
```

### Lower-third para B2B
**Scope**: 🏢

Lower-third con nombre + título es **estándar** en testimoniales B2B:

```css
.lower-third {
  position: absolute;
  bottom: 80px;
  left: 60px;
  background: rgba(0,0,0,0.7);
  padding: 12px 24px;
  border-left: 4px solid #brand-color;
  font-family: corporate-sans;
}
.lower-third .name { font-size: 28px; color: #fff; }
.lower-third .title { font-size: 20px; color: #ccc; }
```

Aparece 2-3s después de que la persona empieza a hablar, queda 5-7s visible, fade out.

### Captions B2B: específicas

**Scope**: 🏢

- **Color**: Blanco o brand color. NUNCA amarillo neon o colors de horror.
- **Stroke**: Mantener stroke para legibilidad, pero menos agresivo (1px vs 2-3px en horror)
- **Font**: Sans-serif corporativo (Inter, Roboto, Helvetica Neue). NO Anton, NO Impact (demasiado clickbait).
- **Tamaño**: 48-64px (más conservador que Reel)
- **Posición**: Bottom 100-150px desde el borde (no zona action del feed)

### Branding obligatorio

**Scope**: 🏢

Cada B2B video DEBE incluir:
- Logo cliente en intro (primeros 5s) O outro (últimos 5s)
- URL / handle en outro
- Brand colors en CTA buttons
- Música licensed (verificar rights antes de render)

### Conversión > engagement

**Scope**: 🏢

A diferencia de Reels donde la métrica es views/likes/comments, B2B mide:
- Click-through al CTA (URL en descripción o link sticker)
- Demo bookings via UTM tracking
- Engagement con account-based marketing

Diseñar el CTA para ser **claro y único**:
- ✅ "Agenda demo gratis" (acción específica)
- ✅ "Descarga el whitepaper" (acción específica)
- ❌ "Saber más" (vago, baja conversión)
- ❌ "Suscríbete" (no aplica a B2B)

---

## UI Safe Zones — LinkedIn (1:1 feed nativo)

```css
/* Para video 1080×1080 en LinkedIn feed */
.lower-third {
  bottom: 80px;    /* arriba de reactions bar */
  left: 60px;
}
.top-overlay {
  top: 60px;       /* debajo de header del autor */
  left: 60px;
}
```

**Zonas a evitar en LinkedIn feed**:
- `bottom: 0-60px` → reactions bar (like, comment, share)
- `top: 0-50px` → header del autor del post

## UI Safe Zones — LinkedIn Story (9:16)

```css
/* Para video 1080×1920 en LinkedIn Stories */
.story-overlay {
  bottom: 400px;   /* arriba de tap zone para forward */
  top: 200px;      /* debajo de profile chip */
}
```

---

## Anti-patterns específicos B2B

### ❌ Tono comedy / casual

**Por qué falla**: contexto profesional. Tono debe ser confiable, no entretenido per se.

**Fix**: profesional pero accesible. Humor sutil OK, pero el video no es para entretener.

### ❌ Captions estilo TikTok (mayúsculas dramáticas, colors neon)

**Por qué falla**: rompe el branding corporativo. Cliente lo va a rechazar.

**Fix**: captions sans-serif corporate, color blanco/brand. Stroke sutil.

### ❌ Render vertical 9:16 sin tener LinkedIn Stories como destino

**Por qué falla**: el feed nativo de LinkedIn es 1:1 o 16:9. 9:16 se ve raro letterboxed.

**Fix**: confirmar destination antes de elegir aspect. Default = 1:1 o 16:9.

### ❌ Música sin verificar licensing

**Por qué falla**: B2B clients tienen compliance. Música no licensed = problema legal.

**Fix**: usar Epidemic Sound, Artlist, o música licensed específica. Documentar la licencia.

### ❌ CTA múltiples / ambiguos

**Por qué falla**: cognitive load. Viewer hace 0 acciones.

**Fix**: 1 CTA único y específico. Repetirlo si es necesario, pero el mismo.

---

## QA específico B2B Commercial

```
Dimensiones específicas B2B:
- ¿El hook en primeros 5s comunica el pain point claramente?
- ¿La narrativa se entiende SIN AUDIO (LinkedIn autoplay muted)?
- ¿Las captions son legibles y professional-looking (no estilo clickbait)?
- ¿Logo del cliente visible al menos 1 vez?
- ¿El CTA es claro, específico y único?
- ¿La música está licensed?
- ¿Tono es professional (no comedy/casual)?
- ¿Color grade es naturalista (no horror filter)?
- ¿Aspect ratio matchea destination (1:1 LinkedIn feed, 16:9 web, 9:16 LinkedIn Story)?
```

---

## Casos producidos

(ninguno aún)

---

## Cross-references

- `DELIVERY-FORMATS.md` — catálogo padre
- `formats/youtube-long.md` — formato hermano horizontal (más narrativo, menos transaccional)
- `formats/instagram-story.md` — para B2B Stories
