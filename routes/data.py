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

from fastapi import APIRouter , Query

from data_fetcher import fetch_ohlcv, fetch_all_paginated

router = APIRouter(prefix="/api" , tags=["Stock Data"])

#  Route to get all data


@router.get("/dashboard")
def get_dashboard_data(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
):
    # filter_type pass nahi kar rahe, default None se all data milega
    return fetch_all_paginated(page=page, size=size)


#  Route to get specific symbol data
@router.get("/data/{symbol}")
def get_by_symbol(symbol: str):
    return {"symbol": symbol, "data": fetch_ohlcv(symbol)}


@router.get("/filter")
def filter_stocks(
    filter: str = Query(..., enum=["gainers", "losers", "volatile"]),
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100)
):
    return fetch_all_paginated(page=page, size=size, filter_type=filter)
