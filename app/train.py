import os
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

MODEL_PATH = "diet_model.pkl"

def train_model():
    """Train the model using diet data from an absolute path."""
    # Construct the absolute path
    base_dir = os.path.dirname(os.path.abspath(__file__))  # Get current script directory
    data_path = os.path.join(base_dir, "data/diet_data.csv")

    print(f"[INFO] Loading dataset from: {data_path}")  # Debugging line

    # Check if file exists before reading
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"[ERROR] Data file not found at {data_path}")

    # Load dataset
    data = pd.read_csv(data_path)

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
    joblib.dump(model, os.path.join(base_dir, MODEL_PATH))

    return model, X_test, y_test


def load_model():
    try:
        return joblib.load(MODEL_PATH)
    except FileNotFoundError:
        return None
