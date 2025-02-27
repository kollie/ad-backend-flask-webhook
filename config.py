import os


baseddir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    DEBUG = False
    SECRET_KEY = os.environ.get("SECRET_KEY") or "this-is-my-secret-key"
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI") \
        or "sqlite:///" + os.path.join(baseddir, "app.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PROPAGATE_EXCEPTIONS = True
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ["access", "refresh"]
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY") or "amazing-api"