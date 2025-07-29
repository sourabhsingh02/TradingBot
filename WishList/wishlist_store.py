from typing import List
from database.db_connection import get_connection
from SymbolsPairs.forexSymbols import get_logo_url
from data.completeData import get_price_change_today_vs_yesterday


def format_symbol_data(symbols: list[str]) -> list[dict]:
    response = []
    for sym in symbols:
        price_data = get_price_change_today_vs_yesterday(sym)
        if not price_data or "error" in price_data:
            print(f"[Warning] Missing data for symbol: {sym}")
            continue

        response.append({
            "symbol": sym,
            "price": price_data.get("current_price", 0),
            "change": price_data.get("change", "N/A"),
            "percent": price_data.get("percent_change", "N/A"),
            "status": price_data.get("status", "unknown"),
            "logo": get_logo_url(sym)
        })
    return response


def add_to_wishlist(symbol: str, user_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO wishlist (user_id, symbol) VALUES (%s, %s)", (user_id, symbol))
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "Added to wishlist"}


def remove_from_wishlist(symbol: str, user_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM wishlist WHERE user_id = %s AND symbol = %s", (user_id, symbol))
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "Removed from wishlist"}


def get_wishlist(user_id: int) -> list[dict]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT symbol FROM wishlist WHERE user_id = %s", (user_id,))
    symbols = [row[0] for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return format_symbol_data(symbols)


def search_wishlist_item(user_id: int, keyword: str) -> list[dict]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT symbol FROM wishlist WHERE user_id = %s AND symbol LIKE %s", (user_id, f"%{keyword}%"))
    symbols = [row[0] for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return format_symbol_data(symbols)


def clear_wishlist(user_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM wishlist WHERE user_id = %s", (user_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "Wishlist cleared"}


# import json
# import os
# from data.completeData import get_price_change_today_vs_yesterday
# from SymbolsPairs.forexSymbols import get_logo_url
# WISHLIST_FILE = "../wishlist.json"
#
# def _load_wishlist():
#     try:
#         with open(WISHLIST_FILE, "r") as f:
#             return json.load(f)
#     except FileNotFoundError :
#         return []
#
# def _save_wishlist(symbols:list):
#     with open(WISHLIST_FILE, "w") as f:
#         json.dump(symbols ,  f)
#
# def add_to_wishlist(symbol: str) -> bool:
#     symbol = symbol.upper()
#     data = _load_wishlist()
#     if symbol not in data:
#         data.append(symbol)
#         _save_wishlist(data)
#         return True
#     return False  # already exists
#
# def remove_from_wishlist(symbol: str) -> bool:
#     symbol = symbol.upper()
#     data = _load_wishlist()
#     if symbol in data:
#         data.remove(symbol)
#         _save_wishlist(data)
#         return True
#     return False  # not found
#
#
# def search_wishlist_by_name(query: str):
#     wishlist = _load_wishlist()
#     response = []
#
#     query = query.strip().lower()
#
#     for symbol in wishlist:
#         if query in symbol.lower():
#             try:
#                 result = get_price_change_today_vs_yesterday(symbol)
#                 price = result.get("current_price", 0)
#                 change = result.get("change_str", "N/A")
#                 percent = result.get("percent_change_str", "N/A")
#                 status = result.get("status", "unknown")
#             except Exception:
#                 price = 0
#                 change = "N/A"
#                 percent = "N/A"
#                 status = "unknown"
#
#             try:
#                 logo = get_logo_url(symbol)
#             except Exception:
#                 logo = []
#
#             response.append({
#                 "symbol": symbol,
#                 "price": price,
#                 "change": change,
#                 "percent": percent,
#                 "status": status,
#                 "logo": logo
#             })
#
#     return {"wishlist": response}
#
#
#
#
# def get_wishlist():
#     wishlist = _load_wishlist()
#     response = []
#
#     for symbol in wishlist:
#         try:
#             result = get_price_change_today_vs_yesterday(symbol)
#             price = result.get("current_price" , 0 )
#             change = result .get("change_str" , "N/A")
#             percent = result.get("percent_change_str" , "N/A")
#             status = result.get("status" , "unknown")
#         except Exception:
#             price = 0
#             change = "N/A"
#             percent = "N/A"
#             status = "unknown"
#
#         logo = get_logo_url(symbol)
#
#         response.append({
#             "symbol": symbol,
#             "price": price,
#             "change": change,
#             "percent": percent,
#             "status": status,
#             "logo": logo
#         })
#
#     return {"wishlist": response}
#
#
#
