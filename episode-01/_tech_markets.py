#!/usr/bin/env python3
"""
RoboStrategy episode — bespoke visuals for the TECHNOLOGY prediction markets that
drive the episode. Each market gets its own layout within the PMN design system
(no two repeat), copy informed by current events (June 2026):

  1. SpaceX IPO     -> implied-valuation CURVE   (P(cap > X) declining; ~$1.75T
                       rumored June debut, crowd prices it above the tag, ~$2.1T)
  2. AI model race  -> DOMINANCE card            (Anthropic 85% after Opus 4.8)
  3. Tesla Optimus  -> HYPE vs ODDS contrast     (market 1% vs the trillion-$ hype)

Data: Polymarket Gamma, pulled 2026-06-08.
Renders a clean primary plus background + glass-transparency variants.
Output -> episode-01/exports-tech/
Run:  python3 episode-01/_tech_markets.py
"""
import os, sys, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
LIB, DV = os.path.join(ROOT, "lib"), os.path.join(ROOT, "data-viz")
OUT = os.path.join(HERE, "exports-tech"); os.makedirs(OUT, exist_ok=True)
sys.path.insert(0, LIB)
import pmn

TINT = 0.74   # reassigned by the glass sweep


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

C, F = pmn.C, pmn.F
M, PADIN, ty = dv.M, dv.PADIN, dv.ty
eyebrow, headline, body = pmn.eyebrow, pmn.headline, pmn.body
INK, MUTE, UP, DOWN = dv.INK, dv.MUTE, dv.UP, dv.DOWN
BLUE, GOLD = C.blue, C.gold
S = 1080

# ── one shared vertical rhythm so every card has the same generous margins ────
# Budgeted so a 2-line caption clears the [PMN] footer band (top ≈ 0.904·h).
TOP   = 0.115   # eyebrow top
HS    = 0.060   # headline size ratio
PY    = 0.343   # panel top
GH    = 0.415   # panel height  (bottom ≈ 0.758·h)
CAPG  = 0.045   # gap panel -> caption
CSZ   = 0.038   # caption size ratio


def _head(out, w, h, tag, title):
    ebs = ty(w, "eyebrow"); hsz = round(w * HS); t = round(h * TOP)
    out += [eyebrow(M(w), t + ebs, tag, size=ebs, color=dv.THEME["eyebrow"])]
    out += [headline(M(w), t + ebs + round(hsz*1.15), title, size=hsz, weight=800, color=dv.THEME["title"])]


def _caption(out, w, h, text):
    py, gh = round(h*PY), round(h*GH)
    csz = round(w * CSZ)
    for j, ln in enumerate(pmn.wrap(text, csz, w - 2*M(w))):
        out += [body(M(w), py + gh + round(h*CAPG) + round(csz*0.85) + j*round(csz*1.24), ln,
                     size=csz, weight=600, color=INK)]


def _foot(out, w, h, src):
    out += [body(w-M(w), h-M(w)-round(ty(w,"caption")*0.1), f"Source: {src}",
                 size=round(ty(w,"caption")*0.92), weight=600, color=dv._src_color(), anchor="end")]
    out += [dv.footer(w, h), pmn.svg_close()]


