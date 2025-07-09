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

class BacktestRequest(BaseModel):
    symbol: str
    market: str = "forex"
    investment: float
    strategy_name: Optional[str] = None
    strategy_names: Optional[List[str]] = None
    strategy: Optional[Strategy] = None;
