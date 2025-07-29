from datetime import datetime
import MetaTrader5 as mt5

def get_current_price(symbol: str):
    tick = mt5.symbol_info_tick(symbol)
    if not tick:
        return None
    return {
        "bid": tick.bid,
        "ask": tick.ask,
        "last": tick.last
    }

def place_buy_order(symbol: str, lot: float):
    price_data = get_current_price(symbol)
    if not price_data:
        return {"status": "error", "message": "Symbol not found or price unavailable"}

    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lot,
        "type": mt5.ORDER_TYPE_BUY,
        "price": price_data["ask"],
        "deviation": 10,
        "magic": 123456,
        "comment": "Manual Buy Order",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }
    result = mt5.order_send(request)
    return {"status": "success" if result.retcode == 10009 else "error", "retcode": result.retcode, "comment": result.comment}

def place_sell_order(symbol: str, lot: float):
    price_data = get_current_price(symbol)
    if not price_data:
        return {"status": "error", "message": "Symbol not found or price unavailable"}

    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lot,
        "type": mt5.ORDER_TYPE_SELL,
        "price": price_data["bid"],
        "deviation": 10,
        "magic": 123456,
        "comment": "Manual Sell Order",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }
    result = mt5.order_send(request)
    return {"status": "success" if result.retcode == 10009 else "error", "retcode": result.retcode, "comment": result.comment}

def close_position_by_ticket(ticket: int):
    if not mt5.initialize():
        return {"status": "error", "message": "MT5 initialization failed"}

    position = mt5.positions_get(ticket=ticket)
    if position is None or len(position) == 0:
        return {"status": "error", "message": "No open position with given ticket"}

    pos = position[0]

    symbol = pos.symbol
    volume = pos.volume
    position_type = pos.type  # 0 = buy, 1 = sell

    price = mt5.symbol_info_tick(symbol).bid if position_type == 0 else mt5.symbol_info_tick(symbol).ask
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

    if result.retcode != mt5.TRADE_RETCODE_DONE:
        return {
            "status": "error",
            "message": f"Failed to close position: {result.comment}",
            "retcode": result.retcode,
        }

    return {"status": "success", "message": "Position closed", "retcode": result.retcode}
