from pydantic import BaseModel
from typing import Optional

class FoodBase(BaseModel):
    name: str
    calories: float
    protein: float
    carbs: float
    fats: float

class FoodCreate(FoodBase):
    pass

class FoodResponse(FoodBase):
    id: int

    class Config:
        orm_mode = True 