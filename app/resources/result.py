from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List
from app.database import get_db
from app.models import Result, User, DietData
from app.schemas.result import ResultCreate, ResultResponse, UserDietData
from app.schemas.user import DietDataResponse, UserResponse
from app.auth import get_current_user
from sqlalchemy.orm import Session

router = APIRouter()

@router.post("/create", response_model=ResultResponse)
async def create_result(
    result: ResultCreate,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    user = db.query(User).filter(User.username == current_user).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db_result = Result(**result.dict(), user_id=user.id)
    db.add(db_result)
    db.commit()
    db.refresh(db_result)
    return db_result

@router.get("/users_diet_data", response_model=List[ResultResponse])
async def get_all_users_diet_data(
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    results = db.query(Result).all()
    return results

@router.get("/user_diet/{user_id}", response_model=List[ResultResponse])
async def get_user_diet_by_id(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    results = db.query(Result).filter(Result.user_id == user_id).all()
    if not results:
        raise HTTPException(status_code=404, detail="No diet records found for this user")
    return results

@router.get("/user_diet_query", response_model=List[ResultResponse])
async def get_user_diet_by_query(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    results = db.query(Result).filter(Result.user_id == user_id).all()
    if not results:
        raise HTTPException(status_code=404, detail="No diet records found for this user")
    return results

@router.get("/users/diet", response_model=List[UserDietData])
async def get_all_users_with_diet_data(
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Fetch all users
    users = db.query(User).all()
    
    # Create response data
    result = []
    for user in users:
        # Get all diet data for this user
        diet_data = db.query(DietData).filter(DietData.user_id == user.id).all()
        
        # Convert SQLAlchemy models to Pydantic models
        user_response = UserResponse(
            id=user.id,
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name
        )
        
        diet_data_responses = [
            DietDataResponse(
                id=diet.id,
                user_id=diet.user_id,
                age=diet.age,
                gender=diet.gender,
                height=diet.height,
                weight=diet.weight,
                activity_level=diet.activity_level,
                goal=diet.goal,
                dietary_preference=diet.dietary_preference
            ) for diet in diet_data
        ]
        
        result.append(UserDietData(
            user_info=user_response,
            diet_data=diet_data_responses
        ))
    
    return result

@router.get("/users/{user_id}/diet", response_model=List[DietDataResponse])
async def get_user_diet_by_path_id(
    user_id: int,
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Fetch diet data for the specified user
    user_diets = db.query(DietData).filter(DietData.user_id == user_id).all()
    
    if not user_diets:
        raise HTTPException(status_code=404, detail="No diet records found for this user")
    
    return user_diets

@router.get("/diet", response_model=List[DietDataResponse])
async def get_user_diet_by_query(
    user_id: int = Query(..., description="User ID to fetch diet data for"),
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Fetch diet data for the specified user
    user_diets = db.query(DietData).filter(DietData.user_id == user_id).all()
    
    if not user_diets:
        raise HTTPException(status_code=404, detail="No diet records found for this user")
    
    return user_diets
