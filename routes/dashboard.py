from fastapi import APIRouter, Query
from data.dashboard_util import (get_top_gainers, get_top_losers,
                                 get_most_volatile ,get_top_movers ,
                                 )

from fastapi.responses import JSONResponse

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@router.get("/top-gainers")
def top_gainers(page : int = Query(1,gt = 0),limit :int = Query(10,gt=0)):
    return {"top_gainers": get_top_gainers(page , limit)}

@router.get("/top-losers")
def top_losers(page : int = Query(1,gt = 0),limit :int = Query(10,gt=0)):
    return {"top_losers": get_top_losers(page , limit)}

@router.get("/top-volatile")
def top_volatile(page : int = Query(1,gt = 0),limit :int = Query(10,gt=0)):
    return {"top_volatile": get_most_volatile(page , limit)}

@router.get("/top-movers")
def top_moviers(page : int = Query(1,gt = 0),limit :int = Query(10,gt=0)):
    return {"top_movers":get_top_movers(page , limit)}



