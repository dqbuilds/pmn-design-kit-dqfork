"""
Visual library — turn market-data pulls into social-embeddable charts/cards.

House rules baked in (see references/visual-style.md for the full doctrine):
  - Canvas: 2048x1365 (3:2) default to survive X compression; also 1:1 and 9:16.
  - Palette: Priced In dark theme (deep-navy bg, indigo/blue brand, green/gold
    accents). Every text + graphical color is WCAG-checked against the bg —
    body text >= 4.5:1, large text & chart bars >= 3:1. Run `check_contrast()`
    (or `python visuals.py contrast`) to prove it passes color.adobe.com's
    contrast analyzer. The build asserts on any failure.
  - Story-driven color: pass `highlight={...}` to color the bars the news cycle
    cares about; everything else stays brand-blue. Color is not axis-locked.
  - Every visual carries a source + as-of stamp (on-chain data is timestamped).

Charts render on a SOLID dark bg (contrast guaranteed). To place a chart/card
over the episode's motion ticker background instead, render transparent and
composite with the FFmpeg multiply/softlight plate recipe in visual-style.md —
do NOT bake busy motion behind body copy (keep motion BGs subtle).
"""
from __future__ import annotations

import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

# Treat '$' as a literal dollar sign, not a mathtext delimiter (USD labels
# would otherwise render paired '$...$' spans in italic math).
matplotlib.rcParams["text.parse_math"] = False

# ---- Palette (Priced In) -----------------------------------------------------
BG      = "#03082A"   # deep navy — canvas
PANEL   = "#0A1340"   # lifted panel / card fill
INK     = "#FFFFFF"   # primary text
MUTED   = "#A7B2DE"   # secondary label (lightened from #6e78a8 to clear 4.5:1)
GRID    = "#22306A"   # gridlines / hairlines (non-text)
BRAND   = "#2F5BFF"   # bright blue — default bars
UP      = "#3BEF8E"   # green — positive / highlight
WARN    = "#EFC23B"   # gold — highlight / attention
DOWN    = "#FF5C7A"   # red — negative

ASPECTS = {"3:2": (2048, 1365), "1:1": (2048, 2048), "9:16": (1152, 2048)}
_DPI = 100

# ---- WCAG contrast -----------------------------------------------------------
def _srgb_to_lin(c: float) -> float:
    c /= 255.0
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def _rel_lum(hexc: str) -> float:
    h = hexc.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    return 0.2126 * _srgb_to_lin(r) + 0.7152 * _srgb_to_lin(g) + 0.0722 * _srgb_to_lin(b)


def contrast_ratio(fg: str, bg: str) -> float:
    """WCAG 2.1 contrast ratio between two hex colors (1.0–21.0)."""
    l1, l2 = _rel_lum(fg), _rel_lum(bg)
    hi, lo = max(l1, l2), min(l1, l2)
    return (hi + 0.05) / (lo + 0.05)


def check_contrast(verbose: bool = True) -> bool:
    """
    Assert every palette pairing meets its WCAG floor against BG:
    body text >= 4.5:1, large text & graphical objects >= 3:1.
    Returns True (raises AssertionError if any pair fails).
    """
    body = {"INK": INK, "MUTED": MUTED}              # need 4.5:1
    large = {"BRAND": BRAND, "UP": UP, "WARN": WARN, "DOWN": DOWN}  # need 3:1
    ok = True
    for name, c in body.items():
        r = contrast_ratio(c, BG)
        if verbose:
            print(f"  text {name:6} {c} vs BG  {r:5.2f}:1  (need 4.5)  {'PASS' if r>=4.5 else 'FAIL'}")
        ok &= r >= 4.5
    for name, c in large.items():
        r = contrast_ratio(c, BG)
        if verbose:
            print(f"  elem {name:6} {c} vs BG  {r:5.2f}:1  (need 3.0)  {'PASS' if r>=3.0 else 'FAIL'}")
        ok &= r >= 3.0
    # accent text on the lifted PANEL too (cards put MUTED on PANEL)
    r = contrast_ratio(MUTED, PANEL)
    if verbose:
        print(f"  text MUTED  {MUTED} vs PANEL {r:5.2f}:1  (need 4.5)  {'PASS' if r>=4.5 else 'FAIL'}")
    ok &= r >= 4.5
    assert ok, "palette fails WCAG — adjust colors before rendering"
    return ok


