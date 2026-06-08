#!/usr/bin/env python3
"""
PMN data-viz cards. Four types, all on the blue field with a frosted data panel:
  1. binary   — Yes/No market (the fixed bars: thin, full-width, % on the line)
  2. multi     — up to 5 outcomes, ranked
  3. timeseries — odds over time (line + area)
  4. hero-quote — a quote + a hero stat ("down 68% since the call · Ep. 2")

Run:  python3 _build.py
"""
import sys, os, io, base64
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "lib"))
import numpy as np
from PIL import Image
import pmn
from pmn import (C, F, svg_open, svg_close, defs, field, eyebrow, headline,
                 body, serif_head, frosted_panel, blue_bar, M, PADIN, ty, logo, wrap)

OUT = os.path.join(os.path.dirname(__file__), "exports"); os.makedirs(OUT, exist_ok=True)

# ── THEME (dark only) ────────────────────────────────────────────────────────
# Black panel + dark field + white text/marks. (Light mode scrapped.)
MODES = {
 "dark":  dict(fa="#05060D",fb="#10204F",fc="#2E5CFF", panel="#06080F", border="#FFFFFF", bop=0.12,
               ink="#FFFFFF", mute="#9AA6C9", track="#FFFFFF", top=0.12, title="#FFFFFF",
               eyebrow="#B6C4DC", mark="#FFFFFF", lockup="white", up="#16C784", down="#EA3943",
               rank=["#2E5CFF","#5A7BF5","#7E97EC","#9DB0E3","#B6C4DC"]),
}
THEME = MODES["dark"]
def _apply():
    global RANK,INK,MUTE,TRACK,PANEL,BORDER,BOP,TOP,UP,DOWN
    t = THEME
    RANK=t["rank"]; INK=t["ink"]; MUTE=t["mute"]; TRACK=t["track"]; PANEL=t["panel"]
    BORDER=t["border"]; BOP=t["bop"]; TOP=t["top"]; UP=t["up"]; DOWN=t["down"]
_apply()

def set_mode(mode):
    """Switch all data-viz cards (this module + _more) between 'light'/'dark'."""
    global THEME
    THEME = MODES[mode]; _apply()
    pmn.set_field_theme(THEME["fa"], THEME["fb"], THEME["fc"])
    other = sys.modules.get("_more")
    if other:
        other.THEME = THEME
        for k in ("RANK","INK","MUTE","TRACK","PANEL","BORDER","BOP","TOP","UP","DOWN"):
            setattr(other, k, globals()[k])


def panel(x, y, pw, gh, w, texture=None):
    """Data panel (textured dark box) + hairline border + shadow. Texture is
    capped at the dark end so white/muted text stays AA (see pmn._panel_body)."""
    rx = round(w*0.025)
    return (pmn._panel_body(x, y, pw, gh, rx, PANEL, texture or pmn.PANEL_TEX)
            + f'<rect x="{x}" y="{y}" width="{pw}" height="{gh}" rx="{rx}" fill="none" '
              f'stroke="{BORDER}" stroke-opacity="{BOP}" stroke-width="1.5"/>')


# ── mode-aware chrome (recoloured marks) + footer lockup ─────────────────────
def _recolor(inner, color): return inner.replace("#FFFFFF", color).replace("white", color)

def chrome(w, h):
    pad = M(w); bh = round(w*0.030); col = THEME["mark"]
    s = bh/pmn._BLOCK_H
    blk = f'<g transform="translate({pad},{pad}) scale({s})">{_recolor(pmn._BLOCK_INNER,col)}</g>'
    ph = round(bh*0.78); ps = ph/pmn._POLY_H; pw_ = pmn._POLY_W*ps; xr = w-pad
    lsz = max(ph*0.52, 15)
    poly = (f'<text x="{xr-pw_-18}" y="{pad+ph*0.5+lsz*0.36:.1f}" text-anchor="end" font-family="{F.sans}" '
            f'font-size="{lsz:.1f}" font-weight="600" letter-spacing="1.5" fill="{THEME["mute"]}">PRESENTED BY</text>'
            f'<g transform="translate({xr-pw_},{pad}) scale({ps})" opacity="0.96">{_recolor(pmn._POLY_INNER,col)}</g>')
    return blk + poly

