# Verified endpoint reference

Verified May 2026 against official docs. All read endpoints below are public —
no API key, no auth, unless noted. Don't re-research these before using them.

## Hyperliquid — `POST https://api.hyperliquid.xyz/info`

JSON body, `Content-Type: application/json`. No auth. Limit 1200 weight/min/IP.
All numeric values return as **strings**. `metaAndAssetCtxs` returns
`[meta, assetCtxs]`; the two inner arrays are index-aligned.

| Need | Body |
|---|---|
| Perp meta + contexts (mark, oracle, OI, funding, 24h vol) | `{"type":"metaAndAssetCtxs","dex":""}` |
| All mid prices (cheapest, weight 2) | `{"type":"allMids","dex":""}` |
| OHLCV candles | `{"type":"candleSnapshot","req":{"coin":"BTC","interval":"1h","startTime":<ms>,"endTime":<ms>}}` |
| Spot meta + contexts | `{"type":"spotMetaAndAssetCtxs"}` |

Candle intervals: `1m 3m 5m 15m 30m 1h 2h 4h 8h 12h 1d 3d 1w 1M`.
Candle fields: `t`(open ms) `T`(close ms) `o h l c v` `n`(#trades).

HIP-3 builder-deployed perps: `{"type":"perpDexs"}` lists builder dexs (first
element is null = default book). Then `{"type":"metaAndAssetCtxs","dex":"<name>"}`
per dex. **Gotcha:** builder-dex universe coin names come back dex-prefixed
(`xyz:SPCX`), not bare — so an exact-match search on `"SPCX"` misses them.
`hyperliquid.py` handles this via `perp_dexs()`, `all_perp_contexts()`,
`find_perp("SPCX")`. Pre-IPO/equity perps live on `xyz` (trade.xyz) and
valuation perps on `vntl` (Ventuals).

WebSocket `wss://api.hyperliquid.xyz/ws`:
`{"method":"subscribe","subscription":{"type":"allMids","dex":""}}`,
`{"type":"candle","coin":"BTC","interval":"1h"}`, `{"type":"l2Book","coin":"BTC"}`.

## Polymarket

Read endpoints public. Auth only for placing orders / user WS channel.

**Gamma** `https://gamma-api.polymarket.com` — events + markets metadata.
- `GET /events`, `GET /markets`
- Filters: `active`, `closed` (default false). Pagination: `limit`, `offset` (NOT page).
- Sort: `order=<field>&ascending=false`. **Order fields are camelCase** and
  differ by endpoint — `/markets`: `volumeNum` (total), `volume24hr`,
  `liquidityNum`; `/events`: `volume24hr`, `volume`, `liquidity`, `endDate`.
  snake_case (`volume_24hr`, `volume_num`) is silently ignored — verified.
- Market filters: `slug`, `id`, `condition_ids`, `clob_token_ids`, `volume_num_min/max`, `liquidity_num_min/max`.
- Odds fields: `outcomes` paired with `outcomePrices`; volume `volume`/`volumeNum`/`volume24hr`; `liquidity`; `clobTokenIds`; `conditionId`.
- **`outcomePrices` and `clobTokenIds` are JSON-encoded strings** — `json.loads()` them.

**Data** `https://data-api.polymarket.com` — `GET /trades`, `/holders?market=<conditionId>`, `/positions`, `/activity`, `/value?user=<0x>`.

**CLOB** `https://clob.polymarket.com`
- `GET /price?token_id=<id>&side=BUY|SELL` → best bid/ask.
- `GET /book?token_id=<id>` → bids(desc)/asks(asc), tick_size, last_trade_price.
- Also `/midpoint`, `/spread`, `/last-trade-price`.

WebSocket `wss://ws-subscriptions-clob.polymarket.com/ws/market`:
subscribe `{"assets_ids":["<token_id>",...],"type":"market"}`;
keepalive plaintext `"PING"` ~10s → server `"PONG"`;
events `book`, `price_change`, `last_trade_price`.

Dead: `api.polymarket.com/v1/markets` (old notebook host) — use Gamma `/markets`.

## CoinGecko — `https://api.coingecko.com/api/v3`

Free anon ~30/min; free Demo key → 100/min, 10k/mo via `x-cg-demo-api-key`
header (set `COINGECKO_API_KEY`). HYPE coin id = `hyperliquid`.
- `/simple/price?ids=&vs_currencies=usd&include_market_cap=&include_24hr_vol=`
- `/coins/{id}` — full object.
- `/coins/{id}/market_chart?vs_currency=usd&days=&interval=daily` → `[ts_ms, value]`.
- `/coins/{id}/ohlc?vs_currency=usd&days=` → `[ts_ms,o,h,l,c]`.
- `/search?query=` — resolve a coin id.

## DeFiLlama — free, no key. Split across 4 subdomains.

`api.llama.fi` (TVL + volume/fees), `stablecoins.llama.fi`, `yields.llama.fi`,
`coins.llama.fi` (prices). Price coin ids are `{chain}:{address}` or
`coingecko:{id}` (e.g. `coingecko:hyperliquid`).

| Need | Endpoint |
|---|---|
| All protocols (TVL, mcap, chains) | `GET api.llama.fi/protocols` |
| One protocol, full history | `GET api.llama.fi/protocol/{slug}` |
| Current TVL (bare number) | `GET api.llama.fi/tvl/{slug}` |
| TVL per chain | `GET api.llama.fi/v2/chains` |
| Chain TVL history | `GET api.llama.fi/v2/historicalChainTvl[/{chain}]` |
| DEX volume leaderboard | `GET api.llama.fi/overview/dexs[/{chain}]` |
| Fees/revenue leaderboard | `GET api.llama.fi/overview/fees?dataType=dailyFees\|dailyRevenue` |
| One DEX volume history | `GET api.llama.fi/summary/dexs/{slug}` |
| One protocol fees history | `GET api.llama.fi/summary/fees/{slug}` |
| All stablecoins | `GET stablecoins.llama.fi/stablecoins?includePrices=true` |
| Stablecoin supply history | `GET stablecoins.llama.fi/stablecoincharts/all` |
| Yield pools | `GET yields.llama.fi/pools` |
| Current price(s) | `GET coins.llama.fi/prices/current/{coins}` |
| Price chart | `GET coins.llama.fi/chart/{coins}?span=&period=` |

Gotchas (handled in `defillama.py`): the `/overview/dexs` and `/overview/fees`
`protocols` arrays come **unsorted** — sort by `total24h` yourself. Stablecoin
`circulating` is a dict `{"peggedUSD": <amount>}`, not a number.

## DexScreener — `https://api.dexscreener.com/latest/dex`

No key. `/tokens/{address}` (pairs for a token), `/search?q=` (search pairs).
Heavier holder/concentration version lives in `~/squeeze_pipeline/dexscreener.py`.

## Not usable as APIs

- **ASXN / hyperscreener** (`api-hyperliquid.asxn.xyz`) — real backend but
  Cloudflare-Turnstile-gated; a plain HTTP client gets `403 TURNSTILE_REQUIRED`.
  Pull the same primitives (OI, funding, volume) from Hyperliquid `/info`.
- **hl.eco** — aggregator/directory, no JSON API. Use the upstream sources it links.
