from pydantic import BaseModel
from typing import List, Optional


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
    strategy: Optional[Strategy] = None
    strategy_name: Optional[str] = None


class PredefinedSignalRequest(BaseModel):
    symbol: str
    strategy_name: str