_LOCK = {}
def _lockup_dark_b64(which):
    if which not in _LOCK:
        idx = pmn.LOGOS[which]
        im = Image.open(pmn.LOGO_DIR / f"logo-{idx:02d}.png").convert("RGBA")
        a = np.array(im).astype(int)
        wh = (a[...,0]>175)&(a[...,1]>175)&(a[...,2]>175)        # white → dark navy
        for k,v in zip((0,1,2),(11,20,48)): a[...,k] = np.where(wh, v, a[...,k])
        out = Image.fromarray(a.astype("uint8"),"RGBA")
        buf = io.BytesIO(); out.save(buf,"PNG")
        _LOCK[which] = (base64.b64encode(buf.getvalue()).decode(), im.width, im.height)
    return _LOCK[which]

# selectable footer lockup (taller lockups get more height to stay legible)
FOOTER_LOGO = "monogram"
# data cards keep footers compact (panels are tall) — smaller than the social set
_FOOTER_H = {"monogram":0.042,"sans-news":0.046,"sans-stack":0.046,"bold-bar":0.052,"arrow-n":0.060}

def footer(w, h, which=None):
    which = which or FOOTER_LOGO
    lh = round(h * _FOOTER_H.get(which, 0.050))
    if THEME["lockup"] == "white":
        return logo(which, M(w), h-M(w)-lh, lh, align="left", opacity=0.97)
    data, iw, ih = _lockup_dark_b64(which)
    return f'<image x="{M(w)}" y="{h-M(w)-lh:.0f}" width="{lh*iw/ih:.0f}" height="{lh}" xlink:href="data:image/png;base64,{data}"/>'


# selectable blue field gradient (matches the social blue-variations)
BLUE_GRADS = {
    "electric-blue": ("#05060D","#10204F","#2E5CFF"),
    "deep-blue":     ("#03040C","#081A46","#0B3AD6"),
    "cover-blue":    ("#050F2A","#0A3AA0","#1450E0"),
    "midnight":      ("#020308","#0A1645","#1E3AD6"),
}
def set_gradient(key):
    pmn.set_field_theme(*BLUE_GRADS[key])


# ── team backgrounds (from PMN backgrounds.zip) ──────────────────────────────
# Bold black→electric-blue gradient + near-black solid + blue edge-glow. Darker
# than the house field, so white text clears AA easily (verified separately).
def bg_team_gradient(w, h):
    return (f'<defs><linearGradient id="tg" x1="0" y1="0" x2="{w}" y2="{h}" gradientUnits="userSpaceOnUse">'
            f'<stop stop-color="#000000"/><stop offset="1" stop-color="#2E5CFF"/></linearGradient></defs>'
            f'<rect width="{w}" height="{h}" fill="url(#tg)"/>')

def bg_team_solid(w, h):
    return f'<rect width="{w}" height="{h}" fill="#111111"/>'

def bg_team_glow(w, h):
    return (f'<defs><radialGradient id="tgl" gradientUnits="userSpaceOnUse" '
            f'cx="{w*0.5}" cy="{h*0.02}" r="{max(w,h)*0.85}">'
            f'<stop offset="0" stop-color="#2E5CFF" stop-opacity="0.40"/>'
            f'<stop offset="0.55" stop-color="#06122E" stop-opacity="0"/></radialGradient></defs>'
            f'<rect width="{w}" height="{h}" fill="#000000"/>'
            f'<rect width="{w}" height="{h}" fill="url(#tgl)"/>')

BACKGROUNDS = {"house": None, "team-gradient": bg_team_gradient,
               "team-solid": bg_team_solid, "team-glow": bg_team_glow}
BACKGROUND = None
def set_background(key):
    global BACKGROUND; BACKGROUND = BACKGROUNDS[key]
def _bg(w, h):
    return BACKGROUND(w, h) if BACKGROUND else field(w, h)
