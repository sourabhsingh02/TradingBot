from fastapi import APIRouter, Depends, HTTPException ,Path
from typing import List
import json

from database.db_connection import get_connection
from Security.auth import get_current_user
from database.schemas.custom_schemas import StrategyCreate , UpdateStrategyRequest , Condition

router = APIRouter(prefix="/custom-strategy", tags=["Custom Strategies"])


@router.post("/create")
def create_custom_strategy(data: StrategyCreate, current_user: dict = Depends(get_current_user)):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id FROM custom_strategy WHERE user_id = %s AND name = %s",
        (current_user["id"], data.name)
    )
    if cursor.fetchone():
        raise HTTPException(status_code=400, detail="Strategy already exists")

    conditions_json = json.dumps([c.model_dump() for c in data.conditions])

    cursor.execute(
        "INSERT INTO custom_strategy (user_id, name, conditions) VALUES (%s, %s, %s)",
        (current_user["id"], data.name, conditions_json)
    )
    conn.commit()
    cursor.close()
    conn.close()

    return {"message": "Strategy created successfully"}


@router.get("/get-all", response_model=List[str])
def get_all_strategy_names(current_user: dict = Depends(get_current_user)):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM custom_strategy WHERE user_id = %s", (current_user["id"],))
    names = [row[0] for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return names


@router.get("/search", response_model=List[str])
def search_strategy(q: str, current_user: dict = Depends(get_current_user)):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT name FROM custom_strategy WHERE user_id = %s AND name LIKE %s",
        (current_user["id"], f"%{q}%")
    )
    results = [row[0] for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return results


@router.get("/full/{name}")
def get_full_strategy(name: str , current_user: dict = Depends(get_current_user)):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, name, conditions FROM custom_strategy WHERE user_id = %s AND name = %s",
        (current_user["id"], name)
    )
    row = cursor.fetchone()
    cursor.close()
    conn.close()

    if not row:
        raise HTTPException(status_code=404, detail="Strategy not found")
    try:
        conditions = json.loads(row[2])
    except Exception:
        raise HTTPException(status_code=500, detail="Invalid JSON in strategy conditions")

    return {
        "id": row[0],
        "name": row[1],
        "conditions": conditions
    }


@router.put("/update/{strategy_id}")
def update_custom_strategy(
    strategy_id: int,
    data: UpdateStrategyRequest,
    current_user: dict = Depends(get_current_user)
):
    conn = get_connection()
    if conn is None:
        raise HTTPException(status_code=500, detail="Database connection failed")

    try:
        cursor = conn.cursor()


        cursor.execute("SELECT id FROM custom_strategy WHERE id = %s AND user_id = %s", (strategy_id, current_user["id"]))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Strategy not found or not owned by user")


        serialized_conditions = json.dumps([condition.model_dump() for condition in data.conditions])

        # Perform update
        cursor.execute("""
            UPDATE custom_strategy
            SET name = %s, conditions = %s
            WHERE id = %s
        """, (data.name, serialized_conditions, strategy_id))

        conn.commit()
        return {"message": "Strategy updated successfully"}

    finally:
        cursor.close()
        conn.close()
        conn.close()


@router.delete("/delete/{name}")
def delete_strategy(name: str, current_user: dict = Depends(get_current_user)):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM custom_strategy WHERE user_id = %s AND name = %s", (current_user["id"], name))
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Strategy not found")
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "Strategy deleted successfully"}

