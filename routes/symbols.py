from fastapi import APIRouter, Query
from symbols_utils import fetch_all_symbols , search_symbol
from data_fetcher import fetch_ohlcv
from typing import List

router = APIRouter(prefix="/api/symbols", tags=["Symbols"])

@router.get("/list")
def get_symbols(page: int = Query(1, ge=1), size: int = Query(10, ge=1, le=100)):

    symbols = fetch_all_symbols()
    total = len(symbols)

    start = (page - 1) * size
    end = start + size
    paginated = symbols[start:end]

    return {
        "page": page,
        "page_size": size,
        "total_symbols": total,
        "symbols": paginated
    }

@router.get("/search")
def search_symbols(query: str = Query(..., min_length=1)):
    symbols: List[str] = search_symbol(query)
    results = []

    for symbol in symbols[:10]:  # Limit to top 10 results
        candles = fetch_ohlcv(symbol)
        if len(candles) < 2:
            continue

        last = candles[-1]
        prev = candles[-2]

        try:
            change_percent = round(((last["close"] - prev["close"]) / prev["close"]) * 100, 2)
        except ZeroDivisionError:
            change_percent = 0.0

        results.append({
            "symbol": symbol,
            "close": last["close"],
            "change_percent": change_percent,
            "timestamp": last["timestamp"]
        })

    return {"results": results}