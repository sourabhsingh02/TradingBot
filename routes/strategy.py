from fastapi import APIRouter, HTTPException, Query
from typing import List
from Strategies.models import (CustomSignalRequest, PredefinedSignalRequest, Strategy, )
from Strategies.predefined_strategies import PREDEFINED_STRATEGIES
from Strategies.strategy_utils import (resolve_strategy, apply_strategy, apply_live_strategy,apply_multiple_strategies )
from Strategies.saved_strategies import (load_saved_strategies, save_strategy, delete_strategy, search_saved_strategies, )
from PastDataFetch.data_fetcher import fetch_ohlcv
from LiveDataFetch.LiveData import fetch_live_candles
import pandas as pd

router = APIRouter(prefix="/api/strategy", tags=["Strategies"])


@router.post("/apply/predefined")
def apply_predefined(req: PredefinedSignalRequest,
                     mode: str = Query("past", enum=["past", "live"])):
    if not (req.strategy_name or req.strategy_names):
        raise HTTPException(status_code=400, detail="Provide strategy_name(s)")

    names = [req.strategy_name] if req.strategy_name else req.strategy_names
    strategies = []
    for n in names:
        strat = next((s for s in PREDEFINED_STRATEGIES if s["name"] == n), None)
        if not strat:
            raise HTTPException(status_code=404, detail=f"Strategy '{n}' not found")
        strategies.append(strat)

    df = _get_df(req.symbol, req.market, mode)
    if len(strategies) == 1:
        return apply_multiple_strategies(df, strategies)[0]  # return single dict
    return {
        "symbol": req.symbol,
        "market": req.market,
        "mode": mode,
        "results": apply_multiple_strategies(df, strategies)
    }


@router.get("/predefined/list", response_model=List[str])
def list_predefined():
    return [s["name"] for s in PREDEFINED_STRATEGIES]



@router.get("/predefined/search")
def search_predefined(query: str = Query(...)):
    results = [s for s in PREDEFINED_STRATEGIES if query.lower() in s["name"].lower()]
    return {"results": results}


@router.post("/apply/custom")
def apply_custom(req: CustomSignalRequest,
                 mode: str = Query("past", enum=["past", "live"])):

    if req.strategy is None:
        raise HTTPException(status_code=400, detail="strategy missing")

    # accept list or single
    strategies: List[Strategy] = req.strategy if isinstance(req.strategy, list) else [req.strategy]


    for s in strategies:
        try:
            save_strategy(s.dict())
        except ValueError:
            pass  # already exists -> ignore

    df = _get_df(req.symbol, req.market, mode)
    if len(strategies) == 1:
        return apply_multiple_strategies(df, [s.dict() for s in strategies])[0]
    return {
        "symbol": req.symbol,
        "market": req.market,
        "mode": mode,
        "results": apply_multiple_strategies(df, [s.dict() for s in strategies])
    }



@router.get("/custom/list")
def list_saved():
    return {"strategies": load_saved_strategies()}


@router.delete("/custom/{name}")
def remove_saved(name: str):
    try:
        delete_strategy(name)
        return {"message": f"Strategy '{name}' deleted"}
    except ValueError as err:
        raise HTTPException(status_code=404, detail=str(err))



@router.get("/custom/search")
def search_saved(query: str = Query(...)):
    return {"results": search_saved_strategies(query)}


@router.put("/custom/{name}")
def update_saved(name: str, strategy: Strategy):
    strategies = load_saved_strategies()
    idx = next((i for i, s in enumerate(strategies) if s["name"] == name), None)
    if idx is None:
        raise HTTPException(status_code=404, detail=f"Strategy '{name}' not found")


    if strategy.name != name and any(s["name"] == strategy.name for s in strategies):
        raise HTTPException(status_code=400, detail="New name already exists")

    strategies[idx] = strategy.dict()

    from Strategies.saved_strategies import _write_file  # type: ignore

    _write_file(strategies)
    return {"message": f"Strategy '{name}' updated"}





def _get_df(symbol, market, mode):
    raw = fetch_live_candles(symbol, market) if mode == "live" else fetch_ohlcv(symbol, market)
    if not raw:
        raise HTTPException(status_code=404, detail="No data")
    return pd.DataFrame(raw)












# from fastapi import APIRouter, HTTPException
# from predefined_strategies import PREDEFINED_STRATEGIES
# from strategy_utils import apply_strategy
# from saved_strategies import save_strategy, load_saved_strategies
# from strategy_utils import resolve_strategy
# from models import Condition, Strategy, CustomSignalRequest, PredefinedSignalRequest
# from saved_strategies import delete_strategy ,search_saved_strategies
#
# router = APIRouter(prefix="/api/strategy", tags=["Strategies"])
#
# @router.post("/custom-signal")
# def get_custom_signal(payload: CustomSignalRequest):
#     strategy = resolve_strategy(payload)
#     return apply_strategy(payload.symbol, strategy)
#
# @router.post("/save")
# def save_custom_strategy(strategy: Strategy):
#     try:
#         save_strategy(strategy.dict())
#         return {"message": "Strategy saved successfully"}
#     except ValueError as err:
#         raise HTTPException(status_code=400, detail=str(err))
#
# @router.get("/savedList")
# def get_saved_strategies():
#     return {"strategies": load_saved_strategies()}
#
#
# @router.get("/search/saved")
# def search_saved(name: str):
#     result = search_saved_strategies(name)
#     return {"results": result}
#
#
#
# @router.post("/predefined-signal")
# def get_predefined_signal(payload: PredefinedSignalRequest):
#     strategy = next((s for s in PREDEFINED_STRATEGIES if s["name"] == payload.strategy_name), None)
#     if not strategy:
#         raise HTTPException(status_code=404, detail="Strategy not found")
#     return apply_strategy(payload.symbol, strategy)
#
#
# @router.get("/PredefinedList")
# def list_strategies():
#     return {"strategies": [s["name"] for s in PREDEFINED_STRATEGIES]}
#
#
# @router.get("/search/predefined")
# def search_predefined(name: str):
#     results = [s for s in PREDEFINED_STRATEGIES if name.lower() in s["name"].lower()]
#     return {"results": results}
#
#
# @router.delete("/delete/{name}")
# def delete_saved_strategy(name: str):
#     try:
#         delete_strategy(name)
#         return {"message": f"Strategy '{name}' deleted successfully"}
#     except ValueError as err:
#         raise HTTPException(status_code=404, detail=str(err))
