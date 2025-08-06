from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from typing import Optional
from database.db_connection import get_connection
from passlib.context import CryptContext
from datetime import datetime
from Admin.admin_routes.admin import  AdminAuth , verify_admin

router = APIRouter(prefix="/admin-user", tags=["Admin || User"])
class UserFilter(AdminAuth):
    name: Optional[str] = None
    email: Optional[str] = None
    mobile: Optional[str] = None

class DeleteUserRequest(UserFilter):
    pass





@router.post("/users")
def get_all_users(credentials: AdminAuth):
    if not verify_admin(credentials.identifier, credentials.password):
        raise HTTPException(status_code=401, detail="Unauthorized admin")

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, name, email, mobile, is_active, created_at FROM users")
    users = cursor.fetchall()
    cursor.close()
    conn.close()
    return {"users": users}

@router.post("/users/search")
def get_user_by_fields(filter: UserFilter):
    if not verify_admin(filter.identifier, filter.password):
        raise HTTPException(status_code=401, detail="Unauthorized admin")

    conditions = []
    values = []
    if filter.name:
        conditions.append("name = %s")
        values.append(filter.name)
    if filter.email:
        conditions.append("email = %s")
        values.append(filter.email)
    if filter.mobile:
        conditions.append("mobile = %s")
        values.append(filter.mobile)

    if not conditions:
        raise HTTPException(status_code=400, detail="No filter provided")

    query = f"SELECT id, name, email, mobile, is_active, created_at FROM users WHERE {' OR '.join(conditions)}"

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query, tuple(values))
    users = cursor.fetchall()
    cursor.close()
    conn.close()

    return {"users": users}


@router.delete("/users/delete")
def delete_user(filter: DeleteUserRequest):
    if not verify_admin(filter.identifier, filter.password):
        raise HTTPException(status_code=401, detail="Unauthorized admin")

    conditions = []
    values = []
    if filter.name:
        conditions.append("name = %s")
        values.append(filter.name)
    if filter.email:
        conditions.append("email = %s")
        values.append(filter.email)
    if filter.mobile:
        conditions.append("mobile = %s")
        values.append(filter.mobile)

    if not conditions:
        raise HTTPException(status_code=400, detail="No identifier provided to delete")

    query = f"DELETE FROM users WHERE {' OR '.join(conditions)}"

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query, tuple(values))
    conn.commit()
    affected = cursor.rowcount
    cursor.close()
    conn.close()

    if affected == 0:
        raise HTTPException(status_code=404, detail="No matching user found")

    return {"message": f"{affected} user(s) deleted"}