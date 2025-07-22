from fastapi import APIRouter, Query
from data.completeData import fetch_mt5_tick_data

router = APIRouter(prefix="/forex", tags=["Forex"])

@router.get("/dashboard")
def forex_dashboard(page:int=1, size:int=10, filter:str="all"):
    return fetch_mt5_tick_data(page, size, filter)

@router.get("/data/{symbol}")
def forex_symbol(symbol:str):
    return {"symbol":symbol.upper(), "data": fetch_mt5_tick_data(symbol.upper(), market="forex")}

