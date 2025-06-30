from fastapi import APIRouter, HTTPException
from symbols_utils import add_to_wishlist, remove_from_wishlist, read_wishlist

router = APIRouter(prefix="/api/wishlist", tags=["Wishlist"])

@router.get("/all_wishlist")
def get_wishlist():
    return {"wishlist": read_wishlist()}

@router.post("/add/{symbol}")
def add_symbol(symbol: str):
    symbol = symbol.upper()
    wishlist = add_to_wishlist(symbol)
    return {"message": f"{symbol} added to wishlist", "wishlist": wishlist}

@router.delete("/remove/{symbol}")
def remove_symbol(symbol: str):
    symbol = symbol.upper()
    wishlist = remove_from_wishlist(symbol)
    return {"message": f"{symbol} removed from wishlist", "wishlist": wishlist}
