"""
Hyperliquid market data — perps stats and OHLCV candles.

Public read endpoint, no API key, no auth. Aggregated REST limit is
1200 weight/min per IP (allMids = weight 2, most info reqs = 20,
candleSnapshot adds weight per 60 candles returned).

  POST https://api.hyperliquid.xyz/info
  Content-Type: application/json

Request bodies used here:
  {"type":"metaAndAssetCtxs","dex":""}     perp meta + per-asset contexts
  {"type":"allMids","dex":""}              all mid prices
  {"type":"candleSnapshot","req":{...}}    OHLCV history for one coin
  {"type":"spotMetaAndAssetCtxs"}          spot meta + contexts

Notes:
  - metaAndAssetCtxs returns a 2-element array: [meta, assetCtxs]. The two
    inner arrays are index-aligned: universe[i] describes assetCtxs[i].
  - All numeric values come back as STRINGS — cast before doing math.
  - For HIP-3 (builder-deployed) assets, prefix the coin with the dex name,
    e.g. "xyz:XYZ100", and pass dex="xyz".

Live data: wss://api.hyperliquid.xyz/ws
  {"method":"subscribe","subscription":{"type":"allMids","dex":""}}
  {"method":"subscribe","subscription":{"type":"candle","coin":"BTC","interval":"1h"}}
  {"method":"subscribe","subscription":{"type":"l2Book","coin":"BTC"}}
"""
from __future__ import annotations

import sys
import time

import requests

_BASE = "https://api.hyperliquid.xyz/info"
_HEADERS = {"Content-Type": "application/json"}
_TIMEOUT = 15  # seconds per request

# candleSnapshot interval strings accepted by the API.
INTERVALS = {
    "1m", "3m", "5m", "15m", "30m",
    "1h", "2h", "4h", "8h", "12h",
    "1d", "3d", "1w", "1M",
}


def _post(body: dict) -> object:
    r = requests.post(_BASE, headers=_HEADERS, json=body, timeout=_TIMEOUT)
    r.raise_for_status()
    return r.json()


def _f(x):
    """Cast Hyperliquid's stringified numbers to float, tolerating None."""
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def perp_contexts(dex: str = "") -> list[dict]:
    """
    Return one row per perp, merging universe metadata with live context.

    Keys: name, mark_px, oracle_px, mid_px, prev_day_px, funding,
          open_interest, day_ntl_vlm (24h notional volume), premium,
          max_leverage. Numerics are floats.
    """
    meta, ctxs = _post({"type": "metaAndAssetCtxs", "dex": dex})
    universe = meta["universe"]
    out = []
    for asset, ctx in zip(universe, ctxs):
        out.append({
            "name": asset.get("name"),
            "max_leverage": asset.get("maxLeverage"),
            "mark_px": _f(ctx.get("markPx")),
            "oracle_px": _f(ctx.get("oraclePx")),
            "mid_px": _f(ctx.get("midPx")),
            "prev_day_px": _f(ctx.get("prevDayPx")),
            "funding": _f(ctx.get("funding")),
            "open_interest": _f(ctx.get("openInterest")),
            "day_ntl_vlm": _f(ctx.get("dayNtlVlm")),
            "premium": _f(ctx.get("premium")),
        })
    return out


def all_mids(dex: str = "") -> dict:
    """Map coin -> mid price (float). Cheapest call (weight 2)."""
    raw = _post({"type": "allMids", "dex": dex})
    return {k: _f(v) for k, v in raw.items()}


def candles(coin: str, interval: str, start_ms: int, end_ms: int) -> list[dict]:
    """
    OHLCV candles for one coin between start_ms and end_ms (epoch millis).

    Returns dicts with: t (open ms), T (close ms), o, h, l, c, v, n (#trades).
    """
    if interval not in INTERVALS:
        raise ValueError(f"interval {interval!r} not in {sorted(INTERVALS)}")
    raw = _post({
        "type": "candleSnapshot",
        "req": {"coin": coin, "interval": interval,
                "startTime": int(start_ms), "endTime": int(end_ms)},
    })
    return [{
        "t": c["t"], "T": c["T"],
        "o": _f(c["o"]), "h": _f(c["h"]), "l": _f(c["l"]), "c": _f(c["c"]),
        "v": _f(c["v"]), "n": c.get("n"),
    } for c in raw]


