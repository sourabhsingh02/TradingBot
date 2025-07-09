from LiveDataFetch.LiveData import fetch_live_candles
from SymbolsPairs.forexSymbols import fetch_all_forex_symbols
import MetaTrader5 as mt5
from datetime import datetime
from App.api_config import MT5_LOGIN, MT5_PASSWORD, MT5_SERVER

def get_forex_paginated(page:int=1, size:int=10, filter_type:str="all"):
    symbols = fetch_all_forex_symbols()
    total   = len(symbols)
    selected= symbols[(page-1)*size : page*size]

    rows=[]
    for s in selected:
        candles = fetch_live_candles(s, market="forex")
        if len(candles)<2: continue
        last, prev = candles[-1], candles[-2]
        change = round((last["close"]-prev["close"])/prev["close"]*100,2)
        rows.append({"symbol":s,"close":last["close"],"prev_close":prev["close"],
                     "change_percent":change,"timestamp":last["timestamp"]})

    if filter_type=="gainers":
        rows.sort(key=lambda x: x["change_percent"], reverse=True)
    elif filter_type=="losers":
        rows.sort(key=lambda x: x["change_percent"])
    elif filter_type=="volatile":
        rows.sort(key=lambda x: abs(x["change_percent"]), reverse=True)

    return {"market":"forex","page":page,"page_size":size,"total":total,"data":rows}
# TIMEFRAME_MAP = {
#     "1m": mt5.TIMEFRAME_M1,
#     "5m": mt5.TIMEFRAME_M5,
#     "15m": mt5.TIMEFRAME_M15,
#     "30m": mt5.TIMEFRAME_M30,
#     "1h": mt5.TIMEFRAME_H1,
#     "4h": mt5.TIMEFRAME_H4,
#     "1d": mt5.TIMEFRAME_D1
# }

# def fetch_mt5_candles_by_timeframe(symbol: str, timeframe: str = "5m", bars: int = 100):
#     tf = TIMEFRAME_MAP.get(timeframe)
#     if tf is None:
#         raise ValueError(" Invalid timeframe. Use one of: " + ", ".join(TIMEFRAME_MAP.keys()))
#
#     if not mt5.initialize(login=MT5_LOGIN, password=MT5_PASSWORD, server=MT5_SERVER):
#         print(" MT5 init failed:", mt5.last_error())
#         return []
#
#     if not mt5.symbol_select(symbol, True):
#         print(f" Symbol selection failed: {symbol}")
#         mt5.shutdown()
#         return []
#
#     raw = mt5.copy_rates_from_pos(symbol, tf, 0, bars)
#
#     if raw is None or len(raw) == 0:
#         print(f" No data found for: {symbol}")
#         mt5.shutdown()
#         return []
#
#     data = [{
#         "timestamp": datetime.fromtimestamp(r['time']).strftime('%Y-%m-%d %H:%M'),
#         "open": float(r['open']),
#         "high": float(r['high']),
#         "low": float(r['low']),
#         "close": float(r['close']),
#         "volume": int(r['tick_volume'])
#     } for r in raw]
#
#     mt5.shutdown()
#     return data