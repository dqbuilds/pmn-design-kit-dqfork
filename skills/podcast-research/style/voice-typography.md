# Voice Rules — Typography & Safe Areas

Load this file whenever a visual contains text that must fit a specific layout
(quote cards, end-of-thread visuals, banner text, data charts with labels,
article hero artwork). Apply alongside `style/voice-visual.md`.

This file exists because text overflow / bleed has been a recurring failure mode
across visual work. The rules here are non-negotiable safeguards.

---

## Core Principle

**Text never exceeds its declared safe zone. Ever.**

If text doesn't fit at the largest font size, shrink the font BEFORE shrinking
the safe zone. If text doesn't fit at the smallest font size, surface a warning
to the caller — do not let it bleed off the canvas or into adjacent UI regions.

---

## Safe Area Definition

Every visual has THREE concentric zones:

```
┌────────────────────────────────────┐  ← canvas edge
│  ▒▒▒ DANGER ZONE (margin) ▒▒▒      │
│  ┌──────────────────────────────┐  │
│  │  ░░░ ALLOWED (content area) │  │
│  │  ┌────────────────────────┐  │  │
│  │  │   SAFE ZONE (text)    │  │  │
│  │  │                       │  │  │
│  │  └────────────────────────┘  │  │
│  └──────────────────────────────┘  │
└────────────────────────────────────┘
```

- **Danger zone**: outermost ~5% of canvas. Nothing of consequence here —
  display crops, social platform avatars, browser bars may obscure it.
- **Content area**: where decorative elements (logos, marks, accent lines)
  can live. Bounded by canvas margin (typically 64px on a 1200×1200 canvas).
- **Safe zone**: where text MUST stay. Smaller than the content area by
  another ~50–100px on each side to leave room for visual hierarchy.

**Recommended margins by canvas size:**

| Canvas | Content margin | Safe-zone margin |
|---|---|---|
| 1200×1200 (square) | 64 px | 200 px (text), 100 px (large headlines) |
| 1500×500 (banner) | 50 px | 80 px (text), 60 px (headlines) |
| 1600×900 (article hero) | 80 px | 200 px (text), 120 px (headlines) |
| 2400×2400+ (supersampled) | Scale all above ×2 |

---

## Font Size Ladder

When text must auto-fit, **always try multiple sizes** and pick the largest
that fits. Hard-coding a single font size is the #1 cause of overflow.

**Recommended ladder for English body / quote text** (pt at 1× — multiply by
SCALE for supersampled rendering):

```
[88, 80, 72, 64, 58, 52, 46, 42, 38, 34, 30, 26]
```

- Start at index 0 (largest), step down, return the first one that fits.
- Use **finer steps near the top** (88 → 80 → 72) so short and medium quotes
  don't drop too aggressively.
- Set a **floor** — usually 22–26pt — below which body text becomes illegible.

**Recommended ladders by purpose:**

| Purpose | Ladder (1× pt) |
|---|---|
| Headlines / hero quotes | `88, 80, 72, 64, 58, 52, 46, 42, 38, 34` |
| Body copy / paragraphs | `24, 22, 20, 18, 17, 16, 15, 14` |
| Labels / micro-text | `15, 14, 13, 12, 11` |
| Big-stat hero numbers | `200, 180, 160, 140, 120, 100, 80` |

---

## Line Height (CRITICAL)

**Wrong way** (causes overflow): measure line height by drawing "Mg" and using
its bounding box height. This excludes the ascent/descent space needed for
characters like `j`, `g`, `Q`.

**Right way:** use the font's actual metrics.

```python
ascent, descent = font.getmetrics()
line_height = int((ascent + descent) * LINE_GAP_RATIO)
```

**Recommended `LINE_GAP_RATIO` values:**

- Headlines (44pt+): `1.15` — tight, dramatic
- Body text (18–22pt): `1.40` — comfortable reading
- Quotes / pull-text (40–80pt): `1.20` — balanced
- Captions / labels (12–14pt): `1.55` — extra breathing for small type

---

## Word-Wrap Algorithm

