from typing import List
from fastapi import APIRouter, Query
import pandas as pd
from datetime import datetime, timedelta
from pydantic import BaseModel
import operator
import pandas_ta as ta
from data.completeData import fetch_mt5_historical_data
from Strategies.predefined_strategies import PREDEFINED_STRATEGIES

router = APIRouter(prefix="/backtesting", tags=["backtesting"])

OP_MAP = {
    ">": operator.gt,
    "<": operator.lt,
    ">=": operator.ge,
    "<=": operator.le,
    "==": operator.eq,
    "!=": operator.ne,
    "crosses_above": lambda a, b: a.shift(1) < b.shift(1) and a > b,
    "crosses_below": lambda a, b: a.shift(1) > b.shift(1) and a < b,
}

def add_indicator(df: pd.DataFrame, indicator: str) -> pd.Series:
    if indicator == "rsi":
        return ta.rsi(df["close"])
    elif indicator.startswith("sma"):
        window = int(indicator.replace("sma", ""))
        return ta.ema(df["close"], length=window)
    elif indicator.startswith("ema"):
        window = int(indicator.replace("ema", ""))
        return ta.ema(df["close"], length=window)
    elif indicator == "macd":
        return ta.macd(df["close"])["MACDh_12_26_9"]
    elif indicator == "bollinger_upper":
        return ta.bbands(df["close"])["BBU_20_2.0"]
    elif indicator == "bollinger_lower":
        return ta.bbands(df["close"])["BBL_20_2.0"]
    elif indicator == "adx":
        return ta.adx(df["high"], df["low"], df["close"])["ADX_14"]
    elif indicator == "close":
        return df["close"]
    else:
        raise ValueError(f"Unsupported indicator: {indicator}")

def evaluate_condition(df: pd.DataFrame, indicator: str, operator_str: str, value: str) -> pd.Series:
    series_a = add_indicator(df, indicator)
    if not value.replace('.', '', 1).isdigit():
        series_b = add_indicator(df, value)
        return OP_MAP[operator_str](series_a, series_b)
    return OP_MAP[operator_str](series_a, float(value))

def run_backtest(symbol: str, interval: str, days: int, investment: float, conditions: list):
    df = fetch_mt5_historical_data(symbol, interval=interval, duration_days=days)
    if isinstance(df, list):
        df = pd.DataFrame(df)
    if df is None or df.empty:
        return {"error": "No data found"}

    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df = df.set_index("timestamp")

    triggers = []
    buy_price = None

    for i in range(50, len(df)):
        row_df = df.iloc[:i+1]
        match = True

        for cond in conditions:
            try:
                cond_result = evaluate_condition(row_df, cond["indicator"], cond["operator"], cond["value"])
                if not cond_result.iloc[-1]:
                    match = False
                    break
            except Exception:
                match = False
                break

        if match:
            price = df.iloc[i]["close"]
            timestamp = df.index[i]

            if buy_price is None:
                buy_price = price
                continue  # only consider signal after a buy is placed
            else:
                sell_price = price
                pl = (sell_price - buy_price) * (investment / buy_price)
                percent = (pl / investment) * 100

                triggers.append({
                    "timestamp": timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                    "buy_price": round(buy_price, 5),
                    "sell_price": round(sell_price, 5),
                    "profit_loss": round(pl, 2),
                    "gain_loss_percent": round(percent, 2)
                })

                buy_price = None  # reset for next buy signal

    if not triggers:
        return {
            "symbol": symbol,
            "total_signals": 0,
            "results": [],
            "average_profit": 0,
            "average_loss": 0,
            "top_10_profitable": [],
            "top_10_loss": []
        }

    profits = [t["profit_loss"] for t in triggers if t["profit_loss"] > 0]
    losses = [t["profit_loss"] for t in triggers if t["profit_loss"] < 0]

    avg_profit = sum(profits) / len(profits) if profits else 0
    avg_loss = sum(losses) / len(losses) if losses else 0

    sorted_trades = sorted(triggers, key=lambda x: x["profit_loss"], reverse=True)
    top_10_profitable = sorted_trades[:10]
    top_10_loss = sorted_trades[-10:]

    return {
        "symbol": symbol,
        "total_signals": len(triggers),
        "average_profit": round(avg_profit, 2),
        "average_loss": round(avg_loss, 2),
        "top_10_profitable": top_10_profitable,
        "top_10_loss": top_10_loss,
        "results": triggers
    }

