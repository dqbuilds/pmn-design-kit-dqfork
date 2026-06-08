# PMN Design System — Human Guide

A multi-brand social-card system for **The Block × Polymarket**. This guide is for
**humans**. Agents: see [`AGENTS.md`](AGENTS.md). The same instructions live on the
**📖 Read Me** page inside the Figma file.

- **Figma file:** PMN Design System · `ILPUHPFyGRtLnc0JJ6lGyW`
- **Pages:** 📖 Read Me · 🎨 Foundations (Brand System board + logos) · 🧩 Components
  (① Card Templates — the 10 cards · ② Building Blocks — Header, Footer, Background, Delta, Row, Scaffold)

---

## The one idea: brands are *modes*

Everything brand-specific (colours, fonts, the field gradient, the accent) lives in the
**`Brand` variable collection**, with **one mode per brand** (PMN, Demo, …). Components
*bind* to those tokens — nothing is hard-coded — so switching a frame's mode reskins it
entirely. Adding a brand is adding a mode, not rebuilding cards.

Edit colours visually on the **🎨 Foundations → Brand System** board, or in the Variables panel.

**Switch a card's brand in Figma:** select the card → right panel → **Appearance** section →
the **`Brand`** dropdown (just under *Opacity* / *Corner radius*) → pick **PMN** or **Demo**. It
reads *"Mixed"* on a whole card because the nested Background/Header/Footer instances carry their
own modes — picking a brand forces the whole selection. It is **not** in the right-click menu.
Select multiple cards (or the Section) to flip them together. For rendered *outputs* you don't
touch this — `renderCard(…, "Demo", …)` sets the mode on the exported frame.

---

## Make a NEW CARD (a new post)

**By hand (fastest):** on 🧩 Components → ① Card Templates, copy the card that fits (Binary,
Leaderboard, Quote, …). Edit the text/numbers. Switch the brand mode if needed (right panel →
the layer's variable mode). Select the card → right panel → **Export → PNG (1×)**.

**From live data (automated):** the renderer fills a template from a data object. Paste
`tools/render.js` into a `use_figma` call (run it on the 🧩 Components page) and append:

```js
const M = /* paste templates/binary.manifest.json */;
const ctx = { card: { /* the card's data */ }, brand: { logos: { /* from brands.json */ } } };
return await renderCard(M, ctx, "PMN", { x: 0, y: 9000 });
```

Card data shapes come from `lib/pmn_live.py`; the per-template `card` schema is listed in `AGENTS.md`.
For photo cards, upload the image bytes onto the returned image-slot node id (`upload_assets`).

---

## Make a NEW BRAND

1. **Figma → Variables panel → `Brand` collection → add a mode** (e.g. "Acme Show"). Fill its
   colour and font values. The Brand System board updates live, so you can eyeball contrast.
2. **Add the brand's three logo components** (publisher / sponsor / show) to the file. Record
   their node ids in `templates/brands.json` as a new entry (copy the PMN block, swap ids).
   See the `_addBrand` recipe in that file.
3. **Run `tools/export_tokens.js`** and commit `templates/tokens.json`.

That's it — every existing card can now render in the new brand (`renderCard(M, ctx, "Acme Show", …)`).

---

## Make a NEW CARD TEMPLATE

1. On 🧩 Components → ② Building Blocks, **duplicate `Scaffold`** (it already has Background +
   Header + Footer + a centred content area). Rename it `Card / <Name>`.
2. **Build your content** in the centre. Reuse Building Blocks. Bind type to font tokens and
   colours to Brand tokens (never raw hex) so it reskins per brand.
3. **Name + tag the data nodes.** Each value the renderer fills is a node named `#name` (text) or
   `@name` (geometry), with shared plugin data in the `pmn` namespace: `bind`, `kind`, `format`,
   `transform`, `scale`, `reflow`. (See the cheat-sheet below.)
4. **Run `tools/export_manifest.js`** for the new component → commit `templates/<name>.manifest.json`.
5. **Run the tests:** `python3 tools/test_pmn.py`.

---

## After a redesign — keeping code in sync

- **Pure visual edits** (move, restyle, re-space, swap a Background variant) need **nothing** —
  the renderer reads the component live next run.
- **Contract changes** — a slot added / renamed / removed, a changed binding, a new brand mode,
  or a new list — need a **re-export**:
  ```bash
  # re-export the changed template (paste export_manifest.js into use_figma)
  #   → templates/<name>.manifest.json
  # if you changed colours / tokens (paste export_tokens.js)
  #   → templates/tokens.json
  python3 tools/test_pmn.py        # verify the contract still holds
  git add -A && git commit         # commit the regenerated files
  ```
- Manifests and `tokens.json` are **generated — never hand-edit them.**

---

## Slot naming cheat-sheet

| Prefix | Means | Example |
|---|---|---|
| `#name` | text / content node | `#headline`, `#odds.yes.pct` |
| `@name` | geometry node | `@bar.yes`, `@gauge.arc`, `@photo` |

Plugin-data (namespace `pmn`) on each slot: `bind` (data path) · `kind` · `format` (e.g. `{}%`) ·
`transform` (`uppercase`) · `scale` (`ratio-of-max`) · `reflow`.

**Kinds:** `text · bar · arc · linechart · delta · image · logo · list`
- `delta` — a triangle **shape** + number that turns **green/red by sign** (no dropped glyphs).
- `list` — a panel that repeats a Row component; declares its row in `pmn:list-item`.
- `logo` — a real logo component the renderer swaps per brand (binds `brand.publisher|sponsor|show`).
- The field/background reskins automatically via the brand mode (gradient stops bound to `color/field/*`).

---

## Handing off to / from a data analyst

This kit is built so a Figma-native designer and a data analyst each work in their own tool and
hand off through one shared contract: `templates/*.manifest.json` + `tokens.json` (both
**generated — never hand-edited**). The full two-direction workflow is in the
**[README → Working together: designer ↔ analyst](README.md#working-together--designer--analyst)**.

In short:
- **Designer → analyst:** edit the layout in Figma, name/tag the data slots (`#`/`@` + `pmn`
  `bind`/`kind`/`format`), run `export_manifest.js`, commit the manifest. The analyst renders it
  with data — no Figma needed.
- **Analyst → designer:** render with data via `render.js`; when you need a *layout* change or a
  *new* data field surfaced, send the designer the template + the exact `bind` path + an example
  render. They edit Figma and re-export.
- **The split:** *how it looks / a new slot* = designer (Figma + re-export); *which data / how a
  number is computed* = analyst (data + manifest `bind`).

## Tests

`python3 tools/test_pmn.py` validates every manifest, `tokens.json`, and `brands.json`, and checks
the renderer supports every slot kind in use. Run it after any re-export and before committing.