# ---- canvas helpers ----------------------------------------------------------
def _font():
    for p in ("/Library/Fonts/Arial Unicode.ttf",
              "/System/Library/Fonts/Supplemental/Arial.ttf",
              "/System/Library/Fonts/Helvetica.ttc"):
        if os.path.exists(p):
            try:
                fm.fontManager.addfont(p)
                return fm.FontProperties(fname=p).get_name()
            except Exception:
                continue
    return "DejaVu Sans"


_FAM = _font()


def _fig(aspect: str):
    w, h = ASPECTS[aspect]
    fig = plt.figure(figsize=(w / _DPI, h / _DPI), dpi=_DPI)
    fig.patch.set_facecolor(BG)
    plt.rcParams["font.family"] = _FAM
    return fig, (w, h)


def _title(fig, title, subtitle, pad_top=0.93):
    fig.text(0.055, pad_top, title, color=INK, fontsize=46, fontweight="bold",
             va="top", ha="left")
    if subtitle:
        fig.text(0.055, pad_top - 0.075, subtitle, color=MUTED, fontsize=26,
                 va="top", ha="left")


def _footer(fig, source, asof):
    line = f"Source: {source}"
    if asof:
        line += f"   ·   as of {asof}"
    fig.text(0.055, 0.045, line, color=MUTED, fontsize=20, va="center", ha="left")
    fig.text(0.945, 0.045, "@kelvinsparksjr", color=MUTED, fontsize=20,
             va="center", ha="right")


def _save(fig, out):
    fig.savefig(out, facecolor=BG, dpi=_DPI)
    plt.close(fig)
    return out


def _fmt_usd(v: float) -> str:
    a = abs(v)
    if a >= 1e9:  return f"${v/1e9:.2f}B"
    if a >= 1e6:  return f"${v/1e6:.2f}M"
    if a >= 1e3:  return f"${v/1e3:.0f}K"
    return f"${v:,.0f}"


# ---- chart types -------------------------------------------------------------
def bar_ranking(items: list[tuple], title: str, subtitle: str = "",
                source: str = "", asof: str = "", highlight: set | None = None,
                value_fmt=_fmt_usd, aspect: str = "3:2", out: str = "bar.png") -> str:
    """
    Horizontal bar ranking. items = [(label, value), ...] (any order; sorted desc).
    highlight = set of labels to paint gold (story-driven); rest are brand-blue.
    """
    check_contrast(verbose=False)
    highlight = highlight or set()
    items = sorted(items, key=lambda kv: kv[1], reverse=True)
    labels = [k for k, _ in items]
    vals = [v for _, v in items]
    fig, (w, h) = _fig(aspect)
    ax = fig.add_axes([0.12, 0.12, 0.82, 0.66])   # left gutter reserved for labels
    ax.set_facecolor(BG)
    y = range(len(items))
    colors = [WARN if lab in highlight else BRAND for lab in labels]
    ax.barh(list(y), vals, color=colors, height=0.66, zorder=3)
    ax.set_ylim(-0.6, len(items) - 0.4)
    ax.invert_yaxis()
    vmax = max(vals) if vals else 1
    for i, (lab, v) in enumerate(zip(labels, vals)):
        ax.text(-vmax * 0.02, i, lab, color=INK, fontsize=26, va="center", ha="right",
                fontweight="bold")
        ax.text(v + vmax * 0.012, i, value_fmt(v), color=INK, fontsize=24, va="center",
                ha="left")
    for s in ax.spines.values():
        s.set_visible(False)
    ax.set_xticks([]); ax.set_yticks([])
    ax.set_xlim(0, vmax * 1.18)
    _title(fig, title, subtitle)
    _footer(fig, source, asof)
    return _save(fig, out)


