from threading import Thread
from fastapi import APIRouter, Depends, HTTPException
from typing import List
from pydantic import BaseModel
import uuid

from Strategies.auto_trade_util import auto_trade_worker
from database.db_connection import get_connection
from Security.auth import get_current_user

router = APIRouter(prefix="/auto-order", tags=["Auto Order"])


class StrategyApplyRequest(BaseModel):
    strategy_name: str
    symbols: List[str]
    lot: int
    interval: str


@router.post("/apply-predefined-strategy")
def apply_predefined_strategy(
    request: StrategyApplyRequest,
    current_user: dict = Depends(get_current_user)
):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM predefined_strategies WHERE name = %s", (request.strategy_name,))
    strategy = cursor.fetchone()

    if not strategy:
        raise HTTPException(status_code=404, detail="Predefined strategy not found")

    for symbol in request.symbols:
        instance_id = str(uuid.uuid4())  # Unique ID for this instance

        cursor.execute("""
            INSERT INTO applied_strategy (user_id, strategy_id, symbol, lot, time_interval, strategy_type, instance_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (current_user["id"], strategy["id"], symbol, request.lot, request.interval, "predefined", instance_id))
        conn.commit()

        # Start independent worker thread
        thread = Thread(
            target=auto_trade_worker,
            args=(symbol, strategy, request.lot, request.interval, current_user["id"], "predefined", instance_id)
        )
        thread.daemon = True
        thread.start()

    cursor.close()
    conn.close()

    return {"message": "Predefined strategy applied to multiple symbols/instances successfully"}


@router.post("/apply-custom-strategy")
def apply_custom_strategy(
    request: StrategyApplyRequest,
    current_user: dict = Depends(get_current_user)
):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT * FROM custom_strategy
        WHERE name = %s AND user_id = %s
    """, (request.strategy_name, current_user["id"]))
    strategy = cursor.fetchone()

    if not strategy:
        raise HTTPException(status_code=404, detail="Custom strategy not found for user")

    for symbol in request.symbols:
        instance_id = str(uuid.uuid4())

        cursor.execute("""
            INSERT INTO applied_strategy (user_id, strategy_id, symbol, lot, time_interval, strategy_type, instance_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (current_user["id"], strategy["id"], symbol, request.lot, request.interval, "custom", instance_id))
        conn.commit()

        # Start independent worker thread
        thread = Thread(
            target=auto_trade_worker,
            args=(symbol, strategy, request.lot, request.interval, current_user["id"], "custom", instance_id)
        )
        thread.daemon = True
        thread.start()

    cursor.close()
    conn.close()

    return {"message": "Custom strategy applied to multiple symbols/instances successfully"}


@router.get("/active-strategies")
def get_active_strategies(current_user: dict = Depends(get_current_user)):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT a.symbol, a.lot, a.time_interval, a.strategy_type, a.instance_id,
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


class StrategyUnapplyRequest(BaseModel):
    instance_id: str  # Now we use instance_id to stop a specific running instance


@router.post("/unapply")
def unapply_strategy(
    request: StrategyUnapplyRequest,
    current_user: dict = Depends(get_current_user)
):
    conn = get_connection()
    cursor = conn.cursor()

    # Mark this specific instance inactive
    cursor.execute("""
        UPDATE applied_strategy
        SET is_active = FALSE
        WHERE user_id = %s AND instance_id = %s
    """, (current_user["id"], request.instance_id))

    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="No active strategy found for the given instance_id")

    conn.commit()
    cursor.close()
    conn.close()

    return {"message": f"Strategy instance {request.instance_id} unapplied successfully"}



# from threading import Thread
# from fastapi import APIRouter, Depends, HTTPException
# from typing import List
# from pydantic import BaseModel
#
# from Strategies.auto_trade_util import auto_trade_worker
# from database.db_connection import get_connection
# from Security.auth import get_current_user
#
# router = APIRouter(prefix="/auto-order", tags=["Auto Order"])
#
#
# class StrategyApplyRequest(BaseModel):
#     strategy_name: str
#     symbols: List[str]
#     lot: int
#     interval: str
#
#
# @router.post("/apply-predefined-strategy")
# def apply_predefined_strategy(
#         request: StrategyApplyRequest,
#         current_user: dict = Depends(get_current_user)
# ):
#     conn = get_connection()
#     cursor = conn.cursor(dictionary=True)
#
#     cursor.execute("SELECT * FROM predefined_strategies WHERE name = %s", (request.strategy_name,))
#     strategy = cursor.fetchone()
#
#     if not strategy:
#         raise HTTPException(status_code=404, detail="Predefined strategy not found")
#
#     for symbol in request.symbols:
#         cursor.execute("""
#             SELECT id FROM applied_strategy
#             WHERE user_id = %s AND strategy_id = %s AND symbol = %s AND is_active = TRUE
#         """, (current_user["id"], strategy["id"], symbol))
#
#         if cursor.fetchone():
#             continue
#
#         cursor.execute("""
#             INSERT INTO applied_strategy (user_id, strategy_id, symbol, lot, time_interval, strategy_type)
#             VALUES (%s, %s, %s, %s, %s, %s)
#         """, (current_user["id"], strategy["id"], symbol, request.lot, request.interval, "predefined"))
#         conn.commit()
#
#         # Start worker thread with full strategy dict
#         thread = Thread(
#             target=auto_trade_worker,
#             args=(symbol, strategy, request.lot, request.interval, current_user["id"], "predefined")
#         )
#         thread.daemon = True
#         thread.start()
#
#     cursor.close()
#     conn.close()
#
#     return {"message": "Predefined strategy applied"}
#
#
# @router.post("/apply-custom-strategy")
# def apply_custom_strategy(
#         request: StrategyApplyRequest,
#         current_user: dict = Depends(get_current_user)
# ):
#     conn = get_connection()
#     cursor = conn.cursor(dictionary=True)
#
#     cursor.execute("""
#         SELECT * FROM custom_strategy
#         WHERE name = %s AND user_id = %s
#     """, (request.strategy_name, current_user["id"]))
#     strategy = cursor.fetchone()
#
#     if not strategy:
#         raise HTTPException(status_code=404, detail="Custom strategy not found for user")
#
#     for symbol in request.symbols:
#         cursor.execute("""
#             SELECT id FROM applied_strategy
#             WHERE user_id = %s AND strategy_id = %s AND symbol = %s AND is_active = TRUE
#         """, (current_user["id"], strategy["id"], symbol))
#
#         if cursor.fetchone():
#             continue
#
#         cursor.execute("""
#             INSERT INTO applied_strategy (user_id, strategy_id, symbol, lot, time_interval, strategy_type)
#             VALUES (%s, %s, %s, %s, %s, %s)
#         """, (current_user["id"], strategy["id"], symbol, request.lot, request.interval, "custom"))
#         conn.commit()
#
#         # Start worker thread with full strategy dict
#         thread = Thread(
#             target=auto_trade_worker,
#             args=(symbol, strategy, request.lot, request.interval, current_user["id"], "custom")
#         )
#         thread.daemon = True
#         thread.start()
#
#     cursor.close()
#     conn.close()
#
#     return {"message": "Custom strategy applied"}
#
#
# @router.get("/active-strategies")
# def get_active_strategies(current_user: dict = Depends(get_current_user)):
#     conn = get_connection()
#     cursor = conn.cursor(dictionary=True)
#
#     cursor.execute("""
#         SELECT a.symbol, a.lot, a.time_interval, a.strategy_type,
#                CASE
#                    WHEN a.strategy_type = 'predefined' THEN p.name
#                    ELSE c.name
#                END AS strategy_name
#         FROM applied_strategy a
#         LEFT JOIN predefined_strategies p ON a.strategy_type = 'predefined' AND a.strategy_id = p.id
#         LEFT JOIN custom_strategy c ON a.strategy_type = 'custom' AND a.strategy_id = c.id
#         WHERE a.user_id = %s AND a.is_active = TRUE
#     """, (current_user["id"],))
#
#     results = cursor.fetchall()
#     cursor.close()
#     conn.close()
#
#     return {"active_strategies": results}
#
#
# class StrategyUnapplyRequest(BaseModel):
#     strategy_name: str
#     symbol: str
#     strategy_type: str  # "predefined" or "custom"
#
#
# @router.post("/unapply")
# def unapply_strategy(
#     request: StrategyUnapplyRequest,
#     current_user: dict = Depends(get_current_user)
# ):
#     conn = get_connection()
#     cursor = conn.cursor()
#
#     # Get strategy ID from correct table
#     if request.strategy_type == "predefined":
#         cursor.execute("SELECT id FROM predefined_strategies WHERE name = %s", (request.strategy_name,))
#     elif request.strategy_type == "custom":
#         cursor.execute("SELECT id FROM custom_strategy WHERE name = %s AND user_id = %s",
#                        (request.strategy_name, current_user["id"]))
#     else:
#         raise HTTPException(status_code=400, detail="Invalid strategy_type")
#
#     strategy = cursor.fetchone()
#     if not strategy:
#         raise HTTPException(status_code=404, detail="Strategy not found")
#
#     strategy_id = strategy[0]
#
#     # Mark as inactive
#     cursor.execute("""
#         UPDATE applied_strategy
#         SET is_active = FALSE
#         WHERE user_id = %s AND strategy_id = %s AND symbol = %s AND strategy_type = %s
#     """, (current_user["id"], strategy_id, request.symbol, request.strategy_type))
#
#     if cursor.rowcount == 0:
#         raise HTTPException(status_code=404, detail="No active strategy found to unapply")
#
#     conn.commit()
#     cursor.close()
#     conn.close()
#
#     return {"message": f"{request.strategy_type.title()} strategy unapplied successfully for {request.symbol}"}
