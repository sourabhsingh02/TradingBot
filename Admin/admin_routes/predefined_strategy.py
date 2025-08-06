from fastapi import APIRouter, Query, HTTPException , Depends , Body
from database.db_connection import get_connection
import json
from database.schemas.custom_schemas import *
from Admin.admin_routes.admin import  AdminAuth , verify_admin

router = APIRouter(prefix="/admin-built-in", tags=["Admin || Built In Strategy"])




@router.post("/admin/predefined-strategy/create")
def create_predefined_strategy(
    data: StrategyCreate,
    identifier: str = Body(...),
    password: str = Body(...)
):
    admin_id = verify_admin(identifier, password)

    conn = get_connection()
    cursor = conn.cursor()

    # Check duplicate
    cursor.execute(
        "SELECT id FROM predefined_strategies WHERE name = %s",
        (data.name,)
    )
    if cursor.fetchone():
        raise HTTPException(status_code=400, detail="Strategy with this name already exists")

    conditions_json = json.dumps([c.model_dump() for c in data.conditions])

    # Insert strategy with admin_id
    cursor.execute(
        "INSERT INTO predefined_strategies (admin_id, name, conditions) VALUES (%s, %s, %s)",
        (admin_id, data.name, conditions_json)
    )

    conn.commit()
    cursor.close()
    conn.close()

    return {"message": "Predefined strategy created successfully"}

@router.put("/update/{strategy_id}")
def update_predefined_strategy(strategy_id: int, data: StrategyCreate, identifier: str, password: str):
    admin = verify_admin(identifier, password)
    if not admin:
        raise HTTPException(status_code=401, detail="Invalid admin credentials")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id FROM predefined_strategies WHERE id = %s AND admin_id = %s",
        (strategy_id, admin["id"])
    )
    if not cursor.fetchone():
        raise HTTPException(status_code=404, detail="Strategy not found")

    conditions_json = json.dumps([c.model_dump() for c in data.conditions])
    cursor.execute(
        "UPDATE predefined_strategies SET name = %s, conditions = %s WHERE id = %s",
        (data.name, conditions_json, strategy_id)
    )

    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "Predefined strategy updated successfully"}

@router.delete("/delete/{strategy_id}")
def delete_predefined_strategy(strategy_id: int, identifier: str, password: str):
    admin = verify_admin(identifier, password)
    if not admin:
        raise HTTPException(status_code=401, detail="Invalid admin credentials")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id FROM predefined_strategies WHERE id = %s AND admin_id = %s",
        (strategy_id, admin["id"])
    )
    if not cursor.fetchone():
        raise HTTPException(status_code=404, detail="Strategy not found")

    cursor.execute("DELETE FROM predefined_strategies WHERE id = %s", (strategy_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "Predefined strategy deleted successfully"}

@router.get("/all")
def get_all_predefined_strategies():
    conn = get_connection()
    if conn is None:
        return {"error": "DB connection failed"}

    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT  name FROM predefined_strategies")  # only id and name
        rows = cursor.fetchall()
        return {"strategies": rows}
    finally:
        cursor.close()
        conn.close()


@router.get("/search")
def search_predefined_strategies(query: str = Query(..., min_length=1)):
    conn = get_connection()
    if conn is None:
        return {"error": "DB connection failed"}

    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT name FROM predefined_strategies
            WHERE LOWER(name) LIKE %s
        """, (f"%{query.lower()}%",))

        rows = cursor.fetchall()
        return {"results": [row["name"] for row in rows]}
    finally:
        cursor.close()
        conn.close()



@router.get("/get")
def get_strategy_by_name_or_id(name: str = None, id: int = None):
    if not name and not id:
        raise HTTPException(status_code=400, detail="Either name or id must be provided")

    conn = get_connection()
    if conn is None:
        return {"error": "DB connection failed"}

    try:
        cursor = conn.cursor(dictionary=True)

        if id:
            cursor.execute("SELECT * FROM predefined_strategies WHERE id = %s", (id,))
        else:
            cursor.execute("SELECT * FROM predefined_strategies WHERE name = %s", (name,))

        strategy = cursor.fetchone()

        if not strategy:
            raise HTTPException(status_code=404, detail="Strategy not found")

        if isinstance(strategy["conditions"], str):
            strategy["conditions"] = json.loads(strategy["conditions"])

        return {"strategy": strategy}
    finally:
        cursor.close()
        conn.close()