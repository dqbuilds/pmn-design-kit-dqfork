#!/usr/bin/env python3
"""
Episode 01 — REAL-photo / real-logo cover set (RoboStrategy · Kevin McCordic).

Renders the six photo builders in episode-01/_build.py to PNG (the source only
emits SVG). The liquid-glass surface is applied to the standard data panel, so
the 16:9 episode card's WITH panel matches the rest of the episode kit.

Uses the real assets: intern portrait / face-circle / studio banner + the
RoboStrategy lockup. Output -> episode-01/exports-robostrategy/cover-*.png

Run:  python3 episode-01/_covers.py
"""
import os, sys, importlib.util, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
LIB = os.path.join(ROOT, "lib")
OUT = os.path.join(HERE, "exports-robostrategy"); os.makedirs(OUT, exist_ok=True)
sys.path.insert(0, LIB)
import pmn

TINT = 0.72


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

# load the episode-01 photo builders
spec = importlib.util.spec_from_file_location("ep01", os.path.join(HERE, "_build.py"))
ep = importlib.util.module_from_spec(spec); sys.modules["ep01"] = ep
spec.loader.exec_module(ep)

JOBS = [("cover-guest-blend",      ep.g1_guest_blend),
        ("cover-guest-box-photo",  ep.g2_guest_box),
        ("cover-quote-blend",      ep.q1_quote_blend),
        ("cover-episode-16x9",     ep.e1_episode_box),
        ("cover-guest-vertical",   ep.g3_guest_blend_vert),
        ("cover-fullbleed-16x9",   ep.g4_guest_fullbleed)]

n = 0
for name, fn in JOBS:
    try:
        svg = fn()
        base = os.path.join(OUT, name)
        open(base + ".svg", "w").write(svg)
        subprocess.run(["rsvg-convert", "-o", base + ".png", base + ".svg"], check=True)
        n += 1; print("   ", name)
    except Exception as e:
        print("   !! skipped", name, "->", repr(e)[:160])

print(f"\nwrote {n}/{len(JOBS)} real-photo covers -> {os.path.relpath(OUT, ROOT)}/")
