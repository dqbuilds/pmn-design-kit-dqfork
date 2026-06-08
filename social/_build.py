#!/usr/bin/env python3
"""
PMN social templates — first batch.
Emits SVGs across platform sizes into ./exports.

Templates:
  guest-announce   — guest reveal, translucent-box treatment (the called-out one)
  episode-card     — new-episode drop
  quote            — pull-quote graphic
  market-card      — Polymarket data card

Run:  python3 _build.py
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "lib"))
import pmn
from pmn import (C, F, svg_open, svg_close, defs, field, chrome, photo_placeholder,
                 frosted_panel, blue_bar, glass_dark, panel, name_chip, eyebrow, headline,
                 serif_head, body, logo, logo_aspect, duration_stamp, block_lockup,
                 polymarket_presented, ty, wrap, M, PADIN, company_mark)

# dark-mode framework tokens (match the data cards)
PINK = C.white          # panel ink (text on the black panel)
PMUTE = C.muted         # panel muted

OUT = os.path.join(os.path.dirname(__file__), "exports")
os.makedirs(OUT, exist_ok=True)

# Final four (Kelvin, 2026-06-03). Wordmarks sign the cards; marks lead cover/avatar.
#   sans-news · bold-bar  = wordmarks   |   monogram · arrow-n = marks
FOOTER_LOGO = "pmn-wordmark"   # larger-format covers use the full show wordmark

# Platform size matrix
SIZES = {
    "1x1":   (1080, 1080),   # IG / X square
    "9x16":  (1080, 1920),   # Stories / Reels / Shorts
    "16x9":  (1920, 1080),   # X / YouTube
    "3x2":   (2048, 1365),   # X in-feed hero (compression-safe)
    "ythumb":(1280, 720),    # YouTube thumbnail
    "cover": (3000, 3000),   # Apple/Spotify podcast cover
    "avatar":(1024, 1024),   # profile / app icon
}


def aspect(w, h):
    r = w / h
    if r < 0.85:  return "vert"
    if r > 1.3:   return "wide"
    return "square"


# footer height per lockup — stacked/pictorial marks need more height to read
_FOOTER_H = {"monogram": 0.045, "sans-news": 0.050, "sans-stack": 0.050,
             "bold-bar": 0.072, "arrow-n": 0.090, "pmn-wordmark": 0.038}

def footer_sig(w, h, which=None, align="left"):
    """Real PMN lockup, bottom signature (Block already leads top-left).
    align='right' moves it clear of bottom-left content in 2-column layouts."""
    which = which or FOOTER_LOGO
    lh = round(h * _FOOTER_H.get(which, 0.050))
    x = M(w) if align == "left" else w - M(w)
    return logo(which, x, h - M(w) - lh + round(lh*0.15), lh, align=align, opacity=0.96)


def _guest_rs(w, ns):
    """Role size scales to the name so hierarchy holds at any name size."""
    return min(ty(w, "lead"), round(ns * 0.58))


def guest_id_height(w, name_size=None, label=True, compact=False):
    """Total height of a guest_id block from name top to logo bottom."""
    ns = name_size or ty(w, "display")
    rs, cs = _guest_rs(w, ns), ty(w, "caption")
    g = 0.78 if compact else 1.0
    h = round(ns*0.78) + round(rs*1.45)
    h += (round(cs*2.05*g) + round(cs*0.55)) if label else round(rs*1.30*g)
    return h + round(rs*1.12)


def guest_id(x, b, name, role, company, w, on_dark=True, name_size=None,
             label="Guest from", compact=False):
    """Name → role → company logo, stacked & left-aligned at x with first
    baseline at b. The company logo is the shareability hook (guest's employer).
    Returns (svg, bottom_y)."""
    ns = name_size or ty(w, "display")
    rs, cs = _guest_rs(w, ns), ty(w, "caption")
    g = 0.78 if compact else 1.0
    txt = C.white if on_dark else C.navy_deep
    sub = C.muted if on_dark else "#5A6488"
    out = [headline(x, b, name, size=ns, weight=800, color=txt)]
    b += round(rs * 1.45)
    out += [body(x, b, role, size=rs, weight=600, color=sub)]
    if label:
        b += round(cs * 2.05 * g)
        out += [eyebrow(x, b, label, color=C.eyebrow_ink, size=cs)]
        b += round(cs * 0.55)
    else:
        b += round(rs * 1.30 * g)
    ch = round(rs * 1.12)
    mark, _ = company_mark(company, x, b, ch, align="left", color=txt)
    out += [mark]
    return "".join(out), b + ch


# ---------------------------------------------------------------------------
def guest_announce(w, h, g):
    a = aspect(w, h)
    m, pin = M(w), PADIN(w)
    out = [svg_open(w, h, "PMN guest announce"), defs(w, h), field(w, h)]

    if a == "wide":
        pw = round(w*0.36); px = w - m - pw
        py = round(h*0.135); ph = h - 2*py
        out += [photo_placeholder(px, py, pw, ph, tone=1)]
        out += [chrome(w, h)]
        # left block (eyebrow + name + role + company), vertically centred in the
        # chrome→footer zone so the company logo never collides with the footer.
        ebs = ty(w,"eyebrow"); nsz = round(w*0.058)
        blk_h = ebs + round(ebs*0.9) + guest_id_height(w, name_size=nsz)
        zt, zb = round(h*0.18), round(h*0.86)
        top = zt + max(0, (zb - zt - blk_h)//2)
        out += [eyebrow(m, top + ebs, "On the next episode", size=ebs)]
        nb = top + ebs + round(ebs*0.9) + round(nsz*0.78)
        sid, _ = guest_id(m, nb, g["name"], g["title"], g["company"], w, name_size=nsz)
        out += [sid]
        out += [footer_sig(w, h, align="right"), svg_close()]
        return "".join(out)
    else:
        vert = a == "vert"
        out += [chrome(w, h)]
        out += [eyebrow(m, round(h * (0.135 if vert else 0.165)),
                        "On the next episode", size=ty(w,"eyebrow"))]
        py = round(h * (0.175 if vert else 0.21))
        ph = round(h * (0.40 if vert else 0.32))
        out += [photo_placeholder(m, py, w-2*m, ph, tone=1)]
        base = py + ph + round(ty(w,"display") * 0.92)
        sid, sid_bot = guest_id(m, base, g["name"], g["title"], g["company"], w)
        out += [sid]
        if vert:  # vertical has room for the value-prop panel
            lines = wrap(g["known"], ty(w,"lead"), w-2*m-2*pin)
            fy = sid_bot + round(h*0.03)
            fh = pin + ty(w,"eyebrow") + round(ty(w,"lead")*0.4) + \
                 len(lines)*round(ty(w,"lead")*1.18) + pin
            out += [panel(m, fy, w-2*m, fh, canvas_w=w)]
            out += [eyebrow(m+pin, fy+pin+ty(w,"eyebrow")*0.4, "Known for",
                            color=C.eyebrow_ink, size=ty(w,"eyebrow"))]
            ly = fy+pin+ty(w,"eyebrow")+round(ty(w,"lead")*0.5)
            for i, ln in enumerate(lines):
                out += [body(m+pin, ly+round(ty(w,"lead")*1.18)*i, ln,
                             size=ty(w,"lead"), weight=700, color=PINK)]

    out += [footer_sig(w, h), svg_close()]
    return "".join(out)


# ---------------------------------------------------------------------------
def guest_panel(x, y, pw, w, name, role, company, nsz=None, label="With"):
    """Glass panel: label + name + role + company logo. Returns (svg, height)."""
    pin = PADIN(w)
    cs = ty(w,"caption")
    nsz = nsz or round(w*0.046)
    rs = _guest_rs(w, nsz)
    ch = round(rs*1.12)
    y_lab  = pin + cs
    y_name = y_lab + round(cs*0.95) + round(nsz*0.82)
    y_bot  = y_name + round(rs*1.45) + round(rs*1.30) + ch
    gh = y_bot + pin
    out = [panel(x, y, pw, gh, canvas_w=w),
           eyebrow(x+pin, y+y_lab, label, color=C.eyebrow_ink, size=cs)]
    sid, _ = guest_id(x+pin, y+y_name, name, role, company, w, name_size=nsz, label=None)
    out.append(sid)
    return "".join(out), gh


def episode_card(w, h, ep):
    a = aspect(w, h)
    m, pin = M(w), PADIN(w)
    out = [svg_open(w, h, "PMN episode card"), defs(w, h), field(w, h), chrome(w, h)]
    ebs = ty(w,"eyebrow")

    if a == "wide":  # two columns: title left, guest panel right (both centred)
        colL = round(w*0.50)
        px = m + colL + round(w*0.04); pw = w - m - px
        nsz = round(w*0.034)
        _, gh = guest_panel(px, 0, pw, w, ep["guest"], ep["guest_title"],
                            ep["company"], nsz=nsz)
        gpy = round((h - gh)/2)
        panel, _ = guest_panel(px, gpy, pw, w, ep["guest"], ep["guest_title"],
                               ep["company"], nsz=nsz)
        hs = round(w*0.044); n = len(ep["title"])
        blk = ebs + round(hs*1.15) + (n-1)*round(hs*1.06) + round(hs*0.6)
        top = round(h*0.16) + max(0, (round(h*0.70) - blk)//2)
        out += [eyebrow(m, top+ebs, f"Episode {ep['num']} · {ep['date']}", size=ebs)]
        hy = top + ebs + round(hs*1.15)
        out += [headline(m, hy, ep["title"], size=hs, weight=800)]
        out += [blue_bar(m, hy + (n-1)*round(hs*1.06) + round(hs*0.45),
                         round(w*0.06), 12)]
        out += [panel]
        out += [footer_sig(w, h, align="left"), svg_close()]
        return "".join(out)

    # square / vert: stacked, balanced
    hs = round(w*0.066)
    nsz = round(w*0.046)
    _, gh = guest_panel(m, 0, w-2*m, w, ep["guest"], ep["guest_title"],
                        ep["company"], nsz=nsz)
    n = len(ep["title"])
    title_blk = ebs + round(hs*1.15) + (n-1)*round(hs*1.06) + round(hs*0.9)
    # centre [title + gap + panel] as one group between chrome and footer
    group_h = title_blk + round(h*0.05) + gh
    top = round(h*0.155) + max(0, (round(h*0.70) - group_h)//2)
    out += [eyebrow(m, top+ebs, f"Episode {ep['num']} · {ep['date']}", size=ebs)]
    hy = top + ebs + round(hs*1.15)
    out += [headline(m, hy, ep["title"], size=hs, weight=800)]
    out += [blue_bar(m, hy + (n-1)*round(hs*1.06) + round(hs*0.5), round(w*0.06), 12)]
    panel, _ = guest_panel(m, top + title_blk + round(h*0.05), w-2*m, w,
                           ep["guest"], ep["guest_title"], ep["company"], nsz=nsz)
    out += [panel, footer_sig(w, h), svg_close()]
    return "".join(out)


# ---------------------------------------------------------------------------
def quote(w, h, q):
    a = aspect(w, h)
    m = M(w)
    out = [svg_open(w, h, "PMN quote"), defs(w, h), field(w, h), chrome(w, h)]
    qs = {"wide": round(w*0.046), "square": round(w*0.058),
          "vert": round(w*0.066)}[a]
    rs, cs = ty(w,"lead"), ty(w,"caption")
    # measure the block (quote mark + lines + attribution + company) and centre it
    # in the zone between the chrome and the footer signature.
    qmark_h = round(qs*1.1)
    block_h = qmark_h + round(qs*1.18)*len(q["lines"]) + round(h*0.05) + \
              round(rs*1.4) + round(cs*1.3) + round(rs*1.2)
    zone_top, zone_bot = round(h*0.13), round(h*0.87)
    top = zone_top + max(0, (zone_bot - zone_top - block_h)//2)
    out += [f'<text x="{m-6}" y="{top+qmark_h*0.85:.0f}" font-family="{F.serif}" '
            f'font-size="{round(w*0.15)}" font-weight="700" fill="{C.blue}">“</text>']
    qy = top + qmark_h + round(qs*0.7)
    out += [serif_head(m, qy, q["lines"], size=qs, italic=True, color=C.white)]
    by = qy + round(qs*1.18)*(len(q["lines"])-1) + round(h*0.075)
    out += [blue_bar(m, by, round(w*0.08), 12)]
    by += round(rs*1.05)
    out += [body(m, by, q["attrib"], size=rs, weight=700, color=C.white)]
    by += round(cs*1.25)
    out += [body(m, by, q["role"], size=cs, weight=500, color=C.muted)]
    # company logo — shareability hook
    mark, _ = company_mark(q["company"], m, by + round(cs*0.55), round(rs*1.05),
                           align="left")
    out += [mark]
    out += [footer_sig(w, h), svg_close()]
    return "".join(out)


# ---------------------------------------------------------------------------
def odds_panel(x, y, pw, w, m_):
    """Frosted odds panel — thin full-width bars with name + % on the line above
    (clear proportions; no stubby pills). Returns (svg, height)."""
    pin = PADIN(w)
    nsz, psz = ty(w,"lead"), round(w*0.032)
    cs = ty(w,"caption"); barh = round(w*0.016)
    gap_nb = round(nsz*0.42)
    row_h = nsz + gap_nb + barh + round(w*0.028)
    gh = pin + 2*row_h + round(cs*1.9) + round(pin*0.4)
    inner = pw - 2*pin
    out = [panel(x, y, pw, gh, canvas_w=w)]
    yy = y + pin
    for lab, pct, col in [("Yes", m_["yes"], C.up), ("No", m_["no"], C.down)]:
        out += [body(x+pin, yy+nsz*0.82, lab, size=nsz, weight=700, color=PINK)]
        out += [body(x+pw-pin, yy+nsz*0.82, f"{pct}%", size=psz, weight=800, color=PINK, anchor="end")]
        bary = yy + nsz + gap_nb
        out += [f'<rect x="{x+pin}" y="{bary}" width="{inner}" height="{barh}" rx="{barh//2}" '
                f'fill="#FFFFFF" fill-opacity="0.12"/>']
        out += [f'<rect x="{x+pin}" y="{bary}" width="{round(inner*pct/100)}" height="{barh}" '
                f'rx="{barh//2}" fill="{col}"/>']
        yy += row_h
    out += [body(x+pin, y+gh-pin+round(cs*0.3), "Source: Polymarket",
                 size=cs, weight=600, color=PMUTE)]
    return "".join(out), gh


def market_card(w, h, m_):
    a = aspect(w, h)
    m, pin = M(w), PADIN(w)
    out = [svg_open(w, h, "PMN market card"), defs(w, h), field(w, h), chrome(w, h)]
    ebs = ty(w,"eyebrow"); hs = round(w*0.052)
    n = len(m_["question"])

    if a == "wide":  # question left, odds panel right (both centred)
        colL = round(w*0.46)
        px = m + colL + round(w*0.04); pw = w - m - px
        _, gh = odds_panel(px, 0, pw, w, m_)
        opy = round((h - gh)/2)
        panel, _ = odds_panel(px, opy, pw, w, m_)
        blk = ebs + round(hs*1.15) + (n-1)*round(hs*1.06)
        top = round(h*0.16) + max(0, (round(h*0.70) - blk)//2)
        out += [eyebrow(m, top+ebs, m_["tag"], size=ebs)]
        out += [headline(m, top+ebs+round(hs*1.15), m_["question"], size=hs, weight=800)]
        out += [panel, footer_sig(w, h, align="left"), svg_close()]
        return "".join(out)

    # square: centre [question + gap + panel] as one group
    _, gh = odds_panel(m, 0, w-2*m, w, m_)
    q_blk = ebs + round(hs*1.15) + (n-1)*round(hs*1.06) + round(hs*0.6)
    group_h = q_blk + round(h*0.05) + gh
    top = round(h*0.155) + max(0, (round(h*0.70) - group_h)//2)
    out += [eyebrow(m, top+ebs, m_["tag"], size=ebs)]
    out += [headline(m, top+ebs+round(hs*1.15), m_["question"], size=hs, weight=800)]
    panel, _ = odds_panel(m, top + q_blk + round(h*0.05), w-2*m, w, m_)
    out += [panel, footer_sig(w, h), svg_close()]
    return "".join(out)


# ---------------------------------------------------------------------------
def podcast_cover(w, h, mark="arrow-n"):
    """Square show cover — the PMN mark leads (covers are where the show
    wordmark is primary). Block + Polymarket sit as endorsement at the base."""
    out = [svg_open(w, h, "PMN podcast cover"), defs(w, h), field(w, h)]
    # subtle top eyebrow
    out += [eyebrow(w/2, round(h*0.165), "The Block original", color=C.muted,
                    size=round(w*0.018), anchor="middle")]
    # centred hero mark — wordmark/monogram sized by width, pictorial by height
    if mark == "pmn-wordmark":
        mw = round(w*0.82); mh = round(mw / pmn.show_wordmark_aspect())
    elif mark == "monogram":
        mw = round(w*0.46); mh = round(mw / logo_aspect("monogram"))
    else:  # arrow-n pictorial
        mh = round(h*0.42)
    out += [logo(mark, w/2, round(h*0.45) - mh//2, mh, align="center")]
    # base endorsement row: [The Block]  |  [Polymarket]  — centred, measured
    by = round(h*0.875)
    bh = round(w*0.026)
    block_aspect = 656/100
    poly_aspect  = 911/168
    bw = bh * block_aspect
    ph = bh
    pw = ph * poly_aspect
    gap = round(w*0.045)
    total = bw + gap + pw
    sx = w/2 - total/2
    out += [block_lockup(sx, by, h=bh)]
    divx = sx + bw + gap/2
    out += [f'<line x1="{divx}" y1="{by-2}" x2="{divx}" y2="{by+bh}" '
            f'stroke="{C.white}" stroke-opacity="0.28" stroke-width="2"/>']
    out += [polymarket_presented(sx + bw + gap + pw, by, h=ph, label=False)]
    out += [svg_close()]
    return "".join(out)


def avatar(w, h, mark="monogram"):
    """Profile / app icon — dark navy with a blue centre-glow so the electric
    mark pops (blue-on-blue fails). Mark centred."""
    out = [svg_open(w, h, "PMN avatar"),
           f'<defs><radialGradient id="avg" cx="0.5" cy="0.46" r="0.72">'
           f'<stop offset="0" stop-color="#16245A"/>'
           f'<stop offset="1" stop-color="{C.navy_deep}"/></radialGradient></defs>',
           f'<rect width="{w}" height="{h}" fill="url(#avg)"/>']
    if mark == "monogram":
        out += [logo(mark, w/2, round(h*0.42), round(h*0.16), align="center")]
    else:  # arrow-n pictorial + wordmark
        out += [logo(mark, w/2, round(h*0.26), round(h*0.48), align="center")]
    out += [svg_close()]
    return "".join(out)


# ---------------------------------------------------------------------------
# Sample launch-episode content (placeholder until real episode drops)
GUEST = {"name": "Shayne Coplan", "role": "Guest", "title": "Founder & CEO",
         "company": "Polymarket", "known": "Built the largest prediction market on-chain"}
# second sample — a non-sponsor guest, to show the company slot is generic
GUEST2 = {"name": "Tarek Mansour", "role": "Guest", "title": "Co-founder & CEO",
          "company": "Kalshi", "known": "Built the first regulated US event exchange"}
EP = {"num": "01", "date": "Launch", "title": ["Why prediction", "markets are the", "new price feed"],
      "guest": "Shayne Coplan", "guest_title": "Founder & CEO", "company": "Polymarket"}
QUOTE = {"lines": ["The market isn't", "predicting the future.", "It's pricing it."],
         "attrib": "Shayne Coplan", "role": "Founder & CEO · Episode 01", "company": "Polymarket"}
MARKET = {"tag": "Priced In · Live odds", "question": ["Fed cuts rates", "before September?"],
          "yes": 63, "no": 37}

JOBS = [
    ("guest-announce",      guest_announce, GUEST,  ["1x1", "9x16", "16x9"]),
    ("guest-announce-alt",  guest_announce, GUEST2, ["1x1"]),
    ("episode-card",        episode_card,   EP,     ["1x1", "16x9", "3x2"]),
    ("quote",               quote,          QUOTE,  ["1x1", "9x16"]),
    ("market-card",         market_card,    MARKET, ["1x1", "16x9"]),
]
# mark-led assets (one arg = the chosen mark)
MARK_JOBS = [
    ("podcast-cover", podcast_cover, "arrow-n",  ["cover"]),
    ("avatar-mono",   avatar,        "monogram", ["avatar"]),
    ("avatar-arrow",  avatar,        "arrow-n",  ["avatar"]),
]

if __name__ == "__main__":
    n = 0
    for name, fn, data, sizes in JOBS:
        for sz in sizes:
            w, h = SIZES[sz]
            with open(os.path.join(OUT, f"{name}--{sz}.svg"), "w") as f:
                f.write(fn(w, h, data))
            n += 1
            print(f"  {name}--{sz}.svg  ({w}x{h})")
    for name, fn, mark, sizes in MARK_JOBS:
        for sz in sizes:
            w, h = SIZES[sz]
            with open(os.path.join(OUT, f"{name}--{sz}.svg"), "w") as f:
                f.write(fn(w, h, mark))
            n += 1
            print(f"  {name}--{sz}.svg  ({w}x{h})")
    print(f"\n{n} templates written to exports/")
