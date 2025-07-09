import MetaTrader5 as mt5

mt5.initialize()
symbol = "USDINR"

# Check symbol info
symbol_info = mt5.symbol_info(symbol)
if symbol_info is None:
    print(f"{symbol} not found")
elif not symbol_info.visible:
    print(f"{symbol} is not visible, trying to enable...")
    mt5.symbol_select(symbol, True)

# Check again
print(mt5.symbol_info(symbol))