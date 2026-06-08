"""
Polymarket market data — events, market odds, volume ranking, CLOB price/book,
and a live order-book websocket stream.

All read endpoints below are PUBLIC (no API key, no wallet signature). Auth is
only needed to place/manage orders or to use the user/orders websocket channel.

Three hosts:
  Gamma  https://gamma-api.polymarket.com   events + markets metadata, odds, volume
  Data   https://data-api.polymarket.com    trades, holders, positions, activity
  CLOB   https://clob.polymarket.com         live price / order book per token

Gotchas:
  - Gamma paginates with limit / offset (NOT page).
  - Sort with order=<field>&ascending=false (e.g. order=volume_24hr).
  - clobTokenIds and outcomePrices come back as JSON-ENCODED STRINGS, not
    arrays. They need a second json.loads() before indexing (see _decode).
  - The old api.polymarket.com/v1/markets host is dead — use Gamma /markets.

Live data: wss://ws-subscriptions-clob.polymarket.com/ws/market
  subscribe: {"assets_ids": ["<token_id>", ...], "type": "market"}
  keepalive: client sends plaintext "PING" ~every 10s, server replies "PONG"
  events: book (full snapshot), price_change (deltas), last_trade_price
"""
from __future__ import annotations

import json
import sys

import requests

GAMMA = "https://gamma-api.polymarket.com"
DATA = "https://data-api.polymarket.com"
CLOB = "https://clob.polymarket.com"
WS_MARKET = "wss://ws-subscriptions-clob.polymarket.com/ws/market"

_HEADERS = {"Accept": "application/json"}
_TIMEOUT = 20


def _get(url: str, params: dict | None = None) -> object:
    r = requests.get(url, params=params, headers=_HEADERS, timeout=_TIMEOUT)
    r.raise_for_status()
    return r.json()


def _decode(market: dict) -> dict:
    """
    Parse Gamma's JSON-string fields into real lists and pair outcomes with
    their prices. Adds 'odds' = [{outcome, price, token_id}, ...].
    """
    def _arr(v):
        if isinstance(v, str):
            try:
                return json.loads(v)
            except json.JSONDecodeError:
                return [v]
        return v or []

    outcomes = _arr(market.get("outcomes"))
    prices = [_to_f(p) for p in _arr(market.get("outcomePrices"))]
    token_ids = _arr(market.get("clobTokenIds"))
    odds = []
    for i, name in enumerate(outcomes):
        odds.append({
            "outcome": name,
            "price": prices[i] if i < len(prices) else None,
            "token_id": token_ids[i] if i < len(token_ids) else None,
        })
    market["odds"] = odds
    return market


