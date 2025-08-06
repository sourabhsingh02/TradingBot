from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from Manual_order.manual_util import place_buy_order, place_sell_order, close_position_by_ticket
import MetaTrader5 as mt5
from database.db_connection import get_connection
from Security.auth import get_current_user
from Security.encryption_mt5 import get_mt5_credentials
router = APIRouter(prefix="/order", tags=["Manual Order"])


class OrderRequest(BaseModel):
    symbol: str
    lot: float


class CloseRequest(BaseModel):
    ticket: int





@router.post("/buy")
def manual_buy(req: OrderRequest, current_user: dict = Depends(get_current_user)):
    creds = get_mt5_credentials(current_user["id"])

    initialized = mt5.initialize(
        login=creds["login"],
        password=creds["password"],
        server=creds["server"]
    )
    if not initialized:
        raise HTTPException(status_code=500, detail="MT5 initialization failed")

    result = place_buy_order(req.symbol, req.lot)
    mt5.shutdown()
    return result


@router.post("/sell")
def manual_sell(req: OrderRequest, current_user: dict = Depends(get_current_user)):
    creds = get_mt5_credentials(current_user["id"])

    initialized = mt5.initialize(
        login=creds["login"],
        password=creds["password"],
        server=creds["server"]
    )
    if not initialized:
        raise HTTPException(status_code=500, detail="MT5 initialization failed")

    result = place_sell_order(req.symbol, req.lot)
    mt5.shutdown()
    return result


@router.post("/close-position")
def close_by_ticket(req: CloseRequest, current_user: dict = Depends(get_current_user)):
    creds = get_mt5_credentials(current_user["id"])

    initialized = mt5.initialize(
        login=creds["login"],
        password=creds["password"],
        server=creds["server"]
    )
    if not initialized:
        raise HTTPException(status_code=500, detail="MT5 initialization failed")

    result = close_position_by_ticket(req.ticket)
    mt5.shutdown()
    return result


@router.post("/close-by-symbol")
def close_position_by_symbol(symbol: str, current_user: dict = Depends(get_current_user)):
    creds = get_mt5_credentials(current_user["id"])

    initialized = mt5.initialize(
        login=creds["login"],
        password=creds["password"],
        server=creds["server"]
    )
    if not initialized:
        raise HTTPException(status_code=500, detail="MT5 initialization failed")

    positions = mt5.positions_get(symbol=symbol)
    if not positions:
        raise HTTPException(status_code=404, detail="No open positions for this symbol")

    for pos in positions:
        close_position_by_ticket(pos.ticket)

    mt5.shutdown()
    return {"message": "Position(s) closed successfully"}