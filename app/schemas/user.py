from pydantic import BaseModel
from typing import Optional

class UserBase(BaseModel):
    username: str
    first_name: str
    last_name: str


class UserLogin(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user_id: int
    username: str
    first_name: str
    last_name: str

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    
    class Config:
        orm_mode = True

class DietDataBase(BaseModel):
    age: int
    gender: str
    height: float
    weight: float
    activity_level: str
    goal: str
    dietary_preference: str

class DietDataCreate(DietDataBase):
    pass

class DietDataResponse(DietDataBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True
