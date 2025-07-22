from fastapi import APIRouter, HTTPException , Query
from WishList.wishlist_store import add_to_wishlist, remove_from_wishlist , get_wishlist  , search_wishlist_by_name
from typing import Optional


router = APIRouter(prefix="/wishlist", tags=["Wishlist"])

@router.post("/add")
def add(symbol: str):
    if not add_to_wishlist(symbol):
        raise HTTPException(status_code=400, detail="Already exists")
    return {"added": symbol.upper()}

@router.get("/wishlist/search")
def search_wishlist_api(query : Optional[str] = Query("" , min_length = 1 ,
    description="Symbol name to search")):
    return search_wishlist_by_name(query)

@router.get("/list")
def view():
    return  get_wishlist()

@router.post("/remove")
def remove(symbol: str):
    if not remove_from_wishlist(symbol):
        raise HTTPException(status_code=404, detail="Symbol not found in wishlist")
    return {"removed": symbol.upper()}

# from fastapi import APIRouter , HTTPException , Query
# from WishList.wishlist_store import add_to_wishlist, remove_from_wishlist, get_wishlist
#
# router = APIRouter(prefix="/wishlist", tags=["Wishlist"])
#
# @router.post("/wishlist/add")
# def add(symbol: str, market: str):
#     if not add_to_wishlist(symbol, market):
#         raise HTTPException(status_code=400, detail="Already exists / bad market")
#     return {"added": symbol.upper(), "market": market}
#
# @router.post("/wishlist/remove")
# def remove(symbol: str, market: str):
#     if not remove_from_wishlist(symbol, market):
#         raise HTTPException(status_code=404, detail="Not found in wishlist")
#     return {"removed": symbol.upper(), "market": market}
#
# @router.get("/wishlist")
# def view(market: str = Query("all")):
#     return get_wishlist(market)