# ── 1) SpaceX IPO — implied-valuation CURVE ──────────────────────────────────
def card_curve(w, h, d):
    m, pin = M(w), PADIN(w)
    out = [pmn.svg_open(w, h, "PMN valuation curve"), pmn.defs(w, h), dv._bg(w, h), dv.chrome(w, h)]
    _head(out, w, h, d["tag"], d["title"])
    px, py = m, round(h*PY); pw = w-2*m; gh = round(h*GH)
    out += [dv.panel(px, py, pw, gh, w)]
    # plot box, generously inset (top headroom for the marker label)
    plx = px+pin+round(w*0.052); ptop = py+pin+round(w*0.058)
    plw = pw-2*pin-round(w*0.052); plh = gh-2*pin-round(w*0.105)
    pts = d["points"]; xmin, xmax = d["xmin"], d["xmax"]
    X = lambda v: plx + plw*(v-xmin)/(xmax-xmin)
    Y = lambda p: ptop + plh*(1-p/100)
    for g in (0, 50, 100):
        gy = Y(g); dash = ' stroke-dasharray="5 6"' if g == 50 else ''
        op = 0.28 if g == 50 else 0.10
        out += [f'<line x1="{plx}" y1="{gy:.0f}" x2="{plx+plw}" y2="{gy:.0f}" '
                f'stroke="{INK}" stroke-opacity="{op}" stroke-width="1.5"{dash}/>']
        out += [body(plx-round(w*0.016), gy+round(ty(w,"caption")*0.34), f"{g}%",
                     size=round(ty(w,"caption")*0.82), weight=600, color=MUTE, anchor="end")]
    poly = " ".join(f"{X(v):.1f},{Y(p):.1f}" for v, p in pts)
    base = f"{X(pts[-1][0]):.1f},{Y(0):.1f} {X(pts[0][0]):.1f},{Y(0):.1f}"
    out += [f'<polygon points="{poly} {base}" fill="{BLUE}" fill-opacity="0.16"/>']
    out += [f'<polyline points="{poly}" fill="none" stroke="{BLUE}" stroke-width="{round(w*0.006)}" '
            f'stroke-linejoin="round" stroke-linecap="round"/>']
    for v, p in pts:
        out += [f'<circle cx="{X(v):.1f}" cy="{Y(p):.1f}" r="{round(w*0.0085)}" fill="{BLUE}" '
                f'stroke="{dv.PANEL}" stroke-width="2"/>']
    for v in d["xlabels"]:
        out += [body(X(v), ptop+plh+round(ty(w,"caption")*1.6), f"${v:g}T",
                     size=round(ty(w,"caption")*0.85), weight=600, color=MUTE, anchor="middle")]
    mk = d["marker"]; mx = X(mk["x"])
    out += [f'<line x1="{mx:.0f}" y1="{ptop}" x2="{mx:.0f}" y2="{ptop+plh}" stroke="{GOLD}" '
            f'stroke-width="2" stroke-dasharray="4 5" stroke-opacity="0.9"/>']
    out += [body(mx, ptop-round(w*0.012), mk["label"], size=round(ty(w,"caption")*0.88),
                 weight=700, color=GOLD, anchor="middle")]
    out += [f'<circle cx="{X(d["crossover"]):.1f}" cy="{Y(50):.1f}" r="{round(w*0.011)}" fill="{GOLD}" '
            f'stroke="{dv.PANEL}" stroke-width="2.5"/>']
    _caption(out, w, h, d["caption"]); _foot(out, w, h, d["source"])
    return "".join(out)


