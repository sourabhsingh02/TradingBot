from pydantic import BaseModel
from typing import List, Dict, Any

# class CustomStrategyBase(BaseModel):
#     name: str
#     conditions: List[Dict[str, Any]]  # or just Any if flexible
#
# class CustomStrategyCreate(CustomStrategyBase):
#     user_id: int
#
# class CustomStrategyUpdate(BaseModel):
#     name: str | None = None
#     conditions: List[Dict[str, Any]] | None = None
#
# class CustomStrategyOut(CustomStrategyBase):
#     id: int
#     user_id: int
#     created_at: str

class Condition(BaseModel) :
    indicator : str
    operator : str
    value :str
    action: str

class StrategyCreate(BaseModel) :
    name : str
    conditions : List[Condition]
class UpdateStrategyRequest(BaseModel):
    name: str
    conditions: List[Condition]