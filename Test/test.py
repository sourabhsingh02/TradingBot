from fastapi import APIRouter
from datetime import datetime, timedelta
import pandas as pd
import MetaTrader5 as mt5

router = APIRouter(prefix="/test", tags=["Most Buy/Sell"])

# ✅ Fetch tick data for a symbol
def tick_data_for_most_buy_sell(symbol: str, minutes: int = 30):
    from data.completeData import fetch_mt5_tick_data
    import pytz
    from datetime import datetime, timedelta

    timezone = pytz.timezone("Etc/UTC")
    end_time = datetime.now(timezone)
    start_time = end_time - timedelta(minutes=minutes)

    ticks = fetch_mt5_tick_data(symbol, start_time, end_time)

    if ticks.empty:
        print(f"[DEBUG] No tick data returned for {symbol} from {start_time} to {end_time}")
        return []

    print(f"[DEBUG] Total ticks fetched: {len(ticks)}")

    # Add 'type' column if not present
    if "type" not in ticks.columns:
        print(f"[DEBUG] Column 'type' not found in ticks")
        return []

    # Actual volume calc
    buy_volume = ticks[ticks["type"] == 0]["volume"].sum()
    sell_volume = ticks[ticks["type"] == 1]["volume"].sum()

    return {
        "symbol": symbol,
        "buy_volume": buy_volume,
        "sell_volume": sell_volume,
    }


# ✅ Most bought
def get_most_bought_pairs(symbols: list, top_n: int = 5):
    result = []
    for symbol in symbols:
        data = tick_data_for_most_buy_sell(symbol)
        if data and data["buy_volume"] > 0:
            result.append(data)
    result.sort(key=lambda x: x["buy_volume"], reverse=True)
    return result[:top_n]

# ✅ Most sold
def get_most_sold_pairs(symbols: list, top_n: int = 5):
    result = []
    for symbol in symbols:
        data = tick_data_for_most_buy_sell(symbol)
        if data and data["sell_volume"] > 0:
            result.append(data)
    result.sort(key=lambda x: x["sell_volume"], reverse=True)
    return result[:top_n]

# ✅ SYMBOL LIST
SYMBOLS = [
    "EURUSD", "GBPUSD", "USDJPY", "USDCHF", "USDCAD",
    "AUDUSD", "NZDUSD", "XAUUSD", "BTCUSD", "ETHUSD"
]

# ✅ API: Get tick volume for one pair
@router.get("/tick_volume")
def get_tick_volume(symbol: str):
    data = tick_data_for_most_buy_sell(symbol)
    if data:
        return {"status": "success", "data": data}
    return {"status": "error", "message": "No tick data or volume unavailable"}

# ✅ API: Most Bought Pairs
@router.get("/most_bought_pairs_dashboard")
def most_bought_pairs_dashboard(page: int = 1, per_page: int = 5):
    top_pairs = get_most_bought_pairs(SYMBOLS, top_n=50)
    start = (page - 1) * per_page
    end = start + per_page
    paginated = top_pairs[start:end]
    return {
        "status": "success",
        "results": {
            "page": page,
            "per_page": per_page,
            "total": len(top_pairs),
            "results": paginated
        }
    }

# ✅ API: Most Sold Pairs
@router.get("/most_sold_pairs_dashboard")
def most_sold_pairs_dashboard(page: int = 1, per_page: int = 5):
    top_pairs = get_most_sold_pairs(SYMBOLS, top_n=50)
    start = (page - 1) * per_page
    end = start + per_page
    paginated = top_pairs[start:end]
    return {
        "status": "success",
        "results": {
            "page": page,
            "per_page": per_page,
            "total": len(top_pairs),
            "results": paginated
        }
    }