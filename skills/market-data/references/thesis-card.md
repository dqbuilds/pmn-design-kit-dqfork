# Thesis Card – the market-data → {trade journal, data-snapshot} hand-off

A single artifact emitted from one `market-data` pull. Two consumers read it:

1. **`podcast-research/workflows/data-snapshot.md`** reads the `## Snapshot`
   table (same columns it already prescribes) and the `repull` block to compute
   publish-time deltas.
2. **Trade journal** reads the fenced `json` block for entry/invalidation/size.

One pull, one timestamp, both downstream uses. Never re-pull separately for each
consumer. That desyncs the as-of and breaks delta comparison.

---

## Rules baked into the format (do not strip)

- **Sign every flow metric.** `flow_dir` is `+buy` / `-sell` / `flat`, never a bare
  magnitude. The board trigger that read PENGU/GIGA as "firing" was unsigned. A
  card with an unsigned flow field is invalid.
- **Confidence label on every metric** (`[High|Medium|Low]`, same scale as
  data-snapshot). Do not size on `[Low]`.
- **DeFiLlama pulls are ask-first.** If a field's `platform` is DeFiLlama, the card
  cannot be emitted until the user approved that specific endpoint. Record the
  approved endpoint in `source_endpoints`.
- **MNPI wall.** `catalyst_watch` entries must be **public, re-pullable metrics**
  only. Anything sourced from a pre-recording guest conversation is editorial,
  never a trade trigger. Leave it out of this card.

---

## Format

```
## Thesis Card – <SYMBOL> (<protocol/name>)
**As-of:** <ISO timestamp + tz>   **Pull:** market-data (<modules used>)
**Episode link (if any):** <guest + air date = the dated catalyst>

### Classification
- Type: <sentiment-meme | protocol-revenue | infra | defi | stable/RWA>
- Setup: <compressed | extended | post-run bleed | dormant>
- Catalyst readiness: <firing | loaded-uncatalyzed | needs-own-catalyst>

### Snapshot   (data-snapshot.md reads this table)
| Metric | Value | flow_dir | Platform | Methodology | Conf |
|---|---|---|---|---|---|
| price / 24h | | | DexScreener/CG | | [H/M/L] |
| liquidity | | n/a | DexScreener | | |
| vol 30d / turnover | | | DexScreener | | |
| price vs 7d/30d VWAP | | | derived | | |
| fees or revenue (daily) | | | DeFiLlama* | | |
| <protocol-specific> | | | | | |

### Underwrite   (trade journal reads the json below)
- Thesis (1 line):
- Entry / level:
- Invalidation:
- Catalyst + green-light metric:
- Size note (liquidity-bounded):

### repull   (data-snapshot delta at publish)
- metrics to re-pull: <list>
- surface delta if: >10% OR direction contradicts the guest's stated narrative
```

```json
{
  "symbol": "", "as_of": "", "type": "", "setup": "", "readiness": "",
  "price": null, "chg_24h_pct": null, "flow_dir": "", "vs_vwap30d_pct": null,
  "liquidity_usd": null, "vol_30d_usd": null, "turnover_pct": null,
  "fees_daily_usd": null, "rev_daily_usd": null,
  "thesis": "", "entry": "", "invalidation": "",
  "catalyst_watch": [{"signal": "", "threshold": "", "platform": ""}],
  "risk_watch": [{"flaw": "", "invalidates_if": "", "source": ""}],
  "confidence": "", "source_endpoints": []
}
```

A card with a populated `catalyst_watch` but an empty `risk_watch` is suspect.
Every thesis has a kill condition. The Tier 1 adversarial lens (Protos, the
litigation docket, the competitive board) exists to fill this field. If a
headline scan returned no flaws, say so explicitly. Don't leave it blank.

---

## Worked example: PUMP (pulled this session)

