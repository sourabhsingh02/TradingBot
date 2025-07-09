import operator
from PastDataFetch.data_fetcher import fetch_ohlcv
from typing import List, Tuple, Union
import pandas as pd
from Strategies.models import Strategy


OP_MAP = { ">": operator.gt,
           "<": operator.lt,
           ">=": operator.ge,
           "< =": operator.le,
           "==": operator.eq,
           "!=": operator.ne,
           "crosses_above": lambda a, b: a.shift(1) < b.shift(1) and a > b,
           "crosses_below": lambda a, b: a.shift(1) > b.shift(1) and a < b }

def add_indicator(df, indicator: str) -> pd.Series:
    import ta

    if indicator == "rsi":
        df["rsi"] = ta.momentum.RSIIndicator(df["close"]).rsi()
        return df["rsi"]

    elif indicator.startswith("ema"):
        window = int(indicator.replace("ema", ""))
        col = f"ema{window}"
        df[col] = ta.trend.EMAIndicator(df["close"], window=window).ema_indicator()
        return df[col]

    elif indicator == "macd":
        df["macd"] = ta.trend.MACD(df["close"]).macd_diff()
        return df["macd"]

    elif indicator == "bollinger_upper":
        bb = ta.volatility.BollingerBands(df["close"])
        df["bollinger_upper"] = bb.bollinger_hband()
        return df["bollinger_upper"]

    elif indicator == "bollinger_lower":
        bb = ta.volatility.BollingerBands(df["close"])
        df["bollinger_lower"] = bb.bollinger_lband()
        return df["bollinger_lower"]

    elif indicator == "adx":
        df["adx"] = ta.trend.ADXIndicator(df["high"], df["low"], df["close"]).adx()
        return df["adx"]

    elif indicator == "close":
        return df["close"]

    else:
        raise ValueError(f"Unsupported indicator: {indicator}")

def evaluate_condition(df: pd.DataFrame, indicator: str, operator_str: str, value: str) -> bool:
    series_a = add_indicator(df, indicator).dropna()
    if value.lower() in df.columns or not value.replace('.', '', 1).isdigit():
        series_b = add_indicator(df, value).dropna()
    else:
        try:
            return OP_MAP[operator_str](series_a.iloc[-1], float(value))
        except Exception as e:
            print(f"Evaluation error: {e}")
            return False

    try:
        if operator_str in ["crosses_above", "crosses_below"]:
            return OP_MAP[operator_str](series_a, series_b).iloc[-1]
        return OP_MAP[operator_str](series_a.iloc[-1], series_b.iloc[-1])
    except Exception as e:
        print(f"Compare error: {e}")
        return False



def evaluate_strategy(df: pd.DataFrame, strategy: Union[Strategy, dict]) -> Tuple[bool, str]:
    """
    Evaluate a single strategy using evaluate_condition (supports indicator vs value or indicator).
    """
    for cond in strategy['conditions'] if isinstance(strategy, dict) else strategy.conditions:
        indicator = cond["indicator"] if isinstance(cond, dict) else cond.indicator
        operator_str = cond["operator"] if isinstance(cond, dict) else cond.operator
        value = cond["value"] if isinstance(cond, dict) else cond.value

        try:
            if not evaluate_condition(df, indicator, operator_str, value):
                return False, f"Failed: {indicator} {operator_str} {value}"
        except Exception as e:
            return False, f"Error: {e}"

    return True, "All conditions passed"



def resolve_strategy(payload) -> dict:
    if payload.strategy:
        return payload.strategy.dict()
    from Strategies.predefined_strategies import PREDEFINED_STRATEGIES
    strategy = next((s for s in PREDEFINED_STRATEGIES if s["name"] == payload.strategy_name), None)
    if not strategy:
        raise ValueError("Strategy not found")
    return strategy



def apply_strategy(symbol: str, strategy: dict, market: str = "nse") -> dict:
    candles = fetch_ohlcv(symbol, market)
    if not candles:
        return {"symbol": symbol, "match": False, "reason": "No data"}
    df = pd.DataFrame(candles)
    match, reason = evaluate_strategy(df, strategy)
    return {
        "symbol": symbol,
        "match": match,
        "reason": reason,
        "action": strategy.get("action", "buy") if match else "hold"
    }


def apply_live_strategy(symbol: str, strategy: dict, market: str = "nse") -> dict:
    candles = fetch_ohlcv(symbol, market)
    if not candles:
        return {"symbol": symbol, "match": False, "reason": "No data"}

    df = pd.DataFrame(candles)
    df = df.tail(5)

    match, reason = evaluate_strategy(df, strategy)

    return {
        "symbol": symbol,
        "match": match,
        "reason": reason,
        "action": strategy.get("action", "buy") if match else None
    }



def apply_multiple_strategies(df: pd.DataFrame, strategies: List[Union[Strategy, dict]]) -> List[dict]:
    results = []

    for strategy in strategies:
        try:
            match, reason = evaluate_strategy(df, strategy)
            action = strategy.get("action", "hold") if isinstance(strategy, dict) else strategy.action
            results.append({
                "strategy": strategy["name"] if isinstance(strategy, dict) else strategy.name,
                "match": match,
                "reason": reason,
                "action": action if match else "hold"
            })
        except Exception as e:
            results.append({
                "strategy": strategy["name"] if isinstance(strategy, dict) else strategy.name,
                "match": False,
                "reason": str(e),
                "action": "hold"
            })

    return results
