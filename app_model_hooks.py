import os
import pickle
import subprocess

import numpy as np
import pandas as pd
from flask import Flask, request
from sklearn.linear_model import Lasso
from sklearn.metrics import mean_absolute_percentage_error, mean_squared_error
from sklearn.model_selection import train_test_split

os.chdir(os.path.dirname(__file__))


app = Flask(__name__)
app.config["DEBUG"] = True


# Route to endpoint /
@app.route("/", methods=["GET"])
def hello():
    # return "Welcome to the API that predicts revenues from advertising!"
    return "The webhook is working! I'm so happy! :) "


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


@app.route("/webhook", methods=["POST"])
def webhook():
    # route to the repository where the git pull will be applied
    # path_repo = "/route/to/your/repository/on/PythonAnywhere"
    # servidor_web = "/route/to/the/WSGI/file/for/configuration"

    path_repo = "/home/prueba83/flask-project/ad-backend"
    servidor_web = "/var/www/prueba83_pythonanywhere_com_wsgi.py"

    # It checks if the POST request has JSON data
    if request.is_json:
        payload = request.json
        # It verifies that the payload holds information about the repository

        if "repository" in payload:
            # It extracts the repository name and the URL to clone it
            repo_name = payload["repository"]["name"]
            clone_url = payload["repository"]["clone_url"]

            # It changes to the repository directory
            try:
                os.chdir(path_repo)
            except FileNotFoundError:
                return {
                    "message": "The directory of the repository does not exist!"
                }, 404

            # Do a git pull in the repository
            try:
                subprocess.run(["git", "pull", clone_url], check=True)
                subprocess.run(
                    ["touch", servidor_web], check=True
                )  # Trick to automatically reload PythonAnywhere WebServer
                return {
                    "message": f"A git pull was applied in the repository {repo_name}"
                }, 200
            except subprocess.CalledProcessError:
                return {
                    "message": f"Error trying to git pull the repository {repo_name}"
                }, 500
        else:
            return {
                "message": "No information found about the repository in the payload"
            }, 400
    else:
        return {"message": "The request does not have JSON data"}, 400


if __name__ == "__main__":
    app.run()
