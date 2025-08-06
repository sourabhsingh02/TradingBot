from data.completeData import get_price_change_today_vs_yesterday , fetch_mt5_tick_data
from SymbolsPairs.forexSymbols import fetch_all_forex_symbols, get_logo_url


def paginate_data(data, page: int = 1, limit: int = 10):
    start = (page - 1) * limit
    end = start + limit
    return data[start:end]

def get_all_metrics():
    symbols = fetch_all_forex_symbols()
    results = []

    for symbol in symbols:
        try:
            data = get_price_change_today_vs_yesterday(symbol)
            if data and data.get("status") == "success":
                percent_change = data["percent_change"]
                results.append({
                    "symbol": symbol,
                    "price": data["current_price"],
                    "change": data["change_str"],  # includes + or -
                    "percent": data["percent_change_str"],  # includes % and sign
                    "absolute_percent": abs(percent_change),  # for sorting trending
                    "status": "up" if percent_change > 0 else "down",
                    "logo": get_logo_url(symbol)
                })
        except Exception as e:
            print(f"Error in {symbol}: {e}")

    return results

def get_top_gainers(page :int =1 , limit : int =10):
    all_data = get_all_metrics()
    gainers = sorted(
        [x for x in all_data if x["status"] == "up"],
        key=lambda x: float(x["percent"].replace("%", "")),
        reverse=True
    )
    paginated = paginate_data(gainers , page , limit)
    return {
        "page" :page ,
        "limit" : limit ,
        "total" : len(gainers) ,
        "result" : paginated
    }



def get_top_losers(page :int =1 , limit : int =10):
    all_data = get_all_metrics()
    losers = sorted(
        [x for x in all_data if x["status"] == "down"],
        key=lambda x: float(x["percent"].replace("%", ""))
    )
    paginated = paginate_data(losers, page, limit)
    return {
        "page": page,
        "limit": limit,
        "total": len(losers),
        "result": paginated
    }


def get_most_volatile(page :int =1 , limit : int =10):
    all_data = get_all_metrics()
    volatile = sorted(
        all_data,
        key=lambda x: abs(float(x["absolute_percent"])),
        reverse=True
    )
    paginated = paginate_data(volatile, page, limit)
    return {
        "page": page,
        "limit": limit,
        "total": len(volatile),
        "result": paginated
    }


def get_top_movers(page :int =1 , limit : int =10):
    all_data = get_all_metrics()
    trending = sorted(all_data, key=lambda x:x["absolute_percent"], reverse=True)
    paginated = paginate_data(trending, page, limit)
    return {
        "page": page,
        "limit": limit,
        "total": len(trending),
        "result": paginated
    }