# Glossary — Canonical Definitions for On-Air Use

Use these definitions when explaining terms on air. They are technically
accurate and written at a level that works for crypto-native and crossover
audiences. Do not use definitions that contradict these without flagging it.

Organized by chapter to mirror the Cermak textbook structure.
Source: *How Crypto Actually Works* — Cermak, Igamberdiev, Pavlov (Wintermute)
https://github.com/lawmaster10/howcryptoworksbook

---

## Ch01 — Bitcoin

**Bitcoin (BTC)** — A peer-to-peer electronic cash system launched January 3,
2009 by Satoshi Nakamoto. Monetary policy is transparent, mathematically
enforced, and capped at 21 million coins — the only asset in the world with
a provably limited supply that anyone can independently verify.

**UTXO (Unspent Transaction Output)** — Bitcoin's accounting model. Rather than
tracking account balances, Bitcoin tracks individual coin "chunks" that haven't
been spent yet. Each UTXO has a value and a locking script defining who can
spend it. Distinct from Ethereum's account-balance model.

**Proof of Work (PoW)** — Bitcoin's consensus mechanism. Miners compete to
solve a cryptographic puzzle (SHA-256 hashing) requiring massive computation
to produce but trivial for anyone to verify. The winner earns the right to
add the next block and claim the block reward.

**Hash function / SHA-256** — A one-way mathematical function converting any
input into a fixed-length output. Tiny input changes produce completely
different outputs. Miners must find an input producing an output below the
difficulty target — the computational work required to do this secures the
network.

**Hash rate** — Total computational power directed at Bitcoin mining, measured
in exahashes per second (EH/s). Proxy for network security: higher hash rate
= more costly to attack.

**Difficulty adjustment** — Bitcoin recalibrates the mining puzzle difficulty
every 2,016 blocks (~2 weeks) to keep block times at ~10 minutes regardless
of hash rate on the network.

**Halving** — Every 210,000 blocks (~4 years), the Bitcoin block reward is
cut in half. Reduces new supply issuance. Embedded in protocol code. The
halving reduces miner revenue from issuance — it does not directly create
demand.

**Mempool** — The waiting room for unconfirmed transactions. Miners select
transactions from the mempool, typically prioritizing highest fee rates
(sats/vbyte). During congestion, low-fee transactions can wait hours or days.

**Nakamoto Consensus** — Bitcoin's longest-chain rule, more accurately
described as the chain with the most cumulative proof-of-work. Nodes always
follow the chain requiring the most computational effort to produce.

**Chain reorganization (reorg)** — When a node switches from one valid chain
to a longer one, reorganizing recent blocks. One-block reorgs occur naturally;
three or more are rare. Each confirmation exponentially reduces reorg risk.
This is why merchants wait for multiple confirmations on large payments.

**SegWit (Segregated Witness)** — A 2017 Bitcoin upgrade that moved signature
data out of the transaction body, fixing transaction malleability and
increasing effective block capacity. All modern Bitcoin transactions use SegWit.

**Taproot** — A 2021 Bitcoin upgrade introducing Schnorr signatures and MAST
(Merkelized Abstract Syntax Trees). Enables more complex scripts to look like
simple single-signature transactions. The technical foundation for Ordinals
and Bitcoin-native applications.

**Lightning Network** — A Layer 2 payment channel network on Bitcoin. Two
parties lock Bitcoin in a multisig channel and transact instantly off-chain,
only settling to the base layer when the channel closes. Enables micropayments
without base-layer fees.

**Ordinals** — A numbering system assigning unique serial numbers to individual
satoshis based on the order they were mined. Inscriptions — arbitrary data
attached to a specific sat — function as Bitcoin-native NFTs, with media
embedded directly in witness data rather than stored off-chain.

**BRC-20** — An experimental token standard on Bitcoin using Ordinal
inscriptions with JSON data to deploy, mint, and transfer fungible tokens.
Unlike Ethereum tokens, validity depends on indexers agreeing on interpretation
of the JSON messages — there is no smart contract enforcing the rules.

**Inscriptions** — Arbitrary data (text, images, code) embedded directly into
Bitcoin's transaction witness data using the Ordinals protocol. Media lives
on-chain, making Bitcoin inscriptions more durable than most Ethereum NFTs
that reference off-chain storage.

---

## Ch02 — Ethereum

**Ethereum** — A programmable blockchain that introduced smart contracts:
self-executing code running deterministically across all nodes. The foundation
for DeFi, NFTs, stablecoins, and most crypto applications.

**EVM (Ethereum Virtual Machine)** — The computation engine executing smart
contract code. Every Ethereum node runs the same EVM, producing identical
outputs from identical inputs. This determinism is what makes trustless
execution possible.

**Smart contract** — Code deployed on a blockchain that executes automatically
when predefined conditions are met, without a trusted intermediary. Once
deployed, the code is immutable and runs exactly as written.

**EIP (Ethereum Improvement Proposal)** — The process by which changes to
Ethereum are proposed, discussed, and implemented. EIP-1559 changed the fee
mechanism; EIP-4844 introduced blobs for rollup data.

**Proof of Stake (PoS)** — Ethereum's consensus mechanism since The Merge
(September 2022). Validators lock 32 ETH as stake and are selected to propose
and attest to blocks. Misbehavior results in slashing. Energy use dropped
~99.95% vs Proof of Work.

**Slashing** — The penalty applied to Ethereum validators who provably
misbehave — primarily double-signing or equivocating. A portion of staked
ETH is destroyed and the validator is ejected from the validator set.

**The Merge** — Ethereum's September 2022 transition from Proof of Work to
Proof of Stake. The execution layer merged with the Beacon Chain (consensus
layer). Issuance dropped ~90%.

**EIP-1559** — The 2021 upgrade changing Ethereum's fee mechanism. Each block
has a base fee that is burned (destroyed), making ETH deflationary when
network demand is high. Users add a priority tip to accelerate inclusion.

**Blobs / EIP-4844** — Introduced in the Dencun upgrade (March 2024). A new
transaction type allowing rollups to post large data payloads to Ethereum at
much lower cost than calldata. The technical foundation for Ethereum scaling
through rollups. Blobs are pruned after ~18 days.

**Rollup** — A Layer 2 scaling solution that executes transactions off-chain,
batches them, and posts compressed data and a proof back to Ethereum. Inherits
Ethereum's security. The primary Ethereum scaling strategy.

**Optimistic rollup** — A rollup assuming all transactions are valid by default
with a challenge window (typically 7 days) for fraud proofs. (e.g., Arbitrum,
Optimism, Base)

**ZK rollup (zero-knowledge rollup)** — A rollup generating a cryptographic
proof (ZK-SNARK or ZK-STARK) that mathematically verifies batch validity.
Faster finality than optimistic rollups but more compute-intensive.
(e.g., zkSync, Starknet, Polygon zkEVM)

**Restaking** — Allowing already-staked ETH to also secure additional
protocols, extending Ethereum's cryptoeconomic security to new systems.
EigenLayer pioneered this. Validators opt-in to additional slashing conditions
in exchange for additional yield — and additional risk.

**Liquid Staking Token (LST)** — A tokenized receipt for staked ETH that can
be used in DeFi while the underlying ETH continues earning staking rewards.
stETH (Lido) is the largest. Represents a claim on staked ETH plus accumulated
rewards.

**Withdrawal credential** — The Ethereum address designated to receive staking
rewards and principal when a validator exits. Misconfigured withdrawal
credentials have caused custody errors for institutional stakers.

---

## Ch03 — Solana

**Solana** — A high-throughput Layer 1 blockchain designed for fast, cheap
transactions. Achieves ~50,000+ TPS through Proof of History, parallel
transaction processing (Sealevel), and a specialized networking stack.

**Proof of History (PoH)** — Solana's time-stamping mechanism. A continuous
verifiable delay function (VDF) creating a historical record of time passage
before and between events. Allows validators to agree on transaction ordering
without constant communication, dramatically reducing coordination overhead.

**Sealevel** — Solana's parallel transaction processing engine. Because
transactions declare upfront which accounts they'll read and write, Solana
can execute non-conflicting transactions simultaneously across multiple CPU
cores — unlike Ethereum's sequential execution.