# ── 2) AI model race — DOMINANCE card ────────────────────────────────────────
def card_dominance(w, h, d):
    m, pin = M(w), PADIN(w)
    out = [pmn.svg_open(w, h, "PMN dominance"), pmn.defs(w, h), dv._bg(w, h), dv.chrome(w, h)]
    _head(out, w, h, d["tag"], d["title"])
    px, py = m, round(h*PY); pw = w-2*m; gh = round(h*GH); inner = pw-2*pin
    out += [dv.panel(px, py, pw, gh, w)]
    # leader
    lead = d["leader"]; lnsz = round(w*0.054)
    yy = py + pin + round(lnsz*0.82)
    out += [body(px+pin, yy, lead[0], size=lnsz, weight=800, color=INK)]
    out += [body(px+pw-pin, yy, f'{lead[1]:g}%', size=lnsz, weight=800, color=INK, anchor="end")]
    barh = round(w*0.024); bary = yy + round(lnsz*0.55)
    out += [f'<rect x="{px+pin}" y="{bary}" width="{inner}" height="{barh}" rx="{barh//2}" '
            f'fill="{dv.TRACK}" fill-opacity="0.10"/>']
    out += [f'<rect x="{px+pin}" y="{bary}" width="{round(inner*lead[1]/100)}" height="{barh}" '
            f'rx="{barh//2}" fill="{BLUE}"/>']
    # divider + field
    yy = bary + barh + round(w*0.044)
    out += [f'<line x1="{px+pin}" y1="{yy}" x2="{px+pw-pin}" y2="{yy}" stroke="{INK}" stroke-opacity="0.10" stroke-width="1.5"/>']
    yy += round(w*0.036)
    out += [eyebrow(px+pin, yy, "The field", size=ty(w,"eyebrow"), color=C.eyebrow_ink)]
    fnsz = round(w*0.034); fbar = round(w*0.011); row_h = round(w*0.066)
    yy += round(fnsz*1.02)
    for nm, pct in d["field"]:
        disp = f'{pct:g}%' if pct >= 1 else "<1%"
        out += [body(px+pin, yy, nm, size=fnsz, weight=700, color=INK)]
        out += [body(px+pw-pin, yy, disp, size=fnsz, weight=800, color=INK, anchor="end")]
        bb = yy + round(fnsz*0.42)
        out += [f'<rect x="{px+pin}" y="{bb}" width="{inner}" height="{fbar}" rx="{fbar//2}" '
                f'fill="{dv.TRACK}" fill-opacity="0.10"/>']
        out += [f'<rect x="{px+pin}" y="{bb}" width="{max(round(inner*pct/100), fbar)}" height="{fbar}" '
                f'rx="{fbar//2}" fill="{dv.RANK[1]}"/>']
        yy += row_h
    _caption(out, w, h, d["caption"]); _foot(out, w, h, d["source"])
    return "".join(out)


# ── 3) Tesla Optimus — HYPE vs ODDS contrast ─────────────────────────────────
def card_contrast(w, h, d):
    m, pin = M(w), PADIN(w)
    out = [pmn.svg_open(w, h, "PMN hype vs odds"), pmn.defs(w, h), dv._bg(w, h), dv.chrome(w, h)]
    _head(out, w, h, d["tag"], d["title"])
    gap = round(w*0.035)
    pwL = round((w-2*m-gap)*0.42); pwR = (w-2*m-gap) - pwL
    py = round(h*PY); gh = round(h*GH)
    # left: the market — custom donut, vertically centred with breathing room
    pxL = m
    out += [dv.panel(pxL, py, pwL, gh, w)]
    out += [eyebrow(pxL+pin, py+pin+round(ty(w,"eyebrow")*0.9), "The market",
                    size=ty(w,"eyebrow"), color=C.eyebrow_ink)]
    cx = pxL+pwL/2; cy = py+gh*0.50; r = round(gh*0.225); sw = round(gh*0.045)
    out += [more.donut(cx, cy, r, sw, d["odds"], DOWN)]
    fs = round(r*0.78)
    out += [f'<text x="{cx}" y="{cy+round(fs*0.34)}" text-anchor="middle" font-family="{F.sans}" '
            f'font-size="{fs}" font-weight="800" fill="{INK}">{d["odds"]}%</text>']
    out += [body(cx, cy+r+round(gh*0.18), d["odds_sub"], size=round(ty(w,"caption")*0.92),
                 weight=600, color=MUTE, anchor="middle")]
    # right: the headlines
    pxR = m + pwL + gap
    out += [dv.panel(pxR, py, pwR, gh, w)]
    out += [eyebrow(pxR+pin, py+pin+round(ty(w,"eyebrow")*0.9), "The headlines",
                    size=ty(w,"eyebrow"), color=C.eyebrow_ink)]
    bsz = round(w*0.029)
    yy = py + pin + round(bsz*2.3)
    wrap_w = pwR - 2*pin - round(bsz*1.2)
    for b in d["bullets"]:
        out += [f'<circle cx="{pxR+pin+round(bsz*0.32)}" cy="{yy-round(bsz*0.30)}" '
                f'r="{round(bsz*0.20)}" fill="{UP}"/>']
        lines = pmn.wrap(b, bsz, wrap_w)
        for k, ln in enumerate(lines):
            out += [body(pxR+pin+round(bsz*0.95), yy+k*round(bsz*1.20), ln,
                         size=bsz, weight=600, color=INK)]
        yy += len(lines)*round(bsz*1.20) + round(bsz*1.0)
    _caption(out, w, h, d["caption"]); _foot(out, w, h, d["source"])
    return "".join(out)


