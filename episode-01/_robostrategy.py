#!/usr/bin/env python3
"""
Episode 01 — RoboStrategy (guest: Kevin McCordic, f.k.a. intern · CMO).

Builds a post-ready card set on the brand team-gradient field with the liquid-
glass panel treatment. Reuses the four glass layouts (episode / binary / gauge /
leaderboard) where they fit the data, and adds one NEW layout — the funding
"deals down, dollars up" divergence — that none of the stock templates express.

All data verified 2026-06-08:
  - Optimus odds ............. Polymarket  (Yes 1.2% -> 1/99)
  - Best AI model, end of June Polymarket  (Anthropic 85 / Google 11 / OpenAI 4)
  - AI & hardware perps ...... Hyperliquid HIP-3 'xyz' dex (Trade.xyz), 24h ntl
  - Crypto VC funding ........ The Block   (deals -59% YoY, dollars +37% YoY)

Run:  python3 episode-01/_robostrategy.py
"""
import os, sys, importlib.util, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
LIB, DV, SOC = (os.path.join(ROOT, d) for d in ("lib", "data-viz", "social"))
OUT = os.path.join(HERE, "exports-robostrategy"); os.makedirs(OUT, exist_ok=True)
sys.path.insert(0, LIB)
import pmn
import pmn_live          # live-data adapter (pull -> dict, with cached fallback)

TINT = 0.72   # see-through glass tint (panel reads the team-gradient through it)


# ── liquid-glass panel (same surface as the _glass-test matrix) ──────────────
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


pmn._panel_body = _glass_panel_body    # every dark panel is now glassy


# ── load the real builders (data-viz first so _more can import _build) ───────
sys.path.insert(0, DV)
import _build as dv          # noqa: E402
import _more as more         # noqa: E402

def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec); sys.modules[name] = mod
    spec.loader.exec_module(mod); return mod

soc = _load("soc_build", os.path.join(SOC, "_build.py"))

# shorthands pulled from the data-viz module (mode-aware, brand-correct)
C, F = pmn.C, pmn.F
M, PADIN, ty = dv.M, dv.PADIN, dv.ty
eyebrow, headline, body = pmn.eyebrow, pmn.headline, pmn.body
INK, MUTE, UP, DOWN = dv.INK, dv.MUTE, dv.UP, dv.DOWN


# ── NEW LAYOUT: divergence — two stats moving opposite directions ────────────
def card_divergence(w, h, d):
    """Two side-by-side stat panels telling a 'this fell / that rose' story.
    d = {tag, title[], left{label,arrow,stat,from,to,color}, right{...},
         caption, source}."""
    m = M(w); pin = PADIN(w)
    out = [pmn.svg_open(w, h, "PMN divergence"), pmn.defs(w, h), dv._bg(w, h), dv.chrome(w, h)]

    # headline block (top, left-aligned like the data cards)
    ebs = ty(w, "eyebrow"); hs = round(w * 0.066)
    top = round(h * 0.155)
    out += [eyebrow(m, top + ebs, d["tag"], size=ebs, color=dv.THEME["eyebrow"])]
    ty0 = top + ebs + round(hs * 1.15)
    out += [headline(m, ty0, d["title"], size=hs, weight=800, color=dv.THEME["title"])]

    # two glass panels, side by side
    gap = round(w * 0.035)
    pw = (w - 2*m - gap) / 2
    py = round(h * 0.420); gh = round(h * 0.280)
    for i, side in enumerate((d["left"], d["right"])):
        px = m + i * (pw + gap)
        out += [dv.panel(px, py, pw, gh, w)]
        cx = px + pw/2
        # metric label
        out += [eyebrow(cx, py + pin + round(ebs*0.5), side["label"],
                        size=ebs, color=C.eyebrow_ink, anchor="middle")]
        # big signed stat (arrow + pct), semantic colour
        ssz = round(w * 0.105)
        out += [f'<text x="{cx}" y="{py + gh*0.555:.0f}" text-anchor="middle" '
                f'font-family="{F.sans}" font-size="{ssz}" font-weight="800" '
                f'letter-spacing="-1.5" fill="{side["color"]}">{side["arrow"]} {side["stat"]}</text>']
        # from -> to line
        fsz = round(w * 0.034)
        out += [body(cx, py + gh - pin - round(fsz*1.35),
                     f'{side["from"]}  →  {side["to"]}',
                     size=fsz, weight=700, color=INK, anchor="middle")]
        out += [body(cx, py + gh - pin + round(fsz*0.1), side["sub"],
                     size=round(ty(w,"caption")*0.92), weight=600, color=MUTE, anchor="middle")]

    # takeaway under the panels (wrapped to the content width)
    if d.get("caption"):
        csz = round(ty(w, "lead") * 0.92)
        clines = pmn.wrap(d["caption"], csz, w - 2*m)
        cy0 = py + gh + round(h*0.060)
        for j, ln in enumerate(clines):
            out += [body(m, cy0 + j*round(csz*1.22), ln, size=csz, weight=600, color=INK)]

    # source (bottom-right) + [PMN] footer (bottom-left)
    out += [body(w-m, h-m-round(ty(w,"caption")*0.1), f'Source: {d["source"]}',
                 size=ty(w,"caption"), weight=600, color=dv._src_color(), anchor="end")]
    out += [dv.footer(w, h), pmn.svg_close()]
    return "".join(out)


