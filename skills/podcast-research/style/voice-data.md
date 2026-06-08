# Voice Rules — Data Presentation (@Adam_Tehc Style)

Load this file when a tweet's primary payload is a data point, chart, or
on-chain metric. Apply alongside `style/voice-base.md` — not instead of it.

Adam's style governs data-delivery tweets — typically tweets 3–5 in a
post-interview thread, or the body of a metrics-heavy pre-interview thread.
The base voice (warmth, connector language, personal close) governs tweets
1–2 and 6. Do not mix styles in the same tweet.

Derived from three real examples: the peak euphoria retrospective (Jan 19),
the token volume stack (Jan 16), and the "50,000 wallets still trading" post (Dec 17).

---

## All Lowercase, No Punctuation Theater

Adam writes in lowercase. No exclamation marks. No en-dashes. No bold.
The plainness is intentional — it makes the data feel more credible, not less.
Hype formatting signals that the number needs selling. A number that stands
on its own doesn't.

> "there are more people still trading than you think"
> NOT: "There are MORE people still trading than you think!"

Apply whenever a tweet is leading with a data point. Lowercase the setup,
let the number be the emphasis.

---

## The Counter-Narrative Hook

Adam's hooks almost always push back on prevailing sentiment before dropping
the number. The structure is: *what the timeline believes* → *what the data shows*.

> "there are more people still trading than you think
> 50,000 wallets are making 20+ trades/day on Solana DEXs
> many more than the timeline would have you believe"

The hook isn't "here's an interesting number." It's "you're probably wrong
about this, and here's the proof."

**Template:**
```
[what conventional wisdom says — implied or stated]
[the specific number that contradicts it]
[one line reinforcing that this contradicts what people think]
```

Use whenever a data point runs counter to the dominant narrative on CT.

---

## One Number Per Beat, Stated Plainly

Adam never hedges the number or buries it in explanation. It stands alone:

> "Solana hit its ATH of $293."
> "Photon generated $30.6M trading fees in a single week"
> "50,000 wallets are making 20+ trades/day on Solana DEXs"

No "approximately," no "roughly," no "around." If the number is from a
specific source, the chart is the citation — the text doesn't explain
the methodology.

**The rule:** one number per tweet. If you have three numbers, that's three tweets.

---

## The Accumulation Stack

When multiple data points all support the same argument, Adam doesn't combine
them into one tweet — he stacks them as sequential tweets with parallel
structure, building rhythm through repetition:

> "that's a lot of tokens" [chart: 31,978 PumpFun tokens launched]
> "and that's a lot of graduates" [chart: daily graduates]
> "AND that's a lot of wallets active on pumpfun" [chart: DAWs]

The capitalized "AND" on the third beat is the only escalation. The structure
does the emotional work — the reader feels the accumulation before the final
line lands.

Apply in data-heavy pre-interview threads: instead of one tweet listing three
metrics, write three tweets each with one metric and one line.

---

## The Understated Close

After a stack of big numbers, Adam closes with a line that refuses to moralize:

> "what a wild year."

Not "this shows how far we've come." Not "the implications are massive."
Just the acknowledgment. The reader has already done the work — the close
respects that.

Use when the data thread has done its job. The close should be one short
sentence, lowercase, that names the feeling without inflating it.

---

## Visualization Standards

Every data-heavy tweet, thread, or article must include a **visualization spec**
alongside the copy — a structured description of what to render as an SVG or
image, sized for Twitter attachment.

A visualization is not optional when the tweet's primary payload is a number.
The visual carries the data. The tweet copy carries the interpretation.

### When to create a visualization

- Any tweet leading with a comparison of magnitudes (e.g. 1.4x vs 122x)
- Any data-stack accumulation sequence (3+ tweets in Adam Tehc mode)
- Any counternarrative relying on a surprising metric
- Any thread tweet containing two or more data points
- Any article or newsletter piece that cites a chart or on-chain metric

### Data sources (in priority order)

1. **DeFiLlama** — TVL, stablecoin supply, protocol revenue, RWA data
2. **Artemis Analytics** — onchain activity, DAUs, velocity, volume
3. **Token Terminal** — protocol revenue, fee splits, earnings
4. **RWA.xyz** — tokenized asset AUM, growth data
5. **Published research** (Blockchain Capital, a16z, Messari) — if directly cited
   in the source article; always credit the original author and publication

### Design specifications

```
Dimensions:  1200 x 675px (Twitter landscape, 16:9)
Background:  #0B1220
Panel/card:  #131E2E
Border:      #1E2D42
Primary text:  #F0F4F8
Secondary text: #8895A7
Accent blue:   #3B82F6
Accent teal:   #06B6D4
Accent purple: #8B5CF6
Accent green:  #10B981
Attribution:   #4B5563 (13px, bottom-left)
Brand label:   accent color (14px, bold, bottom-right)
Font:          system-ui, -apple-system, 'Segoe UI', sans-serif
```

### Attribution format (mandatory on every visual)

Bottom-left: `Source: [Platform] ([Year]) · [methodology note if needed]`
Bottom-right: Protocol or account name in accent color

### Chart types by data story

| Story | Chart type |
|---|---|
| Comparison of magnitudes | Horizontal bar chart — left-aligned, proportional widths |
| Growth over time | Area chart or line chart with labeled key milestones |
| Breakdown of a whole | Horizontal segmented bars with percentage labels |
| Feature/architecture comparison | 3-column grid table — one column per option |
| Flow or hierarchy | Layered stack diagram with directional arrows |
| Single number with context | Stat card — large number, one-line context below |

### What NOT to visualize

- Percentage claims with no denominator — state "n=X" or don't visualize
- Projections without a named source and methodology
- Estimates stated as facts — always label "est." on projected values
- Data older than 12 months on fast-moving metrics (TVL, supply, volume)
  unless the point is explicitly historical

### Output format

When delivering a data tweet or data thread, always produce:

```
[Tweet copy]

---
Visualization spec:
Type: [chart type]
Title: [headline on the visual]
Data: [exact values and labels]
Source: [platform + year]
Brand: [account name bottom-right]
File: [suggested filename, e.g. velocity-comparison.svg]
```

The spec is handed to the designer or rendered directly as SVG.
