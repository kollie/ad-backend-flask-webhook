import os
import pickle
import subprocess
import time
import requests
from threading import Thread

import numpy as np
import pandas as pd  
from flask import request
from sklearn.linear_model import Lasso
from sklearn.metrics import mean_absolute_percentage_error, mean_squared_error
from sklearn.model_selection import train_test_split

from flask import jsonify
from marshmallow import ValidationError

from app import app, jwt, api

from app.resources.user import UserRegister, UserLogin, DietDataResource
from app.resources.food import TrainModelResource, PredictFoodResource
from app.resources.result import AllUsersWithDietData, UserDietByID, UserDietByQuery


os.chdir(os.path.dirname(__file__))
    
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

api.add_resource(UserDietByID, "/user_diet/<int:user_id>")
api.add_resource(UserDietByQuery, "/user_diet_query")

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


# def install_requirements():
#     """Install dependencies from requirements.txt"""
#     print("[INFO] Installing required packages...")
#     try:
#         subprocess.run(["pip", "install", "-r", "requirements.txt"], check=True)
#         print("[SUCCESS] All packages installed successfully.")
#     except subprocess.CalledProcessError:
#         print("[ERROR] Failed to install dependencies!")


# def run_migrations():
#     """Run Flask database migrations with app context"""
#     print("[INFO] Running database migrations...")     

#     os.environ["FLASK_APP"] = "/home/kollie/flask-project/ad-backend-flask-webhook/main.py"

#     try:
#         from main import application  # Import inside function to avoid circular imports
#         from app import db

#         with application.app_context():
#             if not os.path.exists(os.path.join(os.getcwd(), "migrations")):
#                 print("[INFO] Initializing migrations...")
#                 subprocess.run(["flask", "db", "init"], check=True)
#             else:
#                 print("[INFO] Migrations already initialized. Skipping 'flask db init'.")

#             print("[INFO] Running migrations...")
#             subprocess.run(["flask", "db", "migrate", "-m", "Auto migration"], check=True)
#             subprocess.run(["flask", "db", "upgrade"], check=True)

#             print("[SUCCESS] Database migrations completed.")
#     except subprocess.CalledProcessError as e:
#         print(f"[ERROR] Migration failed: {e}")

def run_migrations():
    """Run Flask database migrations only if needed."""
    print("[INFO] Running database migrations...")

    os.environ["FLASK_APP"] = "/home/kollie/flask-project/ad-backend-flask-webhook/main.py"

    try:
        from main import application  # Import inside function to avoid circular imports
        from app import db

        with application.app_context():
            migration_path = os.path.join(os.getcwd(), "app/migrations")
            if not os.path.exists(migration_path) or not os.listdir(migration_path):
                print("[INFO] Initializing migrations...")
                subprocess.run(["flask", "db", "init"], check=True)
            else:
                print("[INFO] Migrations already initialized. Skipping 'flask db init'.")

            # Check if there are any new model changes before running migration
            result = subprocess.run(["flask", "db", "migrate", "-m", "Auto migration"], capture_output=True, text=True)
            if "No changes detected" in result.stdout:
                print("[INFO] No changes detected in models. Skipping 'flask db migrate'.")
            else:
                print("[INFO] Running migrations...")
                subprocess.run(["flask", "db", "upgrade"], check=True)
                print("[SUCCESS] Database migrations completed.")

    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Migration failed: {e}")



def register_users():
    print("[INFO] Registering test users...")
    for user in test_users:
        response = requests.post("http://127.0.0.1/register", json=user, headers=HEADERS)
        if response.status_code == 201:
            print(f"[SUCCESS] User {user['username']} registered.")
        else:
            print(f"[ERROR] User {user['username']} registration failed: {response.json()}")



def login_users():
    print("[INFO] Logging in users...")
    user_tokens = {}
    for user in test_users:
        login_data = {"username": user["username"], "password": user["password"]}
        response = requests.post("http://127.0.0.1/login", json=login_data, headers=HEADERS)
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
        response = requests.post("http://127.0.0.1/diet", json=test_diet_data, headers=auth_headers)
        if response.status_code == 201:
            print(f"[SUCCESS] Diet data saved for {username}.")
        else:
            print(f"[ERROR] Saving diet data for {username} failed: {response.json()}")



def train_model(user_tokens):
    print("[INFO] Training the model...")
    # Use the first user's token to train the model
    token = list(user_tokens.values())[0]
    auth_headers = {**HEADERS, "Authorization": f"Bearer {token}"}
    response = requests.post("http://127.0.0.1/train_model", headers=auth_headers)

    if response.status_code == 200:
        print("[SUCCESS] Model trained successfully.")
    else:
        print("[ERROR] Model training failed:", response.json())


