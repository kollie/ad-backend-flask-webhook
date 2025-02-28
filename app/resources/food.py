import os
from flask_restful import Resource
from flask import request
from flask_jwt_extended import jwt_required
import pandas as pd
import joblib
from app.train import train_model, load_model
from sklearn.metrics import accuracy_score

class TrainModelResource(Resource):
    @jwt_required()
    def post(self):
        model, X_test, y_test = train_model()
        accuracy = accuracy_score(y_test, model.predict(X_test))

        return {"message": "Model trained successfully", "accuracy": round(accuracy, 4)}, 200

class PredictFoodResource(Resource):
    @jwt_required()
    def post(self):
        """Predict diet recommendation based on user input."""
        base_dir = os.path.abspath(os.path.dirname(__file__))  # ✅ Correct base path
        model_path = os.path.join(base_dir, "../diet_model.pkl")  # ✅ Ensure correct model path
        features_path = os.path.join(base_dir, "../model_features.pkl")  # ✅ Ensure correct feature path

        print(f"[INFO] Loading model from: {model_path}")

        # ✅ Load model
        try:
            model = joblib.load(model_path) 
            feature_columns = joblib.load(features_path)  # ✅ Load saved feature names
        except FileNotFoundError:
            return {"message": "Model not trained yet"}, 400

        # ✅ Get user input
        input_data = request.get_json()
        df_input = pd.DataFrame([input_data])

        # ✅ Convert categorical variables into dummy variables
        df_input = pd.get_dummies(df_input)

        # ✅ Ensure input has the same feature columns as training data
        df_input = df_input.reindex(columns=feature_columns, fill_value=0)  # ✅ Fills missing columns with 0

        # ✅ Make prediction
        prediction = model.predict(df_input)[0]
        return {"predicted_diet": prediction}, 200
