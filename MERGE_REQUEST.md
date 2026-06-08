# Merge request — PMN Design Kit v3: Figma-native, multi-brand card pipeline

**From:** `dqbuilds/pmn-design-kit-dqfork@dq/figma-pipeline-v3` → **into:** `kls6um/pmn-design-kit@main`

## Summary

Rebuilds the PMN card system around a **Figma-native, manifest-driven render pipeline** and a
**multi-brand** token model (brands = variable *modes*). Card visuals now live as components in
one Figma file; this repo holds a two-way pipeline that exports each component's contract and
renders it back, filled with live data, in any brand. All 10 card types were redesigned from
first principles (numbers-first, shared real-logo chrome, mono tabular figures, sign-driven
delta triangles). The original SVG generator kit is **superseded but kept** for reference.

Nothing in the original kit is deleted; the new system is additive and clearly documented as the
current path.

## Why

The v2 SVG kit hard-coded one brand's chrome as text per card, had no shared chrome, and the
data-viz (e.g. leaderboard bars) didn't encode magnitude. The redesign makes the numbers the
hero, unifies chrome into shared components, and makes the whole system reskin to a new
brand/show by adding a variable mode — not a rebuild.

## What changed

**New — engines (`tools/`)**
- `render.js` — manifest + data + brand → filled card (PNG) in Figma. Handles slot kinds
  `text · bar · arc · linechart · delta · image · logo · list`; detaches shared chrome so logos
  swap; clone-detaches list rows so bars resize (fixes a latent v2 bar bug); sets brand via mode.
- `export_manifest.js` — Figma component → `templates/<name>.manifest.json` (reads through
  chrome/background instances; row component via `pmn:list-item`).
- `export_tokens.js` — Figma variables → `templates/tokens.json` (the code-side token mirror).
- `test_pmn.py` — stdlib contract tests (manifests, tokens, brands, renderer-kind coverage). **7 passing.**

**New — generated contract (`templates/`)**
- 10 manifests (v0.3): binary, leaderboard, divergence, gauge, timeseries, quote, cover,
  guest-announce, hero-quote, episode.
- `tokens.json` — Brand (PMN/Demo modes) + Layout collections, all values/scopes/code-syntax.
- `brands.json` — extended with an `_addBrand` recipe + per-brand logo ids.

**New — design system in Figma** (file `ILPUHPFyGRtLnc0JJ6lGyW`; see `FIGMA.md`)
- Tokens: added `color/{surface,track,accent-weak,hairline}`, `font/mono` (IBM Plex Mono), and a
  Layout collection (spacing/radius/stroke grid).
- Shared **Header** + **Footer** components (real Block / Polymarket / PMN logos + accent-tab
  hairline) — one source of truth for chrome.
- **Background** component (variant set: Gradient / Solid / Glow / Image + photo/texture slot);
  field gradient binds to `color/field/*` so it reskins via brand mode.
- **Delta** atom (triangle *shapes* + mono value, green/red by sign), **Row** (leaderboard list
  item), **Scaffold** (clone to start a new card).
- All 10 cards rebuilt on the above; brand-neutral names (`Card / Binary`, not `PMN / …`).
- **Brand System board** on Foundations (per-brand swatches bound to live variables) + a
  "Switch a card's brand" callout.

**New — docs & packaging**
- `README.md` rewritten for the v3 pipeline; adds the **designer ↔ analyst handoff** workflow.
- `GUIDE.md` (humans), `AGENTS.md` (rewritten for the Figma pipeline, with per-template data
  schemas), `FIGMA.md` (file reference + node-id map + repo mapping), `previews/` (rendered
  card contact sheet + Brand System board), an in-Figma 📖 Read Me page.

**Superseded (kept for reference, not removed)**
- The SVG kit: `lib/pmn.py` SVG helpers, `data-viz/`, `social/`, `episode-01/_*.py`.
- `lib/pmn_live.py` (live market data) is **still used** as the data source.

## How to review
1. Open the Figma file (`FIGMA.md` has the link + node-id map) and skim `previews/cards.png`.
2. Read `README.md` → `GUIDE.md`/`AGENTS.md`.
3. `python3 tools/test_pmn.py` (should print `7 passed`).

## Notes / compatibility
- `templates/*.manifest.json` and `tokens.json` are **generated** — regenerate via the exporters,
  don't hand-edit.
- Cards are 1080×1080 today; other aspect ratios are a planned follow-up (`HANDOFF.md`).
- Brands are modes: adding a show = add a Brand mode + logos + a `brands.json` entry; every card
  reskins automatically.
