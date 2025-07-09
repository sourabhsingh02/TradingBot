import json
import os

WISHLIST_FILE = "../wishlist.json"

def _load_wishlist():
    with open(WISHLIST_FILE, "r") as f:
        return json.load(f)

def _save_wishlist(data):
    with open(WISHLIST_FILE, "w") as f:
        json.dump(data, f, indent=2)

def add_to_wishlist(symbol: str, market: str):
    symbol = symbol.upper()
    data = _load_wishlist()
    if symbol not in data[market]:
        data[market].append(symbol)
        _save_wishlist(data)

def remove_from_wishlist(symbol: str, market: str):
    symbol = symbol.upper()
    data = _load_wishlist()
    if symbol in data[market]:
        data[market].remove(symbol)
        _save_wishlist(data)

def get_wishlist(market: str = None):
    data = _load_wishlist()
    if market=="all":
        return  data
    return data.get(market, [])
