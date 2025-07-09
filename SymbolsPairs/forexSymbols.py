import MetaTrader5 as mt5
from App.api_config import MT5_LOGIN, MT5_PASSWORD, MT5_SERVER


def fetch_all_forex_symbols() -> list:
    if not mt5.initialize(login=MT5_LOGIN, password=MT5_PASSWORD, server=MT5_SERVER):
        print("MT5 initialization failed:", mt5.last_error())
        return []

    all_symbols = mt5.symbols_get()
    forex_crypto = []

    for sym in all_symbols:
        name = sym.name.upper()
        # Common forex filter
        if len(name) == 6 and "USD" in name:
            forex_crypto.append(name)
        # Crypto filter (flexible length, must end with USD)
        elif any(coin in name for coin in ["BTC", "ETH", "LTC", "XRP", "DOGE", "SOL", "ADA", "DOT", "BCH", "XLM", "EOS", "BNB", "AVAX"]) and name.endswith("USD"):
            forex_crypto.append(name)

    mt5.shutdown()
    return list(set(forex_crypto))