def compare_pair(a: tuple, b: tuple, title: str, subtitle: str = "",
                 source: str = "", asof: str = "", value_fmt=_fmt_usd,
                 aspect: str = "3:2", out: str = "pair.png") -> str:
    """Head-to-head two-bar comparison. a/b = (label, value). a is highlighted gold."""
    check_contrast(verbose=False)
    fig, (w, h) = _fig(aspect)
    ax = fig.add_axes([0.08, 0.16, 0.84, 0.58])
    ax.set_facecolor(BG)
    (la, va), (lb, vb) = a, b
    ax.bar([0, 1], [va, vb], color=[WARN, BRAND], width=0.5, zorder=3)
    for x, (lab, v) in zip([0, 1], [a, b]):
        ax.text(x, v + max(va, vb) * 0.03, value_fmt(v), color=INK, fontsize=40,
                fontweight="bold", ha="center", va="bottom")
        ax.text(x, -max(va, vb) * 0.06, lab, color=MUTED, fontsize=28, ha="center",
                va="top")
    ratio = (va / vb) if vb else 0
    if ratio:
        fig.text(0.5, 0.30, f"{ratio:.1f}x", color=UP, fontsize=34, ha="center",
                 fontweight="bold")
    for s in ax.spines.values():
        s.set_visible(False)
    ax.set_xticks([]); ax.set_yticks([]); ax.set_xlim(-0.6, 1.6)
    ax.set_ylim(0, max(va, vb) * 1.18)
    _title(fig, title, subtitle)
    _footer(fig, source, asof)
    return _save(fig, out)


def dominance(label: str, pct: float, title: str, subtitle: str = "",
              source: str = "", asof: str = "", aspect: str = "1:1",
              out: str = "dominance.png") -> str:
    """Single-share donut: `label` holds `pct`% (0-100) of the whole."""
    check_contrast(verbose=False)
    fig, (w, h) = _fig(aspect)
    ax = fig.add_axes([0.18, 0.18, 0.64, 0.56])
    ax.set_aspect("equal")
    ax.pie([pct, 100 - pct], colors=[WARN, GRID], startangle=90, counterclock=False,
           wedgeprops=dict(width=0.30, edgecolor=BG, linewidth=4))
    ax.text(0, 0.12, f"{pct:.1f}%", color=INK, fontsize=64, fontweight="bold",
            ha="center", va="center")
    ax.text(0, -0.20, label, color=MUTED, fontsize=26, ha="center", va="center")
    _title(fig, title, subtitle)
    _footer(fig, source, asof)
    return _save(fig, out)


def odds_shift(rows: list[tuple], title: str, subtitle: str = "", source: str = "",
               asof: str = "", aspect: str = "3:2", out: str = "odds.png") -> str:
    """
    Probability bars 0-100%. rows = [(label, pct), ...] or [(label, pct, pct_prev)].
    A 3-tuple draws a faint 'prev' marker so a shift reads at a glance.
    """
    check_contrast(verbose=False)
    fig, (w, h) = _fig(aspect)
    ax = fig.add_axes([0.12, 0.13, 0.82, 0.62])   # left gutter reserved for labels
    ax.set_facecolor(BG)
    labels = [r[0] for r in rows]
    for i, r in enumerate(rows):
        pct = r[1]
        ax.barh(i, 100, color=GRID, height=0.5, zorder=2)
        ax.barh(i, pct, color=UP if pct >= 50 else MUTED, height=0.5, zorder=3)
        ax.text(-2.5, i, r[0], color=INK, fontsize=24, va="center", ha="right",
                fontweight="bold")
        ax.text(pct + 1.2, i, f"{pct:.0f}%", color=INK, fontsize=24, va="center",
                ha="left")
        if len(r) == 3 and r[2] is not None:
            ax.plot([r[2], r[2]], [i - 0.28, i + 0.28], color=WARN, lw=4, zorder=4)
    ax.set_ylim(-0.6, len(rows) - 0.4); ax.invert_yaxis()
    ax.set_xlim(0, 112)
    for s in ax.spines.values():
        s.set_visible(False)
    ax.set_xticks([]); ax.set_yticks([])
    _title(fig, title, subtitle)
    _footer(fig, source, asof)
    return _save(fig, out)


