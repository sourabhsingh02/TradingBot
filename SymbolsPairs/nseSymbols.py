import pandas as pd
def fetch_all_nse_symbols():
    try:
        url = "https://archives.nseindia.com/content/equities/EQUITY_L.csv"
        df = pd.read_csv(url)
        symbols = df['SYMBOL'].dropna().tolist()
        return symbols
    except Exception as e:
        print(f"[ERROR] Failed to fetch NSE symbols: {e}")
        return []