# Workflow — Video Script (Short Form)

Use this workflow when writing a short-form video script for a news or research topic.
Target formats: Instagram Reels, TikTok, YouTube Shorts, LinkedIn video.
Target runtime: 45 seconds to 2 minutes.

---

## Speaking Pace Reference

Use these word counts as hard limits per target runtime:

| Target Runtime | Word Count |
|---|---|
| 45 seconds | 95–110 words |
| 60 seconds | 125–145 words |
| 90 seconds | 190–220 words |
| 2 minutes | 255–290 words |

Default to the low end. Deliberate delivery lands better than rushed delivery.

---

## Step 1 — Research Phase (Call Other Subskills)

Before writing a single line of script, ground the topic in sourced facts.

**For news-driven topics:**
Load `workflows/segment-brief.md` — run the full segment brief protocol.
This produces: verified claims, key data points, counternarrative check, sourced talking points.

**For data-driven topics:**
Load `workflows/data-pull.md` + `sources/tier2-primary.md` — pull the specific metrics.
Every number used in the script must trace back to a primary source.

**For topics tied to a guest or episode:**
Load `workflows/guest-diligence.md` + the relevant episode brief from `../podcast-briefs/`.
Pull the 2–3 most compelling facts or claims from that brief to anchor the script.

**Always run:**
`context/counternarrative-flags.md` — check the topic area before scripting.
If a counternarrative flag applies, it either becomes the hook or a check on what not to overstate.

**Always apply:**
`style/voice-base.md` — tone, structure, what to avoid.

---

## Step 2 — Select Runtime and Structure

Ask or infer the target runtime before writing.

If the topic is a single data point or news item: 45–60 seconds.
If the topic requires mechanism explanation: 90 seconds.
If the topic needs context + mechanism + implication: 2 minutes.

Do not pad to hit a longer runtime. A tight 45-second script beats a bloated 90-second one.

---

## Step 3 — Script Structure

Every script has five beats. Adjust time allocation per runtime target.

### Beat 1 — Hook (0–3 seconds)
One line. Spoken. Stops the scroll in the first 2–3 seconds or the video is dead.

The hook is not a headline. Not a thesis. Not a teaser. It is the most counterintuitive,
specific, or provocative version of the story — stated as a hard fact that creates an
immediate question in the viewer's mind before they can decide to scroll.

**The 2-second rule:** If the hook doesn't land by the second word, rewrite it.
Algorithms surface the first 2–3 seconds to cold audiences. That window is the entire battle.

---

#### Hook Framework — Choose One Type

**Type 1: Number Shock**
Lead with a specific number that reframes the story's scale. The number must create
cognitive dissonance — either larger or smaller than expected.

> ❌ "Aviva is one of the biggest asset managers in the UK."
> ✅ "Aviva manages £262 billion. They just picked a blockchain with $38 million in DEX volume."

The gap between the two numbers IS the hook.

---

**Type 2: Consequence Lead**
Start with the outcome or implication, not the cause. Skip the setup entirely.
Viewers will stay to learn how you got there.

> ❌ "Today we're breaking down the Aviva and Ripple partnership."
> ✅ "Traditional finance just handed DeFi its first real test case."

---

**Type 3: Pattern Interrupt**
State something that contradicts what the viewer already believes.
The contradiction must be true — not clickbait, not a hedge.

> ❌ "Most people don't understand DeFi."
> ✅ "The most boring part of DeFi — lending rails — is what institutional money actually wants."

---

**Type 4: Bold Claim**
State the most provocative true thing about the story. Not the balanced take.
The take that makes someone in the space want to argue or share.

> ❌ "XRPL is gaining institutional traction."
> ✅ "XRPL skipped retail and went straight to institutional. That's either genius or a death sentence."

---

#### Hook Rules

- Name a specific number, company, or event in the first sentence
- Do not start with "So," "Hey," "Today we're talking about," or "Did you know"
- Do not ask a question — state a fact that creates a question in the viewer's mind
- Must work without captions (audio-on viewers) and without audio (caption-only viewers)
- The first word sets the tone — make it a noun or a number, never a filler word
- If the hook requires more than one sentence, it's two sentences max — never three

#### First-Frame Visual (0–3 seconds)
What appears on screen during the hook determines whether caption-only viewers stop.

