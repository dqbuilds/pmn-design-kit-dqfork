#!/usr/bin/env python3
"""
Episode 01 — guest: intern (CMO, RoboStrategy).
Five example layouts using his PFP two ways:
  (a) masked + blended into the background field
  (b) placed inside the photo boxes
White text over photo carries a soft black glow for legibility; we measure the
underlying WCAG contrast and report it (Adobe-style check).

Run:  python3 _build.py
"""
import sys, os, base64, io
HERE = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(HERE, "..", "lib"))
sys.path.insert(0, os.path.join(HERE, "..", "social"))
import numpy as np
from PIL import Image
import pmn
from pmn import (C, F, svg_open, svg_close, defs, chrome, eyebrow, headline, body,
                 serif_head, blue_bar, glass_dark, frosted_panel, ty, M, PADIN, logo)

A = os.path.join(HERE, "assets")
OUT = os.path.join(HERE, "exports")
os.makedirs(OUT, exist_ok=True)

DISC   = Image.open(f"{A}/intern-disc.png").convert("RGBA")     # penguin, no ring (blends)
CIRCLE = Image.open(f"{A}/intern-circle.png").convert("RGBA")   # penguin, ring
BOXIMG = Image.open(f"{A}/intern-box.png").convert("RGB")       # penguin square fill
PHOTO  = Image.open(f"{A}/intern-photo.png").convert("RGB")     # REAL portrait (box)
FACE   = Image.open(f"{A}/intern-face-circle.png").convert("RGBA")  # REAL face, circle
BANNER = Image.open(f"{A}/banner.png").convert("RGB")           # REAL studio banner
ROBO   = Image.open(f"{A}/robostrategy-icon.png").convert("RGBA")

# ── episode data ──────────────────────────────────────────────────────────
G = {
    "name": "Kevin McCordic", "handle": "@intern", "title": "CMO",
    "company": "RoboStrategy",
    "prev": "Prev: growth lead at Monad · venture at CMS Holdings",
    "quote": ["Crypto's smartest", "capital already", "left for robots."],   # placeholder — swap for a real pull quote post-record
}

SIZES = {"1x1": (1080,1080), "9x16": (1080,1920), "16x9": (1920,1080)}


# ── helpers ────────────────────────────────────────────────────────────────
def b64(img):
    buf = io.BytesIO(); img.save(buf, "PNG")
    return base64.b64encode(buf.getvalue()).decode()


def img_tag(img, x, y, w, h, rx=0, clip_id=None, par="xMidYMid"):
    s = (f'<image x="{x:.0f}" y="{y:.0f}" width="{w:.0f}" height="{h:.0f}" '
         f'preserveAspectRatio="{par} slice" '
         f'xlink:href="data:image/png;base64,{b64(img)}"')
    if rx:
        cid = clip_id or f"clip{int(x)}{int(y)}"
        return (f'<clipPath id="{cid}"><rect x="{x:.0f}" y="{y:.0f}" width="{w:.0f}" '
                f'height="{h:.0f}" rx="{rx}"/></clipPath>'
                f'{s} clip-path="url(#{cid})"/>')
    return s + "/>"


def field_pil(W, H):
    yy, xx = np.mgrid[0:H, 0:W]
    t = (xx / W + yy / H) / 2
    A0, B0, C0 = np.array([5,6,13]), np.array([16,32,79]), np.array([46,92,255])
    a1 = np.clip(t/0.55, 0, 1)[..., None]
    a2 = np.clip((t-0.55)/0.45, 0, 1)[..., None]
    seg1 = A0 + (B0 - A0)*a1
    seg2 = B0 + (C0 - B0)*a2
    res = np.where((t < 0.55)[..., None], seg1, seg2).astype("uint8")
    return Image.fromarray(res, "RGB")


# ── team backgrounds as PIL (so the PFP mask can blend into ANY field) ───────
# Mirror the SVG team backgrounds in pmn: black→#2E5CFF diagonal, near-black
# solid, black + blue top glow. House = the broadcast diagonal above.
BG_STYLE = "house"        # house | team-gradient | team-solid | team-glow