**Turbine** — Solana's block propagation protocol. Breaks blocks into small
packets distributed across validators in a tree-like structure, minimizing
bandwidth requirements for any single node.

**Gulf Stream** — Solana's mempool-less transaction forwarding protocol.
Transactions are forwarded directly to the expected next leader before the
current block is finished, reducing confirmation times and memory pressure.

**Firedancer** — A second Solana validator client built by Jump Crypto.
Critical for client diversity — Solana currently has one dominant client
(Agave). A single-client bug caused the 2022 network outage. Firedancer
targets order-of-magnitude performance improvements.

**Jito** — A Solana MEV infrastructure provider. Jito-Solana is a validator
client fork enabling a private mempool and MEV-boost-style block building
on Solana, routing tip revenue from searchers to validators.

**Vote transactions** — A significant share of Solana's transaction volume
consists of validator vote transactions required for consensus. These are not
user transactions. They inflate raw TPS figures and should be excluded when
measuring actual user activity.

---

## Ch04 — L1 Blockchains

**Layer 1 (L1)** — A base blockchain handling its own consensus and security
(e.g., Bitcoin, Ethereum, Solana, Avalanche, Sui). All other networks
ultimately settle to or derive security from an L1.

**Layer 2 (L2)** — A network built on an L1 that inherits its security but
processes transactions more cheaply and quickly. Validity or fraud proofs
ensure the L1 can detect invalid L2 state transitions.
(e.g., Arbitrum, Base, Optimism on Ethereum)

**Avalanche** — A Layer 1 using a novel consensus mechanism (Avalanche
consensus) based on repeated random sampling. Achieves sub-2-second finality.
Composed of three chains: X-Chain (assets), C-Chain (EVM-compatible smart
contracts), P-Chain (validator coordination and subnet management).

**Subnet (Avalanche)** — An application-specific blockchain within the
Avalanche ecosystem. Each subnet has its own validator set, execution
environment, and token economics. Comparable to an app-chain.

**BFT (Byzantine Fault Tolerant) consensus** — A consensus class that reaches
agreement even when some nodes behave maliciously. Typically offers faster
finality than Nakamoto consensus but requires known validator sets, creating
different trust assumptions.

**Move (programming language)** — A smart contract language originally
developed for Meta's Diem, now used by Sui and Aptos. Treats assets as
"resources" that can't be copied or accidentally destroyed — a safer model
than Solidity's less restrictive approach.

**Finality** — When a transaction becomes irreversible. Probabilistic finality
(Bitcoin): reversal becomes exponentially unlikely with each block.
Economic finality (Ethereum PoS): reversal would require destroying massive
amounts of staked ETH. Instant finality (Avalanche, BFT): blocks cannot be
rolled back once confirmed.

**TPS (Transactions per second)** — A theoretical maximum that rarely reflects
real load. More meaningful: TPS under real load, cost per transaction, time
to finality, daily active addresses (Artemis is the authoritative source).
A chain with 50,000 theoretical TPS and few users is not outperforming a
chain with 3,000 TPS and real activity.

---

## Ch05 — Custody

**Self-custody** — Holding crypto in a wallet where you control the private
keys. "Not your keys, not your coins." Lost keys are permanently unrecoverable.

**MPC (Multi-Party Computation)** — A cryptographic technique splitting private
key signing authority across multiple parties so no single party ever holds
or sees the complete key. The dominant institutional custody architecture.
Eliminates single points of failure without requiring physical key distribution.

**Multisig** — A wallet requiring M-of-N key signatures to authorize a
transaction (e.g., 3 of 5 signers must approve). Implemented at the protocol
level rather than cryptographically like MPC. Common in DAO treasuries
and institutional setups.

**HSM (Hardware Security Module)** — A dedicated physical device that
generates, stores, and uses cryptographic keys without exposing key material
to software. The key is physically locked in the chip. Used in bank-grade
and institutional custody.

**Threshold Signature Scheme (TSS)** — A form of MPC where parties collectively
sign a transaction producing a single, standard-looking signature without any
party knowing the full key. More private than multisig — the threshold
structure is not visible on-chain.

**Cold storage** — Private keys stored completely offline, disconnected from
the internet. Reduces remote attack surface dramatically. Large custodians
typically keep 90%+ of assets in cold storage.

**Warm wallet** — An intermediate tier between hot (internet-connected) and
cold (fully offline). Often hardware wallets or air-gapped machines requiring
physical access to sign but not fully offline.

**Hot wallet** — An internet-connected wallet for active trading or frequent
transactions. Higher compromise risk — should hold only minimum operational
balance.

**Key ceremony** — The process by which cryptographic keys are generated,
split, and distributed so no single party learns the full key. Critical
security event in institutional custody setup. Typically involves independent
parties in separate locations.

---

## Ch06 — Market Structure

**CEX (Centralized Exchange)** — An exchange operated by a company maintaining
custody of user funds and operating a central limit order book matching engine.
The company is counterparty to all trades. (e.g., Coinbase, Binance, Kraken)

**Order book (CLOB)** — A real-time list of buy and sell orders at each price
level. A matching engine pairs buyers and sellers when prices agree. The
dominant structure in traditional finance and on centralized crypto exchanges.

**Market maker** — A participant continuously quoting both buy and sell prices,
earning the bid-ask spread. Provides liquidity. On CEXes, designated market
makers often have fee rebates and API access privileges.

**Maker / Taker** — A "maker" adds liquidity by placing a resting limit order;
a "taker" removes liquidity by filling an existing order. Makers typically pay
lower fees or receive rebates; takers pay higher fees.

**Perp (Perpetual futures)** — A futures contract with no expiration date.
The dominant crypto trading instrument. Settled in cash, not the underlying
asset. The perp price is anchored to spot through the funding rate mechanism.

**Funding rate** — A periodic payment between long and short holders of
perpetual contracts keeping the perp price anchored to spot. Positive rate:
longs pay shorts (market leans bullish). Negative: shorts pay longs. A direct
signal of market sentiment and leverage positioning.

**Open interest (OI)** — Total open (unsettled) futures or perp contracts.
Rising OI + rising price: new money entering, trend potentially sustainable.
Rising OI + falling price: shorts adding, potential squeeze setup. Falling OI:
positions closing, leverage flushing.

**Basis trade** — A strategy exploiting the price difference between spot and
futures. Buy spot BTC, short BTC futures, earn the premium. Risk: the basis
can narrow or invert.

**Liquidation** — When a leveraged position's margin falls below the maintenance
threshold, the exchange forcibly closes it. Cascading liquidations — where
one liquidation moves price enough to trigger more — can cause rapid violent
price moves.

**RFQ (Request for Quote)** — A trading mechanism where a trader asks
counterparties for a price quote on a specific trade rather than broadcasting
publicly. Used in institutional OTC and some DEXes (UniswapX). Prevents
front-running by keeping trade intent private until execution.

**OTC (Over the Counter)** — Trading directly between parties outside a public
exchange. Institutional-size trades often done OTC to avoid moving the market.
Prices negotiated, not discovered through an order book.

**Dark pool** — A private venue for large block trades where orders are not
visible until after execution. Used by institutions to minimize market impact.

---

## Ch07 — DeFi

**DeFi (Decentralized Finance)** — Financial applications built on public
blockchains using smart contracts. No custodians, no KYC, no intermediaries.
TVL, revenue, and users are all verifiable on-chain.

**TVL (Total Value Locked)** — Total dollar value deposited into a DeFi
protocol. Useful proxy but not perfect — inflates with token price appreciation
and mercenary incentive capital. Methodology varies by platform. Token Terminal
revenue and Artemis DAUs are more useful fundamentals.

**AMM (Automated Market Maker)** — A DEX mechanism using a mathematical
formula (e.g., x*y=k) to price assets and enable trades without an order book.
Anyone can provide liquidity; prices adjust automatically as trades occur.

**Concentrated liquidity (CLMM)** — Introduced by Uniswap v3. LPs allocate
capital within a specific price range rather than across the entire curve.
Capital efficiency increases dramatically but LPs must actively manage ranges
or risk being entirely out-of-range during price moves.

