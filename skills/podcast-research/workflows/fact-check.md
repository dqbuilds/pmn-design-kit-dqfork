# Workflow — Fact-Check Talking Points

Use this workflow when the user provides specific claims to verify before
recording. Accuracy over comprehensiveness — a short, correct answer is
better than a long uncertain one.

---

## Step-by-Step Protocol

For each claim, execute all steps in order before moving to the next claim.

### Step 1 — Restate the Claim
Write the claim back in your own words. This forces disambiguation and catches
vague language before you search for the wrong thing.

### Step 2 — Classify the Claim Type
Identify what kind of claim it is. This determines the search strategy.

| Type | Description | Strategy |
|---|---|---|
| **Factual event** | Something happened at a specific time | Find original source reporting the event |
| **Statistic** | A number or metric | Find the data source behind the number |
| **Superlative** | "First ever," "largest," "record" | Requires explicit verification — do not accept without primary source |
| **Mechanical** | How a protocol or system works | Check textbook (tier2-primary.md) before searching news |
| **Opinion/forecast** | What someone believes will happen | Label as such — do not verify as fact |
| **Attribution** | Someone said or did something | Find primary source (transcript, filing, announcement) |

### Step 3 — Identify the Correct Source Tier
Before searching, decide which tier should hold the answer:
- Mechanical claims → Tier 2 textbook first
- Regulatory events → Tier 2 gov source first
- Protocol/on-chain events → Tier 2 data platforms + Tier 1 news
- Market structure claims → Tier 2 data platforms (Artemis, Token Terminal)
- Investigative/fund flow claims → Tier 2 Arkham + Tier 1 Protos/The Block

### Step 4 — Search and Verify
- Search with a specific 3–6 word query
- Find at least one Tier 1 or Tier 2 source that directly supports the claim
- For statistics: trace the number back to its original data source
- For superlatives: actively search for counterexamples before confirming
- For mechanical claims: cross-check against textbook for plausibility

### Step 5 — Contradiction Check
Before finalizing, ask:
- Does this contradict on-chain data? (If news says X is up but DefiLlama says TVL is down, flag it)
- Does this contradict how the mechanism is supposed to work? (Check textbook)
- Is there a credible counter-narrative? (Check counternarrative-flags.md)

### Step 6 — Label and Deliver

Use exactly these labels:
- ✅ **Verified** — confirmed by Tier 1 or Tier 2 source, no material caveats
- ⚠️ **Partially Verified** — directionally correct but missing context, wrong in detail, or only confirmed by Tier 3
- ❌ **Unverified** — could not find supporting source in Tier 1–3
- 🔄 **Contested** — credible competing narratives exist from Tier 1–2 sources

Add a **confidence note** after every label:
- `[High]` — confirmed in 2+ independent Tier 1/2 sources
- `[Medium]` — confirmed in 1 Tier 1/2 source or corroborated via Tier 3
- `[Low]` — single source, paywalled, or relies on secondary reporting

---

## Output Format

For each claim:

```
### Claim [N]: [Restated claim in your own words]

**Label:** ✅ Verified [High] / ⚠️ Partially Verified [Medium] / etc.

**What's actually true:**
1–3 sentences. Precise. No hedging unless there is genuine uncertainty.

**Sources:**
- [Outlet/Platform] — [URL] — [Date] — Tier [1/2/3]

**What to be careful about on air:**
Any phrasing or framing the host should avoid. Flag missing context that
could make a technically true statement misleading.

**Suggested phrasing:**
One punchy, accurate sentence the host can say directly.
```

---

## Hard Rules for Specific Claim Types

**"First ever" claims**
Never confirm without finding: (a) a Tier 1/2 source explicitly using that
language AND (b) actively searching for prior examples. The crypto space
has a well-documented pattern of overclaiming novelty.

**Statistics cited without a source**
Always find the original data source. If a Tier 1 article says "DeFi TVL
hit $140B," the citation should be DefiLlama, not the article.

**"Institutional" framing**
Distinguish between: an institution buying a token, an institution deploying
infrastructure, an institution filing regulatory paperwork, and an institution
making a press announcement. These are materially different levels of commitment.

**Protocol mechanics claims**
If a claim describes how a protocol works (e.g., "Uniswap v3 uses concentrated
liquidity to..."), verify against protocol documentation or the textbook — not
just news coverage, which frequently oversimplifies.

**Price or market predictions**
Label immediately as opinion/forecast. Do not verify as fact regardless of who
said it.
