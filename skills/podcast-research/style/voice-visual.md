# Voice Rules — Visualization Standards

Load this file whenever a request involves charts, data visuals, or
infographics for Twitter, threads, or articles.

Apply alongside `style/voice-data.md` — not instead of it.
The data rules govern the copy. This file governs the visual.

---

## Core Principle

A visualization does one job: make the data story undeniable at a glance.

It is not decoration. It is not a screenshot of a dashboard.
It is a purpose-built image where every element — layout, color, scale,
label — serves the argument the copy is making.

If the visual requires reading to understand, it has failed.
The insight should land before the viewer reads a single label.

---

## Default Design System

All visuals use this system unless a brand-specific override applies (see below).

```
Canvas:      1200 x 800px  (Twitter landscape — 800h for safe breathing room)
Background:  #0B1220
Panel/card:  #131E2E
Border:      #1E2D42

Primary text:    #F0F4F8   (titles, key numbers)
Secondary text:  #8895A7   (labels, axis text)
Attribution:     #4B5563   (source line, 13px)

Accent blue:     #3B82F6   (primary highlight bar/line)
Accent teal:     #06B6D4   (secondary data series)
Accent purple:   #8B5CF6   (tertiary or comparison data)
Accent green:    #10B981   (positive change, growth)
Muted blue:      #1D4ED8   (medium-emphasis bars)
Dark blue:       #1E3A5F   (low-emphasis bars)

Font: system-ui, -apple-system, 'Segoe UI', sans-serif
```

---

## Brand Override: Elara Finance

When producing visuals for Elara Finance content, replace the default system
with the following. Do not mix the two systems within a single visual.

```
Canvas:      1200 x 800px

Background:  #101010       (near-black)
Panel/card:  #1A1A1A
Border:      #2A2A2A
Featured panel fill: #1D1D0A  (accent tint for highlighted sections)
Featured panel border: #F1FF58

Primary text:    #FFFFFF
Secondary text:  #CCCCCC
Muted text:      #888888
Dim text:        #555555
Attribution:     #444444

Primary accent:  #F1FF58   (Elara chartreuse — bars, lines, highlighted columns)
Accent tint:     rgba(241,255,88,0.12)  (panel backgrounds)
Dim accent:      #888844   (secondary Elara-tinted labels)
Green positive:  #4ADE80   (growth indicators)
Blue secondary:  #3B82F6   (comparison data, non-Elara protocols)
Purple tertiary: #8B5CF6   (third-party protocol data)
```

### Official Brand Assets

All Elara visuals must use the official brand files in
`/Users/kelvinsparksjr/Anthropic/visuals/elara/brand/`.
Do not regenerate, redraw, or AI-generate a similar mark — always pull from this folder.

| File | Dimensions | Background | Use |
|---|---|---|---|
| `elara-logo-mark.png` | 32×32 | transparent | Pure flat logo mark. Use scaled up only when sharpness is acceptable. |
| `elara-logo-3d-chromatic.png` | 1920×1080 | opaque black | Hero/cover shots — dramatic 3D render with chromatic aberration. |
| `elara-logo-outline.png` | 1920×1080 | transparent | Wireframe outline — backgrounds, watermarks, ghost layers. |
| `elara-wordmark.png` | 179×32 | transparent | Standard "ELARA" wordmark for headers and footers. |
| `elara-finance-wordmark.png` | 131×16 | opaque | Small "Elara Finance" lockup for compact bylines. |

**Companion working file** (for embedding inside generated SVGs at retina sharpness):
- `logo-mark-hd.png` (300×298, transparent) — cropped from the official 3D render, used by all current SVGs

**Footer stamp pattern for SVG charts (uses logo-mark-hd embedded as base64):**
```svg
<image x="1096" y="750" width="40" height="40" href="data:image/png;base64,...logo-mark-hd..."/>
<text x="1170" y="762" font-size="14" font-weight="700" fill="#F1FF58">ELARA</text>
```

If a higher-resolution flat mark is needed than 32×32 provides, use `logo-mark-hd.png`
or extract a clean alpha version from `elara-logo-3d-chromatic.png` — never AI-generate
a substitute.

---

## Brand Override: Layer One (podcast) — OFFICIAL ASSETS

For Layer One podcast content — episode clips, guest quotes, episode hero art.
A joint production: hosted on **The Block**, in collaboration with **Avalanche**.

