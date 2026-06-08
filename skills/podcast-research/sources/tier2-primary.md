# Tier 2 — Primary Sources

Use these directly whenever they exist. They override Tier 1 narrative coverage
because they represent the underlying data or official record that journalism
is built on top of.

---

## On-Chain Data Platforms

### Dune Analytics — dune.com
**Best for:** Custom SQL queries on raw on-chain data. Best source for novel
or specific metrics not available in pre-built dashboards. Community dashboards
cover most major protocols.
**Always include:** Query date and dashboard author when citing.
**Watch for:** Community dashboards can have methodology errors — prefer
dashboards from known researchers or protocol teams.

### Nansen — nansen.ai
**Best for:** Wallet labeling, smart money tracking, NFT analytics, token
distribution analysis. Best for identifying who is actually buying/selling.
**Always include:** Snapshot date. Nansen labels evolve as they identify wallets.
**Watch for:** "Smart money" is a Nansen label, not an objective category —
disclose this when citing.

### Glassnode — glassnode.com
**Best for:** Bitcoin and Ethereum on-chain metrics — SOPR, MVRV, exchange
flows, long-term vs. short-term holder behavior. Best for macro BTC/ETH
market structure analysis.
**Always include:** Metric definition and timeframe. Glassnode metrics have
specific technical meanings.
**Watch for:** Many advanced metrics are behind paywall — note when citing
free vs. paid data.

