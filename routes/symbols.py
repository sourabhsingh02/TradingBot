from fastapi import APIRouter, Query, HTTPException
from SymbolsPairs.symbols_utils import search_symbol
from SymbolsPairs.nseSymbols import fetch_all_nse_symbols
from SymbolsPairs.forexSymbols import fetch_all_forex_symbols ,get_logo_url
from fastapi import APIRouter, Query
from data.completeData import  get_price_change_today_vs_yesterday


router = APIRouter(prefix="/symbols", tags=["Symbols"])

# @router.get("/nse")
# def get_nse_symbols():
#     return {"market": "nse", "symbols": fetch_all_nse_symbols()}

@router.get("/forex")
def get_forex_symbols():
    return {"market": "forex", "symbols": fetch_all_forex_symbols()}

@router.get("/search")
def search(query :str = Query(... , min_length=1)):
    result =  search_symbol(query)
    return {"result" : result}



