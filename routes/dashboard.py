from fastapi import APIRouter, Query
from LiveDataFetch.nseData import get_nse_paginated
from LiveDataFetch.forexData import get_forex_paginated

router = APIRouter()

@router.get("/dashboard")
def get_combined_dashboard(
    nse_page: int = 1,
    forex_page: int = 1,
    size: int = 10,
    nse_filter: str = Query("all", enum=["all", "gainers", "losers", "volatile"]),
    forex_filter: str = Query("all", enum=["all", "gainers", "losers", "volatile"])
):

    nse_data = get_nse_paginated(page=nse_page, size=size, market="nse", filter_type=nse_filter)
    forex_data = get_forex_paginated(page=forex_page, size=size, market="forex", filter_type=forex_filter)

    return {
        "nse": nse_data,
        "forex": forex_data
    }