**Hooks (Uniswap v4)** — Smart contract plugins attaching to liquidity pools
and executing custom logic at defined points in the swap lifecycle. Enables
building limit orders, TWAMM, dynamic fees, and custom AMM behaviors on
top of Uniswap infrastructure.

**Liquidity pool** — A smart contract holding two or more assets that an AMM
uses to facilitate trades. LPs deposit assets and earn fees proportional to
their pool share.

**Impermanent loss (IL)** — The opportunity cost an LP faces when the price
ratio of pooled assets changes relative to simply holding them. If the ratio
returns to entry levels, IL disappears. Only realized if you withdraw when
prices have diverged. Not an accounting loss unless you exit.

**DEX (Decentralized Exchange)** — A protocol enabling peer-to-peer trading
directly from wallets. Settlement is on-chain and atomic.

**Lending protocol** — A DeFi application allowing users to supply assets to
earn interest or borrow against collateral. Over-collateralization is required
because there's no credit score or legal recourse. (e.g., Aave, Compound,
Morpho)

**Overcollateralization** — Borrowers must deposit more value than they borrow.
A 75% LTV ratio requires $133 of collateral for every $100 borrowed. Prevents
insolvency when collateral prices drop.

**Flash loan** — An uncollateralized DeFi loan that must be borrowed and
repaid within the same transaction. If repayment doesn't happen atomically,
the entire transaction reverts. Used for arbitrage, liquidations, and exploits.

**Oracle** — A mechanism bringing off-chain data (e.g., price feeds) on-chain.
Critical infrastructure — if an oracle is manipulated, everything depending
on it is at risk. Chainlink is the dominant provider; Pyth focuses on
low-latency data.

**TWAP (Time-Weighted Average Price)** — An on-chain price calculated from
the average over a time window, resistant to single-block manipulation.
Uniswap v3 provides TWAP oracles as a primitive.

**Yield aggregator / Vault** — A DeFi protocol automatically moving capital
between lending protocols, liquidity pools, or yield strategies to maximize
returns. Yearn Finance pioneered the model.

**Real yield** — Protocol revenue paid to token holders in established assets
(ETH, USDC, BTC) rather than newly minted tokens. Contrast with inflationary
"yield" that is simply dilution of existing holders.

**Fee switch** — The DAO mechanism to activate directing a portion of protocol
fees to token holders or treasury rather than entirely to LPs. UNI's fee
switch activation in late 2025 was the first time UNI token holders received
direct economic benefit from the protocol.

---

## Ch08 — MEV

**MEV (Maximal Extractable Value)** — Value that block producers can extract
by reordering, inserting, or censoring transactions within a block. Includes
arbitrage, sandwich attacks, liquidations, and JIT liquidity. Originally
called "Miner Extractable Value" under PoW.

**Searcher** — A MEV bot operator scanning the mempool for profitable
opportunities and submitting high-priority transactions with tips. Searchers
identify MEV; block builders order transactions to maximize total value.

**Frontrunning** — Inserting a transaction ahead of a known pending transaction
to profit from its price impact. A searcher sees a large buy in the mempool,
buys first, lets the original trade push price up, then sells.

**Backrunning** — Placing a transaction immediately after another to capture
the arbitrage or price correction it creates. Less harmful than frontrunning —
often restores prices across pools after large trades.

**Sandwich attack** — A two-transaction attack where a searcher places a buy
before a large trade and a sell after it, profiting from price impact at
the victim's expense. The victim receives worse execution; the searcher earns
the spread.

**Block builder** — In the PBS model, the entity constructing the block body
by selecting and ordering transactions to maximize total value. Builders
compete by offering the highest bid to validators/proposers.

**PBS (Proposer-Builder Separation)** — An architectural design separating
the role of selecting the winning block (proposer/validator) from constructing
block contents (builder). Prevents validators from needing MEV software while
allowing competitive builders to specialize. Currently implemented via MEV-Boost
off-protocol on Ethereum.

**MEV-Boost** — Flashbots' open-source middleware connecting Ethereum validators
to a marketplace of block builders. Validators receive pre-built blocks and
choose the most profitable. ~90% of Ethereum blocks currently use MEV-Boost.

**Flashbots** — The R&D organization that built MEV-Boost and dominant block
building infrastructure for Ethereum. Created to reduce MEV harm by routing it
through transparent channels rather than chaotic mempool competition.

**Private mempool / Private orderflow** — Transactions submitted directly to
block builders (bypassing the public mempool) to avoid being sandwiched.
Private orderflow is the primary competitive moat for large builders —
empirically, ~12% of transactions but >54% of block rewards.

**JIT (Just-In-Time) liquidity** — A MEV strategy where a bot adds liquidity
to a Uniswap position within the same block as a large trade (capturing fees),
then removes it immediately after. Earns fees without long-term IL risk. Harms
passive LPs by diluting their fee share.

**Atomic arbitrage** — An arbitrage executed within a single transaction
exploiting price differences across DEXes. If the arbitrage can't be completed
profitably, the entire transaction reverts. Zero risk of partial execution.

---

## Ch09 — Stablecoins & RWAs

**Stablecoin** — A crypto asset maintaining stable value, typically pegged
to USD. Three types: fiat-backed (USDC, USDT — reserves held by issuer),
crypto-backed (DAI — overcollateralized on-chain), algorithmic (UST —
failed catastrophically in 2022 and no longer the reference model).

**USDC** — Circle's USD-backed stablecoin. Each USDC redeemable 1:1 for USD,
backed by cash and short-term US Treasuries. Monthly attestations from major
accounting firms. Subject to US regulations and has demonstrated on-chain
freeze capability.

**USDT (Tether)** — The largest stablecoin by market cap. Issued by Tether Ltd.
Historically controversial due to reserve transparency. Now publishes quarterly
attestations. Dominant in offshore and emerging market trading.

**Overcollateralization ratio** — For crypto-backed stablecoins, the ratio of
collateral value to outstanding supply. A 150% ratio means $1.50 of collateral
backs every $1.00 of stablecoin. The buffer absorbs price drops before the
peg is threatened.

**Liquidation ratio** — In a crypto-backed stablecoin system, the collateral
ratio below which a position is liquidated to keep the system solvent.

**Peg mechanism** — The design maintaining a stablecoin's price at its target.
Fiat-backed: direct redemption keeps price at $1. Crypto-backed: arbitrage
incentives. Algorithmic: mint/burn mechanics tied to a governance token —
the model that failed with UST.

**Depeg** — A stablecoin trading materially off its intended peg. USDC briefly
depegged to $0.87 during the SVB collapse (March 2023). Sustained depegs signal
structural problems. UST's collapse from $1 to near-zero was catastrophic.

**Reserve attestation** — Third-party verification that a stablecoin issuer
holds assets they claim as backing. Monthly attestations are standard for
compliant issuers. An attestation is a point-in-time snapshot — not the same
as a full internal controls audit.

**RWA (Real-World Asset)** — A traditional financial asset (Treasury bond,
private credit, real estate, invoice) tokenized and represented on a blockchain.
Allows on-chain access to yield from off-chain instruments.

**Tokenized Treasury** — A blockchain representation of short-term US
government debt. BlackRock's BUIDL is the largest. Provides stablecoin-like
stability with yield. Used as DeFi collateral and DAO cash management.

**BUIDL (BlackRock USD Institutional Digital Liquidity Fund)** — BlackRock's
tokenized money market fund on Ethereum, primarily holding US Treasuries and
repo. The largest tokenized Treasury fund by AUM. Note: deployed on UniswapX
using an RFQ model with whitelisted institutional investors — not open
permissionless DeFi.

**GENIUS Act** — Signed into law 2025. First comprehensive federal framework
governing stablecoin issuance in the US. Requires reserve backing, redemption
procedures, and audited reserve reporting.

---

## Ch10 — Hyperliquid

**Hyperliquid** — A decentralized perpetuals exchange built as an
application-specific L1 blockchain. Operates a fully on-chain central limit
order book (CLOB) with sub-second finality. As of late 2024, the largest
perp DEX by volume.