# ── DATA ─────────────────────────────────────────────────────────────────────
SPACEX = {
    "tag": "Implied valuation · SpaceX IPO", "title": ["What the crowd thinks", "SpaceX is worth"],
    "points": [(1.4,96.5),(1.6,92.0),(1.8,77.5),(2.0,62.5),(2.2,45.5),(2.4,27.5),(2.6,14.5),(2.8,10.5),(3.0,6.5)],
    "xmin": 1.3, "xmax": 3.15, "xlabels": [1.4, 2.0, 2.6, 3.0],
    "marker": {"x": 1.75, "label": "Rumored debut ~$1.75T"}, "crossover": 2.12,
    "caption": "The crowd prices SpaceX above its rumored tag. Coin-flip near $2.1T.",
    "source": "Polymarket · Jun 8, 2026"}

AIMODEL = {
    "tag": "Top AI model · end of June", "title": ["One lab is running", "away with it"],
    "leader": ("Anthropic", 85), "field": [("Google", 10), ("OpenAI", 4), ("xAI", 0.4)],
    "caption": "Claude Opus 4.8 took #1 on May 27. The field fights for scraps.",
    "source": "Polymarket · Jun 8, 2026"}

OPTIMUS = {
    "tag": "Hype, meet the order book", "title": ["Wall Street's robot,", "priced at 1%"],
    "odds": 1, "odds_sub": "ships by Jun 30",
    "bullets": ["Jensen Huang: humanoids 'right around the corner'",
                "Goldman 6x'd its forecast: $38B by 2035",
                "Unitree shipped ~5,500 units, eyeing 10–20k"],
    "caption": "The narrative says trillion-dollar industry. The market says 1%.",
    "source": "Polymarket · CNBC · Goldman"}

CARDS = [("spacex-curve", card_curve, SPACEX),
         ("aimodel-dominance", card_dominance, AIMODEL),
         ("optimus-contrast", card_contrast, OPTIMUS)]

# Each background gets its OWN glass transparency: calm fields read through a
# more see-through panel; brighter/busier fields use a more opaque panel so the
# white/muted text stays WCAG-safe (team-gradient's bright corner needs it most).
BG_TINT = {
    "team-solid":    0.55,   # flat near-black -> most see-through
    "team-glow":     0.66,   # blue top-glow reads through the panel head
    "house":         0.80,   # diagonal field -> moderately opaque
    "team-gradient": 0.90,   # black->bright-blue -> most opaque (AA on the corner)
}


def render(fn, data, bg, tint, fname):
    global TINT
    TINT = tint
    pmn.set_background(bg)
    svg = fn(S, S, data)
    base = os.path.join(OUT, fname)
    open(base + ".svg", "w").write(svg)
    subprocess.run(["rsvg-convert", "-o", base + ".png", base + ".svg"], check=True)
    print(f"    {fname}  (bg={bg}, glass={int(tint*100)})")


n = 0
# primaries — the canonical hero look (team-gradient, balanced tint)
for i, (key, fn, data) in enumerate(CARDS, 1):
    render(fn, data, "team-gradient", 0.80, f"tech-0{i}-{key}"); n += 1

# ── background sweep — every card across all 4 fields, each at its own tint ───
for key, fn, data in CARDS:
    for bg, t in BG_TINT.items():
        render(fn, data, bg, t, f"var-{key}--{bg}-t{int(t*100)}"); n += 1

# ── glass sweep — the SpaceX hero on team-gradient at 4 tints (fine compare) ──
for t in (0.50, 0.65, 0.80, 0.92):
    render(card_curve, SPACEX, "team-gradient", t, f"var-spacex-curve--glass-{int(t*100)}"); n += 1

pmn.set_background("house")
print(f"\nwrote {n} tech-market cards (+variants) -> {os.path.relpath(OUT, ROOT)}/")
