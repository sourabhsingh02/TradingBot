from fastapi import APIRouter, HTTPException
from Orders.Order_Utils  import place_order

router = APIRouter(prefix="/api/order", tags=["Order"])

@router.post("/manual")
def manual_order(symbol: str, market: str, action: str, quantity: float):
    result = place_order(symbol, market, action, quantity)
    if result.get("status") == "error":
        raise HTTPException(400, detail=result.get("message"))
    return result