import yfinance as yf
import requests
from datetime import datetime, timedelta
from api_config import API_KEY, ACCESS_TOKEN
from api_config import USE_DHAN , USE_DUMMY_DATA
from symbols_utils import fetch_all_symbols
from datetime import datetime, timedelta

# USE_DHAN = False

# def fetch_ohlcv(symbol: str):
#     if USE_DHAN:
#         return fetch_from_dhan(symbol)
#     else:
#         return fetch_from_yfinance(symbol)




def fetch_ohlcv(symbol: str):
    if USE_DUMMY_DATA:
        return fetch_dummy_data(symbol)
    if USE_DHAN:
        return fetch_from_dhan(symbol)
    return fetch_from_yfinance(symbol)

# Dummy  (tesing)
def fetch_dummy_data(symbol: str):
    today = datetime.now()
    return [
        {
            "timestamp": (today - timedelta(days=i)).strftime("%Y-%m-%d"),
            "open": 100 + i,
            "high": 105 + i,
            "low": 95 + i,
            "close": 100 + i,
            "volume": 100000 + i * 10
        }
        for i in range(30)
    ]


def fetch_from_yfinance(symbol: str):
    symbol = symbol.upper()
    if not symbol.endswith(".NS"):
        symbol += ".NS"

    end_date = datetime.now()
    start_date = end_date - timedelta(days=100)
    try :
        df = yf.download(symbol, start=start_date.strftime("%Y-%m-%d"), end=end_date.strftime("%Y-%m-%d"), interval="1d")
    except Exception as e:
        print(f"[YFINANCE ERROR] {symbol}: {e}")
        return []

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




def fetch_from_dhan(symbol: str):
    url = "https://api.dhan.co/charts/historical"
    headers = {
        "access-token": ACCESS_TOKEN,
        "Content-Type": "application/json"
    }

    end_date = datetime.now()
    start_date = end_date - timedelta(days=100)

    payload = {
        "security_id": "1234",  # Replace with actual ID if required
        "exchange_segment": "NSE_EQ",
        "instrument": symbol,
        "interval": "1d",
        "from_date": start_date.strftime("%Y-%m-%d"),
        "to_date": end_date.strftime("%Y-%m-%d")
    }

    try:
        res = requests.post(url, headers=headers, json=payload)
        res.raise_for_status()
        json_data = res.json()
        candles = json_data.get("data", [])

        # Normalize format like YFinance
        formatted = []
        for item in candles:
            formatted.append({
                "timestamp": item.get("start_time", "")[:10],  # remove time part
                "open": float(item.get("open", 0)),
                "high": float(item.get("high", 0)),
                "low": float(item.get("low", 0)),
                "close": float(item.get("close", 0)),
                "volume": int(item.get("volume", 0))
            })

        return formatted

    except Exception as e:
        print("[ERROR]", e)
        return []

def fetch_all_paginated(page: int = 1, size: int = 10, filter_type: str = "all") -> dict:
    all_symbols = fetch_all_symbols()
    total = len(all_symbols)

    start = (page - 1) * size
    end = start + size
    selected_symbols = all_symbols[start:end]

    result = []

    for symbol in selected_symbols:
        candles = fetch_ohlcv(symbol)
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

    # Agar filter_type 'all' ho toh koi sorting/filtering na kare
    if filter_type == "gainers":
        result = sorted(result, key=lambda x: x["change_percent"], reverse=True)
    elif filter_type == "losers":
        result = sorted(result, key=lambda x: x["change_percent"])
    elif filter_type == "volatile":
        result = sorted(result, key=lambda x: abs(x["change_percent"]), reverse=True)
    # else filter_type == 'all' : no sorting/filtering

    return {
        "page": page,
        "page_size": size,
        "total": total,
        "data": result
    }




# def fetch_all_latest() -> list:
#     result = []
#
#     for symbol in SYMBOL_LIST:
#         candles = fetch_ohlcv(symbol)
#         if not candles or len(candles) < 2:
#             print(f"⚠️ Skipping {symbol} due to no data")
#             continue
#
#         last = candles[-1]
#         prev = candles[-2]
#
#         close = last["close"]
#         prev_close = prev["close"]
#
#         try:
#             change_percent = round(((close - prev_close) / prev_close) * 100, 2)
#         except ZeroDivisionError:
#             change_percent = 0.0
#
#         result.append({
#             "symbol": symbol,
#             "close": close,
#             "prev_close": prev_close,
#             "change_percent": change_percent,
#             "timestamp": last["timestamp"]
#         })
#
#     return result
