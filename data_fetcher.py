import yfinance as yf
import requests
from datetime import datetime, timedelta
from api_config import API_KEY, ACCESS_TOKEN

# 🟢 Use yfinance for testing, Dhan for production
USE_DHAN = False

def fetch_ohlcv(symbol: str):
    if USE_DHAN:
        return fetch_from_dhan(symbol)
    else:
        return fetch_from_yfinance(symbol)

# 🔁 Dummy using yfinance
def fetch_from_yfinance(symbol: str):
    symbol = symbol.upper()
    if not symbol.endswith(".NS"):
        symbol += ".NS"

    end_date = datetime.now()
    start_date = end_date - timedelta(days=5)

    df = yf.download(symbol, start=start_date.strftime("%Y-%m-%d"), end=end_date.strftime("%Y-%m-%d"), interval="1d")

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

# ✅ Real Dhan integration (placeholder)
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


            # ---------------Yfinance------------

# import yfinance as yf
# from datetime import datetime, timedelta
#
# def fetch_ohlcv_dhan(symbol: str):
#     # NSE symbols must be suffixed with '.NS'
#     symbol = symbol.upper() + ".NS"
#
#     # Get last 5 days of OHLCV data
#     end_date = datetime.now()
#     start_date = end_date - timedelta(days=5)
#
#     try:
#         df = yf.download(symbol, start=start_date.strftime("%Y-%m-%d"), end=end_date.strftime("%Y-%m-%d"), interval="1d")
#
#         if df.empty:
#             return []
#
#         # Convert DataFrame to list of dictionaries
#         data = []
#         for index, row in df.iterrows():
#             data.append({
#                 "timestamp": index.strftime("%Y-%m-%d"),
#                 "open": round(row['Open'], 2),
#                 "high": round(row['High'], 2),
#                 "low": round(row['Low'], 2),
#                 "close": round(row['Close'], 2),
#                 "volume": int(row['Volume'])
#             })
#
#         return data
#
#     except Exception as e:
#         print("[ERROR]", e)
#         return []

#                   ?----------------- Dummy DAta -------

# def fetch_ohlcv_dhan(symbol: str):
#     """
#     Returns static OHLCV candles for testing.
#     Replace this later with live–API logic.
#     """
#     symbol = symbol.upper()
#
#     if symbol == "RELIANCE":
#         return [
#             {"timestamp": "2024-06-20", "open": 2500, "high": 2550,
#              "low": 2480, "close": 2520, "volume": 10000},
#             {"timestamp": "2024-06-21", "open": 2520, "high": 2580,
#              "low": 2510, "close": 2570, "volume": 12000},
#             {"timestamp": "2024-06-22", "open": 2570, "high": 2600,
#              "low": 2560, "close": 2590, "volume": 9000},
#             {"timestamp": "2024-06-23", "open": 2590, "high": 2620,
#              "low": 2580, "close": 2610, "volume": 11000},
#             {"timestamp": "2024-06-24", "open": 2610, "high": 2650,
#              "low": 2600, "close": 2630, "volume": 15000}
#         ]
#
#     # fallback dummy for any other symbol
#     return [
#         {"timestamp": "2024-06-20", "open": 100, "high": 110,
#          "low": 90, "close": 105, "volume": 5000},
#         {"timestamp": "2024-06-21", "open": 105, "high": 115,
#          "low": 100, "close": 112, "volume": 6000},
#         {"timestamp": "2024-06-22", "open": 112, "high": 120,
#          "low": 108, "close": 118, "volume": 5500}
#     ]