**HLP (Hyperliquidity Provider)** — Hyperliquid's protocol-owned market-making
vault. Community members deposit assets to provide liquidity, earning a share
of trading fees and market-making profits (and absorbing losses). Acts as
counterparty of last resort.

**CLOB (Central Limit Order Book)** — An on-chain order book matching buy and
sell orders by price-time priority, identical in structure to a traditional
exchange. Hyperliquid runs this fully on-chain unlike most DEXes which use AMMs.

**HYPE token** — Hyperliquid's native governance and utility token. Notable
for its airdrop structure — distributed entirely to community users based on
trading activity with no VC allocation. Became the reference point for
"fair launch" token distribution debates.

**Points airdrop** — A distribution mechanism where protocol users accumulate
points based on activity (trading volume, deposits, referrals) later converted
to tokens. Common technique for bootstrapping liquidity and attributing tokens
to actual users rather than speculators.

---

## Ch11 — NFTs

**NFT (Non-Fungible Token)** — A blockchain token representing ownership of
a unique item. Unlike fungible tokens where each unit is identical, each NFT
has distinct properties. Can represent art, collectibles, game items, domain
names, or real-world assets.

**ERC-721** — The Ethereum token standard for non-fungible tokens. Each token
ID is unique with a single owner. The foundation of the NFT ecosystem. Media
is typically stored off-chain (IPFS or Arweave); the token holds a pointer.

**ERC-1155** — A multi-token standard supporting both fungible and non-fungible
tokens within a single contract. More gas-efficient for gaming and batch
transfers. A single contract can manage entire collections with varying
fungibility.

**IPFS (InterPlanetary File System)** — A distributed file storage protocol
commonly used to store NFT media. Files addressed by content hash rather than
server location. More durable than centralized hosting but requires nodes to
actively pin content to prevent loss.

**Floor price** — The lowest listed price for any NFT in a collection. Proxy
for collection value but easily manipulated by thin liquidity. Large deviations
between floor and average sale price often signal strategic manipulation.

**Mint** — Creating a new NFT by calling a smart contract's mint function and
paying the gas fee. "Free mint" means no purchase price (only gas); Dutch
auction mints start high and drop until sold out.

**Royalties** — A percentage of secondary sales paid to the original creator,
enforced by the smart contract. Enforcement became contentious in 2023 when
some marketplaces made royalties optional. On-chain vs. marketplace-level
enforcement remains unresolved.

---

## Ch12 — Governance & Token Economics

**DAO (Decentralized Autonomous Organization)** — An organization governed by
smart contracts and token holder votes rather than traditional legal structure.
Treasury management, protocol parameters, and upgrades are determined by
on-chain or off-chain governance.

**On-chain governance** — Voting executed directly through smart contracts.
Passed proposals automatically trigger parameter changes or treasury actions.
Provides transparency and automation but risks low participation and plutocracy.

**Off-chain governance** — Voting on platforms like Snapshot (gas-free, wallet-
signed but not executed on-chain). Results enacted by a multisig or trusted
executor. More accessible but requires trust in implementation.

**Quorum** — The minimum participation threshold required for a governance vote
to be valid. Prevents small groups from passing proposals during low-activity
periods. Typically set as a percentage of circulating supply.

**veTokens (Vote Escrow)** — A governance model (pioneered by Curve) where
token holders lock tokens to receive voting power and yield. Longer lock =
more power (veCRV). Aligns governance power with long-term commitment but
concentrates power among well-capitalized players.

**Gauge voting** — In Curve and similar protocols, veToken holders vote on
which liquidity pools receive token emissions. This created the "Curve Wars"
— protocols competed for veCRV to direct emissions to their pools.

**Token unlock / Vesting** — Locked tokens distributed to team, investors,
or advisors per a schedule. Unlocks are cited as bearish catalysts but actual
price impact depends on sell propensity, size relative to daily volume, and
sentiment. Check Tokenomist for actual schedules.

**Emissions** — New tokens created and distributed (typically to LPs or
stakers) as protocol incentives. High emissions dilute existing holders and
are only sustainable if the protocol generates matching real value.
Distinguish "yield from emissions" vs "yield from real protocol revenue."

**Protocol-owned liquidity (POL)** — When a protocol owns liquidity in its
own pools rather than renting it from mercenary LPs. Olympus DAO pioneered
the concept. More stable than incentivized liquidity but requires significant
capital commitment.

**Governance token** — A token granting voting rights over protocol parameters
and treasury. Economic value depends entirely on whether the protocol generates
cash flows and routes them to token holders. Many governance tokens are
structurally closer to coupons than equity — always ask: what does this token
actually entitle you to?

---

## Ch13 — DePIN

**DePIN (Decentralized Physical Infrastructure Network)** — A model where
blockchain token incentives coordinate deployment of real-world physical
infrastructure — wireless networks, storage, compute, mapping, energy.
Token rewards attract hardware operators; usage creates token demand.

**Proof of Coverage** — A mechanism verifying that a DePIN node is actually
providing coverage in a physical location. Helium uses radio frequency
challenges between hotspots to verify location and uptime. Harder to fake
than purely software attestations.

**Proof of Location** — On-chain verification that a hardware node is operating
from a specific geographic location. Critical for DePIN networks where
geographic distribution is the core value proposition.

**Helium** — The largest DePIN network by hardware deployment. Operates
decentralized LoRaWAN (IoT) and 5G wireless networks. Token incentives reward
hotspot operators for providing coverage. Migrated from its own L1 to Solana
in 2023.

**Hivemapper** — A DePIN network for decentralized mapping. Contributors
install dashcams and earn HONEY tokens for footage that builds the map database.

---

## Ch14 — Quantum Resistance

**Quantum computer** — A computer using quantum mechanical phenomena
(superposition, entanglement) to perform certain computations exponentially
faster than classical computers. Relevant to crypto because sufficiently
powerful quantum computers could break elliptic curve cryptography (ECDSA)
used by Bitcoin and Ethereum.

**Post-quantum cryptography (PQC)** — Cryptographic algorithms believed to
be resistant to quantum attacks. NIST finalized first PQC standards in 2024.
Based on problems quantum computers can't efficiently solve (lattice problems,
hash-based signatures).

**Harvest now, decrypt later** — A threat model where adversaries collect
public keys today and decrypt them once quantum computers are powerful enough.
Relevant for long-lived Bitcoin UTXOs with exposed public keys, particularly
pre-SegWit P2PK addresses.

**ECDSA (Elliptic Curve Digital Signature Algorithm)** — The signature scheme
used by Bitcoin and Ethereum to prove ownership of funds. Vulnerable to a
sufficiently powerful quantum computer running Shor's algorithm. Migration to
quantum-resistant signatures requires a hard fork of both networks.

**Cryptographic agility** — The ability of a system to swap out cryptographic
primitives without redesigning the entire protocol. Networks lacking this will
face harder migrations when quantum resistance becomes necessary.

---

## Ch15 — Prediction Markets

**Prediction market** — A financial market where participants trade contracts
based on future event outcomes. Prices reflect the probability the market
assigns to each outcome. Polymarket is the dominant crypto-native platform.

**Binary market** — A prediction market with exactly two outcomes (yes/no).
The price of a "yes" share trades between $0 and $1 and directly represents
the market's probability estimate.

**Scalar market** — A prediction market where outcomes are along a continuous
range. Payout is proportional to where the actual result falls within the range.

**LMSR (Logarithmic Market Scoring Rule)** — An AMM mechanism designed for
prediction markets. A market maker provides initial liquidity in exchange for
information value. Prices always sum to 1 across all outcomes.

