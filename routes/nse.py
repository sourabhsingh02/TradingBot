from fastapi import APIRouter, Query
from LiveDataFetch.nseData import get_nse_paginated
from LiveDataFetch.LiveData import fetch_live_candles

router = APIRouter(prefix="/nse", tags=["NSE"])

@router.get("/dashboard")
def nse_dashboard(page:int=1, size:int=10, filter:str="all"):
    return get_nse_paginated(page, size, filter)

@router.get("/data/{symbol}")
def nse_symbol(symbol:str):
    return {"symbol":symbol.upper(), "data": fetch_live_candles(symbol.upper(), market="nse")}