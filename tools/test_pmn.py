#!/usr/bin/env python3
"""
test_pmn.py — contract tests for the PMN Figma↔code pipeline.
==============================================================
Figma operations themselves need the live Plugin API, but the *contract* that
makes a card renderable is all in the repo: the manifests, tokens.json, and
brands.json. These tests catch the real failure modes BEFORE a render —
an unknown slot kind, a missing bind, a list with no row component, a token a
card needs but a brand mode is missing, a manifest kind the renderer can't fill.

Run:   python3 tools/test_pmn.py          (prints a report, exits non-zero on failure)
   or: pytest tools/test_pmn.py            (each check is a test_* function)

Re-run after every re-export (export_manifest.js / export_tokens.js).
"""
import json, os, re, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TPL = os.path.join(ROOT, "templates")
TOOLS = os.path.join(ROOT, "tools")
NODE_ID = re.compile(r"^\d+:\d+$")

# slot kinds that may appear inside a manifest's slots[] / list rows
SLOT_KINDS = {"text", "bar", "arc", "linechart", "delta", "image", "logo"}
GEOMETRY_KINDS = {"bar", "arc", "linechart", "image"}   # named @…
CONTENT_KINDS = {"text", "delta", "logo", "image"}      # named #…
REQUIRED_BRAND_COLORS = [
    "color/field/start", "color/field/mid", "color/field/end",
    "color/accent", "color/accent-weak", "color/panel-bg", "color/surface",
    "color/track", "color/hairline", "color/text", "color/muted",
    "color/eyebrow-ink", "color/up", "color/down",
]
REQUIRED_BRAND_FONTS = ["font/display", "font/body", "font/mono"]
REQUIRED_LAYOUT = ["space/margin", "space/gutter", "radius/panel", "radius/pill", "stroke/hairline"]


def _load(path):
    with open(path) as f:
        return json.load(f)


def manifests():
    out = {}
    for p in sorted(glob.glob(os.path.join(TPL, "*.manifest.json"))):
        out[os.path.basename(p)] = _load(p)
    return out


def tokens():
    return _load(os.path.join(TPL, "tokens.json"))


def brands():
    return _load(os.path.join(TPL, "brands.json"))


def _check_slot(where, slot):
    assert "name" in slot and isinstance(slot["name"], str), f"{where}: slot missing name"
    name, kind = slot["name"], slot.get("kind")
    assert name[0] in "#@", f"{where}: slot '{name}' must start with # or @"
    assert kind in SLOT_KINDS, f"{where}: slot '{name}' has unknown kind '{kind}'"
    assert "bind" in slot and slot["bind"], f"{where}: slot '{name}' has no bind"
    if kind == "logo":
        assert slot["bind"].startswith("brand."), f"{where}: logo '{name}' bind must be brand.* (got {slot['bind']})"
    if name[0] == "@":
        assert kind in GEOMETRY_KINDS, f"{where}: @-slot '{name}' has non-geometry kind '{kind}'"
    if name[0] == "#":
        assert kind in CONTENT_KINDS, f"{where}: #-slot '{name}' has non-content kind '{kind}'"


# ---------------------------------------------------------------- tests
def test_manifests_structure():
    ms = manifests()
    assert len(ms) == 10, f"expected 10 manifests, found {len(ms)}: {sorted(ms)}"
    for fn, m in ms.items():
        assert isinstance(m.get("template"), str) and m["template"], f"{fn}: no template name"
        nid = m.get("figma", {}).get("componentNodeId")
        assert nid and NODE_ID.match(nid), f"{fn}: bad componentNodeId {nid!r}"
        slots = m.get("slots")
        assert isinstance(slots, list) and slots, f"{fn}: empty slots"
        names = [s["name"] for s in slots]
        assert len(names) == len(set(names)), f"{fn}: duplicate slot names {[n for n in names if names.count(n) > 1]}"
        for s in slots:
            _check_slot(fn, s)
        # every card carries the shared chrome slots
        for req in ("#logo.publisher", "#logo.sponsor", "#logo.show", "#source"):
            assert req in names, f"{fn}: missing chrome slot {req}"


