import MetaTrader5 as mt5
from datetime import datetime
from App.api_config import MT5_SERVER , MT5_PASSWORD , MT5_LOGIN

TIMEFRAME_MAP = {
    "1m": mt5.TIMEFRAME_M1,
    "5m": mt5.TIMEFRAME_M5,
    "15m": mt5.TIMEFRAME_M15,
    "30m": mt5.TIMEFRAME_M30,
    "1h": mt5.TIMEFRAME_H1,
    "4h": mt5.TIMEFRAME_H4,
    "1d": mt5.TIMEFRAME_D1
}

def fetch_mt5_candles_by_timeframe(symbol: str, timeframe: str = "1m", bars: int = 100):
    tf = TIMEFRAME_MAP.get(timeframe)
    if tf is None:
        raise ValueError(" Invalid timeframe. Use one of: " + ", ".join(TIMEFRAME_MAP.keys()))

    if not mt5.initialize(login=MT5_LOGIN, password=MT5_PASSWORD, server=MT5_SERVER):
        print(" MT5 init failed:", mt5.last_error())
        return []

    if not mt5.symbol_select(symbol, True):
        print(f" Symbol selection failed: {symbol}")
        mt5.shutdown()
        return []

    raw = mt5.copy_rates_from_pos(symbol, tf, 0, bars)

    if raw is None or len(raw) == 0:
        print(f" No data found for: {symbol}")
        mt5.shutdown()
        return []

    data = [{
        "timestamp": datetime.fromtimestamp(r['time']).strftime('%Y-%m-%d %H:%M'),
        "open": float(r['open']),
        "high": float(r['high']),
        "low": float(r['low']),
        "close": float(r['close']),
        "volume": int(r['tick_volume'])
    } for r in raw]

    mt5.shutdown()
    return data