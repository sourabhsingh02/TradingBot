from datetime import datetime
import MetaTrader5 as mt5


def init_mt5():
    """Initialize MetaTrader 5 safely"""
    if not mt5.initialize():
        return False, {"status": "error", "message": "MT5 initialization failed"}
    return True, None


def shutdown_mt5():
    """Shutdown MetaTrader 5 session"""
    mt5.shutdown()


def get_current_price(symbol: str):
    tick = mt5.symbol_info_tick(symbol)
    if not tick:
        return None
    return {
        "bid": tick.bid,
        "ask": tick.ask,
        "last": tick.last
    }




def safe_result(result):
    """Convert MT5 TradeResult to dict and extract retcode/comment"""
    if isinstance(result, dict):
        retcode = result.get("retcode")
        comment = result.get("comment")
    else:
        retcode = result.retcode
        comment = result.comment
    return retcode, comment


def place_buy_order(symbol: str, lot: float):
    ok, err = init_mt5()
    if not ok:
        return err

    price_data = get_current_price(symbol)
    if not price_data:
        shutdown_mt5()
        return {"status": "error", "message": "Symbol not found or price unavailable"}

    symbol_info = mt5.symbol_info(symbol)
    if symbol_info is None:
        return {"status": "error", "message": f"Symbol {symbol} not found", "retcode": None}

    filling_mode_map = {
        1: mt5.ORDER_FILLING_FOK,
        2: mt5.ORDER_FILLING_IOC,
        3: mt5.ORDER_FILLING_RETURN
    }
    filling_mode = filling_mode_map.get(symbol_info.filling_mode, mt5.ORDER_FILLING_IOC)

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
        "type_filling": filling_mode,
    }

    result = mt5.order_send(request)
    retcode, comment = safe_result(result)

    shutdown_mt5()

    return {
        "status": "success" if retcode == mt5.TRADE_RETCODE_DONE else "error",
        "retcode": retcode,
        "comment": comment
    }


def place_sell_order(symbol: str, lot: float):
    ok, err = init_mt5()
    if not ok:
        return err

    price_data = get_current_price(symbol)
    if not price_data:
        shutdown_mt5()
        return {"status": "error", "message": "Symbol not found or price unavailable"}

    symbol_info = mt5.symbol_info(symbol)
    if symbol_info is None:
        return {"status": "error", "message": f"Symbol {symbol} not found", "retcode": None}

    filling_mode_map = {
        1: mt5.ORDER_FILLING_FOK,
        2: mt5.ORDER_FILLING_IOC,
        3: mt5.ORDER_FILLING_RETURN
    }
    filling_mode = filling_mode_map.get(symbol_info.filling_mode, mt5.ORDER_FILLING_IOC)
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
        "type_filling": filling_mode,
    }

    result = mt5.order_send(request)
    retcode, comment = safe_result(result)

    shutdown_mt5()

    return {
        "status": "success" if retcode == mt5.TRADE_RETCODE_DONE else "error",
        "retcode": retcode,
        "comment": comment
    }


def close_position_by_ticket(ticket):
    try:
        position = mt5.positions_get(ticket=ticket)
        if not position:
            return {"status": "error", "message": "Position not found", "retcode": None}

        position = position[0]
        symbol = position.symbol
        lot = position.volume
        price = mt5.symbol_info_tick(symbol).bid if position.type == 0 else mt5.symbol_info_tick(symbol).ask

        # Detect filling mode dynamically
        symbol_info = mt5.symbol_info(symbol)
        if symbol_info is None:
            return {"status": "error", "message": f"Symbol {symbol} not found", "retcode": None}

        filling_mode_map = {
            1: mt5.ORDER_FILLING_FOK,
            2: mt5.ORDER_FILLING_IOC,
            3: mt5.ORDER_FILLING_RETURN
        }
        filling_mode = filling_mode_map.get(symbol_info.filling_mode, mt5.ORDER_FILLING_IOC)

        close_request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": lot,
            "type": mt5.ORDER_TYPE_SELL if position.type == 0 else mt5.ORDER_TYPE_BUY,
            "position": ticket,
            "price": price,
            "deviation": 20,
            "type_filling": filling_mode,
        }

        result = mt5.order_send(close_request)
        if result.retcode != mt5.TRADE_RETCODE_DONE:
            return {
                "status": "error",
                "message": f"Failed to close position: {result.comment}",
                "retcode": result.retcode
            }
        return {"status": "success", "message": "Position closed successfully", "retcode": result.retcode}

    except Exception as e:
        return {"status": "error", "message": str(e), "retcode": None}