# ── EPISODE DATA ─────────────────────────────────────────────────────────────
S = 1080

EP = {"num": "01", "date": "RoboStrategy", "title": ["Crypto's capital", "left for robots"],
      "guest": "Kevin McCordic", "guest_title": "CMO · f.k.a. intern", "company": "RoboStrategy"}

OPTIMUS = {"tag": "Live odds · Polymarket",
           "question": ["Tesla ships a consumer", "Optimus by June 30?"],
           "yes": 1, "no": 99, "src": "Polymarket"}

FUNDING_GAUGE = {"tag": "The setup · The Block", "q": ["Crypto VC dealmaking,", "year over year"]}

PERPS = [("Micron (MU)", 102.6, "$102.6M"), ("Nvidia (NVDA)", 29.3, "$29.3M"),
         ("SpaceX (SPCX)", 21.6, "$21.6M"), ("AMD", 12.4, "$12.4M"),
         ("Tesla (TSLA)", 8.2, "$8.2M")]
PERPS_META = {"tag": "AI + hardware perps · 24h volume",
              "q": ["Where crypto-native", "risk went"]}
# ── live refresh (opt-in): re-pull the curated board from Hyperliquid; the
#    committed PERPS above is the cached fallback if the pull fails ───────────
PERPS, PERPS_SRC = pmn_live.perps_leaderboard(pmn_live.PERPS_TICKERS, fallback=PERPS)

AIMODEL = {"tag": "Top AI model · end of June", "question": ["Who leads the", "model race?"],
           "outcomes": [("Anthropic", 85), ("Google", 11), ("OpenAI", 4)], "src": "Polymarket"}

DIVERGE = {"tag": "Crypto VC · 2024 → 2025", "title": ["Deals down.", "Dollars up."],
           "left":  {"label": "Deal count", "arrow": "▼", "stat": "59%",
                     "from": "2,900", "to": "1,200", "sub": "rounds per year", "color": DOWN},
           "right": {"label": "Capital raised", "arrow": "▲", "stat": "37%",
                     "from": "$13.8B", "to": "$18.9B", "sub": "total deployed", "color": UP},
           "caption": "Fewer rounds, bigger checks. May 2026: ~50 deals, a 5-year low.",
           "source": "The Block"}


# ── RENDER ───────────────────────────────────────────────────────────────────
pmn.set_background("team-gradient")

jobs = [
    ("01-cover",            lambda: soc.episode_card(S, S, EP)),
    ("02-optimus-binary",   lambda: dv.card_binary(S, S, OPTIMUS)),
    ("03-funding-gauge",    lambda: more.C_(FUNDING_GAUGE["tag"], FUNDING_GAUGE["q"],
                                            lambda m: lambda x,y,pw,ww: more.gauge_panel(
                                                x, y, pw, ww, 59, "fewer deals than 2024",
                                                color=DOWN), src="The Block")(S, S, FUNDING_GAUGE)),
    ("04-perps-leaderboard",lambda: dv.card_shell(S, S, PERPS_META["tag"], PERPS_META["q"],
                                                  lambda x,y,pw,ww: more.leaderboard_panel(x,y,pw,ww,PERPS),
                                                  hs_ratio=0.050, source=PERPS_SRC)),
    ("05-aimodel-multi",    lambda: dv.card_multi(S, S, AIMODEL)),
    ("06-funding-divergence",lambda: card_divergence(S, S, DIVERGE)),
]

n = 0
for name, thunk in jobs:
    try:
        svg = thunk()
        base = os.path.join(OUT, name)
        open(base + ".svg", "w").write(svg)
        subprocess.run(["rsvg-convert", "-o", base + ".png", base + ".svg"], check=True)
        n += 1
        print("   ", name)
    except Exception as e:
        print("   !! skipped", name, "->", repr(e)[:160])

pmn.set_background("house")
print(f"\nwrote {n}/{len(jobs)} RoboStrategy cards -> {os.path.relpath(OUT, ROOT)}/")
