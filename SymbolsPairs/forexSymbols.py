from App.api_config import MT5_LOGIN, MT5_PASSWORD, MT5_SERVER
import MetaTrader5 as mt5

def fetch_all_forex_symbols() -> list:
    if not mt5.initialize(login=MT5_LOGIN(), password=MT5_PASSWORD(), server=MT5_SERVER()):
        print("MT5 initialization failed:", mt5.last_error())
        return []

    all_symbols = mt5.symbols_get()
    forex_crypto = []

    for sym in all_symbols:
        name = sym.name.upper()
        if len(name) == 6 and "USD" in name:
            forex_crypto.append(name)
        elif any(coin in name for coin in ["BTC", "ETH", "LTC", "XRP", "DOGE", "SOL", "ADA", "DOT", "BCH", "XLM", "EOS", "BNB", "AVAX"]) and name.endswith("USD"):
            forex_crypto.append(name)

    mt5.shutdown()
    return list(set(forex_crypto))

def get_logo_url(symbol: str):
    symbol = symbol.upper()
    crypto_map = {
        "BTC": "bitcoin-btc",
        "ETH": "ethereum-eth",
        "DOGE": "dogecoin-doge",
        "XRP": "ripple-xrp",
        "LTC": "litecoin-ltc",
        "BNB": "binance-coin-bnb",
        "SOL": "solana-sol",
        "ADA": "cardano-ada",
        "DOT": "polkadot-new-dot",
        "BCH": "bitcoin-cash-bch",
        "XLM": "stellar-xlm",
        "EOS": "eos-eos",
        "AVAX": "avalanche-avax"
    }

    for coin, slug in crypto_map.items():
        if coin in symbol:
            return f"https://cryptologos.cc/logos/{slug}-logo.png"

    if len(symbol) == 6:
        base, quote = symbol[:3].lower(), symbol[3:].lower()
        return [f"https://flagcdn.com/w80/{base}.png", f"https://flagcdn.com/w80/{quote}.png"]

    return "https://yourdomain.com/static/default.png"

def fetch_symbols_with_logos():
    symbols = fetch_all_forex_symbols()
    result = []

    for sym in symbols:
        result.append({
            "symbol": sym,
            "logo": get_logo_url(sym)
        })

    return result