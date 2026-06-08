# Workflow — Data Pull

Use this workflow when the request is primarily for a specific metric,
dataset, or on-chain figure. Output is a tight, sourced data summary
with methodology notes.

---

## Platform Selection Guide

First, match the question to the right platform:

| Question Type | Primary Platform | Secondary |
|---|---|---|
| DeFi TVL, protocol fees | DefiLlama | Token Terminal |
| Protocol revenue, P/S ratio | Token Terminal | DefiLlama |
| Cross-chain DAUs, developer activity | Artemis | DefiLlama |
| Wallet behavior, smart money flows | Nansen | Arkham |
| Entity identification, fund flows | Arkham | Nansen |
| BTC/ETH on-chain macro (SOPR, MVRV) | Glassnode | CryptoQuant |
| Custom query on raw on-chain data | Dune Analytics | — |
| RWA tokenization volumes | RWA.xyz | DefiLlama |
| Stablecoin supply and flows | DefiLlama | Token Terminal |
| Funding rounds, M&A | The Block data | Crunchbase |
| Regulatory filings | sec.gov / occ.gov | — |

---

## Step-by-Step Protocol

### Step 1 — Identify the Metric
Restate exactly what is being asked for. Ambiguous questions produce
wrong answers. Clarify:
- What chain(s) are in scope?
- What time window? (24h, 7d, 30d, 90d, all-time?)
- Is this a snapshot (current value) or a trend (change over time)?

### Step 2 — Pull the Data
- Use the platform selection guide above
- Note the exact timestamp of the data pull
- Note the methodology the platform uses (e.g., DefiLlama TVL includes
  borrowed assets — note this if it's material to the claim)

### Step 3 — Sanity Check
Before reporting the number:
- Does it seem plausible given recent context?
- Does it match directionally with what Tier 1 outlets have recently reported?
- If it's a large change from prior period, is there an obvious explanation?
  (If not, double-check the query.)

### Step 4 — Add Context
A raw number is rarely useful alone. Always add:
- Comparison to prior period (7d ago, 30d ago, 1y ago)
- Where it sits relative to all-time high/low if relevant
- What is driving the change if discernible from the data

---

## Output Format

```
## Data: [Metric Name]

**Value:** [Number with units]
**As of:** [Exact date and time if available]
**Source:** [Platform] — [URL]
**Methodology note:** [How this platform calculates this metric, 1 sentence]

**Context:**
- [Comparison: X% change vs. 30 days ago]
- [Comparison: X% below/above ATH of Y, set on Z date]
- [Narrative: what appears to be driving the change]

**Confidence:** [High / Medium / Low]
[High = directly from primary platform with clear methodology]
[Medium = derived or estimated, or methodology is unclear]
[Low = single source, or significant methodology caveats]
```

---

## Timestamp Rules

- **Always include the query date** on any on-chain metric. Crypto data
  changes in real time — a TVL figure from yesterday is not the same as today's.
- For fast-moving metrics (prices, exchange flows, liquidations), include
  the time of day if possible.
- Flag any data older than 7 days for fast-moving metrics or 90 days for
  slower structural metrics (developer activity, holder distribution).

---

## Common Methodology Pitfalls

**DefiLlama TVL** — includes borrowed assets in some protocol calculations.
Always note whether you're using "TVL" or "TVL excluding borrowed."

**Artemis DAUs** — counts unique active addresses, not unique humans.
One user with multiple wallets = multiple DAUs.

**Nansen "Smart Money"** — a proprietary label based on past performance
patterns. Not an objective category. Disclose when citing.

**Token Terminal Revenue** — "protocol revenue" typically means fees going
to the protocol treasury or token holders, not total fees paid by users.
Clarify which you mean.

**Glassnode MVRV** — market value to realized value ratio. Requires explaining
what "realized value" means before using on air with non-technical audiences.
