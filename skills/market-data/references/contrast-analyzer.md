# Color contrast — passing the Adobe analyzer

Tool: **https://color.adobe.com/create/color-contrast-analyzer**. It implements
WCAG 2.1 contrast: paste a text color + background color, it returns the ratio
(1–21) and pass/fail per level. Every visual this skill ships must pass. The
palette in `visuals.py` is pre-checked, and `check_contrast()` runs the same
math on every render, so you rarely need the web tool — but use it to vet any
new color, photo background, or hand-built card.

## Thresholds (what the analyzer checks)
| Element | AA | AAA |
|---|---|---|
| Normal text (< ~24px, or < ~19px bold) | 4.5:1 | 7:1 |
| Large text (≥ ~24px, or ≥ ~19px / 14pt bold) | 3:1 | 4.5:1 |
| Non-text — UI components, icons, **chart bars/lines/wedges** (WCAG 1.4.11) | 3:1 | — |

House floors: **body text ≥ 4.5:1, large text & graphical objects ≥ 3:1.** Aim
higher where free — our INK/MUTED clear 9:1+.

## The ratio, in code
WCAG contrast = `(L_lighter + 0.05) / (L_darker + 0.05)`, where L is relative
luminance: linearize each sRGB channel (`c/12.92` if `c≤0.03928`, else
`((c+0.055)/1.055)^2.4`), then `0.2126R + 0.7152G + 0.0722B`. This is exactly
what `visuals.contrast_ratio(fg, bg)` and `visuals.check_contrast()` compute.

## Workflow
1. Render. `python visuals.py contrast` prints every palette pairing's ratio +
   pass/fail. The build asserts on any failure, so a render that completes is
   already compliant.
2. New color? Add it to `check_contrast()` (body→4.5 floor, graphical→3.0) and
   re-run before using it. Don't ship a color that isn't in the check.
3. Card over a photo/video frame instead of the solid bg? The bg is no longer
   fixed — sample the darkest and brightest regions behind the text and confirm
   the text still clears 4.5:1 against both. If it can't, use a multiply/softlight
   plate (see `ffmpeg-text-plates.md`) to force a contrast floor under the text.

## Known traps in this palette
- The old template label color `#6e78a8` **fails** 4.5:1 as body text on the
  navy bg — that's why MUTED is lightened to `#A7B2DE` (9.4:1). Don't revert it.
- BRAND blue `#2F5BFF` is 3.8:1 — fine for **bars** (graphical, 3:1 floor) but
  **not** for body text. Never set small text in BRAND on the dark bg.
- White-on-gold and white-on-light-green fail — never put white text on the
  WARN/UP fills. Labels go in the gutter (on bg), not inside light bars.
