#!/usr/bin/env python3
"""
Top-volume Polymarket leaderboards — 24h / 7d / 30d — rendered as a matrix of
glass transparency x background, to sample the look across the brand fields.

Data: Polymarket Gamma events, ordered by volume24hr / volume1wk / volume1mo,
pulled 2026-06-08. Each card is the leaderboard layout on the liquid-glass panel.

Outputs -> episode-01/exports-markets/
  pm-<window>--<bg>.png            (background sweep, fixed tint 0.72)
  pm-30d--glass-<tint>.png         (transparency sweep, fixed team-gradient bg)

Run:  python3 episode-01/_markets.py
"""
import os, sys, importlib.util, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
LIB, DV = os.path.join(ROOT, "lib"), os.path.join(ROOT, "data-viz")
OUT = os.path.join(HERE, "exports-markets"); os.makedirs(OUT, exist_ok=True)
sys.path.insert(0, LIB)
import pmn

TINT = 0.72   # reassigned by the transparency sweep below


def glass_overlay(x, y, w, h, rx):
    x, y, w, h, rx = float(x), float(y), float(w), float(h), float(rx)
    u = f"gx{int(x)}y{int(y)}w{int(w)}"
    return (
        f'<linearGradient id="{u}s" x1="{x}" y1="{y}" x2="{x + w*0.55}" y2="{y + h*0.85}" gradientUnits="userSpaceOnUse">'
        f'<stop offset="0" stop-color="#EAF1FF" stop-opacity="0.16"/>'
        f'<stop offset="0.12" stop-color="#EAF1FF" stop-opacity="0.05"/>'
        f'<stop offset="0.40" stop-color="#EAF1FF" stop-opacity="0"/></linearGradient>'
        f'<radialGradient id="{u}h" gradientUnits="userSpaceOnUse" cx="{x + w*0.16}" cy="{y - h*0.04}" r="{max(w,h)*0.55}">'
        f'<stop offset="0" stop-color="#FFFFFF" stop-opacity="0.16"/>'
        f'<stop offset="0.5" stop-color="#FFFFFF" stop-opacity="0"/></radialGradient>'
        f'<linearGradient id="{u}r" x1="0" y1="{y}" x2="0" y2="{y + h}" gradientUnits="userSpaceOnUse">'
        f'<stop offset="0" stop-color="#FFFFFF" stop-opacity="0.55"/>'
        f'<stop offset="0.18" stop-color="#FFFFFF" stop-opacity="0.12"/>'
        f'<stop offset="1" stop-color="#FFFFFF" stop-opacity="0.03"/></linearGradient>'
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="url(#{u}s)"/>'
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="url(#{u}h)"/>'
        f'<rect x="{x + 0.75}" y="{y + 0.75}" width="{w - 1.5}" height="{h - 1.5}" '
        f'rx="{max(rx - 1, 0)}" fill="none" stroke="url(#{u}r)" stroke-width="1.5"/>'
    )


def _glass_panel_body(x, y, w, h, rx, base, tex):
    out = (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" '
           f'fill="{base}" fill-opacity="{TINT}" filter="url(#soft)"/>')
    u = f"pw{int(x)}{int(y)}"
    cx, cy, r = x + w*0.5, y + h*0.02, max(w, h)*0.98
    out += (f'<radialGradient id="{u}" gradientUnits="userSpaceOnUse" cx="{cx:.0f}" cy="{cy:.0f}" r="{r:.0f}">'
            f'<stop offset="0" stop-color="#15397D" stop-opacity="0.32"/>'
            f'<stop offset="0.82" stop-color="#06080F" stop-opacity="0"/></radialGradient>'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="url(#{u})"/>')
    return out + glass_overlay(x, y, w, h, rx)


pmn._panel_body = _glass_panel_body

sys.path.insert(0, DV)
import _build as dv          # noqa: E402
import _more as more         # noqa: E402

S = 1080
SRC = "Polymarket · Jun 8, 2026"

WINDOWS = {
    "24h": {"tag": "Top markets · last 24h", "q": ["Where the volume", "is right now"],
            "rows": [("World Cup winner", 44.3, "$44.3M"),
                     ("Iran closes airspace", 9.2, "$9.2M"),
                     ("US–Iran peace deal", 6.4, "$6.4M"),
                     ("Peru election winner", 4.7, "$4.7M"),
                     ("Fed decision in June", 3.4, "$3.4M")]},
    "7d":  {"tag": "Top markets · last 7 days", "q": ["Where the volume", "went this week"],
            "rows": [("World Cup winner", 286.9, "$286.9M"),
                     ("US–Iran peace deal", 30.3, "$30.3M"),
                     ("Stranger Things drop", 19.3, "$19.3M"),
                     ("Fed decision in June", 18.4, "$18.4M"),
                     ("Australian Open winner", 15.9, "$15.9M")]},
    "30d": {"tag": "Top markets · last 30 days", "q": ["Where the volume", "went this month"],
            "rows": [("World Cup winner", 784.4, "$784.4M"),
                     ("US–Iran peace deal", 61.0, "$61.0M"),
                     ("Dem nominee 2028", 59.5, "$59.5M"),
                     ("Fed decision in June", 50.3, "$50.3M"),
                     ("US president 2028", 47.0, "$47.0M")]},
}


def render(window, bg, fname):
    m = WINDOWS[window]
    pmn.set_background(bg)
    svg = dv.card_shell(S, S, m["tag"], m["q"],
                        lambda x, y, pw, ww: more.leaderboard_panel(x, y, pw, ww, m["rows"]),
                        hs_ratio=0.050, source=SRC)
    base = os.path.join(OUT, fname)
    open(base + ".svg", "w").write(svg)
    subprocess.run(["rsvg-convert", "-o", base + ".png", base + ".svg"], check=True)
    print("   ", fname)


n = 0
# ── A) background sweep — every window across all 4 brand fields (tint 0.72) ──
TINT = 0.72
for win in ("24h", "7d", "30d"):
    for bg in ("house", "team-gradient", "team-solid", "team-glow"):
        render(win, bg, f"pm-{win}--{bg}"); n += 1

# ── B) transparency sweep — the 30d board on team-gradient at 4 tints ─────────
for t in (0.50, 0.65, 0.80, 0.92):
    TINT = t
    render("30d", "team-gradient", f"pm-30d--glass-{int(t*100)}"); n += 1

pmn.set_background("house")
print(f"\nwrote {n} market cards -> {os.path.relpath(OUT, ROOT)}/")