def stat_card(stat: str, caption: str, source: str = "", asof: str = "",
              aspect: str = "1:1", out: str = "stat.png") -> str:
    """Big-number card. `stat` is the headline figure, `caption` the one-liner."""
    check_contrast(verbose=False)
    fig, (w, h) = _fig(aspect)
    ax = fig.add_axes([0.06, 0.06, 0.88, 0.88]); ax.axis("off")
    card = FancyBboxPatch((0.02, 0.02), 0.96, 0.96, transform=ax.transAxes,
                          boxstyle="round,pad=0.0,rounding_size=0.03",
                          facecolor=PANEL, edgecolor=GRID, linewidth=2)
    ax.add_patch(card)
    fig.text(0.5, 0.60, stat, color=WARN, fontsize=120, fontweight="bold",
             ha="center", va="center")
    fig.text(0.5, 0.40, caption, color=INK, fontsize=34, ha="center", va="center",
             wrap=True)
    _footer(fig, source, asof)
    return _save(fig, out)


def trend_bars(items: list[tuple], title: str, subtitle: str = "",
               source: str = "", asof: str = "", highlight_max: bool = True,
               label_every: int = 3, value_fmt=_fmt_usd, aspect: str = "3:2",
               out: str = "trend.png") -> str:
    """
    Chronological vertical bars for a time series (rise-and-fall context that a
    two-bar compare loses). items = [(label, value), ...] in TIME ORDER (not
    sorted). The peak bar is painted gold/WARN, the rest brand; the peak and the
    latest value are annotated. x-ticks thin to every `label_every`-th label.
    """
    check_contrast(verbose=False)
    fig, (w, h) = _fig(aspect)
    ax = fig.add_axes([0.07, 0.17, 0.88, 0.55])
    ax.set_facecolor(BG)
    labels = [k for k, _ in items]
    vals = [v for _, v in items]
    n = len(items)
    vmax = max(vals) if vals else 1
    imax = vals.index(vmax)
    colors = [WARN if (highlight_max and i == imax) else BRAND for i in range(n)]
    ax.bar(range(n), vals, color=colors, width=0.82, zorder=3)
    # annotate peak and latest
    ax.text(imax, vmax + vmax * 0.04, value_fmt(vmax), color=INK, fontsize=30,
            fontweight="bold", ha="center", va="bottom")
    if n - 1 != imax:
        ax.text(n - 1, vals[-1] + vmax * 0.04, value_fmt(vals[-1]), color=INK,
                fontsize=26, fontweight="bold", ha="center", va="bottom")
    ticks = [i for i in range(n) if i % label_every == 0]
    ax.set_xticks(ticks)
    ax.set_xticklabels([labels[i] for i in ticks], color=MUTED, fontsize=18)
    ax.tick_params(axis="x", length=0, colors=MUTED)
    for s in ax.spines.values():
        s.set_visible(False)
    ax.set_yticks([])
    ax.set_xlim(-0.7, n - 0.3)
    ax.set_ylim(0, vmax * 1.20)
    _title(fig, title, subtitle)
    _footer(fig, source, asof)
    return _save(fig, out)


def _cli(argv):
    if argv and argv[0] == "contrast":
        check_contrast(verbose=True)
        return
    print("usage: visuals.py contrast    # prove the palette passes WCAG")
    print("import the module for bar_ranking / compare_pair / dominance / "
          "odds_shift / stat_card")


if __name__ == "__main__":
    _cli(sys.argv[1:])
