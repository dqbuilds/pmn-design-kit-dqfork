# Guest Archetypes — Brief Research Guide

Run `workflows/guest-diligence.md` for every guest. This file tells you
**which angles to prioritize, which traps to avoid, and which questions
are too easy to waste on each archetype.**

Named examples are real guests who represent each type.

---

## Archetype 1 — The TradFi Institutional
*e.g., Robbie Mitchnick (Head of Digital Assets, BlackRock)*

**What they are:** A senior exec at a legacy institution who now owns a
crypto mandate. They exist at the seam between tradfi bureaucracy and
crypto infrastructure. They can speak to both worlds but are disciplined
about what they commit to on record.

**What they've been asked to death:**
- "Why is BlackRock in crypto now?"
- "Is the ETF a turning point for institutional adoption?"
- "What does your internal approval process look like?"

These produce clean, PR-approved talking points. Do not ask them.

**Where the interesting questions live:**
- The infrastructure gap between what institutions need and what crypto
  actually provides. They've run into this wall — ask about specific
  constraints, not general "challenges."
- What their clients actually use crypto for vs. what the narrative says.
  Most institutional BTC exposure is allocation, not utility. What's
  the first utility use case they'd bet on?
- Internal politics: What's harder — convincing the regulators or
  convincing the risk committee? That answer reveals who's actually
  slowing this down.
- Where custody risk actually lives in a $10T AUM context. Coinbase
  custodies ~70% of BTC ETF AUM — ask if that concentration concerns them.

**Textbook chapters to load first:**
- Ch 5 (Custody) — understand MPC, multisig, HSM cold storage before
  you ask anything about how they hold assets
- Ch 6 (Market Structure) — understand authorized participants, in-kind
  creations, and ETF mechanics before any ETF question
- Ch 9 (Stablecoins/RWAs) — BUIDL, tokenized Treasuries, RWA market
  structure

**Counternarrative flags to check:**
- ETF custody concentration (is ~70% via Coinbase disclosed / discussed?)
- "Institutional adoption" language — ask for the specific product, not
  the category
- Attestation vs. audit distinction for any reserve discussion

**Q5 (adversarial) template for this archetype:**
> "If BlackRock's ETF custodian had a key management failure, what's the
> actual user protection mechanism — and is it the same as SIPC?"

---

## Archetype 2 — The Market Maker / Trading Firm
*e.g., Jake Ostrovskis (OTC Trading, Wintermute)*

**What they are:** Practitioners who operate inside the market microstructure
every day. They have proprietary views on liquidity, spreads, and venue
dynamics that don't appear in public reporting. They are also one of the
most over-represented guest types on crypto podcasts — the good interview
is the one where they say something they haven't said before.

**What they've been asked to death:**
- "What's your market making strategy?"
- "How do you think about risk management in crypto?"
- "What's the outlook for [current market condition]?"

**Where the interesting questions live:**
- The microstructure questions only someone who read Ch 6 and Ch 8 would
  know to ask: private orderflow concentration, how builder relationships
  affect execution quality, whether on-chain CLOBs are eating CEX volume
  in specific pairs
- What they actually won't trade and why — the constraints reveal more
  than the strategy
- The DeFi liquidity question: are they allocating HLP-style vault exposure?
  If not, why? If yes, what's the risk model for impermanent loss at
  institutional scale?
- The MEV question from their side: are they a searcher, a builder, or
  deliberately routing to avoid both? That answer tells you where they sit
  in the extraction chain

**Textbook chapters to load first:**
- Ch 6 (Market Structure) — deep, including basis trade, funding arb,
  RFQ mechanics, and mark price. This is their domain. You need to be
  fluent, not just literate.
- Ch 8 (MEV) — private orderflow (~12% of transactions, >54% of block
  rewards), PBS, searcher/builder dynamics
- Ch 7 (DeFi) — AMM mechanics, concentrated liquidity, intent-based
  systems, HLP vaults

**Counternarrative flags to check:**
- "Liquidity" is never uniform — ask about spreads on specific pairs at
  specific sizes, not the category
- Funding rate direction as sentiment proxy — but ask whether the signal
  is still clean when everyone is watching it
- TPS / volume figures that include wash trading

**Q3 (technical depth) template for this archetype:**
> "Walk me through what happens to your Solana order routing when vote
> transactions are excluded from the TPS figure — does that change how
> you model slippage on a high-load day?"

**Q4 (contested territory) template:**
> "Private orderflow is now more than half of Ethereum block rewards.
> Does that change your routing decisions, and what's the equilibrium
> where it stops growing?"

---

## Archetype 3 — The Crypto-Native VC / Analyst
*e.g., Haseeb Qureshi (Managing Partner, Dragonfly Capital) or
Sean Lippel (Framework Ventures)*

**What they are:** Investors with public theses who have made real bets
on their views. They are sharp, media-trained, and used to defending
portfolio positions. The risk is the interview becomes a long-form LP
pitch. The opportunity is they've done the research and will engage at
mechanism level if you match them there.

**What they've been asked to death:**
- "What are you most excited about in the current cycle?"
- "How do you think about valuation in crypto?"
- "What's your thesis on [category they've invested in]?"

These are the questions that produce polished thought-leadership content
for their fund. You are not LP Relations. Do not ask them.

**Where the interesting questions live:**
- The misses: what did they underwrite that turned out to be wrong at the
  mechanism level, not just the timing level? This requires them to engage
  with mechanism, not just narrative
- The Haseeb time-horizon framing works in reverse: what's the thesis that
  most people think is early-cycle but they think is already over?
- For Haseeb specifically: his published writing has made specific mechanistic
  claims about fee compression, L1 vs L2 value capture, and DeFi protocol
  revenue. Any claim he's made in writing is fair game as a direct follow-up
  if the market has since stress-tested it
- The structure of a crypto fund is itself interesting: what's their LP
  base, and how does institutional LP demand shape what they'll touch?
  Most won't disclose but the question itself reveals their comfort level

**Textbook chapters to load first:**
- Ch 12 (Governance & Token Economics) — fee switch, veTokens, buyback-
  and-burn, emissions dilution. Any token thesis depends on this.
- Ch 7 (DeFi) — especially real yield vs. emissions and protocol revenue
  metrics. Relevant for any DeFi portfolio company.
- Ch 4 (L1 Blockchains) — for any "Ethereum vs. Solana" or L1 value
  accrual discussions

**Counternarrative flags to check:**
- "First mover advantage" narratives in fast-moving protocol categories
- TVL as a portfolio metric — ask what % of their TVL claims would survive
  stripping incentivized liquidity
- "Category leader" framing — ask who the most dangerous competitor is,
  not who the current leader is

**Q2 (core thesis) template:**
> "What do most people in crypto fundamentally misunderstand about where
> protocol value actually accrues — at the L1 layer, the application layer,
> or somewhere else entirely?"

**Q5 (adversarial) template:**
> "Which of your active portfolio positions is most dependent on a bet that
> turns out to be wrong if Solana captures the application layer instead
> of Ethereum?"

---

## Archetype 4 — The Macro / Media Figure
*e.g., Anthony Scaramucci (Founder, SkyBridge Capital)*

**What they are:** A high-profile figure whose crypto views are shaped by
macro positioning and whose primary audience is the financial mainstream.
They provide air cover for institutional adoption narratives but often
lack mechanism-level fluency. The risk is the interview stays at
narrative altitude. The opportunity is using their macro framing to
expose the places where narrative and mechanism diverge.

**What they've been asked to death:**
- "Is Bitcoin the new gold?"
- "What's your Bitcoin price target?"
- "How should traditional investors size a crypto allocation?"

**Where the interesting questions live:**
- Where their macro framework breaks down: Bitcoin as "digital gold" fails
  as an inflation hedge on 6-month windows (it's historically more
  correlated to risk assets than gold during stress). Ask about the
  framework, not the conclusion.
- Their actual exposure mechanics: do they hold spot, ETF shares, or
  derivatives? The answer reveals whether their thesis matches their
  structure
- The political dimension: Scaramucci specifically has navigated
  Washington access in ways most crypto figures haven't. The regulatory
  path questions (stablecoin legislation, bank charter clarity) are more
  interesting from him than from a protocol founder because he understands
  the lobbying and political economy layer
- The redemption optionality: SkyBridge had significant FTX exposure.
  How they processed that operationally (risk management, LP relations,
  legal) is more interesting than the post-mortem narrative

**Textbook chapters to load first:**
- Ch 1 (Bitcoin) — security budget, halving mechanics, pseudonymity model.
  Don't let "digital gold" go unchallenged without understanding what
  Bitcoin's actual properties are vs. gold's.
- Ch 6 (Market Structure) — spot ETF mechanics, authorized participant
  dynamics, custody concentration

**Counternarrative flags to check:**
- "Digital gold" correlation claim — empirically weak on short horizons
- "Institutional adoption" language — always ask for the specific
  instrument and the specific use case
- Price prediction framing — redirect to mechanism

**Q3 (technical depth) template for this archetype:**
> "SkyBridge holds BTC exposure — is that through the ETF structure or
> direct custody, and does the authorized participant mechanism create
> any basis risk you think about?"

**Q4 (contested territory) template:**
> "Bitcoin's correlation to the Nasdaq during the 2022 drawdown was
> higher than gold's. How does that fit the store-of-value thesis —
> is the uncorrelation argument about a longer time horizon, or is
> it a claim you'd revise?"

---

## Archetype 5 — The DeFi Builder
*e.g., Hayden Adams (Founder, Uniswap), Stani Kulechov (Founder, Aave),
Robert Leshner (Founder, Compound / Superstate)*

**What they are:** Protocol founders who built the core DeFi primitives.
They are mechanism-fluent by necessity — they designed the thing. They are
also deeply incentivized to frame everything in terms of their own protocol's
narrative. The risk is the interview becomes a product roadmap walkthrough.
The opportunity is they'll actually engage with mechanism if you're precise
enough to make a vague answer feel inadequate.