### Brand hierarchy on every visual
- **Primary:** `LAYER ONE` wordmark — top-right corner
- **Secondary:** `THE BLOCK` logo — bottom-right corner (white variant on dark backgrounds, black on light)
- **Tertiary:** "in collaboration with Avalanche" — small text line beneath attribution

### Official assets (in `visuals/elara/brand/`)
- `layer-one-wordmark.png` (1131×133, transparent) — red wordmark, both modes
- `the-block-dark.png` (6554×1000) — white outline variant for dark backgrounds
- `the-block-light.png` (6554×1000) — black solid variant for light backgrounds
- `layer-one-wordmark.svg` — vector source for the LAYER ONE wordmark

### DARK mode
```
Background:       #0A0A0C       (deep editorial dark)
Pattern:          none
Primary text:     #FAFAFA
Secondary text:   #AAAAAA
Emphasis text:    #FF394A       ← OFFICIAL Layer One red (sampled from wordmark)
Accent:           #FF394A
Quote-mark alpha: 75/255
Secondary brand:  THE BLOCK in white (the-block-dark.png)
```

### LIGHT mode
```
Background:       #FCFAF8       (warm off-white)
Pattern:          subtle grid #DCD7D2 @ 100/255 alpha
Primary text:     #0F0F12
Secondary text:   #646464
Emphasis text:    #FF394A       (same red — vivid on cream)
Accent:           #FF394A
Quote-mark alpha: 60/255
Secondary brand:  THE BLOCK in black (the-block-light.png)
```

**Attribution prefix:** `Layer One · ` (prepended to sub-attribution lines)
**Collaboration line:** `in collaboration with Avalanche` (rendered below attribution)

### Status
✓ All required assets sourced and live in `brands/layer_one.py`.
✗ Avalanche logo not currently used as an image — only credited as text. If we
  ever need it for chart-level co-branding, source the PNG and add it.

---

## Brand Override: The Block

For The Block editorial — articles, news graphics, social shares.
**⚠ same PLACEHOLDER caveat as Layer One.**

### DARK mode
```
Background:       #08080A
Pattern:          none
Primary text:     #FCFCFC
Secondary text:   #AFAFAF
Emphasis text:    #E1322D       (signature red)
Accent:           #E1322D
Quote-mark alpha: 80/255
```

### LIGHT mode
```
Background:       #FFFEFC
Pattern:          subtle grid #D7D2CD @ 100/255 alpha
Primary text:     #0C0C10
Secondary text:   #5F5F5F
Emphasis text:    #B91E19
Accent:           #B91E19
Quote-mark alpha: 65/255
```

**Wordmark:** `THE BLOCK` — sans-serif bold, accent color.
**Attribution prefix:** `The Block · `

### TO SOURCE
1. Official The Block logo PNG
2. Confirmed brand red hex value
3. Approved typography preferences

---

## How to Select the Right Brand

The brand always matches the content's owner / publisher. Never default to the
brand we worked on most recently.

| Content type | Brand to apply |
|---|---|
| Elara protocol post, Elara research, Elara end-of-thread | `elara` |
| Layer One podcast quote, episode hero, host clip | `layer_one` |
| The Block article hero, news headline, market piece | `the_block` |
| Cross-published content | use the originating publication |
| Guest's own content republished | guest's brand (or neutral if unknown) |

If the brand for given content is unclear, **ask the user before generating**.
Cite this section's table when explaining the choice.

---

## Layout Rules

**Title block** (top-left, always present):
- Line 1: headline — 34–40px, font-weight 700, #F0F4F8
- Line 2: subtitle — 16–18px, #8895A7
- Divider line below at #1E2D42

**Chart area**: starts 140px from top, 80px margins left/right

**Footer** (bottom, always present):
- Left: `Source: [Platform] ([Year])` — 13px, #4B5563
- Right: account or protocol name — 14px, bold, #3B82F6

**Padding**: 64px left/right/top minimum · 38px bottom minimum above footer
**Footer zone**: last 38px of canvas — source attribution left, brand mark right
**Minimum font size**: 13px for attribution · 14px for all other labels · never smaller
**Minimum element gap**: 16px between any two elements · 32px between sections

---

## Chart Types and When to Use Them

