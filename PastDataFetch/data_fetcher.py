import yfinance as yf
import requests, MetaTrader5 as mt5
from datetime import datetime, timedelta
from SymbolsPairs.forexSymbols import fetch_all_forex_symbols
from SymbolsPairs.nseSymbols import fetch_all_nse_symbols
from App.api_config import (
    ACCESS_TOKEN, USE_DHAN, USE_DUMMY_DATA,
    MT5_LOGIN, MT5_PASSWORD, MT5_SERVER
)

def fetch_ohlcv(symbol: str, market: str = "nse" , ):
    if market == "nse" :
        if USE_DUMMY_DATA:
            return fetch_from_dummy(symbol)
        return fetch_from_dhan(symbol) if USE_DHAN else (
fetch_from_yfinance(symbol))

    elif market == "forex":
        if USE_DUMMY_DATA:
            return fetch_from_dummy(symbol)
        return fetch_from_mt5(symbol)

        raise ValueError("market must be 'nse' or 'forex'")

# ───────────────────────── Dummy data
def fetch_from_dummy(symbol: str, days: int = 30):
    today = datetime.now()
    return [
        {"timestamp": (today - timedelta(days=i)).strftime("%Y-%m-%d"),
         "open": 100+i, "high":105+i, "low":95+i, "close":100+i,
         "volume": 100_000+i*10}
        for i in range(days)
    ]

# ───────────────────────── NSE via YFinance
def fetch_from_yfinance(symbol: str):
    symbol = (symbol.upper() if symbol.upper().endswith(".NS") else symbol.upper()+".NS")
    start = datetime.now() - timedelta(days=100)
    df = yf.download(symbol, start=start.strftime("%Y-%m-%d"),
                     end=datetime.now().strftime("%Y-%m-%d"), interval="1d")
    if df.empty:
        return []
    return [{"timestamp": idx.strftime("%Y-%m-%d"),
             "open":round(r.Open,2),"high":round(r.High,2),
             "low":round(r.Low,2),"close":round(r.Close,2),
             "volume":int(r.Volume)} for idx,r in df.iterrows()]

# ───────────────────────── NSE via Dhan
def fetch_from_dhan(symbol: str):
    url = "https://api.dhan.co/charts/historical"
    hdr = {"access-token": ACCESS_TOKEN, "Content-Type":"application/json"}
    start = (datetime.now()-timedelta(days=100)).strftime("%Y-%m-%d")
    end   = datetime.now().strftime("%Y-%m-%d")
    payload = {"exchange_segment":"NSE_EQ","instrument":symbol,
               "interval":"1d","from_date":start,"to_date":end}
    try:
        candles = requests.post(url, headers=hdr, json=payload).json().get("data",[])
        return [{"timestamp":c["start_time"][:10],
                 "open":float(c["open"]), "high":float(c["high"]),
                 "low":float(c["low"]),  "close":float(c["close"]),
                 "volume":int(c["volume"])} for c in candles]
    except Exception as e:
        print("[DHAN ERROR]", e); return []

# ───────────────────────── FOREX via MT5 -------------------------------
def _mt5_connect():
    return mt5.initialize(login=MT5_LOGIN, password=MT5_PASSWORD, server=MT5_SERVER)

def fetch_from_mt5(symbol: str, bars: int = 500):
    if not mt5.initialize(login=MT5_LOGIN, password=MT5_PASSWORD, server=MT5_SERVER):
        print(" MT5 init failed:", mt5.last_error())
        return []

    if not mt5.symbol_select(symbol, True):
        print(f"Symbol selection failed: {symbol}")
        mt5.shutdown()
        return []

    raw = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_D1, 0, bars)

    if raw is None or len(raw) == 0:
        print(f"No data found for: {symbol}")
        mt5.shutdown()
        return []

    data = [{
        "timestamp": datetime.fromtimestamp(r['time']).strftime('%Y-%m-%d'),
        "open": float(r['open']),
        "high": float(r['high']),
        "low": float(r['low']),
        "close": float(r['close']),
        "volume": int(r['tick_volume'])
    } for r in raw]

    mt5.shutdown()
    return data

def fetch_all_paginated(page: int = 1, size: int = 10, market: str = "nse", filter_type: str = "all") -> dict:
    symbols = fetch_all_nse_symbols() if market == "nse" else fetch_all_forex_symbols()
    total = len(symbols)
    selected_symbols = symbols[(page - 1) * size : page * size]

    result = []

    for symbol in selected_symbols:
        candles = fetch_ohlcv(symbol, market)
        if not candles or len(candles) < 2:
          continue

        last = candles[-1]
        prev = candles[-2]

        close = last["close"]
        prev_close = prev["close"]

        try:
            change_percent = round(((close - prev_close) / prev_close) * 100, 2)
        except ZeroDivisionError:
            change_percent = 0.0

        result.append({
            "symbol": symbol,
            "close": close,
            "prev_close": prev_close,
            "change_percent": change_percent,
            "timestamp": last["timestamp"]
        })

    if filter_type == "gainers":
        result = sorted(result, key=lambda x: x["change_percent"], reverse=True)
    elif filter_type == "losers":
        result = sorted(result, key=lambda x: x["change_percent"])
    elif filter_type == "volatile":
        result = sorted(result, key=lambda x: abs(x["change_percent"]), reverse=True)

    return {
        "market": market,
        "page": page,
        "page_size": size,
        "total": total,
        "data": result
    }





