"""
DeFiLlama market data — TVL, stablecoins, DEX volume, fees/revenue, yields,
and historical price charts. Free public API, no key, no auth.

Four hosts (DeFiLlama splits its API across subdomains):
  api.llama.fi          protocols + TVL, DEX volume, fees/revenue overviews
  stablecoins.llama.fi  stablecoin supply (circulating, by chain, history)
  yields.llama.fi       yield/APY pools
  coins.llama.fi        token prices (current + historical chart)

Coin ids for the price endpoints are "{chain}:{address}" or "coingecko:{id}",
e.g. coingecko:hyperliquid, ethereum:0xA0b8..., solana:So111...

Key endpoints used here:
  GET api.llama.fi/protocols                         all protocols (TVL, mcap, chains)
  GET api.llama.fi/protocol/{slug}                   one protocol, full history
  GET api.llama.fi/tvl/{slug}                         current TVL (bare number)
  GET api.llama.fi/v2/chains                          current TVL per chain
  GET api.llama.fi/v2/historicalChainTvl[/{chain}]    TVL history (all / one chain)
  GET api.llama.fi/overview/dexs                       DEX volume leaderboard
  GET api.llama.fi/overview/fees[?dataType=...]        fees/revenue leaderboard
  GET api.llama.fi/summary/dexs/{protocol}             one DEX's volume history
  GET api.llama.fi/summary/fees/{protocol}             one protocol's fees history
  GET stablecoins.llama.fi/stablecoins?includePrices=true   all stablecoins
  GET stablecoins.llama.fi/stablecoincharts/all             total supply history
  GET yields.llama.fi/pools                            all yield pools
  GET coins.llama.fi/prices/current/{coins}            current price(s)
  GET coins.llama.fi/chart/{coins}?span=&period=       historical price chart
"""
from __future__ import annotations

import sys

import requests

API = "https://api.llama.fi"
STABLES = "https://stablecoins.llama.fi"
YIELDS = "https://yields.llama.fi"
COINS = "https://coins.llama.fi"

_HEADERS = {"Accept": "application/json"}
_TIMEOUT = 20


def _get(url: str, params: dict | None = None) -> object:
    r = requests.get(url, params=params, headers=_HEADERS, timeout=_TIMEOUT)
    r.raise_for_status()
    return r.json()


# ---- TVL ---------------------------------------------------------------------

def protocols() -> list[dict]:
    """All protocols with current TVL, chains, category, mcap."""
    return _get(f"{API}/protocols")


def protocol(slug: str) -> dict:
    """One protocol: full TVL history, breakdown by chain and token."""
    return _get(f"{API}/protocol/{slug}")


def protocol_tvl(slug: str) -> float:
    """Current TVL of a protocol as a bare float (e.g. 'hyperliquid')."""
    return float(_get(f"{API}/tvl/{slug}"))


def chains() -> list[dict]:
    """Current TVL per chain, highest first."""
    data = _get(f"{API}/v2/chains")
    data.sort(key=lambda c: c.get("tvl") or 0, reverse=True)
    return data


def chain_tvl_history(chain: str | None = None) -> list[dict]:
    """TVL history [{date, tvl}, ...] for one chain, or all chains if None."""
    url = f"{API}/v2/historicalChainTvl"
    if chain:
        url += f"/{chain}"
    return _get(url)


def top_protocols(n: int = 20, chain: str | None = None,
                  category: str | None = None) -> list[dict]:
    """Top protocols by TVL, optionally filtered to a chain or category."""
    rows = protocols()
    if chain:
        rows = [p for p in rows if chain in (p.get("chains") or [])]
    if category:
        rows = [p for p in rows if p.get("category") == category]
    rows.sort(key=lambda p: p.get("tvl") or 0, reverse=True)
    return [{"name": p.get("name"), "tvl": p.get("tvl"),
             "category": p.get("category"), "chains": p.get("chains"),
             "change_7d": p.get("change_7d")} for p in rows[:n]]


# ---- Stablecoins -------------------------------------------------------------

def stablecoins(include_prices: bool = True) -> list[dict]:
    """
    All stablecoins with circulating supply. Each row's 'circulating' is a dict
    like {'peggedUSD': <amount>}. Sorted by USD circulating, highest first.
    """
    data = _get(f"{STABLES}/stablecoins",
                {"includePrices": str(include_prices).lower()})
    rows = data.get("peggedAssets", data) if isinstance(data, dict) else data

    def _circ(p):
        c = p.get("circulating") or {}
        return c.get("peggedUSD") or 0
    rows.sort(key=_circ, reverse=True)
    return rows


def stablecoin_supply_history() -> list[dict]:
    """Total stablecoin market-cap history across all chains."""
    return _get(f"{STABLES}/stablecoincharts/all")


# ---- DEX volume & fees -------------------------------------------------------

def dex_overview(chain: str | None = None) -> dict:
    """
    DEX volume leaderboard. Returns {total24h, total7d, protocols: [...]}.
    Pass chain to scope to one chain's DEXs.
    """
    params = {"excludeTotalDataChart": "true",
              "excludeTotalDataChartBreakdown": "true"}
    url = f"{API}/overview/dexs"
    if chain:
        url += f"/{chain}"
    return _get(url, params)