def bg_pil(W, H, style=None):
    style = style or BG_STYLE
    if style == "team-solid":
        return Image.new("RGB", (W, H), (17, 17, 17))
    if style == "team-gradient":
        yy, xx = np.mgrid[0:H, 0:W]
        t = ((xx / W + yy / H) / 2)[..., None]
        res = (np.array([0, 0, 0]) + np.array([46, 92, 255]) * t).astype("uint8")
        return Image.fromarray(res, "RGB")
    if style == "team-glow":
        yy, xx = np.mgrid[0:H, 0:W]
        cx, cy, r = W*0.5, H*0.02, max(W, H)*0.85
        dist = np.sqrt((xx-cx)**2 + (yy-cy)**2) / r
        a = (np.clip((0.55 - dist)/0.55, 0, 1) * 0.40)[..., None]
        res = (np.array([46, 92, 255]) * a).astype("uint8")     # over black
        return Image.fromarray(res, "RGB")
    return field_pil(W, H)


def blend_bg(W, H, strength=0.62, ramp_start=0.32, ramp_end=0.78,
             pos="right", scrim=None, scrim_strength=0.72):
    """Field gradient with the PFP disc masked + faded in. pos='right' fades
    horizontally (text on the left); pos='top' centres the disc up high.
    scrim='bottom'/'left' lays a dark gradient so text stays legible."""
    bg = bg_pil(W, H).convert("RGBA")
    if pos == "top":
        ds = int(min(W*1.1, H*0.92)); x = (W-ds)//2; y = -int(ds*0.08)
    else:
        ds = int(H*1.3); x = W - int(ds*0.58); y = (H-ds)//2
    d = DISC.resize((ds, ds)).convert("RGBA")
    canvas_alpha = Image.new("L", (W, H), 0)
    canvas_alpha.paste(d.split()[3], (x, y))
    if pos == "top":
        yy = np.tile(np.linspace(0, 1, H), (W, 1)).T
        fade = np.clip((0.78 - yy)/0.5, 0, 1) * 255 * strength      # fade out lower
    else:
        grad = np.tile(np.linspace(0, 1, W), (H, 1))
        fade = np.clip((grad - ramp_start)/(ramp_end - ramp_start), 0, 1) * 255 * strength
    comb = np.minimum(np.array(canvas_alpha), fade.astype("uint8")).astype("uint8")
    disc_canvas = Image.new("RGBA", (W, H), (0,0,0,0))
    disc_canvas.paste(d, (x, y)); disc_canvas.putalpha(Image.fromarray(comb))
    bg = Image.alpha_composite(bg, disc_canvas)
    if scrim == "bottom":
        yy = np.tile(np.linspace(0, 1, H), (W, 1)).T
        sc = (np.clip((yy - 0.30)/0.7, 0, 1)**1.3 * 255 * scrim_strength).astype("uint8")
        black = Image.new("RGBA", (W, H), (0,0,0,0)); black.putalpha(Image.fromarray(sc))
        bg = Image.alpha_composite(bg, black)
    elif scrim == "left":
        xx = np.tile(np.linspace(0, 1, W), (H, 1))
        sc = (np.clip((0.62 - xx)/0.62, 0, 1)**1.2 * 255 * scrim_strength).astype("uint8")
        black = Image.new("RGBA", (W, H), (0,0,0,0)); black.putalpha(Image.fromarray(sc))
        bg = Image.alpha_composite(bg, black)
    return bg.convert("RGB")


def robostrategy(x, y, h, on_dark=True, anchor="left"):
    """[ ] icon + 'RoboStrategy' wordmark. Returns (svg, width)."""
    col = "#FFFFFF" if on_dark else C.navy_deep
    iw = h * (ROBO.width / ROBO.height)
    gap = h * 0.45
    label = "RoboStrategy"
    tw = len(label) * h * 0.55
    total = iw + gap + tw
    if anchor == "right":
        x -= total
    out = (f'<image x="{x:.0f}" y="{y:.0f}" width="{iw:.0f}" height="{h:.0f}" '
           f'xlink:href="data:image/png;base64,{b64(ROBO)}"/>'
           f'<text x="{x+iw+gap:.0f}" y="{y+h*0.80:.0f}" font-family="{F.sans}" '
           f'font-size="{h*0.92:.0f}" font-weight="800" letter-spacing="-0.5" '
           f'fill="{col}">{label}</text>')
    return out, total


def glow_defs(w):
    sd = max(5, round(w*0.006))
    return (f'<filter id="tglow" x="-40%" y="-40%" width="180%" height="180%">'
            f'<feDropShadow dx="0" dy="0" stdDeviation="{sd}" flood-color="#000000" '
            f'flood-opacity="0.55"/>'
            f'<feDropShadow dx="0" dy="0" stdDeviation="{sd*2}" flood-color="#000000" '
            f'flood-opacity="0.35"/></filter>')


