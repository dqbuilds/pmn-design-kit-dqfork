# FFmpeg text plates & blend modes — full notes

Source: `visuals/general-knowledge/grok_report.pdf` ("Layer Blending Modes for
Good-Looking Text Backgrounds in FFmpeg") + the blend-mode table screenshot.
Complete reference for putting readable, broadcast-quality text/cards over
video (e.g. the episode's motion ticker bg). For static charts, `visuals.py`
already guarantees contrast on a solid bg — this is the video path.

In FFmpeg, "layer blending modes" mean the **`blend`** video filter (and its
temporal counterpart **`tblend`**), which composites two layers using
Photoshop-style math. Use it when a text background should *interact* with the
footage — preserving contrast, avoiding clash — instead of sitting on it as a
harsh solid rectangle. The everyday tool, though, is the `box` option in
`drawtext` with alpha; reach for `blend` only for frosted-glass, adaptive
darkening, contrast boosting, or full creative control.

## 1. Core concepts
- **Alpha compositing is the 90% solution.** Most "blending" for text is just
  normal overlay with opacity. Use color syntax like `black@0.65` (65% opaque
  black). Fast, hardware-friendly, sufficient for ~95% of professional work.
- **The `blend` filter** takes two inputs (base + overlay) and applies a
  per-pixel/per-channel formula. ~33 modes (FFmpeg 7.x). Set with
  `all_mode=xxx` (or per-channel `c0_mode`, `c1_mode`, …).
- **Colorspace is critical.** Blending in YUV (video default) produces
  unexpected colors (e.g. pink artifacts with `lighten`). Insert `format=gbrp`
  or `format=rgba` *before* blending and convert back to `yuv420p`/`yuv444p`
  after, for compatibility.
- **Alpha handling.** `blend` respects alpha — use `format=rgba` for
  transparent layers. Premultiplied vs straight alpha changes results; test both.
- **Performance & output.** Blending adds CPU/GPU load. For real-time or long
  video, prefer a simple `drawtext` box + `boxblur` over a full `blend`.

## 2. Blend modes that matter for text backgrounds
Ranked by practical usefulness:

| Mode | What it does mathematically | Best use for text backgrounds | Example opacity |
|---|---|---|---|
| normal | Standard layering (top layer replaces bottom where opaque) | Default with alpha — the everyday choice | 0.5–0.8 |
| multiply | Darkens (multiplies values) | Excellent dark semi-transparent plates that adapt to bright video | 0.6–1.0 |
| screen | Lightens (inverts & multiplies) | Light backgrounds or glowing text plates | 0.4–0.7 |
| overlay | Combines multiply + screen (contrast boost) | Natural-looking, high-contrast panels | 0.5–0.8 |
| softlight | Subtle, photographic contrast | Premium "modern" look — very forgiving | 0.5–0.75 |
| hardlight | Stronger contrast version of overlay | Dramatic or high-energy text | 0.4–0.7 |
| darken | Keeps darker pixel from each layer | Guarantees dark area for white text | 1.0 |
| lighten | Keeps lighter pixel | Guarantees light area for dark text (use with care) | 1.0 |
| linearburn | Strong darkening | Deep, cinematic text plates | 0.7–1.0 |
| exclusion | Inverts colors where overlapping | Creative/graphic effects (less common for text) | 0.5–0.8 |

Other modes (addition, difference, grainmerge, etc.) are rarely useful for
clean text backgrounds and often create noisy or unnatural results.

## 3. Practical workflows (simple → advanced)

### Workflow 1 — Simple & fast (recommended starting point)
```bash
ffmpeg -i input.mp4 -vf "
drawtext=
  text='Sales Q3 Results':
  fontcolor=white:
  fontsize=52:
  fontfile=/path/to/font.ttf:
  x=(w-text_w)/2:
  y=h*0.85:
  box=1:
  boxcolor=black@0.68:
  boxborderw=30:20:
  shadowx=3:shadowy=3:shadowcolor=black@0.6
" -c:v libx264 -crf 18 -c:a copy output.mp4
```
Why it looks good: `@0.68` gives just enough opacity for readability without
blocking the video.

### Workflow 2 — Custom-shaped background with `drawbox` + alpha
For a full-width banner or precise padding.
```bash
ffmpeg -i input.mp4 -vf "
format=yuv444p,
drawbox=
  x=100:
  y=ih-180:
  w=iw-200:
  h=120:
  color=black@0.72:
  t=fill,
drawtext=
  text='Your Text':
  fontcolor=white:
  fontsize=48:
  x=130:
  y=ih-130
" -c:v libx264 output.mp4
```

### Workflow 3 — True blending modes (adaptive backgrounds)
Create a separate background layer, blend it, then draw text on top.
```bash
ffmpeg -i input.mp4 -filter_complex "
[0:v]split[main][tmp];
[tmp]crop=iw:160:0:ih-160,boxblur=8:2[blur];          # frosted glass effect
[main][blur]blend=all_mode=multiply:all_opacity=0.75[bg];
[bg]drawtext=
  text='Your Text Here':
  fontcolor=white:
  fontsize=50:
  x=(w-text_w)/2:
  y=h-110:
  box=1:boxcolor=black@0.3
" -c:v libx264 output.mp4
```
Alternative — full-screen colored layer (multiply for a dark adaptive plate):
```bash
ffmpeg -i input.mp4 -filter_complex "
color=color=black:s=1920x1080:d=60,format=rgba[bg];
[0:v][bg]blend=all_mode=multiply:all_opacity=0.65[blended];
[blended]drawtext=...[final]
" -map "[final]" output.mp4
```

### Workflow 4 — Glassmorphic / premium modern look (most requested 2025–2026)
Blur a section of video → overlay with `softlight` or `multiply` → add a thin
text plate. Creates the trendy frosted-glass effect that feels expensive and
reads on any background.

## 4. Nuances, edge cases & pro tips
- **Readability first.** Always test on the darkest and brightest parts of the
  video. **Multiply + white text is the most reliable combination.**
- **Color accuracy.** Insert `format=yuv444p` or `gbrp` before any blend/draw
  if colors shift.
- **Rounded corners.** FFmpeg has no native rounded rectangle in `drawbox` —
  approximate with multiple overlapping boxes or an external PNG overlay with alpha.
- **Dynamic text.** Use `textfile` + `reload=1` for changing text; blending
  still applies the same way.
- **Performance.** For 4K or long video, prefer simple alpha boxes. Full
  `blend` + blur can be 3–5× slower.
- **HDR / 10-bit.** Use `format=gbrpf` or higher-precision pipelines; blend
  modes behave differently in HDR.
- **Subtitles vs hardcoded.** For burned-in text the above applies. For soft
  subtitles use the `subtitles` filter with its own styling (less blend control).
- **Common pitfalls:**
  - Forgetting to convert colorspace → pink/magenta artifacts.
  - Overly opaque backgrounds → blocks video content.
  - No padding → text touches the edge of the box.
  - Using `lighten` without testing → text can disappear on bright areas.

## 5. Long-term implications & best practices
Well-blended backgrounds turn amateur overlays into broadcast-quality elements
and keep viewer focus on the message rather than fighting poor readability.

**Recommended workflow order for any project:**
1. Start with `drawtext` box + alpha (fast iteration).
2. Add `boxblur` on a background layer if you want a premium feel.
3. Only move to the `blend` filter when the background must react to video content.
4. Always add a subtle text shadow and generous padding.
5. Test export to MP4 (H.264) and WebM (VP9) — some players handle alpha differently.

Once you internalize **multiply + softlight + alpha compositing**, you'll
rarely need anything more complex — these give ~95% of After Effects' power
inside a single FFmpeg command.