**What they've been asked to death:**
- "How did you come up with the idea for [protocol]?"
- "Where do you see DeFi in five years?"
- "How do you think about competing with Coinbase / Binance?"
- "What's next on your roadmap?"

These produce origin myth + vision content. You are not a conference
moderator. Do not ask them.

**Where the interesting questions live:**
- The governance question they don't want to answer: does the DAO actually
  govern, or does the core team govern and the DAO ratifies? Ask about a
  specific governance decision that didn't go the way the core team expected.
  That answer reveals the real power structure.
- The fee switch / value accrual tension: for every major DeFi protocol,
  the question of whether the token captures value is live and contested.
  Ask about the specific mechanism — not whether they're bullish on the token.
- The MEV exposure: every AMM is a MEV surface. Ask how sandwich attack
  volume has changed since Uniswap v3/v4 hooks, or how they think about
  JIT liquidity crowding out passive LPs. Only someone who read Ch 7 and
  Ch 8 together would know to connect these.
- The real yield question: what percentage of protocol revenue goes to
  LPs vs. token holders vs. treasury, and what's the number after stripping
  emissions? That one question separates "real yield" from "emissions theater."
- Protocol-specific stress tests: ask about the worst day the protocol had
  — not the biggest hack in DeFi broadly, but the moment their specific
  design assumptions were tested hardest. The oracle manipulation events,
  the depeg incidents, the governance attacks. These are on public record.
  Use them.

**Textbook chapters to load first:**
- Ch 7 (DeFi) — deep, especially AMM mechanics, concentrated liquidity,
  hooks, impermanent loss, real yield vs. emissions, fee switch mechanics.
  This is their domain. Being imprecise here costs credibility.
- Ch 8 (MEV) — JIT liquidity, sandwich attacks, private orderflow, PBS.
  Every AMM founder has views here they haven't fully aired.
- Ch 12 (Governance & Token Economics) — DAO structure, veTokens, gauge
  voting, quorum mechanics, governance attacks. The governance question is
  almost always the most interesting one for this archetype.

**Counternarrative flags to check:**
- TVL as a health metric — ask what their TVL looks like ex-incentives
- "Decentralized" governance claims — ask about the last decision the
  DAO made that the core team disagreed with
- Real yield vs. emissions yield — get the breakdown before the interview
  so you can challenge a vague "sustainable yield" claim with actual numbers
- Uniswap specifically: the fee switch activation (late 2025) was the first
  time UNI holders received direct economic benefit. Ask what took so long
  and what the internal resistance was.

**Q3 (technical depth) template:**
> "Walk me through what actually happens to a passive LP position during a
> JIT liquidity attack — does v4's hook architecture change the calculus,
> or does the LP still lose the fee race?"

**Q4 (contested territory) template:**
> "What percentage of [Protocol] TVL do you think remains if you zero out
> the token incentive program tomorrow — and has that number changed since
> you launched?"

**Q5 (adversarial) template:**
> "What would a credibly decentralized version of [Protocol]'s governance
> actually look like — and is that something you want, or is it in tension
> with shipping product?"

---

## Archetype 6 — The Exchange Executive
*e.g., Brian Armstrong (CEO, Coinbase), Richard Teng (CEO, Binance),
Paul Grewal (CLO, Coinbase), Jesse Powell (Co-founder, Kraken)*

**What they are:** The operators who run the regulated-or-quasi-regulated
venues where the majority of crypto trading volume actually happens. They
sit at the intersection of product, regulatory compliance, and geopolitics
in ways no other archetype does. They are also the most media-trained
guests you will interview — they have comms teams and pre-approved answer
sets for every predictable question.

**What they've been asked to death:**
- "What's your reaction to the latest SEC / CFTC action?"
- "How do you think about competing with Binance?"
- "Is crypto regulated enough / too much?"
- "What does mainstream adoption look like?"

These produce lawyer-approved, on-brand non-answers. Do not ask them.

**Where the interesting questions live:**
- The custodial model: Coinbase custodies ~70% of BTC ETF AUM. That
  concentration is a systemic risk question that has nothing to do with
  Coinbase being good or bad — it's a structural fragility. Ask how
  they think about that concentration from the inside.
- The market structure conflict of interest: exchanges run the venue and
  the market maker simultaneously in many cases. Ask how they separate
  prop trading from customer order routing — this is the question that
  produces either a very precise answer or a very revealing non-answer.
- The stablecoin relationship: USDC's relationship with Coinbase (Circle
  co-founder, revenue share on reserves) is public but under-examined.
  Ask what happens to that revenue model when rates drop.
- The geographic arbitrage: Binance's regulatory fragmentation across
  jurisdictions is the most interesting story in exchange regulation.
  Ask Richard Teng specifically what legal entity a US user is actually
  counterparty to when they trade on Binance. The answer is more
  complicated than the marketing.
- The delisting question: every exchange has delisted tokens under
  regulatory pressure. Ask about a specific delisting — not the policy
  in general. The specific case reveals how the decision actually gets made.
- Post-FTX risk management: what changed operationally? Proof of reserves
  is now table stakes. Ask what they believe PoR actually proves — and
  what it doesn't. The attestation vs. audit distinction matters here
  (Ch 9 counternarrative flags).

**Textbook chapters to load first:**
- Ch 6 (Market Structure) — CLOB mechanics, maker/taker, perp funding,
  mark price, liquidation mechanics, OTC, dark pools. Their entire product
  surface lives here.
- Ch 5 (Custody) — MPC, multisig, HSM, cold/warm/hot wallet architecture.
  Custody is their core liability.
- Ch 9 (Stablecoins/RWAs) — attestation vs. audit, reserve composition,
  GENIUS Act implications. Every major exchange has a stablecoin relationship.

**Counternarrative flags to check:**
- Proof of reserves vs. proof of liabilities — PoR without liabilities
  proves nothing about solvency. Ask for both.
- "Regulated" language — ask which entity, which regulator, which
  jurisdiction. "Regulated exchange" can mean a CFTC-registered DCM or
  a Seychelles LLC with a license.
- Volume figures — exchange self-reported volume is notoriously
  unaudited. Ask about the methodology.
- The "institutional" narrative — ask what percentage of their revenue
  comes from retail vs. institutional and whether that's changed since 2022.

**Q3 (technical depth) template:**
> "Walk me through what your proof-of-reserves attestation actually covers —
> specifically, does it include liabilities, and is it a point-in-time
> snapshot or a continuous audit?"

**Q4 (contested territory) template:**
> "Coinbase custodies roughly 70% of BTC ETF AUM. From your position
> inside that concentration — is that a feature or a fragility, and
> who's responsible for managing the systemic risk that creates?"

**Q5 (adversarial) template:**
> "What's the specific scenario where your exchange's interests and
> your users' interests are in direct conflict — and what's the
> mechanism that resolves it in the user's favor?"

---

## Archetype 7 — The L1 / Infrastructure Founder
*e.g., Anatoly Yakovenko (Co-founder, Solana), Emin Gün Sirer (Founder, Ava Labs),
Silvio Micali (Founder, Algorand), Do Kwon-era cautionary parallels*

**What they are:** The people who made base-layer architectural bets —
consensus design, execution model, validator economics — and now have to
live with the tradeoffs in public. They are technically deeper than almost
any other guest type but also have the most reputational skin in the game.
Every question about their chain's weaknesses is also a question about
their judgment. That tension is where the interview lives.

**What they've been asked to death:**
- "Why did you build a new L1 instead of building on Ethereum?"
- "How does your TPS compare to Ethereum / Solana?"
- "What's the killer app for your chain?"
- "How do you think about decentralization vs. performance?"

These produce the same trilemma talking points every L1 founder has
memorized. Do not ask them.

**Where the interesting questions live:**
- The tradeoffs they chose not to mention in the whitepaper: every
  architectural decision has a cost they accepted. Solana accepted
  validator hardware concentration. Avalanche accepted subnet complexity.
  Ask about the specific cost, not the benefit.
- Validator economics and the superminority problem: on Solana, 19-22
  validators control enough stake to halt consensus. Ask the founder
  what the actual decentralization number is — not the validator count,
  but the superminority threshold. If they haven't read their own
  data, that's the story.
- Client diversity: Ethereum has multiple independent clients in
  production. Most other L1s have one codebase lineage. Ask what
  happens to their chain if a critical bug is found in the single
  reference client. Firedancer/Frankendancer is the right Solana
  analogy — ask where they are in that process.
- The slashing decision: Solana doesn't slash on mainnet. Ethereum
  does. Ask why. The answer reveals the security model philosophy.
- The upgrade cycle and governance: how does a protocol change actually
  get activated? Ask about a specific controversial upgrade and who
  had the decisive vote. The honest answer is rarely "the community."

**Textbook chapters to load first:**
- Ch 3 (Solana) — if guest is Anatoly: Alpenglow, superminority
  threshold, SIMD process, Frankendancer status, validator economics.
  Be precise — he will notice imprecision.
- Ch 4 (L1 Blockchains) — four planes, consensus tradeoffs, finality
  types, BFT families, parallel execution models. Load this for any L1
  founder regardless of chain.
- Ch 2 (Ethereum) — for comparison framing. Know slashing, inactivity
  leak, client diversity, and EIP process before any "vs. Ethereum" question.

**Counternarrative flags to check:**
- TPS figures: always theoretical maximum. Ask about sustained throughput
  under real load. Vote transactions inflate Solana's raw TPS figure —
  ask for user-transaction-only figures.
- "Decentralization" claims — ask for the superminority threshold number,
  not the total validator count.
- Client diversity claims — ask how many independent codebases are
  running on mainnet today, not how many are in development.

**Q3 (technical depth) template:**
> "Firedancer has been in development for years and Frankendancer went
> mainnet in late 2024 — but full Firedancer independence from Agave
> still isn't there. What's actually blocking it, and what does the
> client diversity picture look like in practice today?"

