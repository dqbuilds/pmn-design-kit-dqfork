# Workflow — Article Writer

Two output modes. Select at the start of every run based on the request:

- **X Article** — 3–5 minute read (~750–1,250 words). No headers. Hook-first. Mobile-optimized.
- **Substack** — 5–10 minute read (~1,250–2,500 words). Light headers allowed. Developed argument. Room for mechanism, data, and counternarrative.

State the mode before writing anything.

---

## Pre-Writing Phase (mandatory — do not skip)

Run all four steps before drafting a single sentence.

### Step 1 — Fact-Check
Load `workflows/fact-check.md`.
Run every claim that will appear in the article through the fact-check protocol.
A claim that cannot be sourced to Tier 1 or Tier 2 either gets cut or gets explicitly caveated.
No unsourced assertions enter the draft.

### Step 2 — Data Pull
Load `workflows/data-pull.md`.
Pull and timestamp every metric that will appear in the article.
Data enters prose only after it has been sourced. Do not write toward data you intend to find later.

### Step 3 — Counternarrative Check
Load `context/counternarrative-flags.md`.
Surface any contested claims, inflated comparisons, or known misconceptions in the topic area before writing.
These either become the article's counternarrative (highest-engagement angle) or get flagged as assumptions to handle carefully.

### Step 4 — Voice Mode Selection
Load `style/voice-analysts.md`.
Select one analyst mode and hold it throughout the article. Do not mix modes.

| Topic type | Mode |
|---|---|
| Market structure / multi-year thesis / narrative that's run ahead of data | Ryan Watkins |
| Protocol valuation / catalyst sequencing / model output | defi_monk |
| Portfolio construction / fund strategy / time horizon arguments | Haseeb or Sean |
| Regime naming / structural critique / principal-agent problems | Sean or Santi |

Also load `style/voice-base.md` and `style/voice-data.md` for all modes.

---

## Chart Suggestion Protocol

Run this after the pre-writing phase and before drafting. Identify every data point or trend in the article that is better understood visually than in prose, then assign a chart placement to each one.

### What qualifies for a chart suggestion

- Any metric that changes over time (TVL growth, collateral share shift, stablecoin market cap)
- Any comparison between two or more things (RWA TVL vs. DeFi TVL; Aave vs. Morpho collateral composition)
- Any data point whose magnitude is hard to appreciate without a reference point (stablecoin settlement volume vs. Visa)
- Any trend that the article's argument depends on (decoupling of DeFi TVL from BTC price)

Do not suggest charts for data that is self-explanatory in a single sentence, or for qualitative claims that have no natural visual form.

### How to place chart suggestions

Insert inline in the article text immediately before the paragraph the chart is meant to support. Use this format:

```
[CHART: [what to show — be specific about axes and timeframe] | Source: [platform name] | Find it: [navigation path, dashboard name, or query description] | Note: [any methodology or freshness caveat]]
```

The chart suggestion is an editorial note — it does not appear in the published article. Strip it before final publication.

### Chart Data Source Reference

Use this as the primary lookup for where to get data for each chart type.

| Chart type | Best source | How to find it |
|---|---|---|
| RWA TVL by category (Treasuries, private credit, etc.) | RWA.xyz | rwa.xyz → top-level dashboard → filter by asset type |
| RWA TVL vs. DeFi TVL comparison | DefiLlama | defillama.com → DeFi → Categories → select RWA; compare against total DeFi TVL chart |
| DeFi TVL over time (all chains) | DefiLlama | defillama.com → DeFi → Overview → export CSV |
| Protocol collateral composition (Aave, Morpho) | Dune Analytics | dune.com → search "Aave collateral composition" or "Morpho collateral breakdown" — prefer dashboards from known researchers or protocol teams |
| Stablecoin market cap and supply over time | DefiLlama | defillama.com → Stablecoins → Chains or Total; also The Block → Data → Stablecoins |
| Stablecoin settlement volume | The Block | theblock.co → Data → Stablecoins → Adjusted On-Chain Volume |
| Protocol revenue and fees | Token Terminal | tokenterminal.com → search protocol name → Revenue or Fees tab |
| BTC/ETH price vs. DeFi TVL correlation | DefiLlama + Glassnode | Layer DeFi TVL (DefiLlama export) against BTC price (Glassnode or CoinMetrics) in a charting tool |
| Tokenized Treasury issuers and market share | RWA.xyz | rwa.xyz → Treasuries → breakdown by issuer (BUIDL, BENJI, USDY, etc.) |
| Cross-chain TVL or revenue comparison | Artemis | artemis.xyz → select chains or protocols → compare revenue or fees |
| Institutional wallet flows | Nansen or Arkham | nansen.ai → Smart Money; arkham.com → entity search |
| On-chain BTC/ETH metrics (MVRV, exchange flows) | Glassnode | glassnode.com → Studio → select metric |

**Freshness rule:** Always note the query date on any chart sourced from a live dashboard. Flag any data older than 30 days on fast-moving metrics (TVL, stablecoin supply, protocol revenue).

---

## Paragraph-Level Quality Gate

Every paragraph must clear this gate before you move to the next one.

Score two dimensions on a 1–10 scale:

**Signal score**
Does this paragraph advance the thesis?
Does it contain at least one of: a specific mechanism, a named data point, a named protocol/person/event, or an explicit implication?
Could it be cut without the reader missing anything? If yes → low signal.

**Human score**
Does this read like a person wrote it?
Does it commit to a position rather than hedge around one?
Is the word choice specific, occasionally unexpected — not the "correct" word but the *right* word?
Does it pass the AI detection check from CLAUDE.md?