def G_(inner):  # wrap in glow
    return f'<g filter="url(#tglow)">{inner}</g>'


# ── contrast measurement (WCAG) ─────────────────────────────────────────────
def _lin(c):
    c = c/255
    return c/12.92 if c <= 0.03928 else ((c+0.055)/1.055)**2.4
def rel_lum(rgb): return 0.2126*_lin(rgb[0])+0.7152*_lin(rgb[1])+0.0722*_lin(rgb[2])
def contrast(c1, c2):
    L1, L2 = rel_lum(c1), rel_lum(c2)
    hi, lo = max(L1, L2), min(L1, L2)
    return (hi+0.05)/(lo+0.05)

REPORT = []
def check(bg_img, name, region, fg=(255,255,255), large=True):
    """region=(x0,y0,x1,y1) in px on the rendered bg. Reports worst-case contrast."""
    x0,y0,x1,y1 = [int(v) for v in region]
    crop = np.array(bg_img.convert("RGB"))[max(0,y0):y1, max(0,x0):x1].reshape(-1,3)
    if len(crop)==0: return
    # worst case = brightest background pixel under the text
    bright = crop[np.argmax(crop.sum(1))]
    mean = crop.mean(0)
    cw = contrast(fg, bright); cm = contrast(fg, mean)
    need = 3.0 if large else 4.5
    REPORT.append((name, round(cm,1), round(cw,1), need,
                   "PASS" if cw>=need else ("glow-needed" if cm>=need else "FAIL")))


def footer(w, h, align="left"):
    lh = round(h*0.05); x = M(w) if align == "left" else w - M(w)
    return logo("sans-news", x, h-M(w)-lh+round(lh*0.15), lh, align=align, opacity=0.96)


def guest_text_block(w, x, top, glow=True):
    """eyebrow + name + handle + role + GUEST FROM RoboStrategy. Returns svg."""
    ebs, ns = ty(w,"eyebrow"), round(w*0.092)
    rs, cs = round(ns*0.40), ty(w,"caption")
    wrap = G_ if glow else (lambda s: s)
    b = top + ebs
    out = [wrap(eyebrow(x, b, "On the next episode", size=ebs))]
    b += round(ns*0.95)
    out += [wrap(headline(x, b, G["name"], size=ns, weight=800))]
    b += round(rs*1.15)
    out += [wrap(body(x, b, G["handle"] + "  ·  " + G["title"], size=rs, weight=600, color="#C8D2F0"))]
    b += round(cs*2.0)
    out += [wrap(eyebrow(x, b, "Guest from", color=C.eyebrow_ink, size=cs))]
    b += round(cs*0.5)
    robo, _ = robostrategy(x, b, round(rs*1.05))
    out += [wrap(robo)]
    return "".join(out), b + round(rs*1.05)


# 1) guest 1:1 — PFP blended into background --------------------------------
def g1_guest_blend(key="g1"):
    w, h = SIZES["1x1"]; bg = blend_bg(w, h)
    svg = [svg_open(w,h,"ep01 guest blend"), "<defs>"+glow_defs(w)+"</defs>",
           img_tag(bg,0,0,w,h), G_(chrome(w,h))]
    blk, _ = guest_text_block(w, M(w), round(h*0.30))
    svg += [blk, footer(w,h), svg_close()]
    check(bg, key+" name", (M(w), round(h*0.36), round(w*0.62), round(h*0.46)))
    return "".join(svg)


# 2) guest 1:1 — REAL photo inside the box -----------------------------------
def g2_guest_box(key="g2"):
    w, h = SIZES["1x1"]; m = M(w)
    bg = bg_pil(w, h)
    svg = [svg_open(w,h,"ep01 guest box"), defs(w,h), img_tag(bg,0,0,w,h), chrome(w,h)]
    svg += [eyebrow(m, round(h*0.165), "On the next episode", size=ty(w,"eyebrow"))]
    py, ph = round(h*0.205), round(h*0.46)
    svg += [img_tag(PHOTO, m, py, w-2*m, ph, rx=24, par="xMidYMin")]
    ns = round(w*0.082); rs = round(ns*0.42); cs = ty(w,"caption")
    b = py+ph+round(ns*0.82)
    svg += [headline(m, b, G["name"], size=ns, weight=800)]
    svg += [body(m, b+round(rs*1.15), G["handle"]+"  ·  "+G["title"], size=rs, weight=600, color="#C8D2F0")]
    b += round(rs*1.15)+round(cs*2.0)
    svg += [eyebrow(m, b, "Guest from", color=C.eyebrow_ink, size=cs)]
    robo,_ = robostrategy(m, b+round(cs*0.5), round(rs*1.0)); svg += [robo]
    svg += [footer(w,h), svg_close()]
    return "".join(svg)