def _to_f(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


# ---- Gamma: events & markets -------------------------------------------------

def events(active: bool = True, closed: bool = False,
           order: str = "volume24hr", ascending: bool = False,
           limit: int = 50, offset: int = 0) -> list[dict]:
    """
    List events. Default: open, sorted by 24h volume, highest first.
    Valid order fields are camelCase: volume24hr, volume, liquidity, endDate.
    (snake_case like volume_24hr is silently ignored by Gamma.)
    """
    return _get(f"{GAMMA}/events", {
        "active": str(active).lower(), "closed": str(closed).lower(),
        "order": order, "ascending": str(ascending).lower(),
        "limit": limit, "offset": offset,
    })


def markets(active: bool = True, closed: bool = False,
            order: str = "volumeNum", ascending: bool = False,
            limit: int = 50, offset: int = 0, **filters) -> list[dict]:
    """
    List markets with odds decoded. Default sort: total volume, highest first.
    Valid order fields are camelCase: volumeNum (total), volume24hr, liquidityNum.
    Extra filters pass through to Gamma, e.g. slug=..., id=...,
    volume_num_min=..., clob_token_ids=..., condition_ids=...
    """
    params = {
        "active": str(active).lower(), "closed": str(closed).lower(),
        "order": order, "ascending": str(ascending).lower(),
        "limit": limit, "offset": offset, **filters,
    }
    return [_decode(m) for m in _get(f"{GAMMA}/markets", params)]


def market_odds(slug: str | None = None, market_id: str | None = None) -> dict | None:
    """Fetch a single market by slug or id and return it with decoded odds."""
    params = {}
    if slug:
        params["slug"] = slug
    if market_id:
        params["id"] = market_id
    if not params:
        raise ValueError("pass slug= or market_id=")
    rows = _get(f"{GAMMA}/markets", params)
    return _decode(rows[0]) if rows else None


def top_markets_by_volume(n: int = 10, page_size: int = 100) -> list[dict]:
    """
    Pull open markets sorted by total volume, highest first. Paginates until n
    are gathered. Each row has 'volumeNum' and decoded 'odds'.
    """
    out: list[dict] = []
    offset = 0
    while len(out) < n:
        batch = markets(order="volumeNum", limit=page_size, offset=offset)
        if not batch:
            break
        out.extend(batch)
        offset += page_size
    return out[:n]


# ---- Data API ----------------------------------------------------------------

def trades(limit: int = 100, offset: int = 0, **filters) -> list[dict]:
    """Recent trades. Filters e.g. market=<conditionId>, user=<0x...>."""
    return _get(f"{DATA}/trades", {"limit": limit, "offset": offset, **filters})


def holders(condition_id: str) -> object:
    """Top holders for a market (by conditionId)."""
    return _get(f"{DATA}/holders", {"market": condition_id})


# ---- CLOB: live price & book -------------------------------------------------

def clob_price(token_id: str, side: str = "BUY") -> float | None:
    """Best bid (side=BUY) or best ask (side=SELL) for a token id."""
    d = _get(f"{CLOB}/price", {"token_id": token_id, "side": side})
    return _to_f(d.get("price"))


def clob_book(token_id: str) -> dict:
    """Full order book: bids (desc), asks (asc), tick_size, last_trade_price..."""
    return _get(f"{CLOB}/book", {"token_id": token_id})


def stream_market(token_ids: list[str], on_message, ping_every: float = 10.0) -> None:
    """
    Blocking live order-book stream for the given token ids. Calls
    on_message(dict) for each event. Requires `websockets` (pip install websockets).
    Press Ctrl-C to stop.
    """
    import asyncio
    import websockets

    async def _run():
        async with websockets.connect(WS_MARKET) as ws:
            await ws.send(json.dumps({"assets_ids": token_ids, "type": "market"}))
            last_ping = 0.0
            loop = asyncio.get_event_loop()
            while True:
                try:
                    msg = await asyncio.wait_for(ws.recv(), timeout=ping_every)
                except asyncio.TimeoutError:
                    await ws.send("PING")
                    continue
                if msg == "PONG":
                    continue
                try:
                    on_message(json.loads(msg))
                except json.JSONDecodeError:
                    on_message({"raw": msg})
                now = loop.time()
                if now - last_ping > ping_every:
                    await ws.send("PING")
                    last_ping = now

    asyncio.run(_run())


def _cli(argv: list[str]) -> None:
    cmd = argv[0] if argv else "top"
    if cmd == "events":
        print(json.dumps(events(limit=int(argv[1]) if len(argv) > 1 else 20), indent=2))
    elif cmd == "top":
        n = int(argv[1]) if len(argv) > 1 else 10
        rows = top_markets_by_volume(n)
        print(json.dumps([{"question": m.get("question"),
                            "volume": m.get("volumeNum"),
                            "odds": m.get("odds")} for m in rows], indent=2))
    elif cmd == "market":
        # market SLUG
        print(json.dumps(market_odds(slug=argv[1]), indent=2))
    elif cmd == "price":
        # price TOKEN_ID [SIDE]
        side = argv[2] if len(argv) > 2 else "BUY"
        print(clob_price(argv[1], side))
    elif cmd == "book":
        print(json.dumps(clob_book(argv[1]), indent=2))
    elif cmd == "stream":
        # stream TOKEN_ID [TOKEN_ID ...]
        stream_market(argv[1:], lambda d: print(json.dumps(d)))
    else:
        print("usage: polymarket.py [events N | top N | market SLUG | "
              "price TOKEN_ID [SIDE] | book TOKEN_ID | stream TOKEN_ID...]")
        sys.exit(1)


if __name__ == "__main__":
    _cli(sys.argv[1:])
