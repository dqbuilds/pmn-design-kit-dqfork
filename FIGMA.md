# The Figma file — reference & repo mapping

The card visuals are authored in one Figma file. That file is the **source of truth for
design**; this repo packages everything needed to *operate, review, and reproduce* it — the
generated contract (`templates/*.manifest.json`, `tokens.json`), the brand/logo registry
(`brands.json`), the two engines (`tools/`), and rendered **previews** (below). Figma can't
export its `.fig` binary programmatically, so the file is referenced by link + node-id map
rather than committed as a binary.

- **File:** [PMN Design System](https://www.figma.com/design/ILPUHPFyGRtLnc0JJ6lGyW) · key `ILPUHPFyGRtLnc0JJ6lGyW`

## Previews (committed)

| | |
|---|---|
| All 10 card templates | [`previews/cards.png`](previews/cards.png) |
| Brand System board (PMN + Demo) | [`previews/brand-system.png`](previews/brand-system.png) |

## Pages

| Page | nodeId | Contents |
|---|---|---|
| 📖 Read Me | `108:2` | In-Figma human guide (mirrors `GUIDE.md`) + designer↔analyst handoff |
| 🎨 Foundations | `52:195` | Brand System board (`73:2`), "Switch a card's brand" callout, logo components |
| 🧩 Components | `60:2` | ① Card Templates section (`104:300`) · ② Building Blocks section (`105:300`) |

## Components (page 🧩 Components)

| Component | nodeId | Manifest |
|---|---|---|
| Header (shared chrome) | `60:3` | — |
| Footer (shared chrome) | `61:13` | — |
| Background (variant set: Gradient/Solid/Glow/Image) | `67:44` | — |
| Delta (sign-driven ▲▼) | `79:40` | — |
| Row / Leaderboard (list item) | `79:44` | — |
| Card / _Scaffold (clone to start a card) | `86:92` | — |
| Card / Binary | `62:14` | `templates/binary.manifest.json` |
| Card / Leaderboard | `80:40` | `templates/leaderboard.manifest.json` |
| Card / Divergence | `84:66` | `templates/divergence.manifest.json` |
| Card / Gauge | `86:137` | `templates/gauge.manifest.json` |
| Card / Timeseries | `89:144` | `templates/timeseries.manifest.json` |
| Card / Quote | `91:170` | `templates/quote.manifest.json` |
| Card / Cover | `93:196` | `templates/cover.manifest.json` |
| Card / Guest-Announce | `94:222` | `templates/guest-announce.manifest.json` |
| Card / Hero-Quote | `96:248` | `templates/hero-quote.manifest.json` |
| Card / Episode | `97:274` | `templates/episode.manifest.json` |

Logos (Foundations): The Block `35:143` · Polymarket `35:147` · PMN `35:148` · Demo News `49:192` · Acme `49:194` · Demo `49:196` (also in `templates/brands.json`).

## Variables (→ `templates/tokens.json`)

- **Brand** collection (`VariableCollectionId:7:2`) — one **mode per brand**: `PMN`, `Demo`.
  17 tokens: `color/field/{start,mid,end}`, `color/{accent,accent-weak,panel-bg,surface,track,hairline,text,muted,eyebrow-ink,up,down}`, `font/{display,body,mono}`.
- **Layout** collection (`VariableCollectionId:59:2`, mode `Value`) — `space/*`, `radius/*`, `stroke/hairline`.

Edit values in Figma's Variables panel (or eyeball on the Brand System board), then run
`tools/export_tokens.js` → commit `templates/tokens.json`.

## How the repo mirrors the file

| Figma | Repo (generated) | Regenerate with |
|---|---|---|
| A card component's named slots (`#…`/`@…` + `pmn` plugin data) | `templates/<name>.manifest.json` | `tools/export_manifest.js` |
| Brand + Layout variables (all modes) | `templates/tokens.json` | `tools/export_tokens.js` |
| Brand logo components (per mode) | `templates/brands.json` | hand-maintained registry |

`render.js` fills a manifest with data + a brand mode and writes the finished card back into
Figma. **Manifests and `tokens.json` are generated — never hand-edit them.** Validate the whole
contract with `python3 tools/test_pmn.py`.

## Reproduce / open
1. Open the Figma file (link above).
2. To render: paste `tools/render.js` into a `use_figma` call on the 🧩 Components page; see
   `README.md` (Quickstart) and `AGENTS.md` (per-template data schemas).
3. After any contract change in Figma, re-export (above) and run the tests before committing.