def test_prediction(user_tokens):
    print("[INFO] Running diet prediction...")
    for username, token in user_tokens.items():
        auth_headers = {**HEADERS, "Authorization": f"Bearer {token}"}
        response = requests.post("http://127.0.0.1/predict_food", json=test_diet_data, headers=auth_headers)

        if response.status_code == 200:
            prediction = response.json()
            print(f"[SUCCESS] Diet prediction for {username}: {prediction}")
        else:
            print(f"[ERROR] Diet prediction for {username} failed: {response.json()}")


# @app.route("/webhook", methods=["POST"])
# def webhook():
#     print("[INFO] Webhook triggered.")
#     path_repo = "/home/kollie/flask-project/ad-backend-flask-webhook"
#     servidor_web = "/var/www/kollie_pythonanywhere_com_wsgi.py"

#     if request.is_json:
#         payload = request.json
#         if "repository" in payload:
#             repo_name = payload["repository"]["name"]
#             clone_url = payload["repository"]["clone_url"]

#             try:
#                 os.chdir(path_repo)
#             except FileNotFoundError:
#                 print("[ERROR] Repository path not found!")
#                 return {"message": "The directory of the repository does not exist!"}, 404

#             try:
#                 print("[INFO] Running Git Pull...")
#                 subprocess.run(["git", "pull", clone_url], check=True)
#                 print("[SUCCESS] Git Pull Completed.")

#                 from app import app
#                 with app.app_context():
#                     print("[INFO] Running Migrations...")
#                     run_migrations()

#                     print("[INFO] Registering Users...")
#                     register_users()

#                     print("[INFO] Logging in Users...")
#                     user_tokens = login_users()

#                     if user_tokens:
#                         print("[INFO] Passing User Diet Data...")
#                         pass_user_data(user_tokens)

#                         print("[INFO] Training Model...")
#                         train_model(user_tokens)

#                         print("[INFO] Running Predictions...")
#                         test_prediction(user_tokens)

#                 subprocess.run(["touch", servidor_web], check=True)
#                 print("[SUCCESS] Web server reloaded.")
#                 return {"message": f"Webhook processed for {repo_name}."}, 200

#             except subprocess.CalledProcessError as e:
#                 print(f"[ERROR] Git pull failed: {str(e)}")
#                 return {"message": f"Git pull error: {repo_name}"}, 500
#     return {"message": "Invalid webhook payload"}, 400


# from threading import Thread

# @app.route("/webhook", methods=["POST"])
# def webhook():
#     print("[INFO] Webhook triggered.")
#     path_repo = "/home/kollie/flask-project/ad-backend-flask-webhook"
#     servidor_web = "/var/www/kollie_pythonanywhere_com_wsgi.py"
#     BASE_URL = "https://kollie.pythonanywhere.com"

#     if request.is_json:
#         payload = request.json
#         if "repository" in payload:
#             repo_name = payload["repository"]["name"]
#             clone_url = payload["repository"]["clone_url"]

#             try:
#                 os.chdir(path_repo)
#             except FileNotFoundError:
#                 print("[ERROR] Repository path not found!")
#                 return {"message": "The directory of the repository does not exist!"}, 404

#             # Run long processes in the background
#             def process_webhook():
#                 try:
#                     print("[INFO] Running Git Pull...")
#                     subprocess.run(["git", "pull", clone_url], check=True)
#                     print("[SUCCESS] Git Pull Completed.")

#                     from app import app
#                     with app.app_context():  

#                         print("[INFO] Running Migrations...")

#                         run_migrations()

#                         print("[INFO] Registering Users...")
#                         register_users()

#                         print("[INFO] Logging in Users...")
#                         user_tokens = login_users()

#                         if user_tokens:
#                                 print("[INFO] Passing User Diet Data...")
#                                 pass_user_data(user_tokens)

#                                 print("[INFO] Training Model...")
#                                 train_model(user_tokens)

#                                 print("[INFO] Running Predictions...")
#                                 test_prediction(user_tokens)

#                     subprocess.run(["touch", servidor_web], check=True)
#                     print("[SUCCESS] Web server reloaded.")

#                 except subprocess.CalledProcessError as e:
#                     print(f"[ERROR] Git pull failed: {str(e)}")

#             # Run webhook process in a separate thread to avoid GitHub timeout
#             thread = Thread(target=process_webhook)
#             thread.start()