**Resolution oracle** — The mechanism determining the official outcome of a
prediction market and triggering payouts. Can be decentralized (UMA's
optimistic oracle, Polymarket's UMA integration) or centralized. Oracle
manipulation is the primary attack surface.

**Conditional market** — A prediction market on an outcome contingent on
another event occurring. (e.g., "If X wins, what will Y do?") Useful for
nuanced probability distributions but harder to resolve cleanly.

**Polymarket** — The dominant crypto-native prediction market, built on
Polygon. Gained mainstream attention during the 2024 US election with hundreds
of millions in open interest. Uses USDC for settlement.

---

## General (Cross-Chapter)

**Gas** — The fee paid to process a transaction on a blockchain. Paid in the
network's native token (ETH on Ethereum, SOL on Solana, AVAX on Avalanche).
Gas price is set by demand for block space.

**Slippage** — The difference between the expected price of a trade and actual
execution price. Higher for large trades relative to pool depth. Setting a
slippage tolerance in a DEX determines the worst price you'll accept.

**ABS (Asset-Backed Security)** — A financial instrument backed by a pool of
loans or assets. Ledn's Bitcoin ABS (2025) was backed by Bitcoin-collateralized
loans and received a BBB- S&P rating. Hit structural stress when BTC dropped 27%,
demonstrating both the progress and limits of BTC as structured finance
collateral.

**Spot ETF** — An ETF holding the actual underlying asset (e.g., actual Bitcoin).
Bitcoin spot ETFs were approved in the US in January 2024; Ethereum spot ETFs
followed. Custodied primarily by Coinbase (~70% of BTC ETF AUM).

**National Trust Bank Charter** — A federal banking license issued by the OCC
authorizing fiduciary activities: custody, stablecoin issuance, reserve
management, and settlement. Does NOT authorize FDIC-insured deposit-taking or
lending. Not the same as a full banking license.

**Wallet** — Software or hardware storing private keys and interfacing with
blockchains to sign transactions. The wallet doesn't store crypto; the
blockchain does. The wallet stores the credentials to prove ownership.

**Private key** — A secret number proving ownership of a crypto address and
authorizing transactions. Anyone with your private key controls your funds.
Loss is permanent and unrecoverable.

**Seed phrase (mnemonic)** — A human-readable backup of a private key,
typically 12 or 24 words. Derives all keys for a wallet. Whoever has your
seed phrase has your funds — store offline, never digitally.

**Consensus mechanism** — The rules by which a blockchain's nodes agree on
which transactions are valid. Proof of Work uses computation; Proof of Stake
uses locked capital; BFT uses known validator sets with direct communication.

**Validator** — A node participating in a Proof of Stake network by locking
capital (staking) to vote on the validity of transactions and propose new blocks.

---

## Ch01 — Bitcoin (Extended Terms)

**BIP (Bitcoin Improvement Proposal)** — The formal process for proposing
changes to Bitcoin. Policy BIPs (e.g., mempool relay rules) ship in Bitcoin
Core releases and need no coordination. Consensus BIPs modify fundamental
validity rules and require near-universal adoption. SegWit and Taproot both
went through this process.

**Security budget** — Total miner revenue (block subsidy + transaction fees)
that determines the cost of a 51% attack. As halvings reduce the subsidy,
fee revenue must grow to maintain security. In 2024 the subsidy was ~94% of
miner revenue. This long-run dynamic is Bitcoin's most contested design
question.

**Hard fork** — A protocol change that relaxes or expands consensus rules,
making previously invalid blocks/transactions valid. Non-upgraded nodes reject
the new chain — a permanent split unless one side has overwhelming adoption.
Bitcoin Cash (2017) is the canonical hard fork example.

**Soft fork** — A protocol change that tightens consensus rules. Upgraded
nodes reject things old nodes would accept. Old nodes still follow the longest
chain and remain in consensus as long as the majority of hash power enforces
the new rules. All of Bitcoin's major upgrades (SegWit, Taproot) have been
soft forks.

**MASF (Miner Activated Soft Fork)** — Hash power signals readiness via
version bits in block headers. BIP9 required ~95% of blocks over a 2,016-block
window. Used historically for most Bitcoin upgrades until miners stalled SegWit.

**UASF (User Activated Soft Fork)** — Economic nodes (exchanges, businesses,
wallets) coordinate a \"flag day\" to enforce new rules regardless of miner
signaling. If major economic actors enforce the rules, miners face the choice:
follow or mine a chain the market ignores. Resolved the SegWit standoff in 2017.

**Speedy Trial** — A miner signaling mechanism with a lower threshold (90%)
and short window. If miners don't signal within the window, no activation
occurs and other mechanisms can be tried. Used to activate Taproot in 2021.

**Satoshi** — The smallest unit of Bitcoin: 0.00000001 BTC (one hundred-millionth
of a BTC). Fees are quoted in satoshis per virtual byte (sats/vB). Named after
Satoshi Nakamoto.

**CoinJoin** — A privacy technique combining inputs from multiple users into
a single transaction with many equal-value outputs, breaking the on-chain
assumption that all inputs belong to one owner. Implementations add Tor routing,
output blinding, and multi-round mixing to improve the anonymity set.

**Pseudonymous** — Bitcoin's privacy model. Addresses aren't inherently linked
to real-world identity, but transaction graph analysis can cluster addresses and
trace flows. KYC at exchanges and companies like Chainalysis routinely de-anonymize
on-chain activity. Bitcoin is not anonymous — it is traceable by default.

**Stale block (orphan)** — A valid block that was mined simultaneously with
another block but lost the chain race. Its transactions return to the mempool.
Natural one-block reorgs occur occasionally; two-block reorgs are rare absent
an attack.

---

## Ch02 — Ethereum (Extended Terms)

**EOA (Externally Owned Account)** — A standard Ethereum account controlled
by a private key. Can initiate transactions but has no code. Contrast with
smart contract accounts, which execute code on call. EIP-7702 (Pectra) allows
EOAs to temporarily delegate to smart contract logic, enabling batch transactions
and sponsored gas.

**Account abstraction** — Removing the hard distinction between EOAs and smart
contracts so any account can define custom validation logic. Enables sponsored
transactions (someone else pays your gas), batch operations, social recovery,
and passkey authentication without migrating to a new address. EIP-7702 in
Pectra is Ethereum's first major step.

**Slot / Epoch** — Ethereum's time units post-Merge. A slot = 12 seconds;
one validator proposes a block per slot. An epoch = 32 slots (~6.4 minutes).
Finality checkpoints occur at epoch boundaries when a supermajority attests
to justify and finalize blocks.

**Attestation** — A cryptographic vote from a validator confirming that a
proposed block follows the rules. Hundreds of validators attest per slot; a
block is justified when 2/3 of validators attest to it, and finalized in the
following epoch when another supermajority confirms the justification.

**BLS signatures** — Boneh–Lynn–Shacham signatures used by Ethereum validators.
Can be aggregated: thousands of individual validator signatures compress into
a single compact proof, dramatically reducing verification overhead.

**Inactivity leak** — If the chain fails to finalize for >4 epochs (due to
>1/3 of validators being offline), offline validators' balances slowly drain.
This allows the remaining active validators to regain supermajority and resume
finality. A mechanism ensuring liveness even during large partitions.

**Validium** — A rollup variant that posts state commitments to Ethereum but
keeps transaction data off-chain (under control of a committee or operator).
Cheaper than a true rollup but weaker security guarantees — if data becomes
unavailable, users can't prove ownership or challenge invalid state.

**Data Availability Sampling (DAS)** — A technique allowing resource-constrained
nodes to verify that full block data was published by checking only small,
random samples rather than downloading everything. Celestia's core innovation;
enables Ethereum's long-term Danksharding roadmap.

**Celestia** — A specialized modular blockchain providing only consensus and
data availability, not execution. Uses DAS so even light clients can verify
full data availability. The most prominent alternative data availability layer
for rollups that don't want to pay Ethereum's DA costs.

**AVS (Actively Validated Service)** — An external protocol that opts into
EigenLayer's restaking system to borrow Ethereum's economic security. AVSs
cover data availability (EigenDA), oracle networks, bridges, rollup sequencers,
and keeper networks. Each defines its own slashing conditions.

**EigenDA** — EigenLayer's data availability AVS. Operators who restake on
EigenLayer attest to data availability for rollups using EigenDA. Provides
high throughput at lower cost than posting to Ethereum L1 directly.

**Intersubjective slashing** — EigenLayer's mechanism for handling violations
that can't be proven purely on-chain (e.g., an oracle reporting a clearly
wrong price). Resolution relies on token holder / committee social consensus
rather than automated proof verification. Introduces governance risk but
handles real-world scenarios pure algorithms can't.

