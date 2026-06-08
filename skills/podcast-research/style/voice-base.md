# Voice Rules — Base (@imyoungsparks Thread Style)

Derived from real threads. These rules govern ALL thread output.
Load this file for every thread or content request.

Before returning any thread output, apply the AI Detection Check from
`~/.claude/CLAUDE.md` — the same rules that govern tweet output apply here.

---

## Format Rules (Non-Negotiable)

**Numbering:** Every tweet uses [N/Total] at the start. No exceptions.
- Determine total count before writing. Standard length: 6 tweets.
- Longer threads (8–11) only for technically dense pre-interview topics.

**No hashtags.** None. Not in the hook, not in the close.

**No emojis** unless the source material contains them (e.g., quoting another tweet).

**No hype language.** Never: "🔥", "alpha", "LFG", "massive", "insane", "huge".
Use specific, substantive adjectives instead.

**Character limit awareness:** Each tweet must fit within 280 characters.
When in doubt, break into a new tweet rather than compress.

---

## Structural Patterns

### Post-Interview Thread (6 tweets standard)

| Tweet | Purpose |
|---|---|
| 1/6 | Hook: frame the guest's significance + embed media link or retweet |
| 2/6 | Partner acknowledgment OR the episode's central tension/thesis |
| 3/6 | First substantive takeaway — what the guest explained/outlined |
| 4/6 | Second takeaway — often a mechanism or product detail |
| 5/6 | Third takeaway — usually a surprising admission, counter-take, or human moment |
| 6/6 | Personal reflection + CTA close |

### Pre-Interview / Analysis Thread (8–11 tweets)

| Tweet | Purpose |
|---|---|
| 1/N | Hook: surface a surprising fact, new development, or retweet of source material |
| 2/N | Why this matters — bridge from the news to the broader implication |
| 3–8/N | One idea per tweet, building a logical chain. Label opinions explicitly. |
| 9–10/N | Forward-looking speculation — "if I were building X..." or "this could enable..." |
| 11/N (if used) | Summary of the thesis + open question |

---

## Voice Characteristics

**Warm and generous.** You express genuine admiration for guests. Use phrases like:
- "I was often left in awe by..."
- "He was such a great guest..."
- "Alex had many extremely profound takes."

Do not overdo it — one or two warm moments per thread. The rest is substantive.

**Narrator, not reporter.** You are telling the story of a conversation,
not transcribing it. Say "He outlined predecessors like dYdX and GMX and
how they drove innovations in onchain trading" — not "Leonard discussed DEX history."

**Specific over vague.** Name the protocols, name the mechanisms, name the people.
"Hidden order features prevent order hunting" > "privacy features help traders."

**Label opinions.** When expressing your own analysis or speculation (especially
in pre-interview threads), end the tweet with "(opinion)". Example from your threads:
"This breakthrough combined with AI will be very impactful in shaping how
autonomous agents behave (opinion)."

**Quote guests sparingly and purposefully.** When you do quote, use a clean format:
`[Name]: "[Quote]"` — on its own line for emphasis. One quote per thread maximum.

**Line breaks for emphasis.** Use a blank line to separate a key one-liner from
the surrounding context. Example:
```
"We're a nostalgia brand for parents who grew up with Pinkfong." Thomas: Kids sing today, parents sang yesterday.

Generational IP = forever users
```

**Close with warmth + CTA, not hype.** Standard close for post-interview threads:
"I hope you enjoy this interview as much as I did!"
Variations are fine but keep the same energy — personal, inviting, not promotional.

---

## Data Integration Rules

Data appears **inline** with immediate context — not in a separate data section.

Good: "With over 16 BILLION views, Baby Shark Universe chose BNB Chain to bring
Pinkfong's IP to Web3 — family onboarding at scale, a conversation seldom
discussed in crypto."

Bad: "BSU has 16B views. This is bullish for BNB Chain adoption."

**Always contextualize the number.** What does it mean? Why does it matter here?
A raw metric with no frame is not useful in a thread.

For pre-interview threads using on-chain data (TVL, fees, OI, funding rates, etc.):
- State the number and source in the same tweet
- Immediately follow with what changed and why it's relevant
- If comparing pre vs. post: use the snapshot format from `workflows/data-snapshot.md`

For data-heavy tweets, also load `style/voice-data.md`.

---

## Connector Language

Use these phrasings to introduce guest takeaways naturally:
- "He outlined..."
- "He spoke on..."
- "He noted..."
- "He expounded on..."
- "He addressed..."
- "He clarified..."
- "Leonard spoke to..."
- "Thomas unpacked..."

Vary across tweets. Do not use the same connector twice in one thread.

---

## What to Avoid

- Starting a tweet with "In summary" or "Overall" (except final tweet of long analysis threads)
- Bullet points within a tweet — write in prose
- Stacking multiple ideas into one tweet — one idea per tweet, always
- Passive voice framing ("it was noted that...")
- Repeating the guest's name every tweet — use "He" after establishing in tweet 1
- Price targets or market predictions presented as fact
- Collapsing the valuation question into "bullish/bearish" — the honest answer
  is almost always "it depends on what you need to believe" (Santi's frame)
