"""
Prediction Market News — social design library
===============================================

Single source of truth for the PMN social/template system. Tokens + components
are derived from the Draft-1 broadcast frames and YT thumbnails (June 2026):

  - palette sampled from the shipped Single/Two/Four-cam frames
  - lockup hierarchy = THE BLOCK leads (top-left) + "PRESENTED BY Polymarket"
    (top-right, fixed sponsor). The PMN show wordmark lives in covers/logo
    lockups, not on the broadcast chrome. (Decided 2026-06-03.)
  - the "translucent box" treatment from the thumbnails (frosted white panel +
    electric-blue translucent bar) is exposed as reusable helpers.

Type renders in Helvetica Neue (native on macOS, matches the broadcast grotesk).
Serif accents use Georgia/Times for the editorial logo variant.

Everything returns an SVG string. No shared state.
"""
from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
import re, base64

ROOT     = Path(__file__).resolve().parent.parent
MARKS    = ROOT / "brand" / "marks"
LOGO_DIR = ROOT / "brand" / "logo-options" / "png"

# Real PMN lockups sliced from Draft-1 Logo.svg (see brand/logo-options/).
# FINAL FOUR (Kelvin, 2026-06-03) — the approved set:
#   monogram  [PMN •]                       — compact mark / avatar / favicon
#   arrow-n   rising-N + PREDICTION...       — pictorial mark / cover / avatar
#   sans-news PREDICTION MARKET / NEWS(serif)— primary wordmark (cards, footer)
#   bold-bar  PREDICTION / MARKET NEWS       — heavy wordmark (hero, show-open)
LOGOS = {
    "monogram":   0,
    "sans-news":  1,
    "bold-bar":   3,
    "arrow-n":   10,
    # legacy aliases retained so older calls still resolve
    "sans-stack": 1,
}
FINALISTS = ("monogram", "arrow-n", "sans-news", "bold-bar")


# ---------------------------------------------------------------------------
# TOKENS
# ---------------------------------------------------------------------------
@dataclass(frozen=True)
class Colors:
    # Broadcast field (sampled from Single-Cam Frame.png)
    ink:         str = "#000000"   # top-left corner of frame gradient
    navy_deep:   str = "#091130"   # near-black navy
    navy_header: str = "#11215C"   # header bar tone
    # Electric blue family (logo + frame accent)
    blue:        str = "#2E5CFF"   # ANCHOR accent (≈ old #2F5BFF, survives)
    blue_bright: str = "#0059FF"   # pure bright blue (logo)
    blue_deep:   str = "#003CFF"   # deep blue (logo)
    cover_blue:  str = "#0B50CF"   # section-divider blue
    # Name-plate gradient (sampled from lower-third)
    plate_a:     str = "#2C44BE"
    plate_b:     str = "#3D59EC"
    # Frame gradient stops
    grad_a:      str = "#05060D"   # dark origin (top-left)
    grad_b:      str = "#10204F"   # mid
    grad_c:      str = "#2E5CFF"   # electric (bottom-right)
    # Data semantic (carried from prior system / market overlay)
    up:          str = "#16C784"
    down:        str = "#EA3943"
    gold:        str = "#EFC23B"
    poly_orange: str = "#F7931A"   # market-card accent in overlay
    # Neutrals
    white:       str = "#FFFFFF"
    off:         str = "#E8ECF7"
    muted:       str = "#9AA6C9"
    # Eyebrow / section-label ink — muted light blue-grey (reads >=11:1 on the
    # dark field; replaces the low-contrast electric-blue eyebrow). Set in Open Sans.
    eyebrow_ink: str = "#B6C4DC"
    tab_ink:     str = "#09112E"   # HOST/GUEST tab


@dataclass(frozen=True)
class Fonts:
    sans:  str = "'Helvetica Neue', Helvetica, Arial, sans-serif"
    serif: str = "Georgia, 'Times New Roman', serif"
    mono:  str = "'SF Mono', ui-monospace, Menlo, monospace"
    label: str = "'Open Sans', 'Helvetica Neue', Arial, sans-serif"   # eyebrows