**Scoring method: Harmonic Mean**
Formula: H = 2(S × H) / (S + H)

Use harmonic mean, not arithmetic. A paragraph that is technically precise but written like a press release fails. A paragraph that reads naturally but says nothing also fails.

**Minimum: 8.5 in BOTH Signal AND Human before the harmonic mean is computed.**
At 8.5/8.5 → HM = 8.5. That is the floor.
Below 8.5 in either dimension → rewrite before advancing.

When a paragraph is high signal but low human: find the sentence that would make a person reading on their phone stop scrolling. Lead with that.
When a paragraph is high human but low signal: add a specific constraint — a number, a named mechanism, a concrete implication — that makes the point non-generic.

Never present a paragraph with a harmonic mean below 8.0.

---

## Article-Level Quality Gate

After the full draft is complete, score the article as a whole on the same two dimensions:

**Signal coherence score**
Does the thesis hold through every paragraph?
Does each section add something the previous one didn't?
Is the argument cumulative — does the reader know more at the end than at the start?

**Human voice score**
Does the whole piece sound like one person with a consistent point of view?
Does it pass the full AI Detection Check from CLAUDE.md applied to the entire article?
Does it commit to a position from the first paragraph and hold it?

Apply the same harmonic mean formula. Minimum 8.5 in both.
If the article-level score fails, identify which section is pulling the score down and rewrite it before returning output.

---

## AI Detection Check (final gate)

Load and apply the AI Detection Check from CLAUDE.md before returning any output.

Specific tells to eliminate from article prose:

- Em-dashes — avoid entirely. En-dashes fine for ranges and contrasts.
- Transition words nobody says out loud: "Furthermore", "Moreover", "It's worth noting", "It's important to consider"
- Naked hedging with nothing behind it: "This could potentially suggest..." — hedge only when backed by data or a stated reason
- Perfectly balanced takes that see every side without committing to one
- Sentences that start with "This" referring to the previous sentence
- Summary paragraphs that restate what the article just argued
- Endings that wrap everything up neatly — end on an implication, not a bow
- Vocabulary flags: "delve", "certainly", "absolutely", "of course", "in conclusion", "in summary", "landscape", "ecosystem" (when used generically)

---

## Format — X Article (750–1,250 words)

**Structure:**
- No headers or section labels
- Hook paragraph: 1–2 sentences. Thesis-first. The reader should know the claim before the first scroll.
- Body: 5–8 paragraphs, max 3 sentences each. One idea per paragraph. Each paragraph advances the argument — no setup-only paragraphs.
- Final paragraph: ends on an implication or a forward-looking observation. Not a summary. Not a call to action.

**Mobile-first rules:**
- Max 3 sentences per paragraph — no exceptions
- If a paragraph runs longer, break it
- No lists — write in prose
- No pull quotes or formatting — plain text only

**Tone:**
Sharp and committed. Reads like a smart reporter who also reads on-chain data. Does not sound like a newsletter.

---

## Format — Substack (1,250–2,500 words)

**Structure:**
- 2–3 light headers maximum. Headers are section labels, not titles — keep them short and functional.
- Hook section (2–3 paragraphs): establish stakes. Why this topic, why now, what the piece will argue.
- Development sections: mechanism, data, counternarrative, implications — in whatever sequence the argument requires. One coherent argument unit per section.
- Closing section: forward-looking implication. Not a summary. The last paragraph should leave the reader with something to think about, not a recap of what they just read.

**Tone:**
More developed than X Article but not more tentative. The extra length is for more evidence and more mechanism — not for hedging or balance. The POV stays consistent throughout.

---

## Output Format

Return the article followed by a scoring report.

```
# [Article Title]

[Full article text]

---

## Scoring Report

**Mode:** [X Article / Substack]
**Word count:** [N] (~[N] minute read)
**Analyst voice mode:** [Selected mode]

### Paragraph Scores
| # | Signal | Human | HM | Status |
|---|---|---|---|---|
| 1 | X | X | X | Pass / Rewritten |
| 2 | X | X | X | Pass / Rewritten |
...

### Article-Level Scores
Signal coherence: X/10
Human voice: X/10
Harmonic mean: X

### AI Detection
Tells removed: [list any that were caught and fixed]
Final assessment: [Clean / Rewritten]

### Chart Index
| # | Placement | What it shows | Source | How to find it |
|---|---|---|---|---|
| 1 | After para [N] | [description] | [platform] | [path or dashboard] |
| 2 | After para [N] | [description] | [platform] | [path or dashboard] |

### What was cut or caveated
[Any claims removed for lack of sourcing, or caveated with explicit uncertainty]
```

---

## Quality Gates Checklist

Before returning output, verify:

- [ ] Chart suggestions identified for every visual-worthy data point
- [ ] Each chart suggestion includes platform, navigation path, and freshness note
- [ ] Chart suggestions placed inline immediately before the paragraph they support
- [ ] Chart index included in scoring report
- [ ] All claims fact-checked against Tier 1 or Tier 2 sources
- [ ] All data points sourced and timestamped
- [ ] Counternarrative-flags.md was loaded and checked
- [ ] One analyst voice mode selected and held throughout
- [ ] Every paragraph cleared 8.5 Signal AND 8.5 Human before advancing
- [ ] Article-level harmonic mean ≥ 8.5 in both dimensions
- [ ] AI detection check applied to full text
- [ ] Word count within mode range (750–1,250 for X Article / 1,250–2,500 for Substack)
- [ ] Article ends on an implication, not a summary
- [ ] No paragraph exceeds 3 sentences (X Article)
- [ ] No more than 3 headers (Substack)
- [ ] Scoring report included
