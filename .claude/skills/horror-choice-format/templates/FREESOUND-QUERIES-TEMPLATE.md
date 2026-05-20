# FREESOUND-QUERIES.md — [NOMBRE_PROYECTO]

> ⚠️ **TEMPLATE OPCIONAL — NO parte del workflow estándar.**
>
> **Default actualizado 2026-05-10: ElevenLabs cubre todos los casos del workflow estándar** (incluyendo loops largos vía `loop:true` + ffmpeg `stream_loop` expansion, instrumentos acústicos y voces humanas). Validado en bosque-abandonado v3.
>
> Solo copiar este template al proyecto si **un asset puntual de EL salió notoriamente uncanny** y no se arregla iterando el prompt. En ese caso, descargar el reemplazo de Freesound para ESE asset específico, dejar el resto en EL.

Lista de SFX que históricamente iban a Freesound (loops largos >22s, instrumentos acústicos reales, voces humanas naturales). Mantener este template como referencia del fallback.

**Base URL:** https://freesound.org/search/

**Cómo descargar:**
1. Crear cuenta gratis (solo para descargar).
2. Click en URL de cada query → escuchar 3-5 candidatos → elegir el mejor.
3. "Download" → guardar en `assets/sfx/` con el nombre indicado.
4. **Verificar licencia**: CC0 (sin atribución) o CC-BY (atribución requerida → `CREDITS.md`).
5. Si es WAV, convertir:
   ```bash
   ffmpeg -i tu_descarga.wav -ar 44100 -ac 2 assets/sfx/nombre-final.mp3 -y
   ```

---

## 1. `assets/sfx/ambient-forest-wind.mp3`

**Función:** capa atmosférica continua bajo toda la sección de horror (H1–H5).
**URL:** https://freesound.org/search/?q=forest+night+wind+ambience&f=duration%3A%5B60+TO+300%5D
**Criterio:** ≥60s, sin pájaros nocturnos identificables, sin lluvia, tono frío, sin loops obvios.
**Fallback recorte:**
```bash
ffmpeg -i wind-source.wav -ss 30 -t 75 -ar 44100 assets/sfx/ambient-forest-wind.mp3 -y
```

---

## 2. `assets/sfx/ambient-dawn-warmth.mp3`

**Función:** capa atmosférica del cliffhanger cálido (H6).
**URL:** https://freesound.org/search/?q=dawn+forest+birds+warm+ambience&f=duration%3A%5B10+TO+60%5D
**Criterio:** 12-20s utilizables, pájaros suaves no estridentes, sin viento fuerte, cálido.

---

## 3. `assets/sfx/h5-first-bird.mp3`

**Función:** un solo canto distante al borde del bosque (~68.5s).
**URL:** https://freesound.org/search/?q=distant+blackbird+single+call&f=duration%3A%5B0+TO+5%5D
**Criterio:** 1-3s, un solo canto identificable, lejos, suena solitario.

---

## 4. `assets/sfx/h6-laughter.mp3`

**Función:** humanidad cálida en la fogata (~73.5s).
**URL:** https://freesound.org/search/?q=group+people+laughing+warm+intimate&f=duration%3A%5B2+TO+8%5D
**Criterio:** 3-5s, 3-5 voces, risa genuina (no actuada), distancia cercana.

---

## 5. `assets/sfx/h6-acoustic-strum.mp3`

**Función:** un acorde de guitarra acústica cálida (~75s).
**URL:** https://freesound.org/search/?q=acoustic+guitar+single+chord+warm&f=duration%3A%5B1+TO+4%5D
**Criterio:** 1-3s, UN solo acorde (no progresión), abierto/mayor/sus2, íntimo.

---

## 6. `assets/sfx/h6-dawn-birds.mp3`

**Función:** coro de pájaros del amanecer (~78s).
**URL:** https://freesound.org/search/?q=morning+birds+chorus+countryside&f=duration%3A%5B3+TO+10%5D
**Criterio:** 4-6s, múltiples especies, cálido, sin tráfico ni voces.

---

## Workflow

Hazlo en una sesión (~15-20 min):

1. Abrir los 6 URLs en pestañas.
2. Escuchar 3-5 candidatos en cada uno → descargar mejor.
3. Convertir a MP3 si es WAV.
4. Renombrar siguiendo `assets/sfx/<nombre>.mp3`.
5. Anotar en `CREDITS.md` los CC-BY (autor + URL).

---

## Alternativa automatizada

Si preferís delegar al agente: instalar el MCP comunitario `freesound-mcp` (requiere API key gratis de Freesound). El agente busca, descarga, verifica licencia, y rellena `CREDITS.md` solo.