C = Colors()
F = Fonts()


def esc(t) -> str:
    """XML-escape text content."""
    return (str(t).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


# ---------------------------------------------------------------------------
# MOBILE-FIRST TYPE SCALE
# ---------------------------------------------------------------------------
# A 1080-class image in a phone feed displays at ~358 pt wide. Since on-canvas
# px scale by (358 / canvas_w), type defined as a *ratio of width* renders at a
# fixed on-screen size regardless of aspect:  effective_pt ≈ ratio × 358.
# Floors below target a casual-scroll read (≈13 pt minimum for content text).
TYPE = {
    "display": 0.090,   # ~32 pt — names, hero
    "title":   0.066,   # ~24 pt — card questions
    "lead":    0.048,   # ~17 pt — key body / value prop
    "eyebrow": 0.040,   # ~14 pt — bold tracked labels
    "caption": 0.038,   # ~13.5 pt — attributions, secondary
    "fine":    0.020,   # ~7 pt — true fine print (source, sponsor label) only
}


def ty(w, role):
    """On-canvas font px for a type role at the given canvas width."""
    return round(w * TYPE[role])


def wrap(text, size, max_w, char_factor=0.54):
    """Greedy word-wrap to fit max_w at the given font size. Returns list[str]."""
    words = str(text).split()
    lines, cur = [], ""
    cw = size * char_factor
    for word in words:
        trial = (cur + " " + word).strip()
        if len(trial) * cw <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur); cur = word
    if cur:
        lines.append(cur)
    return lines


# ---------------------------------------------------------------------------
# MARK LOADING (inline the real Block + Polymarket art)
# ---------------------------------------------------------------------------
def _inner(path: Path) -> tuple[str, float, float]:
    t = path.read_text()
    vb = re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', t)
    w, h = (float(vb.group(1)), float(vb.group(2))) if vb else (100.0, 100.0)
    body = re.search(r"<svg[^>]*>(.*)</svg>", t, re.DOTALL).group(1)
    return body, w, h


_BLOCK_INNER, _BLOCK_W, _BLOCK_H = _inner(MARKS / "the-block-primary-white.svg")
_POLY_INNER,  _POLY_W,  _POLY_H  = _inner(MARKS / "polymarket-wordmark-white.svg")
# PMN show wordmark (white "PREDICTION MARKET NEWS" + blue dot) — the lockup for
# LARGER formats with room to breathe (covers, 16:9/9:16). Tight square data
# cards keep the compact [PMN •] monogram instead.
_PMN_INNER, _PMN_W, _PMN_H = _inner(MARKS / "pmn-wordmark-white.svg")


def show_wordmark(x: float, y: float, h: float, align: str = "left",
                  opacity: float = 1.0) -> str:
    """Place the full PMN wordmark (vector) scaled to cap-height `h`."""
    s = h / _PMN_H
    w = _PMN_W * s
    if align == "right":  x -= w
    elif align == "center": x -= w / 2
    return (f'<g transform="translate({x:.1f},{y:.1f}) scale({s:.5f})" '
            f'opacity="{opacity}" aria-label="Prediction Market News">{_PMN_INNER}</g>')


def show_wordmark_aspect() -> float:
    """w/h of the PMN wordmark (for layout math)."""
    return _PMN_W / _PMN_H


def _png_size(p: Path) -> tuple[int, int]:
    head = p.read_bytes()[:26]
    return (int.from_bytes(head[16:20], "big"), int.from_bytes(head[20:24], "big"))


_LOGO_B64: dict[int, tuple[str, int, int]] = {}