# from datetime import datetime
# import MetaTrader5 as mt5
#
# def get_current_price(symbol: str):
#     tick = mt5.symbol_info_tick(symbol)
#     if not tick:
#         return None
#     return {
#         "bid": tick.bid,
#         "ask": tick.ask,
#         "last": tick.last
#     }
#
# def place_buy_order(symbol: str, lot: float):
#     price_data = get_current_price(symbol)
#     if not price_data:
#         return {"status": "error", "message": "Symbol not found or price unavailable"}
#
#     request = {
#         "action": mt5.TRADE_ACTION_DEAL,
#         "symbol": symbol,
#         "volume": lot,
#         "type": mt5.ORDER_TYPE_BUY,
#         "price": price_data["ask"],
#         "deviation": 10,
#         "magic": 123456,
#         "comment": "Manual Buy Order",
#         "type_time": mt5.ORDER_TIME_GTC,
#         "type_filling": mt5.ORDER_FILLING_IOC,
#     }
#     result = mt5.order_send(request)
#     return {"status": "success" if result.retcode == 10009 else "error", "retcode": result.retcode, "comment": result.comment}
#
# def place_sell_order(symbol: str, lot: float):
#     price_data = get_current_price(symbol)
#     if not price_data:
#         return {"status": "error", "message": "Symbol not found or price unavailable"}
#
#     request = {
#         "action": mt5.TRADE_ACTION_DEAL,
#         "symbol": symbol,
#         "volume": lot,
#         "type": mt5.ORDER_TYPE_SELL,
#         "price": price_data["bid"],
#         "deviation": 10,
#         "magic": 123456,
#         "comment": "Manual Sell Order",
#         "type_time": mt5.ORDER_TIME_GTC,
#         "type_filling": mt5.ORDER_FILLING_IOC,
#     }
#     result = mt5.order_send(request)
#     return {"status": "success" if result.retcode == 10009 else "error", "retcode": result.retcode, "comment": result.comment}
#
# def close_position_by_ticket(ticket: int):
#     if not mt5.initialize():
#         return {"status": "error", "message": "MT5 initialization failed"}
#
#     position = mt5.positions_get(ticket=ticket)
#     if position is None or len(position) == 0:
#         return {"status": "error", "message": "No open position with given ticket"}
#
#     pos = position[0]
#
#     symbol = pos.symbol
#     volume = pos.volume
#     position_type = pos.type
#
#
#     tick = mt5.symbol_info_tick(symbol)
#     if tick is None:
#         return {"status": "error", "message": f"No tick data for {symbol}"}
#
#     price = tick.bid if position_type == 0 else tick.ask
#     order_type = mt5.ORDER_TYPE_SELL if position_type == 0 else mt5.ORDER_TYPE_BUY
#
#
#     symbol_info = mt5.symbol_info(symbol)
#     if symbol_info is None:
#         return {"status": "error", "message": f"Symbol info not available for {symbol}"}
#
#     filling_modes = []
#     if symbol_info.filling_mode & mt5.ORDER_FILLING_FOK:
#         filling_modes.append(mt5.ORDER_FILLING_FOK)
#     if symbol_info.filling_mode & mt5.ORDER_FILLING_IOC:
#         filling_modes.append(mt5.ORDER_FILLING_IOC)
#     if symbol_info.filling_mode & mt5.ORDER_FILLING_RETURN:
#         filling_modes.append(mt5.ORDER_FILLING_RETURN)
#
#     if not filling_modes:
#         return {"status": "error", "message": f"No valid filling mode supported for {symbol}"}
#
#     filling_mode = filling_modes[0]
#
#     # filling_mode = mt5.symbol_info(symbol).filling_mode
#
#     request = {
#         "action": mt5.TRADE_ACTION_DEAL,
#         "symbol": symbol,
#         "volume": volume,
#         "type": order_type,
#         "position": ticket,
#         "price": price,
#         "deviation": 10,
#         "magic": 234000,
#         "comment": "Close position by ticket",
#         "type_time": mt5.ORDER_TIME_GTC,
#         "type_filling": filling_mode,  # Dynamic filling mode
#     }
#
#     # Send the close order
#     result = mt5.order_send(request)
#
#     if result.retcode != mt5.TRADE_RETCODE_DONE:
#         return {
#             "status": "error",
#             "message": f"Failed to close position: {result.comment}",
#             "retcode": result.retcode,
#         }
#
#     return {"status": "success", "message": "Position closed", "retcode": result.retcode}
#
#
# # def close_position_by_ticket(ticket: int):
# #     if not mt5.initialize():
# #         return {"status": "error", "message": "MT5 initialization failed"}
# #
# #     position = mt5.positions_get(ticket=ticket)
# #     if position is None or len(position) == 0:
# #         return {"status": "error", "message": "No open position with given ticket"}
# #
# #     pos = position[0]
# #
# #     symbol = pos.symbol
# #     volume = pos.volume
# #     position_type = pos.type  # 0 = buy, 1 = sell
# #
# #     price = mt5.symbol_info_tick(symbol).bid if position_type == 0 else mt5.symbol_info_tick(symbol).ask
# #     order_type = mt5.ORDER_TYPE_SELL if position_type == 0 else mt5.ORDER_TYPE_BUY
# #
# #     request = {
# #         "action": mt5.TRADE_ACTION_DEAL,
# #         "symbol": symbol,
# #         "volume": volume,
# #         "type": order_type,
# #         "position": ticket,
# #         "price": price,
# #         "deviation": 10,
# #         "magic": 234000,
# #         "comment": "Close position by ticket",
# #         "type_time": mt5.ORDER_TIME_GTC,
# #         "type_filling": mt5.ORDER_FILLING_IOC,
# #     }
# #
# #     result = mt5.order_send(request)
# #
# #     if result.retcode != mt5.TRADE_RETCODE_DONE:
# #         return {
# #             "status": "error",
# #             "message": f"Failed to close position: {result.comment}",
# #             "retcode": result.retcode,
# #         }
# #
# #     return {"status": "success", "message": "Position closed", "retcode": result.retcode}