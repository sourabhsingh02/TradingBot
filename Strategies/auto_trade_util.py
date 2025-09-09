from data.completeData import fetch_mt5_historical_data
from Test.Backtesting import evaluate_condition, add_indicator
from Manual_order.manual_util import place_buy_order, close_position_by_ticket
from database.db_connection import get_connection
from Security.encryption_mt5 import get_mt5_credentials
import MetaTrader5 as mt5
import time
from datetime import datetime

INTERVAL_MAP = {
    "1min": 60,
    "5min": 300,
    "15min": 900,
    "1h": 3600,
    "1d": 86400
}

def auto_trade_worker(symbol: str, strategy: dict, lot: int, interval: str, user_id: int, strategy_type: str, instance_id: str):
    creds = get_mt5_credentials(user_id)

    if not mt5.initialize(login=creds["login"], server=creds["server"], password=creds["password"]):
        print(f"[ERROR] MT5 init failed for user {user_id}")
        return

    sleep_duration = INTERVAL_MAP.get(interval, 60)
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    active_tickets = []
    next_run = time.time()

    while True:
        start_time = time.time()

        # Check if this instance is still active
        cursor.execute("""
            SELECT id FROM applied_strategy
            WHERE user_id = %s AND instance_id = %s AND is_active = TRUE
        """, (user_id, instance_id))

        if not cursor.fetchone():
            print(f"[INFO] Strategy instance {instance_id} stopped for {symbol}")
            break

        # Fetch historical data and apply strategy
        df = fetch_mt5_historical_data(symbol, interval, 500)
        df = add_indicator(df, strategy)
        latest_row = df.iloc[-1]

        buy_match = evaluate_condition(latest_row, strategy["conditions"], action="buy")
        sell_match = evaluate_condition(latest_row, strategy["conditions"], action="sell")

        # Buy condition
        if buy_match:
            ticket = place_buy_order(symbol, lot)
            if ticket:
                active_tickets.append(ticket)
                print(f"[BUY] {symbol} ticket: {ticket}")

        # Sell condition
        if sell_match and active_tickets:
            for ticket in active_tickets:
                close_position_by_ticket(symbol, ticket)
            active_tickets.clear()
            print(f"[SELL] {symbol} all positions closed")

        next_run += sleep_duration
        sleep_time = max(0, next_run - time.time())
        print(f"[INFO] Next run after {sleep_time:.2f}s ({datetime.now()})")
        time.sleep(sleep_time)

    cursor.close()
    conn.close()
    mt5.shutdown()


# from data.completeData import fetch_mt5_historical_data
# from Test.Backtesting import evaluate_condition, add_indicator
# from Manual_order.manual_util import place_buy_order, close_position_by_ticket
# from database.db_connection import get_connection
# from Security.encryption_mt5 import get_mt5_credentials
# import MetaTrader5 as mt5
# import time
# from datetime import datetime
#
# INTERVAL_MAP = {
#     "1min": 60,
#     "5min": 300,
#     "15min": 900,
#     "1h": 3600,
#     "1d": 86400
# }
#
# def auto_trade_worker(symbol: str, strategy: dict, lot: int, interval: str, user_id: int, strategy_type: str):
#     creds = get_mt5_credentials(user_id)
#
#     if not mt5.initialize(login=creds["login"], server=creds["server"], password=creds["password"]):
#         print(f"[ERROR] MT5 init failed for user {user_id}")
#         return
#
#     sleep_duration = INTERVAL_MAP.get(interval, 60)
#     conn = get_connection()
#     cursor = conn.cursor(dictionary=True)
#
#     last_buy_ticket = None
#     next_run = time.time()  # Start scheduling
#
#     while True:
#         start_time = time.time()
#
#
#         cursor.execute("""
#             SELECT id FROM applied_strategy
#             WHERE user_id = %s AND strategy_type = %s
#             AND strategy_id = %s AND symbol = %s AND is_active = TRUE
#         """, (user_id, strategy_type, strategy["id"], symbol))
#
#         if not cursor.fetchone():
#             print(f"[INFO] Strategy stopped for user {user_id}, symbol {symbol}")
#             break
#
#
#         df = fetch_mt5_historical_data(symbol, interval, 500)
#         df = add_indicator(df, strategy)
#         latest_row = df.iloc[-1]
#
#
#         buy_match = evaluate_condition(latest_row, strategy["conditions"], action="buy")
#         sell_match = evaluate_condition(latest_row, strategy["conditions"], action="sell")
#
#         if buy_match and not last_buy_ticket:
#             ticket = place_buy_order(symbol, lot)   # place buy order
#             last_buy_ticket = ticket
#             print(f"[BUY] {symbol} ticket: {ticket}")
#
#         elif sell_match and last_buy_ticket:
#             close_position_by_ticket(symbol)
#             last_buy_ticket = None
#             print(f"[SELL] {symbol} closed")
#
#
#
#         next_run += sleep_duration
#         sleep_time = max(0, next_run - time.time())
#         print(f"[INFO] Next run after {sleep_time:.2f} seconds ({datetime.now()})")
#         time.sleep(sleep_time)
#
#     cursor.close()
#     conn.close()
#     mt5.shutdown()
#
#
# # from data.completeData import fetch_mt5_historical_data
# # from Test.Backtesting import evaluate_condition, add_indicator
# # from Manual_order.manual_util import place_buy_order, close_position_by_ticket
# # from database.db_connection import get_connection
# # from Security.encryption_mt5 import get_mt5_credentials
# # import MetaTrader5 as mt5
# # import time
# #
# # INTERVAL_MAP = {
# #     "1min": 60,
# #     "5min": 300,
# #     "15min": 900,
# #     "1h": 3600,
# #     "1d": 86400
# # }
# #
# # def auto_trade_worker(symbol: str, strategy: dict, lot: int, interval: str, user_id: int, strategy_type: str):
# #     creds = get_mt5_credentials(user_id)
# #
# #     if not mt5.initialize(login=creds["login"], server=creds["server"], password=creds["password"]):
# #         print(f"[ERROR] MT5 init failed for user {user_id}")
# #         return
# #
# #     sleep_duration = INTERVAL_MAP.get(interval, 60)
# #     conn = get_connection()
# #     cursor = conn.cursor(dictionary=True)
# #
# #     last_buy_ticket = None
# #
# #     while True:
# #         # Check if strategy is still active
# #         cursor.execute("""
# #             SELECT id FROM applied_strategy
# #             WHERE user_id = %s AND strategy_type = %s
# #             AND strategy_id = %s AND symbol = %s AND is_active = TRUE
# #         """, (user_id, strategy_type, strategy["id"], symbol))
# #
# #         if not cursor.fetchone():
# #             break
# #
# #         # Fetch fresh data
# #         df = fetch_mt5_historical_data(symbol, interval, 500)
# #         df = add_indicator(df, strategy)
# #         latest_row = df.iloc[-1]
# #
# #         # Apply conditions
# #         buy_match = evaluate_condition(latest_row, strategy["conditions"], action="buy")
# #         sell_match = evaluate_condition(latest_row, strategy["conditions"], action="sell")
# #
# #         if buy_match and not last_buy_ticket:
# #             ticket = place_buy_order(symbol, lot)   # 👈 now using lot directly
# #             last_buy_ticket = ticket
# #
# #         elif sell_match and last_buy_ticket:
# #             close_position_by_ticket(symbol)
# #             last_buy_ticket = None
# #
# #         time.sleep(sleep_duration)
# #
# #     cursor.close()
# #     conn.close()
# #     mt5.shutdown()
