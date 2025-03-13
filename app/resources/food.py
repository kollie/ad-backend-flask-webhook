from fastapi import APIRouter, Depends, HTTPException
from typing import List, Dict, Tuple
from app.database import get_db
from app.models import Food, User, Result, DietData
from app.schemas.food import FoodCreate, FoodResponse
from app.schemas.result import ResultCreate, ResultResponse
from app.auth import get_current_user
from sqlalchemy.orm import Session
import joblib
import os
import pandas as pd
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import numpy as np
from pathlib import Path

router = APIRouter()

def train_model(db: Session) -> Tuple[RandomForestClassifier, pd.DataFrame, pd.Series]:
    """Training logic for the diet recommendation model"""
    try:
        # Get all diet data from database using SQLAlchemy session
        diet_records = db.query(DietData).all()
        if not diet_records:
            raise HTTPException(status_code=400, detail="No training data available")

        # Convert to DataFrame
        diet_data = pd.DataFrame([{
            "age": diet.age,
            "gender": diet.gender,
            "height": diet.height,
            "weight": diet.weight,
            "activity_level": diet.activity_level,
            "goal": diet.goal,
            "dietary_preference": diet.dietary_preference
        } for diet in diet_records])

        # Create target variable (for example, using dietary_preference as target)
        y = diet_data['dietary_preference']
        X = diet_data.drop('dietary_preference', axis=1)

        # Convert categorical variables to dummy variables
        X = pd.get_dummies(X)

        # Save feature columns for prediction
        base_dir = Path(__file__).parent.parent
        joblib.dump(X.columns.tolist(), base_dir / "model_features.pkl")

        # Handle small datasets
        if len(diet_data) < 5:  # If we have less than 5 samples
            # Use the same data for training and testing
            X_train = X_test = X
            y_train = y_test = y
        else:
            # Split the data if we have enough samples
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42
            )

        # Train the model
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)

        # Save the model
        joblib.dump(model, base_dir / "diet_model.pkl")

        return model, X_test, y_test

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error training model: {str(e)}")

@router.post("/train_model")
async def train_model_endpoint(
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        # Pass the database session to train_model
        model, X_test, y_test = train_model(db)
        accuracy = accuracy_score(y_test, model.predict(X_test))

        return {
            "message": "Model trained successfully", 
            "accuracy": round(float(accuracy), 4)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/predict_food")
async def predict_food(
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        # Get base directory and model paths
        base_dir = Path(__file__).parent.parent
        model_path = base_dir / "diet_model.pkl"
        features_path = base_dir / "model_features.pkl"

        print(f"[INFO] Loading model from: {model_path}")

        # Load trained model and feature names
        try:
            model = joblib.load(model_path)
            feature_columns = joblib.load(features_path)
        except FileNotFoundError:
            raise HTTPException(
                status_code=400,
                detail="Model not trained yet"
            )

        # Get user's diet data
        user = db.query(User).filter(User.username == current_user).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        user_diet = (
            db.query(DietData)
            .filter(DietData.user_id == user.id)
            .order_by(DietData.id.desc())
            .first()
        )
        
        if not user_diet:
            raise HTTPException(
                status_code=404,
                detail="No saved diet data found for this user"
            )

        # Convert retrieved data into DataFrame
        df_input = pd.DataFrame([{
            "age": user_diet.age,
            "gender": user_diet.gender,
            "height": user_diet.height,
            "weight": user_diet.weight,
            "activity_level": user_diet.activity_level,
            "goal": user_diet.goal,
            "dietary_preference": user_diet.dietary_preference
        }])

        # Convert categorical variables into dummy variables
        df_input = pd.get_dummies(df_input)

        # Ensure input has the same feature columns as training data
        df_input = df_input.reindex(columns=feature_columns, fill_value=0)

        # Make prediction
        prediction = model.predict(df_input)[0]

        return {"predicted_diet": prediction}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/", response_model=FoodResponse)
async def create_food(
    food: FoodCreate,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    db_food = Food(**food.dict())
    db.add(db_food)
    db.commit()
    db.refresh(db_food)
    return db_food

@router.get("/{food_id}", response_model=FoodResponse)
async def get_food(
    food_id: int,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    food = db.query(Food).filter(Food.id == food_id).first()
    if not food:
        raise HTTPException(status_code=404, detail="Food not found")
    return food

