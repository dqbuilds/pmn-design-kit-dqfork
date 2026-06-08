# Workflow — Content Plan (Episode Publishing Calendar)

Use this workflow when an episode brief has been completed and you need a
full publishing calendar: what to write, in what format, in what order,
and why each piece earns its place.

This workflow mines the brief for five types of content seeds and produces
a prioritized calendar with one-line rationales, format recommendations,
and the specific angle for each piece. It does NOT write the content —
it produces the plan. Use the appropriate workflow to execute each piece.

Load `style/voice.md` before finalizing format recommendations.

---

## Step-by-Step Protocol

### Step 1 — Identify the Content Seeds

Read the completed episode brief and tag the following:

**Seed Type A — The Macro Hook**
Any financially relevant macro or geopolitical development referenced in
the brief that connects to the episode's core topic. This is always
publishable standalone because it has urgency independent of the episode.

**Seed Type B — The Data Story**
Any on-chain metric, market data point, or financial figure from the brief
that tells a story on its own. These should be stated plainly in a single
tweet or short thread (Adam Tehc mode). Best if the data contradicts the
prevailing narrative on CT.

**Seed Type C — The Counternarrative**
Any contested claim, inflated comparison, or common misconception surfaced
in the brief (from `context/counternarrative-flags.md` or original research).
These are the highest-engagement content type — the "actually..." post.
Works as a standalone tweet, short thread, or article depending on complexity.

**Seed Type D — The Episode Frame**
The "why this guest, why now" hook — the pre-interview thread. Draws on
the macro context + the guest's thesis + one unanswered question.

**Seed Type E — The Long-Form Angle**
Any topic from the brief that requires more than a thread to do justice —
a mechanism that needs diagrams, a regulatory analysis, a historical
comparison. These become articles or newsletter pieces.

---

### Step 2 — Sequence by Publishing Stage

Map each seed to the correct publishing window:

```
PRE-RECORDING (1–2 weeks before episode):
  → Macro hook tweet(s) — establish context while the topic is live
  → Data story tweet(s) — "why this matters now" fuel
  → Counternarrative post — prime the audience to ask better questions

PRE-DROP (48–72 hrs before episode publishes):
  → Pre-interview thread — drive anticipation, frame the conversation

POST-DROP (within 24–48 hrs of episode going live):
  → Post-interview thread — synthesize what actually landed
  → Quotable standalone tweet — the single most re-shareable moment

EVERGREEN (1–2 weeks after drop, or anytime):
  → Article / newsletter — the long-form angle that gives the topic room
  → Second-order data tweet — updated metrics now that the conversation
    has had time to circulate
```

---

### Step 3 — Prioritize by Impact

Rank the planned pieces by expected reach × relevance to audience. Use
this heuristic:

| Piece Type | Typical Reach | Best Condition |
|---|---|---|
| Counternarrative tweet | Highest | When it contradicts a widely held belief |
| Data tweet (Adam Tehc) | High | When the number surprises |
| Pre-interview thread | Medium-High | When the guest is well-known or the topic is hot |
| Post-interview thread | Medium-High | When the conversation produced a genuine reveal |
| Standalone quotable | Medium | When the guest said something no one expected |
| Article / newsletter | Lower reach, higher trust | When the mechanism needs more than 280 chars |

---

### Step 4 — Write the Content Plan

Produce one entry per planned piece. Each entry must contain:

```
## [Piece Number] — [Content Type]: [Working Title]
**Publishing window:** [Pre-recording / Pre-drop / Post-drop / Evergreen]
**Format:** [Single tweet / Short thread (3–5) / Full thread (6+) / Article]
**Angle:** [One sentence: what is the specific claim or story this piece makes?]
**Hook:** [Draft opening line or tweet 1 — this is the deliverable the host can react to]
**Source(s):** [What from the brief or external research supports this piece?]
**Execute with:** [Which workflow to load: thread-pre.md / thread-post.md / standalone]
**Why this piece earns its place:** [One sentence on what it does for the audience
  or for the episode that nothing else in the calendar does]
```

---

### Step 5 — Flag Dependencies

Note which pieces depend on other pieces being published first, and which
pieces are time-sensitive (i.e., tied to a live news event that will age).

Format:
```
Dependencies:
- [Piece 3] must publish before [Piece 4] (establishes context)
- [Piece 1] is time-sensitive — tied to [event/data point] — publish within [timeframe]
```

---

## Output Format

```
# Content Plan — [Guest Name] Episode
**Episode status:** [Pre-recording / Recorded / Dropping [date]]
**Total pieces planned:** [N]

---

## Publishing Calendar

### PRE-RECORDING

[Piece entries]

---

### PRE-DROP

[Piece entries]

---

### POST-DROP

[Piece entries]

---

### EVERGREEN

[Piece entries]

---

## Dependencies & Time-Sensitive Flags

[Dependency notes]

---

## What NOT to Write

[1–3 content ideas that seem obvious from the brief but would be weak,
redundant, or age badly. One sentence each on why to skip them.]
```

---

## Quality Gates

Before delivering the content plan, verify:
- [ ] Every piece has a specific angle, not a generic topic area
- [ ] At least one piece contradicts something (counternarrative)
- [ ] At least one piece uses data plainly (Adam Tehc mode)
- [ ] No two pieces make the same argument in different formats
- [ ] The pre-drop thread has a hook that works without knowing the episode outcome
- [ ] The "What NOT to Write" section exists — it prevents calendar bloat
- [ ] Every piece has a "why this piece earns its place" rationale
- [ ] Time-sensitive pieces are flagged with a publish-by window

---

## Format Decision Guide

Use this to decide between a tweet, thread, or article for any given angle:

**Single tweet** when:
- The entire argument fits in one number + one implication
- The counternarrative can be stated in one sentence
- It's a reaction to breaking news that needs immediacy over depth

**Short thread (3–5 tweets)** when:
- The argument has 2–3 sequential steps
- You need one tweet of context + one of data + one of implication
- The Adam Tehc accumulation stack applies (same story, multiple data beats)

**Full thread (6+ tweets)** when:
- This is a pre or post-interview thread following standard structure
- The topic has multiple mechanisms worth explaining sequentially
- You're making a case that requires building evidence across beats

**Article / newsletter** when:
- The mechanism requires more than 280 characters to explain accurately
- The topic has a historical dimension that needs context
- You want something that persists and can be linked to from future episodes
- The counternarrative is complex enough that a tweet would be misleading

---

## Article Angle Identification

When the brief contains an Evergreen article seed, use this framework to
sharpen the angle before committing to writing it:

**The explainer angle:** "Here is how [mechanism] actually works"
Best when: the brief surfaced a technical distinction most of CT gets wrong

**The comparison angle:** "Here is why [X] and [Y] are not the same thing"
Best when: the brief surfaced an inflated comparison or conflation

**The trajectory angle:** "Here is what [trend] looks like if it continues"
Best when: the brief contains data with a clear directional story

**The stakes angle:** "Here is why [topic] matters more than the coverage suggests"
Best when: the episode touches something underreported relative to its significance

Only use one angle per article. Mixing angles produces unfocused pieces.
