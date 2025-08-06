from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from typing import Optional
from database.db_connection import get_connection
from passlib.context import CryptContext
from datetime import datetime

router = APIRouter(prefix="/admin", tags=["Admin"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
class AdminAuth(BaseModel):
    identifier: str  # email or mobile
    password: str

class AdminCreateRequest(BaseModel):
    name: str
    email: EmailStr
    mobile: str
    password: str
    is_super_admin: bool = False

def verify_admin(identifier: str, password: str):
    conn = get_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="DB Connection failed")
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM admins WHERE email = %s OR mobile = %s", (identifier, identifier))
    admin = cursor.fetchone()
    cursor.close()
    conn.close()

    if not admin:
        return False

    return pwd_context.verify(password, admin["password_hash"])



@router.post("/create")
def create_admin(admin: AdminCreateRequest):
    conn = get_connection()
    cursor = conn.cursor()

    # Hash password
    hashed_password = pwd_context.hash(admin.password)

    # Check if exists
    cursor.execute("SELECT id FROM admins WHERE email = %s OR mobile = %s", (admin.email, admin.mobile))
    if cursor.fetchone():
        raise HTTPException(status_code=400, detail="Email or mobile already exists.")

    cursor.execute("""
        INSERT INTO admins (name, email, mobile, password_hash, is_super_admin, created_at)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (
        admin.name,
        admin.email,
        admin.mobile,
        hashed_password,
        int(admin.is_super_admin),
        datetime.now()
    ))
    conn.commit()
    cursor.close()
    conn.close()

    return {"message": "Admin created successfully"}


@router.post("/login")
def admin_login(credentials: AdminAuth):
    if verify_admin(credentials.identifier, credentials.password):
        return {"message": "Admin login successful"}
    raise HTTPException(status_code=401, detail="Invalid credentials")

@router.post("/all")
def get_all_admins(credentials: AdminAuth):
    if not verify_admin(credentials.identifier, credentials.password):
        raise HTTPException(status_code=401, detail="Unauthorized admin")

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT id, name, email, mobile, password_hash AS password, is_super_admin, created_at
        FROM admins
    """)
    admins = cursor.fetchall()
    cursor.close()
    conn.close()

    return {"admins": admins}