### Horizontal Bar Chart
Use for: comparing magnitudes across categories
Rule: bars left-aligned from a shared axis. Widths proportional to value.
The most important bar is always the bottom one — the visual reads top to bottom.
Label the value at the end of each bar, outside the bar if it fits.

### Area / Line Chart
Use for: showing growth over time
Rule: one clear line or filled area. Label key milestones directly on the chart
(not in a legend). Show start and end values prominently.
Avoid gridlines — use only the axis baseline.

### Segmented Horizontal Bar
Use for: showing parts of a whole (breakdown of $X total)
Rule: single bar spanning full width, segmented by category.
Each segment labeled with category name and value.
Largest segment leftmost.

### 3-Column Comparison Grid
Use for: comparing architectures, protocols, or options side by side
Rule: 3 columns, 4–5 rows max. Column headers are the options.
Row headers are the attributes. Use accent color for the "best" column.
Keep cell text to one line.

### Layered Stack Diagram
Use for: showing hierarchy, flow, or who-captures-what
Rule: 3–4 boxes stacked vertically. Top = highest capture layer.
Directional arrows between boxes. One-line description per box.
Highlight the winning layer with accent color.

### Stat Card
Use for: single number that needs context
Rule: large central number (72–96px), context text below (20–24px),
source attribution bottom. Works as a square (675x675) or landscape.

---

## Attribution Rules (Non-Negotiable)

Every visual must cite its source. No exceptions.

Format: `Source: [Platform name] ([Year]) · [brief methodology note]`

Where the data comes from determines what note is needed:

| Source | Required note |
|---|---|
| DeFiLlama | "TVL / supply data, [date accessed]" |
| Artemis Analytics | "Adjusted volume methodology" |
| Token Terminal | "Protocol revenue excl. LP fees" |
| Blockchain Capital | "Via [article title], [author]" |
| RWA.xyz | "Distributed asset value, [date]" |
| Own calculation | "Calculated from [source A] / [source B]" |

If the data is estimated or projected, add "est." to the label on the chart.
If the data is older than 6 months on a fast-moving metric, add the date.

---

## Visual Spec Format

When producing a visual spec alongside tweet copy, use this format:

```
---
Visualization:
Type: [horizontal bar / area chart / segmented bar / comparison grid / stack diagram / stat card]
Title: "[headline that appears on the visual]"
Subtitle: "[subtitle line]"
Data:
  - [Label 1]: [Value 1]
  - [Label 2]: [Value 2]
  - [Label 3]: [Value 3]
Source: [Platform] ([Year])
Note: [methodology note if needed]
Brand: [account name, bottom-right]
File: [suggested filename].svg
Size: 1200x675
---
```

---

## What Makes a Visual Fail

- Title that describes the chart ("Bar chart of stablecoin velocity") instead of
  making the argument ("The Onchain Dollar Works 87x Harder")
- Legend instead of direct labels — the reader should never have to cross-reference
- Color used decoratively rather than to encode meaning
- More than 5–6 data series — simplify or split into multiple visuals
- Missing attribution — always source the data
- Projected values labeled as facts — always mark estimates
- Text too small to read in a Twitter thumbnail — minimum 18px for labels

---

## Pairing Copy and Visuals

The tweet copy and the visual should not say the same thing twice.

**Copy job**: interpret the data. State the insight and implication.
**Visual job**: prove the claim. Show the numbers that make the copy undeniable.

If the visual already communicates the number clearly, the tweet copy does not
need to repeat it. The copy adds the layer of interpretation.

Example:
- Visual: bar chart showing 1.4x, 40x, 122x
- Copy: "The onchain dollar is never sitting still. That velocity is why CLMM yield works."
- Not: "Stablecoins have 122x velocity as shown in the chart above."

---

## Loading This File

Load for every request that involves:
- A chart or dashboard being converted into a tweet or thread
- A data-heavy thread where at least one tweet carries a number
- An article or newsletter piece citing on-chain metrics
- Any content-plan entry where the format includes a visual attachment

Always load alongside `style/voice-data.md` and `style/voice-base.md`.

**If the visual contains text** (quote cards, end-of-thread visuals, banners with
copy, hero artwork with headlines, charts with labels), also load
`style/voice-typography.md` — it codifies the safe-area and auto-fit rules
that prevent text overflow/bleed.
