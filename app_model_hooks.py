import os
import pickle
import subprocess
import time
import requests
from flask import Flask, request

import numpy as np
import pandas as pd
from flask import Flask, request
from sklearn.linear_model import Lasso
from sklearn.metrics import mean_absolute_percentage_error, mean_squared_error
from sklearn.model_selection import train_test_split
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from app.resoureces.user import UserRegister, UserLogin, DietDataResource
from app.resoureces.food import TrainModelResource, PredictFoodResource
from app.resoureces.result import AllUsersWithDietData

os.chdir(os.path.dirname(__file__))


app = Flask(__name__)
app.config["DEBUG"] = True
app = Flask(__name__)
api = Api(app)
jwt = JWTManager(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
ma = Marshmallow(app)
CORS(app)


# Configure Database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"  # Update for PostgreSQL/MySQL if needed
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize Extensions
db.init_app(app)
migrate.init_app(app, db)

# Route to endpoint /
@app.route("/", methods=["GET"])
def hello():
    # return "Welcome to the API that predicts revenues from advertising!"
    return "The webhook is working! happy yayyyy :) "

# user info

api.add_resource(UserRegister, "/register")
api.add_resource(UserLogin, "/login")
api.add_resource(DietDataResource, "/diet")  # Protected route

# food prediciton

api.add_resource(TrainModelResource, "/train_model")
api.add_resource(PredictFoodResource, "/predict_food")

# return result
api.add_resource(AllUsersWithDietData, "/users_diet_data")

# Route to endpoint /api/v1/predict

"""
The petition would be:
http://x.x.x.x:5000/api/v1/predict?radio=15&newspaper=60&tv=80
"""


@app.route("/api/v1/predict", methods=["GET"])
def predict():
    model = pickle.load(open("ad_model.pkl", "rb"))
    tv = request.args.get("tv", None)
    radio = request.args.get("radio", None)
    newspaper = request.args.get("newspaper", None)

    print(tv, radio, newspaper)
    print(type(tv))

    if tv is None or radio is None or newspaper is None:
        return "Args empty, the data is not enough to predict!"
    else:
        prediction = model.predict([[float(tv), float(radio), float(newspaper)]])

    return {"predictions": prediction[0]}


"""
The petition would be:
http://x.x.x.x:5000/api/v1/retrain
"""


@app.route("/api/v1/retrain", methods=["GET"])
def retrain():
    if os.path.exists("data/Advertising_new.csv"):
        data = pd.read_csv("data/Advertising_new.csv")

        X_train, X_test, y_train, y_test = train_test_split(
            data.drop(columns=["sales"]), data["sales"], test_size=0.20, random_state=42
        )

        model = Lasso(alpha=6000)
        model.fit(X_train, y_train)
        rmse = np.sqrt(mean_squared_error(y_test, model.predict(X_test)))
        mape = mean_absolute_percentage_error(y_test, model.predict(X_test))
        model.fit(data.drop(columns=["sales"]), data["sales"])
        pickle.dump(model, open("ad_model.pkl", "wb"))

        return f"Model retrained. New evaluation metric RMSE: {str(rmse)}, MAPE: {str(mape)}"
    else:
        return "<h2>New data for retrain NOT FOUND. Nothing done!</h2>"
    
# Repository and server paths on PythonAnywhere
path_repo = "/home/kollie/flask-project/ad-backend-flask-webhook"
servidor_web = "/var/www/kollie_pythonanywhere_com_wsgi.py"
BASE_URL = "https://kollie.pythonanywhere.com"  # Update with your actual deployment URL

HEADERS = {"Content-Type": "application/json"}

# Test users
test_users = [
    {"first_name": "John", "last_name": "Doe", "username": "johndoe", "password": "password123"},
    {"first_name": "Jane", "last_name": "Smith", "username": "janesmith", "password": "securepass"},
    {"first_name": "Alice", "last_name": "Brown", "username": "alicebrown", "password": "pass1234"},
    {"first_name": "Bob", "last_name": "Wilson", "username": "bobwilson", "password": "mypassword"},
]

# Test diet data
test_diet_data = {
    "age": 30,
    "gender": "Male",
    "height": 175.0,
    "weight": 75.0,
    "activity_level": "Moderate",
    "goal": "Muscle Gain",
    "dietary_preference": "Balanced"
}


def install_requirements():
    """Install dependencies from requirements.txt"""
    print("[INFO] Installing required packages...")
    try:
        subprocess.run(["pip", "install", "-r", "requirements.txt"], check=True)
        print("[SUCCESS] All packages installed successfully.")
    except subprocess.CalledProcessError:
        print("[ERROR] Failed to install dependencies!")


def run_migrations():
    """Run Flask database migrations with app context"""
    print("[INFO] Running database migrations...")

    # Set Flask app manually if needed
    os.environ["FLASK_APP"] = "app_model_hooks.py"

    from app_model_hooks import app, db  # Import inside function to ensure context

    with app.app_context():
        if not os.path.exists(os.path.join(path_repo, "migrations")):
            print("[INFO] Initializing migrations...")
            subprocess.run(["flask", "db", "init"], check=True)

        subprocess.run(["flask", "db", "migrate", "-m", "Auto migration"], check=True)
        subprocess.run(["flask", "db", "upgrade"], check=True)

    print("[SUCCESS] Database migrations completed.")



def register_users():
    print("[INFO] Registering test users...")
    for user in test_users:
        response = requests.post(f"{BASE_URL}/register", json=user, headers=HEADERS)
        if response.status_code == 201:
            print(f"[SUCCESS] User {user['username']} registered.")
        else:
            print(f"[ERROR] User {user['username']} registration failed: {response.json()}")


def login_users():
    print("[INFO] Logging in users...")
    user_tokens = {}
    for user in test_users:
        login_data = {"username": user["username"], "password": user["password"]}
        response = requests.post(f"{BASE_URL}/login", json=login_data, headers=HEADERS)
        if response.status_code == 200:
            token = response.json()["access_token"]
            user_tokens[user["username"]] = token
            print(f"[SUCCESS] User {user['username']} logged in.")
        else:
            print(f"[ERROR] User {user['username']} login failed: {response.json()}")
    return user_tokens


def pass_user_data(user_tokens):
    print("[INFO] Passing diet data for users...")
    for username, token in user_tokens.items():
        auth_headers = {**HEADERS, "Authorization": f"Bearer {token}"}
        response = requests.post(f"{BASE_URL}/diet", json=test_diet_data, headers=auth_headers)
        if response.status_code == 201:
            print(f"[SUCCESS] Diet data saved for {username}.")
        else:
            print(f"[ERROR] Saving diet data for {username} failed: {response.json()}")


def train_model(user_tokens):
    print("[INFO] Training the model...")
    # Use the first user's token to train the model
    token = list(user_tokens.values())[0]
    auth_headers = {**HEADERS, "Authorization": f"Bearer {token}"}
    response = requests.post(f"{BASE_URL}/train_model", headers=auth_headers)

    if response.status_code == 200:
        print("[SUCCESS] Model trained successfully.")
    else:
        print("[ERROR] Model training failed:", response.json())


def test_prediction(user_tokens):
    print("[INFO] Running diet prediction...")
    for username, token in user_tokens.items():
        auth_headers = {**HEADERS, "Authorization": f"Bearer {token}"}
        response = requests.post(f"{BASE_URL}/predict_food", json=test_diet_data, headers=auth_headers)

        if response.status_code == 200:
            prediction = response.json()
            print(f"[SUCCESS] Diet prediction for {username}: {prediction}")
        else:
            print(f"[ERROR] Diet prediction for {username} failed: {response.json()}")


@app.route("/webhook", methods=["POST"])
def webhook():
    """GitHub Webhook to pull latest code and reload the server"""
    if request.is_json:
        payload = request.json

        if "repository" in payload:
            repo_name = payload["repository"]["name"]
            clone_url = payload["repository"]["clone_url"]

            # Change to the repository directory
            try:
                os.chdir(path_repo)
            except FileNotFoundError:
                return {"message": "Repository directory does not exist!"}, 404

            # Force Fetch Latest Code
            try:
                subprocess.run(["git", "fetch", "origin"], check=True)
                subprocess.run(["git", "reset", "--hard", "origin/master"], check=True)  # Hard reset
                subprocess.run(["git", "pull", "origin", "master"], check=True)  # Ensure latest changes
                print("[SUCCESS] Git pull applied.")
            except subprocess.CalledProcessError:
                return {"message": "Error pulling from GitHub!"}, 500

            # # Install Dependencies
            # install_requirements()

            # Run Database Migrations
            run_migrations()

            # Register Multiple Users
            register_users()

            # Log In Users & Retrieve JWT Tokens
            user_tokens = login_users()

            if user_tokens:
                # Pass User Diet Data
                pass_user_data(user_tokens)

                # Train the Model
                train_model(user_tokens)

                # Run Prediction
                test_prediction(user_tokens)

            # Reload PythonAnywhere Web Server
            subprocess.run(["touch", servidor_web], check=True)
            print("[SUCCESS] Web server reloaded.")

            return {"message": f"Pull request processed for {repo_name}, API updated successfully."}, 200

        return {"message": "No repository info in payload"}, 400

    return {"message": "Request does not have JSON data"}, 400


# @app.route("/webhook", methods=["POST"])
# def webhook():
#     # route to the repository where the git pull will be applied
#     # path_repo = "/route/to/your/repository/on/PythonAnywhere"
#     # servidor_web = "/route/to/the/WSGI/file/for/configuration"

#     path_repo = "/home/kollie/flask-project/ad-backend-flask-webhook"
#     servidor_web = "/var/www/kollie_pythonanywhere_com_wsgi.py"

#     # It checks if the POST request has JSON data
#     if request.is_json:
#         payload = request.json
#         # It verifies that the payload holds information about the repository

#         if "repository" in payload:
#             # It extracts the repository name and the URL to clone it
#             repo_name = payload["repository"]["name"]
#             clone_url = payload["repository"]["clone_url"]

#             # It changes to the repository directory
#             try:
#                 os.chdir(path_repo)
#             except FileNotFoundError:
#                 return {
#                     "message": "The directory of the repository does not exist!"
#                 }, 404

#             # Do a git pull in the repository
#             try:
#                 subprocess.run(["git", "pull", clone_url], check=True)
#                 subprocess.run(
#                     ["touch", servidor_web], check=True
#                 )  # Trick to automatically reload PythonAnywhere WebServer
#                 return {
#                     "message": f"A git pull was applied in the repository {repo_name}"
#                 }, 200
#             except subprocess.CalledProcessError:
#                 return {
#                     "message": f"Error trying to git pull the repository {repo_name}"
#                 }, 500
#         else:
#             return {
#                 "message": "No information found about the repository in the payload"
#             }, 400
#     else:
#         return {"message": "The request does not have JSON data"}, 400


if __name__ == "__main__":
    app.run()
