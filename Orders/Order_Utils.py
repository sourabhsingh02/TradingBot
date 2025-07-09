import MetaTrader5 as mt5
import requests
from App.api_config import MT5_LOGIN, MT5_PASSWORD, MT5_SERVER, DHAN_ORDER_URL, ACCESS_TOKEN

def place_order(symbol: str, market: str, action: str, quantity: float):
    if market == "forex":
        if not mt5.initialize(login=MT5_LOGIN, password=MT5_PASSWORD, server=MT5_SERVER):
            return {"status": "error", "message": "MT5 init failed"}

        price = mt5.symbol_info_tick(symbol).ask if action == "buy" else mt5.symbol_info_tick(symbol).bid
        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": quantity,
            "type": mt5.ORDER_TYPE_BUY if action == "buy" else mt5.ORDER_TYPE_SELL,
            "price": price,
            "deviation": 10,
            "magic": 123456,
            "comment": "Auto/Manual Order",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
        }
        result = mt5.order_send(request)
        mt5.shutdown()
        return {"status": result.retcode, "details": result._asdict()}

    elif market == "nse":
        try:
            payload = {
                "transaction_type": "BUY" if action == "buy" else "SELL",
                "quantity": int(quantity),
                "symbol": symbol,
                "order_type": "MARKET",
                "product_type": "INTRADAY"
            }
            headers = {"access-token": ACCESS_TOKEN, "Content-Type": "application/json"}
            res = requests.post(DHAN_ORDER_URL, json=payload, headers=headers)
            return res.json()
        except Exception as e:
            return {"status": "error", "message": str(e)}

    return {"status": "error", "message": "Invalid market"}