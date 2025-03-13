from pydantic import BaseModel
from typing import Optional, List
from app.schemas.user import UserResponse, DietDataResponse

class ResultBase(BaseModel):
    diet_recommendation: str
    calories: float
    protein: float
    carbs: float
    fats: float

class ResultCreate(ResultBase):
    pass

class ResultResponse(ResultBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True

class UserDietData(BaseModel):
    user_info: UserResponse
    diet_data: List[DietDataResponse]

    class Config:
        orm_mode = True 