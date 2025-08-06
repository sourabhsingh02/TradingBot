from fastapi import APIRouter, Query, HTTPException
from database.db_connection import get_connection
import json

router = APIRouter(prefix="/admin-custom", tags=["Admin || Custom"])

@router.get("/all")
def get_all_predefined_strategies():
    conn = get_connection()
    if conn is None:
        return {"error": "DB connection failed"}

    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT  name FROM custom_strategy")  # only id and name
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
            SELECT name FROM custom_strategy
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
            cursor.execute("SELECT * FROM custom_strategy WHERE id = %s", (id,))
        else:
            cursor.execute("SELECT * FROM custom_strategy WHERE name = %s", (name,))

        strategy = cursor.fetchone()

        if not strategy:
            raise HTTPException(status_code=404, detail="Strategy not found")

        if isinstance(strategy["conditions"], str):
            strategy["conditions"] = json.loads(strategy["conditions"])

        return {"strategy": strategy}
    finally:
        cursor.close()
        conn.close()

