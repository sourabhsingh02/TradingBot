from fastapi import APIRouter, HTTPException
from Strategies.models import BacktestRequest
from Strategies.strategy_utils import resolve_strategy, evaluate_strategy
from PastDataFetch.data_fetcher import fetch_ohlcv
import pandas as pd

router = APIRouter(prefix="/api/backtest", tags=["Backtesting"])

@router.post("/backtest")
def run_backtest(payload: BacktestRequest):
    candles = fetch_ohlcv(payload.symbol, market=payload.market)
    if not candles or len(candles) < 2:
        raise HTTPException(status_code=404, detail="Not enough data for backtesting")

    strategy = resolve_strategy(payload)
    df = pd.DataFrame(candles)

    positions = []  # to store entry points
    in_position = False
    entry_price = 0

    for i in range(len(df)):
        try:
            slice_df = df.iloc[:i+1]  # till current candle
            match, _ = evaluate_strategy(slice_df, strategy)

            if match and not in_position:
                in_position = True
                entry_price = df.iloc[i]['close']

            elif not match and in_position:
                exit_price = df.iloc[i]['close']
                positions.append((entry_price, exit_price))
                in_position = False
        except:
            continue

    if in_position:
        exit_price = df.iloc[-1]['close']
        positions.append((entry_price, exit_price))

    results = {
        "symbol": payload.symbol,
        "market": payload.market,
        "investment": payload.investment,
        "total_trades": len(positions),
        "profitable_trades": 0,
        "loss_trades": 0,
        "net_profit": 0.0
    }

    for entry, exit in positions:
        units = payload.investment / entry
        profit = (exit - entry) * units
        results["net_profit"] += profit
        if profit > 0:
            results["profitable_trades"] += 1
        else:
            results["loss_trades"] += 1

    if payload.investment > 0:
        results["return_percent"] = round((results["net_profit"] / payload.investment) * 100, 2)
    else:
        results["return_percent"] = 0

    results["net_profit"] = round(results["net_profit"], 2)
    return results