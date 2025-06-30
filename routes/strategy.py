from fastapi import APIRouter, HTTPException
from predefined_strategies import PREDEFINED_STRATEGIES
from strategy_utils import apply_strategy
from saved_strategies import save_strategy, load_saved_strategies
from strategy_utils import resolve_strategy
from models import Condition, Strategy, CustomSignalRequest, PredefinedSignalRequest
from saved_strategies import delete_strategy ,search_saved_strategies

router = APIRouter(prefix="/api/strategy", tags=["Custom Strategy"])

@router.post("/custom-signal")
def get_custom_signal(payload: CustomSignalRequest):
    strategy = resolve_strategy(payload)
    return apply_strategy(payload.symbol, strategy)



@router.post("/predefined-signal")
def get_predefined_signal(payload: PredefinedSignalRequest):
    strategy = next((s for s in PREDEFINED_STRATEGIES if s["name"] == payload.strategy_name), None)
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return apply_strategy(payload.symbol, strategy)



@router.get("/PredefinedList")
def list_strategies():
    return {"strategies": [s["name"] for s in PREDEFINED_STRATEGIES]}




@router.post("/save")
def save_custom_strategy(strategy: Strategy):
    try:
        save_strategy(strategy.dict())
        return {"message": "Strategy saved successfully"}
    except ValueError as err:
        raise HTTPException(status_code=400, detail=str(err))



@router.get("/savedList")
def get_saved_strategies():
    return {"strategies": load_saved_strategies()}

@router.get("/search/saved")
def search_saved(name: str):
    result = search_saved_strategies(name)
    return {"results": result}


@router.get("/search/predefined")
def search_predefined(name: str):
    results = [s for s in PREDEFINED_STRATEGIES if name.lower() in s["name"].lower()]
    return {"results": results}



@router.delete("/delete/{name}")
def delete_saved_strategy(name: str):
    try:
        delete_strategy(name)
        return {"message": f"Strategy '{name}' deleted successfully"}
    except ValueError as err:
        raise HTTPException(status_code=404, detail=str(err))
