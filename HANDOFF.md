# PMN — Figma↔code pipeline · session handoff (v3)

**Status:** the design overhaul is **built and verified end to end**. All 10 card
templates were redesigned from first principles on a shared, multi-brand system,
the two engines were wired to it, the manifests were re-exported, and a live-data
render was confirmed (binary, leaderboard, divergence). The pipeline, tokens,
logos, exporter, and renderer are all current.

Branch: `main` (committed + pushed). Legacy pages wiped; human/agent docs + contract tests added; the file is organized for delivery (📖 Read Me · 🎨 Foundations · 🧩 Components).

---

## The Figma file
[PMN Design System](https://www.figma.com/design/ILPUHPFyGRtLnc0JJ6lGyW) · fileKey `ILPUHPFyGRtLnc0JJ6lGyW`

Pages: **📖 Read Me** (`108:2`) — the human guide · **🎨 Foundations** (`52:195`) — tokens, logos,
**Brand System board** (`73:2`) · **🧩 Components** (`60:2`) — ① Card Templates (the 10 cards) +
② Building Blocks (Header, Footer, Background, Delta, Row, Scaffold). Legacy v2 pages were deleted.

### v3 component node ids (page 🧩 Components)
| Component | nodeId | notes |
|---|---|---|
| Header | `60:3` | shared chrome: Block + Presented-by-Polymarket + accent-tab rule |
| Footer | `61:13` | shared chrome: PMN show mark + source + accent-tab rule |
| Background (set) | `67:44` | variants Gradient `67:40` · Image `67:41` · Solid · Glow |
| Delta | `79:40` | up/down triangle shapes + mono value (sign-driven) |
| Row / Leaderboard | `79:44` | list row (renderer clones + detaches it) |
| Card / _Scaffold | `86:92` | bg + header + content(topBlock) + footer — clone to start a card |
| Card / Binary | `62:14` | |
| Card / Leaderboard | `80:40` | |
| Card / Divergence | `84:66` | |
| Card / Gauge | `86:137` | |
| Card / Timeseries | `89:144` | |
| Card / Quote | `91:170` | |
| Card / Cover | `93:196` | |
| Card / Guest-Announce | `94:222` | |
| Card / Hero-Quote | `96:248` | |
| Card / Episode | `97:274` | |

### Logos (Foundations) + Brand collection
Block `35:143` · Polymarket `35:147` · PMN `35:148` · Demo News `49:192` · Acme `49:194` · Demo `49:196`.
Recorded in `templates/brands.json`.

---

## The design system (what's new in v3)

**Foundations / tokens** (all in Figma Variables, mirrored to `templates/tokens.json`):
- **Brand** collection — one **mode per brand** (PMN, Demo). 17 tokens: `color/field/{start,mid,end}`,
  `color/{accent,accent-weak,panel-bg,surface,track,hairline,text,muted,eyebrow-ink,up,down}`,
  `font/{display,body,mono}`. **Adding a sub-brand = add a mode + fill its column.**
- **Layout** collection (single mode) — `space/*`, `radius/*`, `stroke/hairline` (the grid).
- Type: Inter (display/body) + **IBM Plex Mono** (numbers). Weights are limited to **Bold/Medium/Black**
  on the Inter side because Roboto (Demo mode) lacks Extra/Semi Bold — keeps brand-font-swap safe.

**Design language:** numbers-first, broadcast-grade. Signature device = an **electric-blue accent-tab
hairline** under the header / above the footer + **mono tabular figures** + **sign-colored delta
triangles** + a **LIVE pill** on live-data cards. Green/red are reserved for *signed* values only.

**Multi-brand UX (do this, not a rebuild later):**
- Brands are **modes**, component names are **brand-neutral** (Header, Background, Card / X).
- **Background is a component** (variant set) so each brand can drop textures/photos/overlays.
- The **Brand System board** (`73:2`, Foundations) shows each brand as a column of swatches bound
  to the live variables — the control surface. Edit a variable → board + every card updates.
- **Code tracks tokens**: `tools/export_tokens.js` → `templates/tokens.json` (re-run after color edits).

---

## The loop (both directions) — unchanged contract, updated mechanics
```
Figma component  ──[ tools/export_manifest.js ]──►  templates/<name>.manifest.json
manifest + data + brand  ──[ tools/render.js ]──►  filled asset (PNG) in Figma
```
Slots are still nodes named `#…`/`@…` carrying `pmn` shared plugin data
(`bind·kind·format·transform·scale·reflow`). Kinds: `text · bar · arc · linechart ·
image · logo · delta · list`.

**v3 engine specifics (already wired):**
- **Shared chrome** (Header/Footer) are nested instances tagged `pmn:role=chrome`. The exporter
  reads *through* them (roles `chrome|background|showmark` are transparent); the renderer
  **detaches** them after the top-level detach so logos swap and source fills.
- **Field** = a Background instance with gradient stops **bound to `color/field/*`** → it reskins on
  the brand-mode switch. No code-set field (manifest `field` is null).
- **Lists** declare their row component in `pmn:list-item`; the renderer **clones AND detaches** each
  row (instance sublayers can't be resized — this is why v2's bars looked uniform).
- **delta** kind: container holds `tri.up`/`tri.down` vector triangles + `val`; the renderer toggles
  the triangle and colors the value green/red by the sign of the bound number.

### Run the exporter
Paste `tools/export_manifest.js`, set the page to **🧩 PMN v3**, then:
`return await exportManifest("<nodeId>", "<name>", "ILPUHPFyGRtLnc0JJ6lGyW")` → write `templates/<name>.manifest.json`.

### Run the renderer
Paste `tools/render.js` (on the **🧩 PMN v3** page so the Row component is found), then:
`return await renderCard(MANIFEST, { card:{…}, brand:{ logos:{ publisher:{id}, sponsor:{id}, show:{id} } } }, "PMN", { x, y })`.
`card` data from `lib/pmn_live.py`. For `image` slots, fetch the URL bytes and `upload_assets` onto the returned node ids.

---

## Repo
- `lib/pmn.py` — original token values (source) · `lib/pmn_live.py` — live market data → card dicts
- `tools/export_manifest.js` — Figma → manifest (v3: transparent chrome/bg, list-item) 
- `tools/render.js` — manifest + data + brand → asset (v3: chrome-detach, row clone-detach, delta kind)
- `tools/export_tokens.js` — Figma variables → `templates/tokens.json`
- `tools/test_pmn.py` — contract tests (manifests · tokens · brands · renderer kinds): `python3 tools/test_pmn.py`
- `templates/` — 10 v3 `*.manifest.json` (version 0.3), `tokens.json`, `brands.json`, `README.md`
- `GUIDE.md` (humans) · `AGENTS.md` (agents) — make cards / brands / templates + keep code in sync

## Verified this session
All 4 of DQ's directives (brand package + code tracking; background-as-component; multi-brand UX;
rebalanced composition). 10 redesigned cards. Live render of binary / leaderboard / divergence
(reflow, proportional bars incl. the list path, sign-driven deltas, logo swap, brand reskin PMN↔Demo).

## Next session (polish + extend)
1. **Expose logos as INSTANCE_SWAP props** on Header/Footer for in-Figma per-brand preview (render
   swap already works via brands.json). Add a 3rd brand mode to stress-test N-brand.
2. **Multi-format**: cards are 1:1 (1080). Add 9:16 / 16:9 / 4:5 variants (content is auto-layout;
   the shell ports — mostly a canvas + margin change).
3. Wire `lib/pmn_live.py` data shapes to the v3 card dicts and add a thin orchestration script that
   pulls → renders → exports PNGs (the `episode-01/_*.py` generators target the old SVG kit).
4. Optional: real photo on guest-announce/episode via `upload_assets`; per-show cover wordmark as a
   swappable component.