Standard word-wrap is fine for English. The key trap: **single words that
exceed `max_width`**. These cause overflow even after wrapping. Detect them:

```python
def wrap_text(text, font, max_w):
    overflow = False
    words = text.split()
    lines = []
    current = []
    for word in words:
        test = ' '.join(current + [word])
        if measure_width(test, font) <= max_w:
            current.append(word)
        else:
            if current:
                lines.append(' '.join(current))
            if measure_width(word, font) > max_w:
                overflow = True   # ← single word too wide — drop font size
            current = [word]
    if current:
        lines.append(' '.join(current))
    return lines, overflow
```

When `overflow=True`, **skip this font size and try the next smaller one.**
Don't accept a layout where a long word will bleed past the safe zone.

---

## Vertical Block Placement

After determining font size and wrapping, the text block has a known height
(`line_height × n_lines`, plus inter-paragraph gaps).

**Always centre the block vertically within the band**, not anchored to top or
bottom. This way short and long quotes both look balanced.

```python
block_h = line_height * len(lines) + sum_of_paragraph_gaps
cy = (BAND_TOP + BAND_BOTTOM) // 2
start_y = cy - block_h // 2
```

**Hard safety clamp:** if `block_h > BAND_BOTTOM - BAND_TOP`, anchor to top with
safety margin AND log a warning. Do not let the block extend past the band.

```python
if block_h > (BAND_BOTTOM - BAND_TOP):
    start_y = BAND_TOP + SAFETY_MARGIN
    print("⚠  text too long for safe band — shorten the copy")
```

---

## Overlap With Decorative Elements

Decorative elements (large quote marks, logos, frames) can VISUALLY overlap
with text only when they are **at low opacity** (≤ 30%) AND **behind** the text
layer.

Never let text overlap with:
- Solid logo marks
- Footer attribution blocks
- Channel pill buttons or CTA elements
- Other text at full opacity

When in doubt, reduce the decorative element's opacity below 30% OR move the
text further from it.

### Sizing decorative elements relative to the safe band

A common failure mode: oversized decorative glyphs (large pull-quote marks,
giant chapter numbers) push into the text safe band even when at low opacity,
making the composition feel crowded.

**Rule:** the decorative element's visible bounding box must end at least
`SAFETY_MARGIN` (16–20px native) BEFORE the top of the text safe band starts.

For pull-quote glyphs specifically:
- A curly quote `"` at font size N has a visible glyph height of roughly
  `N × 0.5` and sits in the UPPER portion of its em-box.
- Position the mark with `anchor="lt"` and verify:
  `mark_y + (mark_size × 0.55) + SAFETY_MARGIN ≤ BAND_TOP`
- If this constraint isn't met, either:
  1. **Shrink the mark** (preferred — keeps composition airy)
  2. **Push BAND_TOP down** to clear it
  3. **Move the mark further from the band** (e.g., into the corner)

Default sizing for pull-quote marks on a 1600×900 canvas:
- `QM_SIZE` (font size): 200–240pt — anything larger competes with text
- `BAND_TOP` must be ≥ `mark_y + mark_size × 0.55 + 20`

The closing mark (bottom-right with `anchor="rb"`) sits below the band, so the
constraint flips: `mark_y - mark_size × 0.55 ≥ BAND_BOTTOM + 20`.

---

## Auto-fit Pseudocode (the canonical pattern)

This is the algorithm every text-fitting visual should use:

```python
SAFE_W = TEXT_X_END - TEXT_X_START
SAFE_H = BAND_BOTTOM - BAND_TOP - 2 * SAFETY_MARGIN

for size in SIZE_LADDER:                       # largest first
    font = load_font(size)
    line_h = font_line_height(font)
    lines, overflow = wrap_text(text, font, SAFE_W)
    if overflow:
        continue                                # word too wide — try smaller
    block_h = line_h * len(lines)
    if block_h <= SAFE_H:
        return size, lines, line_h, ok=True     # ✓ this size fits

# nothing fit cleanly — return smallest with warning
return SIZE_LADDER[-1], ..., ok=False
```