**Q4 (contested territory) template:**
> "Solana doesn't slash on mainnet. Every other major PoS chain treats
> slashing as fundamental to crypto-economic security. What's the actual
> argument for why reputation and opportunity cost are sufficient deterrents
> against a well-resourced attacker?"

**Q5 (adversarial) template:**
> "Walk me through the specific scenario where your chain halts — not
> a theoretical attack, but the realistic failure mode given your actual
> validator distribution and infrastructure concentration today."

---

## Archetype 8 — The Regulator / Policy / Legal
*e.g., Hester Peirce (SEC Commissioner), Jake Chervinsky (Variant Fund,
former policy lead), Brian Brooks (former Comptroller), Kristin Smith
(Blockchain Association)*

**What they are:** The people who either write the rules, interpret them,
or fight them on behalf of the industry. They speak in hedged, precise
language by professional necessity. The risk is the interview becomes a
regulatory briefing that produces no new information. The opportunity is
that policy guests have views on the gap between what the law says and
how it's enforced — and that gap is where the most interesting content
lives.

**What they've been asked to death:**
- "Is crypto regulated enough / too much?"
- "What's your reaction to the latest [agency] action?"
- "When will we get regulatory clarity?"
- "What does sensible crypto regulation look like?"

These produce prepared statements. Do not ask them.

**Where the interesting questions live:**
- The specific jurisdictional conflict: ask about a named case or
  rulemaking where two agencies claimed overlapping authority. The
  SEC vs. CFTC commodity/security boundary is the canonical one but
  the GENIUS Act's stablecoin preemption of state law is the live
  version. Ask which specific provisions they think will generate
  litigation first.
- The enforcement gap: there's a difference between what an agency's
  rules say, what they choose to enforce, and what the courts ultimately
  allow. Ask about a specific case where the enforcement action exceeded
  what the rule actually authorized. These guests know the cases.
- What the industry is actually asking for vs. what it claims to want:
  "regulatory clarity" is an industry demand that means different
  things to Coinbase, a DeFi protocol, and a stablecoin issuer. Ask
  which specific provision the guest believes the industry most actively
  lobbied against, and why.
- The international arbitrage: crypto firms choose jurisdiction. Ask
  which regulatory regime they'd describe as most coherent — not most
  favorable to industry, but most internally consistent. The answer
  is usually MiCA for stablecoins and Singapore/Dubai for spot exchanges,
  and why that is tells you something about the US approach.
- The revolving door: policy guests often move between government and
  industry. Ask directly: what did they change their mind about after
  moving to the industry side?

**Textbook chapters to load first:**
- Ch 9 (Stablecoins/RWAs) — GENIUS Act mechanics, reserve requirements,
  MiCA framework, attestation vs. audit. Stablecoins are the most active
  regulatory battleground.
- Ch 5 (Custody) — National Trust Bank Charter vs. full banking license
  distinction. This trips up everyone in policy discussions.
- Ch 6 (Market Structure) — ETF mechanics, spot vs. derivatives
  jurisdiction (SEC vs. CFTC), OTC and RFQ regulatory treatment.

**Counternarrative flags to check:**
- "Regulatory clarity" language — ask what specific legal question
  they want answered, not the category
- National Trust Bank Charter vs. full commercial banking license —
  these are not the same thing. The OCC charter BitGo received does
  not authorize FDIC-insured deposits or lending.
- "The industry wants X" framing — ask which part of the industry,
  because stablecoin issuers, DeFi protocols, and exchanges have
  directly conflicting regulatory interests.

**Q3 (technical depth) template:**
> "The GENIUS Act requires reserve backing and redemption procedures
> but doesn't explicitly resolve whether algorithmic stablecoins are
> covered. What's the enforcement theory if an algo stablecoin depeg
> happens under the new framework — does the issuer have liability?"

**Q4 (contested territory) template:**
> "The OCC national trust bank charter covers fiduciary activities —
> custody, stablecoin issuance, reserve management — but doesn't
> authorize deposit-taking or lending. Several exchanges have publicly
> called this 'full banking access.' Is that an accurate characterization
> of what the charter actually does?"

**Q5 (adversarial) template:**
> "What's the regulatory provision that crypto says it wants but that
> would actually harm the industry if it passed — the thing where the
> stated preference and the real interest diverge?"

---

## Archetype 9 — The Bitcoin Native / OG
*e.g., Michael Saylor (Strategy), Nic Carter (Castle Island Ventures),
Saifedean Ammous (The Bitcoin Standard), Pierre Rochard (Riot Platforms)*

**What they are:** Guests whose entire worldview is organized around
Bitcoin as the singular important crypto asset. They range from
Austrian-economics-adjacent monetarists (Saylor, Ammous) to technically
grounded analysts (Nic Carter) to mining-side practitioners (Rochard).
What they share: adversarial relationship to altcoin narratives, deep
familiarity with Bitcoin's technical and monetary properties, and
well-rehearsed answers to every softened version of the hard questions.

**What they've been asked to death:**
- "Why Bitcoin and not [alt]?"
- "What's your price target?"
- "What do you say to critics who call Bitcoin a Ponzi?"
- "How does Bitcoin fix [problem]?"

The first three produce the rehearsed adversarial lecture. The fourth
produces a 45-minute detour. Do not ask any of them.

**Where the interesting questions live:**
- The security budget: Bitcoin's block subsidy halves every four years.
  In 2024, it was ~94% of miner revenue. Around 2140, it goes to zero
  and miners earn only fees. The security model post-subsidy is the most
  contested long-term question in Bitcoin — and most Bitcoin-native guests
  have practiced but not fully stress-tested answers for it. Ask what fee
  revenue level is required to maintain current hash rate, and what that
  implies about what a Bitcoin transaction will cost in 2050.
- Lightning adoption numbers vs. narrative: the Lightning Network is
  Bitcoin's primary payment scaling solution. Ask for the actual public
  capacity figure, the routing success rate for payments above a threshold,
  and whether custodial Lightning (Strike, Cash App) counts as
  self-sovereign payment. These are mechanistically precise questions that
  separate prepared talking points from genuine engagement.
- The quantum vulnerability of legacy addresses: P2PK addresses with
  exposed public keys (pre-SegWit, Satoshi's coins, early miners) are
  vulnerable to harvest-now-decrypt-later quantum attacks. A migration
  requires a hard fork. Ask when they think the migration needs to happen
  and who has the legitimacy to coordinate it.
- The Ordinals / BRC-20 tension: the Bitcoin block space debate is real
  — inscription data competes with financial transaction throughput and
  fee revenue for miners. Ask whether they view Ordinals as a feature
  (fee revenue, cultural expansion) or a bug (block space pollution,
  mission drift). Nic Carter and Saylor have publicly different views.
- For Saylor specifically: the convertible note arbitrage that enables
  Strategy's accumulation model depends on stock volatility making
  conversion options valuable. Ask what happens to the model if MSTR
  stock volatility compresses toward BTC volatility directly.

**Textbook chapters to load first:**
- Ch 1 (Bitcoin) — all of it, deeply. Security budget, halving, UTXO
  model, address types, CoinJoin, BIP process, fork types, UASF history.
  These guests will notice if you're imprecise about Bitcoin mechanics.
- Ch 14 (Quantum Resistance) — Shor's algorithm, harvest-now-decrypt-later,
  P2PK address exposure, ECDSA vulnerability, migration path requiring
  hard fork.
- Ch 6 (Market Structure) — for Saylor: ETF authorized participants,
  convertible note mechanics, DAT trend.

**Counternarrative flags to check:**
- Halving reduces supply issuance, not demand — price appreciation
  requires buyer pressure, not just supply reduction.
- "Digital gold" correlation: empirically weak on 6-month windows during
  risk-off events. Bitcoin has historically correlated more with Nasdaq
  than gold during drawdowns.
- Lightning Network routing success rates and capacity figures are
  publicly available — don't let narrative substitute for the number.
- Saylor's "no liquidation risk" framing: technically true (no margin
  call on the convertible notes) but Strategy could still face dilution
  pressure or refinancing risk at the wrong time.

**Q3 (technical depth) template:**
> "Bitcoin's security budget in 2024 was roughly 94% block subsidy and
> 6% fees. What fee revenue level per block do you think is necessary to
> maintain current hash rate once the subsidy is materially smaller —
> and what does that imply about transaction costs?"

**Q4 (contested territory) template:**
> "Satoshi's coins and early P2PK outputs have exposed public keys —
> they're the addresses most vulnerable to a quantum attack under the
> harvest-now-decrypt-later threat model. A migration requires a hard
> fork. Who coordinates that, and what's the timeline before you'd say
> it becomes urgent?"

**Q5 (adversarial) template:**
> "The convertible note arbitrage that lets Strategy issue near-zero-
> coupon debt depends on MSTR volatility being high enough to make the
> conversion option valuable. What happens to the capital formation model
> if MSTR vol compresses toward Bitcoin's own realized volatility?"

---

## Archetype 10 — The Prediction Markets Developer
*e.g., Shayne Coplan (Founder, Polymarket), Jack Clark (Manifold Markets),
UMA Protocol team, Gnosis / Conditional Tokens team*

**What they are:** Builders who've made the technical and product bets
on information markets as a coordination primitive. They have strong views
on mechanism design (AMM vs. CLOB, LMSR vs. order book), oracle architecture,
and the regulatory line between prediction markets and gambling. The risk
is the interview becomes a Polymarket success story. The opportunity is
that the mechanism questions in this space are genuinely unsolved and
these builders have operational views on them.

**What they've been asked to death:**
- "How did the 2024 election validate prediction markets?"
- "Are prediction markets better than polls?"
- "When will prediction markets be legal everywhere?"

**Where the interesting questions live:**
- Oracle design is the primary attack surface: every prediction market
  lives or dies on resolution. Ask about a specific contested resolution
  — not the general design, but what happened when the outcome was
  genuinely ambiguous. The CFTC vs. Kalshi case on political events
  is one. Polymarket's US election market with hundreds of millions in
  OI resolving correctly but narrowly is another.
