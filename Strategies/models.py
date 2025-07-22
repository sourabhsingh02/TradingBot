from pydantic import BaseModel
from typing import List, Optional , Union


class Condition(BaseModel):
    indicator: str
    operator: str
    value: str


class Strategy(BaseModel):
    name: str
    conditions: List[Condition]
    action: str


class CustomSignalRequest(BaseModel):
    symbol: str
    market :str = "forex"
    strategy_name: Optional[str] = None
    strategy_names: Optional[List[str]] = None
    strategy:Optional[Strategy] = None ;
    strategies: Optional[List[str]] = None;

class PredefinedSignalRequest(BaseModel):
    symbol: str
    market:str = "forex"
    strategy_name: Optional[str] = None
    strategy_names: Optional[list[str]] = None


class StrategyCondition(BaseModel):
    indicator: str
    operator: str
    value: str

class StrategyPayload(BaseModel):
    id: Optional[str] = None
    name: str
    action: str  # 'buy', 'sell', or 'alert'
    conditions: List[StrategyCondition]

class StrategyRequest(BaseModel):
    symbol: str
    market: str = "forex"  # or "nse"
    interval: str  # seconds
    auto_trade: Optional[bool] = True
    strategy: Optional[StrategyPayload] = None
    strategy_name: Optional[str] = None

class ManualOrderRequest(BaseModel):
    symbol: str
    action: str  # 'buy' or 'sell'
    investment : float


CUSTOM_STRATEGIES = []

class BacktestRequest(BaseModel):
    symbol: str
    market: str = "forex"
    investment: float
    strategy_name: Optional[str] = None
    strategy_names: Optional[List[str]] = None
    strategy: Optional[Strategy] = None
    interval : str = "1d"
    days : int = 365

