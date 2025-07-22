import json
import os
from data.completeData import get_price_change_today_vs_yesterday
from SymbolsPairs.forexSymbols import get_logo_url
WISHLIST_FILE = "../wishlist.json"

def _load_wishlist():
    try:
        with open(WISHLIST_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError :
        return []

def _save_wishlist(symbols:list):
    with open(WISHLIST_FILE, "w") as f:
        json.dump(symbols ,  f)

def add_to_wishlist(symbol: str) -> bool:
    symbol = symbol.upper()
    data = _load_wishlist()
    if symbol not in data:
        data.append(symbol)
        _save_wishlist(data)
        return True
    return False  # already exists

def remove_from_wishlist(symbol: str) -> bool:
    symbol = symbol.upper()
    data = _load_wishlist()
    if symbol in data:
        data.remove(symbol)
        _save_wishlist(data)
        return True
    return False  # not found


def search_wishlist_by_name(query: str):
    wishlist = _load_wishlist()
    response = []

    query = query.strip().lower()

    for symbol in wishlist:
        if query in symbol.lower():
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

            response.append({
                "symbol": symbol,
                "price": price,
                "change": change,
                "percent": percent,
                "status": status,
                "logo": logo
            })

    return {"wishlist": response}



# def get_wishlist():
#     return _load_wishlist()




def get_wishlist():
    wishlist = _load_wishlist()
    response = []

    for symbol in wishlist:
        try:
            result = get_price_change_today_vs_yesterday(symbol)
            price = result.get("current_price" , 0 )
            change = result .get("change_str" , "N/A")
            percent = result.get("percent_change_str" , "N/A")
            status = result.get("status" , "unknown")
        except Exception:
            price = 0
            change = "N/A"
            percent = "N/A"
            status = "unknown"

        logo = get_logo_url(symbol)

        response.append({
            "symbol": symbol,
            "price": price,
            "change": change,
            "percent": percent,
            "status": status,
            "logo": logo
        })

    return {"wishlist": response}



# import json
# import os
#
# WISHLIST_FILE = "../wishlist.json"
#
# def _load_wishlist():
#     with open(WISHLIST_FILE, "r") as f:
#         return json.load(f)
#
# def _save_wishlist(data):
#     with open(WISHLIST_FILE, "w") as f:
#         json.dump(data, f, indent=2)
#
# def add_to_wishlist(symbol: str, market: str):
#     symbol = symbol.upper()
#     data = _load_wishlist()
#     if symbol not in data[market]:
#         data[market].append(symbol)
#         _save_wishlist(data)
#
# def remove_from_wishlist(symbol: str, market: str):
#     symbol = symbol.upper()
#     data = _load_wishlist()
#     if symbol in data[market]:
#         data[market].remove(symbol)
#         _save_wishlist(data)
#
# def get_wishlist(market: str = None):
#     data = _load_wishlist()
#     if market=="all":
#         return  data
#     return data.get(market, [])
