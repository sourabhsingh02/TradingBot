from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from MetaTrader5 import initialize, shutdown, last_error
from database.db_connection import get_connection
from Security.auth import get_current_user
from Security.encryption_mt5 import encrypt_password

router = APIRouter(prefix="/mt5creds", tags=["MT5creds"])


class MT5LoginRequest(BaseModel):
    login: int
    password: str
    server: str


@router.post("/login")
def login_mt5(
    request: MT5LoginRequest,
    current_user: dict = Depends(get_current_user)
):
    # Step 1: Encrypt password inside function
    encrypted_pw = encrypt_password(request.password)

    # Step 2: Try to initialize MT5 with plain password to check if it’s valid
    initialized = initialize(
        login=request.login,
        password=request.password,
        server=request.server
    )

    if not initialized:
        return {
            "status": "error",
            "message": f"MT5 initialization failed: {last_error()}"
        }

    shutdown()


    conn = get_connection()
    if conn is None:
        raise HTTPException(status_code=500, detail="Database connection failed")

    cursor = conn.cursor()

    cursor.execute("SELECT id FROM mt5_credentials WHERE user_id = %s", (current_user["id"],))
    existing = cursor.fetchone()
    if existing:
        raise HTTPException(status_code=400, detail="MT5 credentials already linked for this user")

    insert_query = """
        INSERT INTO mt5_credentials (user_id, login, server, encrypted_password)
        VALUES (%s, %s, %s, %s)
    """
    cursor.execute(insert_query, (
        current_user["id"],
        request.login,
        request.server,
        encrypted_pw
    ))

    conn.commit()
    cursor.close()
    conn.close()

    return {"status": "success", "message": "MT5 credentials verified and saved."}