- Lead with the most striking number or claim as on-screen text — not the speaker's face
- Text should be large, high-contrast, single line
- If the hook is a number: put the number on screen before you say it
- Avoid lower-thirds or small text overlays — they don't stop the scroll

#### Hook Scoring (run before finalizing)

Score the hook 1–10 on each:

| Dimension | Question |
|---|---|
| Specificity | Does it name a real number, company, or event? |
| Surprise | Does it contradict or reframe something the viewer assumed? |
| Compression | Is every word earning its place — could any be cut? |
| Scroll-stop | Would this make you stop mid-scroll? |

If any dimension scores below 7, rewrite the hook before moving to Beat 2.
A great script with a weak hook is an unwatched video.

### Beat 2 — Setup (5–20 seconds)
What happened. Why now. One or two sentences maximum.
No jargon without a one-phrase gloss. Assume the viewer knows crypto but not this specific story.

### Beat 3 — Mechanism (20–50 seconds)
Why it matters. How it works. The thing most coverage gets wrong or skips.
This is where the research from Step 1 lands — one specific fact or mechanism, not a list.

Pull from the segment brief's "Context & Nuance" section if available.
If a counternarrative flag applies, deploy it here — not as "critics say" but as a mechanism check.

### Beat 4 — Data Point (50–80 seconds, or omit for 45-second scripts)
One number. Sourced. Stated plainly.
Do not stack multiple stats. One number lands. Three numbers blur.

Format: state the number, state what it means, move on.
> "XRPL's DEX has $38 million in TVL. Aviva manages $330 billion. One of those numbers has to move."

### Beat 5 — Close (final 10–15 seconds)
The implication. Not a call to action. Not "follow for more."
A single sentence that gives the viewer something to think about or repeat.

Rules:
- Commit to a position — do not hedge
- Do not end with a question
- Do not end with "let me know what you think"
- The last line should work as a standalone tweet

---

## Step 4 — Script Formatting

Format the final script exactly as shown below.
Include timing markers, word count, estimated runtime, and B-roll notes.

```
## [Script Title]

**Target runtime:** [45s / 60s / 90s / 2min]
**Word count:** [X words]
**Estimated runtime at deliberate pace:** [X seconds]
**Fact-check status:** ✅ All claims sourced / ⚠️ Flag any unverified claims

---

### Script

[HOOK — 0:00–0:05]
[Line]

[SETUP — 0:05–0:20]
[Line. Line.]

[MECHANISM — 0:20–0:50]
[Line. Line. Line.]

[DATA — 0:50–1:10]
[Line.]

[CLOSE — final 10–15 seconds]
[Line.]

---

### B-Roll / Visual Notes
- Hook frame: [what should be on screen at second 0]
- Data beat: [suggest chart, graphic, or on-screen text]
- Close: [suggest text overlay or hold on speaker]

---

### Hook Alternatives
1. [Alternative hook line]
2. [Alternative hook line]
3. [Alternative hook line]

---

### Sources Used
- [Source] — [URL] — [Date] — Tier [1/2/3]
```

---

## Step 5 — Quality Gates

Before delivering the script, verify:

- [ ] Every claim traces to a source from the segment brief or data pull
- [ ] Word count is within the target runtime range
- [ ] Hook does not start with "So," "Hey," "Did you know," or a question
- [ ] No more than one data point in Beat 4
- [ ] Close commits to a position — no hedging, no invitation to engage
- [ ] Counternarrative-flags.md was checked for this topic
- [ ] The hook line works as a standalone tweet (test it)
- [ ] No jargon without a one-phrase gloss

---

## Step 6 — Signal Check on Hook

After writing the script, run a signal check on the hook line only using the
signal-filter scoring categories:

- Originality: Is this non-generic?
- Clarity: Does it land on first listen?
- Compression: Is every word earning its place?
- Implication Strength: Does it create a question in the viewer's mind?

If the hook scores below 7/10 on any category, rewrite it before delivering the script.
The hook is the only line that determines whether the video gets watched.

---

## Runtime Decision Tree

```
Is this a single data point or announcement?
  → 45–60 seconds

Does it require explaining a mechanism (how something works)?
  → 90 seconds

Does it need context + mechanism + implication + data?
  → 2 minutes

Is the research still being gathered?
  → Run segment-brief.md or data-pull.md first, then return here
```