- Manipulation and market depth: a thin prediction market can be
  manipulated for reputational or hedging purposes at a cost that's
  cheap relative to the decision being influenced. Ask what depth is
  required before a market becomes manipulation-resistant, and what
  their thinnest meaningful market has been.
- The MEV surface in prediction markets: binary event resolution creates
  a known oracle-front-running opportunity. In the blocks before a market
  resolves, anyone with early information can trade. Ask how they've
  thought about this in design or observed it in practice.
- Conditional markets and the combinatorial explosion: conditional
  markets ("if X wins, what will Y do?") are theoretically the most
  useful information structure but the hardest to make liquid. Ask why
  the liquidity doesn't aggregate on conditional markets and what the
  design fix is.
- The regulatory line: Kalshi is CFTC-regulated as a DCM. Polymarket
  blocked US users. Ask what the specific legal theory is that draws the
  line between a prediction market contract and a gambling product —
  and whether they think that line is coherent.

**Textbook chapters to load first:**
- Ch 15 (Prediction Markets) — all of it: LMSR, binary vs. scalar vs.
  conditional markets, resolution oracle design, Polymarket architecture,
  UMA optimistic oracle, Augur/Gnosis failure analysis, Kalshi regulatory
  path.
- Ch 8 (MEV) — oracle front-running as a specific MEV vector. Resolution
  events create known information asymmetry windows.
- Ch 7 (DeFi) — intent-based systems and RFQ designs, relevant to how
  prediction market liquidity is sourced.

**Counternarrative flags to check:**
- "Prediction markets beat polls" framing — empirically, they're more
  accurate on average but the 2024 US election was within the margin
  where the statement is not falsifiable. Ask for the specific accuracy
  metric and sample.
- "Decentralized oracle" claims — UMA's optimistic oracle is decentralized
  in governance but centralized in that a small dispute-resolution
  community makes contested calls. Ask what percentage of resolutions
  are actually disputed.

**Q3 (technical depth) template:**
> "UMA's optimistic oracle assumes disputes are rare — but the incentive
> to front-run a resolution event scales with OI. At what OI level does
> the economics of an oracle manipulation attack become rational, and what
> changes in your architecture at that scale?"

**Q4 (contested territory) template:**
> "Polymarket had hundreds of millions in OI on the 2024 US election.
> A sophisticated actor could have bought a position and then spent a
> fraction of that on influence operations to move the underlying outcome.
> How do you think about the hedge-your-bet attack surface, and at what
> market depth does it become too expensive to run?"

**Q5 (adversarial) template:**
> "What's the class of real-world events that prediction markets will
> never be able to price accurately — and is that a design limitation
> or a fundamental property of information markets?"

---

## Archetype 11 — The Privacy Developer / Advocate
*e.g., Zooko Wilcox (Zcash / ECC), Ying Tong (Ethereum Privacy R&D),
Roman Storm (Tornado Cash developer), Paul Brody (EY Blockchain),
Aztec Protocol team, Aleo team*

**What they are:** Builders and researchers working on programmable
privacy — either at the protocol layer (ZK proofs, MPC, confidential
transactions) or the application layer (mixers, private smart contracts,
confidential DeFi). They sit at the most legally exposed position in
crypto: the same technology that enables financial privacy enables
sanctions evasion, and regulators have used this conflation aggressively.
The interview has to hold both the technical and the political dimensions
simultaneously.

**What they've been asked to death:**
- "Is privacy a right?"
- "How do you respond to people who say you're helping criminals?"
- "Does crypto need to comply with AML?"

These produce philosophical position statements. Do not ask them.

**Where the interesting questions live:**
- The cryptographic distinction between privacy and anonymity: ZK proofs
  prove knowledge without revealing the underlying data. That's not the
  same as making something untraceable — it's making something selectively
  disclosable. Ask how they distinguish the two in their own design, and
  what "regulatory auditability" actually means in a ZK context. Token-2022
  on Solana has confidential transfers with auditor keys built in — ask
  whether that's the right design compromise.
- The Tornado Cash legal theory: the US Treasury sanctioned a smart
  contract, not a person or company. The code is now on the OFAC SDN list.
  Ask whether their own protocol's architecture would survive the same legal
  theory — specifically, what makes their design different from Tornado Cash
  in a way that matters legally, not just technically.
- The compliance-privacy tension in practice: EY has worked on enterprise
  blockchain with privacy features. The design tension between FATF travel
  rule compliance (counterparty identification) and cryptographic privacy
  is real and unresolved. Ask what a compliant private transaction actually
  looks like end-to-end.
- The ZK proof trust assumptions: ZK proofs are only as strong as the
  setup ceremony (for SNARKs) or the cryptographic assumptions underlying
  the scheme. Ask what the failure mode looks like if a trusted setup is
  compromised, or what the quantum attack surface is on their proving system.
- For Zooko specifically: the Zcash t-address vs. z-address adoption split
  is public data. The majority of Zcash transactions use transparent
  addresses. Ask why, and what that says about the demand for on-chain
  privacy when it requires active opt-in.

**Textbook chapters to load first:**
- Ch 14 (Quantum Resistance) — ZK proving systems have their own quantum
  attack surface depending on which cryptographic assumptions underlie them.
  Post-quantum ZK is an active research area.
- Ch 1 (Bitcoin) — CoinJoin privacy model, pseudonymity vs. anonymity,
  Chainalysis de-anonymization. The baseline privacy model to contrast against.
- Ch 2 (Ethereum) — account abstraction and EIP-7702 implications for
  privacy. ZK rollup trust assumptions.
- Ch 3 (Solana) — Token-2022 confidential transfers with auditor keys as
  a specific design example of compliance-privacy balance.

**Counternarrative flags to check:**
- "Trustless privacy" claims: ZK-SNARKs with trusted setup ceremonies
  are not trustless. Ask about the specific setup and what it assumes.
- "Compliant by design" claims: ask what specific compliance requirement
  they satisfy and what a regulator would need to verify a transaction.
- The Zcash adoption data: if the protocol is designed for privacy but
  most transactions are transparent, ask what that reveals about user
  demand and adoption barriers.

**Q3 (technical depth) template:**
> "Token-2022's confidential transfers include an auditor key that lets
> a designated party view transaction amounts while they remain hidden
> on-chain. Is that the right architectural answer to the FATF travel
> rule problem — and does it require trusting the auditor key holder the
> same way you'd trust a bank?"

**Q4 (contested territory) template:**
> "The Treasury sanctioned Tornado Cash's smart contract, not a person.
> Your protocol also processes transactions without counterparty identification.
> What's the specific architectural or legal distinction that means your
> code wouldn't be subject to the same theory — and has your legal team
> stress-tested that argument?"

**Q5 (adversarial) template:**
> "The majority of Zcash transactions use transparent addresses, not
> shielded ones. If users aren't opting into privacy when it's available
> for free, what does that say about the actual market demand for
> cryptographic financial privacy — and does it change how you think
> about where to put the default?"

---

## Archetype 12 — The Hyperliquid Builder
*e.g., Hyperliquid core team (Jeff Yan / pseudonymous founders),
TradeXYZ / Unit team, Felix Protocol, Ventuals, Trove,
HyperEVM application developers*

**What they are:** Two distinct sub-types now exist under this archetype
and they require different prep:

**Core infrastructure builders** (Hyperliquid foundation, HyperBFT
validator operators) — focused on protocol mechanics, governance, and
the decentralization path.

**HIP-3 front-end deployers** (TradeXYZ/Unit, Felix Protocol, Ventuals,
Trove) — teams that staked 500K HYPE (~$19-25M at various points) to win
a Dutch auction slot and deploy permissionless perp markets. They are
building the distribution layer for equities, metals, FX, and custom
indices on top of HyperCore's matching engine. Their questions are about
oracle design, collateral choices, cold-start liquidity, and getting
non-crypto-native users through the wallet UX problem.

Since October 2025, HIP-3 has become the primary growth story in on-chain
derivatives: within three months, HIP-3 markets captured over $1B in open
interest and ~$25B in total trading volume. The single-day record was $5.2B
on February 5, 2026, driven almost entirely by precious metals trading as
gold broke $5,000/oz and silver broke $100. TradeXYZ's silver contracts
alone accounted for the majority of that volume. This is no longer a
crypto-perps story — it is a traditional asset access story.

**What they've been asked to death:**
- "How does Hyperliquid compare to dYdX / GMX?"
- "What's your take on Hyperliquid's decentralization?"
- "How did HYPE's fair launch change the airdrop meta?"
- "What's the TAM for tokenized equities on-chain?" [now every interview]

**Where the interesting questions live:**

*For HIP-3 front-end deployers (TradeXYZ, Felix, Ventuals):*
- The oracle is the whole game: HIP-3 markets don't have foundation-
  controlled price feeds. Each deployer sources their own oracle.
  TradeXYZ uses one stack; Felix uses HyperStone (RedStone's dedicated
  HIP-3 oracle, ~2.5-3 second update cadence, three-tier architecture
  with primary/fallback price states). Ask what happens to a live position
  during a price feed failure — is there a circuit breaker, who can
  activate it, and what does HLP exposure look like during the gap?
- Collateral denomination as competitive strategy: TradeXYZ denominates
  markets in USDC; Felix uses USDH (their own stablecoin), offering 20%
  lower taker fees and 50% higher rebates as a result. Ask what the actual
  user behavior difference looks like between USDC and USDH markets in
  practice, and whether the fee structure changes liquidity depth or just
  attracts arbitrageurs.
- The cold-start problem is real: five markets still dominate Hyperliquid
  volume. The vast majority of HIP-3 markets outside XYZ100 (Nasdaq
  proxy) and the metals markets have thin natural flow. Ask what the
  deployer's actual market-making arrangement looks like — who is
  providing liquidity on day one, and what the arrangement costs.
