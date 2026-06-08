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
| `_podcast_covers.py` | `exports-podcast-covers/` | Show cover art — both PMN logos (wordmark + monogram) across all 4 backgrounds (1500×1500) |

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
skills/market-data/   # the scripts that SOURCED the market data (see below)
skills/podcast-research/ # editorial framing / question / thread workflows
brand/                # The Block + Polymarket marks, PMN logo lockups
AGENTS.md             # end-to-end guide for an agent to generate visuals
```

## Data sourcing (`skills/market-data/`)

The generators render from numbers **hardcoded** in their data dicts, but those
numbers were pulled with the scripts in `skills/market-data/scripts/` (each has a
CLI; the only hard dependency is `requests`). Endpoint docs in
`skills/market-data/references/endpoints.md`.

```bash
cd skills/market-data/scripts
python3 polymarket.py top 10                  # top markets by volume + odds
python3 polymarket.py events 20               # open events by 24h volume
python3 polymarket.py market <slug>           # one market's odds + token ids
python3 hyperliquid.py find SPCX CRWV NVDA    # locate tickers across HIP-3 dexs
python3 hyperliquid.py dex xyz 25             # Trade.xyz board by 24h volume
python3 coingecko.py price <id>               # cross-ecosystem price
python3 defillama.py stables 10               # stablecoin supply, TVL, fees
python3 dexscreener.py token <address>        # DEX liquidity for a contract
```

The `skills/podcast-research/` skill holds the editorial workflows (segment
briefs, question craft, threads, fact-check, voice/style) used to frame an
episode. It's prompt scaffolding, not code.

**For agents:** see [`AGENTS.md`](AGENTS.md) for the full research → pull →
update → render pipeline.

**Provenance for the shipped cards (pulled 2026-06-08):**

| Card data | Source script / source |
|---|---|
| Optimus odds, AI-model race, SpaceX IPO cap ladder, top-volume leaderboards | `polymarket.py` (Polymarket Gamma) |
| AI + hardware perp 24h volumes (Trade.xyz / `xyz` HIP-3 dex) | `hyperliquid.py` (Hyperliquid `/info`) |
| Crypto VC funding decline (deals −59% / dollars +37% YoY) | The Block — `theblock.co/data` (manual + web; no script) |

To refresh: re-run the relevant script and paste the new figures into the data
dict at the bottom of the matching generator.

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
