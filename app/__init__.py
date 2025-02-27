from flask import Flask
# from flask_admin import Admin
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
api = Api(app)
jwt = JWTManager(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
ma = Marshmallow(app)
CORS(app)


from app import routes