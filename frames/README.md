# Broadcast frames + lower-thirds (static SVG)

On-air video assets for the PMN show (1920×1080), from Design Draft 1. **Vector
SVG is the source of truth; a `.png` preview sits next to each** (regenerate with
`rsvg-convert <file>.svg -o <file>.png`).

## Frames (`frames/`)
- `Single-Cam Frame.svg` — solo host
- `Two-Cam Frame.svg` — host + guest
- `Three-cam Frame.svg` — host + two
- `Four-Cam Frame.svg` — host / co-host / two guests
- `Market Overlay + 2 cams.svg`, `+ 3 cams`, `+ 4 cams` — Polymarket market card + cam feeds

Each carries The Block + Polymarket chrome and the lower-third name chips.
(Camera wells use watermarked stock as placeholders — swap for live feeds.)

## Lower-thirds (`frames/lower-thirds/`)
Standalone name-chip overlays (blue plate + black role tab):
- `lower-third-host.svg` / `lower-third-host-full.svg` — HOST (1-line / 3-line)
- `lower-third-cohost.svg` / `lower-third-cohost-full.svg` — CO-HOST
- `lower-third-guest-full.svg` — GUEST (name / title / company)
- `lower-third-guest-1..4.svg` — GUEST 1–4 (compact)

## Note
These are **static design exports, not code-generated**. `lib/pmn.py` has the
building blocks (`chrome()`, `name_chip(role, name, line2, line3)`) if you want a
parameterized frame / lower-third generator later.