The caller MUST check `ok` and either truncate or warn — never silently let
text overflow.

---

## Pre-Render Validation Checklist

Before saving any visual that contains text, verify:

- [ ] Every text element has a declared safe zone
- [ ] Font size was chosen via auto-fit (not hard-coded)
- [ ] Line height uses font metrics, not `textbbox("Mg")`
- [ ] No word in the wrapped output exceeds the safe width
- [ ] Total block height ≤ safe band height
- [ ] Vertical block placement uses band centering, not fixed Y
- [ ] Text never overlaps full-opacity decorative elements
- [ ] If auto-fit returned `ok=False`, a warning was logged
- [ ] Decorative elements (quote marks, brackets, logos) sit ≥ 16px from text edges OR are at ≤ 30% opacity

---

## Common Failure Modes (and Fixes)

| Symptom | Cause | Fix |
|---|---|---|
| Text bleeds off right edge | `max_w` too generous OR overflowing word not detected | Reduce `TEXT_X_END` margin · Add overflow check in wrap_text |
| Text bleeds below safe band | Line height too small, ignores descenders | Use `font.getmetrics()` for line height |
| Last line clipped at bottom | Block height calculated without final descender | Same fix — use proper metrics |
| Long quote breaks layout | Font ladder doesn't go low enough | Add 30pt, 26pt to ladder |
| Single long word breaks line | `wrap_text` doesn't detect unbreakable words | Add overflow check, skip font size if any word > max_w |
| Body collides with footer | No safety margin between sections | Always leave 60–80px between text block and adjacent UI |
| Text overlaps decorative mark | Decoration at full opacity | Reduce to ≤ 30% opacity or move further from text |

---

## Branding by Content (mandatory)

Typography rules are universal but **branding is always content-driven**.
Never default to one brand's identity (e.g. Elara) for content that belongs to
a different publication, podcast, or product.

**Brand selection rule:** match the brand to whoever owns or publishes the
content. Examples:

| Content origin | Brand to use |
|---|---|
| Elara protocol announcement, Elara research thread | `elara` |
| Layer One podcast episode quote, host clip | `layer_one` |
| The Block article hero, news story | `the_block` |
| Guest's own content republished | guest's brand (or neutral if unknown) |

If the content's brand is unclear, ask before generating — don't guess.

### Architecture for brand-aware templates

Reusable templates must accept `brand` and `mode` parameters and consume a
brand config dict. Recommended structure:

```
scripts/
  brands/
    __init__.py       # load_brand(name, mode) loader
    elara.py          # BRAND dict
    layer_one.py
    the_block.py
  quote_template.py   # imports load_brand
```

Each brand config exposes a `BRAND` dict with this schema (see brands/elara.py
for a reference implementation):

```python
BRAND = {
    'name':                str,         # 'elara', 'layer_one', etc.
    'wordmark_text':       str,         # 'ELARA', 'LAYER ONE'
    'mark_path':           str | None,  # logo PNG path or None for text-only
    'attribution_prefix':  str,         # e.g. 'Layer One · '
    'modes': {
        'dark':  { ...mode_config... },
        'light': { ...mode_config... },
    }
}
```

Each mode_config contains:

```python
{
    'bg_color':           (r, g, b, a),  # canvas fill
    'bg_pattern':         str,           # 'stars' | 'dots' | 'grid' | 'none'
    'bg_pattern_color':   (r, g, b, a),
    'text_primary':       (r, g, b, a),  # main text
    'text_emphasis':      (r, g, b, a),  # emphasis/punchline lines
    'text_secondary':     (r, g, b, a),  # attributions, captions
    'accent':             (r, g, b, a),  # brand accent (quote marks, accent lines)
    'quote_mark_alpha':   int 0–255,     # alpha for decorative quote marks
}
```

### Light vs Dark mode rules

Both modes must be supported by every brand template (unless the brand has
declared one-mode-only). Common patterns:

