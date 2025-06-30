import pandas as pd
import ta
import operator
from data_fetcher import fetch_ohlcv
from fastapi import HTTPException
from saved_strategies import load_saved_strategies, save_strategy
from typing import Dict
from models import CustomSignalRequest


OP_MAP = {
    ">": operator.gt,
    "<": operator.lt,
    "==": operator.eq,
    ">=": operator.ge,
    "<=": operator.le,
    "!=": operator.ne
}

def add_indicators(df: pd.DataFrame):
    df["SMA_50"] = df["close"].rolling(window=50).mean()
    df["SMA_200"] = df["close"].rolling(window=200).mean()
    df["RSI_14"] = ta.momentum.RSIIndicator(df["close"], window=14).rsi()
    return df



def evaluate_condition(row, condition):
    left = row.get(condition["indicator"])
    val = condition["value"]

    try:

        right = float(val)
    except ValueError:
        if val in row:
            right = row[val]
        else:
            raise ValueError(f"Unknown value or indicator: {val}")

    if left is None or right is None:
        raise ValueError(f"Invalid indicator or value: {condition}")

    return OP_MAP[condition["operator"]](left, right)

def evaluate_strategy(df: pd.DataFrame, strategy: dict) -> str:
    row = df.iloc[-1]
    for cond in strategy["conditions"]:
        if not evaluate_condition(row, cond):
            return "HOLD"
    return strategy["action"]

def apply_strategy(symbol: str, strategy: dict):
    candles = fetch_ohlcv(symbol)
    if not candles or len(candles) < 20:
        return {"symbol": symbol, "error": "Not enough data"}

    df = pd.DataFrame(candles)
    df = add_indicators(df)

    try:
        signal = evaluate_strategy(df, strategy)

        return {
            "symbol": symbol,
            "close": float(df.iloc[-1]["close"]),  # convert numpy.float64 to native float
            "signal": str(signal)  # ensure string type
        }

    except Exception as e:
        return {
            "symbol": symbol,
            "error": str(e)
        }





def resolve_strategy(payload: CustomSignalRequest) -> Dict:
    if payload.strategy_name and not payload.strategy:
        strategy = next((s for s in load_saved_strategies() if s["name"] == payload.strategy_name), None)
        if not strategy:
            raise HTTPException(status_code=404, detail="Saved strategy not found")
        return strategy

    elif payload.strategy:
        saved = next((s for s in load_saved_strategies() if s["name"] == payload.strategy.name), None)
        new_strategy = payload.strategy.dict()

        if saved:
            if saved["conditions"] != [c.dict() for c in payload.strategy.conditions] or saved["action"] != payload.strategy.action:
                raise HTTPException(
                    status_code=400,
                    detail=f"Strategy name '{payload.strategy.name}' already exists with different conditions."
                )
            return saved

        save_strategy(new_strategy)
        return new_strategy

    raise HTTPException(status_code=400, detail="Either strategy or strategy_name is required")
