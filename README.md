# PMN Design Kit

Generative social-asset system for **Prediction Market News** (PMN), presented by
Polymarket. Every card is built as an SVG from a shared Python design library and
rasterized to PNG — so the brand chrome, palette, grid, type scale, and the
"liquid-glass" data panels stay consistent across every visual.

This repo contains the **code and assets that generate** the PMN data cards,
market leaderboards, and the episode-01 (RoboStrategy) visual set.

## What it produces

| Generator | Output folder | What |
|---|---|---|
| `episode-01/_robostrategy.py` | `episode-01/exports-robostrategy/` | Episode data cards — cover, binary, gauge, leaderboard, multi, and a custom "deals down / dollars up" divergence card |
| `episode-01/_markets.py` | `episode-01/exports-markets/` | Top-volume Polymarket leaderboards (24h / 7d / 30d) across 4 brand backgrounds + a glass-transparency sweep |
| `episode-01/_tech_markets.py` | `episode-01/exports-tech/` | Bespoke technology-market cards — SpaceX implied-valuation curve, AI-model dominance, Optimus hype-vs-odds — with per-background glass transparency |
| `episode-01/_covers.py` | `episode-01/exports-robostrategy/` | Real-photo / logo episode covers (1:1, 16:9, 9:16) |

## Architecture

```
lib/pmn.py            # single source of truth: palette, type scale, grid,
                      # chrome (The Block + "Presented by Polymarket"), panels,
                      # backgrounds, type primitives, brand-mark loading
data-viz/_build.py    # card_shell + binary / multi / timeseries / hero / area /
                      # stacked-bar layouts + the team backgrounds
data-viz/_more.py     # gauge / leaderboard / scorecard / movers / map / scatter
social/_build.py      # episode card, market card, quote card, podcast cover
episode-01/           # the episode generators + the guest assets they use
brand/                # The Block + Polymarket marks, PMN logo lockups
```

The "liquid glass" panel is a monkeypatch over `pmn._panel_body` applied inside
each generator, so the same dark data panels render translucent over the brand
field. Transparency (`TINT`) and the page background (`pmn.set_background`) are
set per render.

## Setup

**System dependency — librsvg** (provides `rsvg-convert`, used for SVG→PNG):

```bash
# macOS
brew install librsvg
# Debian/Ubuntu
sudo apt-get install librsvg2-bin
```

**Python deps:**

```bash
pip install -r requirements.txt
```

**Fonts:** type renders in Helvetica Neue (native on macOS). On Linux, install a
close grotesk or the cards will fall back to a system sans — layout math is
unaffected, but exact glyph metrics will shift slightly.

## Run

```bash
python3 episode-01/_robostrategy.py
python3 episode-01/_markets.py
python3 episode-01/_tech_markets.py
python3 episode-01/_covers.py
```

Each writes SVG + PNG into its `exports-*` folder (gitignored — regenerate
locally). Edit the data dicts at the bottom of each generator to change the
numbers; rerun to refresh.

## Data provenance

Market figures were pulled from Polymarket (Gamma API) and Hyperliquid on
2026-06-08 and are **hardcoded** in each generator's data dicts. Re-pull and
update those dicts to refresh. Sources are stamped on every card.

## Brand notes

- The Block leads top-left; "Presented by Polymarket" is the fixed top-right
  sponsor stamp; the `[PMN]` lockup anchors the footer.
- Electric-blue field; green/red/gold are data semantics only.
- Canvas defaults to 1080×1080 (also 16:9 / 9:16 for covers); type is sized as a
  ratio of canvas width to stay legible in a mobile feed.
