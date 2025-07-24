from fastapi import APIRouter
from datetime import datetime, timedelta
import pandas as pd
import MetaTrader5 as mt5
from App.api_config import MT5_LOGIN, MT5_PASSWORD, MT5_SERVER
router = APIRouter(prefix="/test", tags=["Most Buy/Sell"])


def fetch_mt5_tick_data_for_db(symbol: str, start_time=None, end_time=None):
    import pytz
    from datetime import datetime, timedelta

    if not mt5.initialize(login=MT5_LOGIN(), password=MT5_PASSWORD(), server=MT5_SERVER()):
        print("MT5 init failed:", mt5.last_error())
        return pd.DataFrame()

    if not mt5.symbol_select(symbol, True):
        print(f"Symbol select failed: {symbol}")
        mt5.shutdown()
        return pd.DataFrame()

    if start_time is None or end_time is None:
        end_time = datetime.now(pytz.UTC)
        start_time = end_time - timedelta(minutes=30)

    ticks = mt5.copy_ticks_range(symbol, start_time, end_time, mt5.COPY_TICKS_ALL)
    mt5.shutdown()

    if ticks is None or len(ticks) == 0:
        print(f"No tick data found for {symbol}")
        return pd.DataFrame()

    df = pd.DataFrame(ticks)
    df["timestamp"] = pd.to_datetime(df["time"], unit="s")
    return df


from datetime import datetime, timedelta
import pandas as pd
from data.completeData import fetch_mt5_tick_data

from datetime import datetime, timedelta
import pandas as pd
from data.completeData import fetch_mt5_tick_data

def tick_data_for_most_buy_sell(symbol: str, minutes: int = 30):
    ticks = fetch_mt5_tick_data(symbol)

    if not ticks:
        return {"status": "error", "message": "No tick data or volume unavailable"}

    df = pd.DataFrame(ticks)
    if df.empty or "epoch" not in df.columns:
        return {"status": "error", "message": "Tick data invalid or missing 'epoch'"}

    # Filter by time window
    cutoff_epoch = int((datetime.utcnow() - timedelta(minutes=minutes)).timestamp())
    df = df[df["epoch"] >= cutoff_epoch]

    if df.empty:
        return {"status": "error", "message": f"No tick data in last {minutes} minutes"}

    # Improved classification logic
    df["type"] = df.apply(lambda row: 0 if row["bid"] <= row["ask"] else 1, axis=1)

    buy_volume = df[df["type"] == 0]["volume"].sum()
    sell_volume = df[df["type"] == 1]["volume"].sum()

    return {
        "status": "success",
        "data": {
            "symbol": symbol,
            "buy_volume": float(buy_volume),
            "sell_volume": float(sell_volume)
        }
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