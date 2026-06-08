"""
PMN live-data adapter
=====================
Bridges ``skills/market-data/scripts`` -> generator data dicts. The market-data
modules return raw numbers; the generators want ready-to-render dicts that mix
those numbers with EDITORIAL copy (tag / title / caption) and a dated source
stamp. This module pulls the numbers and merges them into editorial templates,
stamping the real as-of date.

Design split (the whole point):
  - EDITORIAL fields (tag, title, caption) are written, not pulled — they carry
    the show's voice. You pass them in.
  - LIVE fields (odds %, 24h volume, the source date) are pulled here.

Robustness: every fetch FALLS BACK to the committed values you pass as
``fallback`` on any failure (no network, market not found, shape change), so a
render never breaks — it just renders the last-known numbers with a "(cached)"
source. Pulls are logged to stderr so a scheduler can tell live from cached.

Scope: "just the adapter" — pull writes the dict; you still run the generator.
A generator opts in with::

    import pmn_live
    rows, src = pmn_live.perps_leaderboard(TICKERS, fallback=PERPS_FALLBACK)

CLI (pull + print + snapshot to episode-01/data/live.json)::

    python3 lib/pmn_live.py
"""
from __future__ import annotations

import datetime
import os
import sys

# ── wire in the market-data scripts (sibling skill) ──────────────────────────
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS = os.path.join(ROOT, "skills", "market-data", "scripts")
if SCRIPTS not in sys.path:
    sys.path.insert(0, SCRIPTS)


def _log(msg: str) -> None:
    print(f"[pmn_live] {msg}", file=sys.stderr)


def as_of(date: datetime.date | None = None) -> str:
    """Card-style date stamp, e.g. 'Jun 8, 2026'. Pass a date for reproducible
    renders; defaults to today."""
    d = date or datetime.date.today()
    return f"{d.strftime('%b')} {d.day}, {d.year}"


# ── Hyperliquid: curated perps leaderboard ───────────────────────────────────
def perps_leaderboard(tickers, dex: str = "xyz",
                      source_label: str = "Trade.xyz · Hyperliquid",
                      fallback=None, date: datetime.date | None = None):
    """Live 24h-notional leaderboard for a CURATED ticker set (the editorial
    choice of which names belong on the card), ranked high->low.

    tickers: list of (display_name, symbol), e.g. [("Micron (MU)", "MU"), ...].
             display_name is editorial; symbol is matched against the dex book.
    Returns (rows, source) where rows = [(display, vol_musd, "$X.XM")] and
    source carries the real pull date. Falls back to `fallback` rows on failure.
    """
    try:
        import hyperliquid as hl
        book = {(r.get("name") or "").split(":")[-1].upper(): r
                for r in hl.perp_contexts(dex)}
        rows = []
        missing = []
        for disp, sym in tickers:
            r = book.get(sym.upper())
            vol = (r or {}).get("day_ntl_vlm")
            if not vol:
                missing.append(sym)
                continue
            v = vol / 1e6
            rows.append((disp, round(v, 1), f"${v:.1f}M"))
        if not rows:
            raise RuntimeError("no curated tickers matched the live book")
        rows.sort(key=lambda x: x[1], reverse=True)
        if missing:
            _log(f"perps: matched {len(rows)}, missing {missing}")
        _log(f"perps: LIVE {[(d, s) for d, _, s in rows]}")
        return rows, f"{source_label} · {as_of(date)}"
    except Exception as e:  # noqa: BLE001 — any failure -> cached render
        _log(f"perps: FELL BACK ({e!r}); rendering cached values")
        return (fallback or []), f"{source_label} (cached)"


# ── Polymarket: binary (Yes/No) market ───────────────────────────────────────
def binary_from_slug(slug: str, editorial: dict, fallback: dict | None = None,
                     date: datetime.date | None = None):
    """Build a binary-card dict from a live Polymarket market.

    editorial: {tag, question, src?} — the written framing.
    Returns {**editorial, yes, no, src} with live integer percentages, or
    `fallback` on any failure.
    """
    try:
        import polymarket as pm
        m = pm.market_odds(slug=slug)
        if not m:
            raise RuntimeError(f"market not found: {slug}")
        od = {(o.get("outcome") or "").lower(): (o.get("price") or 0.0)
              for o in m.get("odds", [])}
        if "yes" not in od or "no" not in od:
            raise RuntimeError(f"not a Yes/No market: {sorted(od)}")
        yes, no = round(od["yes"] * 100), round(od["no"] * 100)
        _log(f"binary[{slug}]: LIVE Yes {yes}% / No {no}%")
        return {**editorial, "yes": yes, "no": no,
                "src": f"{editorial.get('src', 'Polymarket')} · {as_of(date)}"}
    except Exception as e:  # noqa: BLE001
        _log(f"binary[{slug}]: FELL BACK ({e!r})")
        return fallback


def top_binary(editorial: dict, scan: int = 50, date: datetime.date | None = None):
    """Self-contained demo: build a binary card from the highest-volume LIVE
    Yes/No market right now. Proves the Polymarket -> card path with no slug to
    hardcode. (For a real card, prefer binary_from_slug with the exact slug.)
    """
    try:
        import polymarket as pm
        for m in pm.top_markets_by_volume(scan):
            od = {(o.get("outcome") or "").lower(): (o.get("price") or 0.0)
                  for o in m.get("odds", [])}
            if "yes" in od and "no" in od:
                yes, no = round(od["yes"] * 100), round(od["no"] * 100)
                q = (m.get("question") or "").strip()
                _log(f"top_binary: LIVE '{q}' Yes {yes}% / No {no}%")
                return {**editorial,
                        "question": editorial.get("question") or [q],
                        "yes": yes, "no": no, "_market": q,
                        "src": f"Polymarket · {as_of(date)}"}
        raise RuntimeError("no Yes/No market in the scanned set")
    except Exception as e:  # noqa: BLE001
        _log(f"top_binary: FAILED ({e!r})")
        return None


# ── CLI: pull, print, snapshot ───────────────────────────────────────────────
# The curated AI + hardware perps set behind the RoboStrategy episode card.
PERPS_TICKERS = [("Micron (MU)", "MU"), ("Nvidia (NVDA)", "NVDA"),
                 ("SpaceX (SPCX)", "SPCX"), ("AMD", "AMD"), ("Tesla (TSLA)", "TSLA")]
# committed (cached) values — used if the pull fails
PERPS_FALLBACK = [("Micron (MU)", 102.6, "$102.6M"), ("Nvidia (NVDA)", 29.3, "$29.3M"),
                  ("SpaceX (SPCX)", 21.6, "$21.6M"), ("AMD", 12.4, "$12.4M"),
                  ("Tesla (TSLA)", 8.2, "$8.2M")]


def _cli() -> None:
    import json
    rows, src = perps_leaderboard(PERPS_TICKERS, fallback=PERPS_FALLBACK)
    bincard = top_binary({"tag": "Live odds · Polymarket", "question": None})
    snapshot = {
        "as_of": as_of(),
        "perps_leaderboard": {"rows": rows, "source": src},
        "top_binary": bincard or "unavailable",
    }
    print(json.dumps(snapshot, indent=2, ensure_ascii=False))
    out_dir = os.path.join(ROOT, "episode-01", "data")
    os.makedirs(out_dir, exist_ok=True)
    out = os.path.join(out_dir, "live.json")
    with open(out, "w") as f:
        json.dump(snapshot, f, indent=2, ensure_ascii=False)
    _log(f"wrote snapshot -> {os.path.relpath(out, ROOT)}")


if __name__ == "__main__":
    _cli()