def test_lists():
    for fn, m in manifests().items():
        for lst in m.get("lists", []):
            assert lst.get("node") and lst.get("bind"), f"{fn}: list missing node/bind"
            item = lst.get("item") or {}
            assert item.get("component"), f"{fn}: list '{lst['node']}' has no item.component"
            assert item.get("slots"), f"{fn}: list '{lst['node']}' has no row slots"
            for s in item["slots"]:
                _check_slot(f"{fn}:row", s)


def test_tokens():
    tk = tokens()["collections"]
    assert "Brand" in tk and "Layout" in tk, "tokens.json missing Brand/Layout collections"
    brand_modes = tk["Brand"]["modes"]
    for need in ("PMN", "Demo"):
        assert need in brand_modes, f"Brand collection missing mode {need}"
    btok = tk["Brand"]["tokens"]
    for name in REQUIRED_BRAND_COLORS + REQUIRED_BRAND_FONTS:
        assert name in btok, f"Brand missing token {name}"
        for mode in brand_modes:
            v = btok[name]["values"].get(mode)
            assert v is not None, f"token {name} has no value for mode {mode}"
            if name.startswith("color/"):
                assert isinstance(v, str) and v.startswith("#"), f"{name}/{mode} not a hex color: {v!r}"
    ltok = tk["Layout"]["tokens"]
    for name in REQUIRED_LAYOUT:
        assert name in ltok, f"Layout missing token {name}"


def test_brands():
    tk = tokens()["collections"]["Brand"]["modes"]
    for key, b in brands().items():
        if key.startswith("_"):
            continue
        logos = b.get("logos", {})
        for role in ("publisher", "sponsor", "show"):
            assert role in logos and NODE_ID.match(logos[role].get("id", "")), f"brand {key}: bad logo id for {role}"
        assert b.get("mode") in tk, f"brand {key}: mode '{b.get('mode')}' not in tokens Brand modes {tk}"


def test_manifest_brand_modes_exist():
    tk = set(tokens()["collections"]["Brand"]["modes"])
    for fn, m in manifests().items():
        for mode in (m.get("brand") or {}).get("modes", []):
            assert mode in tk, f"{fn}: brand mode '{mode}' not defined in tokens.json"


def test_renderer_supports_all_kinds():
    src = open(os.path.join(TOOLS, "render.js")).read()
    used = set()
    for m in manifests().values():
        for s in m["slots"]:
            used.add(s["kind"])
        for lst in m.get("lists", []):
            for s in lst["item"]["slots"]:
                used.add(s["kind"])
    for kind in used:
        if kind == "text":
            continue  # the renderer's default branch
        assert f'"{kind}"' in src, f"render.js has no handler for slot kind '{kind}'"


def test_tools_present():
    for name, marker in [("render.js", "renderCard"), ("export_manifest.js", "exportManifest"), ("export_tokens.js", "exportTokens")]:
        p = os.path.join(TOOLS, name)
        assert os.path.exists(p), f"missing tools/{name}"
        assert marker in open(p).read(), f"tools/{name} missing {marker}()"


# ---------------------------------------------------------------- runner
def _main():
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    passed, failed = 0, 0
    for t in tests:
        try:
            t()
            print(f"  \033[32m✓\033[0m {t.__name__}")
            passed += 1
        except AssertionError as e:
            print(f"  \033[31m✗\033[0m {t.__name__}: {e}")
            failed += 1
        except Exception as e:
            print(f"  \033[31m✗\033[0m {t.__name__}: {type(e).__name__}: {e}")
            failed += 1
    print(f"\n{passed} passed, {failed} failed")
    return 1 if failed else 0


if __name__ == "__main__":
    import sys
    print("PMN pipeline contract tests\n")
    sys.exit(_main())
