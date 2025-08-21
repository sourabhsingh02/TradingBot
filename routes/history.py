from fastapi import APIRouter, Depends, Query
from History.history_util import (
    get_open_positions,
    get_trade_history,
    close_position_by_ticket,
    get_account_info ,
    get_open_positions_by_user
)
from Security.auth import get_current_user
from fastapi import APIRouter, Depends
from database.db_connection import get_connection



router = APIRouter(prefix="/history", tags=["History"])


@router.get("/open-positions")
def open_positions_by_symbol(
    symbol: str = Query(default=None),
    current_user: dict = Depends(get_current_user)
):
    return get_open_positions(user_id=current_user["id"], symbol=symbol)


@router.get("/my-open-positions")
def user_open_positions(current_user: dict = Depends(get_current_user)):
    return get_open_positions_by_user(current_user["id"])

@router.get("/trade-history")
def trade_history(current_user: dict = Depends(get_current_user)):
    return get_trade_history(user_id=current_user["id"])


# def close_by_ticket(
#     ticket: int = Query(...),
#     current_user: dict = Depends(get_current_user)
# ):
#     return close_position_by_ticket(user_id=current_user["id"], ticket=ticket)


@router.get("/account-info")
def account_info_api(current_user: dict = Depends(get_current_user)):
    return get_account_info(user_id=current_user["id"])


@router.get("/active-strategies")
def get_active_strategies(current_user: dict = Depends(get_current_user)):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT a.symbol, a.investment, a.time_interval, a.strategy_type,
               CASE 
                   WHEN a.strategy_type = 'predefined' THEN p.name 
                   ELSE c.name 
               END AS strategy_name
        FROM applied_strategy a
        LEFT JOIN predefined_strategies p ON a.strategy_type = 'predefined' AND a.strategy_id = p.id
        LEFT JOIN custom_strategy c ON a.strategy_type = 'custom' AND a.strategy_id = c.id
        WHERE a.user_id = %s AND a.is_active = TRUE
    """, (current_user["id"],))

    results = cursor.fetchall()
    cursor.close()
    conn.close()

    return {"active_strategies": results}
