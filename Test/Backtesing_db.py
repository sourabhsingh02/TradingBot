from typing import List
from fastapi import APIRouter, Query
import pandas as pd
from datetime import datetime, timedelta
from pydantic import BaseModel
import operator
import pandas_ta as ta
from data.completeData import fetch_mt5_historical_data
from database.db_connection import get_connection
import json

router = APIRouter(prefix="/backtestingdb", tags=["backtesting || DB"])


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
        return ta.sma(df["close"], length=window)
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
                continue
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

                buy_price = None

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

@router.get("/backtest")
def backtest(
    symbol: str = Query(...),
    investment: float = Query(...),
    strategy: str = Query(...),
    interval: str = Query("1d"),
    days: int = Query(365)
):
    conn = get_connection()
    if conn is None:
        return {"error": "DB connection failed"}

    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT conditions FROM predefined_strategies WHERE LOWER(name) = %s", (strategy.lower(),))
    row = cursor.fetchone()

    if not row:
        return {"error": f"Strategy '{strategy}' not found"}

    try:
        conditions = json.loads(row["conditions"])
    except Exception:
        return {"error": "Invalid strategy conditions format"}
    finally:
        cursor.close()
        conn.close()

    result = run_backtest(symbol, interval, days, investment, conditions)

    if isinstance(result, dict) and isinstance(result.get("results", []), list) and len(result["results"]) == 0:
        return {"message": "No signals found"}

    return result