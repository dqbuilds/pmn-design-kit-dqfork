# Workflow — Live Tweet (During Recording)

Use this workflow when the episode is a live stream and you need to generate
tweets that can be posted in real time during the recording. Goal: capture the
moments worth sharing before the episode is archived, without editorially
framing what hasn't finished yet.

Load `style/voice-base.md` before writing anything.

---

## When to Use This Workflow vs. Post-Production

**Live tweet:** For moments that are time-sensitive — a coined term, a
surprising data point, a line that lands so cleanly it should go out now.

**Post-production thread:** For synthesis — the takeaways, the arc,
the "what this means." That requires the full conversation.

Do not try to do both at once. Live tweets capture moments. Post-production
threads construct meaning. They require different inputs.

---

## What Qualifies as a Live-Tweetable Moment

Not every exchange is worth live tweeting. Surface only:

**1. Coined terms or new language**
A guest invents a phrase that compresses a behavior or concept nobody has named yet.
> Example: "Clawdogging" — giving an agent a private key and letting it deploy
> smart contracts with minimal guardrails.

**2. Clean data-backed claims**
A specific number with context attached. Not a vague assertion — a number
that tells a story in one sentence.
> Example: "Base is running ~90% of X402 transaction volume right now."

**3. Direct quotes that compress a large idea**
A line the guest said that would make someone who wasn't watching stop scrolling.
Must be accurate to what was said — no paraphrase that shifts meaning.

**4. Moments of productive tension**
Two guests disagree on something specific and substantive. Frame the
disagreement without picking a side. The debate is the content.

**5. Counterintuitive one-liners**
A claim that flips the obvious read of something. Worth surfacing immediately
because the audience is primed to engage with it while it's live.

---

## What Does NOT Qualify

- General agreement or banter — not worth the character budget
- Anything that requires post-production context to make sense
- Claims you can't verify in real time — flag for post-production fact-check instead
- Price commentary or market speculation from guests — too hot to handle live
- Anything that would require explanation longer than the tweet itself

---

## Format Rules for Live Tweets

**Speaker attribution — always.** This is a multi-guest show. The reader
doesn't know who said what. First name + context on first reference.

> ✅ "Austin Griffith, Ethereum Foundation:"
> ✅ "Sam Green, Cambrian Network:"
> ❌ "Guest says..."

**Present tense.** It's happening now.
> ✅ "Austin on why agents don't need standards the way humans do..."
> ❌ "Austin explained that agents..."

**No editorial framing.** Save the takes for post-production. The live
tweet reports the moment. It does not conclude from it.
> ✅ "Sam: 'For the purely agentic economy, X402 is brilliant. You just can't beat permissionless.'"
> ❌ "Sam just confirmed X402 will win the payments wars. Big."

**No formula structure.** Live tweets are not drafts from tweet-drafter.
They are moment captures. One speaker, one moment, one line.

**Include timestamp.** Every live tweet draft should carry a timestamp reference
(e.g., `[~00:49]`) so it can be matched to the recording for post-production use.
The timestamp is internal — not in the published tweet.

**Character limit:** 220 characters target, 280 maximum.

---

## Step-by-Step Protocol

### Step 1 — Ingest the transcript or live notes
If working from a live feed or partial transcript, read enough to identify
the 5–8 moments worth capturing. Do not start writing until you've scanned
ahead enough to know whether a moment is the best version of itself.

### Step 2 — Tag qualifying moments
Identify each moment by type:
- Coined term
- Data-backed claim
- Direct quote
- Productive tension
- Counterintuitive one-liner

Discard anything that doesn't fit a type. Resist the urge to over-tweet.

### Step 3 — Draft live tweets
One tweet per moment. Speaker attribution. Present tense. No framing.
Under 220 characters. Include internal timestamp marker.

### Step 4 — Flag post-production seeds
After the live tweet drafts, list the 2–3 moments from the transcript that
are NOT suited for live tweeting but ARE high-value for the post-production
thread. These become the inputs for `workflows/thread-post.md`.

---

## Output Format

```
## Live Tweets — [Episode Name / Number]
**Format:** Live stream
**Guests:** [Names, titles]
**Status:** [Recording in progress / Recording complete — use for timing guidance]

---

### Live Tweet 1
[~timestamp]
[Tweet text — under 220 chars]
**Moment type:** [Coined term / Data claim / Direct quote / Tension / One-liner]
**Post if:** [Condition — e.g., "post immediately once defined on air"]

---

### Live Tweet 2
[~timestamp]
[Tweet text]
**Moment type:**
**Post if:**

---

[Continue for all qualified moments — 5 to 8 maximum]

---

## Post-Production Seeds
Flag these moments for `workflows/thread-post.md` — do not live tweet:

- [Timestamp] — [What happened and why it belongs in post-production, not live]
- [Timestamp] — [Same]
```

---

## Quality Gates

Before delivering live tweet drafts:
- [ ] Every tweet has speaker attribution
- [ ] Present tense throughout
- [ ] No editorial conclusion drawn from the moment
- [ ] Each tweet is one moment — not a summary of a segment
- [ ] Timestamp included as internal reference
- [ ] Total tweet count is 5–8 maximum — if over, cut the weakest ones
- [ ] Post-production seeds are flagged separately