def logo(which, x: float, y: float, h: float, align: str = "left",
         opacity: float = 1.0) -> str:
    """Place a real PMN lockup (by name or slice index). Embeds the vector art
    as a transparent PNG (preserves the dot-matrix patterns exactly).
    The special name "pmn-wordmark" routes to the vector show wordmark (the
    larger-format lockup) instead of a PNG slice."""
    if which == "pmn-wordmark":
        return show_wordmark(x, y, h, align=align, opacity=opacity)
    idx = LOGOS[which] if isinstance(which, str) else which
    if idx not in _LOGO_B64:
        p = LOGO_DIR / f"logo-{idx:02d}.png"
        iw, ih = _png_size(p)
        _LOGO_B64[idx] = (base64.b64encode(p.read_bytes()).decode(), iw, ih)
    b64, iw, ih = _LOGO_B64[idx]
    w = h * iw / ih
    if align == "right":  x -= w
    elif align == "center": x -= w / 2
    return (f'<image x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" '
            f'opacity="{opacity}" xlink:href="data:image/png;base64,{b64}"/>')


def logo_aspect(which) -> float:
    """w/h of a lockup (for layout math)."""
    if which == "pmn-wordmark":
        return show_wordmark_aspect()
    idx = LOGOS[which] if isinstance(which, str) else which
    iw, ih = _png_size(LOGO_DIR / f"logo-{idx:02d}.png")
    return iw / ih


# ---------------------------------------------------------------------------
# GRID  — one margin + one panel padding, used by every template (kills drift)
# ---------------------------------------------------------------------------
def M(w):       return round(w * 0.055)   # outer content margin (left edge of everything)
def PADIN(w):   return round(w * 0.042)   # panel inner padding


# ---------------------------------------------------------------------------
# GUEST-COMPANY LOGO  — leverage the guest's employer for shareability.
# Real logo if we have the asset; else a clean wordmark of the company name.
# ---------------------------------------------------------------------------
COMPANY_LOGOS = {
    "polymarket": MARKS / "polymarket-wordmark-white.svg",
}


def company_mark(name, x, y, h, align="left", color=None):
    """Return (svg, width). Places the guest's company logo/wordmark, top-left
    anchored at (x, y) unless align overrides. `h` is the cap/mark height."""
    color = color or C.white
    key = str(name).lower().strip()
    if key in COMPANY_LOGOS:
        inner, w0, h0 = _inner(COMPANY_LOGOS[key])
        s = h / h0
        ww = w0 * s
        if align == "right":  x -= ww
        elif align == "center": x -= ww / 2
        return (f'<g transform="translate({x:.1f},{y:.1f}) scale({s:.4f})" '
                f'aria-label="{esc(name)}">{inner}</g>', ww)
    # fallback: bold wordmark
    ww = len(str(name)) * h * 0.60
    if align == "right":  x -= ww
    elif align == "center": x -= ww / 2
    return (f'<text x="{x:.1f}" y="{y + h*0.82:.1f}" font-family="{F.sans}" '
            f'font-size="{h:.1f}" font-weight="800" letter-spacing="-0.5" '
            f'fill="{color}">{esc(name)}</text>', ww)


def block_lockup(x: float, y: float, h: float = 34) -> str:
    """THE BLOCK primary wordmark, white. Lead mark — top-left of every asset."""
    s = h / _BLOCK_H
    return (f'<g transform="translate({x},{y}) scale({s})" '
            f'aria-label="The Block">{_BLOCK_INNER}</g>')


def polymarket_presented(x_right: float, y: float, h: float = 26,
                         label: bool = True) -> str:
    """'PRESENTED BY  Polymarket' — fixed top-right sponsor stamp."""
    s = h / _POLY_H
    pw = _POLY_W * s
    out = []
    if label:
        lsize = max(h * 0.52, 15)
        out.append(f'<text x="{x_right - pw - 18}" y="{y + h*0.5 + lsize*0.36:.1f}" '
                   f'text-anchor="end" font-family="{F.sans}" font-size="{lsize:.1f}" '
                   f'font-weight="600" letter-spacing="1.5" fill="{C.muted}">PRESENTED BY</text>')
    out.append(f'<g transform="translate({x_right - pw},{y}) scale({s})" '
               f'opacity="0.96" aria-label="Polymarket">{_POLY_INNER}</g>')
    return "".join(out)


