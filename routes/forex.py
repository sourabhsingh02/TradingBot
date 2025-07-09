from fastapi import APIRouter, Query
from LiveDataFetch.forexData import get_forex_paginated
from LiveDataFetch.LiveData import fetch_live_candles

router = APIRouter(prefix="/forex", tags=["Forex"])

@router.get("/dashboard")
def forex_dashboard(page:int=1, size:int=10, filter:str="all"):
    return get_forex_paginated(page, size, filter)

@router.get("/data/{symbol}")
def forex_symbol(symbol:str):
    return {"symbol":symbol.upper(), "data": fetch_live_candles(symbol.upper(), market="forex")}

