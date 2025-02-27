import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

MODEL_PATH = "diet_model.pkl"

def train_model():
    # Load dataset
    data = pd.read_csv("data/diet_data.csv")  # Ensure dataset exists

    # Features and target
    X = data[['age', 'gender', 'height', 'weight', 'activity_level', 'goal', 'dietary_preference']]
    y = data['recommended_diet']

    # Convert categorical features
    X = pd.get_dummies(X)

    # Split dataset
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train model
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Save model
    joblib.dump(model, MODEL_PATH)

    return model, X_test, y_test

def load_model():
    try:
        return joblib.load(MODEL_PATH)
    except FileNotFoundError:
        return None
