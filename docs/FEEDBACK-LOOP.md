# The Feedback Loop

How an agent (me) actually verifies its own video work without being able to watch or listen to the output.

## The core insight

I can't play a video. I can't listen to audio. But I **can** read images and text. So the whole method is:

> Convert the output medium into something I can read, inspect the conversion, decide what to fix, edit, re-render. Loop.

One loop, same six stages, different conversion tools per medium.

```
Render  →  Slice  →  Read  →  Diagnose  →  Edit  →  Re-render
                                                        │
                                                        ▼
                                              (back to Slice)
```

---

## The six stages

### 1. Render — produce the artifact, cheaply first

**Goal:** get a runnable draft, not a final. Drafts surface structural bugs (missing elements, broken layouts, wrong timing) without wasting minutes on high-quality encoding.

**Rule:** always start in draft quality. Upgrade to standard/high only when the structure is known-good.

```bash
npx hyperframes render -q draft -o renders/draft.mp4        # ~2 min
npx hyperframes render -q standard -o renders/final.mp4     # ~5 min
```

Use `-w` to tune worker count if the machine allows. 6 workers is the usual sweet spot.

### 2. Slice — convert the medium into readable pieces

**Goal:** reduce the 60-second opaque MP4 into a handful of discrete inspectable stills.

**Rule:** sample at least one frame per scene. For a 60s video with 7 scenes, sampling every 6 seconds (10 frames) catches each scene once.

```bash
ffmpeg -v error -i renders/draft.mp4 \
  -vf "fps=1/6,scale=540:-1" \
  /tmp/frames/f%02d.png -y
```

- `fps=1/6` — one frame every 6 seconds
- `scale=540:-1` — shrink to 540px wide to save tokens (original is 1080px)
- `f%02d.png` — zero-padded filenames so they sort correctly

For targeted checks (a specific timestamp), use `-ss` instead of `-vf fps`:

```bash
ffmpeg -ss 49 -i draft.mp4 -frames:v 1 -vf "scale=540:-1" /tmp/f_t49.png
```

### 3. Read — actually see the output

**Goal:** observe the pixels with the same tool the user would use (their eyes).

**Rule:** read every frame, not a sample. Reading only half the frames means missing bugs in the half you skipped. 10 frames = 10 `Read` calls, in parallel.

```
Read f01.png
Read f02.png
...
Read f10.png
```

The `Read` tool feeds the image into my vision model. I perceive the frame as a human would — I can describe what's there, spot overflow, misalignment, wrong colors, missing elements.

### 4. Diagnose — reason from evidence, don't guess

**Goal:** map each visible problem to the specific CSS rule or GSAP tween that caused it.

**Rule:** "make it smaller" is a guess. "220px × ~0.58em × 8 chars = ~1020px but content area is only 920px wide, overflow 100px, reduce to 200px" is a diagnosis. Do the second one.

What to write down per issue:
- **Where** (frame number, scene, element)
- **What** (observable symptom — "text cut off right edge")
- **Why** (numeric reason — "font-size × char width > content width")
- **Fix** (specific change — "200px" not "smaller")

### 5. Edit — surgical, one-pass changes

**Goal:** apply every known fix in one batch, not iteratively.

**Rule:** if you found 3 problems, send 3 edits in the same round. Don't render between edits. Rendering is the expensive step; batch edits to minimize render count.

```
Edit: font-size 220 → 200  (Scene 3 hero)
Edit: font-size 170 → 118  (Scene 4 reveal)
Edit: font-size 108 → 92   (Scene 6 prelude)
```

Also: re-run lint between edit and re-render.

```bash
npx hyperframes lint                # catch syntax and schema bugs
npx hyperframes validate --no-contrast   # catch broken resources
```

### 6. Re-render — confirm, then promote

**Goal:** verify the fixes landed AND the fixes didn't break anything else.

**Rule:** after the fix-render, slice and read the exact frames that previously failed — **plus** two or three that previously worked. Regressions love neighboring scenes.

When the re-render looks clean at draft quality, promote to standard quality for the final output.

---

## Per-medium applications

### Video

Medium: `.mp4` → Cannot be played, only rendered and transcoded.

| Stage | Tool | Output |
|---|---|---|
| Render | `npx hyperframes render` | `.mp4` |
| Slice | `ffmpeg -vf fps=1/N` | `.png` frames |
| Read | `Read f*.png` | visual perception |
| Diagnose | reasoning from pixel evidence | list of fixes |
| Edit | `Edit` on `index.html` | new HTML |
| Re-render | back to step 1 | new `.mp4` |

