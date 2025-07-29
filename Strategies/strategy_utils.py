# auto_trade.py
from fastapi import APIRouter, HTTPException
from datetime import datetime
from typing import List
from pydantic import BaseModel
from threading import Thread
import time
from Strategies.predefined_strategies import PREDEFINED_STRATEGIES
from data.completeData import fetch_mt5_historical_data
from Test.Backtesting import evaluate_condition, add_indicator
from Manual_order.manual_util import place_buy_order, close_position_by_ticket

applied_strategies = []

def auto_trade_worker(symbol: str, strategy_name: str, investment: float, interval: str):
    strategy = next((s for s in PREDEFINED_STRATEGIES if s["name"] == strategy_name), None)
    if not strategy:
        return

    last_buy_ticket = None

    while any(s for s in applied_strategies if s["symbol"] == symbol and s["strategy_name"] == strategy_name):
        df = fetch_mt5_historical_data(symbol, interval, 500)
        df = add_indicator(df, strategy)

        latest_row = df.iloc[-1]
        buy_match = evaluate_condition(latest_row, strategy["conditions"], action="buy")
        sell_match = evaluate_condition(latest_row, strategy["conditions"], action="sell")

        if buy_match and not last_buy_ticket:
            ticket = place_buy_order(symbol, investment)
            last_buy_ticket = ticket

        elif sell_match and last_buy_ticket:
            close_position_by_ticket(symbol)
            last_buy_ticket = None

        time.sleep(60)
# from data.completeData import fetch_mt5_historical_data
# from Strategies.predefined_strategies import PREDEFINED_STRATEGIES
# from datetime import datetime
# import pytz
#
# def evaluate_condition(row, condition):
#     indicator_val = row.get(condition["indicator"])
#     target_val = row.get(condition["value"]) if condition["value"] in row else float(condition["value"])
#     op = condition["operator"]
#
#     if op == "<": return indicator_val < target_val
#     if op == ">": return indicator_val > target_val
#     if op == "==": return indicator_val == target_val
#     if op == "crosses_above": return row.get("prev_" + condition["indicator"]) <= row.get("prev_" + condition["value"]) and indicator_val > target_val
#     if op == "crosses_below": return row.get("prev_" + condition["indicator"]) >= row.get("prev_" + condition["value"]) and indicator_val < target_val
#     return False
#
#
# def apply_predefined_strategy_logic(symbol, strategy_name, interval, investment):
#     strategy = next((s for s in PREDEFINED_STRATEGIES if s["name"] == strategy_name), None)
#     if not strategy:
#         raise ValueError("Strategy not found")
#
#     df = fetch_mt5_historical_data(symbol, interval)
#     df["prev_close"] = df["close"].shift(1)
#
#     for condition in strategy["conditions"]:
#         if "crosses" in condition["operator"]:
#             df[f"prev_{condition['indicator']}"] = df[condition["indicator"]].shift(1)
#             df[f"prev_{condition['value']}"] = df[condition["value"]].shift(1)
#
#     active_trade = None
#     results = []
#
#     for i in range(1, len(df)):
#         row = df.iloc[i]
#         timestamp = row.name.tz_localize("UTC").astimezone(pytz.timezone("Asia/Kolkata"))
#
#         for condition in strategy["conditions"]:
#             if evaluate_condition(row, condition):
#                 if condition["action"] == "buy" and not active_trade:
#                     price = row["close"]
#                     active_trade = {
#                         "buy_price": price,
#                         "buy_time": timestamp,
#                         "investment": investment
#                     }
#                 elif condition["action"] == "sell" and active_trade:
#                     sell_price = row["close"]
#                     profit = (sell_price - active_trade["buy_price"]) * (investment / active_trade["buy_price"])
#                     results.append({
#                         "buy_price": active_trade["buy_price"],
#                         "sell_price": sell_price,
#                         "buy_time": active_trade["buy_time"],
#                         "sell_time": timestamp,
#                         "profit": round(profit, 2)
#                     })
#                     active_trade = None
#                 break
#     return results