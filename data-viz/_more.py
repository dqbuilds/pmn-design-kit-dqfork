#!/usr/bin/env python3
"""
Ten more PMN infographics, on the black panel (white text, AA). Reuses helpers
from _build.py (panel, legend, _axes, card_shell, footer, tokens).

  07 movers        biggest movers board (▲/▼ this week)
  08 head-to-head  same market on two venues
  09 gauge         single probability dial
  10 leaderboard   top markets by volume
  11 calendar      what resolves this week
  12 scorecard     calls vs outcomes
  13 annotated     odds line with event markers
  14 range         implied probability range
  15 map           battleground tile cartogram
  16 scatter       odds vs volume
Run:  python3 _more.py
"""
import os, math
import _build as B
from pmn import svg_open, svg_close, defs, field, chrome, eyebrow, headline, body, ty, M, C, F

OUT = B.OUT
# theme vars (kept in sync by B.set_mode)
INK, MUTE, TRACK, PANEL, RANK = B.INK, B.MUTE, B.TRACK, B.PANEL, B.RANK
BORDER, BOP, TOP, UP, DOWN, THEME = B.BORDER, B.BOP, B.TOP, B.UP, B.DOWN, B.THEME
def esc(t): return B.esc(t)
def pin_(w): return B.PADIN(w)


def donut(cx, cy, r, sw, pct, color=C.blue):
    circ = 2*math.pi*r; arc = circ*pct/100
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{TRACK}" stroke-opacity="{TOP}" stroke-width="{sw}"/>'
            f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{color}" stroke-width="{sw}" '
            f'stroke-linecap="round" stroke-dasharray="{arc:.1f} {circ-arc:.1f}" transform="rotate(-90 {cx} {cy})"/>')

def divider(x1, x2, y):
    return f'<line x1="{x1}" y1="{y:.0f}" x2="{x2}" y2="{y:.0f}" stroke="{TRACK}" stroke-opacity="{TOP}" stroke-width="1"/>'

def fit(s, size, maxw):
    """Truncate a label with an ellipsis so it never reaches the right-hand column."""
    maxch = max(5, int(maxw/(size*0.52)))
    return s if len(s) <= maxch else s[:maxch-1].rstrip()+"…"

def lerp_color(a, b, t):
    a = tuple(int(a[i:i+2],16) for i in (1,3,5)); b = tuple(int(b[i:i+2],16) for i in (1,3,5))
    return "#%02X%02X%02X" % tuple(round(a[i]+(b[i]-a[i])*t) for i in range(3))


# 07 ─ biggest movers ────────────────────────────────────────────────────────
def movers_panel(x, y, pw, w, rows):
    pin = pin_(w); nsz = ty(w,"lead"); psz = round(w*0.034); dsz = round(w*0.030)
    row_h = round(nsz*2.1); gh = pin + len(rows)*row_h + round(pin*0.3)
    out = [B.panel(x, y, pw, gh, w)]
    yy = y+pin+round(nsz*0.9)
    for i,(name, cur, delta) in enumerate(rows):
        out += [body(x+pin, yy, fit(name, nsz, pw-2*pin-round(w*0.23)), size=nsz, weight=700, color=INK)]
        out += [body(x+pw-pin, yy, f"{cur}%", size=psz, weight=800, color=INK, anchor="end")]
        up = delta >= 0; col = UP if up else DOWN; arr = "▲" if up else "▼"
        out += [body(x+pw-pin-round(w*0.105), yy, f"{arr} {abs(delta)}", size=dsz, weight=700, color=col, anchor="end")]
        if i < len(rows)-1: out += [divider(x+pin, x+pw-pin, yy+row_h*0.45)]
        yy += row_h
    return "".join(out), gh

