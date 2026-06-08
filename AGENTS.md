# AGENTS.md — generate PMN visuals end to end

This repo is a self-contained pipeline for producing **Prediction Market News**
(PMN) social visuals: research a market → pull live data → drop the numbers into
a generator → render brand-correct PNGs. This file is the operating manual for an
AI agent (or a human) doing that end to end.

---

## 0. One-time setup

```bash
# system: librsvg gives `rsvg-convert` (SVG -> PNG). REQUIRED.
brew install librsvg            # macOS
# sudo apt-get install librsvg2-bin   # Debian/Ubuntu

# python deps
pip install -r requirements.txt
```

Fonts: cards render in Helvetica Neue (native on macOS). On Linux install a close
grotesk; layout math is unaffected but glyph metrics shift slightly.

Verify the toolchain works:

```bash
python3 episode-01/_tech_markets.py     # should write PNGs into episode-01/exports-tech/
```

---

## 1. Mental model

- **`lib/pmn.py`** is the single source of truth: palette, type scale, the grid
  (`M` margin + `PADIN` panel padding), brand chrome (The Block top-left,
  "Presented by Polymarket" top-right), the `[PMN]` footer, backgrounds, and the
  dark data panel. Never hardcode brand colors/spacing in a generator — pull them
  from here.
- **`data-viz/_build.py` + `_more.py`** are the card layouts (binary, multi,
  gauge, leaderboard, hero-quote, area, stacked-bar, scorecard, movers, map…).
- **`social/_build.py`** has the episode/market/quote/cover cards.
- **A generator** (`episode-01/_*.py`) is just: a glass monkeypatch + a set of
  **data dicts** + a render loop. To change a visual you change the data dict and
  rerun. To make a *new* kind of visual you add a small card function.

The "liquid glass" look is a monkeypatch over `pmn._panel_body` defined at the
top of each generator. `TINT` controls panel transparency (0.50 see-through →
0.92 opaque). `pmn.set_background("team-gradient"|"house"|"team-solid"|"team-glow")`
sets the field. Both are set per render.

---

## 2. The pipeline

### Step A — (optional) frame the episode
Use `skills/podcast-research/` for editorial framing: `workflows/segment-brief.md`,
`context/question-craft.md`, `workflows/data-pull.md`, plus `style/` for voice.
This decides *which markets matter* and *what the cards should say*.

### Step B — pull live data
All scripts have a CLI; only dep is `requests`. Endpoint docs:
`skills/market-data/references/endpoints.md`.

```bash
cd skills/market-data/scripts

# Polymarket (odds, event/market volume)
python3 polymarket.py top 10                 # top markets by total volume + odds
python3 polymarket.py events 20              # open events by 24h volume
python3 polymarket.py market <event-slug>    # one market/event odds + token ids

# Hyperliquid (perps; HIP-3 builder dexs incl. Trade.xyz = `xyz`)
python3 hyperliquid.py find SPCX CRWV NVDA   # locate tickers across all dexs
python3 hyperliquid.py dex xyz 25            # one dex board by 24h notional vol
python3 hyperliquid.py perps 20              # top HL perps

# CoinGecko / DeFiLlama / DexScreener
python3 coingecko.py price <id>
python3 defillama.py stables 10
python3 dexscreener.py token <address>
```

Decoding gotchas are handled in the modules (Polymarket `odds` is a list of
`{outcome, price, token_id}`; Hyperliquid returns strings cast to float). Always
record the **pull timestamp** — it goes on the card as the source stamp.

### Step C — update the data dict
Open the matching generator in `episode-01/` and edit the dict near the bottom.
Example (`_tech_markets.py`):

```python
AIMODEL = {
    "tag": "Top AI model · end of June", "title": ["One lab is running", "away with it"],
    "leader": ("Anthropic", 85), "field": [("Google", 10), ("OpenAI", 4), ("xAI", 0.4)],
    "caption": "Claude Opus 4.8 took #1 on May 27. The field fights for scraps.",
    "source": "Polymarket · Jun 8, 2026"}     # <- update the as-of date
```

