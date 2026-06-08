# Broadcast frames (static)

On-air video frames for the PMN show (1920×1080), from Design Draft 1:

- `Single-Cam Frame.png` — solo host, lower-third name chip
- `Two-Cam Frame.png` — host + guest
- `Four-Cam Frame.png` — host / co-host / two guests, each with a lower-third
- `Market Overlay + 2 cams.png` — Polymarket market card + two camera feeds

**These are static design exports, not code-generated** (unlike the cards,
covers, and podcast covers, which have Python generators). They carry The Block +
Polymarket chrome and the **lower-third name chips** (HOST / CO-HOST / GUEST) —
the lower-thirds are baked into each frame, there are no standalone lower-third
files.

If you want code-generated, per-episode frames or standalone transparent
lower-thirds, `lib/pmn.py` already has the building blocks — `chrome()` and
`name_chip(x, y, role, name, line2, line3)` (the broadcast lower-third) — so a
frame generator can be built the same way as `_podcast_covers.py`.
