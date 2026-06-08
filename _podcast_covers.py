#!/usr/bin/env python3
"""
PMN podcast / show cover art — both PMN logos across all four brand backgrounds.

Layout (from Design Draft 1): "THE BLOCK ORIGINAL" eyebrow, a centred hero PMN
lockup, and a "THE BLOCK | Polymarket" endorsement row at the base. Two heroes:

  - wordmark : the full PMN show wordmark (PREDICTION MARKET NEWS + blue dot) —
               for larger formats with room to breathe.
  - monogram : the compact [PMN •] mark — the tighter lockup.

Rendered 1500x1500 (podcast-platform safe; >= Apple's 1400 min, monogram stays
crisp from its 1683px source). Output -> exports-podcast-covers/
Run:  python3 _podcast_covers.py
"""
import os, sys, importlib.util, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = HERE
LIB, SOC = os.path.join(ROOT, "lib"), os.path.join(ROOT, "social")
OUT = os.path.join(ROOT, "exports-podcast-covers"); os.makedirs(OUT, exist_ok=True)
sys.path.insert(0, LIB)
import pmn

spec = importlib.util.spec_from_file_location("soc_build", os.path.join(SOC, "_build.py"))
soc = importlib.util.module_from_spec(spec); sys.modules["soc_build"] = soc
spec.loader.exec_module(soc)

S = 1500
HEROES = [("wordmark", "pmn-wordmark"), ("monogram", "monogram")]
BACKGROUNDS = ["team-solid", "team-gradient", "team-glow", "house"]

n = 0
for bg in BACKGROUNDS:
    pmn.set_background(bg)
    for label, mark in HEROES:
        svg = soc.podcast_cover(S, S, mark)
        base = os.path.join(OUT, f"podcast-cover--{label}--{bg}")
        open(base + ".svg", "w").write(svg)
        subprocess.run(["rsvg-convert", "-o", base + ".png", base + ".svg"], check=True)
        n += 1
        print(f"    podcast-cover--{label}--{bg}")
pmn.set_background("house")
print(f"\nwrote {n} podcast covers -> {os.path.relpath(OUT, ROOT)}/")
