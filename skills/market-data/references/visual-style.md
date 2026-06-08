# Visual style — market-data social assets

Governs every chart/card from `visuals.py`. Two hard gates: **WCAG contrast**
(passes color.adobe.com's contrast analyzer) and the **canvas dimensions** that
survive X compression. Static charts render on solid dark bg (contrast inherent);
the FFmpeg blend rules below are for placing text/cards over *video*.

## Canvas
- **3:2 — 2048×1365** (default; the X-compression-safe master).
- **1:1 — 2048×2048** (feed square / stat cards).
- **9:16 — 1152×2048** (stories / Reels / vertical cut).
Render at the largest, downscale per platform. Never upscale.

## Palette (Priced In) + measured contrast vs bg `#03082A`
| Token | Hex | Role | Ratio | Floor |
|---|---|---|--:|---|
| INK | `#FFFFFF` | primary text | 19.6:1 | 4.5 (AAA) |
| MUTED | `#A7B2DE` | labels / source | 9.4:1 | 4.5 |
| BRAND | `#2F5BFF` | default bars | 3.8:1 | 3.0 (graphical) |
| UP | `#3BEF8E` | positive / highlight | 13.0:1 | 3.0 |
| WARN | `#EFC23B` | highlight / big stat | 11.6:1 | 3.0 |
| DOWN | `#FF5C7A` | negative | 6.6:1 | 3.0 |
| PANEL | `#0A1340` | card fill | — | (MUTED on it = 8.5:1) |
| GRID | `#22306A` | hairlines (non-text) | — | decorative only |

**Contrast rule:** body text ≥ 4.5:1, large text (≥24px) and graphical objects
(bars, wedges) ≥ 3:1. `visuals.check_contrast()` asserts this on every render;
run `python visuals.py contrast` to print the proof. Don't introduce a color
without adding it to the check. `#6e78a8` from the old templates fails 4.5:1 as
body text — that's why MUTED is lightened to `#A7B2DE`.
→ Full WCAG thresholds, the luminance formula, and the Adobe analyzer workflow:
**`contrast-analyzer.md`**.

## Story-driven color (not axis-locked)
Bars default to BRAND blue. Pass `highlight={...}` to paint the names the news
cycle cares about in WARN gold. The grouping follows the story, not a fixed
per-asset/chain mapping — re-decide it each render.

## Every visual is sourced
Footer carries `Source: … · as of <date>` and the handle. On-chain figures are
timestamped (they move intraday) — pass the query date as `asof`.

---

## Text over video — FFmpeg blend doctrine (from grok_report.pdf)
→ Full notes, all 4 workflows with copy-paste ffmpeg commands, colorspace
fixes, pitfalls, and the complete blend-mode table: **`ffmpeg-text-plates.md`**.
Quick version below — use when a card/lower-third sits over the episode's motion
ticker bg. Order of escalation (stop at the first that looks good):

1. **Alpha box (90% of cases).** `drawtext … box=1:boxcolor=black@0.68:boxborderw=30:20`
   plus a subtle shadow (`shadowx=3:shadowy=3:shadowcolor=black@0.6`). Fast.
2. **drawbox banner** for full-width lower-thirds with precise padding
   (`drawbox=…:color=black@0.72:t=fill`).
3. **Adaptive blend plate** when the bg must show through and stay readable on
   bright *and* dark footage — the premium/glassmorphic look:
   blur a crop, `blend=all_mode=multiply:all_opacity=0.75`, then draw text.

**Blend mode → opacity (for text plates):**
| Mode | Use | Opacity |
|---|---|--:|
| normal | default alpha plate | 0.5–0.8 |
| multiply | dark plate that adapts to bright video (most reliable) | 0.6–1.0 |
| softlight | premium "modern", very forgiving | 0.5–0.75 |
| screen | light / glowing plates | 0.4–0.7 |
| overlay | natural high-contrast panels | 0.5–0.8 |
| darken | guarantee a dark area for white text | 1.0 |
| linearburn | deep cinematic plates | 0.7–1.0 |

Defaults that always work: **multiply + white text**, ~0.68 opacity, generous
padding, subtle shadow. Insert `format=yuv444p` (or `gbrp`) before blending to
avoid pink/magenta colorspace artifacts; convert back to `yuv420p` after.

## Motion-bg restraint
Behind body copy, keep motion subtle — ripple or a muted uniform ticker. Busy,
tilted, high-contrast motion competes with the text and loses. The static
charts here are designed to sit on solid bg; only composite over motion when
the plate rules above are applied.
