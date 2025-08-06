from data.completeData import fetch_mt5_historical_data
from Test.Backtesting import evaluate_condition, add_indicator
from Manual_order.manual_util import place_buy_order, close_position_by_ticket
from database.db_connection import get_connection
from Security.encryption_mt5 import get_mt5_credentials
import MetaTrader5 as mt5
import time

INTERVAL_MAP = {
    "1min": 60,
    "5min": 300,
    "15min": 900,
    "1h": 3600,
    "1d": 86400
}

def auto_trade_worker(symbol: str, strategy: dict, investment: float, interval: str, user_id: int, strategy_type: str):
    creds = get_mt5_credentials(user_id)

    if not mt5.initialize(login=creds["login"], server=creds["server"], password=creds["password"]):
        print(f"[ERROR] MT5 init failed for user {user_id}")
        return

    sleep_duration = INTERVAL_MAP.get(interval, 60)
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    last_buy_ticket = None

    while True:
        # Check if strategy still active
        if strategy_type == "predefined":
            cursor.execute("""
                SELECT id FROM applied_strategy
                WHERE user_id = %s AND strategy_type = 'predefined' 
                AND strategy_id = %s AND symbol = %s AND is_active = TRUE
            """, (user_id, strategy["id"], symbol))
        else:
            cursor.execute("""
                SELECT id FROM applied_strategy
                WHERE user_id = %s AND strategy_type = 'custom' 
                AND strategy_id = %s AND symbol = %s AND is_active = TRUE
            """, (user_id, strategy["id"], symbol))

        if not cursor.fetchone():
            break

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

        time.sleep(sleep_duration)

    cursor.close()
    conn.close()
    mt5.shutdown()