# 08 ─ head to head ──────────────────────────────────────────────────────────
def h2h_panel(x, y, pw, w, left, right):
    pin = pin_(w); gh = round(pw*0.50)
    out = [B.panel(x, y, pw, gh, w)]
    out += [f'<line x1="{x+pw/2}" y1="{y+pin}" x2="{x+pw/2}" y2="{y+gh-pin}" stroke="{TRACK}" stroke-opacity="{TOP}" stroke-width="1.5"/>']
    for i,(venue, pct, col) in enumerate([left, right]):
        cx = x+pw*(0.25 if i==0 else 0.75)
        out += [body(cx, y+pin+round(ty(w,"caption")*0.9), venue, size=ty(w,"caption"), weight=700, color=MUTE, anchor="middle")]
        out += [f'<text x="{cx}" y="{y+gh*0.60}" text-anchor="middle" font-family="{F.sans}" font-size="{round(pw*0.15)}" font-weight="800" fill="{col}">{pct}%</text>']
        out += [body(cx, y+gh*0.60+round(pw*0.045), "Yes", size=ty(w,"caption"), weight=600, color=MUTE, anchor="middle")]
    spread = abs(left[1]-right[1])
    out += [f'<rect x="{x+pw/2-round(w*0.10)}" y="{y+gh-pin-round(w*0.045)}" width="{round(w*0.20)}" height="{round(w*0.052)}" rx="{round(w*0.026)}" fill="{TRACK}" fill-opacity="{TOP}"/>']
    out += [body(x+pw/2, y+gh-pin-round(w*0.012), f"{spread} pt spread", size=ty(w,"caption"), weight=700, color=INK, anchor="middle")]
    return "".join(out), gh

# 09 ─ gauge ─────────────────────────────────────────────────────────────────
def gauge_panel(x, y, pw, w, pct, sub, color=C.blue):
    gh = round(pw*0.52); cx = x+pw/2; cy = y+gh*0.45; r = round(gh*0.36); sw = round(gh*0.066)
    fs = round(r*0.66)                                   # fits inside the ring
    out = [B.panel(x, y, pw, gh, w), donut(cx, cy, r, sw, pct, color)]
    out += [f'<text x="{cx}" y="{cy+round(fs*0.34)}" text-anchor="middle" font-family="{F.sans}" '
            f'font-size="{fs}" font-weight="800" fill="{INK}">{pct}%</text>']
    out += [body(cx, cy+r+round(gh*0.15), sub, size=ty(w,"lead"), weight=600, color=MUTE, anchor="middle")]
    return "".join(out), gh

# 10 ─ leaderboard ───────────────────────────────────────────────────────────
def leaderboard_panel(x, y, pw, w, rows):
    pin = pin_(w); nsz = round(w*0.040); barh = round(w*0.014)
    row_h = nsz + round(nsz*0.40) + barh + round(w*0.014)
    gh = pin + len(rows)*row_h + round(pin*0.3)
    maxv = max(r[1] for r in rows); inner = pw-2*pin
    out = [B.panel(x, y, pw, gh, w)]; yy = y+pin
    for i,(name, vol, disp) in enumerate(rows):
        out += [body(x+pin, yy+nsz*0.82, fit(f"{i+1}.  {name}", nsz, pw-2*pin-round(w*0.17)), size=nsz, weight=700, color=INK)]
        out += [body(x+pw-pin, yy+nsz*0.82, disp, size=round(w*0.032), weight=800, color=INK, anchor="end")]
        bary = yy+nsz+round(nsz*0.42)
        out += [f'<rect x="{x+pin}" y="{bary}" width="{inner}" height="{barh}" rx="{barh//2}" fill="{TRACK}" fill-opacity="{TOP}"/>']
        out += [f'<rect x="{x+pin}" y="{bary}" width="{round(inner*vol/maxv)}" height="{barh}" rx="{barh//2}" fill="{RANK[i%len(RANK)]}"/>']
        yy += row_h
    return "".join(out), gh

