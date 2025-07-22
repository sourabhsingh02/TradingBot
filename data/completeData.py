import MetaTrader5 as mt5
from datetime import datetime, timedelta
import pytz
import pandas as pd
from App.api_config import MT5_LOGIN, MT5_PASSWORD, MT5_SERVER


def fetch_mt5_historical_data(symbol, interval="1d", duration_days=5 * 365):
    timeframes = {
        "1min": mt5.TIMEFRAME_M1,
        "5min": mt5.TIMEFRAME_M5,
        "15min": mt5.TIMEFRAME_M15,
        "1h": mt5.TIMEFRAME_H1,
        "1d": mt5.TIMEFRAME_D1,
    }

    if interval not in timeframes:
        raise ValueError("Invalid interval")

    if not mt5.initialize(login=MT5_LOGIN(), password=MT5_PASSWORD(), server=MT5_SERVER()):
        print("MT5 init failed:", mt5.last_error())
        return []

    if not mt5.symbol_select(symbol, True):
        print(f"Symbol select failed: {symbol}")
        mt5.shutdown()
        return []

    from_date = datetime.now() - timedelta(days=duration_days)
    to_date = datetime.now()

    rates = mt5.copy_rates_range(symbol, timeframes[interval], from_date, to_date)
    mt5.shutdown()

    if rates is None or len(rates) == 0:
        print(f"No historical data found for {symbol}")
        return []

    return [
        {
            "timestamp": datetime.fromtimestamp(int(bar["time"])).strftime("%Y-%m-%d %H:%M"),
            "open": round(bar["open"], 5),
            "high": round(bar["high"], 5),
            "low": round(bar["low"], 5),
            "close": round(bar["close"], 5),
            "volume": int(bar["tick_volume"]),
        }
        for bar in rates
    ]


def fetch_mt5_tick_data(symbol: str, days: int = 1):
    if not mt5.initialize(login=MT5_LOGIN(), password=MT5_PASSWORD(), server=MT5_SERVER()):
        print("MT5 init failed:", mt5.last_error())
        return []

    if not mt5.symbol_select(symbol, True):
        print(f"Symbol select failed: {symbol}")
        mt5.shutdown()
        return []

    from_time = datetime.now() - timedelta(days=days)
    ticks = mt5.copy_ticks_from(symbol, from_time, 500000, mt5.COPY_TICKS_ALL)
    mt5.shutdown()

    if ticks is None or len(ticks) == 0:
        print(f"No tick data found for {symbol}")
        return []

    return [
        {
            "timestamp": datetime.fromtimestamp(int(t["time"])).strftime("%Y-%m-%d %H:%M:%S"),
            "bid": float(t["bid"]),
            "ask": float(t["ask"]),
            "last": float(t["last"]),
            "volume": float(t["volume"]),
            "epoch": int(t["time"])  # Renamed for safety
        }
        for t in ticks
    ]



def fetch_tick_data_last_n_minutes(symbol: str, minutes: int = 1):
    if not mt5.initialize(login=MT5_LOGIN(), password=MT5_PASSWORD(), server=MT5_SERVER()):
        print("MT5 init failed:", mt5.last_error())
        return []

    if not mt5.symbol_select(symbol, True):
        print(f"Symbol select failed: {symbol}")
        mt5.shutdown()
        return []

    from_time = datetime.now() - timedelta(minutes=minutes)
    ticks = mt5.copy_ticks_from(symbol, from_time, 100000, mt5.COPY_TICKS_ALL)

    mt5.shutdown()

    if ticks is None or len(ticks) == 0:
        print(f"No tick data found for {symbol}")
        return []

    return [
        {
            "timestamp": datetime.fromtimestamp(t["time"]).strftime("%Y-%m-%d %H:%M:%S"),
            "bid": float(t["bid"]),
            "ask": float(t["ask"]),
            "last": float(t["last"]),
            "volume": float(t["volume"]),
            "raw_time": int(t["time"])
        }
        for t in ticks
    ]


from datetime import datetime, timedelta

def get_price_change_today_vs_yesterday(symbol):
    try:

        candles = fetch_mt5_historical_data(symbol, interval="1d", duration_days=5)

        if len(candles) < 2:
            return {
                "symbol": symbol,
                "status": "error",
                "reason": "Insufficient candle data (need 2 days)"
            }

        # Use last 2 candles
        yesterday_close = candles[-2]["close"]
        today_close = candles[-1]["close"]

        change = today_close - yesterday_close
        percent_change = (change / yesterday_close) * 100

        sign = "+" if change >= 0 else "-"

        return {
            "symbol": symbol,
            "current_price": round(today_close, 5),
            "yesterday_price": round(yesterday_close, 5),
            "change": round(change, 5),
            "percent_change": round(percent_change, 2),
            "change_str": f"{sign}{abs(round(change, 5))}",
            "percent_change_str": f"{sign}{abs(round(percent_change, 2))}%",
            "status": "success"
        }

    except Exception as e:
        return {
            "symbol": symbol,
            "status": "error",
            "reason": str(e)
        }


