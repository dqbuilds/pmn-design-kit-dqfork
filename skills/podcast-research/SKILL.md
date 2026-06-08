---
name: podcast-research
description: >
  Use this skill whenever preparing research for a podcast, interview, or panel
  discussion. Triggers include: "research for my podcast", "fact-check these
  talking points", "find data on X for my episode", "pull sources on", "prep me
  for this guest", or any request involving episode prep, guest research, or
  claim verification. Prioritizes crypto-native publications and primary sources
  over aggregators.
allowed-tools: Read, WebSearch, Bash
---

# Podcast Research — Coordinator

## Source Tier Summary

- **Tier 1** — Crypto-native news outlets (The Block, CoinDesk, Blockworks, etc.)
- **Tier 2** — Primary sources: on-chain data, gov filings, protocol docs, the Cermak textbook
- **Tier 3** — Traditional financial media (Bloomberg, WSJ) for macro context only
- **Tier 4** — Aggregators and secondary sources — use sparingly, always flag

Full outlet details and use-case guidance: `sources/tier1-outlets.md`
Full Tier 2 platform index and textbook chapter map: `sources/tier2-primary.md`

---

## Grill-Me Brief Input

If the request includes a completed Grill-Me Brief (Episode or Content Strategy),
treat it as a resolved framing layer and skip any steps it already answers.

| Brief field | Replaces this step |
|---|---|
| Central tension | The episode framing question in segment-brief.md |
| Guest's unique value | The primary research focus in guest-diligence.md |
| Audience prior belief to challenge | The counternarrative identification step in counternarrative-flags.md |
| Must-cover topics (ranked) | Topic scoping in segment-brief.md |
| Anchor question | The starting point for question-craft.md — score it via harmonic mean and build around it |
| Data to pull pre-recording | The pull list for data-pull.md and data-snapshot.md |
| Pre-drop thread angle | The hook for thread-pre.md |

Do not re-derive decisions the brief has already resolved. Start from the brief
and run only the steps it leaves open.

---

## Output Mode Confirmation

Before generating any output, state:
1. Which workflow is active
2. What format will be produced (brief / questions / thread / data pull / content plan)

This prevents generating a thread when a brief was needed, or questions when
research was the ask. If the request is ambiguous, ask before loading files.

---

## Routing Logic

Read the request type, load the appropriate workflow file, then execute it fully.

| Request Type | Load These Files |
|---|---|
| "Fact-check these talking points" | `workflows/fact-check.md` + `sources/tier1-outlets.md` |
| "Research this topic for my episode" | `workflows/segment-brief.md` + `sources/tier1-outlets.md` + `sources/tier2-primary.md` |
| "Prep me for this guest" or "Who is X" | `workflows/guest-diligence.md` + `briefs/GUEST-ARCHETYPES.md` + `sources/tier2-primary.md` + `context/question-craft.md` |
| "Give me data on X" | `workflows/data-pull.md` + `sources/tier2-primary.md` |
| "Write a pre-interview thread" or "pre-thread" | `workflows/thread-pre.md` + `style/voice-base.md` + `style/voice-analysts.md` + `style/examples.md` |
| "Write a post-interview thread" or "post-thread" | `workflows/thread-post.md` + `style/voice-base.md` + `style/voice-analysts.md` + `style/examples.md` |
| "Take a data snapshot" or "pull metrics before the interview" | `workflows/data-snapshot.md` + `workflows/data-pull.md` + `sources/tier2-primary.md` |
| "Write questions for my guest" or "help me prep questions" | `context/question-craft.md` + `workflows/guest-diligence.md` + `briefs/GUEST-ARCHETYPES.md` |
| "What should I write" or "content plan" or "what to post" or "give me a publishing calendar" | `workflows/content-plan.md` + `content-plans/CONTENT-PLAN-ARCHETYPES.md` + `style/voice-base.md` |
| "Write a tweet about" or "write a standalone post" (data-driven) | `style/voice-base.md` + `style/voice-data.md` + `style/examples.md` |
| "Write a tweet about" or "write a standalone post" (narrative) | `style/voice-base.md` + `style/examples.md` |
| "Write an X article" or "short article" or "write for X" | `workflows/article-writer.md` + `workflows/fact-check.md` + `workflows/data-pull.md` + `context/counternarrative-flags.md` + `style/voice-base.md` + `style/voice-analysts.md` + `style/voice-data.md` |
| "Write a Substack" or "long-form piece" or "write a newsletter" or "write an article" | `workflows/article-writer.md` + `workflows/fact-check.md` + `workflows/data-pull.md` + `context/counternarrative-flags.md` + `style/voice-base.md` + `style/voice-analysts.md` + `style/voice-data.md` |
| "Write a video script" or "short video" or "reel" or "tiktok" or "youtube short" or "60 second script" or "45 second script" or "2 minute video" | `workflows/video-script.md` + `workflows/segment-brief.md` + `sources/tier1-outlets.md` + `style/voice-base.md` + `context/counternarrative-flags.md` |
| "Live tweet this episode" or "tweet during recording" or "live stream" or "Twitter Spaces" or "X Spaces" | `workflows/live-tweet.md` + `style/voice-base.md` |
| Any episode with metric-driven topic | Also load `workflows/data-snapshot.md` + `style/voice-data.md` alongside primary workflow |
| Any ambiguous or multi-part request | State output mode and confirm before proceeding |

### Live Stream Episodes — Special Handling

When the episode format is a live stream (X Spaces, Twitter Spaces, Twitch, YouTube Live):

- **Quotables are restricted to two uses only:** live tweeting during the recording, and post-production threads/clips after the episode ends.
- Do NOT generate pre-drop threads that quote the guest — the conversation hasn't happened yet.
- Do NOT generate post-drop threads that present themselves as "key takeaways" until the recording is confirmed done and reviewed.
- Live tweet drafts must include a timestamp reference so they can be matched to the recording for post-production use.
- Post-production content from a live stream follows the same workflows as a studio episode.

For every request involving technical crypto topics, also load:
`context/counternarrative-flags.md` — to surface known contested narratives before delivering output.

For any request where a technical term needs on-air definition, load:
`context/glossary.md` — canonical definitions for on-air use.

---

## Universal Rules

- Always prefer higher-tier sources. Only fall back when higher tiers don't cover the topic.
- Date every source. Flag anything older than 90 days on fast-moving topics.
- For on-chain data, always include the query timestamp.
- Never cite Tier 4 as sole support for any factual claim.
- Never fabricate citations. If paywalled, say so and seek corroboration.

## On-Chain Data — DeFi Llama Corroboration Rule

For any on-chain claim — TVL, protocol revenue, stablecoin supply, bridge flows, solver/intent inventory, fees, chain activity, DEX volume — **DeFi Llama (defillama.com, api.llama.fi) is the default corroboration source.** It is one of the most trusted public on-chain data sources, and any fact-check or data pull involving on-chain metrics should actively attempt to corroborate against it.

**Always ask before pulling.** Free-API rate limits and frontend-scraping behavior are not assumed safe. Before issuing any request:

1. State the exact endpoint or page you intend to hit (e.g. `https://api.llama.fi/protocol/uniswap`, or a specific dashboard URL).
2. State the specific question the pull will answer and how it connects to the claim.
3. Wait for explicit approval. Do not bundle the request inside another tool call.

Be very explicit. A user shouldn't have to infer that a DeFi Llama call is about to happen.
