import json
import os
from typing import List
from datetime import datetime
import pytz


BASE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(os.path.dirname(BASE_DIR), "data")

FOREX_LIST_FILE = os.path.join(BASE_DIR, "forex_list.json")
# WISHLIST_FILE   = os.path.join(DATA_DIR, "wishlist.json")

# Ensure data folder exists
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

# If wishlist doesn't exist, initialize with empty forex list

# if not os.path.exists(WISHLIST_FILE):
#     with open(WISHLIST_FILE, "w") as f:
#         json.dump({"forex": []}, f, indent=2)

def _load_json(path: str) -> List[str]:
    if not os.path.exists(path):
        return []
    with open(path, "r") as f:
        return json.load(f)

def fetch_all_forex_symbols() -> List[str]:
    return _load_json(FOREX_LIST_FILE)

def search_symbol(query: str):
    from data.completeData import get_price_change_today_vs_yesterday
    from SymbolsPairs.forexSymbols import fetch_all_forex_symbols, get_logo_url

    all_symbols = fetch_all_forex_symbols()
    query_lower = query.strip().lower()

    matched = [s for s in all_symbols if query_lower in s.lower()]
    results = []

    for symbol in matched[:20]:
        try:
            result = get_price_change_today_vs_yesterday(symbol)
            price = result.get("current_price", 0)
            change = result.get("change_str", "N/A")
            percent = result.get("percent_change_str", "N/A")
            status = result.get("status", "unknown")
        except Exception:
            price = 0
            change = "N/A"
            percent = "N/A"
            status = "unknown"

        try:
            logo = get_logo_url(symbol)
        except Exception:
            logo = []

        results.append({
            "symbol": symbol,
            "price": price,
            "change": change,
            "percent": percent,
            "status": status,
            "logo": logo
        })

    return results




