from threading import Thread
from fastapi import APIRouter, Depends, HTTPException
from typing import List
from pydantic import BaseModel
from datetime import datetime
import time
import MetaTrader5 as mt5

from data.completeData import fetch_mt5_historical_data
from Test.Backtesting import evaluate_condition, add_indicator
from Manual_order.manual_util import place_buy_order, close_position_by_ticket
from database.db_connection import get_connection
from Security.auth import get_current_user
from Security.encryption_mt5 import get_mt5_credentials

router = APIRouter(prefix="/advance-auto-order", tags=["Advance Auto Order"])

INTERVAL_MAP = {
    "1min": 60,
    "5min": 300,
    "15min": 900,
    "1h": 3600,
    "1d": 86400
}

# ✅ Request models
class AutoSelectRequest(BaseModel):
    symbols: List[str]
    lot: int
    interval: str


class StrategyUnapplyRequest(BaseModel):
    strategy_name: str
    symbol: str
    strategy_type: str  # "predefined" or "custom"



@router.post("/apply-auto-strategy")
def apply_auto_strategy(
    request: AutoSelectRequest,
    current_user: dict = Depends(get_current_user)
):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    # Fetch all predefined strategies
    cursor.execute("SELECT * FROM predefined_strategies")
    predefined_strategies = cursor.fetchall()

    # Fetch all custom strategies for this user
    cursor.execute("SELECT * FROM custom_strategy WHERE user_id = %s", (current_user["id"],))
    custom_strategies = cursor.fetchall()

    applied_count = 0

    for symbol in request.symbols:
        # Apply all matching predefined strategies
        for strategy in predefined_strategies:
            if match_strategy_conditions(symbol, strategy):
                applied = _apply_strategy(cursor, conn, current_user["id"], strategy, symbol, request.lot, request.interval, "predefined")
                if applied:
                    applied_count += 1

        # Apply all matching custom strategies
        for strategy in custom_strategies:
            if match_strategy_conditions(symbol, strategy):
                applied = _apply_strategy(cursor, conn, current_user["id"], strategy, symbol, request.lot, request.interval, "custom")
                if applied:
                    applied_count += 1

    cursor.close()
    conn.close()

    if applied_count == 0:
        raise HTTPException(status_code=404, detail="No matching strategy found for provided symbols")

    return {"message": f"{applied_count} strategy-symbol combinations applied successfully"}


def _apply_strategy(cursor, conn, user_id, strategy, symbol, lot, interval, strategy_type):
    # Check if already active for same symbol & strategy
    cursor.execute("""
        SELECT id FROM applied_strategy
        WHERE user_id = %s AND strategy_id = %s AND symbol = %s AND is_active = TRUE
    """, (user_id, strategy["id"], symbol))

    if cursor.fetchone():
        return False

    # Insert applied strategy
    cursor.execute("""
        INSERT INTO applied_strategy (user_id, strategy_id, symbol, lot, time_interval, strategy_type)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (user_id, strategy["id"], symbol, lot, interval, strategy_type))
    conn.commit()

    # Start auto-trade thread
    thread = Thread(
        target=auto_trade_worker,
        args=(symbol, strategy, lot, interval, user_id, strategy_type)
    )
    thread.daemon = True
    thread.start()

    return True


# ✅ Get all active strategies for user
@router.get("/active-strategies")
def get_active_strategies(current_user: dict = Depends(get_current_user)):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT a.symbol, a.lot, a.time_interval, a.strategy_type,
               CASE 
                   WHEN a.strategy_type = 'predefined' THEN p.name 
                   ELSE c.name 
               END AS strategy_name
        FROM applied_strategy a
        LEFT JOIN predefined_strategies p ON a.strategy_type = 'predefined' AND a.strategy_id = p.id
        LEFT JOIN custom_strategy c ON a.strategy_type = 'custom' AND a.strategy_id = c.id
        WHERE a.user_id = %s AND a.is_active = TRUE
    """, (current_user["id"],))

    results = cursor.fetchall()
    cursor.close()
    conn.close()

    return {"active_strategies": results}


