# from fastapi import APIRouter, HTTPException , Query
# from models import CustomSignalRequest
# from strategy_utils import evaluate_strategy
# from strategy_utils import apply_live_strategy, resolve_strategy
# from predefined_strategies import PREDEFINED_STRATEGIES
# from models import CustomSignalRequest, PredefinedSignalRequest
# from LiveDataFetch.forexData import fetch_mt5_candles_by_timeframe
# from models import CustomSignalRequest, PredefinedSignalRequest
# from LiveDataFetch.nseData import fetch_nse_candles_by_timeframe
#
# router = APIRouter(prefix="/api/live", tags=["Live Signal"])
#
# @router.post("/custom")
# def live_custom_signal(payload: CustomSignalRequest):
#     strategy = resolve_strategy(payload)
#     return apply_live_strategy(payload.symbol, strategy, market="forex")
#
#
# @router.post("/predefined")
# def live_predefined_signal(payload: PredefinedSignalRequest):
#     strategy = next((s for s in PREDEFINED_STRATEGIES if s["name"] == payload.strategy_name), None)
#     if not strategy:
#         raise HTTPException(status_code=404, detail="Strategy not found")
#     return apply_live_strategy(payload.symbol, strategy, market="forex")
#
# @router.get("/candles")
# def get_candles(symbol: str = Query(...), timeframe: str = Query("5m"), bars: int = Query(50)):
#     data = fetch_mt5_candles_by_timeframe(symbol, timeframe, bars)
#     if not data:
#         return {"error": "No data"}
#     return {"symbol": symbol, "timeframe": timeframe, "data": data}
#
