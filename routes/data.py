# from fastapi import APIRouter
# from data_fetcher import fetch_ohlcv , fetch_all_latest
#
# router = APIRouter(prefix="/api/data", tags=["Stock Data"])
#
# @router.get("/{symbol}")
# def get_stock_data(symbol: str):
#     data = fetch_ohlcv(symbol)
#     return {"symbol": symbol, "data": data}
#
# @router.get("/all")
# def get_all_data():
#     return {"data": fetch_all_latest()}

from fastapi import APIRouter
from data_fetcher import fetch_ohlcv, fetch_all_latest

router = APIRouter(prefix="/api" , tags=["Stock Data"])

#  Route to get all data
@router.get("/data/all")
def get_all():
    return {"data": fetch_all_latest()}

#  Route to get specific symbol data
@router.get("/data/{symbol}")
def get_by_symbol(symbol: str):
    return {"symbol": symbol, "data": fetch_ohlcv(symbol)}