- The non-crypto distribution wall: the Felix founder put it plainly —
  non-crypto-native users don't want wallet complexity. The builder code
  architecture allows Privy-style embedded wallets integrated into a
  Bloomberg or brokerage-style interface. Ask which distribution partners
  are in conversations and what the regulatory precondition is for a
  traditional finance front-end to route order flow to Hyperliquid.
- The metals thesis specifically: gold and silver on HIP-3 weren't a
  deliberate product decision — they emerged organically as global macro
  events (gold at $5,000, silver at $100, geopolitical stress) drove
  traders to the only 24/7 venue. Ask whether the team built for this
  or responded to it, and what the oracle infrastructure looked like
  during the February 5 volume spike.
- The HYPE tokenomics flywheel and its overhang: every HIP-3 deployer
  stakes 500K HYPE, removing it from circulation and creating structural
  buy pressure. But team token unlocks started November 2025 at roughly
  $200M/month. Ask how the deployer thinks about that supply overhang
  against the buyback and burn mechanics from fee revenue.

*For core infrastructure builders:*
- The JELLY incident as governance precedent: validators decided to
  delist and settle at a specific price within hours, without a
  governance vote. Ask what the decision-making process looked like
  in real time and whether that emergency governance path is now
  formalized or still ad hoc.
- HLP exposure to HIP-3 markets: HLP is counterparty of last resort
  across all markets including HIP-3 permissionless ones. Ask whether
  HLP has different position concentration limits for HIP-3 markets
  vs. foundation-operated markets, and how those limits are enforced
  when an oracle fails on a thin market.
- The validator set and decentralization path: foundation still controls
  validator onboarding as of early 2026. Ask what the specific milestones
  trigger permissionless validator entry.
- HyperEVM mainnet and composability risk: HyperEVM launched on mainnet
  March 2026. Asset linking lets Core spot assets flow into HyperEVM DeFi
  without wrapped tokens. Ask what happens to Core order book state if
  an HyperEVM application creates a position that affects Core liquidity
  in the same block — is the sequencing deterministic?

**Textbook chapters to load first:**
- Ch 10 (Hyperliquid) — all of it, deeply. HyperBFT, HyperCore,
  HyperEVM, dual block architecture, asset linking, HLP design, JELLY
  manipulation, HIPs governance, validator control. This is the only
  chapter that covers this ecosystem directly.
- Ch 6 (Market Structure) — perp mechanics, funding rates, mark price,
  liquidation mechanics, CLOB design. Also load the RWA and tokenized
  equity section from Ch 9 — equities and metals perps on HIP-3 are
  the growth edge of this ecosystem right now.
- Ch 8 (MEV) — oracle front-running as the primary MEV vector on HIP-3.
  Builder codes create a front-end incentive layer; understand how that
  interacts with the order routing stack.
- Ch 9 (Stablecoins/RWAs) — tokenized equities and the RWA framework.
  HIP-3 equity perps are a different legal and structural instrument than
  tokenized stocks on Solana (e.g., xStocks), but the regulatory question
  is adjacent.

**Counternarrative flags to check:**
- "24/7 equity trading" framing: HIP-3 equity markets are perpetual
  futures referencing a stock price — not actual stock ownership. Ask
  what rights the holder has if the oracle goes dark during a corporate
  event (earnings, halts, delistings).
- "Fully decentralized" claims: validator set entry is still foundation-
  controlled. Ask for the current validator count and what permissionless
  entry actually requires.
- Volume figures during the February 2026 metals spike: TradeXYZ silver
  contracts reported extraordinary single-day volumes. Ask what the open
  interest was relative to volume — a high volume/OI ratio can indicate
  wash trading or very short-term positioning rather than sustained
  directional interest.
- HYPE tokenomics: fair launch narrative is accurate (no VC allocation),
  but team unlocks at ~$200M/month started November 2025. The buyback
  and burn from HIP-3 fees runs against this supply. Ask what the net
  HYPE flow has looked like since unlocks started.

**Q3 (technical depth) template — HIP-3 deployer:**
> "Walk me through what happened to your oracle feed on February 5 when
> silver volume spiked — what's the fallback if HyperStone's primary
> price state diverges from the backup by more than the 1% rejection
> threshold, and what does that gap mean for open positions?"

**Q3 (technical depth) template — core infrastructure:**
> "HyperEVM launched on mainnet in March 2026. Asset linking means Core
> spot positions and EVM DeFi positions share the same underlying supply.
> Walk me through what happens to the Core order book if an HyperEVM
> contract atomically moves a large position in the same HyperBFT slot
> — is the sequencing deterministic, and who resolves a conflict?"

**Q4 (contested territory) template:**
> "HIP-3 equity markets are perps referencing a stock price — not stock
> ownership. If the oracle goes dark during an earnings halt or trading
> suspension, what's the settlement mechanism, who decides the reference
> price, and what's the user's recourse? Walk me through a specific
> failure scenario."

**Q5 (adversarial) template:**
> "The distribution problem for non-crypto-native equity traders is
> fundamentally a regulatory and UX problem — wallet complexity and no
> regulatory cover for a traditional broker to route to Hyperliquid.
> What has to happen legally before a Bloomberg terminal or retail
> brokerage can list your market as a venue, and which regulator's
> approval matters most?"

---

## Archetype 13 — The Solana Builder
*e.g., Meow (Jupiter Exchange), Tristan Frizza (Zeta Markets / Drift),
Anatoly's application-layer ecosystem, Pump.fun team, Armani Ferrante
(Backpack / Coral / Anchor)*

**What they are:** Founders and engineers building production applications
on Solana — DEX aggregators, perp exchanges, wallets, launchpads, token
infrastructure. They have operational views on Solana's performance
characteristics, MEV landscape, and developer experience that don't appear
in protocol documentation. They've also lived through the outages, the
Jito dynamics, and the memecoin cycle firsthand.

**What they've been asked to death:**
- "Why did you build on Solana instead of Ethereum?"
- "What's it like building on Solana vs. EVM?"
- "Is Solana ready for institutional DeFi?"

**Where the interesting questions live:**
- The dropped transaction problem in practice: Solana's local fee markets
  are theoretically isolated, but the 2024-2025 spam events caused global
  performance degradation. Ask what their application's dropped transaction
  rate looked like during those events and how they mitigated it — not
  the protocol-level fix, the application-level workaround.
- The Jito relationship: most production Solana applications now route
  through Jito for bundle inclusion. Ask what the Jito tip economics look
  like for their specific use case — how much are they paying, to whom,
  and what would break if Jito changed its fee structure.
- The BAM/Harmonic implications: Jito's Block Assembly Marketplace puts
  transactions in TEEs before ordering, which prevents validators from
  front-running but changes the bundle submission mechanics. Ask whether
  BAM changes their MEV protection strategy or their routing architecture.
- The Anchor framework and program security: Anchor automates a lot of
  safety checks but logic bugs still get through. Ask about a specific
  edge case in their program's account validation that Anchor didn't catch
  and they had to handle manually.
- Alpenglow and what changes for application builders: 100-150ms finality
  vs. current 12.8s changes what's possible for UX. Ask what specific
  product features they'd build that are currently impossible at 12.8s
  finality — and whether the simulation numbers are sufficient to start
  building against now.

**Textbook chapters to load first:**
- Ch 3 (Solana) — all of it. SVM, local fee markets, Gulf Stream, Turbine,
  Jito, BAM, Harmonic, Raiku, Alpenglow, Firedancer/Frankendancer, SPL
  tokens, ATAs, state compression. Application builders live inside all
  of these systems.
- Ch 7 (DeFi) — AMM mechanics, intent-based systems, bonding curves,
  Pump.fun model, concentrated liquidity. Most Solana builders are
  building DeFi applications.
- Ch 8 (MEV) — Jito-Solana's bundle auction system is the Solana-specific
  MEV infrastructure. Understand how it differs from Ethereum's PBS model.

**Counternarrative flags to check:**
- TPS claims: always ask for user transaction TPS excluding vote
  transactions, at actual sustained load, not theoretical maximum.
- "Sub-second finality" framing: economic finality is fast; Alpenglow's
  100-150ms is from simulations, not mainnet. Current guaranteed finality
  is 12.8s. Distinguish them.
- Pump.fun "no rug" framing: the bonding curve prevents LP withdrawal
  during the curve phase, but graduated tokens on PumpSwap have all
  the standard liquidity risks.

**Q3 (technical depth) template:**
> "Walk me through what your dropped transaction rate looked like during
> the worst congestion event you hit — what was the application-level
> fix, and how does BAM's TEE-based ordering change whether that problem
> recurs?"

**Q4 (contested territory) template:**
> "Alpenglow's finality numbers are from simulation, not mainnet — and
> DoubleZero's dedicated fiber isn't available to most validators yet.
> Are you building product features that depend on sub-200ms finality,
> and if so, what's your fallback if mainnet Alpenglow ships at 400ms
> rather than 150ms?"

**Q5 (adversarial) template:**
> "The Jito tip market gives validators a revenue stream that's partly
> disconnected from standard priority fees. If Jito changes its fee
> structure or the foundation changes the MEV policy, what breaks in
> your application's economics — and do you have a routing alternative?"

---

## Archetype 14 — The Ethereum Builder
*e.g., Vitalik Buterin (Ethereum Foundation), Justin Drake (EF researcher),
Jesse Pollak (Base / Coinbase), Steph Orpi (Arbitrum), Karl Floersch
(Optimism), Ryan Berckmans (Ethereum community)*

**What they are:** Core researchers, rollup founders, and application
builders who are either defining Ethereum's roadmap or building production
systems inside it. This is the most technically heterogeneous archetype —
Vitalik discussing account abstraction research and Jesse Pollak discussing
Base's sequencer economics are both "Ethereum builders" but require
completely different preparation. Split by layer before writing questions:
core protocol (EF researchers), execution layer (rollup operators), and
application layer (protocol founders building on L2s).

**What they've been asked to death:**
- "Is Ethereum still the most important blockchain?"
- "When will gas fees be low enough for mainstream adoption?"
- "What's Ethereum's roadmap?"
- "How do you think about the Solana competition?"