Extra useful commands:

```bash
ffprobe -v error -show_entries format=duration,bit_rate \
  -show_entries stream=codec_name,width,height,r_frame_rate \
  -of default=nw=1 video.mp4
```
→ confirms duration, resolution, codecs in one shot.

### Images

Medium: `.png` from Gemini → readable directly, no slicing needed.

| Stage | Tool | Output |
|---|---|---|
| Render | `ai-video image` (Gemini) | `.png` |
| Slice | — (images are already single frames) | — |
| Read | `Read scene-factory.png` | visual perception |
| Diagnose | on-brand / off-brand, crop, aesthetic | prompt adjustment |
| Edit | rewrite prompt | new prompt |
| Re-render | re-run the script | new `.png` |

Short-circuit: if the first generation is on-brand (monochrome, editorial, no color bleed), skip steps 4-6 and ship it. Save tokens and API calls.

**Prompt-engineering the loop shut:** The smartest move is embedding brand constraints into the prompt itself so the first output is usually correct. `ai-video image` always appends:

```
Pure monochromatic black and white only. Absolute black background #000000.
Grayscale exclusively — no color, no tints, no hues of any kind.
High contrast, surgical, editorial. Vercel / OpenAI / Studio Aberrante aesthetic.
No text, no logos, no watermarks.
```

This narrows the output distribution before any feedback loop starts.

### Audio

Medium: `.mp3` / `.wav` → cannot listen. Need two proxies: duration and transcription.

| Stage | Tool | Output |
|---|---|---|
| Render | `ai-video tts` (ElevenLabs) | `.mp3` |
| Slice | `ffprobe -show_entries format=duration` | duration in seconds |
| Slice (pt.2) | `npx hyperframes transcribe` | word-level `transcript.json` |
| Read | `Read transcript.json` | text + timestamps |
| Diagnose | is the text actually Spanish? right words? right length? | script revision |
| Edit | rewrite `script.txt` | new text |
| Re-render | re-run `ai-video tts` | new `.mp3` |

Two proxies because audio can fail in two ways:
- **Duration wrong** → too short or too long for the video (first attempt: 37.4s, needed 52s → rewrite script longer)
- **Content wrong** → transcript reveals English words when Spanish was intended (the bug that taught us `language_code: "es"` doesn't translate)

ffprobe catches duration bugs. Transcription catches content bugs. Together they substitute for ears.

### Animation timing

Medium: GSAP tweens inside a composition → cannot be "played" in isolation.

Proxy: render a frame at a specific timestamp and inspect.

```bash
ffmpeg -ss 49 -i draft.mp4 -frames:v 1 /tmp/t49.png
Read /tmp/t49.png
```

If the element that was supposed to enter at t=49s isn't visible at t=49s → tween fired late, fire earlier. If an element is fully visible at t=49s but the tween is scheduled at 49s → the `from` state leaked its end-state; fix with `fromTo` or explicit `tl.set` at t=0.

---

## Escalation rules — when to break the loop

The loop assumes the composition mostly works and needs polishing. Break it when:

- **Lint or validate fail** → fix the schema/resource bug before rendering anything. Don't render broken HTML.
- **Audio duration doesn't match target** → fix the script first. Rendering a 60s composition over 37s of audio leaves 23s of dead air — the whole plan changes.
- **More than 5 overflow issues in one render** → you chose font sizes by guess. Stop, measure the content area (1080 − 2×padding), compute max char counts per font size, rewrite the scene dimensions deterministically.
- **Same fix, three iterations in a row, still broken** → you're misdiagnosing. Step back. Read the composition top to bottom. Look for hidden causes (parent opacity, filter inheritance, a `tl.from` whose end-state leaked).

---

## What makes the loop efficient

1. **Draft first, final last.** Never render final quality before the structure is known-good.
2. **Batch edits.** Never render after a single fix if you already know three.
3. **Read every frame, not a sample.** Sampling misses bugs.
4. **Reason from numbers.** "Cut off by 100px" is actionable; "looks wrong" is not.
5. **Constraint-load the prompts.** Bake brand rules into the generator so the first output is usually correct and the loop rarely needs to run.
6. **Use the right proxy per medium.** Stills for video, transcription for audio, JSON for data. Pick the tool that converts the medium into something readable.

---

## The meta-pattern

> I cannot perceive the output medium directly.
> So I convert it into something I can read.
> I inspect the conversion, decide what to fix, edit, re-convert.
> Loop until clean.

That's the whole thing. Every other method flows from this one.
