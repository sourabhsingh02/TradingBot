import json
import os
from typing import List, Dict



BASE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(os.path.dirname(BASE_DIR), "data")

NSE_LIST_FILE   = os.path.join(BASE_DIR, "nse_list.json")
FOREX_LIST_FILE = os.path.join(BASE_DIR, "forex_list.json")
WISHLIST_FILE   = os.path.join(DATA_DIR, "wishlist.json")


if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

if not os.path.exists(WISHLIST_FILE):
    with open(WISHLIST_FILE, "w") as f:
        json.dump({"nse": [], "forex": []}, f, indent=2)



def _load_json(path: str) -> List[str]:
    if not os.path.exists(path):
        return []
    with open(path, "r") as f:
        return json.load(f)

def fetch_all_nse_symbols() -> List[str]:
    return _load_json(NSE_LIST_FILE)

def fetch_all_forex_symbols() -> List[str]:
    return _load_json(FOREX_LIST_FILE)


def search_symbols(query: str, market: str = "all") -> list:
    query = query.upper()
    results = []

    if market == "nse" or market == "all":
        for symbol in fetch_all_nse_symbols():
            if query in symbol.upper():
                results.append({"symbol": symbol, "market": "nse"})

    if market == "forex" or market == "all":
        for symbol in fetch_all_forex_symbols():
            if query in symbol.upper():
                results.append({"symbol": symbol, "market": "forex"})

    return results


def _load_wishlist() -> Dict[str, List[str]]:
    with open(WISHLIST_FILE, "r") as f:
        return json.load(f)

def _save_wishlist(data: Dict[str, List[str]]):
    with open(WISHLIST_FILE, "w") as f:
        json.dump(data, f, indent=2)

def add_to_wishlist(symbol: str, market: str) -> bool:
    market = market.lower()
    symbol = symbol.upper()
    data   = _load_wishlist()
    if market not in data:
        return False
    if symbol not in data[market]:
        data[market].append(symbol)
        _save_wishlist(data)
        return True
    return False

def remove_from_wishlist(symbol: str, market: str) -> bool:
    market = market.lower()
    symbol = symbol.upper()
    data   = _load_wishlist()
    if market not in data:
        return False
    if symbol in data[market]:
        data[market].remove(symbol)
        _save_wishlist(data)
        return True
    return False

def get_wishlist(market: str | None = None):
    data = _load_wishlist()
    if market is None or market == "all":
        return data
    return data.get(market.lower(), [])