def _src_color():
    # team-gradient's bottom-right corner is bright #2E5CFF; muted fine-print
    # fails AA there (2.2:1). Promote to white (5.2:1) only for that field.
    return "#FFFFFF" if BACKGROUND is bg_team_gradient else THEME["mute"]

def esc(t): return str(t).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")


# ── shared: outcome panel (thin full-width bars; works for 2–5 outcomes) ─────
def outcome_panel(x, y, pw, w, outcomes, source="Polymarket", title=None):
    """outcomes = [(name, pct, color)]. Returns (svg, height)."""
    pin = PADIN(w)
    dense = len(outcomes) > 3
    nsz = round(w*0.042) if dense else ty(w, "lead")
    psz = round(w*(0.030 if dense else 0.032)); barh = round(w*(0.013 if dense else 0.016))
    gap_nb = round(nsz*0.40)               # name → bar
    row_h = nsz + gap_nb + barh + round(w*(0.013 if dense else 0.028))
    th = (round(ty(w,'eyebrow')*1.7) if title else 0)
    src_h = round(ty(w,"caption")*(1.5 if dense else 1.9))
    gh = pin + th + len(outcomes)*row_h + src_h + round(pin*0.4)
    inner = pw - 2*pin
    out = [panel(x, y, pw, gh, w)]
    yy = y + pin
    if title:
        out += [eyebrow(x+pin, yy+round(ty(w,'eyebrow')*0.9), title, color=C.eyebrow_ink, size=ty(w,'eyebrow'))]
        yy += th
    for name, pct, col in outcomes:
        out += [body(x+pin, yy+nsz*0.82, esc(name), size=nsz, weight=700, color=INK)]
        out += [body(x+pw-pin, yy+nsz*0.82, f"{pct}%", size=psz, weight=800, color=INK, anchor="end")]
        bary = yy + nsz + gap_nb
        out += [f'<rect x="{x+pin}" y="{bary}" width="{inner}" height="{barh}" rx="{barh//2}" '
                f'fill="{TRACK}" fill-opacity="0.10"/>']
        out += [f'<rect x="{x+pin}" y="{bary}" width="{round(inner*pct/100)}" height="{barh}" '
                f'rx="{barh//2}" fill="{col}"/>']
        yy += row_h
    out += [body(x+pin, y+gh-pin+round(ty(w,'caption')*0.3), f"Source: {source}",
                 size=ty(w,"caption"), weight=600, color=MUTE)]
    return "".join(out), gh