# @router.get("/backtest")
# def backtest(
#     symbol: str = Query(...),
#     investment: float = Query(...),
#     strategy: str = Query(...),
#     interval: str = Query("1d"),
#     days: int = Query(365)
# ):
#     strategy_def = next((s for s in PREDEFINED_STRATEGIES if s["name"].lower() == strategy.lower()), None)
#     if not strategy_def:
#         return {"error": f"Strategy '{strategy}' not found"}
#     return run_backtest(symbol, interval, days, investment, strategy_def["conditions"])

# ... [rest of your imports remain same] ...

@router.get("/backtest")
def backtest(
    symbol: str = Query(...),
    investment: float = Query(...),
    strategy: str = Query(...),
    interval: str = Query("1d"),
    days: int = Query(365)
):
    strategy_def = next((s for s in PREDEFINED_STRATEGIES if s["name"].lower() == strategy.lower()), None)
    if not strategy_def:
        return {"error": f"Strategy '{strategy}' not found"}
    result = run_backtest(symbol, interval, days, investment, strategy_def["conditions"])
    if (
        isinstance(result, dict)
        and isinstance(result.get("results", []), list)
        and len(result["results"]) == 0
    ):
        return {
            "message": f"No signals found — strategy does not match for {symbol},"
                       f" interval: {interval}, days: {days}. Try different parameters."
        }
    return result

# OLD BACKTEST WORKING FOR BUY CONDITION


