from fastapi import APIRouter
from History.history_util import get_open_positions, get_trade_history ,close_position_by_ticket , get_account_info

router = APIRouter(prefix="/history", tags=["History"])

@router.get("/open-positions")
def api_open_positions(symbol: str = None):
    return get_open_positions(symbol)

@router.get("/trade-history")
def api_trade_history():
    return get_trade_history()

@router.get("/close-position")
def close_by_ticket(ticket: int):
    return close_position_by_ticket(ticket)

@router.get("/account-info")
def account_info_api():
    return get_account_info()

