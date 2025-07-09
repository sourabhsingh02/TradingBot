import requests
from datetime import datetime , timedelta
from App.api_config import ACCESS_TOKEN

def fetch_nse_candles_by_timeframe(symbol: str, timeframe: str = "1m", bars: int = 50):
    end = datetime.now()
    start = end - timedelta(minutes=bars * int(timeframe.replace("m", "")))

    url = "https://api.dhan.co/charts/historical"
    headers = {
        "access-token": ACCESS_TOKEN,
        "Content-Type": "application/json"
    }
    payload = {
        "exchange_segment": "NSE_EQ",
        "instrument": symbol,
        "interval": timeframe,
        "from_date": start.strftime("%Y-%m-%d"),
        "to_date": end.strftime("%Y-%m-%d")
    }

    try:
        res = requests.post(url, headers=headers, json=payload)
        candles = res.json().get("data", [])
        return [
            {
                "timestamp": c["start_time"][:16],
                "open": float(c["open"]),
                "high": float(c["high"]),
                "low": float(c["low"]),
                "close": float(c["close"]),
                "volume": int(c["volume"])
            }
            for c in candles
        ]
    except Exception as e:
        print("[DHAN NSE ERROR]", e)
        return []

    VALID_NSE_TIMEFRAMES = {"1m", "5m", "10m", "15m", "30m", "1h", "1d"}
    if timeframe not in VALID_NSE_TIMEFRAMES:
        raise ValueError(f"Invalid timeframe '{timeframe}'. Use one of: {', '.join(VALID_NSE_TIMEFRAMES)}")