---

## Ch03 — Solana (Extended Terms)

**SVM (Solana Virtual Machine)** — Solana's complete execution environment:
the register-based VM, loaders, syscalls, the account model, and the Sealevel
parallel scheduler. Register-based (unlike Ethereum's stack-based EVM) for
faster parallel execution. Programs must declare upfront which accounts they'll
read/write, enabling Sealevel to run non-overlapping transactions simultaneously.

**Lamport** — Solana's smallest unit of account: 0.000000001 SOL (10⁻⁹).
Analogous to satoshis for Bitcoin. Accounts must maintain a minimum lamport
balance to remain rent-exempt (preventing state bloat).

**Program Derived Address (PDA)** — A Solana address with no private key,
generated mathematically from program inputs. Only the owning program can
authorize transactions from it. Solves the custodial problem: escrow contracts
hold funds directly with no human private key that could be stolen.

**Cross-Program Invocation (CPI)** — One Solana program calling another,
passing accounts as inputs. Enables composability: DeFi protocols can interact
atomically without deploying new code. The runtime verifies all necessary
accounts are present before execution.

**Local fee markets** — Solana prices congestion at the account level rather
than network-wide. Heavily congested accounts pay more without degrading
performance for the rest of the network. In practice, during extreme 2024-2025
spam events, congested traffic still elevated global dropped-transaction rates.

**Atomic composability** — The ability to execute multiple protocol interactions
within a single transaction that either fully succeeds or fully fails. No partial
executions, no stuck funds. A key Solana UX advantage over fragmented multi-chain
ecosystems where users must navigate bridges and separate state.

**Tower BFT** — Solana's current consensus mechanism, layered on top of Proof
of History timestamps. Validators cast stake-weighted votes on blocks; PoH
timestamps prevent equivocation (voting for conflicting blocks). Produces
guaranteed finality at ~12.8 seconds. Being replaced by Alpenglow.

**QUIC** — The modern internet protocol Solana uses for transaction transport.
Handles multiple data streams over one connection, recovers from packet loss
faster than TCP, and allows stake-weighted Quality of Service: validators with
more stake get priority bandwidth, making the network more resistant to spam.

**Gulf Stream** — Solana's transaction forwarding protocol. Rather than
broadcasting to a public mempool, transactions are sent directly to the current
and upcoming scheduled leaders. Reduces latency by eliminating the public
broadcast phase; transactions can be forwarded to future leaders before their
slot begins.

**Turbine** — Solana's block propagation protocol. Breaks blocks into small
chunks called shreds and distributes them via a tree structure — each validator
receives shreds and forwards to a small subset of peers. Redundant encoding
means the full block can be reconstructed even if some shreds are lost.

**DoubleZero** — A private network overlay connecting Solana validators through
dedicated fiber optic links (the same infrastructure as Nasdaq/CME). Eliminates
the variable latency of the public internet, enabling the tight timing windows
Alpenglow's fast finality requires.

**Alpenglow** — Solana's planned consensus upgrade (targeting mainnet early-mid
2026, timeline uncertain). Replaces Tower BFT with Votor (new voting method)
and Rotor (block dissemination), targeting ~100-150ms median finality (vs
current 12.8s). Deprecates Proof of History entirely — the largest protocol
change in Solana's history.

**Votor** — Alpenglow's new voting mechanism. Validators exchange votes directly
and form certificates proving sufficient stake has agreed. Runs two finalization
paths in parallel: blocks finalizing immediately with 80%+ stake support, and
in two rounds with 60%+ support. No Tower BFT chaining of multiple rounds.

**Rotor** — Alpenglow's planned block dissemination replacement for Turbine.
Routes messages through high-stake validators with reliable bandwidth, using
fewer relay steps. Enables the tight propagation windows fast finality requires.

**BAM (Block Assembly Marketplace)** — Jito's reimagining of Solana's transaction
pipeline. Inserts a marketplace with Trusted Execution Environments (TEEs) so
neither validators nor builders can see raw transaction content before ordering.
Prevents frontrunning — validators order transactions without being able to
front-run them.

**Harmonic** — An open block-builder aggregation layer for Solana. Validators
can accept block proposals from multiple competing builders in real time. BAM
handles transaction ordering within blocks; Harmonic handles which builders
construct the blocks. Together: a more competitive, transparent block-building
ecosystem.

**Raiku** — A scheduling and auction layer adjacent to Solana's validator set
for applications requiring deterministic execution (CLOBs, high-frequency
trading). Provides Ahead-of-Time (AOT) and Just-in-Time (JIT) transaction types
for pre-committed and real-time execution needs. Offers guarantees approaching
centralized systems while retaining on-chain settlement.

**Superminority threshold** — Roughly one-third of total Solana stake — the
amount required to halt consensus. As of January 2026, just 19-22 large validators
control enough stake to reach this threshold. If these operators coordinated,
they could halt block production. A central decentralization concern for Solana.

**SIMD (Solana Improvement Document)** — Solana's equivalent of Ethereum's
EIP. Proposed via GitHub and Discord. Changes require broad validator and
developer buy-in. Core contributors activate approved changes via feature gates
once a supermajority of stake-weighted validators has upgraded.

**Feature gates** — Disabled-by-default protocol changes that upgraded Solana
clients understand but don't enforce. Once a supermajority has upgraded and
there is clear community support, core contributors activate the feature gate
on-chain at a specific slot. Validators that haven't upgraded are then out of
consensus.

**SPL tokens** — Solana's fungible token standard. Unlike Ethereum where each
token is a separate smart contract, all SPL tokens share a single battle-tested
program. Creating a new token means creating a mint account — not deploying
new code. Security improvements to the SPL token program benefit every token
simultaneously.

**Associated Token Accounts (ATAs)** — Solana's system for auto-deriving a
standard token account address for each wallet-token pair. Eliminates the user
error of sending tokens to wrong addresses. If wallet X holds SOL and you send
token Y, the ATA address for Y at wallet X is deterministic and predictable.

**Token-2022** — Solana's extended token standard. Adds programmable features:
transfer hooks (custom logic executing on every transfer, enabling royalties
or compliance checks), confidential transfers (privacy via cryptographic proofs),
transfer fees, and permanent delegates. Backward-compatible with SPL.

**State compression** — A technique storing NFT metadata off-chain while
maintaining a single on-chain concurrent Merkle tree as cryptographic proof of
the entire collection. Ownership proved via a short Merkle proof. Reduces a
1 million NFT collection from ~$250,000 in account rent to under $100.

**Frankendancer** — The transitional Solana validator combining Firedancer's
networking and block production modules with Agave's runtime and consensus.
Went live on a subset of mainnet validators in September 2024. As of early 2026,
full Firedancer (independent of Agave) is still not available for mainnet.

**Anchor** — The de facto standard Solana development framework, analogous to
React in web development. Automates: Interface Definition Language (IDL)
generation for client code, account validation, and standardized patterns for
common operations. Significantly lowers the learning curve and reduces attack
surface from manual account checks.

---

## Ch04 — L1 Blockchains (Extended Terms)

**Modular blockchain** — An architecture separating the four functions of a
blockchain (execution, settlement, consensus, data availability) across
specialized layers rather than handling all four in a monolithic L1. Enables
each layer to optimize independently. Celestia provides data availability; a
rollup handles execution; Ethereum provides settlement.

**Four planes** — The conceptual framework for blockchain architecture:
(1) Execution — where transactions are processed and state changes computed,
(2) Settlement — where finalized state is recorded and disputes resolved,
(3) Consensus — ensuring validators agree on transaction ordering,
(4) Data availability — ensuring transaction data is published and accessible
for verification. Monolithic L1s handle all four; modular systems split them.

**Liveness vs. Safety** — The fundamental tradeoff in distributed systems.
Liveness: the network keeps making progress (producing blocks) even with some
faulty nodes. Safety: the network never finalizes conflicting state. BFT
systems like Ethereum's Casper prioritize safety (halting rather than finalizing
inconsistencies). Bitcoin prioritizes liveness (always extending the longest
chain). You cannot have both under all network conditions (CAP theorem).

