---
name: market-data
description: Pull live and historical market data from Hyperliquid (perps stats, OHLCV candles), Polymarket (event/market odds, volume ranking, CLOB price/book, live stream), CoinGecko (price/market cap/charts), DeFiLlama (TVL, stablecoin supply, DEX volume, protocol fees/revenue, yields), and DexScreener (DEX liquidity/volume). Use when a tweet, thread, chart, or podcast brief needs real numbers from these venues.
allowed-tools: Bash, Read, Write, Edit
---

# Market Data

Fetch real numbers from Hyperliquid, Polymarket, CoinGecko, and DexScreener.
This skill is the data layer — it does not write copy. Hand its output to
`chart-tweet`, `tweet-drafter`, `research-to-thread`, or `podcast-research`.

All endpoints are verified and documented in `references/endpoints.md`. Read
that file before writing any new request — do not re-research or guess URLs.

## How to use

Each source is a self-contained Python module in `scripts/`. Run them directly
(every module has a CLI) or import the functions. Only hard dependency is
`requests`; `websockets` is needed only for the live Polymarket stream.

```bash
cd .claude/skills/market-data/scripts

# Hyperliquid
python hyperliquid.py perps 20          # top 20 perps by 24h notional volume
python hyperliquid.py candles HYPE 1h 30 # HYPE 1h candles, last 30 days
python hyperliquid.py mids               # all mid prices
# HIP-3 builder-deployed perps (pre-IPO / equities / commodities)
python hyperliquid.py perpdexs           # list builder dexs (xyz, vntl, ...)
python hyperliquid.py dex xyz 30         # one dex's board by 24h volume
python hyperliquid.py find SPCX CBRS     # locate tickers across all dexs

# Polymarket
python polymarket.py top 10             # top 10 open markets by volume + odds
python polymarket.py events 20          # open events by 24h volume
python polymarket.py market <slug>      # one market's odds + token ids
python polymarket.py price <token_id> BUY
python polymarket.py book <token_id>
python polymarket.py stream <token_id>  # live order book (needs websockets)

# CoinGecko (cross-ecosystem context)
python coingecko.py price hyperliquid
python coingecko.py chart hyperliquid 30 daily
python coingecko.py search <name>       # resolve a coin id

# DeFiLlama (TVL, stablecoins, DEX volume, fees/revenue, yields)
python defillama.py tvl hyperliquid     # current protocol TVL
python defillama.py chains 15           # TVL per chain
python defillama.py protocols 20 Hyperliquid  # top protocols, optional chain
python defillama.py stables 10          # stablecoins by circulating supply
python defillama.py dexs                # DEX volume leaderboard (+ chain arg)
python defillama.py fees dailyRevenue   # fees or revenue leaderboard
python defillama.py yields aave Ethereum

# DexScreener
python dexscreener.py token <address>
python dexscreener.py search <query>

# Visuals — turn a pull into a social-embeddable chart/card
python visuals.py contrast               # prove the palette passes WCAG / Adobe analyzer
```

## Visuals (social charts/cards)

`visuals.py` renders pulled data into PNGs for X/social, governed by
`references/visual-style.md`: 2048×1365 (3:2) default canvas (+ 1:1, 9:16), the
Priced In dark palette, and a WCAG contrast self-check that runs on every render
(body text ≥4.5:1, bars ≥3:1 — passes color.adobe.com's contrast analyzer).
Import and call:

```python
import sys; sys.path.insert(0, ".claude/skills/market-data/scripts")
import visuals as v
v.bar_ranking(items, title, subtitle, source=, asof=, highlight={...}, out=)  # ranked horizontal bars
v.compare_pair(a, b, title, ...)        # head-to-head two-bar (auto Nx ratio)
v.dominance(label, pct, title, ...)     # single-share donut
v.odds_shift(rows, title, ...)          # probability bars; 3-tuple adds a prev marker
v.stat_card(stat, caption, ...)         # big-number card
```

`highlight={...}` paints the story's names gold (story-driven color, not
axis-locked). Every call stamps source + as-of.

Reference docs (read before designing a new visual or compositing over video):
- `references/visual-style.md` — canvas dims, palette + measured contrast, story-driven color, motion-bg restraint.
- `references/contrast-analyzer.md` — WCAG thresholds, the luminance formula, and the color.adobe.com analyzer workflow; how to vet a new color or a card over a photo bg.
- `references/ffmpeg-text-plates.md` — full FFmpeg text-plate doctrine: the complete blend-mode/opacity table and all four workflows (alpha box → drawbox banner → adaptive blend → glassmorphic) with copy-paste commands, colorspace fixes, and pitfalls. Use to place a card over the episode's motion ticker bg — don't bake busy motion behind body copy.

To compose data, import instead of shelling out:

```python
import sys; sys.path.insert(0, ".claude/skills/market-data/scripts")
import hyperliquid, polymarket, coingecko, defillama

perps = hyperliquid.perp_contexts()                 # list of dicts, floats
hype  = next(p for p in perps if p["name"] == "HYPE")
mkts  = polymarket.top_markets_by_volume(10)        # decoded odds included
px    = coingecko.simple_price("hyperliquid")
tvl   = defillama.protocol_tvl("hyperliquid")       # bare float
usdt  = defillama.stablecoins()[0]                  # largest stablecoin
```

## Pick the right source

- **Hyperliquid perps truth** (mark/oracle price, open interest, funding, perp
  volume, OHLCV) → `hyperliquid.py`. This is primary for anything HL-native.
- **Prediction-market odds / event volume / order book** → `polymarket.py`.
- **HYPE (or any token) price, market cap, supply, multi-day chart** for
  cross-ecosystem framing → `coingecko.py`. Lower tier — it's not HL-native, so
  prefer Hyperliquid `/info` when both can answer.
- **TVL, stablecoin supply, DEX volume, protocol fees/revenue, yields** →
  `defillama.py`. Primary for your stablecoin/TVL/market-structure beats.
- **DEX liquidity/volume for a specific token contract** → `dexscreener.py`.

## Gotchas (already handled in the modules — don't re-fix)

- Hyperliquid returns all numbers as **strings**; the module casts to float.
- Polymarket `outcomePrices` and `clobTokenIds` are **JSON-encoded strings**;
  `polymarket._decode()` parses them into an `odds` list.
- Polymarket Gamma paginates with `limit`/`offset`, not `page`. The old
  `api.polymarket.com/v1/markets` host is dead.
- **ASXN/hyperscreener** and **hl.eco** have no usable public API (Turnstile /
  dashboard-only). Get the same metrics from Hyperliquid `/info`. See references.

## Keys

Nothing required. Optional CoinGecko free Demo key lifts the rate limit — set
`COINGECKO_API_KEY` in the environment and the module sends it automatically.

## After fetching

Report the numbers with their as-of context (a perp's 24h volume, a market's
current odds, a coin's daily change). Keep it data-native and let the voice
rules in the project CLAUDE.md carry the framing.
