# PMN templates — Figma is the source of truth

Templates are **auto-layout components in Figma**; this folder holds their
**generated manifests** (the code-side contract). Brand assets are **Figma
Variables** (`Brand` collection, one mode per show). The render pipeline fills a
template with episode/market data and exports the asset.

```
Figma component (visual SoT)  ──export──▶  templates/<name>.manifest.json (contract)
        ▲                                            │
        │ edit / fine-tune                           ▼
   you, in Figma                         renderer fills slots from data → PNG/SVG
```

## The Figma → code loop

A **pure visual edit** in Figma (move, restyle, re-space) needs nothing here —
Figma renders it next run. Only a **contract change** (slot added/renamed/removed,
a token rebinding, a new brand mode, a new list) requires a re-export:

1. Edit the component in Figma. New slot? name it `#path` / `@path` and annotate
   its binding (shared plugin data, namespace `pmn`: `bind`, `kind`, `format`,
   `transform`, `reflow`, `scale`).
2. Run `tools/export_manifest.js` (paste into a `use_figma` call; see its header).
3. Commit the regenerated `templates/<name>.manifest.json`.

The manifest is generated — **do not hand-edit it.**

## v3 architecture (current)

- **Shared chrome.** Every card instances a `Header` + `Footer` component (the real Block /
  Polymarket / show logos + the accent-tab hairline). One edit propagates to all cards.
- **Background is a component** (`Background` variant set: Gradient · Solid · Glow · Image), placed
  as the card's bottom layer. Its gradient stops bind to `color/field/*`, so the field reskins on
  the brand-mode switch (no code-set). The Image variant has an `@bg.image` slot for textures/photos.
- **Brands are modes** of the `Brand` variable collection (PMN, Demo, …). Adding a sub-brand = add a
  mode and fill its token column; swap logos via `brands.json`. Component names are brand-neutral.
- **Tokens mirror to code** via `tools/export_tokens.js` → `tokens.json`; the **Brand System board**
  on the Foundations page is the visual control surface (swatches bound to the live variables).

## Slot convention (the contract)

Slots are nodes named `#…` (content) or `@…` (geometry). Each carries its data
binding as shared plugin data (namespace `pmn`: `bind`, `kind`, `format`,
`transform`, `reflow`, `scale`). The renderer dispatches on `kind`:

| `kind` | Node | What the renderer does |
|--------|------|------------------------|
| `text` | `#…` text | sets `characters` from `bind` (+ `format`/`transform`) |
| `bar` | `@…` rect | width = `bind`/100 × track (or `scale: ratio-of-max` for lists) |
| `arc` | `@…` ellipse | sweeps the donut arc proportional to `bind` |
| `linechart` | `@…` frame | draws gridlines + area + polyline from a `bind` series |
| `image` | `@…` rect/ellipse | photo well — bytes placed via `upload_assets` (see below) |
| `logo` | `#…` instance | real logo component; renderer swaps it per brand (after detaching the shared chrome) |
| `delta` | `#…` frame | container with `tri.up`/`tri.down` triangle **shapes** + a `val` text; renderer shows the right triangle and colors the value green/red by the **sign** of the bound number |
| `field` | (none in v3) | v3 binds the Background's gradient stops to `color/field/*`, so it reskins via the brand mode. legacy v2 used a code-set `field` node |
| `brand-content` | `#…` text | (legacy v2) per-brand text; v3 uses real logos instead |
| `pmn:list` | frame | repeating list; declares its row component in `pmn:list-item`. Renderer clones **and detaches** each row (instance sublayers can't be resized) |

Reflow is automatic: every template is auto-layout, so text length and
list length resize the panel and re-center the column (within reason).

### Images (photos)

The Figma plugin sandbox here **cannot fetch URLs** (`createImageAsync` is
unavailable). So the photo flow is: the data carries a URL → the **orchestration
layer** (agent/Python) fetches the bytes → POSTs them to an `upload_assets`
submitUrl bound to the `@photo` node. `renderCard` returns each image slot's
node id + url so the caller knows where to upload.

## Render flow (on-demand / agent-triggered)

`tools/render.js` is the generic engine — `renderCard(manifest, ctx, brand, pos)`:

1. Read `<name>.manifest.json` + the fill data (`card` data often from `lib/pmn_live.py`).
2. Instantiate + detach the component; set the brand mode; code-set the gradient field.
3. Fill each slot by `kind` (text/bar/arc/linechart/list); lists clone the row component per item.
4. For `image` slots, fetch the URL bytes (orchestration) and `upload_assets` them onto the returned node ids.
5. Export PNG/SVG. The filled frame stays in Figma — open it to fine-tune.

## Templates

Data cards: `binary`, `leaderboard` (variable-length list), `divergence`,
`gauge` (arc), `hero-quote`, `timeseries` (linechart).
Social cards: `guest-announce` (photo), `quote`, `episode` (photo), `cover`.
Each has a generated `<name>.manifest.json`. `binary.example.json` shows a fill input.

## Tools

- `tools/export_manifest.js` — Figma → manifest (the reverse loop)
- `tools/render.js` — manifest + data + brand → filled asset