```
## Thesis Card – PUMP (pump.fun)
**As-of:** 2026-06-02 ~08:10 UTC   **Pull:** market-data (defillama, dexscreener)
**Episode link:** hypothetical pump.fun founder ep; air date = dated catalyst

### Classification
- Type: protocol-revenue
- Setup: compressed (price coiled, but revenue deteriorating)
- Catalyst readiness: needs-own-catalyst (a revenue turn, not sentiment)

### Snapshot
| Metric | Value | flow_dir | Platform | Methodology | Conf |
|---|---|---|---|---|---|
| price / 24h | $0.00182 / ~flat | flat | DexScreener | aggregate pairs | [H] |
| liquidity | n/a | n/a | DexScreener | top-pool sum | [H] |
| vol 30d / turnover | $376M / high | +buy (B/S 1.04) | DexScreener+CSV | 30d sum | [H] |
| price vs 30d VWAP | -4.0% | n/a | derived | rolling_30d_vwap | [H] |
| fees daily | $1.04M (6/01), 7d avg $0.92M | flat (+2% w/w) | DeFiLlama* | summary/fees/pump.fun | [H] |
| revenue daily | $0.80M (6/01), 7d avg $0.70M | flat | DeFiLlama* | dailyRevenue | [H] |
| revenue annualized | ~$320M (2026) vs $971M (2025) | -sell (fundamental) | Tier1+DeFiLlama | YoY | [H] |
```

```json
{
  "symbol": "PUMP", "as_of": "2026-06-02T08:10:00Z",
  "type": "protocol-revenue", "setup": "compressed", "readiness": "needs-own-catalyst",
  "chg_24h_pct": 0.0, "flow_dir": "flat", "vs_vwap30d_pct": -4.0,
  "vol_30d_usd": 375868487, "turnover_pct": null,
  "fees_daily_usd": 1039717, "rev_daily_usd": 795748,
  "thesis": "Falling-revenue turnaround bet: ~$320M annualized vs $971M in 2025; 50% buyback already failed at full size; cross-chain + holder-distribution optionality un-priced; RICO/securities docket is the tail.",
  "entry": "starter only; add on a revenue-trend turn, not a fee-level pop",
  "invalidation": "revenue decline persists; securities/RICO ruling; 30d VWAP loss with -sell flow",
  "catalyst_watch": [
    {"signal": "pump.fun GO bounty board (launched 2026-06-04, verified @Pumpfun)", "threshold": "GO take-rate breaks the flat $0.65-0.80M/day revenue band", "platform": "DeFiLlama / fees.pump.fun", "note": "narrative-confirmed; revenue contribution UNPROVEN. Likely pro-cyclical (X-engagement bounties), not counter-cyclical as first assumed."},
    {"signal": "daily revenue trend (decline arresting/reversing)", "threshold": "YoY decline flattens then turns up", "platform": "DeFiLlama"},
    {"signal": "cross-chain fees (Base/ETH/BSC/Monad)", "threshold": "non-Solana revenue surface goes live", "platform": "DeFiLlama"},
    {"signal": "holder revenue-distribution mechanism live", "threshold": "ship date", "platform": "Tier1/onchain"}
  ],
  "risk_watch": [
    {"flaw": "revenue -67% YoY ($971M 2025 -> ~$320M annualized 2026)", "invalidates_if": "decline continues; 50% buyback shrinks with it", "source": "CoinDesk 2026-04-29"},
    {"flaw": "buyback cut 100%->50%; even 100% failed to support price", "invalidates_if": "halved bid can't offset unlock/sell pressure", "source": "CoinDesk 2026-04-29"},
    {"flaw": "SDNY RICO + securities class actions (PNUT/HAWK), UK ban", "invalidates_if": "securities/RICO ruling against launchpad token", "source": "Decrypt RICO; CoinDesk class action"},
    {"flaw": "GO bounty board adds money-transmission/escrow/consumer-harm surface (pump.fun escrows funds + selects winners + 'pay anyone for anything')", "invalidates_if": "regulator/plaintiff targets GO escrow or paid-engagement model", "source": "@Pumpfun ToS 2026-06-04"},
    {"flaw": "launchpad share volatile (LetsBonk hit 64% Jul-2025)", "invalidates_if": "rival re-flip on creator incentives", "source": "The Block launchpad war"}
  ],
  "confidence": "High",
  "source_endpoints": ["https://api.llama.fi/summary/fees/pump.fun"]
}
```
