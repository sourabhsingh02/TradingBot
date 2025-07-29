from fastapi import APIRouter, Depends
from Security.auth import get_current_user
from WishList.wishlist_store import (
    get_wishlist, search_wishlist_item, add_to_wishlist, remove_from_wishlist, clear_wishlist
)

router = APIRouter(prefix="/wishlist", tags=["Wishlist"])
from fastapi import APIRouter, Depends
from Security.auth import get_current_user
from WishList.wishlist_store import (
    get_wishlist, search_wishlist_item, add_to_wishlist, remove_from_wishlist, clear_wishlist
)
from database.schemas.wishlist_schema import WishlistRequest

router = APIRouter(prefix="/wishlist", tags=["Wishlist"])


@router.get("/list", summary="Get full wishlist")
def get_user_wishlist(user=Depends(get_current_user)):
    return get_wishlist(user["id"])

@router.get("/search", summary="Search wishlist")
def search_wishlist(keyword: str, user=Depends(get_current_user)):
    return search_wishlist_item(user["id"], keyword)


@router.post("/add", summary="Add symbol to wishlist")
def add(request: WishlistRequest, user=Depends(get_current_user)):
    return add_to_wishlist(request.symbol, user["id"])


@router.delete("/remove", summary="Remove symbol from wishlist")
def remove(request: WishlistRequest, user=Depends(get_current_user)):
    return remove_from_wishlist(request.symbol, user["id"])


@router.delete("/clear", summary="Clear entire wishlist")
def clear(user=Depends(get_current_user)):
    return clear_wishlist(user["id"])

# from fastapi import APIRouter, HTTPException , Query
# from WishList.wishlist_store import add_to_wishlist, remove_from_wishlist , get_wishlist  , search_wishlist_by_name
# from typing import Optional
#
#
# router = APIRouter(prefix="/wishlist", tags=["Wishlist"])
#
# @router.post("/add")
# def add(symbol: str):
#     if not add_to_wishlist(symbol):
#         raise HTTPException(status_code=400, detail="Already exists")
#     return {"added": symbol.upper()}
#
# @router.get("/wishlist/search")
# def search_wishlist_api(query : Optional[str] = Query("" , min_length = 1 ,
#     description="Symbol name to search")):
#     return search_wishlist_by_name(query)
#
# @router.get("/list")
# def view():
#     return  get_wishlist()
#
# @router.post("/remove")
# def remove(symbol: str):
#     if not remove_from_wishlist(symbol):
#         raise HTTPException(status_code=404, detail="Symbol not found in wishlist")
#     return {"removed": symbol.upper()}
#