def fees_overview(data_type: str = "dailyFees", chain: str | None = None) -> dict:
    """
    Fees/revenue leaderboard. data_type: 'dailyFees' or 'dailyRevenue'.
    Returns {total24h, protocols: [...]}.
    """
    params = {"excludeTotalDataChart": "true",
              "excludeTotalDataChartBreakdown": "true",
              "dataType": data_type}
    url = f"{API}/overview/fees"
    if chain:
        url += f"/{chain}"
    return _get(url, params)


def protocol_volume(slug: str) -> dict:
    """One DEX protocol's volume summary + history (e.g. 'hyperliquid')."""
    return _get(f"{API}/summary/dexs/{slug}")


def protocol_fees(slug: str, data_type: str = "dailyFees") -> dict:
    """One protocol's fees/revenue summary + history."""
    return _get(f"{API}/summary/fees/{slug}", {"dataType": data_type})


# ---- Yields ------------------------------------------------------------------

def yield_pools(project: str | None = None, chain: str | None = None,
                min_tvl: float = 0) -> list[dict]:
    """Yield pools, optionally filtered by project/chain/min TVL, by APY desc."""
    rows = _get(f"{YIELDS}/pools").get("data", [])
    if project:
        rows = [p for p in rows if p.get("project") == project]
    if chain:
        rows = [p for p in rows if p.get("chain") == chain]
    rows = [p for p in rows if (p.get("tvlUsd") or 0) >= min_tvl]
    rows.sort(key=lambda p: p.get("apy") or 0, reverse=True)
    return rows


# ---- Prices ------------------------------------------------------------------

def price(coins: str | list[str]) -> dict:
    """
    Current price(s). coins = "coingecko:hyperliquid" or "{chain}:{address}",
    or a list of such ids. Returns {coins: {id: {price, symbol, timestamp}}}.
    """
    if isinstance(coins, (list, tuple)):
        coins = ",".join(coins)
    return _get(f"{COINS}/prices/current/{coins}")


def price_chart(coins: str | list[str], span: int = 30, period: str = "1d") -> dict:
    """Historical price chart. span = #points, period e.g. '1d','1h'."""
    if isinstance(coins, (list, tuple)):
        coins = ",".join(coins)
    return _get(f"{COINS}/chart/{coins}", {"span": span, "period": period})


def _cli(argv: list[str]) -> None:
    import json
    cmd = argv[0] if argv else "chains"
    if cmd == "chains":
        n = int(argv[1]) if len(argv) > 1 else 15
        print(json.dumps([{"name": c["name"], "tvl": c.get("tvl")}
                          for c in chains()[:n]], indent=2))
    elif cmd == "tvl":
        # tvl SLUG
        print(protocol_tvl(argv[1]))
    elif cmd == "protocols":
        # protocols N [chain]
        n = int(argv[1]) if len(argv) > 1 else 20
        ch = argv[2] if len(argv) > 2 else None
        print(json.dumps(top_protocols(n, chain=ch), indent=2))
    elif cmd == "stables":
        n = int(argv[1]) if len(argv) > 1 else 10
        rows = stablecoins()[:n]
        print(json.dumps([{"symbol": p.get("symbol"), "name": p.get("name"),
                           "circulating_usd": (p.get("circulating") or {}).get("peggedUSD")}
                          for p in rows], indent=2))
    elif cmd == "dexs":
        ch = argv[1] if len(argv) > 1 else None
        d = dex_overview(ch)
        ps = sorted(d.get("protocols") or [], key=lambda p: p.get("total24h") or 0, reverse=True)
        print(json.dumps({"total24h": d.get("total24h"),
                          "top": [{"name": p.get("name"), "vol24h": p.get("total24h")}
                                  for p in ps[:10]]}, indent=2))
    elif cmd == "fees":
        dt = argv[1] if len(argv) > 1 else "dailyFees"
        d = fees_overview(dt)
        ps = sorted(d.get("protocols") or [], key=lambda p: p.get("total24h") or 0, reverse=True)
        print(json.dumps({"total24h": d.get("total24h"),
                          "top": [{"name": p.get("name"), "fees24h": p.get("total24h")}
                                  for p in ps[:10]]}, indent=2))
    elif cmd == "yields":
        # yields PROJECT [chain]
        proj = argv[1] if len(argv) > 1 else None
        ch = argv[2] if len(argv) > 2 else None
        rows = yield_pools(project=proj, chain=ch, min_tvl=1_000_000)[:15]
        print(json.dumps([{"project": p.get("project"), "symbol": p.get("symbol"),
                           "chain": p.get("chain"), "apy": p.get("apy"),
                           "tvlUsd": p.get("tvlUsd")} for p in rows], indent=2))
    elif cmd == "price":
        print(json.dumps(price(argv[1] if len(argv) > 1 else "coingecko:hyperliquid"), indent=2))
    else:
        print("usage: defillama.py [chains N | tvl SLUG | protocols N [chain] | "
              "stables N | dexs [chain] | fees [dailyFees|dailyRevenue] | "
              "yields PROJECT [chain] | price COIN_ID]")
        sys.exit(1)


if __name__ == "__main__":
    _cli(sys.argv[1:])