# 3) quote 1:1 — PFP blended background --------------------------------------
def q1_quote_blend(key="q1"):
    w, h = SIZES["1x1"]; m = M(w)
    bg = blend_bg(w, h, strength=0.5)
    svg = [svg_open(w,h,"ep01 quote blend"), "<defs>"+glow_defs(w)+"</defs>",
           img_tag(bg,0,0,w,h), G_(chrome(w,h))]
    qs = round(w*0.058); rs = ty(w,"lead"); cs = ty(w,"caption")
    top = round(h*0.30)
    svg += [G_(f'<text x="{m-6}" y="{top}" font-family="{F.serif}" font-size="{round(w*0.15)}" '
               f'font-weight="700" fill="{C.blue}">“</text>')]
    qy = top + round(qs*1.1)
    svg += [G_(serif_head(m, qy, G["quote"], size=qs, italic=True, color=C.white))]
    by = qy + round(qs*1.18)*(len(G["quote"])-1) + round(h*0.085)
    svg += [blue_bar(m, by, round(w*0.08), 12)]
    by += round(rs*1.05)
    svg += [G_(body(m, by, G["name"]+", "+G["title"], size=rs, weight=700, color=C.white))]
    robo,_ = robostrategy(m, by+round(cs*0.7), round(rs*0.95)); svg += [G_(robo)]
    svg += [footer(w,h), svg_close()]
    check(bg, key+" quote", (m, top, round(w*0.66), qy+round(qs*1.18)*len(G["quote"])))
    return "".join(svg)


