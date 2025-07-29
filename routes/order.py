from fastapi import APIRouter , HTTPException
from pydantic import BaseModel
from Manual_order.manual_util import place_buy_order , place_sell_order , close_position_by_ticket
import MetaTrader5  as mt5
router = APIRouter(prefix="/order", tags=["Manual Order"])

class OrderRequest(BaseModel):
    symbol: str
    lot: float

@router.post("/buy")
def manual_buy(req: OrderRequest):
    if not mt5.initialize():
        raise HTTPException(status_code=500, detail="MT5 initialization failed")

    result = place_buy_order(req.symbol, req.lot)
    mt5.shutdown()
    return result

@router.post("/sell")
def manual_sell(req: OrderRequest):
    if not mt5.initialize():
        raise HTTPException(status_code=500, detail="MT5 initialization failed")

    result = place_sell_order(req.symbol, req.lot)
    mt5.shutdown()
    return result

@router.get("/close-position")
def close_by_ticket(ticket: int):
    return close_position_by_ticket(ticket)