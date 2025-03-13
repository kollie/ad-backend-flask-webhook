from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.database import get_db
from app.models import User, DietData
from app.schemas.user import UserCreate, UserResponse, DietDataCreate, DietDataResponse, UserLogin, TokenResponse
from app.auth import create_access_token, get_current_user
from sqlalchemy.orm import Session

router = APIRouter()

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name
    )
    db_user.set_password(user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.post("/login", response_model=TokenResponse)
async def login(user_data: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == user_data.username).first()
    if not user or not user.check_password(user_data.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(data={"sub": user.username})
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": user.id,
        "username": user.username,
        "first_name": user.first_name,
        "last_name": user.last_name
    }

@router.post("/diet", response_model=DietDataResponse)
async def create_diet_data(
    diet_data: DietDataCreate,
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.username == current_user).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db_diet = DietData(**diet_data.dict(), user_id=user.id)
    db.add(db_diet)
    db.commit()
    db.refresh(db_diet)
    return db_diet