**Where the interesting questions live:**

*For core protocol researchers (Vitalik, Justin Drake):*
- The rollup endgame and sequencer decentralization: most rollups today
  have a single centralized sequencer with a 7-day fraud proof window
  for optimistic rollups. Ask when a major rollup will have a fully
  permissionless sequencer, and what the specific technical blocker is.
- Account abstraction and the EIP-7702 tradeoff: smart contract wallets
  can do things EOAs can't (batch transactions, sponsored gas, social
  recovery) but they're also harder to reason about from a security
  model standpoint. Ask about the specific attack surface that EIP-7702's
  delegation model creates and how Pectra's design addresses it.
- The blob economics: EIP-4844 introduced blobs that are pruned after
  ~18 days. Ask what happens to rollup security models if blob data
  disappears before a fraud proof window closes — and whether the
  blobspace pricing model is actually creating the data availability
  market that was envisioned.
- The restaking concentration question: EigenLayer has several billion
  dollars restaked. Ask what the systemic risk is if a single large
  AVS has a slashing event, and what the correlation between AVS slashing
  and Ethereum base layer security actually looks like.

*For rollup operators (Jesse Pollak, Steph Orpi, Karl Floersch):*
- Sequencer revenue and the decentralization incentive problem: rollup
  operators earn sequencer fees. Decentralizing the sequencer reduces
  that revenue concentration. Ask directly: what's the financial incentive
  to decentralize a profitable sequencer, and what forces the timeline?
- The interoperability stack: OP Stack, Arbitrum Orbit, and ZK Stack all
  have different approaches to cross-rollup communication. Ask what the
  state of cross-rollup liquidity fragmentation is in practice for their
  users and what the design fix looks like on their specific stack.
- The validium / training wheels question: many ZK rollups launched with
  admin keys that can override the proof system. Ask when those training
  wheels come off, what the specific condition triggers it, and who
  makes that decision.

**Textbook chapters to load first:**
- Ch 2 (Ethereum) — deep: EVM, EIP process, PoS mechanics, slashing,
  inactivity leak, BLS signatures, liquid staking, rollup mechanics
  (optimistic and ZK), blobs, EIP-4844, restaking, EigenLayer, AVS
  design. This is the most technically dense chapter. Load it fully.
- Ch 4 (L1 Blockchains) — modular architecture, four planes, DA solutions,
  Celestia vs. EigenDA vs. Ethereum DA. Relevant for rollup design choice.
- Ch 8 (MEV) — PBS, MEV-Boost, Flashbots, private orderflow. Rollup
  sequencer design inherits MEV dynamics from Ethereum but in a
  modified form — sequencers extract their own MEV unless constrained.

**Counternarrative flags to check:**
- "Decentralized rollup" claims: ask about the sequencer, the fraud
  proof system, and the admin key status specifically. Most rollups
  are not fully decentralized on all three dimensions.
- "Training wheels" on ZK rollups: many ZK proofs launched with
  override keys. Ask for the current status of the safety multisig.
- Blob pruning vs. data availability: blobs are pruned after ~18 days.
  Ask what the DA guarantee actually is for a rollup that relies on
  Ethereum blobs and has a 7-day fraud proof window.
- EigenLayer restaking yield: most of the current incremental restaking
  yield comes from incentive programs, not durable AVS fee revenue.
  Ask what percentage of their restaking yield is from protocol
  emissions vs. real AVS fees.

**Q3 (technical depth) template — core researcher:**
> "EIP-4844 blobs are pruned at roughly 18 days, but Optimism's fraud
> proof window is 7 days. If blob data for a disputed transaction batch
> disappears before the fraud proof resolves, what's the fallback —
> and does that create a window where a rollup operator could commit
> fraud and rely on data unavailability to avoid challenge?"

**Q3 (technical depth) template — rollup operator:**
> "Your sequencer currently earns the MEV and priority fees before they
> hit the L1. What's the design that prevents you from front-running your
> own users' transactions — and is it enforced at the protocol level or
> just a policy commitment right now?"

**Q4 (contested territory) template:**
> "Most of EigenLayer's current restaking yield comes from incentive
> programs rather than durable AVS fee revenue. If you strip emissions
> from the yield figure, what does restaking actually earn today — and
> at what point does the yield become real rather than speculative?"

**Q5 (adversarial) template:**
> "What's the specific sequence of events where Ethereum loses application
> layer dominance to Solana — not 'if Ethereum fails' but the realistic
> market share erosion path — and what in the current roadmap actually
> addresses it?"

---

## Archetype 15 — The Stablecoin Infrastructure Provider
*e.g., Jeremy Allaire (Circle), Paolo Ardoino (Tether), Walter Hessert (Paxos),
Nir Kshetri (Agora)*

**What they are:** Executives running the plumbing behind the largest dollar-
denominated assets in crypto. Circle and Tether together are the dominant
dollar settlement layer for the entire industry. Paxos issues PYUSD for PayPal
and has operated under NY DFS oversight. This archetype sits at the
intersection of monetary policy, payment infrastructure, banking relationships,
and sovereign risk — and they have prepared answers for almost everything
except the mechanism questions.

**What they've been asked to death:**
- "How do you think about the stablecoin market opportunity?"
- "How does USDC / USDT differ from a bank deposit?"
- "What does the GENIUS Act mean for your business?"
- "Are stablecoins a threat to the dollar?"

**Where the interesting questions live:**
- The reserve composition and yield capture: USDC and USDT both hold
  short-term Treasuries and repo as primary reserves. At current interest
  rates, that's material yield. Ask what the actual yield on reserves is
  relative to reported earnings — the issuer captures all of it while
  holders get $1.00 flat. That asymmetry is the business model. Ask whether
  they expect competitive pressure to share yield with holders (as GENIUS
  Act provisions around yield-bearing stablecoins are interpreted), and
  what that does to margins.
- The attestation vs. audit gap: monthly attestations from accounting firms
  verify that reserves existed at a point in time. They don't verify internal
  controls, counterparty quality within the reserve, or whether the same
  reserves are pledged elsewhere. Ask what a full audit would look like for
  their specific reserve structure — and why they haven't done one.
- Banking relationship fragility: the USDC depeg to $0.87 during the SVB
  collapse (March 2023) was caused by Circle having $3.3B in uninsured
  deposits at SVB. Ask what their banking relationships look like today —
  specifically, which banks hold their cash portion and whether those
  deposits exceed FDIC insurance limits.
- The GENIUS Act's preemption implications: the Act establishes federal
  standards but also lets state-chartered issuers continue under state
  oversight. Ask whether their competitive moat depends on federal
  preemption narrowing the field of compliant issuers — and whether they
  lobbied for or against the state-charter carve-out.
- The offshore / onshore split for Tether specifically: USDT dominates
  in emerging markets and offshore trading. Ask what percentage of USDT
  redemptions come from the 48 hours vs. standard 30-day window — the
  redemption mechanics reveal where the liquidity actually is.
- For Circle specifically: the USDC / Coinbase revenue share is disclosed
  in Circle's S-1 (from their SPAC attempt). Ask what the effective
  distribution cost per USDC in circulation is, and whether the model
  holds if Coinbase reduces its distribution commitment.

**Textbook chapters to load first:**
- Ch 9 (Stablecoins/RWAs) — all of it: fiat-backed mechanics, reserve
  attestation vs. audit, USDC SVB depeg mechanism, GENIUS Act provisions,
  MiCA framework, use cases. This is their chapter — know it cold.
- Ch 6 (Market Structure) — stablecoins as trading pairs, T+0 settlement
  on-chain vs. T+1 in TradFi, how stablecoin dominance affects exchange
  revenue.
- Ch 5 (Custody) — how reserve assets are held, HSM and cold storage
  relevance for stablecoin issuer risk management.

**Counternarrative flags to check:**
- Attestation ≠ audit: point-in-time snapshot, no internal controls
  verification, no counterparty quality check within reserve.
- "Fully backed" framing: ask about reserve composition in detail —
  cash, repo, T-bills, and whether any portion is in money market funds
  that themselves hold Treasuries via repo.
- FDIC insurance: stablecoin reserve cash deposits at banks are not
  individually insured beyond standard FDIC limits. SVB proved this matters.
- GENIUS Act "first federal framework" — accurate, but ask what specific
  provisions they found most and least favorable to their business.

**Q3 (technical depth) template:**
> "Walk me through what your reserve composition looks like today —
> specifically the cash portion, which banks hold it, whether any of those
> deposits exceed FDIC limits, and what changed in that structure after
> the SVB event."

**Q4 (contested territory) template:**
> "Your monthly attestations verify reserves existed at a point in time.
> They don't verify internal controls or whether those same assets are
> pledged elsewhere. What would a full audit of your reserve structure
> actually require — and what's the reason you haven't published one?"

**Q5 (adversarial) template:**
> "GENIUS Act provisions are being interpreted as potentially requiring
> stablecoin issuers to offer yield to holders at some threshold of
> scale. If yield-sharing becomes mandatory, what happens to your
> margin structure — and is your current reserve strategy optimized
> for that world or against it?"

---

## Archetype 16 — The DAT Executive
*e.g., Michael Saylor (Strategy), Jeff Park (Bitwise), Saul van Staveren
(Hyperion DeFi / HYPE treasury company), BitMine, SharpLink Gaming*

**What they are:** Executives who have made the decision to accumulate a
crypto asset as the primary corporate treasury strategy — either Bitcoin
(the Strategy playbook) or altcoin variants that layer in staking and DeFi
yield (the second-wave DATs for ETH, SOL, HYPE). This archetype is distinct
from the Bitcoin Native/OG (Archetype 9) because the interesting questions
are not about Bitcoin's monetary properties — they're about corporate finance
structure, capital markets mechanics, and the specific risks of being a
publicly traded company whose primary asset is a volatile token.