def card_shell(w, h, tag, q_lines, panel_fn, hs_ratio=0.052, source=None):
    """Aspect-aware: stacked for square/portrait/vertical, 2-column for landscape.
    The panel always gets an *effective* width so its type scales to the column,
    not the full canvas."""
    m = M(w); n = len(q_lines)
    out = [svg_open(w, h, "PMN data card"), defs(w, h), _bg(w, h), chrome(w, h)]
    foot_lh = round(h * _FOOTER_H.get(FOOTER_LOGO, 0.050))

    if w/h > 1.30:                                   # ── landscape: 2 columns ──
        colL = round(w*0.45); gap = round(w*0.035)
        px = m + colL + gap; pw = w - m - px
        w_eff = round(pw/0.89)                       # so panel type sizes to its column
        _, gh = panel_fn(px, 0, pw, w_eff)
        gpy = max(round(h*0.16), round((h-gh)/2))
        panel, _ = panel_fn(px, gpy, pw, w_eff)
        ebs = round(w*0.032); hs = round(w*0.050)
        ql = []                                      # wrap long titles to the left column
        for ln in q_lines: ql += wrap(ln, hs, colL-round(w*0.015))
        n = len(ql)
        blk = ebs + round(hs*1.15) + (n-1)*round(hs*1.06)
        ttop = round(h*0.17) + max(0, (round(h*0.62)-blk)//2)
        out += [eyebrow(m, ttop+ebs, tag, size=ebs, color=THEME["eyebrow"])]
        out += [headline(m, ttop+ebs+round(hs*1.15), ql, size=hs, weight=800, color=THEME["title"])]
        out += [panel]
        if source:
            out += [body(w-m, h-m-round(ty(w_eff,"caption")*0.1), f"Source: {source}",
                         size=ty(w_eff,"caption"), weight=600, color=_src_color(), anchor="end")]
        out += [footer(w, h), svg_close()]
        return "".join(out)

    # ── square / portrait / vertical: stacked, centred ──
    ebs = ty(w,"eyebrow"); hs = round(w*hs_ratio)
    _, gh = panel_fn(m, 0, w-2*m, w)
    q_blk = ebs + round(hs*1.15) + (n-1)*round(hs*1.06) + round(hs*0.6)
    tp_gap = round(h*0.038)
    group = q_blk + tp_gap + gh
    zone_top = round(h*0.13); zone_bot = h - m - foot_lh - round(h*0.025)
    top = zone_top + max(0, (zone_bot - zone_top - group)//2)
    out += [eyebrow(m, top+ebs, tag, size=ebs, color=THEME["eyebrow"])]
    out += [headline(m, top+ebs+round(hs*1.15), q_lines, size=hs, weight=800, color=THEME["title"])]
    panel, _ = panel_fn(m, top+q_blk+tp_gap, w-2*m, w)
    out += [panel]
    if source:
        out += [body(w-m, h-m-round(ty(w,"caption")*0.1), f"Source: {source}",
                     size=ty(w,"caption"), weight=600, color=_src_color(), anchor="end")]
    out += [footer(w, h), svg_close()]
    return "".join(out)


# ── 1. binary market card ───────────────────────────────────────────────────
def card_binary(w, h, m_):
    outs = [("Yes", m_["yes"], UP), ("No", m_["no"], DOWN)]
    return card_shell(w, h, m_["tag"], m_["question"],
                      lambda x,y,pw,ww: outcome_panel(x,y,pw,ww,outs,m_.get("src","Polymarket")))


# ── 2. multi-outcome (up to 5) ──────────────────────────────────────────────
def card_multi(w, h, m_):
    outs = [(o[0], o[1], RANK[i % len(RANK)]) for i, o in enumerate(m_["outcomes"])]
    return card_shell(w, h, m_["tag"], m_["question"],
                      lambda x,y,pw,ww: outcome_panel(x,y,pw,ww,outs,m_.get("src","Polymarket")),
                      hs_ratio=0.046)


# ── 3. timeseries (odds over time) ──────────────────────────────────────────
def line_panel(x, y, pw, w, series, cur, delta, source="Polymarket"):
    pin = PADIN(w)
    lab_w = round(w*0.058)                       # dedicated y-axis label column
    head_h = round(w*0.085)                      # room for the current-value callout
    ph = round(pw*0.50)
    gh = ph + head_h
    out = [panel(x, y, pw, gh, w)]
    # current value + delta, top-left of the panel
    dcol_ = UP if delta>=0 else DOWN; arr_ = "▲" if delta>=0 else "▼"
    out += [f'<text x="{x+pin}" y="{y+pin+round(w*0.058)}" font-family="{F.sans}" '
            f'font-size="{round(w*0.060)}" font-weight="800" fill="{INK}">{cur}%</text>']
    out += [f'<text x="{x+pin+round(w*0.105)}" y="{y+pin+round(w*0.050)}" font-family="{F.sans}" '
            f'font-size="{round(w*0.024)}" font-weight="700" fill="{dcol_}">{arr_} {abs(delta)} pts</text>']
    plot_x = x+pin+lab_w; plot_y = y+pin+head_h
    plot_w = pw-2*pin-lab_w; plot_h = gh-pin-head_h-round(w*0.04)
    vals = [v for _, v in series]
    # gridlines + y labels (0..100) — labels live inside the panel, right-aligned
    for g in (0, 25, 50, 75, 100):
        gy = plot_y + plot_h*(1-g/100)
        out += [f'<line x1="{plot_x}" y1="{gy:.0f}" x2="{plot_x+plot_w}" y2="{gy:.0f}" '
                f'stroke="{INK}" stroke-opacity="0.10" stroke-width="1.5"/>']
        out += [body(plot_x-round(w*0.018), gy+round(ty(w,"caption")*0.35), f"{g}",
                     size=round(ty(w,"caption")*0.85), weight=600, color=MUTE, anchor="end")]
    n = len(series)
    def px(i): return plot_x + plot_w*i/(n-1)
    def py(v): return plot_y + plot_h*(1-v/100)
    pts = " ".join(f"{px(i):.1f},{py(v):.1f}" for i,(_,v) in enumerate(series))
    area = f"{plot_x},{plot_y+plot_h} " + pts + f" {plot_x+plot_w},{plot_y+plot_h}"
    out += [f'<defs><linearGradient id="area" x1="0" y1="0" x2="0" y2="1">'
            f'<stop offset="0" stop-color="{C.blue}" stop-opacity="0.28"/>'
            f'<stop offset="1" stop-color="{C.blue}" stop-opacity="0.02"/></linearGradient></defs>']
    out += [f'<polygon points="{area}" fill="url(#area)"/>']
    out += [f'<polyline points="{pts}" fill="none" stroke="{C.blue}" stroke-width="{max(3,round(w*0.004))}" '
            f'stroke-linejoin="round" stroke-linecap="round"/>']
    # end dot + current value
    ex, ey = px(n-1), py(series[-1][1])
    out += [f'<circle cx="{ex:.0f}" cy="{ey:.0f}" r="{round(w*0.008)}" fill="{C.blue}" stroke="#FFF" stroke-width="3"/>']
    # x labels (first / mid / last) just under the plot
    for i in (0, n//2, n-1):
        out += [body(px(i), plot_y+plot_h+round(ty(w,"caption")*1.5), series[i][0],
                     size=round(ty(w,"caption")*0.9), weight=600, color=MUTE,
                     anchor=("start" if i == 0 else "end" if i == n-1 else "middle"))]
    return "".join(out), gh

def card_timeseries(w, h, m_):
    series = m_["series"]; cur = series[-1][1]; delta = cur - series[0][1]
    return card_shell(w, h, m_["tag"], m_["question"],
                      lambda x,y,pw,ww: line_panel(x,y,pw,ww,series,cur,delta),
                      hs_ratio=0.050, source="Polymarket")


# ── 4. hero stat + quote ────────────────────────────────────────────────────
def card_hero_quote(w, h, q):
    m = M(w)
    out = [svg_open(w,h,"PMN hero quote"), defs(w,h), field(w,h), chrome(w,h)]
    out += [eyebrow(m, round(h*0.175), q["tag"], size=ty(w,"eyebrow"), color=THEME["eyebrow"])]
    qs = round(w*0.052)
    out += [f'<text x="{m-6}" y="{round(h*0.30)}" font-family="{F.serif}" font-size="{round(w*0.13)}" '
            f'font-weight="700" fill="{C.blue}">“</text>']
    qy = round(h*0.355)
    out += [serif_head(m, qy, q["lines"], size=qs, italic=True, color=THEME["title"])]
    by = qy + round(qs*1.18)*(len(q["lines"])-1) + round(h*0.06)
    out += [body(m, by, q["attrib"], size=ty(w,"lead"), weight=700, color=THEME["title"])]
    out += [body(m, by+round(ty(w,"caption")*1.35), q["sub"], size=ty(w,"caption"), weight=500, color=THEME["mute"])]
    # hero stat panel
    dcol = UP if q["dir"]==">" else DOWN; arr = "▲" if q["dir"]==">" else "▼"
    py = round(h*0.66); ph = round(h*0.20); pinr = PADIN(w)
    out += [panel(m, py, w-2*m, ph, w)]
    out += [eyebrow(m+pinr, py+pinr+round(ty(w,'eyebrow')*0.4), q["stat_label"], color=dcol, size=ty(w,"eyebrow"))]
    out += [f'<text x="{m+pinr}" y="{py+ph-pinr}" font-family="{F.sans}" font-size="{round(w*0.11)}" '
            f'font-weight="800" fill="{dcol}">{arr} {q["stat"]}</text>']
    out += [body(w-m-pinr, py+ph-pinr-round(w*0.005), q["stat_sub"], size=ty(w,"lead"),
                 weight=600, color=INK, anchor="end")]
    out += [footer(w,h), svg_close()]
    return "".join(out)


# ── 5. stacked area (odds share over time) ──────────────────────────────────
def legend(x, y, items, w):
    sw = round(w*0.020); fs = round(w*0.026); out = []; cx = x
    for lab, col in items:
        out += [f'<rect x="{cx}" y="{y-sw}" width="{sw}" height="{sw}" rx="3" fill="{col}"/>']
        out += [f'<text x="{cx+sw+round(w*0.008)}" y="{y-round(sw*0.12)}" font-family="{F.sans}" '
                f'font-size="{fs}" font-weight="600" fill="{INK}">{esc(lab)}</text>']
        cx += sw + round(w*0.008) + len(lab)*round(fs*0.54) + round(w*0.028)
    return "".join(out)

def _axes(x, y, pw, w, gh, lab_w, ymax, ylabels, source):
    pin = PADIN(w)
    plot_x = x+pin+lab_w; plot_top = y+pin+round(w*0.075)
    plot_w = pw-2*pin-lab_w; plot_h = gh-2*pin-round(w*0.115)
    out = []
    for g in ylabels:
        gy = plot_top + plot_h*(1-g/ymax)
        out += [f'<line x1="{plot_x}" y1="{gy:.0f}" x2="{plot_x+plot_w}" y2="{gy:.0f}" '
                f'stroke="{INK}" stroke-opacity="0.10" stroke-width="1.5"/>']
        out += [body(plot_x-round(w*0.018), gy+round(ty(w,"caption")*0.35), f"{g}",
                     size=round(ty(w,"caption")*0.82), weight=600, color=MUTE, anchor="end")]
    return out, plot_x, plot_top, plot_w, plot_h

def area_panel(x, y, pw, w, times, bands, source="Polymarket"):
    """Stacked-to-100 area. bands = [(name,color,values[])]. Returns (svg,h)."""
    pin = PADIN(w); lab_w = round(w*0.052); gh = round(pw*0.58)
    out = [panel(x, y, pw, gh, w)]
    ax, plot_x, plot_top, plot_w, plot_h = _axes(x, y, pw, w, gh, lab_w, 100, (0,25,50,75,100), source)
    n = len(times)
    px = lambda i: plot_x + plot_w*i/(n-1)
    py = lambda v: plot_top + plot_h*(1-v/100)
    cum = [0]*n
    areas = []
    for name, col, vals in bands:
        top = [cum[i]+vals[i] for i in range(n)]
        pts = [f"{px(i):.1f},{py(top[i]):.1f}" for i in range(n)] + \
              [f"{px(i):.1f},{py(cum[i]):.1f}" for i in reversed(range(n))]
        areas += [f'<polygon points="{" ".join(pts)}" fill="{col}" fill-opacity="0.88"/>']
        cum = top
    out += areas + ax
    for i in (0, n//2, n-1):
        out += [body(px(i), plot_top+plot_h+round(ty(w,"caption")*1.5), times[i],
                     size=round(ty(w,"caption")*0.9), weight=600, color=MUTE,
                     anchor=("start" if i==0 else "end" if i==n-1 else "middle"))]
    out += [legend(plot_x, y+pin+round(w*0.045), [(n_,c) for n_,c,_ in bands], w)]
    return "".join(out), gh


# ── 6. stacked bar (volume by category over time) ───────────────────────────
def stacked_bar_panel(x, y, pw, w, cats, segments, source="Polymarket", unit="$M"):
    """segments = [(name,color,values[] per cat)], absolute stacked. Returns (svg,h)."""
    pin = PADIN(w); lab_w = round(w*0.058); gh = round(pw*0.58)
    totals = [sum(s[2][i] for s in segments) for i in range(len(cats))]
    raw = max(totals); ymax = int((raw//10 + 1)*10)
    out = [panel(x, y, pw, gh, w)]
    ax, plot_x, plot_top, plot_w, plot_h = _axes(x, y, pw, w, gh, lab_w, ymax,
                                                 (0, ymax//2, ymax), source)
    out += ax
    bw = plot_w/len(cats)*0.62; step = plot_w/len(cats)
    for i, cat in enumerate(cats):
        bx = plot_x + step*i + (step-bw)/2
        base = 0
        for name, col, vals in segments:
            v = vals[i]; bh = plot_h*v/ymax
            by = plot_top + plot_h*(1-(base+v)/ymax)
            out += [f'<rect x="{bx:.1f}" y="{by:.1f}" width="{bw:.1f}" height="{bh:.1f}" fill="{col}"/>']
            base += v
        out += [body(bx+bw/2, plot_top+plot_h+round(ty(w,"caption")*1.5), cat,
                     size=round(ty(w,"caption")*0.9), weight=600, color=MUTE, anchor="middle")]
    out += [legend(plot_x, y+pin+round(w*0.045), [(n_,c) for n_,c,_ in segments], w)]
    return "".join(out), gh

def card_area(w, h, m_):
    return card_shell(w, h, m_["tag"], m_["question"],
                      lambda x,y,pw,ww: area_panel(x,y,pw,ww,m_["times"],m_["bands"]),
                      hs_ratio=0.048, source="Polymarket")
def card_stacked(w, h, m_):
    return card_shell(w, h, m_["tag"], m_["question"],
                      lambda x,y,pw,ww: stacked_bar_panel(x,y,pw,ww,m_["cats"],m_["segments"],unit=m_.get("unit","$M")),
                      hs_ratio=0.048, source="Polymarket")


# ── sample data ─────────────────────────────────────────────────────────────
BINARY = {"tag":"Live odds","question":["Fed cuts rates","before September?"],"yes":63,"no":37}
MULTI = {"tag":"Live odds · top 5","question":["2028 GOP","presidential nominee"],
         "outcomes":[("J.D. Vance",42),("Ron DeSantis",17),("Marco Rubio",11),
                     ("Nikki Haley",8),("Vivek Ramaswamy",6)]}
TS = {"tag":"Odds over time · 60d","question":["Fed cuts before September?"],
      "series":[("Apr",38),("",41),("",39),("May",46),("",52),("",49),("Jun",58),("Now",63)]}
HERO = {"tag":"The scorecard","lines":["ETH flips BTC","by end of year."],
        "attrib":"A guest","sub":"On another show · Jan 2026",
        "dir":"<","stat":"68%","stat_label":"ETH/BTC since the call","stat_sub":"as of Ep. 02"}
AREA = {"tag":"Odds share · 6 mo","question":["2028 GOP nominee —","how the field shifted"],
        "times":["Jan","Feb","Mar","Apr","May","Now"],
        "bands":[("Vance", "#2E5CFF", [22,26,31,35,39,42]),
                 ("DeSantis", "#16C784", [20,19,18,18,17,17]),
                 ("The field", "#5A6378", [58,55,51,47,44,41])]}
STACK = {"tag":"Volume by category · 6 wk","question":["Where the money","actually traded"],"unit":"$M",
         "cats":["W1","W2","W3","W4","W5","W6"],
         "segments":[("Politics","#2E5CFF",[31,38,44,52,61,73]),
                     ("Crypto","#16C784",[18,22,19,26,24,29]),
                     ("Sports","#4FB6FF",[12,14,17,15,21,19]),
                     ("Macro","#EFC23B",[8,9,11,10,13,14])]}

JOBS = [("01-binary", card_binary, BINARY), ("02-multi-5", card_multi, MULTI),
        ("03-timeseries", card_timeseries, TS), ("04-hero-quote", card_hero_quote, HERO),
        ("05-stacked-area", card_area, AREA), ("06-stacked-bar", card_stacked, STACK)]

if __name__ == "__main__":
    for name, fn, data in JOBS:
        open(f"{OUT}/{name}.svg","w").write(fn(1080,1080,data)); print("  ",name)
    print(f"\nwrote {len(JOBS)} data cards")
