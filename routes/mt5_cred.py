from fastapi import APIRouter
from pydantic import BaseModel
from MetaTrader5 import initialize, shutdown, last_error
from App.api_config import set_user_credentials

router = APIRouter(prefix="/mt5creds", tags=["MT5creds"])

class MT5LoginRequest(BaseModel):
    login: int
    password: str
    server: str

@router.post("/mt5/login")
def login_mt5(request: MT5LoginRequest):
    # Set dynamic credentials
    set_user_credentials(request.login, request.password, request.server)

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
    return {"status": "success", "message": "MT5 login verified and credentials stored."}