| Element | Dark mode | Light mode |
|---|---|---|
| Background | near-black `(5, 5, 10)` or solid `(0, 0, 0)` | warm off-white `(252, 250, 248)` |
| Background pattern | stars (white dots) | dots, grid, or none |
| Primary text | near-white `(252, 252, 252)` | near-black `(12, 12, 16)` |
| Secondary text | light grey `(170, 170, 170)` | medium grey `(95, 95, 95)` |
| Decorative quote marks alpha | 60–90 (subtle on dark) | 45–65 (visible on light) |
| Accent color | usually brand color at full intensity | brand color (may need darkening for contrast — e.g. chartreuse → olive) |

**Watch for**: brand accents that are illegible in one mode. Chartreuse `#F1FF58`
is unreadable on white — in light mode the Elara brand swaps to dark grey for
text-purpose elements while keeping yellow for decorative-only uses (or skips
light mode entirely).

### Confirming brand assets before shipping

When a brand config still has placeholder values (signalled by comments like
`⚠ PLACEHOLDER` or `# TODO`), surface this to the user before delivering
final visuals. The user must confirm:
1. Logo file (transparent PNG)
2. Primary accent hex value
3. Approved wordmark text
4. Both mode background and text colors

Until confirmed, deliver visuals with a clear caveat: "Layer One brand values
are placeholders — confirm and I'll regenerate with official assets."

### Render resolution (supersample / quality)

**Final output size: 2048 × 1365 px (3:2 aspect).** This is the X "no-crop"
sweet spot — survives the platform's JPEG re-encode cleanly, hits the
single-image preview at full size, and avoids the aggressive recompression
that larger files get.

**Internal layout coords: 1600 × 1067** (3:2). Supersample at SCALE=3 for
crispness, then downsample to 2048×1365 with `Image.LANCZOS` at save time.

Why 3:2 (not 16:9):
- 16:9 (1600×900) gets letterboxed or cropped in the X timeline preview
- 3:2 fills the no-crop slot, no wasted dead zone, no surprise cropping of
  decorative elements (quote marks, end-dots) at the canvas edges

Why downsample (vs. saving at 4800×3201 native):
- X aggressively recompresses anything over ~5 MB or beyond ~2048 on the long
  edge; smaller-but-supersample-sourced files survive compression with less
  artifacting than larger-uncompressed files
- 2048×1365 PNGs land in the ~300 KB range — well under the 5 MB limit

Implementation pattern:

```python
SCALE = 3
W, H = 1600 * SCALE, 1067 * SCALE      # internal: 4800×3201
OUTPUT_W, OUTPUT_H = 2048, 1365        # X-safe 3:2

def _s(v): return int(v * SCALE)       # everywhere coords/sizes go through this

# ...at save time:
final = canvas.resize((OUTPUT_W, OUTPUT_H), Image.LANCZOS)
final.convert('RGB').save(output_path, 'PNG', quality=95, optimize=True)
```

For animated GIF/MP4 from frame sequences:
- GIF: frames at 2048×1365 exact (palette-optimized two-pass)
- MP4: 2048×1364 (one pixel less to satisfy yuv420p even-dimension requirement)

**Always set `Image.LANCZOS`** as the resampling filter on any raster logo
resize. Bicubic and nearest-neighbor introduce visible artifacts at the scales
typical for brand marks (downscaling logos from 1000–6000px source to 200–500px
display).

**Never embed raster logos at less than 2× their display target.** If a logo
asset is 100×100 source and display target is 200×200, the upscale will be
visible. Source a larger asset before scaling.

---

### Output file organization

Generated visuals must be organized by brand-first, then by content type, then
by mode where applicable. This keeps assets findable, prevents collisions
across episodes/articles, and makes it obvious which brand owns each output.

**Top-level structure:**

```
visuals/elara/exports/abstract/quotes/
├── elara/                          ← Elara protocol content
│   ├── quote-01-capital-suck.png
│   └── ...
└── layer_one/                      ← Layer One podcast content
    ├── dinari/                     ← per-episode topic folder
    │   ├── dark/
    │   │   ├── dinari-01-custodial-model.png
    │   │   └── ...
    │   └── light/
    │       ├── dinari-01-custodial-model.png
    │       └── ...
    ├── opentrade/                  ← future OpenTrade/Mercury episode
    │   ├── dark/
    │   └── light/
    └── ...
```

