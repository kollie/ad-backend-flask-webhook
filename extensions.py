# extensions.py
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow

db = SQLAlchemy()  # Initialize without an app instance
migrate = Migrate()
ma = Marshmallow()
