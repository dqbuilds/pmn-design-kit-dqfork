# Workflow — Guest Diligence

Use this workflow when prepping to interview a specific person or company.
The goal is to give the host enough technical fluency and contextual knowledge
to ask questions the guest hasn't been asked before.

---

## Step-by-Step Protocol

### Step 1 — Domain Mapping
Identify the guest's primary domain(s) and map to textbook chapters
(see sources/tier2-primary.md for the full index).

Common domain mappings:
- DeFi protocol founder → Ch 7 (DeFi), Ch 8 (MEV), Ch 12 (Governance)
- L1/L2 infrastructure → Ch 2 (Ethereum), Ch 3 (Solana), Ch 4 (L1s)
- Institutional/TradFi → Ch 9 (Stablecoins/RWAs), Ch 6 (Market Structure)
- Bitcoin-focused → Ch 1 (Bitcoin)
- Custody/security → Ch 5 (Custody)
- NFT/gaming/consumer → Ch 11 (NFTs)
- Stablecoin issuer → Ch 9 (Stablecoins/RWAs)
- DePIN → Ch 13 (DePIN)
- Prediction markets → Ch 15 (Prediction Markets)

### Step 2 — Textbook Grounding
Read the relevant chapters before searching news. This prevents the host
from accidentally using incorrect terminology or asking mechanically confused
questions. Note any concepts that are commonly misunderstood in the guest's
domain — these are often good question angles.

### Step 3 — Research the Guest
**Check for repeat appearances first.** Search your episode history and Podscan
(podscan.fm) for this guest's name. If they've appeared before: note the episode,
list the questions already asked, and flag topics that were covered so they are
not repeated. Prior appearance context belongs in the brief header.

Search across Tier 1 outlets, Podscan, and primary sources. Build a profile covering:

**Public record:**
- Current role, company, and what they're building
- Founding story and background (prior roles, projects)
- Most recent major announcement or news item
- Conference talks, podcast appearances, long-form interviews