**Sharding** — Splitting network state and transaction processing across
multiple parallel shards, each handled by different validator subsets. Ethereum's
original roadmap included execution sharding, but this approach has largely
given way to rollup-centric scaling due to the complexity of cross-shard
communication and security guarantees.

**WASM (WebAssembly)** — A portable binary instruction format increasingly
used as an alternative to the EVM for smart contract execution. Used by
CosmWasm, Polkadot's Substrate, and Near Protocol. Supports multiple programming
languages and has a larger existing developer toolchain than Solidity.

**Monad** — An EVM-compatible L1 pursuing parallel execution of Ethereum
transactions. Decouples transaction execution from consensus and implements
optimistic concurrency control to run non-conflicting transactions simultaneously.
Aims to bring SVM-style parallelization to the EVM ecosystem.

---

## Ch06 — Market Structure (Extended Terms)

**Mark price** — An exchange-calculated estimate of a futures contract's fair
value, blending spot index prices, bid/ask spreads, and basis components.
Used for liquidation triggers and unrealized PnL — not the last traded price.
Prevents liquidations from single large trades or temporary manipulation spikes.

**Auto-deleveraging (ADL)** — When liquidations create losses exceeding the
insurance fund, profitable opposing positions are forcibly reduced to cover the
shortfall. If you hold a winning long during a crash and the exchange can't
cover all the losing shorts, your position may be involuntarily closed. A
tail risk of trading on leveraged venues.

