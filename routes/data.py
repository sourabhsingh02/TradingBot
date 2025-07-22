from fastapi import APIRouter, Query
from typing import Optional
import MetaTrader5 as mt5
from datetime import datetime, timedelta
from data.completeData import fetch_mt5_historical_data, fetch_mt5_tick_data ,fetch_tick_data_last_n_minutes , get_price_change_today_vs_yesterday


router = APIRouter(prefix="/Data", tags=["DataFetch"])


@router.get("/mt5/ohlcv")
def get_mt5_ohlcv_data(
    symbol: str = Query(..., description="Symbol name e.g. 'EURUSD'"),
    interval: str = Query("1d", description="Time interval: 1min, 5min, 15min, 1h, 1d"),
    days: int = Query(3, description="Number of past days")
):
    try:
        data = fetch_mt5_historical_data(symbol, interval, days)
        return {"status": "success", "data": data}
    except Exception as e:
        return {"status": "error", "message": str(e)}


@router.get("/mt5/ticks_days")
def get_mt5_tick_data(
    symbol: str = Query(..., description="Symbol name e.g. 'EURUSD'"),
    days: int = Query(1, description="Number of past days to fetch tick data for (default: 1)")
):
    try:
        data = fetch_mt5_tick_data(symbol, days)
        return {"status": "success", "data": data}
    except Exception as e:
        return {"status": "error", "message": str(e)}


@router.get("/mt5/ticks_minutes")
def get_mt5_ticks_filtered(symbol:str , minutes :int = 1) :
    return fetch_tick_data_last_n_minutes(symbol , minutes)




@router.get("/Data/price-change")
def get_price_change_api(symbol: str):
    return get_price_change_today_vs_yesterday(symbol)