# 11 ─ resolution calendar ───────────────────────────────────────────────────
def calendar_panel(x, y, pw, w, rows):
    pin = pin_(w); nsz = ty(w,"lead"); dsz = round(w*0.030)
    row_h = round(nsz*2.2); gh = pin + len(rows)*row_h + round(pin*0.3)
    lx = x+pin+round(w*0.15)
    out = [B.panel(x, y, pw, gh, w)]
    out += [f'<line x1="{lx}" y1="{y+pin+round(nsz*0.4)}" x2="{lx}" y2="{y+gh-pin}" stroke="{TRACK}" stroke-opacity="0.18" stroke-width="2"/>']
    yy = y+pin+round(nsz*0.9)
    for date, name, pct in rows:
        out += [body(x+pin, yy, date, size=dsz, weight=700, color=MUTE)]
        out += [f'<circle cx="{lx}" cy="{yy-round(nsz*0.28)}" r="{round(w*0.011)}" fill="{C.blue}" stroke="{PANEL}" stroke-width="3"/>']
        out += [body(lx+round(w*0.045), yy, name, size=nsz, weight=700, color=INK)]
        out += [body(x+pw-pin, yy, f"{pct}%", size=round(w*0.032), weight=800, color=INK, anchor="end")]
        yy += row_h
    return "".join(out), gh

# 12 ─ scorecard ─────────────────────────────────────────────────────────────
def scorecard_panel(x, y, pw, w, rows):
    pin = pin_(w); nsz = round(w*0.038); rsz = round(w*0.030)
    row_h = round(nsz*2.3); gh = pin + len(rows)*row_h + round(pin*0.3)
    out = [B.panel(x, y, pw, gh, w)]; yy = y+pin+round(nsz*0.9); br = round(w*0.022)
    for i,(call, result, hit) in enumerate(rows):
        col = UP if hit else DOWN; sym = "✓" if hit else "✗"
        out += [f'<circle cx="{x+pin+br}" cy="{yy-round(nsz*0.3)}" r="{br}" fill="{col}" fill-opacity="0.18"/>'
                f'<text x="{x+pin+br}" y="{yy-round(nsz*0.3)+round(br*0.4)}" text-anchor="middle" '
                f'font-family="{F.sans}" font-size="{round(br*1.2)}" font-weight="800" fill="{col}">{sym}</text>']
        cx0 = x+pin+2*br+round(w*0.025)
        out += [body(cx0, yy, fit(call, nsz, (x+pw-pin-round(w*0.30))-cx0), size=nsz, weight=700, color=INK)]
        out += [body(x+pw-pin, yy, result, size=rsz, weight=700, color=col, anchor="end")]
        if i < len(rows)-1: out += [divider(x+pin, x+pw-pin, yy+row_h*0.42)]
        yy += row_h
    return "".join(out), gh

# 13 ─ annotated odds line ───────────────────────────────────────────────────
def annot_panel(x, y, pw, w, series, marks):
    pin = pin_(w); lab_w = round(w*0.058); gh = round(pw*0.56)
    out = [B.panel(x, y, pw, gh, w)]
    ax, plot_x, plot_top, plot_w, plot_h = B._axes(x, y, pw, w, gh, lab_w, 100, (0,25,50,75,100), "")
    out += ax
    n = len(series)
    px = lambda i: plot_x + plot_w*i/(n-1); py = lambda v: plot_top + plot_h*(1-v/100)
    pts = " ".join(f"{px(i):.1f},{py(v):.1f}" for i,(_,v) in enumerate(series))
    out += [f'<defs><linearGradient id="aa" x1="0" y1="0" x2="0" y2="1">'
            f'<stop offset="0" stop-color="{C.blue}" stop-opacity="0.26"/>'
            f'<stop offset="1" stop-color="{C.blue}" stop-opacity="0.02"/></linearGradient></defs>']
    out += [f'<polygon points="{plot_x},{plot_top+plot_h} {pts} {plot_x+plot_w},{plot_top+plot_h}" fill="url(#aa)"/>']
    out += [f'<polyline points="{pts}" fill="none" stroke="{C.blue}" stroke-width="{max(3,round(w*0.004))}" stroke-linejoin="round"/>']
    for idx, label in marks:
        mx = px(idx)
        out += [f'<line x1="{mx:.0f}" y1="{plot_top}" x2="{mx:.0f}" y2="{plot_top+plot_h}" stroke="{INK}" stroke-opacity="0.35" stroke-width="1.5" stroke-dasharray="5 5"/>']
        out += [f'<circle cx="{mx:.0f}" cy="{py(series[idx][1]):.0f}" r="{round(w*0.008)}" fill="{INK}"/>']
        out += [body(mx, plot_top-round(w*0.012), label, size=round(ty(w,"caption")*0.82), weight=700, color=INK, anchor="middle")]
    for i in (0, n-1):
        out += [body(px(i), plot_top+plot_h+round(ty(w,"caption")*1.4), series[i][0],
                     size=round(ty(w,"caption")*0.9), weight=600, color=MUTE, anchor=("start" if i==0 else "end"))]
    return "".join(out), gh