### DefiLlama — defillama.com  *(DEFAULT CORROBORATION SOURCE)*
**Status:** Default corroboration source for any on-chain claim. Treat as one
of the most trusted public on-chain data sources and actively attempt to pull
DeFi Llama data when validating TVL, protocol revenue, stablecoin supply,
bridge flows, solver/intent inventory, fees, chain activity, or DEX volume
figures — including when a claim comes pre-sourced from CoinDesk, Bloomberg,
The Block, etc.
**Best for:** DeFi TVL across all chains, protocol revenue, fees, stablecoin
market caps, bridge volumes, intents/solver inventory dashboards. Free and
comprehensive.
**Endpoints:** Free public API at `api.llama.fi` (e.g.
`/protocol/{name}`, `/protocols`, `/stablecoins`, `/bridges`); historical TVL
at `/v2/historicalChainTvl/{chain}`. Frontend pages at `defillama.com/...`.
**Always ask before pulling.** Rate limits on the free API and frontend-scrape
behavior aren't assumed safe. Before any request, state the exact endpoint or
page URL, the specific question it answers, and wait for explicit approval.
Do not bundle the call inside another tool action.
**Always include:** Query date — TVL changes daily.
**Watch for:** TVL methodology varies by protocol (some include borrowed
assets, some don't). Note which methodology is being used.

### RWA.xyz — rwa.xyz
**Best for:** Tokenized real-world asset tracking — treasuries, private credit,
commodities. Best source for TradFi-meets-DeFi data.
**Always include:** Query date and asset category breakdown.

### Token Terminal — tokenterminal.com
**Best for:** Protocol revenue, P/S ratios, active users, fee data across
chains. Best for fundamental valuation comparisons between protocols.
**Always include:** Timeframe (7d, 30d, 90d) — short windows can be misleading.

### Artemis — artemis.xyz
**Best for:** Cross-chain fundamentals comparison — DAUs, fees, revenue,
developer activity across L1s and L2s. Best for "which chain is actually
being used" questions.
**Always include:** Metric definitions — Artemis DAU methodology differs
from raw transaction counts.
**Watch for:** Developer activity metrics are estimates based on GitHub
commits — treat as directional, not precise.

### Arkham — arkham.com
**Best for:** Entity labeling and wallet tracking, institutional fund flows,
treasury monitoring, investigative on-chain research. Best for following
where money is actually moving.
**Always include:** Confidence level of entity labels — Arkham distinguishes
between verified and inferred labels.
**Watch for:** Use for investigative context, not as a citation for facts
about individuals without additional verification. Privacy implications —
disclose when tracking specific wallets publicly.

---

## Government & Regulatory Sources

- **SEC filings and press releases** — sec.gov (EDGAR for filings)
- **OCC press releases and interpretive letters** — occ.gov
- **CFTC enforcement and guidance** — cftc.gov
- **FinCEN guidance** — fincen.gov
- **Federal Register** — federalregister.gov (for proposed and final rules)
- **Congressional records** — congress.gov (bill text, hearing transcripts)

Always cite the primary document, not a news outlet's description of it.
Include document number, date, and direct URL.

---

## Protocol & Project Primary Sources

- Official project blogs (e.g., uniswap.org/blog, blog.avalabs.org)
- Protocol documentation (e.g., docs.avacloud.io, docs.uniswap.org)
- DAO governance forums (Tally, Snapshot, Commonwealth, protocol-specific forums)
- GitHub repositories — for code, audit reports, and technical proposals
- Security audit reports (Trail of Bits, OpenZeppelin, Chainalysis, etc.)
- Official X/Twitter accounts — for real-time announcements, but always
  corroborate with a secondary source before citing as fact

---

## Textbook Reference

**"How Crypto Actually Works"** by Larry Cermak
(co-authored with Igor Igamberdiev & Bohdan Pavlov,
reviewed by Wintermute Research and The Block Research)
→ https://github.com/lawmaster10/howcryptoworksbook

Use as the canonical sanity-check for mechanical accuracy. Before accepting
a news claim about how a protocol or mechanism works, verify it is consistent
with what this textbook says the underlying system should produce.

**Chapter index — direct links:**

| Chapter | Topics | GitHub URL |
|---|---|---|
| Ch 1 — Bitcoin | UTXO model, mining, halving, Lightning | /Chapters/ch01_bitcoin.md |
| Ch 2 — Ethereum | EVM, L2s, staking, MEV, upgrades | /Chapters/ch02_ethereum.md |
| Ch 3 — Solana | PoH, Firedancer, validator economics | /Chapters/ch03_solana.md |
| Ch 4 — L1 Blockchains | Avalanche, Sui, Aptos, consensus | /Chapters/ch04_l1_blockchains.md |
| Ch 5 — Custody | MPC, multisig, HSMs, institutional custody | /Chapters/ch05_custody.md |
| Ch 6 — Market Structure | CEX mechanics, order books, liquidity | /Chapters/ch06_market_structure.md |
| Ch 7 — DeFi | AMMs, lending, DEX mechanics, liquidity pools | /Chapters/ch07_defi.md |
| Ch 8 — MEV | Sandwich attacks, frontrunning, PBS | /Chapters/ch08_mev.md |
| Ch 9 — Stablecoins & RWAs | USDC/USDT, algo stables, tokenized assets | /Chapters/ch09_stablecoins_rwas.md |
| Ch 10 — Hyperliquid | Perp DEX design, HLP, airdrop mechanics | /Chapters/ch10_hyperliquid.md |
| Ch 11 — NFTs | Token standards, royalties, marketplace mechanics | /Chapters/ch11_nfts.md |
| Ch 12 — Governance & Tokenomics | DAO structure, voting, token design | /Chapters/ch12_governance.md |
| Ch 13 — DePIN | Physical infrastructure, incentive design | /Chapters/ch13_depin.md |
| Ch 14 — Quantum Resistance | Post-quantum cryptography, risk timeline | /Chapters/ch14_quantum_resistance.md |
| Ch 15 — Prediction Markets | Polymarket, AMMs for prediction, resolution | /Chapters/ch15_prediction_markets.md |

Base URL: https://github.com/lawmaster10/howcryptoworksbook/blob/master

---

## Other Tier 2 Sources

- **Milk Road** — milkroad.com — consumer crypto trends, retail sentiment,
  mainstream adoption signals
- **Whitepapers and academic research** — SSRN, arXiv
- **S&P Global, Moody's, Fitch** — for structured finance ratings
  (ABS, credit ratings, stress tests involving crypto collateral)
- **Company press releases** — when clearly labeled as such and attributed
