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


app = Flask(__name__)
api = Api(app)
app.config["DEBUG"] = True
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"  # Update for PostgreSQL/MySQL if needed
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
jwt = JWTManager(app)
db = SQLAlchemy(app)
migrage = Migrate(app, db)
ma = Marshmallow(app)
CORS(app)

# WSGI Web Server Gateway Interface

from app import routes, resources, models