# ---------------------------------------------------------------------------
# SVG SHELL
# ---------------------------------------------------------------------------
def svg_open(w: int, h: int, label: str = "") -> str:
    return (f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
            f'xmlns="http://www.w3.org/2000/svg" '
            f'xmlns:xlink="http://www.w3.org/1999/xlink" data-label="{label}">')


def svg_close() -> str:
    return "</svg>"


# Active field gradient — BLUE family only. Override with set_field_theme() to
# render an asset in a different permissible blue gradient. (Never non-blue:
# green/red/gold are data-viz semantics, not field colours.)
_FIELD = {"a": C.grad_a, "b": C.grad_b, "c": C.grad_c}

def set_field_theme(a=None, b=None, c=None):
    """Set the field gradient stops for subsequent defs() calls (blue family)."""
    if a: _FIELD["a"] = a
    if b: _FIELD["b"] = b
    if c: _FIELD["c"] = c

def reset_field_theme():
    _FIELD.update(a=C.grad_a, b=C.grad_b, c=C.grad_c)


def defs(w: int, h: int) -> str:
    """Shared gradients: broadcast field + name-plate + frosted panel."""
    return f'''<defs>
  <linearGradient id="field" x1="0" y1="0" x2="{w}" y2="{h}" gradientUnits="userSpaceOnUse">
    <stop offset="0" stop-color="{_FIELD['a']}"/>
    <stop offset="0.55" stop-color="{_FIELD['b']}"/>
    <stop offset="1" stop-color="{_FIELD['c']}"/>
  </linearGradient>
  <linearGradient id="plate" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="{C.plate_a}"/>
    <stop offset="1" stop-color="{C.plate_b}"/>
  </linearGradient>
  <linearGradient id="blueBar" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="{C.blue_bright}"/>
    <stop offset="1" stop-color="{C.blue}"/>
  </linearGradient>
  <linearGradient id="photoScrim" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#000000" stop-opacity="0"/>
    <stop offset="1" stop-color="#000000" stop-opacity="0.72"/>
  </linearGradient>
  <filter id="soft" x="-20%" y="-20%" width="140%" height="140%">
    <feDropShadow dx="0" dy="6" stdDeviation="18" flood-color="#000000" flood-opacity="0.35"/>
  </filter>
</defs>'''


# ---------------------------------------------------------------------------
# BACKGROUNDS
# ---------------------------------------------------------------------------
# ── team backgrounds (shared; from PMN backgrounds.zip) ──────────────────────
# Black->electric-blue diagonal, near-black solid, blue edge-glow. All darker
# than the house field, so white text clears WCAG AA (the only watch-out is the
# bright corner of team-gradient — keep fine-print white there, not muted).
def bg_team_gradient(w, h):
    return (f'<linearGradient id="tg" x1="0" y1="0" x2="{w}" y2="{h}" gradientUnits="userSpaceOnUse">'
            f'<stop stop-color="#000000"/><stop offset="1" stop-color="#2E5CFF"/></linearGradient>'
            f'<rect width="{w}" height="{h}" fill="url(#tg)"/>')

def bg_team_solid(w, h):
    return f'<rect width="{w}" height="{h}" fill="#111111"/>'

def bg_team_glow(w, h):
    return (f'<radialGradient id="tgl" gradientUnits="userSpaceOnUse" '
            f'cx="{w*0.5}" cy="{h*0.02}" r="{max(w,h)*0.85}">'
            f'<stop offset="0" stop-color="#2E5CFF" stop-opacity="0.40"/>'
            f'<stop offset="0.55" stop-color="#06122E" stop-opacity="0"/></radialGradient>'
            f'<rect width="{w}" height="{h}" fill="#000000"/>'
            f'<rect width="{w}" height="{h}" fill="url(#tgl)"/>')

BACKGROUNDS = {"house": None, "team-gradient": bg_team_gradient,
               "team-solid": bg_team_solid, "team-glow": bg_team_glow}
_BG = None
def set_background(key):
    """Swap the field for a team background (or 'house' for the diagonal field)."""
    global _BG; _BG = BACKGROUNDS[key]


