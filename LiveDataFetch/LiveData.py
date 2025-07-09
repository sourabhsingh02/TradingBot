from LiveDataFetch.ForexHelper import fetch_mt5_candles_by_timeframe
from LiveDataFetch.NseHelper import fetch_nse_candles_by_timeframe


def fetch_live_candles(symbol: str, market: str, timeframe: str = "5m", bars: int = 50):
    if market == "nse":
        return fetch_nse_candles_by_timeframe(symbol, timeframe, bars)
    elif market == "forex":
        return fetch_mt5_candles_by_timeframe(symbol, timeframe, bars)
    else:
        raise ValueError("Market must be 'nse' or 'forex'")