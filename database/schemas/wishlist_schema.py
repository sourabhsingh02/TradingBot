from pydantic import BaseModel
from datetime import datetime

class WishlistRequest(BaseModel):
    symbol: str

class WishlistOut(BaseModel):
    id: int
    user_id: int
    symbol: str
    added_at: datetime

    class Config:
        orm_mode = True