from fastapi import APIRouter
from data_fetcher import fetch_ohlcv

router = APIRouter(prefix="/api/data", tags=["Stock Data"])

@router.get("/{symbol}")
def get_stock_data(symbol: str):
    data = fetch_ohlcv(symbol)
    return {"symbol": symbol, "data": data}


# from fastapi import APIRouter
# from data_fetcher import fetch_ohlcv_dhan
#
# router = APIRouter()
#
# @router.get("/api/data/{symbol}")
# def get_data(symbol: str):
#     """
#     Dummy OHLCV data for a given symbol.
#     Later we'll swap fetch_ohlcv_dhan() with real API version.
#     """
#     data = fetch_ohlcv_dhan(symbol)
#     return {"symbol": symbol.upper(), "data": data}