# 14 ─ implied range ─────────────────────────────────────────────────────────
def range_panel(x, y, pw, w, low, mid, high):
    pin = pin_(w); gh = round(pw*0.40)
    out = [B.panel(x, y, pw, gh, w)]
    tx = x+pin; tw = pw-2*pin; tyy = y+gh*0.56; th = round(w*0.020)
    fx = lambda v: tx + tw*v/100
    out += [f'<rect x="{tx}" y="{tyy}" width="{tw}" height="{th}" rx="{th//2}" fill="{TRACK}" fill-opacity="{TOP}"/>']
    out += [f'<rect x="{fx(low):.0f}" y="{tyy}" width="{fx(high)-fx(low):.0f}" height="{th}" rx="{th//2}" fill="{C.blue}" fill-opacity="0.45"/>']
    out += [f'<circle cx="{fx(mid):.0f}" cy="{tyy+th/2:.0f}" r="{round(th*0.95)}" fill="{C.blue}" stroke="{PANEL}" stroke-width="3"/>']
    out += [f'<text x="{fx(mid):.0f}" y="{tyy-round(w*0.025)}" text-anchor="middle" font-family="{F.sans}" font-size="{round(w*0.064)}" font-weight="800" fill="{INK}">{mid}%</text>']
    for v, lab in [(low,f"Low {low}%"),(high,f"High {high}%")]:
        out += [body(fx(v), tyy+th+round(w*0.05), lab, size=ty(w,"caption"), weight=600, color=MUTE, anchor="middle")]
    return "".join(out), gh

# 15 ─ battleground tile map ─────────────────────────────────────────────────
def map_panel(x, y, pw, w, states):
    pin = pin_(w); gh = round(pw*0.55)
    cols = max(c for _,c,_,_ in states)+1; rows = max(r for _,_,r,_ in states)+1
    avail_w = pw-2*pin; avail_h = gh-2*pin-round(w*0.085)
    t = min(avail_w/cols, avail_h/rows); gap = t*0.12; ts = t-gap
    ox = x+pin+(avail_w-cols*t)/2; oy = y+pin+round(w*0.03)
    out = [B.panel(x, y, pw, gh, w)]
    for abbr, c, r, pct in states:
        bx = ox+c*t; by = oy+r*t
        col = lerp_color(DOWN, C.blue, pct/100) if pct>=0 else "#3A4150"
        out += [f'<rect x="{bx:.0f}" y="{by:.0f}" width="{ts:.0f}" height="{ts:.0f}" rx="{round(ts*0.16)}" fill="{col}"/>']
        out += [f'<text x="{bx+ts/2:.0f}" y="{by+ts*0.45:.0f}" text-anchor="middle" font-family="{F.sans}" font-size="{round(ts*0.26)}" font-weight="800" fill="#FFFFFF">{abbr}</text>']
        out += [f'<text x="{bx+ts/2:.0f}" y="{by+ts*0.74:.0f}" text-anchor="middle" font-family="{F.sans}" font-size="{round(ts*0.22)}" font-weight="700" fill="#FFFFFF" fill-opacity="0.85">{pct}</text>']
    # legend gradient
    lgx = x+pin; lgy = y+gh-round(w*0.055); lgw = round(pw*0.5); lgh = round(w*0.018)
    out += [f'<defs><linearGradient id="mg" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{DOWN}"/><stop offset="1" stop-color="{C.blue}"/></linearGradient></defs>']
    out += [f'<rect x="{lgx}" y="{lgy}" width="{lgw}" height="{lgh}" rx="{lgh//2}" fill="url(#mg)"/>']
    out += [body(lgx, lgy-round(w*0.01), "No", size=round(ty(w,"caption")*0.85), weight=600, color=MUTE)]
    out += [body(lgx+lgw, lgy-round(w*0.01), "Yes", size=round(ty(w,"caption")*0.85), weight=600, color=MUTE, anchor="end")]
    return "".join(out), gh