# 4) episode 16:9 — PFP (circle) inside the WITH panel -----------------------
def e1_episode_box(key="e1"):
    w, h = SIZES["16x9"]; m, pin = M(w), PADIN(w)
    bg = bg_pil(w, h)
    svg = [svg_open(w,h,"ep01 episode box"), defs(w,h), img_tag(bg,0,0,w,h), chrome(w,h)]
    ebs = ty(w,"eyebrow"); hs = round(w*0.044)
    title = ["Crypto's capital", "left for robots"]
    # left column title, centred
    blk = ebs + round(hs*1.15) + (len(title)-1)*round(hs*1.06)
    top = round(h*0.16) + max(0, (round(h*0.70)-blk)//2)
    svg += [eyebrow(m, top+ebs, "Episode 01 · Launch", size=ebs)]
    svg += [headline(m, top+ebs+round(hs*1.15), title, size=hs, weight=800)]
    svg += [blue_bar(m, top+ebs+round(hs*1.15)+(len(title)-1)*round(hs*1.06)+round(hs*0.45), round(w*0.06), 12)]
    # right glass panel: circular PFP + WITH + name + role + company
    pw = round(w*0.40); px = w - m - pw
    cs, rs = ty(w,"caption"), round(w*0.030)
    av = round(h*0.26)
    gh = pin + av + round(rs*1.5) + round(rs*1.3) + round(rs*1.0) + round(rs*1.2) + pin
    gy = round((h-gh)/2)
    svg += [pmn.panel(px, gy, pw, gh, canvas_w=w)]     # soft-textured panel (standard)
    svg += [img_tag(FACE, px+pin, gy+pin, av, av)]
    tx = px+pin+av+round(pin*0.9); ty0 = gy+pin+round(av*0.42)
    svg += [eyebrow(tx, ty0, "With", color=C.eyebrow_ink, size=cs)]
    svg += [headline(tx, ty0+round(rs*1.25), G["name"], size=rs, weight=800)]
    svg += [body(tx, ty0+round(rs*1.25)+round(rs*1.0), G["handle"]+" · "+G["title"], size=round(rs*0.6), weight=600, color="#9AA6C9")]
    robo,_ = robostrategy(px+pin, gy+gh-pin-round(rs*0.7), round(rs*0.75)); svg += [robo]
    svg += [footer(w,h,align="left"), svg_close()]
    return "".join(svg)


# 5) guest 9:16 — PFP blended background -------------------------------------
def g3_guest_blend_vert(key="g3"):
    w, h = SIZES["9x16"]; m = M(w)
    bg = blend_bg(w, h, strength=0.85, pos="top", scrim="bottom", scrim_strength=0.78)
    svg = [svg_open(w,h,"ep01 guest blend vert"), "<defs>"+glow_defs(w)+"</defs>",
           img_tag(bg,0,0,w,h), G_(chrome(w,h))]
    ns = round(w*0.105); rs = round(ns*0.34); cs = ty(w,"caption"); ebs = ty(w,"eyebrow")
    top = round(h*0.60)
    b = top
    svg += [G_(eyebrow(m, b, "On the next episode", size=ebs))]
    b += round(ns*0.92)
    svg += [G_(headline(m, b, G["name"], size=ns, weight=800))]
    b += round(rs*1.2)
    svg += [G_(body(m, b, G["handle"]+"  ·  "+G["title"], size=rs, weight=600, color="#C8D2F0"))]
    b += round(rs*1.5)
    svg += [G_(body(m, b, G["prev"], size=cs, weight=500, color="#AFBCEB"))]
    b += round(cs*2.2)
    svg += [G_(eyebrow(m, b, "Guest from", color=C.eyebrow_ink, size=cs))]
    robo,_ = robostrategy(m, b+round(cs*0.5), round(rs*1.0)); svg += [G_(robo)]
    svg += [footer(w,h), svg_close()]
    check(bg, key+" name", (m, top, round(w*0.80), top+round(ns*1.1)))
    return "".join(svg)


# 6) guest 16:9 — REAL studio banner, full-bleed, text left over scrim -------
def g4_guest_fullbleed(key="g4"):
    w, h = SIZES["16x9"]; m = M(w)
    scale = h / BANNER.height
    big = BANNER.resize((round(BANNER.width*scale), h))
    bg = big.crop((big.width - w, 0, big.width, h)).convert("RGBA")   # right = guest
    xx = np.tile(np.linspace(0, 1, w), (h, 1))
    sc = (np.clip((0.62 - xx)/0.62, 0, 1)**1.05 * 255 * 0.85).astype("uint8")
    black = Image.new("RGBA", (w, h), (0,0,0,0)); black.putalpha(Image.fromarray(sc))
    bg = Image.alpha_composite(bg, black)
    tint = field_pil(w, h).convert("RGBA"); tint.putalpha(64)
    bg = Image.alpha_composite(bg, tint).convert("RGB")
    svg = [svg_open(w,h,"ep01 guest fullbleed"), "<defs>"+glow_defs(w)+"</defs>",
           img_tag(bg,0,0,w,h), G_(chrome(w,h))]
    ns = round(w*0.058); rs = round(ns*0.40); cs = ty(w,"caption"); ebs = ty(w,"eyebrow")
    blk = ebs + round(ns*0.95) + round(rs*1.2) + round(cs*2.0) + round(rs*1.05)
    top = round(h*0.18) + max(0, (round(h*0.64) - blk)//2)
    b = top + ebs
    svg += [G_(eyebrow(m, b, "On the next episode", size=ebs))]
    b += round(ns*0.95)
    svg += [G_(headline(m, b, G["name"], size=ns, weight=800))]
    b += round(rs*1.2)
    svg += [G_(body(m, b, G["handle"]+"  ·  "+G["title"], size=rs, weight=600, color="#C8D2F0"))]
    b += round(cs*2.0)
    svg += [G_(eyebrow(m, b, "Guest from", color=C.eyebrow_ink, size=cs))]
    robo,_ = robostrategy(m, b+round(cs*0.5), round(rs*1.0)); svg += [G_(robo)]
    svg += [footer(w,h,align="right"), svg_close()]
    check(bg, key+" name", (m, top, round(w*0.40), top+blk))
    return "".join(svg)


JOBS = [("01-guest-blend", g1_guest_blend), ("02-guest-box-photo", g2_guest_box),
        ("03-quote-blend", q1_quote_blend), ("04-episode-photo", e1_episode_box),
        ("05-guest-blend-vert", g3_guest_blend_vert),
        ("06-guest-fullbleed-photo", g4_guest_fullbleed)]

if __name__ == "__main__":
    for name, fn in JOBS:
        svg = fn()
        open(f"{OUT}/{name}.svg", "w").write(svg)
        print("  ", name)
    print("\nContrast (white text vs underlying background, WCAG):")
    print("  block                  mean  worst  need  verdict")
    for r in REPORT:
        print(f"  {r[0]:22} {r[1]:>4}  {r[2]:>4}   {r[3]:>3}   {r[4]}")
    print("\n(glow adds a black halo → effective local contrast is higher than 'worst')")