# ✅ Unapply strategy for specific symbol
@router.post("/unapply")
def unapply_strategy(
    request: StrategyUnapplyRequest,
    current_user: dict = Depends(get_current_user)
):
    conn = get_connection()
    cursor = conn.cursor()

    # Get strategy ID
    if request.strategy_type == "predefined":
        cursor.execute("SELECT id FROM predefined_strategies WHERE name = %s", (request.strategy_name,))
    elif request.strategy_type == "custom":
        cursor.execute("SELECT id FROM custom_strategy WHERE name = %s AND user_id = %s",
                       (request.strategy_name, current_user["id"]))
    else:
        raise HTTPException(status_code=400, detail="Invalid strategy_type")

    strategy = cursor.fetchone()
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")

    strategy_id = strategy[0]

    # Mark inactive
    cursor.execute("""
        UPDATE applied_strategy
        SET is_active = FALSE
        WHERE user_id = %s AND strategy_id = %s AND symbol = %s AND strategy_type = %s
    """, (current_user["id"], strategy_id, request.symbol, request.strategy_type))

    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="No active strategy found to unapply")

    conn.commit()
    cursor.close()
    conn.close()

    return {"message": f"{request.strategy_type.title()} strategy unapplied successfully for {request.symbol}"}


# ✅ Worker: Auto trading logic
def auto_trade_worker(symbol: str, strategy: dict, lot: int, interval: str, user_id: int, strategy_type: str):
    creds = get_mt5_credentials(user_id)

    if not mt5.initialize(login=creds["login"], server=creds["server"], password=creds["password"]):
        print(f"[ERROR] MT5 init failed for user {user_id}")
        return

    sleep_duration = INTERVAL_MAP.get(interval, 60)
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    last_buy_ticket = None
    next_run = time.time()

    while True:
        start_time = time.time()

        #  Check if strategy is still active
        cursor.execute("""
            SELECT id FROM applied_strategy
            WHERE user_id = %s AND strategy_type = %s 
            AND strategy_id = %s AND symbol = %s AND is_active = TRUE
        """, (user_id, strategy_type, strategy["id"], symbol))

        if not cursor.fetchone():
            print(f"[INFO] Strategy stopped for user {user_id}, symbol {symbol}")
            break

        #  Fetch market data & apply indicators
        df = fetch_mt5_historical_data(symbol, interval, 500)
        df = add_indicator(df, strategy)
        latest_row = df.iloc[-1]

        #  Evaluate conditions
        buy_match = evaluate_condition(latest_row, strategy["conditions"], action="buy")
        sell_match = evaluate_condition(latest_row, strategy["conditions"], action="sell")

        if buy_match and not last_buy_ticket:
            ticket = place_buy_order(symbol, lot)
            last_buy_ticket = ticket
            print(f"[BUY] {symbol} ticket: {ticket}")

        elif sell_match and last_buy_ticket:
            close_position_by_ticket(symbol)
            last_buy_ticket = None
            print(f"[SELL] {symbol} closed")

        #  Schedule next run
        next_run += sleep_duration
        sleep_time = max(0, next_run - time.time())
        print(f"[INFO] Next run after {sleep_time:.2f} seconds ({datetime.now()})")
        time.sleep(sleep_time)

    cursor.close()
    conn.close()
    mt5.shutdown()


#  Strategy condition matcher
def match_strategy_conditions(symbol: str, strategy: dict) -> bool:
    # Example: check if strategy allows symbol
    allowed_symbols = strategy.get("symbols")
    if allowed_symbols:
        symbol_list = [s.strip().upper() for s in allowed_symbols.split(",")]
        if symbol.upper() not in symbol_list:
            return False
    return True
