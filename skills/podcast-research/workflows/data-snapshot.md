# Workflow — Data Snapshot

Use this workflow to capture a timestamped data snapshot before an interview
records, so the same metrics can be re-pulled at publish time for comparison.

Called by: `workflows/thread-pre.md`, `workflows/thread-post.md`

---

## When to Run This

Run a pre-interview snapshot when the episode topic involves a protocol,
asset class, or market structure claim that will have measurable state:
- DeFi protocol coverage (TVL, fees, volume, utilization)
- Perp DEX coverage (open interest, funding rates, volume)
- Lending protocol coverage (utilization rates, interest rates, TVL)
- Stablecoin / RWA coverage (supply, market cap, backing)
- Macro / market structure (BTC dominance, total crypto market cap)

Do NOT force a snapshot if the episode is primarily about a person's philosophy,
history, or non-metric topics (e.g., cypherpunk ethos, builder psychology).

---

## Metric Selection by Topic

| Episode Focus | Metrics to Snapshot |
|---|---|
| Perp DEX (e.g., Aster, Hyperliquid, GMX) | Open interest, 24h volume, funding rates, fee revenue |
| Spot DEX / AMM | TVL, 24h volume, fee revenue, unique LPs |
| Lending protocol | TVL, utilization rate, borrow/supply rates, bad debt |
| L1 / L2 infrastructure | TVL, DAUs, TPS (real load), fee revenue, developer count |
| Stablecoin issuer | Circulating supply, market cap, reserve composition |
| RWA / tokenized assets | Total tokenized value, category breakdown, yield |
| Bitcoin-specific | Price, market cap, exchange netflow, MVRV, SOPR |
| Macro / market overview | Total crypto market cap, BTC dominance, stablecoin supply |

---

## Step-by-Step Protocol

### Step 1 — Identify 3–5 Metrics
Pick the metrics most likely to be discussed in the episode.
More than 5 is noise. Fewer than 3 gives no comparison signal.

### Step 2 — Pull From Correct Platform
Use the platform selection guide in `workflows/data-pull.md`.
Always pull from primary platform (DefiLlama, Token Terminal, Artemis,
Glassnode, etc.) — not from a news article citing the platform.

### Step 3 — Record the Snapshot

```
## Data Snapshot — [Protocol/Topic]

**Snapshot timestamp:** [Date, time, timezone]
**Episode context:** [Guest name + episode topic, 1 sentence]

| Metric | Value | Platform | Methodology Note |
|---|---|---|---|
| [Metric 1] | [Value] | [Platform] | [e.g., "TVL excludes borrowed"] |
| [Metric 2] | [Value] | [Platform] | |
| [Metric 3] | [Value] | [Platform] | |
| [Metric 4] | [Value] | [Platform] | |
| [Metric 5] | [Value] | [Platform] | |
```

### Step 4 — Re-Pull at Publish Time

When the episode publishes, re-pull the same metrics from the same platforms.
Record a second snapshot in the same format with a new timestamp.

Then calculate delta:

```
## Snapshot Comparison

| Metric | At Recording | At Publish | Delta | Note |
|---|---|---|---|---|
| TVL | $2.1B | $2.4B | +14% | Protocol launched new incentive program |
| 24h Volume | $890M | $1.2B | +35% | KBW week volume spike |
| Funding Rate | 0.01% | -0.03% | flipped negative | Market sentiment shifted |
```

---

## Which Deltas Are Worth Surfacing in Threads

**Include in thread if:**
- Delta is >10% in either direction
- Direction contradicts what the guest said (e.g., they called for growth but TVL fell)
- Direction confirms what the guest said in a striking way
- A metric crossed a meaningful threshold (ATH, zero, a round number)

**Exclude from thread if:**
- Change is within normal daily variance (<5%)
- The metric wasn't discussed in the episode
- The change has an obvious mechanical explanation unrelated to the guest's thesis

---

## Confidence Labels

Apply to each metric in the snapshot:
- `[High]` — Direct platform API or dashboard, methodology clear
- `[Medium]` — Derived metric, estimated, or methodology has known caveats
- `[Low]` — Single source, paywalled, or self-reported by the project