#             return {"message": f"Webhook received for {repo_name}, processing in background."}, 200

#     return {"message": "Invalid webhook payload"}, 400


@app.route("/webhook", methods=["POST"])
def webhook():
    """GitHub Webhook - Only Runs Migrations"""
    print("[INFO] Webhook triggered.")
    path_repo = "/home/kollie/flask-project/ad-backend-flask-webhook"
    servidor_web = "/var/www/kollie_pythonanywhere_com_wsgi.py"

    if request.is_json:
        payload = request.json
        if "repository" in payload:
            repo_name = payload["repository"]["name"]
            clone_url = payload["repository"]["clone_url"]

            try:
                os.chdir(path_repo)
            except FileNotFoundError:
                print("[ERROR] Repository path not found!")
                return {"message": "The directory of the repository does not exist!"}, 404

            try:
                print("[INFO] Running Git Pull...")
                subprocess.run(["git", "pull", clone_url], check=True)
                print("[SUCCESS] Git Pull Completed.")

                from app import app
                with app.app_context():
                    print("[INFO] Running Migrations...")
                    run_migrations()  # ✅ Only running migrations!

                subprocess.run(["touch", servidor_web], check=True)
                print("[SUCCESS] Web server reloaded.")

                return {"message": f"Webhook processed for {repo_name}, migrations completed."}, 200

            except subprocess.CalledProcessError as e:
                print(f"[ERROR] Git pull failed: {str(e)}")
                return {"message": f"Git pull error: {repo_name}"}, 500
    return {"message": "Invalid webhook payload"}, 400


@app.route("/run-migrations", methods=["GET"])
def run_migrations_endpoint():
    """Manually run database migrations inside Flask app context."""
    print("[INFO] Running Migrations...")
    try:
        with app.app_context():
            run_migrations()
        return jsonify({"message": "Migrations completed successfully."}), 200
    except Exception as e:
        print(f"[ERROR] Migration failed: {str(e)}")
        return jsonify({"message": f"Migration failed: {str(e)}"}), 500


@app.route("/register-users", methods=["GET"])
def register_users_endpoint():
    """Manually register test users inside Flask app context."""
    print("[INFO] Registering Users...")
    try:
        with app.app_context():
            register_users()
        return jsonify({"message": "Users registered successfully."}), 200
    except Exception as e:
        print(f"[ERROR] User registration failed: {str(e)}")
        return jsonify({"message": f"User registration failed: {str(e)}"}), 500


@app.route("/login-users", methods=["GET"])
def login_users_endpoint():
    """Manually log in users and retrieve JWT tokens inside Flask app context."""
    print("[INFO] Logging in Users...")
    try:
        with app.app_context():
            user_tokens = login_users()
        return jsonify({"message": "Users logged in successfully.", "tokens": user_tokens}), 200
    except Exception as e:
        print(f"[ERROR] User login failed: {str(e)}")
        return jsonify({"message": f"User login failed: {str(e)}"}), 500


@app.route("/pass-diet-data", methods=["GET"])
def pass_diet_data_endpoint():
    """Manually send diet data for users inside Flask app context."""
    print("[INFO] Passing User Diet Data...")
    try:
        with app.app_context():
            user_tokens = login_users()
            pass_user_data(user_tokens)
        return jsonify({"message": "Diet data passed successfully."}), 200
    except Exception as e:
        print(f"[ERROR] Passing diet data failed: {str(e)}")
        return jsonify({"message": f"Passing diet data failed: {str(e)}"}), 500


@app.route("/train-model", methods=["GET"])
def train_model_endpoint():
    """Manually train the machine learning model inside Flask app context."""
    print("[INFO] Training Model...")
    try:
        with app.app_context():
            user_tokens = login_users()
            train_model(user_tokens)
        return jsonify({"message": "Model trained successfully."}), 200
    except Exception as e:
        print(f"[ERROR] Model training failed: {str(e)}")
        return jsonify({"message": f"Model training failed: {str(e)}"}), 500


@app.route("/run-predictions", methods=["GET"])
def run_predictions_endpoint():
    """Manually run predictions for users inside Flask app context."""
    print("[INFO] Running Predictions...")
    try:
        with app.app_context():
            user_tokens = login_users()
            test_prediction(user_tokens)
        return jsonify({"message": "Predictions completed successfully."}), 200
    except Exception as e:
        print(f"[ERROR] Predictions failed: {str(e)}")
        return jsonify({"message": f"Predictions failed: {str(e)}"}), 500