**Authorized Participant (AP)** — In spot ETFs, the institutional entity
(typically a large bank or broker-dealer) that creates or redeems ETF shares
in large blocks (\"creation units\") by delivering or receiving the underlying
asset. The AP mechanism keeps ETF prices aligned with NAV through arbitrage.
After mid-2025 SEC relief, BTC/ETH ETF APs can transact in-kind (crypto
directly) rather than cash, tightening the arbitrage.

**Digital Asset Treasury (DAT)** — A public company that raises capital to
accumulate a crypto asset as its primary balance sheet strategy. Strategy
(MicroStrategy) pioneered this with Bitcoin. A second wave of DATs emerged in
2025 applying the same playbook to ETH and SOL, often layering staking yields
on top of the treasury position.

**Convertible note arbitrage** — The strategy that makes corporate DAT bond
offerings viable. Specialized hedge funds buy convertible bonds at 0% interest
because the embedded conversion option has value (rising stock → profit on
conversion). They hedge the equity exposure by shorting the stock. This demand
from arb funds enables companies like Strategy to issue near-zero-coupon debt
and deploy proceeds into crypto.

---

## Ch07 — DeFi (Extended Terms)

**StableSwap (Curve Finance)** — A hybrid AMM formula blending constant-sum
(near zero slippage near the peg) with constant-product (protective walls far
from peg) behavior, controlled by an amplification factor (A). Designed for
pegged assets (stablecoins, LSTs). Charges 0.01-0.04% fees vs Uniswap's 0.3%.
Curve's 3pool (USDC/USDT/DAI) became foundational stablecoin infrastructure.

**Meta-pool** — A Curve mechanism letting new stablecoins pair directly against
3pool LP tokens, giving them instant liquidity against all three major
stablecoins without fragmenting existing liquidity.

**Bonding curve** — A mathematical function defining token price as a function
of supply. Buying increases price along the curve; selling decreases it.
Pump.fun used this as a pre-AMM launchpad: tokens trade on the bonding curve
until reaching a threshold, then \"graduate\" to a standard AMM pool.

**Pump.fun** — Solana's permissionless bonding-curve token launchpad. Anyone
can create a token with a fixed supply; it trades on the bonding curve until
a target amount of SOL accumulates, then auto-seeds a Raydium/PumpSwap liquidity
pool. Compressed the friction of token creation to near-zero. Became the
defining retail application of the 2024-2025 memecoin cycle.

**Intent-based trading** — Users sign high-level \"intents\" describing desired
outcomes (\"give me at least 1,000 USDC for my 1 ETH within 2 minutes\") rather
than exact swap paths. Off-chain solvers compete to fulfill these intents across
multiple venues. CoW Swap uses batch auctions; UniswapX uses Dutch auctions.

**Coincidence of Wants (CoW)** — When two orders can be settled directly
against each other without AMM liquidity (e.g., user A wants ETH for USDC,
user B wants USDC for ETH). CoW Swap's batch auction engine finds these matches
first, delivering better execution for both parties with zero LP fees.

**Morpho** — A minimal DeFi lending protocol built as a permissionless primitive.
A Morpho Blue market has fixed parameters (one loan asset, one collateral,
LTV, oracle, rate model) set at creation and never changed. Above this,
MetaMorpho vaults let risk curators build yield strategies across multiple markets.

**Risk curator** — An entity (risk firm, DAO, fund) that designs and manages
MetaMorpho vaults on Morpho: choosing which markets to supply, adjusting
allocations, and earning fees for this service. Users opt into a specific
curator's risk decisions rather than relying on a global DAO-set parameter.
Leading curators: Gauntlet, Steakhouse, MEV Capital, RE7 Labs.

**Sky (formerly MakerDAO)** — The decentralized protocol issuing USDS stablecoins
backed by crypto collateral and RWAs, operating like an on-chain central bank.
USDS (replacing DAI) is issued via Vaults. The Sky Savings Rate (SSR) acts as
a demand lever: governance can raise SSR to attract USDS holders and support
the peg. DAI and USDS coexist during the migration.

**Wildcat** — An under-collateralized DeFi lending protocol connecting
institutional borrowers (market makers, hedge funds) with lenders seeking
higher yields than fully-collateralized protocols. Borrowers set rates, lockup
periods, and withdrawal windows. Relies on a reserve buffer rather than full
collateral. First official default occurred mid-2025 when Kinto shut down,
causing a 24% haircut to lenders in that facility with no contagion to other
Wildcat loans.

**Delta-neutral** — A position where gains and losses from price movements
cancel out, leaving exposure to other factors (e.g., yield). Strategy: hold
the underlying asset while simultaneously shorting its futures. Net delta ≈ 0.
Ethena's USDe uses this structure: hold ETH spot, short ETH perps on CEXes.

**Ethena / USDe** — A synthetic dollar protocol generating yield via a
delta-neutral hedge. Users deposit ETH (or LSTs); the protocol shorts equivalent
ETH perp exposure on centralized exchanges. The net position is dollar-stable;
yield comes from perp funding rates (positive in bull markets) and staking yield
on the ETH collateral. Risk: negative funding in bear markets erodes yield.
Custody risk via Off-Exchange Settlement (OES) providers (Copper, Ceffu, Fireblocks).

**Pendle** — A DeFi protocol that tokenizes yield. Any yield-bearing asset can
be split into Principal Tokens (PT, redeemable for the underlying at maturity)
and Yield Tokens (YT, receiving all future yield). Enables fixed-rate lending
(buy PT at a discount), yield speculation (buy YT to bet on yield increasing),
or yield trading without selling the underlying position.

**Points farming** — A pre-token protocol incentive mechanism where users
accumulate off-chain points based on activity (deposits, trading volume,
referrals) that later convert to token allocations at a date determined by
the protocol. Creates speculative demand before launch; rewards actual users
with token airdrops but introduces cliff-risk if conversion terms disappoint.

---

## Ch08 — MEV (Extended Terms)

**Cross-domain MEV** — MEV strategies spanning multiple blockchains
simultaneously — exploiting price differences and timing advantages across
separate chains (e.g., Ethereum mainnet + a rollup, or two different L1s).
Requires specialized infrastructure to monitor and act across domains atomically
or near-atomically.

---

## Ch09 — Stablecoins & RWAs (Extended Terms)

**PYUSD (PayPal USD)** — PayPal's fiat-backed stablecoin, issued by Paxos
on Ethereum and Solana. Backed 1:1 by USD deposits and US Treasuries. Gives
PayPal's 400M+ user base a native crypto payment rail and broadens institutional
stablecoin adoption beyond Circle and Tether.

**MiCA (Markets in Crypto-Assets Regulation)** — The EU's comprehensive
crypto regulatory framework, fully in force from 2024. Governs stablecoin
issuers (requiring reserves, redemption procedures, and registration) and
crypto asset service providers across EU member states. The most comprehensive
jurisdictional framework globally until the US GENIUS Act (2025).

**Tokenized equities** — Blockchain representations of traditional company
shares. Platforms like xStocks bring synthetic representations of public
company stock onto Solana and other chains, enabling 24/7 trading, fractional
ownership, and DeFi composability. Technically off-chain claims on real shares;
counterparty risk on the issuer. A key use case in the RWA category.

---

## Ch10 — Hyperliquid (Extended Terms)

**HyperBFT** — Hyperliquid's custom consensus mechanism, a variant of HotStuff
BFT. Achieves sub-second finality (median ~0.2s) with the validator set
controlled by the Hyperliquid Foundation. Each block contains all order book
state changes. Optimized for financial applications where latency matters more
than permissionless validator entry.

**HyperCore** — Hyperliquid's L1 layer running the native perp and spot CLOB.
Contains the order matching engine, liquidation system, and clearinghouse.
Intentionally minimal: the \"clearing\" layer of the system.

**HyperEVM** — Hyperliquid's EVM-compatible execution layer running on top of
HyperCore. Supports general smart contracts. Uses a dual block architecture:
large EVM blocks (~2s) and small HyperCore blocks (every Tendermint proposal).
This allows Ethereum DeFi composability while keeping the core CLOB's
microsecond order matching unaffected by EVM execution load.

**Asset linking** — The mechanism connecting a HyperCore spot asset to an
ERC-20 on HyperEVM via bridge contracts at special 0x200... addresses. Once
linked, assets flow between Core trading and EVM DeFi without wrapped tokens
or separate bridges. The same USDC or HYPE supply is shared across both layers.

**Hyperps (pre-launch perps)** — Perpetual futures on Hyperliquid for tokens
that haven't launched yet. Allows price discovery and positioning before TGE
(Token Generation Event). Similar to pre-market OTC but fully on-chain. Can
become highly volatile around launch events and listing decisions.

**JELLY manipulation (March 2025)** — An attacker accumulated a large short
position in the illiquid JELLY token across multiple accounts, then pumped the
spot price, causing the HLP vault (the protocol's counterparty of last resort)
to absorb losses as JELLY's price spiked. Exposed the risk of HLP's open
exposure to illiquid tokens. Hyperliquid responded by delisting JELLY and
settling at a price that minimized HLP losses — a validator-controlled
intervention that raised decentralization concerns.

---

## Ch12 — Governance (Extended Terms)

**Quadratic voting** — A governance mechanism where voting power scales with
the square root of tokens committed (1 token = 1 vote, 4 tokens = 2 votes,
9 tokens = 3 votes). Reduces plutocracy by making large holdings progressively
less powerful. Theoretically improves preference aggregation; vulnerable to
Sybil attacks (splitting a large wallet into many small ones).

**Futarchy** — A governance model where token holders vote on values/goals,
but prediction markets determine policy. \"Vote on values; bet on beliefs.\"
Policies are adopted if prediction markets forecast they'll improve the
protocol's target metric. Largely theoretical in crypto governance today but
discussed as an alternative to token-weighted plutocracy.

**Governance attack** — Accumulating enough voting power to pass a malicious
proposal and drain the treasury or alter critical parameters. Historic examples:
Beanstalk (2022, lost $182M via flash-loan governance manipulation), Build
Finance hostile takeover. Flash loan governance attacks are largely mitigated
by time-locked proposals and snapshot-based voting, but remain a theoretical
vector.

**Buyback-and-burn** — A token value accrual mechanism where a protocol uses
revenue to buy its own token on the open market and permanently destroy it,
reducing supply. Analogous to corporate share buybacks. GMX and dYdX have
used variations. Creates token price support but benefits all holders, not
just active governance participants.

**RFC (Request for Comment)** — The first stage of major DeFi governance
proposals: informal community discussion on forums (Commonwealth, Discourse)
before any formal on-chain submission. Tests social consensus before spending
governance capital on a formal vote. Proposals dying at the RFC stage is normal
and healthy.

**Snapshot polling** — Off-chain, gas-free voting using signed wallet messages.
Results not automatically executed — require a trusted multisig or timelocked
executor to implement. Used for temperature checks before costly on-chain votes.
Primary venue: Snapshot.org.

---

## Ch13 — DePIN (Extended Terms)

**Proof of Spacetime** — A verification mechanism for storage networks proving
that a node has continuously stored specified data for a period of time (not
just at a single point). Used by Filecoin's PoRep/PoSt system. Harder to game
than a one-time storage proof.

**Filecoin** — An open, decentralized storage marketplace where clients pay
FIL tokens for providers to store data. Uses Proof of Replication (PoRep) and
Proof of Spacetime (PoSt) to verify storage. Positioned as a permissionless
alternative to cloud storage with cryptographic guarantees of data persistence.

**Arweave** — A permanent, endowment-based storage protocol. Users pay once;
data is stored forever, funded by an endowment that earns interest. Distinct
from IPFS (requires active pinning) and Filecoin (time-limited contracts by
default). Common storage layer for NFT metadata and archival applications.

**Render Network** — A DePIN protocol for GPU compute, specifically rendering.
Idle GPU owners provide rendering power for visual artists and 3D/VR applications,
earning RENDER tokens. Demonstrates DePIN's application to compute resources
beyond storage and wireless.

**Akash** — A decentralized cloud computing marketplace. Tenants bid on compute
resources provided by data center operators, with AKT tokens governing the
network. Provides permissionless access to cloud compute at rates often below
AWS/GCP for workloads that don't require enterprise SLAs.

---

## Ch14 — Quantum Resistance (Extended Terms)

**Shor's algorithm** — A quantum algorithm that can efficiently factor large
integers and compute discrete logarithms. Breaks RSA and elliptic curve
cryptography (ECDSA) — the signature schemes securing Bitcoin, Ethereum,
and most other blockchains. A quantum computer powerful enough to run Shor's
at scale would compromise all exposed public keys.

**Grover's algorithm** — A quantum algorithm that quadratically speeds up
brute-force search. Halves the effective security of hash functions (a 256-bit
hash provides only ~128-bit security against Grover). Manageable: the defense
is longer hashes. Contrast with Shor's, which breaks elliptic curve cryptography
entirely.

**Lattice-based cryptography** — One of the leading post-quantum cryptographic
approaches. Security based on the hardness of lattice problems (believed
quantum-resistant). One of the four NIST-standardized PQC algorithms (CRYSTALS-
Kyber for key encapsulation, CRYSTALS-Dilithium for signatures) use lattice
problems. Both Bitcoin and Ethereum PQC roadmaps include lattice-based
signature schemes.

---

## Ch15 — Prediction Markets (Extended Terms)

**Kalshi** — A CFTC-regulated US prediction market, operating as a licensed
Designated Contract Market. Can offer binary event contracts on political,
economic, and social outcomes legally to US users — unlike Polymarket, which
restricted US participants. Demonstrated that prediction markets can comply
with US financial regulation.

**UMA (Universal Market Access)** — The optimistic oracle protocol powering
Polymarket's dispute resolution. When a market resolves, anyone can propose
an outcome. If no one disputes within the challenge window, it finalizes
automatically. Disputes are adjudicated by UMA token holders as a last resort.

**Optimistic resolution** — A resolution design where outcomes are assumed
correct unless challenged. Reduces costs and speeds up settlement for
uncontested outcomes. Only contested resolutions go through expensive full
arbitration. Used by Polymarket/UMA; the design assumes disputes are rare.

**Augur** — One of the earliest decentralized prediction markets (launched
2018). Failed to gain traction due to poor UX, slow settlement, and the
complexity of its reporting and dispute system. A cautionary case study in
technically correct but user-hostile design.

**Gnosis** — The team that built an early prediction market protocol and
LMSR-based market maker. The team later pivoted to infrastructure (Gnosis Safe
multisig, Gnosis Chain). Their prediction market work became the intellectual
foundation for later protocols.

