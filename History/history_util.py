import MetaTrader5 as mt5
from datetime import datetime
from database.db_connection import get_connection
from Security.encryption_mt5 import decrypt_password , get_mt5_credentials


def init_mt5(user_id: int):
    creds = get_mt5_credentials(user_id)
    if not creds:
        return {"status": "error", "message": "MT5 credentials not found"}

    if not mt5.initialize(
        login=creds["login"],
        password=creds["password"],
        server=creds["server"]
    ):
        return {"status": "error", "message": "MT5 initialization failed"}

    return {"status": "success"}



def get_open_positions_by_user(user_id: int):
    creds = get_mt5_credentials(user_id)

    initialized = mt5.initialize(
        login=creds["login"],
        password=creds["password"],  # already stored
        server=creds["server"]
    )
    if not initialized:
        return {"status": "error", "message": "MT5 initialization failed"}

    positions = mt5.positions_get()

    if positions is None:
        mt5.shutdown()
        return {"status": "error", "message": "Failed to get positions"}

    result = []
    for pos in positions:
        result.append({
            "symbol": pos.symbol,
            "ticket": pos.ticket,
            "type": "buy" if pos.type == 0 else "sell",
            "volume": pos.volume,
            "price_open": pos.price_open,
            "profit": pos.profit,
            "time": pos.time
        })

    mt5.shutdown()
    return {"status": "success", "positions": result}

def get_open_positions(user_id: int, symbol=None):
    init_result = init_mt5(user_id)
    if init_result["status"] != "success":
        return init_result

    positions = mt5.positions_get(symbol=symbol) if symbol else mt5.positions_get()
    if positions is None:
        return {"status": "error", "message": "Failed to get positions"}

    result = []
    for pos in positions:
        result.append({
            "symbol": pos.symbol,
            "ticket": pos.ticket,
            "type": "buy" if pos.type == 0 else "sell",
            "volume": pos.volume,
            "price_open": pos.price_open,
            "profit": pos.profit,
            "time": pos.time
        })

    mt5.shutdown()
    return {"status": "success", "positions": result}


def close_position_by_ticket(user_id: int, ticket: int):
    init_result = init_mt5(user_id)
    if init_result["status"] != "success":
        return init_result

    position = mt5.positions_get(ticket=ticket)
    if position is None or len(position) == 0:
        return {"status": "error", "message": "No open position with given ticket"}

    pos = position[0]
    symbol = pos.symbol
    volume = pos.volume
    position_type = pos.type

    tick = mt5.symbol_info_tick(symbol)
    if tick is None:
        return {"status": "error", "message": "Symbol tick info not found"}

    price = tick.bid if position_type == 0 else tick.ask
    order_type = mt5.ORDER_TYPE_SELL if position_type == 0 else mt5.ORDER_TYPE_BUY

    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": volume,
        "type": order_type,
        "position": ticket,
        "price": price,
        "deviation": 10,
        "magic": 234000,
        "comment": "Close position by ticket",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }

    result = mt5.order_send(request)
    mt5.shutdown()

    if result.retcode != mt5.TRADE_RETCODE_DONE:
        return {
            "status": "error",
            "message": f"Failed to close position: {result.comment}",
            "retcode": result.retcode,
        }

    return {"status": "success", "message": "Position closed", "retcode": result.retcode}




def get_trade_history(user_id: int):
    init_result = init_mt5(user_id)
    if init_result["status"] != "success":
        return init_result

    from_date = datetime(2024, 1, 1)
    to_date = datetime.now()

    deals = mt5.history_deals_get(from_date, to_date)
    last_error = mt5.last_error()

    if deals is None:
        mt5.shutdown()
        return {
            "status": "error",
            "message": "Failed to get trade history",
            "error_code": last_error[0],
            "error_message": last_error[1]
        }

    result = []
    for deal in deals:
        symbol_info = mt5.symbol_info(deal.symbol)
        if symbol_info is None:
            continue

        contract_size = symbol_info.trade_contract_size


        notional = deal.price * deal.volume * contract_size
        profit_percent = (deal.profit / notional * 100) if notional > 0 else 0

        result.append({
            "symbol": deal.symbol,
            "ticket": deal.ticket,
            "type": "buy" if deal.type == 0 else "sell",
            "volume": deal.volume,
            "price": deal.price,
            "profit": deal.profit,
            "profit_percent": round(profit_percent, 2),
            "time": datetime.fromtimestamp(deal.time).strftime("%Y-%m-%d %H:%M:%S")
        })

    mt5.shutdown()
    return {"status": "success", "count": len(result), "history": result}


def get_account_info(user_id: int):
    init_result = init_mt5(user_id)
    if init_result["status"] != "success":
        return init_result

    account_info = mt5.account_info()
    if account_info is None:
        mt5.shutdown()
        return {"status": "error", "message": "Failed to retrieve account info"}

    mt5.shutdown()
    return {
        "status": "success",
        "account": {
            "login": account_info.login,
            "name": account_info.name,
            "server": account_info.server,
            "currency": account_info.currency,
            "leverage": account_info.leverage,
            "balance": account_info.balance,
            "equity": account_info.equity,
            "margin": account_info.margin,
            "margin_free": account_info.margin_free,
            "margin_level": account_info.margin_level,
            "trade_mode": account_info.trade_mode
        }
    }