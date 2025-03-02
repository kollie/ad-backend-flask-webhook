import os
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

MODEL_PATH = "diet_model.pkl"
FEATURES_PATH = "model_features.pkl"  # ✅ Save feature names

def train_model():
    """Train the model using diet data from an absolute path."""
    base_dir = os.path.abspath(os.path.dirname(__file__))  # ✅ Correct base path
    data_path = os.path.join(base_dir, "data/Diet_Data.csv")  # ✅ Looks inside `app/data/`
    
    print(f"[INFO] Loading dataset from: {data_path}")  # Debugging
    
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"[ERROR] Data file not found at {data_path}")

    data = pd.read_csv(data_path)

    # ✅ Convert categorical features into dummy variables
    X = data[['age', 'gender', 'height', 'weight', 'activity_level', 'goal', 'dietary_preference']]
    y = data['recommended_diet']
    X = pd.get_dummies(X)  # Converts categorical features into multiple columns

    # ✅ Save the feature names for prediction
    joblib.dump(X.columns, os.path.join(base_dir, FEATURES_PATH))

    # Split dataset
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train model
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Save model
    joblib.dump(model, os.path.join(base_dir, MODEL_PATH))

    return model, X_test, y_test


def load_model():
    # Ensure input has same columns as training data
    base_dir = os.path.abspath(os.path.dirname(__file__))  # Gets `/home/kollie/flask-project/ad-backend-flask-webhook/app/`

        # ✅ Construct the correct file path
    model_path_ = os.path.join(base_dir, "diet_model.pkl")

    print(f"[INFO] Loading model from: {model_path_}")
    try:
        return joblib.load(model_path_)
    except FileNotFoundError:
        return None
    
