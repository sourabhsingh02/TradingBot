# from datetime import datetime
# from http.client import HTTPException
# import json
# from database.db_connection import get_connection
#
#
# def create_custom_strategy(user_id: int, name: str, conditions: dict):
#     conn = get_connection()
#     if conn is None:
#         return {"error": "DB connection failed"}
#
#     try:
#         cursor = conn.cursor()
#         query = """
#             INSERT INTO custom_strategies (user_id, name, conditions)
#             VALUES (%s, %s, %s)
#         """
#         cursor.execute(query, (user_id, name, str(conditions)))
#         conn.commit()
#         return {"message": "Strategy created successfully", "id": cursor.lastrowid}
#     finally:
#         cursor.close()
#         conn.close()
#
#
# def get_strategies_by_user(user_id: int):
#     conn = get_connection()
#     if conn is None:
#         return {"error": "DB connection failed"}
#
#     try:
#         cursor = conn.cursor(dictionary=True)
#         cursor.execute("SELECT * FROM custom_strategies WHERE user_id = %s", (user_id,))
#         return cursor.fetchall()
#     finally:
#         cursor.close()
#         conn.close()
#
#
# def delete_strategy(strategy_id: int):
#     conn = get_connection()
#     if conn is None:
#         return {"error": "DB connection failed"}
#
#     try:
#         cursor = conn.cursor()
#         cursor.execute("DELETE FROM custom_strategies WHERE id = %s", (strategy_id,))
#         conn.commit()
#         return {"message": "Deleted successfully"} if cursor.rowcount > 0 else {"message": "Not found"}
#     finally:
#         cursor.close()
#         conn.close()
#
#
# def search_strategies_by_name(user_id: int, query: str):
#     conn = get_connection()
#     if conn is None:
#         return {"error": "DB connection failed"}
#
#     try:
#         cursor = conn.cursor(dictionary=True)
#         cursor.execute("""
#             SELECT name FROM custom_strategies
#             WHERE user_id = %s AND name LIKE %s
#         """, (user_id, f"{query}%"))
#         return cursor.fetchall()
#     finally:
#         cursor.close()
#         conn.close()
#
#
# def get_full_strategy_by_name(user_id: int, name: str):
#     conn = get_connection()
#     if conn is None:
#         return {"error": "DB connection failed"}
#
#     try:
#         cursor = conn.cursor(dictionary=True)
#         cursor.execute("""
#             SELECT name, conditions FROM custom_strategies
#             WHERE user_id = %s AND name = %s
#         """, (user_id, name))
#         strategy = cursor.fetchone()
#         if strategy:
#             return strategy
#         raise HTTPException(status_code=404, detail="Strategy not found")
#     finally:
#         cursor.close()
#         conn.close()
#
#
#
# def update_custom_strategy(strategy_id: int, name: str, conditions: list[dict]):
#     conn = get_connection()
#     if conn is None:
#         return {"error": "DB connection failed"}
#
#     try:
#         cursor = conn.cursor()
#         cursor.execute("""
#             UPDATE custom_strategy
#             SET name = %s, conditions = %s
#             WHERE id = %s
#         """, (name, json.dumps(conditions), strategy_id))
#         conn.commit()
#         if cursor.rowcount == 0:
#             return {"message": "Strategy not found"}
#         return {"message": "Strategy updated successfully"}
#     finally:
#         cursor.close()
#         conn.close()