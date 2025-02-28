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
        model = load_model()
        if not model:
            return {"message": "Model not trained yet"}, 400

        # Get user input
        input_data = request.get_json()
        df_input = pd.DataFrame([input_data])

        # Convert categorical data
        df_input = pd.get_dummies(df_input)

        # Ensure input has same columns as training data
        base_dir = os.path.abspath(os.path.dirname(__file__))  # Gets `/home/kollie/flask-project/ad-backend-flask-webhook/app/`

        # ✅ Construct the correct file path
        model_path = os.path.join(base_dir, "diet_model.pkl")

        print(f"[INFO] Loading model from: {model_path}")

        model_features = joblib.load(model_path)  # Save feature columns separately
        df_input = df_input.reindex(columns=model_features, fill_value=0)

        prediction = model.predict(df_input)[0]
        return {"predicted_diet": prediction}, 200
