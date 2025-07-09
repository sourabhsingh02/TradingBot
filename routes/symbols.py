from fastapi import APIRouter, Query, HTTPException
from SymbolsPairs.symbols_utils import (
    search_symbols
)
from SymbolsPairs.nseSymbols import fetch_all_nse_symbols
from SymbolsPairs.forexSymbols import fetch_all_forex_symbols

router = APIRouter(prefix="/symbols", tags=["Symbols & Pairs"])

@router.get("/nse")
def get_nse_symbols():
    return {"market": "nse", "symbols": fetch_all_nse_symbols()}

@router.get("/forex")
def get_forex_symbols():
    return {"market": "forex", "symbols": fetch_all_forex_symbols()}

@router.get("/search")
def search(q: str = Query(...), market: str = Query("all")):
    res = search_symbols(q, market)
    if not res:
        raise HTTPException(status_code=404, detail="No match")
    return res


# @router.post("/wishlist/add")
# def add(symbol: str, market: str):
#     if not add_to_wishlist(symbol, market):
#         raise HTTPException(status_code=400, detail="Already exists / bad market")
#     return {"added": symbol.upper(), "market": market}
#
#
# @router.post("/wishlist/remove")
# def remove(symbol: str, market: str):
#     if not remove_from_wishlist(symbol, market):
#         raise HTTPException(status_code=404, detail="Not found in wishlist")
#     return {"removed": symbol.upper(), "market": market}
#
#
# @router.get("/wishlist")
# def view(market: str = Query("all")):
#     return get_wishlist(market)