def field(w: int, h: int) -> str:
    """The broadcast diagonal field: dark origin -> electric blue corner.
    Honours an active team background (set_background) when one is selected."""
    if _BG is not None:
        return _BG(w, h)
    return f'<rect width="{w}" height="{h}" fill="url(#field)"/>'


def photo_placeholder(x, y, w, h, rx=18, tone=0):
    """Neutral photo well + faint head/shoulders silhouette (until real art drops)."""
    g = f"phl{int(x)}{int(y)}"
    base = ["#1A2342", "#222C4E", "#15203F"][tone % 3]
    cx = x + w / 2
    # head + shoulders silhouette, centred, sized to the well
    hr = min(w, h) * 0.16
    hcy = y + h * 0.40
    sh_w = hr * 3.2
    sh_top = hcy + hr * 1.25
    return (f'<defs><radialGradient id="{g}" cx="0.5" cy="0.36" r="0.9">'
            f'<stop offset="0" stop-color="{base}"/>'
            f'<stop offset="1" stop-color="#070B1A"/></radialGradient></defs>'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="url(#{g})"/>'
            f'<g fill="#000000" fill-opacity="0.22">'
            f'<circle cx="{cx}" cy="{hcy}" r="{hr}"/>'
            f'<path d="M {cx-sh_w/2} {y+h} '
            f'Q {cx-sh_w/2} {sh_top} {cx} {sh_top} '
            f'Q {cx+sh_w/2} {sh_top} {cx+sh_w/2} {y+h} Z"/>'
            f'</g>')


# ---------------------------------------------------------------------------
# CHROME (applies the locked hierarchy to any asset)
# ---------------------------------------------------------------------------
def chrome(w: int, h: int, pad: float = None, block_h: float = None,
           poly: bool = True, poly_label: bool = True) -> str:
    """Standard top chrome: Block top-left, Polymarket top-right."""
    pad = pad if pad is not None else M(w)
    block_h = block_h if block_h is not None else round(w * 0.030)
    out = [block_lockup(pad, pad, h=block_h)]
    if poly:
        out.append(polymarket_presented(w - pad, pad,
                                        h=round(block_h * 0.78),
                                        label=poly_label))
    return "".join(out)


# ---------------------------------------------------------------------------
# TRANSLUCENT BOX TREATMENT  (from the YT thumbnails)
# ---------------------------------------------------------------------------
def frosted_panel(x, y, w, h, rx=20, opacity=0.86, stroke=True):
    """White frosted rounded panel — the thumbnail's signature container."""
    s = (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" '
         f'fill="#FFFFFF" fill-opacity="{opacity}" filter="url(#soft)"/>')
    if stroke:
        s += (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" '
              f'fill="none" stroke="#FFFFFF" stroke-opacity="0.5" stroke-width="1.5"/>')
    return s


def blue_bar(x, y, w, h, rx=8, opacity=0.92, grad=True):
    """Electric-blue translucent bar — the thumbnail accent block."""
    fill = "url(#blueBar)" if grad else C.blue
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" '
            f'fill="{fill}" fill-opacity="{opacity}"/>')


def glass_dark(x, y, w, h, rx=20, opacity=0.46):
    """Dark frosted panel (for text over bright photo areas)."""
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" '
            f'fill="{C.navy_deep}" fill-opacity="{opacity}" filter="url(#soft)"/>'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" '
            f'fill="none" stroke="#FFFFFF" stroke-opacity="0.14" stroke-width="1.5"/>')


# The canonical data/content panel (dark-mode framework): near-black, hairline
# border + soft shadow. Text on it is white (C.white) / muted (C.muted); tracks
# are white at low opacity. Used across data cards AND content cards.
PANEL_BG = "#06080F"

# Panel texture: replaces the flat black box with a subtle fill drawn from the
# team backgrounds — one option per field style, all capped at the DARK end so
# white (and muted) text stay WCAG AA:
#   solid/flat — flat near-black (echoes team-solid)
#   gradient   — black→deep-navy diagonal (echoes team-gradient)
#   glow       — blue radial wash up top (echoes team-glow)
#   field      — 3-stop broadcast diagonal, dark origin→blue corner (echoes house)
#   glow-corner— blue wash from the top-left corner (alt glow angle)
PANEL_TEXTURES = ["solid", "gradient", "glow", "field", "glow-corner"]
PANEL_TEX = "glow"           # solid/flat | gradient | glow | field | glow-corner
def set_panel_texture(key):
    global PANEL_TEX; PANEL_TEX = key