**Stated positions:**
- Their public thesis on their domain (what do they believe that others don't?)
- Predictions they've made publicly (and whether they were right)
- How their position has evolved over time

**Controversies and contested claims:**
- Has their project been criticized? By whom? Is the criticism substantiated?
- Have they made claims that Protos, The Defiant, or other critical outlets
  have disputed?
- Any regulatory, legal, or community governance conflicts?

**Competitive landscape:**
- Who are their main competitors and how do they publicly differentiate?
- What do critics of their approach say?

### Step 4 — Check Counternarrative Flags
Load `context/counternarrative-flags.md` and check if the guest's domain or
specific project appears. If it does, build at least one question around the
contested narrative.

**Before using a flag:** Confirm it meets the standard in that file — a specific
data point or mechanism must back the counter, not just a general sense that
the claim is oversold. If the guest's stated position is directionally correct
and the flag is a nuance, frame the question as clarifying rather than adversarial.
The goal is a better conversation, not gotcha contrarianism. An unsupported
pushback wastes interview time and signals to the guest that you haven't done
the work.

### Step 5 — Generate Questions

**Before writing a single question, load `context/question-craft.md`.**
Every question must pass the Question Quality Check and Harmonic Mean Scoring
framework in that file. The core discipline: arrive deeply informed, but keep
that research out of the questions. The question should create a vacuum the
guest has to fill — not a thesis they can agree with, qualify, or push back on.

**Tone standard — non-negotiable:** Every question must carry a neutral-to-slightly-positive
connotation. This is not about being soft. It is about making honesty easier than
deflection. A guest who feels accused gives a rehearsed rebuttal. A guest who feels
genuinely asked gives a real answer. The goal is always the real answer.

**Controversy questions — special rule:** If any of the 5 questions touch on
allegations, legal proceedings, regulatory action, or contested press coverage,
apply the Controversy Question Protocol from `context/question-craft.md` before
scoring. Questions that name an allegation directly fail the neutral-to-positive
check regardless of signal score. Reframe as a mechanism or decision question.
The test: would the guest feel accused or curious? If accused — rewrite.

**Two versions per question — always.**
For each of the 5 question types below, produce two versions:
- **Version A (humanity-led):** Personal frame first, signal embedded inside.
- **Version B (signal-led):** Specific constraint first, generous framing second.

Both versions must score **minimum 8.5 on both signal AND human dimensions**
before being presented. Score each using harmonic mean: H = 2(S × H) / (S + H).
If either version fails the threshold, rewrite before presenting.

**Compound question rule — enforced:** Each version must contain exactly one question.
Before presenting any question, read it aloud and count the question marks and
the "and"s that join distinct asks. If there are two things the guest could answer
separately — split it. Ask the harder one. Compound questions give the guest an
escape hatch: they will always answer the easier half and the harder half goes
unaddressed. Use compound structure only when the two parts are so tightly
linked that splitting them would lose the meaning entirely — which is rare.

The host chooses which version to use. Present both — do not pre-select.

---

Produce 5 question pairs in this order:

1. **Warm-up / credibility establishment** — Draw on their origin story or
   background. Ask about the journey, not the achievement.
   *Non-leading check: no compliment-loading, no flattery.*
   > ❌ "You've had a remarkable path — what drove you into this space?"
   > ✅ A: "What's the first moment you remember thinking the thing you were building at [prior role] wasn't enough?"
   > ✅ B: "What were you working on right before this, and what made the timing right to leave?"

2. **Core thesis** — Make them state their central belief without your framing
   pre-loaded. Do not name the thesis you found in research.
   *Non-leading check: no thesis-first setup.*
   > ❌ "You've argued governance tokens are structurally broken — can you explain?"
   > ✅ A: "What's the thing you believe about [their domain] that most people in the room would push back on?"
   > ✅ B: "What does your user acquisition actually look like right now?"

3. **Technical depth / mechanism** — Ask how something works, not whether it
   works. Only someone who read the relevant textbook chapter would know to ask.
   *Non-leading check: ask about mechanism, not narrative.*
   > ❌ "Has the Atlas upgrade meaningfully improved zkSync's position?"
   > ✅ A: "Walk me through what actually happens on your end when a transaction settles — what does that process feel like to manage?"
   > ✅ B: "Walk me through how Atlas actually changes the liquidity fragmentation problem."

4. **Contested territory** — From `context/counternarrative-flags.md` or a
   controversy from Step 3. Assume they've thought about this honestly.
   Frame it as a mechanism question, not a "critics say" question.
   *Non-leading check: don't frame as gotcha, don't soften with preamble.*
   > ❌ "Critics argue your TVL is inflated by mercenary capital — how do you respond?"
   > ✅ A: "What does the data actually look like after the incentive program ends — have you seen that play out yet?"
   > ✅ B: "What percentage of your TVL do you think stays if you remove the incentive program?"

5. **Adversarial / forward-looking** — The question they least want to answer.
   Don't make it a trap. Create space for them to answer honestly.
   *Non-leading check: no comfort cushioning, but no ambush either.*
   > ❌ "Given everything you've built, what keeps you up at night?"
   > ✅ A: "What's the version of this that doesn't work — and how close do you think you are to that line?"
   > ✅ B: "What would have to be true for this to fail?"

---

## Output Format

```
## Guest: [Name] — [Title, Company]

### Domain Summary
[2–3 sentences on their domain and why it matters right now]

### Relevant Textbook Chapters
- [Chapter]: [Why relevant, key concept to understand]

### Key Background
**Current focus:** [What they're building/leading right now]
**Thesis:** [Their core public belief, in one sentence]
**Recent news:** [Most significant recent development, with source]

### Controversies / Contested Claims
- [Claim or criticism] — [Source, date] — [Status: substantiated/disputed/ongoing]

### 5 Interview Question Pairs

Each pair includes a humanity-led version (A) and a signal-led version (B).
Both versions are scored on signal, human, and harmonic mean.
Minimum threshold: 8.5 on both dimensions. Host selects which to use.

**Q1 (Warm-up):**
*Version A — humanity-led:*
[Question text]
Signal: X/10 | Human: X/10 | HM: X

*Version B — signal-led:*
[Question text]
Signal: X/10 | Human: X/10 | HM: X

*Why ask:* [What you're hoping to surface — stated as what you don't yet know]

---

**Q2 (Core thesis):**
*Version A — humanity-led:*
[Question text]
Signal: X/10 | Human: X/10 | HM: X

*Version B — signal-led:*
[Question text]
Signal: X/10 | Human: X/10 | HM: X

*Why ask:* [What you're hoping to surface — stated as what you don't yet know]

---

**Q3 (Technical depth):**
*Version A — humanity-led:*
[Question text]
Signal: X/10 | Human: X/10 | HM: X

*Version B — signal-led:*
[Question text]
Signal: X/10 | Human: X/10 | HM: X

*Why ask:* [What you're hoping to surface — stated as what you don't yet know]

---

**Q4 (Contested territory):**
*Version A — humanity-led:*
[Question text]
Signal: X/10 | Human: X/10 | HM: X

*Version B — signal-led:*
[Question text]
Signal: X/10 | Human: X/10 | HM: X

*Why ask:* [What you're hoping to surface — stated as what you don't yet know]

---

**Q5 (Adversarial):**
*Version A — humanity-led:*
[Question text]
Signal: X/10 | Human: X/10 | HM: X

*Version B — signal-led:*
[Question text]
Signal: X/10 | Human: X/10 | HM: X

*Why ask:* [What you're hoping to surface — stated as what you don't yet know]

### Sources
- [Outlet] — [URL] — [Date] — Tier [1/2/3]

### Content Seeds
*After delivering this brief, offer to run `workflows/content-plan.md` +
`content-plans/CONTENT-PLAN-ARCHETYPES.md` against these seeds to generate
the full publishing calendar.*

**Macro hook (pre-recording tweet):**
[One sentence: the live news development that makes this episode timely right now]

**Data story (standalone tweet or short thread):**
[The specific number from the brief that surprises or contradicts CT consensus — stated plainly]

**Counternarrative (high-engagement post):**
[The inflated claim or common misconception from this brief worth correcting publicly]

**Pre-drop thread angle:**
[The "why this guest, why now" hook — one sentence that would make someone who already knows this guest stop scrolling]

**Long-form angle (article / newsletter):**
[The topic from this brief that needs more than a thread — the mechanism, the comparison, or the stakes that deserve 800–1200 words]
```
