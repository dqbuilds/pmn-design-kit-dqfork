# Workflow — Segment Brief

Use this workflow when researching a topic for a podcast segment. Output is a
full briefing document the host can use directly for prep.

---

## Step-by-Step Protocol

### Step 1 — Scope the Segment
Identify:
- The core claim or question the segment is answering
- The audience assumption level (crypto-native vs. mainstream crossover)
- Whether this is breaking news, analysis, or explainer content
- Which textbook chapter(s) apply — consult before searching

### Step 2 — Build the Source Stack
For each major claim in the segment, identify and search in tier order:
1. Tier 2 primary sources first (on-chain data, gov filings, protocol docs)
2. Tier 1 crypto-native outlets for narrative and context
3. Tier 3 only for macro framing or when institutional sourcing is superior

Minimum source requirements:
- At least 2 independent Tier 1/2 sources per major factual claim
- At least 1 on-chain data point per segment if the topic is protocol-related
- At least 1 counter-narrative or critical perspective per segment

### Step 3 — Contradiction and Counternarrative Check
Before writing the brief:
- Check `context/counternarrative-flags.md` for the topic area
- Check if on-chain data contradicts narrative claims from news sources
- Check if the textbook suggests the mechanism should behave differently
  than how it's being reported

**Counternarrative deployment rule:** Only surface a counter if it is backed
by a specific data point, documented mechanism, or named source. If the
original claim is directionally correct and the counter is a footnote, frame
it as nuance — not contradiction. A valid claim with pushback is the goal.
Do not manufacture contrarianism where the underlying claim holds up.

### Step 4 — Write the Brief
Use the template below. Hard constraints:
- Summary: max 4 sentences
- Key data points: max 6 bullets
- Talking points: max 5, each under 35 words
- Questions: max 4

**Complexity override:** For technically dense segments (DeFi mechanics, L1
architecture, custody, regulatory deep-dives), limits may expand by 50% —
but note the override and justify each expansion briefly in the brief header.

---

## Output Template

```
## [Segment Title]

**Verification status:** ✅ Verified / ⚠️ Partially Verified / 🔄 Contested
**Confidence:** [High / Medium / Low] — [Brief reason]
**Audience level:** [Crypto-native / Crossover / Mainstream]

---

### Summary
[Max 4 sentences. What actually happened or what is actually true.
Written in plain English — no jargon without a one-phrase gloss.]

---

### Key Data Points
- [Stat or fact] — [Source, Date]
- [Stat or fact] — [Source, Date]
- [Stat or fact] — [Source, Date]
[Max 6 bullets. Each must have an inline source.]

---

### Primary Sources
- [Outlet/Platform] — [URL] — [Date] — Tier [1/2/3]
[List all sources used. Minimum 3.]

---

### Context & Nuance
[What the headline misses. Counter-narratives. Structural caveats.
What would make a technically true statement misleading on air.
Draw from counternarrative-flags.md where applicable.]

---

### Suggested Talking Points
1. [Max 35 words. Punchy. Cite-able. Accurate at sentence level.]
2. [Max 35 words.]
3. [Max 35 words.]
[Max 5 total.]

---

### What to Avoid Saying
[Specific phrasings or framings that are inaccurate, misleading, or likely
to age badly. Be direct — "don't say X, say Y instead."]

---

### Questions This Opens
- [Open question worth exploring in the segment or with a guest]
- [Open question]
[Max 4.]
```

---

## Quality Gates

Before delivering the brief, verify:
- [ ] Every stat traces back to its original data source, not a news article
- [ ] At least one critical or counter perspective is included
- [ ] "First ever" or superlative language has been explicitly confirmed
- [ ] On-chain data has a query timestamp
- [ ] No claim relies solely on a Tier 3 or Tier 4 source
- [ ] Talking points are accurate word-for-word, not just directionally
- [ ] counternarrative-flags.md was checked for this topic area