# 16 ─ scatter (odds vs volume) ──────────────────────────────────────────────
def scatter_panel(x, y, pw, w, points):
    pin = pin_(w); lab_w = round(w*0.06); gh = round(pw*0.58)
    out = [B.panel(x, y, pw, gh, w)]
    plot_x = x+pin+lab_w; plot_top = y+pin+round(w*0.03)
    plot_w = pw-2*pin-lab_w; plot_h = gh-2*pin-round(w*0.07)
    maxv = max(p[2] for p in points);
    for g in (0,25,50,75,100):
        gx = plot_x+plot_w*g/100
        out += [f'<line x1="{gx:.0f}" y1="{plot_top}" x2="{gx:.0f}" y2="{plot_top+plot_h}" stroke="{TRACK}" stroke-opacity="{TOP}" stroke-width="1"/>']
        out += [body(gx, plot_top+plot_h+round(ty(w,"caption")*1.3), f"{g}", size=round(ty(w,"caption")*0.8), weight=600, color=MUTE, anchor="middle")]
    px = lambda o: plot_x+plot_w*o/100; py = lambda v: plot_top+plot_h*(1-v/maxv)
    for name, odds, vol in points:
        out += [f'<circle cx="{px(odds):.0f}" cy="{py(vol):.0f}" r="{round(w*0.013)}" fill="{C.blue}" fill-opacity="0.85" stroke="{PANEL}" stroke-width="1.5"/>']
        out += [body(px(odds)+round(w*0.018), py(vol)+round(ty(w,"caption")*0.3), name, size=round(ty(w,"caption")*0.85), weight=600, color=INK)]
    out += [body(plot_x+plot_w/2, plot_top+plot_h+round(ty(w,"caption")*2.6), "Odds (Yes %)  →", size=round(ty(w,"caption")*0.85), weight=600, color=MUTE, anchor="middle")]
    out += [body(x+pin, plot_top-round(w*0.005), "Volume ↑", size=round(ty(w,"caption")*0.85), weight=600, color=MUTE)]
    return "".join(out), gh


# ── cards ───────────────────────────────────────────────────────────────────
def C_(tag, q, fn, src="Polymarket", hs=0.050):
    return lambda w,h,m: B.card_shell(w,h, m["tag"], m["q"], fn(m), hs_ratio=hs, source=src)

MOVERS = {"tag":"Biggest movers · this week","q":["What the market","repriced"]}
H2H    = {"tag":"Same market, two venues","q":["Fed cuts before","September?"]}
GAUGE  = {"tag":"Live odds","q":["U.S. recession","before 2027?"]}
LEAD   = {"tag":"Top markets by volume · 7d","q":["Where the action","is right now"]}
CAL    = {"tag":"Resolving this week","q":["On the calendar"]}
SCORE  = {"tag":"The scorecard · season","q":["How the calls","aged"]}
ANNOT  = {"tag":"What moved the market · 60d","q":["Fed cuts before September?"]}
RANGE  = {"tag":"Implied probability","q":["Recession before 2027?"]}
MAP    = {"tag":"Battleground odds · 2028","q":["Who takes the","swing states?"]}
SCAT   = {"tag":"Odds vs depth","q":["Which markets","are thin?"]}