def candles_lookback(coin: str, interval: str, days: float) -> list[dict]:
    """Convenience: candles for the last `days` days up to now."""
    now_ms = int(time.time() * 1000)
    start_ms = now_ms - int(days * 86_400_000)
    return candles(coin, interval, start_ms, now_ms)


def spot_contexts() -> list[dict]:
    """Spot pairs with day volume / mark / mid / prev-day price (floats)."""
    meta, ctxs = _post({"type": "spotMetaAndAssetCtxs"})
    universe = meta["universe"]
    out = []
    for asset, ctx in zip(universe, ctxs):
        out.append({
            "name": asset.get("name"),
            "mark_px": _f(ctx.get("markPx")),
            "mid_px": _f(ctx.get("midPx")),
            "prev_day_px": _f(ctx.get("prevDayPx")),
            "day_ntl_vlm": _f(ctx.get("dayNtlVlm")),
        })
    return out


def perp_dexs() -> list[dict]:
    """
    Builder-deployed perp dexs (HIP-3), e.g. 'xyz' (trade.xyz pre-IPO/equities),
    'vntl' (Ventuals valuation perps). Excludes the default book.
    """
    return [d for d in _post({"type": "perpDexs"}) if d]


def all_perp_contexts(include_default: bool = True) -> list[dict]:
    """
    perp_contexts across the default book + every HIP-3 builder dex. Each row
    gets a 'dex' key (''=default). Builder-dex coin names are dex-prefixed
    (e.g. 'xyz:SPCX'), which is how the API returns them.
    """
    out = []
    if include_default:
        for r in perp_contexts(""):
            r["dex"] = ""
            out.append(r)
    for d in perp_dexs():
        try:
            for r in perp_contexts(d["name"]):
                r["dex"] = d["name"]
                out.append(r)
        except Exception:
            continue
    return out


def find_perp(symbol: str) -> list[dict]:
    """
    Find a perp by ticker across the default book and all HIP-3 dexs. Matches
    bare ('SPCX') or prefixed ('xyz:SPCX'). Useful for pre-IPO / equity perps.
    """
    s = symbol.upper().split(":")[-1]
    return [r for r in all_perp_contexts()
            if (r["name"] or "").upper().split(":")[-1] == s]


def _cli(argv: list[str]) -> None:
    import json
    cmd = argv[0] if argv else "perps"
    if cmd == "perps":
        rows = sorted(perp_contexts(), key=lambda r: r["day_ntl_vlm"] or 0, reverse=True)
        n = int(argv[1]) if len(argv) > 1 else 20
        print(json.dumps(rows[:n], indent=2))
    elif cmd == "mids":
        print(json.dumps(all_mids(), indent=2))
    elif cmd == "candles":
        # candles COIN INTERVAL DAYS
        coin = argv[1]
        interval = argv[2] if len(argv) > 2 else "1h"
        days = float(argv[3]) if len(argv) > 3 else 30
        print(json.dumps(candles_lookback(coin, interval, days), indent=2))
    elif cmd == "spot":
        print(json.dumps(spot_contexts(), indent=2))
    elif cmd == "perpdexs":
        print(json.dumps([{"name": d["name"], "deployer": d.get("deployer")}
                          for d in perp_dexs()], indent=2))
    elif cmd == "dex":
        # dex NAME [N] — one builder dex's board by 24h volume
        name = argv[1]
        rows = sorted(perp_contexts(name), key=lambda r: r["day_ntl_vlm"] or 0, reverse=True)
        n = int(argv[2]) if len(argv) > 2 else 30
        print(json.dumps(rows[:n], indent=2))
    elif cmd == "find":
        # find SYMBOL [SYMBOL ...] — locate ticker(s) across all dexs
        rows = [r for sym in argv[1:] for r in find_perp(sym)]
        print(json.dumps([{"coin": r["name"], "dex": r["dex"], "mark_px": r["mark_px"],
                           "day_ntl_vlm": r["day_ntl_vlm"], "open_interest": r["open_interest"]}
                          for r in rows], indent=2))
    else:
        print("usage: hyperliquid.py [perps N | mids | candles COIN INTERVAL DAYS | "
              "spot | perpdexs | dex NAME [N] | find SYMBOL...]")
        sys.exit(1)


if __name__ == "__main__":
    _cli(sys.argv[1:])