# from typing import Optional ,List
# from fastapi import APIRouter, Query, Body
# import pandas as pd
# from datetime import datetime, timedelta
# from pydantic import BaseModel
# import operator
# import pandas_ta as ta
# from data.completeData import fetch_mt5_historical_data
# from Strategies.predefined_strategies import PREDEFINED_STRATEGIES
#
# router = APIRouter(prefix="/backtesting", tags=["backtesting"])
#
# OP_MAP = {
#     ">": operator.gt,
#     "<": operator.lt,
#     ">=": operator.ge,
#     "<=": operator.le,
#     "==": operator.eq,
#     "!=": operator.ne,
#     "crosses_above": lambda a, b: a.shift(1) < b.shift(1) and a > b,
#     "crosses_below": lambda a, b: a.shift(1) > b.shift(1) and a < b,
# }
#
# def add_indicator(df: pd.DataFrame, indicator: str) -> pd.Series:
#     if indicator == "rsi":
#         return ta.rsi(df["close"])
#     elif indicator.startswith("ema"):
#         window = int(indicator.replace("ema", ""))
#         return ta.ema(df["close"], length=window)
#     elif indicator == "macd":
#         return ta.macd(df["close"])["MACDh_12_26_9"]
#     elif indicator == "bollinger_upper":
#         return ta.bbands(df["close"])["BBU_20_2.0"]
#     elif indicator == "bollinger_lower":
#         return ta.bbands(df["close"])["BBL_20_2.0"]
#     elif indicator == "adx":
#         return ta.adx(df["high"], df["low"], df["close"])["ADX_14"]
#     elif indicator == "close":
#         return df["close"]
#     else:
#         raise ValueError(f"Unsupported indicator: {indicator}")
#
# def evaluate_condition(df: pd.DataFrame, indicator: str, operator_str: str, value: str) -> pd.Series:
#     series_a = add_indicator(df, indicator)
#     if not value.replace('.', '', 1).isdigit():
#         series_b = add_indicator(df, value)
#         return OP_MAP[operator_str](series_a, series_b)
#     return OP_MAP[operator_str](series_a, float(value))
#
# def run_backtest(symbol: str, investment: float, conditions: list):
#     df = fetch_mt5_historical_data(symbol)
#     if isinstance(df, list):
#         df = pd.DataFrame(df)
#     if df is None or df.empty:
#         return {"error": "No data found"}
#
#     df["timestamp"] = pd.to_datetime(df["timestamp"])
#     df = df.set_index("timestamp")
#
#     one_year_ago = datetime.now() - timedelta(days=365)
#     df = df[df.index >= one_year_ago]
#
#     triggers = []
#     buy_price = None
#
#     for i in range(50, len(df)):
#         row_df = df.iloc[:i+1]
#         match = True
#
#         for cond in conditions:
#             try:
#                 cond_result = evaluate_condition(row_df, cond["indicator"], cond["operator"], cond["value"])
#                 if not cond_result.iloc[-1]:
#                     match = False
#                     break
#             except Exception:
#                 match = False
#                 break
#
#         if match:
#             price = df.iloc[i]["close"]
#             timestamp = df.index[i]
#
#             if buy_price is None:
#                 buy_price = price
#                 pl = 0
#                 percent = 0
#             else:
#                 pl = (price - buy_price) * (investment / buy_price)
#                 percent = (pl / investment) * 100
#                 buy_price = price
#
#             triggers.append({
#                 "timestamp": timestamp.strftime("%Y-%m-%d %H:%M:%S"),
#                 "price": round(price, 5),
#                 "profit_loss": round(pl, 2),
#                 "gain_loss_percent": round(percent, 2)
#             })
#
#     if not triggers:
#         return {
#             "symbol": symbol,
#             "total_signals": 0,
#             "results": [],
#             "average_profit": 0,
#             "average_loss": 0,
#             "top_10_profitable": [],
#             "top_10_loss": []
#         }
#
#     profits = [t["profit_loss"] for t in triggers if t["profit_loss"] > 0]
#     losses = [t["profit_loss"] for t in triggers if t["profit_loss"] < 0]
#
#     avg_profit = sum(profits) / len(profits) if profits else 0
#     avg_loss = sum(losses) / len(losses) if losses else 0
#
#     sorted_trades = sorted(triggers, key=lambda x: x["profit_loss"], reverse=True)
#     top_10_profitable = sorted_trades[:10]
#     top_10_loss = sorted_trades[-10:]
#
#     return {
#         "symbol": symbol,
#         "total_signals": len(triggers),
#         "average_profit": round(avg_profit, 2),
#         "average_loss": round(avg_loss, 2),
#         "top_10_profitable": top_10_profitable,
#         "top_10_loss": top_10_loss,
#         "results": triggers
#     }
#
# # GET for predefined
# @router.get("/backtest")
# def backtest(
#     symbol: str = Query(...),
#     investment: float = Query(...),
#     strategy: str = Query(...)
# ):
#     strategy_def = next((s for s in PREDEFINED_STRATEGIES if s["name"].lower() == strategy.lower()), None)
#     if not strategy_def:
#         return {"error": f"Strategy '{strategy}' not found"}
#     return run_backtest(symbol, investment, strategy_def["conditions"])
#
# # POST for custom
# class Condition(BaseModel):
#     indicator: str
#     operator: str
#     value: str
#
# class CustomStrategyRequest(BaseModel):
#     symbol: str
#     investment: float
#     investment: float
#     conditions: list[Condition]
#
#
# class Strategy(BaseModel):
#     name: str
#     conditions: List[Condition]
#     action: str
# class BacktestRequest(BaseModel):
#     symbol: str
#     market: str = "forex"
#     investment: float
#     strategy_name: Optional[str] = None
#     strategy_names: Optional[List[str]] = None
#     strategy: Optional[Strategy] = None
#     interval : str = "1d"
#     days : int = 365
# @router.post("/custom-backtest")
# def custom_backtest(body: CustomStrategyRequest):
#     return run_backtest(body.symbol, body.investment, [c.dict() for c in body.conditions])
