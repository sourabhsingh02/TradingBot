import time
import pandas as pd
import smtplib
from email.mime.text import MIMEText
import operator
import pandas_ta as ta
from MetaTrader5 import *
from App.api_config import MT5_LOGIN, MT5_PASSWORD, MT5_SERVER
from data.completeData import fetch_mt5_tick_data

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
        return ta.momentum.RSIIndicator(df["close"]).rsi()
    elif indicator.startswith("ema"):
        window = int(indicator.replace("ema", ""))
        return ta.trend.EMAIndicator(df["close"], window=window).ema_indicator()
    elif indicator == "macd":
        return ta.trend.MACD(df["close"]).macd_diff()
    elif indicator == "bollinger_upper":
        return ta.volatility.BollingerBands(df["close"]).bollinger_hband()
    elif indicator == "bollinger_lower":
        return ta.volatility.BollingerBands(df["close"]).bollinger_lband()
    elif indicator == "adx":
        return ta.trend.ADXIndicator(df["high"], df["low"], df["close"]).adx()
    elif indicator == "close":
        return df["close"]
    else:
        raise ValueError(f"Unsupported indicator: {indicator}")

def evaluate_condition(df: pd.DataFrame, indicator: str, operator_str: str, value: str) -> bool:
    series_a = add_indicator(df, indicator).dropna()
    if not value.replace('.', '', 1).isdigit():
        series_b = add_indicator(df, value).dropna()
        return OP_MAP[operator_str](series_a.iloc[-1], series_b.iloc[-1])
    return OP_MAP[operator_str](series_a.iloc[-1], float(value))


from Strategies.predefined_strategies import PREDEFINED_STRATEGIES


def resolve_strategies(payload: list[str] | list[dict]) -> list[dict]:
    resolved = []
    for item in payload:
        if isinstance(item, dict):
            resolved.append(item)
        else:
            match = next((s for s in PREDEFINED_STRATEGIES if s["name"].lower() == item.lower()), None)
            if match:
                resolved.append(match)
            else:
                print(f"Strategy not found: {item}")
    return resolved


def evaluate_strategy(df: pd.DataFrame, strategy: dict) -> tuple[bool, str]:
    for cond in strategy["conditions"]:
        try:
            if not evaluate_condition(df, cond["indicator"], cond["operator"], cond["value"]):
                return False, f"Failed: {cond['indicator']} {cond['operator']} {cond['value']}"
        except Exception as e:
            return False, f"Error: {e}"
    return True, "All conditions passed"

def evaluate_all_strategies(df: pd.DataFrame, strategies: list[dict], symbol: str, auto_trade: bool = True):
    results = []

    for strategy in strategies:
        match, reason = evaluate_strategy(df, strategy)
        if match:
            action = strategy.get("action", "buy")
            print(f"[{strategy['name']}] ✅ Triggered: {reason} → {action.upper()}")
            send_email_alert(f"[{symbol}] {strategy['name']}", reason)
            if auto_trade:
                place_order(symbol, action)
            results.append({
                "strategy": strategy["name"],
                "status": "triggered",
                "action": action
            })
        else:
            print(f"[{strategy['name']}] ❌ Not triggered → {reason}")
            results.append({
                "strategy": strategy["name"],
                "status": "not_triggered",
                "reason": reason
            })

    return results


def place_order(symbol: str, action: str, lot: float = 0.1):
    if not initialize(login=MT5_LOGIN(), password=MT5_PASSWORD(), server=MT5_SERVER()):
        print("MT5 Init Failed")
        return False

    if not symbol_info(symbol).visible:
        symbol_select(symbol, True)

    tick = symbol_info_tick(symbol)
    price = tick.ask if action == "buy" else tick.bid
    order_type = ORDER_TYPE_BUY if action == "buy" else ORDER_TYPE_SELL

    request = {
        "action": TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lot,
        "type": order_type,
        "price": price,
        "deviation": 10,
        "magic": 123456,
        "comment": "AutoTrade",
        "type_time": ORDER_TIME_GTC,
        "type_filling": ORDER_FILLING_IOC,
    }

    result = order_send(request)
    print("order result " , result )
    shutdown()

    return result.retcode == TRADE_RETCODE_DONE

def send_email_alert(subject, body):
    sender = "your_email@gmail.com"
    password = "your_app_password"
    receiver = "target_email@gmail.com"

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = receiver

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender, password)
            server.send_message(msg)
    except Exception as e:
        print("Email error:", e)

import asyncio

async def monitor_and_trade(symbol, strategies, market, interval=30, auto_trade=True):
    strategy_names = [s['name'] for s in strategies]
    print(f"🔍 Watching {symbol} with strategies: {', '.join(strategy_names)}")

    while True:
        data = fetch_mt5_tick_data(symbol)
        if not data:
            await asyncio.sleep(interval)
            continue

        df = pd.DataFrame(data)
        results = evaluate_all_strategies(df, strategies, symbol, auto_trade)

        # Stop loop if any strategy is triggered
        if any(r["status"] == "triggered" for r in results):
            break

        await asyncio.sleep(interval)
def place_manual_order(symbol : str, action: str , investment: float):
    lot = round(investment / 1000,2)
    return place_order(symbol, action , lot)