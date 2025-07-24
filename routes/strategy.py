from fastapi import APIRouter, HTTPException , Form
from pydantic import BaseModel
from typing import Optional, List
from uuid import uuid4
from Strategies.strategy_utils import resolve_strategies, monitor_and_trade, place_manual_order
from Strategies.predefined_strategies import PREDEFINED_STRATEGIES
from Strategies.models import Strategy,StrategyCondition,StrategyPayload,StrategyRequest,CUSTOM_STRATEGIES,ManualOrderRequest,Condition

router = APIRouter(prefix="/strategy", tags=["Strategy"])



@router.post("/apply_predefined")
def apply_predefined_strategy(req: StrategyRequest):
    strategies = resolve_strategies(req.strategy_name)
    for strategy in strategies:
        monitor_and_trade(req.symbol, strategy, req.market, req.interval, auto_trade=req.auto_trade)
    return {"status": "watching", "strategies": [s["name"] for s in strategies]}


@router.post("/apply_custom")
def apply_custom_strategy(req: StrategyRequest):
    if not req.strategy:
        raise HTTPException(status_code=400, detail="Strategy payload required")
    strategies = req.strategy if isinstance(req.strategy, list) else [req.strategy]
    for strategy in strategies:
        monitor_and_trade(req.symbol, strategy.dict(), req.market, req.interval, auto_trade=req.auto_trade)
    return {"status": "watching", "strategy": req.strategy.name}


@router.get("/predefined_List")
def list_predefined():
    return PREDEFINED_STRATEGIES


@router.get("/custom_List")
def list_custom():
    return CUSTOM_STRATEGIES



@router.post("/custom_create")
def create_custom_strategy(payload: StrategyPayload):
    payload.id = str(uuid4())
    CUSTOM_STRATEGIES.append(payload.dict())
    return {"status": "created", "id": payload.id}


@router.delete("/custom_delete/{strategy_id}")
def delete_custom(strategy_id: str):
    global CUSTOM_STRATEGIES
    CUSTOM_STRATEGIES = [s for s in CUSTOM_STRATEGIES if s['id'] != strategy_id]
    return {"status": "deleted"}



# @router.post("/manual")  json dene k liye
# def manual_trade(req: ManualOrderRequest):
#     try:
#         success = manual_order(req.symbol, req.action)
#         return {"status": "success" if success else "failed"}
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=str(e))

# for direct parameters
@router.post("/manual")
def manual_order(
        symbol : str ,
        action : str ,
        investment : float ,
):
    return  place_manual_order(symbol , action ,investment)