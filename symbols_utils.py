import json
from pathlib import Path
import pandas as pd

WISHLIST_FILE = Path("wishlist.json")




def fetch_all_symbols():
    try:
        url = "https://archives.nseindia.com/content/equities/EQUITY_L.csv"
        df = pd.read_csv(url)
        symbols = df['SYMBOL'].dropna().tolist()
        return symbols
    except Exception as e:
        print(f"[ERROR] Failed to fetch NSE symbols: {e}")
        return []



# Load once for search (or you can fetch fresh in search)
SYMBOLS = fetch_all_symbols()

def search_symbol(query: str):
    query = query.upper()
    return [s for s in SYMBOLS if query in s]

def read_wishlist():
    if WISHLIST_FILE.exists():
        with open(WISHLIST_FILE, "r") as f:
            return json.load(f)
    return []

def save_wishlist(wishlist):
    with open(WISHLIST_FILE, "w") as f:
        json.dump(wishlist, f)

def add_to_wishlist(symbol):
    symbol = symbol.upper()
    wishlist = read_wishlist()
    if symbol not in wishlist:
        wishlist.append(symbol)
        save_wishlist(wishlist)
    return wishlist

def remove_from_wishlist(symbol):
    symbol = symbol.upper()
    wishlist = read_wishlist()
    if symbol in wishlist:
        wishlist.remove(symbol)
        save_wishlist(wishlist)
    return wishlist
