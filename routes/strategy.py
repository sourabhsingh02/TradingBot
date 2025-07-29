# auto_trade.py
from fastapi import APIRouter, HTTPException ,Query
from datetime import datetime
from typing import List
from pydantic import BaseModel
from threading import Thread
import time


from Strategies.predefined_strategies import PREDEFINED_STRATEGIES
from Strategies.strategy_utils import auto_trade_worker
router = APIRouter(prefix= "/autoTrade" , tags=["Auto Trade And Strategies"])


class StrategyApplyRequest(BaseModel):
    strategy_name: str
    symbols: List[str]
    investment: float
    interval: str  # E.g., "M15", "H1"



@router.post("/apply-strategy")
def apply_strategy(request: StrategyApplyRequest):
    for symbol in request.symbols:
        existing = next((s for s in applied_strategies if s["symbol"] == symbol and s["strategy_name"] == request.strategy_name), None)
        if existing:
            continue  # Already applied

        applied_strategies.append({
            "strategy_name": request.strategy_name,
            "symbol": symbol,
            "investment": request.investment,
            "interval": request.interval
        })

        thread = Thread(target=auto_trade_worker, args=(symbol, request.strategy_name, request.investment, request.interval))
        thread.daemon = True
        thread.start()

    return {"message": "Strategy applied to all symbols."}


@router.post("/unapply-strategy")
def unapply_strategy(request: StrategyApplyRequest):
    global applied_strategies
    applied_strategies = [s for s in applied_strategies if not (s["strategy_name"] == request.strategy_name and s["symbol"] in request.symbols)]
    return {"message": "Strategy unapplied from given symbols."}


@router.get("/strategies")
def get_all_strategies():
    return {"strategies": PREDEFINED_STRATEGIES}


@router.get("/applied-strategies")
def get_applied():
    return {"applied": applied_strategies}

@router.get("/strategies/search")
def search_predefined_strategies(query: str = Query(...)):
    query_lower = query.lower()
    matched = [
        strategy["name"]
        for strategy in PREDEFINED_STRATEGIES
        if query_lower in strategy["name"].lower()
    ]
    return {"matched_strategies":matched}

@router.get("/strategies/names")
def get_all_strategy_names():
    names = [strategy["name"] for strategy in PREDEFINED_STRATEGIES]
    return {"strategy_names":names}

 # +++++++++++++++++    OLD  WORKING FOR ONLY BUY CONDITION

# from fastapi import APIRouter, HTTPException
# from pydantic import BaseModel
# from Strategies.predefined_strategies import PREDEFINED_STRATEGIES
# from Strategies.strategy_utils import apply_predefined_strategy_logic
# from SymbolsPairs.forexSymbols import fetch_all_forex_symbols
#
#
# router = APIRouter(prefix="/predefined", tags=["Auto Order And Strategies"])
#
# class PredefinedApplyRequest(BaseModel):
#     symbol: str
#     strategy_name: str
#     interval: str
#     investment: float
#
# @router.get("/list")
# def list_predefined_strategies():
#     return PREDEFINED_STRATEGIES
#
# @router.post("/apply")
# def apply_predefined_strategy(req: PredefinedApplyRequest):
#     try:
#         valid_symbols = fetch_all_forex_symbols()
#         if req.symbol not in valid_symbols:
#             raise HTTPException(status_code=400, detail="Invalid or unsupported symbol")
#
#         results = apply_predefined_strategy_logic(
#             symbol=req.symbol,
#             strategy_name=req.strategy_name,
#             interval=req.interval,
#             investment=req.investment
#         )
#         return {
#             "status": "completed",
#             "strategy": req.strategy_name,
#             "results": results
#         }
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=str(e))