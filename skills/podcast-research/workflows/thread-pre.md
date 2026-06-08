# Workflow — Thread (Pre-Interview)

Use this workflow when writing a thread to publish *before* the episode drops.
Goal: frame why this guest matters right now, prime the audience's curiosity,
and drive listens.

Load `style/voice.md` and `style/examples.md` before writing anything.

---

## Inputs Required

- Guest name, title, company
- Episode topic(s) / hook angle
- Record date or episode drop date
- Output from `workflows/guest-diligence.md` (if already run)
- Data snapshot from `workflows/data-snapshot.md` (if topic is metric-driven)

---

## Step-by-Step Protocol

### Step 1 — Identify the Hook Angle
The hook angle is the single most interesting thing about this guest or topic
right now. Not their biography — the *current tension* or *timely development*.

Ask: What would make someone who's already heard of this person want to listen?

Candidates:
- A counter-narrative about their project ("overnight success" vs. long road)
- A recent product launch, upgrade, or announcement
- A position they hold that others dispute
- A mechanism they've built that most people misunderstand

Avoid: Generic framing like "I'm interviewing [X] who is a leader in [Y]."

### Step 2 — Pull Supporting Data (if applicable)
If the episode is about a protocol, asset, or market structure topic, run
`workflows/data-snapshot.md` before writing. This data is the "why now" fuel.

Metrics most useful for pre-interview threads:
- TVL / protocol fees / revenue (DefiLlama, Token Terminal)
- Open interest, funding rates (for perp DEX guests)
- Volume trends (Artemis, DefiLlama)
- Market cap, circulating supply (for token-focused discussions)
- Utilization rates, interest rates (for lending protocol guests)

The pre-interview thread uses this data to establish stakes — not to show off
the numbers. One or two data points max; the rest is narrative.

### Step 3 — Check Counternarrative Flags
Load `context/counternarrative-flags.md`. If the guest's domain or project
appears, identify the contested narrative. This often becomes the most
interesting tweet (tweet 2 or 3) — the thing that complicates the obvious read.

### Step 4 — Write the Thread

**Standard structure (6 tweets for guest-focused; 8–11 for analysis-heavy):**

```
[1/N] Hook — the current tension + what this episode will answer.
      Include embedded media link or retweet if available.

[2/N] Why this person/topic is interesting RIGHT NOW.
      Lead with the counternarrative or the surprising data point.

[3/N] First substantive framing point — what the guest has built, argued,
      or revealed that the audience should understand before listening.

[4/N] Second framing point — mechanism, market context, or key debate.

[5/N] A question this episode will explore. Frame it genuinely — not
      rhetorically. Something you actually want to know the answer to.

[6/N] CTA. Warm, personal. Tease what kind of conversation this will be.
      Link to episode or "dropping soon."
```

For analysis threads without a specific guest (Example C pattern):
Follow the 8–11 tweet structure from `style/examples.md`.

### Step 5 — Apply Voice Rules
Run through `style/voice.md` checklist:
- [ ] [N/Total] numbering on every tweet
- [ ] No hashtags
- [ ] No emojis
- [ ] Opinions labeled with (opinion)
- [ ] One idea per tweet
- [ ] Data has context immediately following the number
- [ ] Hook does not lead with price or generic praise

---

## Output Format

Deliver as plain numbered tweets, ready to copy-paste. No surrounding commentary.
Annotate inline only if the user requests explanation.

```
[1/6] ...

[2/6] ...

[3/6] ...

[4/6] ...

[5/6] ...

[6/6] ...
```

If data snapshot was used, append below the thread:

```
---
Data pulled: [Date]
Sources: [Platform — metric — value]
```
