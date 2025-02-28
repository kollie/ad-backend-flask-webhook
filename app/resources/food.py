import os
from flask_restful import Resource
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
import pandas as pd
import joblib
from app.train import train_model, load_model
from sklearn.metrics import accuracy_score
from app.models import DietData

class TrainModelResource(Resource):
    @jwt_required()
    def post(self):
        model, X_test, y_test = train_model()
        accuracy = accuracy_score(y_test, model.predict(X_test))

        return {"message": "Model trained successfully", "accuracy": round(accuracy, 4)}, 200

class PredictFoodResource(Resource):
    @jwt_required()
    def post(self):
        """Predict diet recommendation using saved user data."""
        base_dir = os.path.abspath(os.path.dirname(__file__))  # ✅ Correct base path
        model_path = os.path.join(base_dir, "../diet_model.pkl")  # ✅ Model path
        features_path = os.path.join(base_dir, "../model_features.pkl")  # ✅ Feature names path

        print(f"[INFO] Loading model from: {model_path}")

        # ✅ Load trained model and feature names
        try:
            model = joblib.load(model_path)
            feature_columns = joblib.load(features_path)
        except FileNotFoundError:
            return {"message": "Model not trained yet"}, 400

        # ✅ Get logged-in user ID
        user_id = get_jwt_identity()

        # ✅ Retrieve the latest diet data for the user
        user_diet = DietData.query.filter_by(user_id=user_id).order_by(DietData.id.desc()).first()
        if not user_diet:
            return {"message": "No saved diet data found for this user"}, 404

        # ✅ Convert retrieved data into DataFrame
        df_input = pd.DataFrame([{
            "age": user_diet.age,
            "gender": user_diet.gender,
            "height": user_diet.height,
            "weight": user_diet.weight,
            "activity_level": user_diet.activity_level,
            "goal": user_diet.goal,
            "dietary_preference": user_diet.dietary_preference
        }])

        # ✅ Convert categorical variables into dummy variables
        df_input = pd.get_dummies(df_input)

        # ✅ Ensure input has the same feature columns as training data
        df_input = df_input.reindex(columns=feature_columns, fill_value=0)

        # ✅ Make prediction
        prediction = model.predict(df_input)[0]

        return {"predicted_diet": prediction}, 200

