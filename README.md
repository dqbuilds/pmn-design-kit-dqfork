# PMN Design Kit

Multi-brand social-card system for **Prediction Market News** — The Block × Polymarket.
Card visuals live as components in one Figma file; this repo holds a **code↔Figma
pipeline** that fills those components with live data and exports finished assets.
**Brands are modes** — one design system, many shows.

> **v3 (current).** The card system was rebuilt in Figma with a manifest-driven render
> pipeline. The legacy SVG kit (`lib/pmn.py` SVG helpers, `data-viz/`, `social/`,
> `episode-01/_*.py`) is **superseded** and kept only for reference. `lib/pmn_live.py`
> (live market data → card dicts) is still used.

---

## The two halves

**Figma** — file `ILPUHPFyGRtLnc0JJ6lGyW`. Pages:
- **📖 Read Me** — the in-Figma human guide (mirrors this repo's docs)
- **🎨 Foundations** — the Brand System board (every brand's colours/type/logos as live swatches) + the logo components
- **🧩 Components** — ① **Card Templates** (the 10 cards) and ② **Building Blocks** (Header, Footer, Background, Delta, Row, and the Scaffold you clone to start a new card)

**Repo** — the engines + the generated contract:

| Path | What |
|---|---|
| `tools/render.js` | manifest + data + brand → filled card (PNG) in Figma |
| `tools/export_manifest.js` | Figma component → `templates/<name>.manifest.json` |
| `tools/export_tokens.js` | Figma variables → `templates/tokens.json` |
| `tools/test_pmn.py` | contract tests — run after any re-export |
| `templates/` | generated manifests, `tokens.json`, `brands.json` (do not hand-edit the first two) |
| `lib/pmn_live.py` | live Polymarket/Hyperliquid data → card dicts |

**Docs:** [`GUIDE.md`](GUIDE.md) (humans — make a card / brand / template, update code) ·
[`AGENTS.md`](AGENTS.md) (agents — run the pipeline, slot kinds, per-template data schemas) ·
[`FIGMA.md`](FIGMA.md) (file link + node-id map + repo mapping) · [`HANDOFF.md`](HANDOFF.md).

---

## Brands are modes

Everything brand-specific (colours, fonts, field gradient, accent) is a token in the
**`Brand`** variable collection, with one **mode per brand** (PMN, Demo, …). Components
bind to tokens — nothing is hard-coded — so switching a frame's mode reskins it entirely.

**Switch a card's brand in Figma:** select the card → right panel → **Appearance** section
→ the **`Brand`** dropdown (just under *Opacity* / *Corner radius*) → pick **PMN** or **Demo**.

- It reads **"Mixed"** on a whole card because the nested Background / Header / Footer
  instances each carry their own mode; picking a brand from the dropdown forces the whole
  selection to that brand.
- It is **not** in the right-click menu (Figma moved per-layer modes into the Appearance panel).
- Select **multiple cards** (or the Section) first to flip them together.

**Switch the brand for an output (render):** you don't touch Figma at all —
`renderCard(manifest, ctx, "Demo", pos)` sets the mode on the rendered frame. The in-Figma
dropdown is only for previewing.

---

## Quickstart — render a card

Paste `tools/render.js` into a `use_figma` call (run it on the 🧩 Components page so the Row
component resolves), then:

```js
const M = /* paste templates/binary.manifest.json */;
const ctx = { card: { /* the card's data — see AGENTS.md §5 */ },
              brand: { logos: { /* publisher/sponsor/show ids from brands.json */ } } };
return await renderCard(M, ctx, "PMN", { x: 0, y: 9000 });
```

For photo cards, upload the image bytes onto the returned image-slot node id (`upload_assets`).
Validate the contract any time with `python3 tools/test_pmn.py`.

---

## Working together: designer ↔ analyst

The whole point of this kit is that a **Figma-native designer** and a **data analyst** can
each work in their own tool and hand off through one shared contract:
`templates/*.manifest.json` + `tokens.json` (both **generated — never hand-edited**).

### Designer → Analyst  ("here's a template you can run with data")

You work in **Figma**: design and refine the card layouts, the brand tokens, and the Brand
System board. To hand a template off so an analyst can fill it with data without ever opening Figma:

1. **Build / edit the card in Figma.** New card type? Duplicate **Scaffold** (it already has
   Background + Header + Footer). Keep colours bound to **Brand** tokens and fonts to the font
   tokens — that's what makes it reskin per brand.
2. **Name + tag every data-driven node.** Each value the analyst will fill is a node named
   `#slot` (text) or `@slot` (geometry) carrying `pmn` plugin data: **`bind`** (the data path,
   e.g. `card.outcomes.0.pct`), `kind`, `format`. This naming **is** the contract.
3. **Re-export the contract.** Run `tools/export_manifest.js` for the component (and
   `export_tokens.js` if you changed colours) — or ask an agent to — then **commit**
   `templates/<name>.manifest.json`.
4. **Tell the analyst the data shape.** Point them at the slot `bind` paths (or `AGENTS.md` §5,
   which lists the `card` schema per template).

> **Golden rule:** pure *visual* edits (move, restyle, re-space, swap a Background variant)
> need **no** handoff — the renderer reads the component live. Only a **contract change**
> (slot added / renamed / removed, a new binding, a new brand mode, a new list) requires a
> re-export + commit.

### Analyst → Designer  ("I need a layout change")

You work in **code/data**: pull numbers (`lib/pmn_live.py`), shape them into the per-template
`card` dict, pick a brand, and render via `tools/render.js`. When you hit something that's a
**layout/visual** problem rather than a data problem:

1. **Don't hack it in code.** The visuals live in Figma — editing the renderer to nudge pixels
   will be wiped next redesign.
2. **Write the designer a tight request:** which template, what should change, and — if you
   need a *new* number surfaced — the **exact data field** (the `bind` path) plus an example
   value. Attach a render that shows the problem.
3. The designer edits the Figma component. If they added/renamed a slot, they re-export the
   manifest; you `git pull` and re-render. Tokens changed? `tokens.json` updates too.

> **Golden rule:** if it's about *how a number is computed or which data shows*, that's you
> (data + manifest `bind`). If it's about *how it looks, the layout, or a brand-new slot*,
> that's the designer (Figma + re-export).

**Neither side hand-edits `*.manifest.json` or `tokens.json`** — they're regenerated from
Figma by the exporters. Run `python3 tools/test_pmn.py` before committing to catch a broken
contract (unknown slot kind, missing bind, a list with no row component, a token a card needs
that a brand mode is missing).

---

## Make a brand / card / template

Full steps in [`GUIDE.md`](GUIDE.md). Short version:
- **New brand** → add a **mode** to the `Brand` collection, fill its colours/fonts (eyeball on
  the Brand System board), add its 3 logos to `brands.json`, run `export_tokens.js`.
- **New card (post)** → copy a template, edit text/numbers, switch brand, **Export → PNG** — or
  `renderCard(..., brand, ...)` with live data.
- **New template** → duplicate **Scaffold**, build content, name `#`/`@` slots + tag them, run
  `export_manifest.js`.

---

## Broadcast & legacy assets

The card *generators* are superseded by the Figma pipeline above, but the repo also holds
production assets and the original SVG kit, kept for reference:

- **`frames/`** — static 1920×1080 on-air **broadcast frames** (Single / Two / Three / Four-cam
  + market overlay) and **lower-thirds** name chips. These are design exports, not
  code-generated — see `frames/README.md`. (`lib/pmn.py` still has `chrome()` + `name_chip()`
  if you ever build a frame generator.)
- **Legacy SVG generators** (superseded for cards): `lib/pmn.py`, `data-viz/`, `social/`,
  `episode-01/_*.py`, and `_podcast_covers.py` (show cover art — both PMN logos × 4
  backgrounds, 1500×1500). `lib/pmn_live.py` (live data) is still used by the current pipeline.

---

## Data sourcing (`skills/market-data/`)

Card numbers come from `lib/pmn_live.py` (cached-fallback live data) and the CLI scripts in
`skills/market-data/scripts/` (only dependency: `requests`; endpoints in
`skills/market-data/references/endpoints.md`):

```bash
cd skills/market-data/scripts
python3 polymarket.py top 10                 # top markets by volume + odds
python3 hyperliquid.py dex xyz 25            # Trade.xyz board by 24h volume
python3 coingecko.py price <id>              # cross-ecosystem price
```

Every card is dated via `card.source` — re-pull if stale.

---

## Setup

The v3 pipeline runs through Figma (the `use_figma` Plugin-API bridge / an agent), so there's
no rasterizer to install. For the data + tests:

```bash
pip install -r requirements.txt     # for lib/pmn_live.py data pulls
python3 tools/test_pmn.py           # contract tests (stdlib only)
```

Type: **Inter** (display/body) + **IBM Plex Mono** (numbers); Roboto stands in for the Demo
brand. Cards are 1080×1080 today (other ratios are a planned add — see `HANDOFF.md`).
