# AGENTS.md — operate the PMN Figma↔code pipeline

This repo produces **Prediction Market News** social cards through a **Figma-native,
manifest-driven** pipeline. Figma is the source of truth for visuals; the repo holds the
generated contract (`templates/*.manifest.json`, `tokens.json`) and the two engines that move
data between them. Humans: see [`GUIDE.md`](GUIDE.md).

> The legacy SVG kit (`lib/pmn.py` SVG helpers, `data-viz/`, `social/`, `episode-01/_*.py`) is
> **superseded** by this Figma pipeline. `lib/pmn_live.py` (live market data → card dicts) is still
> the data source. Old Figma pages (v2 Components/Renders) were removed.

Figma file: `ILPUHPFyGRtLnc0JJ6lGyW` · Pages: **📖 Read Me**, **🎨 Foundations**, **🧩 Components**.

---

## 1. Mental model

```
Figma component  ──[ tools/export_manifest.js ]──►  templates/<name>.manifest.json   (the contract)
manifest + data + brand  ──[ tools/render.js ]──►  filled card (PNG) back in Figma
Figma variables  ──[ tools/export_tokens.js ]──►  templates/tokens.json              (token mirror)
```

- A card is a **component** = a `Background` instance + a `Header` + content + a `Footer`, all bound
  to **Brand** tokens. **Brands are MODES** of the `Brand` variable collection (PMN, Demo, …).
- Slots are nodes named `#…` (content) / `@…` (geometry) carrying `pmn` shared plugin data
  (`bind·kind·format·transform·scale·reflow`). The renderer dispatches on `kind`.
- All three tools are plain Plugin API scripts: **paste the file into a `use_figma` call** (load the
  `figma-use` skill first) and append the documented call. On-demand, no headless infra.

## 2. Running the tools

**Render a card** (run on the 🧩 Components page so the Row component resolves):
```js
const M = /* templates/<name>.manifest.json */;
const ctx = { card: {/* §5 schema */}, brand: { logos: { publisher:{id}, sponsor:{id}, show:{id} } } };
return await renderCard(M, ctx, "PMN", { x, y });   // returns { nodeId, imageSlots, shot }
```
For `image` slots: take the returned `imageSlots[].nodeId`, fetch the URL bytes in the orchestration
layer, and `upload_assets` them onto that node (the sandbox can't fetch URLs).

**Export a manifest** (after a contract change): set the page to 🧩 Components, then
`return await exportManifest("<componentNodeId>", "<name>", "ILPUHPFyGRtLnc0JJ6lGyW")` → write
`templates/<name>.manifest.json`.

**Export tokens** (after a colour/token change): `return await exportTokens()` → write `templates/tokens.json`.

## 3. Slot kinds (how the renderer fills each)

| kind | node | renderer behaviour |
|---|---|---|
| `text` | `#…` | sets `characters` from `bind` (+ `format`/`transform`) |
| `bar` | `@…` rect | width = `bind`/100 × track, or `scale:ratio-of-max` for lists |
| `arc` | `@…` ellipse | sweeps the donut `arcData` proportional to `bind` |
| `linechart` | `@…` frame | draws gridlines + area + polyline from a `[[label,value]…]` series |
| `delta` | `#…` frame | shows `tri.up`/`tri.down` shape + colours `val` green/red by the **sign** of `bind` |
| `image` | `@…` rect/ellipse | photo well — returns node id for out-of-band `upload_assets` |
| `logo` | `#…` instance | `swapComponent` to the brand's logo (`bind` = `brand.{publisher\|sponsor\|show}`) |
| `list` | frame | clears + clones a Row (`pmn:list-item`) per `bind` item; **detaches each clone** |

## 4. v3 architecture specifics (already wired — don't re-introduce the old assumptions)

- **Shared chrome:** `Header`/`Footer` are nested instances tagged `pmn:role=chrome`. The exporter
  reads *through* them (transparent roles: `chrome|background|showmark`); the renderer **detaches**
  them after the top-level detach so logos swap and `#source` fills.
- **Field:** the `Background` instance's gradient stops are **bound to `color/field/*`** → it reskins
  on the brand-mode switch. There is **no code-set `field` node** (manifest `field` is `null`).
- **Lists:** instance sublayers can't be resized, so the renderer **clones AND detaches** each Row
  before filling (this is why v2's bars looked uniform — that bug is fixed).
- **Fonts:** Inter weights are limited to **Bold / Medium / Black** (Roboto, used by the Demo mode,
  lacks Extra/Semi Bold) so brand-font-swap never hits a missing style. Numbers use **IBM Plex Mono**.

## 5. Per-template `card` data schema

```
binary       { tag, question, outcomes:[{label,pct},{label,pct}], source }
leaderboard  { tag, question, rows:[{name, value, mag}], source }                 # mag drives ratio-of-max bars
divergence   { tag, question, left:{label,delta,detail,sub}, right:{…}, caption, source }   # delta is a signed number
gauge        { tag, question, pct, label, source }
timeseries   { tag, question, current, delta, series:[[label,value]…], source }
quote        { tag, quote, attrib, attribSub, source }
hero-quote   { tag, quote, attrib, attribSub, stat:{label,value,sub}, source }
cover        { tag, subtitle, source }
guest-announce { tag, photo:<url>, guest:{name,role,company}, source }
episode      { tag, question, guest:{photo:<url>, name, role}, source }
```
Every card also fills chrome from `ctx.brand.logos` (publisher/sponsor/show) and `#source` from `card.source`.

## 6. Tests
`python3 tools/test_pmn.py` — validates all manifests, `tokens.json`, `brands.json`, and that the
renderer supports every slot kind in use. **Run after every re-export and before committing.**

## 7. Conventions
- Manifests + `tokens.json` are **generated — never hand-edit.** Re-run the exporters.
- Component names are **brand-neutral** (`Card / Binary`, `Header`, `Background`). Brands are modes.
- Voice for any copy: sharp, analytical, crypto-native, concise. No em-dashes, buzzwords, or emojis.
- Every card is dated via `card.source`. Re-pull data if stale (`lib/pmn_live.py`).
