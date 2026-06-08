"""
CoinGecko market data — price, market cap, volume, and historical charts.

Use for cross-ecosystem context (it isn't HL/Polymarket-native, so it's the
lower-tier source — prefer Hyperliquid /info for on-chain HL perps truth).

Free/Demo base:  https://api.coingecko.com/api/v3
  Anonymous shared IP: ~30 calls/min.
  With a free Demo key: 100 calls/min, 10k/month. Pass it as the
  x-cg-demo-api-key header. Set COINGECKO_API_KEY in the environment to use it.
  (The pro-api.coingecko.com host needs a paid key — not used here.)

HYPE coin id is "hyperliquid" (symbol HYPE). Find any id with search().

Endpoints used:
  GET /simple/price?ids=&vs_currencies=&include_market_cap=&include_24hr_vol=
  GET /coins/{id}
  GET /coins/{id}/market_chart?vs_currency=&days=&interval=   -> [ts_ms, value]
  GET /coins/{id}/ohlc?vs_currency=&days=                     -> [ts_ms,o,h,l,c]
  GET /search?query=
"""
from __future__ import annotations

import os
import sys

import requests

_BASE = "https://api.coingecko.com/api/v3"
_TIMEOUT = 20


def _headers() -> dict:
    h = {"Accept": "application/json"}
    key = os.environ.get("COINGECKO_API_KEY")
    if key:
        h["x-cg-demo-api-key"] = key
    return h


def _get(path: str, params: dict | None = None) -> object:
    r = requests.get(f"{_BASE}{path}", params=params, headers=_headers(), timeout=_TIMEOUT)
    r.raise_for_status()
    return r.json()


def simple_price(ids: str | list[str], vs: str = "usd",
                 market_cap: bool = True, vol_24h: bool = True,
                 change_24h: bool = True) -> dict:
    """Lightweight price + market data for one or more coin ids."""
    if isinstance(ids, (list, tuple)):
        ids = ",".join(ids)
    return _get("/simple/price", {
        "ids": ids, "vs_currencies": vs,
        "include_market_cap": str(market_cap).lower(),
        "include_24hr_vol": str(vol_24h).lower(),
        "include_24hr_change": str(change_24h).lower(),
    })


def coin(coin_id: str) -> dict:
    """Full coin object: market_data, supply, contracts, tickers."""
    return _get(f"/coins/{coin_id}", {
        "localization": "false", "tickers": "false",
        "community_data": "false", "developer_data": "false",
    })


def market_chart(coin_id: str, days: int | str = 30,
                 interval: str | None = None, vs: str = "usd") -> dict:
    """
    Historical prices/market_caps/volumes as [timestamp_ms, value] arrays.
    days = int or "max"; interval = "5m" | "hourly" | "daily" (omit for auto).
    """
    params = {"vs_currency": vs, "days": days}
    if interval:
        params["interval"] = interval
    return _get(f"/coins/{coin_id}/market_chart", params)


def ohlc(coin_id: str, days: int | str = 30, vs: str = "usd") -> list[list]:
    """OHLC candles as [timestamp_ms, open, high, low, close]."""
    return _get(f"/coins/{coin_id}/ohlc", {"vs_currency": vs, "days": days})


def search(query: str) -> dict:
    """Resolve a name/symbol to a coin id."""
    return _get("/search", {"query": query})


def _cli(argv: list[str]) -> None:
    import json
    cmd = argv[0] if argv else "price"
    if cmd == "price":
        ids = argv[1] if len(argv) > 1 else "hyperliquid"
        print(json.dumps(simple_price(ids), indent=2))
    elif cmd == "coin":
        print(json.dumps(coin(argv[1]), indent=2))
    elif cmd == "chart":
        # chart ID DAYS [INTERVAL]
        cid = argv[1]
        days = argv[2] if len(argv) > 2 else 30
        interval = argv[3] if len(argv) > 3 else None
        print(json.dumps(market_chart(cid, days, interval), indent=2))
    elif cmd == "ohlc":
        cid = argv[1]
        days = argv[2] if len(argv) > 2 else 30
        print(json.dumps(ohlc(cid, days), indent=2))
    elif cmd == "search":
        print(json.dumps(search(argv[1]), indent=2))
    else:
        print("usage: coingecko.py [price IDS | coin ID | chart ID DAYS [INTERVAL] | "
              "ohlc ID DAYS | search QUERY]")
        sys.exit(1)


if __name__ == "__main__":
    _cli(sys.argv[1:])
