# PMN — Figma↔code pipeline · session handoff

**Status:** the code↔Figma pipeline is **built and proven end to end**. The 10 card
templates in Figma are **proofs-of-concept** — the *next session redesigns the
visuals from first principles*. The pipeline, tokens, logos, exporter, and
renderer are the keepers.

Branch: `dq/live-data-adapter` (on fork `dqbuilds`). **Uncommitted** as of this handoff.

---

## The Figma file

[PMN Design System — Tokens + Components](https://www.figma.com/design/ILPUHPFyGRtLnc0JJ6lGyW) · fileKey `ILPUHPFyGRtLnc0JJ6lGyW`

Pages: **📖 Read Me** (start here) · **🎨 Foundations** (tokens + logos) ·
**🧩 Components** (templates) · **🖼 Renders (proofs)**.

### Component node ids (Components page)
| Template | nodeId | manifest |
|---|---|---|
| Binary | `8:2` | binary |
| Leaderboard Row (atom) | `14:68` | — |
| Leaderboard | `15:68` | leaderboard |
| Divergence | `23:133` | divergence |
| Gauge | `24:133` | gauge |
| Hero-Quote | `28:133` | hero-quote |
| Timeseries | `29:133` | timeseries |
| Guest-Announce | `36:133` | guest-announce |
| Quote | `45:181` | quote |
| Episode | `46:181` | episode |
| Cover | `47:181` | cover |

### Logos (Foundations page) + Brand collection
The Block `35:143` · Polymarket `35:147` · PMN `35:148` · Demo News `49:192` ·
Acme `49:194` · Demo `49:196`. Brand variable collection: `VariableCollectionId:7:2`
(modes **PMN**, **Demo**). Ids are recorded in `templates/brands.json`.

---

## The loop (both directions)

```
Figma component  ──[ tools/export_manifest.js ]──►  templates/<name>.manifest.json
manifest + data + brand  ──[ tools/render.js ]──►  filled asset (PNG) in Figma
```

- **Edit a component visually → no code change** (Figma renders it next run).
- **Add/rename a slot or rebinding → re-run the exporter → commit the manifest.**

Both engines are plain Plugin API scripts: paste the file into a `use_figma` call
and append the documented call (see each file's header). On-demand / agent-driven —
no headless infra (matches the chosen automation level).

### Run the exporter
Paste `tools/export_manifest.js`, then:
`return await exportManifest("<nodeId>", "<template-name>", "ILPUHPFyGRtLnc0JJ6lGyW")`
→ write the result to `templates/<name>.manifest.json`.

### Run the renderer
Paste `tools/render.js`, then:
`return await renderCard(MANIFEST, { card:{…}, brand:{…logos…} }, "PMN", { x, y })`
`card` data often comes from `lib/pmn_live.py`. For `image` slots, fetch the URL
bytes in the orchestration layer and `upload_assets` them onto the returned node ids.

---

## Conventions

- **Slots:** nodes named `#text` / `@geometry`, bindings in `pmn` shared plugin data
  (`bind`, `kind`, `format`, `transform`, `reflow`, `scale`).
- **Kinds:** `text · bar · arc · linechart · image · logo · list` (+ `field` gradient).
- **Brand:** templates bind to role tokens (`color/accent`, `font/display`…); a render
  sets the brand **mode** (reskins solids+fonts), code-sets the gradient field, and
  swaps **logos** per `templates/brands.json`.
- **Auto-layout everywhere** → text length + list length reflow within reason.

---

## Repo

- `lib/pmn.py` — original design tokens/components (Kelvin's kit; source of token values)
- `lib/pmn_live.py` — live market data (Polymarket/Hyperliquid) → card dicts, cached fallback
- `tools/export_manifest.js` — Figma → manifest
- `tools/render.js` — manifest + data + brand → asset (9 fill kinds)
- `templates/` — 10 `*.manifest.json`, `brands.json`, `README.md`, `binary.example.json`
- `episode-01/_robostrategy.py` — original generator, wired to `pmn_live` (the pull→render proof)

---

## Proven this session
Live data fill (binary, leaderboard, timeseries) · brand reskin (PMN↔Demo) ·
auto-layout reflow (long headline, 3↔5 rows) · arc + linechart geometry from data ·
real photo via `upload_assets` · per-brand logo swap. See the Renders page.

## Known limitations (deferred to the design overhaul)
1. **Shared shell** — chrome/field/footer are duplicated per template (clone pattern).
   Make a shared shell component so all cards share one chrome (and all use real logos —
   currently only social cards + cover do; data cards still use text chrome).
2. **▲/▼ glyphs** drop on render (symbol-font fallback). Replace with triangle *shapes*,
   which also enables **sign-driven color** (delta/stat auto red/green) — currently fixed per template.
3. **Cover show-wordmark** is static art (per-show variant needed for true multi-brand covers).
4. Gauge arc, line chart, and bar widths are **code-set** (Figma can't bind those to variables) —
   correct, just know they live in the renderer, not as pure variable bindings.

## Next session
Design overhaul of the template **visuals** from first principles, building on this
pipeline. Keep: the pipeline (export/render), Brand tokens + modes, logo components +
swap, the slot convention. Redesign: the card layouts themselves (these 10 are POCs).
Knock out limitation #1 early (shared shell) — it removes #2's per-template duplication too.