**Naming rules:**

| Tier | Convention | Examples |
|---|---|---|
| Brand folder | brand name in `snake_case` | `elara/`, `layer_one/`, `the_block/` |
| Sub-brand / episode topic | short topic slug (no episode numbers in folder) | `dinari/`, `opentrade/`, `kite-ai/` |
| Mode folder | `dark/` or `light/` when both supported | `dark/`, `light/` |
| File name | `<topic>-NN-<slug>.png` | `dinari-01-custodial-model.png` |

**Why this matters:**
- Layer One is the umbrella podcast; episodes like Dinari, OpenTrade/Mercury,
  Kite AI all sit inside it.
- The Block, when given its own content (articles, news graphics), gets its
  own top-level folder — separate from Layer One because the content type
  differs even if brand styling overlaps.
- Elara stays separate from all podcast content because it's a different
  brand domain (protocol vs. media).

When generating new visuals, always create the brand folder first if it
doesn't exist, then the topic subfolder, then mode folders. Don't drop
loose files at the top level.

---

### Multi-brand hierarchy (co-productions, partnerships)

Some content is co-produced or hosted under multiple brands. The classic
example is Layer One — a podcast hosted on The Block, in collaboration with
Avalanche. There are THREE brand identities at play; rendering them well
requires a clear hierarchy:

| Tier | Role | Visual position | Visual treatment |
|---|---|---|---|
| **Primary** | The show / product identity | Top-right corner | Wordmark + (optional) logo, brand accent color, ~20pt |
| **Secondary** | Publisher / host network | Bottom-right corner | Smaller wordmark (~15pt), muted color, optional small dot anchor |
| **Tertiary** | Collaborator / partner | Small text line under attribution | Plain text, secondary text color, ~11pt |

**Implementation pattern (brand config schema):**

```python
BRAND = {
    'name': 'layer_one',
    'wordmark_text': 'LAYER ONE',           # primary — top-right
    'mark_path': None,                       # primary logo file
    'attribution_prefix': 'Layer One · ',
    'collaboration_line': 'in collaboration with Avalanche',  # tertiary
    'secondary_brand': {                     # secondary — bottom-right corner
        'wordmark_text': 'THE BLOCK',
        'mark_path': None,
        'position': 'bottom-right',
    },
    'modes': {
        'dark': {
            ...
            'accent': (225, 50, 45, 255),         # primary accent
            'secondary_accent': (200, 200, 200, 255),  # muted for secondary
        }
    }
}
```

**Decorative element conflicts:**

When a secondary brand occupies the bottom-right corner, the decorative
closing quote mark (typically placed there) must yield. Three options, in
preference order:

1. **Drop the closing mark** (cleanest) — let the secondary brand occupy the
   corner alone. The opening quote mark still signals "pull quote".
2. **Stack vertically** — closing mark above secondary brand, with vertical
   safety margin between them.
3. **Move the closing mark** to bottom-left, paired with attribution.

In the quote-template, the rule is: if `secondary_brand` is present in the
brand config, the closing mark is automatically suppressed.

**Watch for visual dominance issues:**

The secondary brand must never compete with the primary brand for attention.
Keep it ~25% smaller, use a muted color (`secondary_accent` in mode config —
white/grey in dark mode, dark grey in light mode), and never place it at the
same size or same corner as the primary wordmark.

---

## When this file applies

Load `style/voice-typography.md` (this file) whenever you are:

- Generating any visual that contains text (PIL, SVG, or otherwise)
- Building reusable visual templates
- Debugging text overflow or alignment issues
- Designing a new layout that includes copy
- Choosing which brand to apply to content (see "Branding by Content" above)

Always cite this file's rules when delivering a visual to the user — it builds
trust that text fitting AND brand selection are being handled deliberately,
not by chance.
