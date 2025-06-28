import yfinance as yf
import requests
from datetime import datetime, timedelta
from api_config import API_KEY, ACCESS_TOKEN
from api_config import USE_DHAN
# 🟢 Use yfinance for testing, Dhan for production

# USE_DHAN = False

def fetch_ohlcv(symbol: str):
    if USE_DHAN:
        return fetch_from_dhan(symbol)
    else:
        return fetch_from_yfinance(symbol)

#  Dummy using yfinance
def fetch_from_yfinance(symbol: str):
    symbol = symbol.upper()
    if not symbol.endswith(".NS"):
        symbol += ".NS"

    end_date = datetime.now()
    start_date = end_date - timedelta(days=5)

    df = yf.download(symbol, start=start_date.strftime("%Y-%m-%d"), end=end_date.strftime("%Y-%m-%d"), interval="1d")

    if df.empty:
        return []
    data = []
    for index, row in df.iterrows():
        data.append({
            "timestamp": index.strftime("%Y-%m-%d"),
            "open": round(row['Open'], 2),
            "high": round(row['High'], 2),
            "low": round(row['Low'], 2),
            "close": round(row['Close'], 2),
            "volume": int(row['Volume'])
        })
    return data

#  Real Dhan integration (placeholder)
def fetch_from_dhan(symbol: str):
    url = "https://api.dhan.co/charts/historical"
    headers = {
        "access-token": ACCESS_TOKEN,
        "Content-Type": "application/json"
    }
    payload = {
        "security_id": "1234",  # replace with real ID
        "exchange_segment": "NSE_EQ",
        "instrument": symbol,
        "interval": "1d",
        "from_date": "2024-06-01",
        "to_date": "2024-06-25"
    }

    try:
        res = requests.post(url, headers=headers, json=payload)
        json_data = res.json()
        return json_data.get("data", [])
    except Exception as e:
        print("[ERROR]", e)
        return []


SYMBOL_LIST = ["RELIANCE", "TCS", "INFY", "SBIN", "HDFCBANK", "ICICIBANK"]

def fetch_all_latest() -> list:
    result = []

    for symbol in SYMBOL_LIST:
        candles = fetch_ohlcv(symbol)
        if not candles or len(candles) < 2:
            print(f"⚠️ Skipping {symbol} due to no data")
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

    return result