JOBS = [
 ("07-movers",      lambda w,h,m: B.card_shell(w,h,m["tag"],m["q"], lambda x,y,pw,ww: movers_panel(x,y,pw,ww,
     [("Trump declassifies UFO files",67,12),("BTC above $150k in 2026",41,-9),
      ("Fed cuts before September",63,8),("Recession before 2027",34,-6),
      ("ETH flips BTC by EOY",4,-3)]), hs_ratio=0.050), MOVERS),
 ("08-head-to-head",lambda w,h,m: B.card_shell(w,h,m["tag"],m["q"], lambda x,y,pw,ww: h2h_panel(x,y,pw,ww,
     ("Polymarket",63,C.blue),("Kalshi",58,B.UP)), hs_ratio=0.052,source="Polymarket · Kalshi"), H2H),
 ("09-gauge",       lambda w,h,m: B.card_shell(w,h,m["tag"],m["q"], lambda x,y,pw,ww: gauge_panel(x,y,pw,ww,34,"chance of recession"), hs_ratio=0.052,source="Polymarket"), GAUGE),
 ("10-leaderboard", lambda w,h,m: B.card_shell(w,h,m["tag"],m["q"], lambda x,y,pw,ww: leaderboard_panel(x,y,pw,ww,
     [("2028 Presidential winner",9100,"$9.1M"),("Fed September decision",4300,"$4.3M"),
      ("Trump UFO files",2980,"$3.0M"),("Recession 2026",1800,"$1.8M"),
      ("Bitcoin $150k",1620,"$1.6M")]), hs_ratio=0.050,source="Polymarket"), LEAD),
 ("11-calendar",    lambda w,h,m: B.card_shell(w,h,m["tag"],m["q"], lambda x,y,pw,ww: calendar_panel(x,y,pw,ww,
     [("Mon","Fed rate decision",63),("Wed","CPI print > 3%",44),
      ("Fri","Jobless claims beat",58),("Sun","French Open winner",71)]), hs_ratio=0.052,source="Polymarket"), CAL),
 ("12-scorecard",   lambda w,h,m: B.card_shell(w,h,m["tag"],m["q"], lambda x,y,pw,ww: scorecard_panel(x,y,pw,ww,
     [("BTC tops $100k in 2024","Resolved YES",True),("ETH flips BTC by EOY","▼ 68%",False),
      ("Fed cuts by September","On track · 63%",True),("Recession in 2025","Resolved NO",False)]), hs_ratio=0.050,source="Polymarket"), SCORE),
 ("13-annotated",   lambda w,h,m: B.card_shell(w,h,m["tag"],m["q"], lambda x,y,pw,ww: annot_panel(x,y,pw,ww,
     [("Apr",38),("",41),("",39),("",46),("",52),("",49),("",58),("Now",63)],
     [(3,"Powell"),(6,"CPI")]), hs_ratio=0.050,source="Polymarket"), ANNOT),
 ("14-range",       lambda w,h,m: B.card_shell(w,h,m["tag"],m["q"], lambda x,y,pw,ww: range_panel(x,y,pw,ww,26,34,47), hs_ratio=0.052,source="Polymarket"), RANGE),
 ("15-map",         lambda w,h,m: B.card_shell(w,h,m["tag"],m["q"], lambda x,y,pw,ww: map_panel(x,y,pw,ww,
     [("NV",0,1,49),("AZ",1,1,46),("WI",2,0,52),("MI",3,0,54),("PA",4,0,51),
      ("GA",4,2,47),("NC",5,2,44)]), hs_ratio=0.052,source="Polymarket"), MAP),
 ("16-scatter",     lambda w,h,m: B.card_shell(w,h,m["tag"],m["q"], lambda x,y,pw,ww: scatter_panel(x,y,pw,ww,
     [("Election",52,95),("Fed",63,43),("UFO",67,30),("Recession",34,18),("BTC",41,16)]), hs_ratio=0.050,source="Polymarket"), SCAT),
]

if __name__ == "__main__":
    for name, fn, data in JOBS:
        open(f"{OUT}/{name}.svg","w").write(fn(1080,1080,data)); print("  ",name)
    print(f"wrote {len(JOBS)} infographics")