def _panel_body(x, y, w, h, rx, base, tex):
    """Just the filled (rounded, shadowed) box — no border. Every texture is a
    SOFT, diffuse radial wash (no hard diagonal light shafts) drawn from one
    direction. Brightest tone stays low so white ≥14:1 and muted ≥5:1 (verified).
      (cx_frac, cy_frac, radius_frac, peak_opacity, falloff_offset)"""
    box = lambda fill, filt='filter="url(#soft)"': (
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" {filt}/>')
    PRESETS = {
        "glow":        (0.50, 0.02, 0.98, 0.38, 0.82),   # soft wash from the top
        "glow-corner": (0.08, 0.05, 1.02, 0.40, 0.82),   # soft wash from top-left
        "gradient":    (0.82, 0.96, 1.12, 0.38, 0.84),   # soft light rising bottom-right
        "field":       (1.00, 0.45, 1.22, 0.34, 0.86),   # soft side light from the right
    }
    if tex not in PRESETS:
        return box(base)                                  # solid / flat
    cxf, cyf, rf, op, fo = PRESETS[tex]
    uid = f"pgl{int(x)}x{int(y)}"
    cx, cy, r = x + w*cxf, y + h*cyf, max(w, h)*rf
    return (box(base)
            + f'<radialGradient id="{uid}" gradientUnits="userSpaceOnUse" '
              f'cx="{cx:.0f}" cy="{cy:.0f}" r="{r:.0f}">'
              f'<stop offset="0" stop-color="#15397D" stop-opacity="{op}"/>'
              f'<stop offset="{fo}" stop-color="#06080F" stop-opacity="0"/></radialGradient>'
            + box(f"url(#{uid})", filt=""))

def panel(x, y, w, h, rx_ratio=None, canvas_w=None, texture=None):
    rx = round((canvas_w or w) * 0.025) if rx_ratio is None else rx_ratio
    return (_panel_body(x, y, w, h, rx, PANEL_BG, texture or PANEL_TEX)
            + f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="none" '
              f'stroke="#FFFFFF" stroke-opacity="0.12" stroke-width="1.5"/>')


# ---------------------------------------------------------------------------
# LOWER-THIRD / NAME CHIP  (from the broadcast frames)
# ---------------------------------------------------------------------------
def name_chip(x, y, role, name, line2="", line3="", scale=1.0):
    """Black role tab + blue name plate, stacked text. Frame lower-third."""
    tab_w = 84 * scale
    tab_h = 132 * scale
    plate_w = max(360 * scale, (len(name) * 17 + 90) * scale)
    txt_x = x + tab_w + 28 * scale
    out = [
        # role tab
        f'<rect x="{x}" y="{y}" width="{tab_w}" height="{tab_h}" fill="{C.tab_ink}"/>',
        f'<text x="{x+tab_w/2}" y="{y+tab_h/2+5*scale}" text-anchor="middle" '
        f'font-family="{F.sans}" font-size="{15*scale:.1f}" font-weight="700" '
        f'letter-spacing="1.5" fill="#FFFFFF" '
        f'transform="rotate(-90 {x+tab_w/2} {y+tab_h/2})">{esc(role).upper()}</text>',
        # name plate
        f'<rect x="{x+tab_w}" y="{y}" width="{plate_w}" height="{tab_h}" fill="url(#plate)"/>',
        f'<text x="{txt_x}" y="{y+50*scale}" font-family="{F.sans}" '
        f'font-size="{30*scale:.1f}" font-weight="700" fill="#FFFFFF">{esc(name)}</text>',
    ]
    if line2:
        out.append(f'<text x="{txt_x}" y="{y+82*scale}" font-family="{F.sans}" '
                   f'font-size="{19*scale:.1f}" font-weight="500" fill="#D9E0F7">{esc(line2)}</text>')
    if line3:
        out.append(f'<text x="{txt_x}" y="{y+108*scale}" font-family="{F.sans}" '
                   f'font-size="{19*scale:.1f}" font-weight="500" fill="#AFBCEB">{esc(line3)}</text>')
    return "".join(out)


# ---------------------------------------------------------------------------
# TYPE PRIMITIVES
# ---------------------------------------------------------------------------
def eyebrow(x, y, text, color=None, size=22, anchor="start"):
    # muted blue-grey label in Open Sans, at HALF the caller's size (uppercase,
    # lightly tracked). Size is halved globally here so every caller scales down.
    color = color or C.eyebrow_ink
    fs = size * 0.5
    ls = max(1, round(fs * 0.10))
    return (f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-family="{F.label}" '
            f'font-size="{fs:.1f}" font-weight="700" letter-spacing="{ls}" '
            f'fill="{color}">{esc(text).upper()}</text>')


def headline(x, y, lines, size=72, lh=1.06, weight=800, color=None, anchor="start"):
    color = color or C.white
    if isinstance(lines, str):
        lines = [lines]
    out = []
    for i, ln in enumerate(lines):
        out.append(f'<text x="{x}" y="{y + i*size*lh:.0f}" text-anchor="{anchor}" '
                   f'font-family="{F.sans}" font-size="{size}" font-weight="{weight}" '
                   f'letter-spacing="-1" fill="{color}">{esc(ln)}</text>')
    return "".join(out)


def serif_head(x, y, lines, size=64, lh=1.05, color=None, anchor="start", italic=True):
    color = color or C.white
    if isinstance(lines, str):
        lines = [lines]
    st = "italic" if italic else "normal"
    out = []
    for i, ln in enumerate(lines):
        out.append(f'<text x="{x}" y="{y + i*size*lh:.0f}" text-anchor="{anchor}" '
                   f'font-family="{F.serif}" font-style="{st}" font-size="{size}" '
                   f'font-weight="700" fill="{color}">{esc(ln)}</text>')
    return "".join(out)


def body(x, y, text, size=26, weight=500, color=None, anchor="start"):
    color = color or C.off
    return (f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-family="{F.sans}" '
            f'font-size="{size}" font-weight="{weight}" fill="{color}">{esc(text)}</text>')


# ---------------------------------------------------------------------------
# PMN SHOW WORDMARK (knockout-bar variant, for covers/footers — NOT on frames)
# ---------------------------------------------------------------------------
def pmn_wordmark(x, y, size=40, anchor="start"):
    """Bold-sans 'PREDICTION MARKET NEWS' with blue knockout bar under NEWS."""
    return (
        f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-family="{F.sans}" '
        f'font-size="{size}" font-weight="800" letter-spacing="0.5" '
        f'fill="{C.white}">PREDICTION MARKET</text>'
        f'<g>'
        f'<rect x="{x}" y="{y + size*0.18:.0f}" width="{size*4.0:.0f}" height="{size*0.62:.0f}" '
        f'fill="{C.blue}"/>'
        f'<text x="{x + size*0.18:.0f}" y="{y + size*0.66:.0f}" font-family="{F.sans}" '
        f'font-size="{size}" font-weight="800" letter-spacing="2" '
        f'fill="{C.white}">NEWS</text>'
        f'</g>'
    )


def duration_stamp(x_right, y_bottom, text="48:56"):
    """Bottom-right runtime stamp (thumbnail convention)."""
    w = len(text) * 13 + 24
    return (f'<rect x="{x_right - w}" y="{y_bottom - 34}" width="{w}" height="30" rx="6" '
            f'fill="#000000" fill-opacity="0.78"/>'
            f'<text x="{x_right - w/2}" y="{y_bottom - 13}" text-anchor="middle" '
            f'font-family="{F.mono}" font-size="18" font-weight="600" '
            f'fill="#FFFFFF">{text}</text>')