**What they've been asked to death:**
- "Why Bitcoin / ETH / SOL as a treasury asset?"
- "What's your price target?"
- "Are you worried about the price going down?"
- "How does this compare to MicroStrategy's approach?"

**Where the interesting questions live:**
- The capital formation mechanics: Strategy raises money through convertible
  bonds (near-zero coupon because the embedded conversion option has value
  due to MSTR volatility) and at-the-money equity offerings. Ask what the
  actual financing cost is on an annualized basis, and at what BTC price
  level the cost of capital inverts — i.e., where it becomes more expensive
  to raise than the expected asset return.
- The premium/NAV relationship: Strategy's stock has historically traded at
  a significant premium to its BTC NAV. That premium is what makes the
  convertible arbitrage work. Ask what their current premium is, what
  drives it, and what happens to the capital formation model if the premium
  compresses to 1x or below. This is the mechanism most interviewers never
  ask about.
- For altcoin DATs specifically: ETH and SOL DATs enhance returns through
  staking and DeFi strategies. Ask what their validator infrastructure looks
  like, what the custody arrangement is for staked assets, and what smart
  contract risk they're underwriting to access DeFi yield. These risks don't
  exist in a Bitcoin-only structure.
- The HYPE DAT structure specifically: Hyperion and similar HYPE treasury
  companies are exploring HIP-3 deployment as a yield strategy — staking
  HYPE to deploy HIP-3 markets. Ask what their legal analysis is of whether
  operating a HIP-3 market as a public company creates regulated exchange
  or broker-dealer obligations.
- The dilution question: at-the-market equity offerings and convertible notes
  are dilutive to existing shareholders. Ask how they think about the
  dilution cost vs. the BTC/token accumulation benefit — specifically, what
  BTC/token price appreciation rate is required to make the financing
  accretive on a per-share basis.
- Regulatory and accounting treatment: FASB now requires mark-to-market
  accounting for crypto holdings (ASC 350, effective for fiscal years
  beginning after December 15, 2024). Ask how that accounting change affects
  their earnings volatility and what it means for their equity story with
  institutional investors who care about GAAP earnings.

**Textbook chapters to load first:**
- Ch 6 (Market Structure) — convertible note arbitrage mechanics, basis
  trade, corporate treasury adoption section, DAT trend. The capital
  markets structure around these companies is a market structure story.
- Ch 1 (Bitcoin) — for Strategy guests: security budget, halving, UTXO
  model. Don't let monetary theory dominate; redirect to capital structure.
- Ch 10 (Hyperliquid) — for HYPE DAT guests: HIP-3 mechanics, staking,
  HLP vault risk.

**Counternarrative flags to check:**
- "No liquidation risk" framing: technically accurate (no margin call on
  convertibles) but refinancing risk and dilution pressure are real
  alternative failure modes. Ask about the debt maturity schedule.
- "Infinite demand" for the convertible notes: demand exists because of
  MSTR volatility. If vol compresses, the conversion option loses value
  and demand for low-coupon notes dries up. Ask about their vol assumptions.
- FASB mark-to-market: many DAT executives haven't fully internalized that
  their earnings will now swing dramatically with token prices. Ask how
  they're communicating that to the street.

**Q3 (technical depth) template:**
> "Strategy's convertible note demand comes from hedge funds running
> the convertible arb — they buy the note for the conversion option and
> short the stock to hedge equity risk. What's your model for what happens
> to that demand if MSTR realized volatility compresses toward Bitcoin's
> own vol? And what does that do to your cost of capital?"

**Q4 (contested territory) template:**
> "FASB's new crypto accounting rules require mark-to-market on your
> holdings. Your GAAP earnings are now going to move with [BTC/ETH/SOL]
> price every quarter. How are institutional investors you've spoken to
> actually reacting to that earnings volatility — and is there a price
> level where it becomes a material governance problem?"

**Q5 (adversarial) template:**
> "Walk me through the specific sequence where this structure breaks.
> Not a crash scenario — the slow version: premium compresses to NAV,
> convertible demand softens as vol drops, the ATM shelf gets expensive.
> At what premium-to-NAV level do you stop raising capital, and what's
> the plan after that?"

---

## Archetype 17 — The Stablecoin Project
*e.g., Rune Christensen (Sky / formerly MakerDAO), Guy Young (Ethena),
Sam Kazemian (Frax), Nick van Eck (Agora AUSD)*

**What they are:** Founders building novel stablecoin mechanisms — whether
crypto-backed (Sky/USDS), delta-neutral synthetic (Ethena/USDe), fractional-
algorithmic (Frax), or RWA-backed (Agora). They are building the most
financially complex products in DeFi and they're also building the ones
with the most catastrophic failure modes. UST/LUNA is the permanent scar
on this category — every stablecoin founder has a practiced answer for
why they're different. The interview lives in whether that answer is
actually mechanistic or just reputational distance.

**What they've been asked to death:**
- "How is your stablecoin different from UST?"
- "What's your collateralization ratio?"
- "Is your stablecoin decentralized?"
- "What happens if there's a bank run?"

These questions get answered in terms of design features, not failure paths.

**Where the interesting questions live:**
- The specific failure scenario they've modeled: don't ask "what happens
  in a crisis" — ask "walk me through the exact sequence of events that
  would cause your peg to break, and at what collateral ratio does the
  system become insolvent." The specific scenario is always more revealing
  than the general framework.
- For Ethena specifically: delta-neutral yield depends on positive funding
  rates. In bear markets, funding goes negative and the yield disappears —
  or inverts. Ask what the reserve fund size is relative to the total USDe
  supply, what the maximum sustained negative funding rate the reserve can
  absorb is, and what the user experience looks like as the reserve depletes.
  The OES (Off-Exchange Settlement) provider risk (Copper, Ceffu, Fireblocks)
  is the other axis — ask what happens to minting/redemption if one OES
  provider has an operational incident.
- For Sky/MakerDAO: the transition from DAI to USDS, the Sky Savings Rate
  as a demand lever, and the increasing allocation to RWAs (Treasuries) as
  collateral means the protocol is now partially dependent on traditional
  finance counterparties. Ask what percentage of USDS supply is backed by
  RWAs vs. crypto collateral, and what the protocol's exposure is to a
  US Treasury market disruption.
- The peg mechanism under stress: the LitePSM (for Sky) and the reserve
  fund (for Ethena) are described as peg defense mechanisms. Ask what the
  maximum stress they've been tested under in production is — not in
  simulation, in live market conditions.
- Protocol revenue vs. emissions: many stablecoin protocols use token
  incentives to bootstrap adoption. Ask for the split between real protocol
  revenue (interest income, swap fees) and emission-funded growth. That
  ratio is the solvency indicator no one asks about directly.

**Textbook chapters to load first:**
- Ch 9 (Stablecoins/RWAs) — all of it: all three stablecoin types,
  overcollateralization ratio, liquidation ratio, peg mechanism, depeg
  history, GENIUS Act, MiCA. This is the primary chapter.
- Ch 7 (DeFi) — Ethena delta-neutral mechanics, Sky decentralized central
  bank model, Pendle and yield tokenization as adjacent instruments,
  real yield vs. emissions distinction.
- Ch 6 (Market Structure) — funding rate dynamics for Ethena; perp market
  mechanics are the yield source and primary risk for delta-neutral stables.

**Counternarrative flags to check:**
- "Overcollateralized therefore safe" framing: the ratio matters, but so
  does the correlation of collateral to the peg — DAI backed by ETH
  during an ETH crash is more dangerous than the ratio suggests.
- Ethena funding rate risk: the yield is not guaranteed and goes negative
  in bear markets. Ask for the current reserve ratio explicitly.
- "Decentralized" stablecoin claims: Sky/MakerDAO has a Foundation and
  a core team with significant influence. Ask about the last governance
  decision that went against the core team's recommendation.
- UST comparison deflection: most founders respond to UST comparisons by
  listing structural differences. Ask instead: what's the specific
  mechanism that prevents a self-reinforcing redemption spiral in their
  system, and what's the maximum redemption velocity the system can handle
  before that mechanism fails?

**Q3 (technical depth) template:**
> "Walk me through the specific failure path for your peg — not the
> general framework, the exact sequence. At what collateral ratio does
> the system become technically insolvent, what triggers that level,
> and what's the on-chain mechanism that prevents the redemption spiral
> from accelerating past the point of recovery?"

**Q4 (contested territory) template:**
> "[For Ethena] Your reserve fund is sized against a sustained negative
> funding scenario. What's the maximum annualized negative funding rate
> the reserve can absorb before USDe holders see losses, and what was
> the actual reserve utilization rate during the worst funding period
> you've seen in production?"

**Q5 (adversarial) template:**
> "What's the version of this that ends badly — not an attack, not a
> black swan, just the slow deterioration path where the mechanism
> works as designed but the outcome is still a depeg? Every stablecoin
> has one. What's yours?"

---

## Archetype 18 — The Risk Manager
*e.g., Tarun Chitra (Gauntlet), Max Einhorn (Chaos Labs), risk curators
at Morpho (RE7 Labs, Steakhouse, MEV Capital), Nansen risk team,
Block Analitica*

**What they are:** Quantitative risk analysts and firms who either advise
protocol DAOs on parameter settings (Gauntlet advising Aave, Chaos Labs
advising multiple protocols) or directly manage vault strategies as risk
curators (Morpho, Euler). They are the least-interviewed archetype relative
to their influence — they set the collateral ratios, liquidation thresholds,
and supply caps that determine whether a lending protocol is solvent under
stress. They have the most data-grounded views in DeFi and the least
incentive to oversell.

**What they've been asked to death:**
- "How do you think about DeFi risk?"
- "What's the biggest risk in DeFi right now?"
- "How does risk management in DeFi differ from TradFi?"

**Where the interesting questions live:**
- The parameter update process in practice: risk firms advise DAOs, but
  DAOs vote on whether to implement the recommendations. Ask for a specific
  case where they recommended a parameter change, the DAO delayed or
  rejected it, and whether a bad outcome followed. The gap between
  recommendation and implementation is where DeFi risk actually lives.