### Step D — render
```bash
python3 episode-01/_robostrategy.py     # -> exports-robostrategy/  (episode data cards)
python3 episode-01/_markets.py          # -> exports-markets/       (top-volume leaderboards)
python3 episode-01/_tech_markets.py     # -> exports-tech/          (bespoke tech cards)
python3 episode-01/_covers.py           # -> exports-robostrategy/  (real-photo covers)
```

Each writes `<name>.svg` + `<name>.png`. Exports are gitignored — they regenerate.

### Step E — review
Open the PNGs. Check: nothing overlaps the `[PMN]` footer or the source line;
no element crosses a panel border; captions wrap to ≤2 lines; white/muted text is
legible on the chosen background (the brighter the field, the more opaque `TINT`
should be — team-gradient's bright corner needs the most cover).

---

## 3. Generators and what they emit

| Generator | Output | Layouts |
|---|---|---|
| `_robostrategy.py` | `exports-robostrategy/` | cover, binary, gauge, leaderboard, multi, **divergence** (custom) |
| `_markets.py` | `exports-markets/` | Polymarket 24h/7d/30d leaderboards × 4 backgrounds + glass sweep |
| `_tech_markets.py` | `exports-tech/` | **valuation curve**, **dominance**, **hype-vs-odds** (all custom) + per-background glass |
| `_covers.py` | `exports-robostrategy/` | real-photo / logo episode covers (1:1, 16:9, 9:16) |

---

## 4. Recipes

**Change the numbers on a card:** edit its data dict, rerun the generator.

**Render every brand background at its own transparency:** see the `BG_TINT` map
in `_tech_markets.py` — calmer fields get a more see-through panel, brighter ones
a more opaque one. Reuse that pattern.

**Add a new card type:** write a `card_x(w, h, d)` that returns an SVG string,
following the structure of `card_curve`/`card_dominance` in `_tech_markets.py`:
`pmn.svg_open` → `pmn.defs` → `dv._bg` (background) → `dv.chrome` → your panels
via `dv.panel(...)` → caption → `dv.footer` + source → `pmn.svg_close`. Use
`M`, `PADIN`, `ty()` for spacing/type so it stays on-grid.

**Start a new episode:** copy `episode-01/` to `episode-02/`, swap the data dicts
and (for covers) the assets in `assets/`, rerun. Paths are relative to the
generator, so it just works.

---

## 5. Brand rules (do not violate)

- **Chrome is fixed:** The Block leads top-left; "Presented by Polymarket" is the
  top-right sponsor stamp; `[PMN]` anchors the footer. Don't move or recolor them.
- **Field is electric-blue.** Green/red/gold are **data semantics only** (up /
  down / highlight) — never field or decoration colors.
- **Type sizes as a ratio of canvas width** (`ty()`), so it stays legible in a
  mobile feed. Default canvas 1080×1080; covers also 16:9 / 9:16.
- **Every card is dated** at the source line. Re-pull if data is stale.
- **Voice** (for any copy — tags, titles, captions): sharp, analytical,
  crypto-native, concise. Observation → explanation → implication. No em-dashes
  (en-dashes OK), no buzzwords, no emojis/hashtags unless asked. See
  `skills/podcast-research/style/` for the full voice spec.
- **Contrast floor:** body text ≥ 4.5:1, bars ≥ 3:1 against the panel.

---

## 6. Troubleshooting

- `command not found: rsvg-convert` → install librsvg (Step 0).
- `Entity 'AMP' not defined` on render → an `&` ended up in an eyebrow/tag string;
  `pmn.eyebrow` upper-cases after escaping, which breaks `&amp;`. Avoid `&` in
  eyebrow/tag text (use "and"/"+").
- Text overlapping the footer → the caption ran to 3 lines or the panel is too
  tall; shorten the caption or reduce `GH`/`CAPG` (see the rhythm constants at
  the top of `_tech_markets.py`).
- Fonts look wrong on Linux → install a Helvetica-class grotesk.
