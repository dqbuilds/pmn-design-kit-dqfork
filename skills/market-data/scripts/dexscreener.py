"""
DexScreener market data — DEX pair price, liquidity, and volume by token.

Public API, no key. Use for on-chain DEX liquidity/volume on any token across
chains (the squeeze_pipeline has a heavier version that also pulls holder
counts via Solscan/Helius — this is the slim, key-free subset).

  GET https://api.dexscreener.com/latest/dex/tokens/{address}   pairs for a token
  GET https://api.dexscreener.com/latest/dex/search?q={query}   search pairs
"""
from __future__ import annotations

import sys

import requests

_BASE = "https://api.dexscreener.com/latest/dex"
_HEADERS = {"Accept": "application/json"}
_TIMEOUT = 15


def _get(path: str, params: dict | None = None) -> dict:
    r = requests.get(f"{_BASE}{path}", params=params, headers=_HEADERS, timeout=_TIMEOUT)
    r.raise_for_status()
    return r.json()


def _slim(pair: dict) -> dict:
    return {
        "chain": pair.get("chainId"),
        "dex": pair.get("dexId"),
        "pair": (pair.get("baseToken", {}).get("symbol", "") + "/"
                 + pair.get("quoteToken", {}).get("symbol", "")),
        "price_usd": _to_f(pair.get("priceUsd")),
        "liquidity_usd": (pair.get("liquidity") or {}).get("usd"),
        "volume_24h": (pair.get("volume") or {}).get("h24"),
        "price_change_24h": (pair.get("priceChange") or {}).get("h24"),
        "url": pair.get("url"),
    }


def _to_f(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def token_pairs(address: str, slim: bool = True) -> list[dict]:
    """All DEX pairs for a token address (most-liquid first if slim)."""
    pairs = _get(f"/tokens/{address}").get("pairs") or []
    if not slim:
        return pairs
    rows = [_slim(p) for p in pairs]
    rows.sort(key=lambda r: r["liquidity_usd"] or 0, reverse=True)
    return rows


def search(query: str, slim: bool = True) -> list[dict]:
    """Search pairs by symbol/name/address."""
    pairs = _get("/search", {"q": query}).get("pairs") or []
    return [_slim(p) for p in pairs] if slim else pairs


def _cli(argv: list[str]) -> None:
    import json
    cmd = argv[0] if argv else "search"
    if cmd == "token":
        print(json.dumps(token_pairs(argv[1]), indent=2))
    elif cmd == "search":
        print(json.dumps(search(argv[1]), indent=2))
    else:
        print("usage: dexscreener.py [token ADDRESS | search QUERY]")
        sys.exit(1)


if __name__ == "__main__":
    _cli(sys.argv[1:])