- The oracle concentration problem: nearly every major DeFi protocol
  uses Chainlink for price feeds, with Pyth as a secondary. Ask what
  the systemic risk is if Chainlink has a price feed failure during a
  high-volatility event — specifically, which protocols would face
  cascading liquidations, and what the aggregate bad debt estimate is.
- Correlation risk in collateral: lending protocols accept multiple
  assets as collateral. In a market crash, most assets are correlated.
  Ask how they model correlation risk when setting supply caps and
  collateral ratios — specifically, whether their stress tests assume
  50% correlated drawdown or worse.
- The Morpho risk curator model vs. the Aave governance model: on Aave,
  risk firms advise and governance executes. On Morpho, risk curators
  own the vault strategy directly. Ask which model they think produces
  better risk-adjusted outcomes — and what the principal-agent problem
  looks like in each.
- MEV and liquidation quality: liquidations in DeFi are executed by bots
  competing for the liquidation bonus. In fast markets, if no liquidator
  bots execute fast enough, the protocol accrues bad debt. Ask what the
  worst liquidation quality event they've observed in production was —
  specifically, which protocol, what the bad debt was, and whether the
  parameter assumptions were wrong ex-ante or just hit an out-of-sample
  tail event.

**Textbook chapters to load first:**
- Ch 7 (DeFi) — lending protocol mechanics, overcollateralization ratios,
  liquidation ratio, flash loans, oracle design, TWAP vs. spot price feeds,
  risk curator model on Morpho. This is primary.
- Ch 8 (MEV) — liquidation bots as a specific MEV category, the searcher
  ecosystem, how liquidation quality depends on MEV infrastructure.
- Ch 9 (Stablecoins/RWAs) — stablecoin depeg events create cascading
  liquidations in lending protocols. The USDC SVB depeg and its effect
  on Aave and Compound is the canonical case study.

**Counternarrative flags to check:**
- "Battle-tested" protocol language: ask what the worst stress event was
  in production and whether the parameters held. "Battle-tested" often
  means the last crash didn't break it — not that the next one won't.
- TVL as a health signal: high TVL in a lending protocol with aggressive
  parameters can indicate excess risk, not safety. Ask what their maximum
  acceptable bad debt ratio is.
- Governance lag as a hidden risk: parameter recommendations often take
  weeks to reach governance votes. Ask whether they have emergency
  multisig authority to change critical parameters without a full vote
  and what the threshold to use it is.

**Q3 (technical depth) template:**
> "When you're setting supply caps for a new collateral asset, what
> correlation assumption are you using against the rest of the collateral
> portfolio in a 50% drawdown scenario — and has the actual realized
> correlation during past stress events matched your ex-ante model?"

**Q4 (contested territory) template:**
> "The gap between your parameter recommendation and a governance vote
> passing can be two to four weeks. Walk me through a specific case
> where that lag was consequential — and whether protocols should have
> emergency multisig authority to change parameters without a vote."

**Q5 (adversarial) template:**
> "Which currently live DeFi protocol has the parameter setting you're
> most worried about — not a hypothetical, an actual live configuration
> where you think the combination of collateral quality, oracle design,
> and liquidation bonus creates a plausible path to material bad debt
> in the next market stress event?"

---

## Archetype 19 — The Crypto x AI Developer
*e.g., Shaw Walters (ElizaOS / ai16z), Basem Wael (Virtuals Protocol),
Jesse Pollak on Coinbase AgentKit / x402, Bittensor core team,
Giza / ARMA, Almanak*

**What they are:** Builders at the intersection of AI agent infrastructure
and on-chain execution. Two distinct sub-types:

**Framework builders** (ElizaOS, Virtuals G.A.M.E., ARC, Solana Agent Kit)
— building the runtime and plugin layer that lets AI agents interact with
blockchains. Their questions are about agent architecture, key management,
and what "autonomous" actually means when an agent has a wallet.

**Agentic finance builders** (Coinbase AgentKit / Agentic Wallets, Giza /
ARMA, Almanak) — building the transactional layer: wallets that agents can
hold, spend caps and session controls, MPC custody for agent keys, and
the x402 payment protocol for machine-to-machine stablecoin flows.

This space moves extremely fast. ElizaOS peaked in GitHub activity in
December 2024 then declined significantly. Virtuals surged after integrating
Coinbase's x402 standard. The second wave (Wayfinder, HeyAnon, AgentKit)
shifted from communicative agents toward automated DeFi execution. By
early 2026, Coinbase had launched Agentic Wallets with session spending
caps, TEE security, and gasless Base transactions — framing it as
"give any agent a wallet." The key live questions are about custody,
liability, and what happens when an agent makes a bad trade.

**What they've been asked to death:**
- "What can AI agents do on-chain?"
- "Is this the killer app for crypto?"
- "How does your agent decide what to do?"
- "What's the token for?"

**Where the interesting questions live:**
- The key management problem is unresolved: if an AI agent holds a private
  key, either a human controls that key (in which case it's not autonomous)
  or the key is controlled by the model's runtime (in which case it's
  vulnerable to prompt injection, model hijacking, and infrastructure
  failure). Ask how they've actually solved key custody — MPC, TEE, or
  something else — and what the failure mode is if the AI model underlying
  the agent is updated or replaced.
- The liability question when agents transact: if an AI agent makes a
  trade that loses money, routes through a sanctioned address, or
  triggers a regulatory obligation, who is liable? The agent has no
  legal personhood. Ask what their legal analysis of that question is —
  specifically, whether they've obtained any legal opinion on whether
  their agent's transactions create MSB (Money Services Business)
  obligations for the operator.
- Prompt injection as the primary attack vector: an on-chain AI agent
  that reads public data (mempool, social media, price feeds) can be
  manipulated by adversarially crafted on-chain data. If a searcher
  puts a message in an on-chain transaction that the agent reads and
  acts on, that's an attack. Ask if they've seen this in production
  and how the architecture defends against it.
- The spending cap / session control design: Coinbase Agentic Wallets
  have session caps and transaction size limits. Ask who sets those
  caps, whether they're enforced at the smart contract level or just
  policy, and what happens if the agent's LLM reasons its way around
  the spending limit by chaining smaller transactions.
- Token vs. product: most AI agent projects have a token. Ask what the
  token actually does mechanically — is it required for agent operation,
  does it gate access to the framework, or is it purely speculative?
  The distinction between "the token is the product" and "the product
  has a token" is the most important question in this space.
- The ElizaOS GitHub decline: the framework saw massive developer interest
  peak in December 2024 and then drop significantly. Ask what drove that
  decline — were developers building things that didn't work, or did the
  framework evolve in a direction the community didn't follow?

**Textbook chapters to load first:**
- Ch 8 (MEV) — prompt injection as a MEV-adjacent attack vector. Agents
  that read on-chain data are vulnerable to adversarially crafted messages.
  The searcher/builder ecosystem is the threat model.
- Ch 5 (Custody) — MPC, TSS, TEE for agent key management. The custody
  question is the most important unsolved problem in this archetype.
- Ch 12 (Governance & Token Economics) — agent tokens and what they
  actually entitle holders to. Most don't pass the "what does this token
  do?" test.
- Ch 7 (DeFi) — if agents are executing DeFi strategies autonomously,
  understanding AMM mechanics, lending protocols, and flash loan risk
  is table stakes for asking good questions.

**Counternarrative flags to check:**
- "Autonomous" agent claims: ask specifically who controls the private
  key and under what conditions a human can intervene. Full autonomy
  and human override are in tension.
- Token value claims: ask what the token is technically required for
  in the protocol stack. If it's not required for operation, it's not
  utility — it's speculation.
- AI agent "managed funds" narratives: the ai16z DAO's AI fund manager
  ("AI Marc") had limited transparency. Ask what the actual realized
  returns were and whether the AI was making decisions or executing
  pre-approved strategies.
- Framework GitHub activity as adoption proxy: GitHub stars peaked and
  declined for both ElizaOS and ARC. Ask what the actual production
  deployment count is — wallets with agent keys, not repos forked.

**Q3 (technical depth) template:**
> "Your agent holds a private key and reads on-chain data to decide
> what to execute. Walk me through your defense against prompt injection
> — specifically, what prevents an adversary from embedding a message
> in an on-chain transaction that your agent reads and interprets as
> an instruction to transfer funds?"

**Q4 (contested territory) template:**
> "When your agent executes a transaction that loses money or routes
> through a flagged address, who bears the legal liability — the user
> who deployed the agent, the framework operator, or nobody? Have you
> gotten a legal opinion on whether operating an autonomous spending
> agent creates MSB obligations for you or your users?"

**Q5 (adversarial) template:**
> "ElizaOS saw a significant drop in GitHub activity after its December
> 2024 peak. Virtuals and ARC had similar patterns. What's the honest
> explanation for why developer momentum in this space hasn't compounded —
> is this a tooling problem, a use-case problem, or is the current
> architecture fundamentally not suited for the applications people are
> trying to build?"

---

## Cross-Archetype Rules (Apply to All Guests)

**The transcript pre-read protocol:**
If prior interviews exist, read them before writing any questions.
Flag all rehearsed answers in the brief. Do not re-ask them.
The prior-interview analysis belongs in a **"What He's Already Said"**
section at the top of the brief, before the questions.

**The non-leading question discipline:**
Every question goes through `context/question-craft.md` before inclusion.
The test: can this question be answered with a yes, a no, or a polished
prepared talking point? If yes, rewrite it.

**The counternarrative integration rule:**
At least one of the five questions must come directly from
`context/counternarrative-flags.md` for the guest's domain. The goal is
to put a technically accurate challenge on the table, not a gotcha.

**The content seeds rule:**
Every brief ends with Content Seeds (see output template in
`workflows/guest-diligence.md`). The seeds are not optional — they are
how the brief connects to the content calendar in `workflows/content-plan.md`.
