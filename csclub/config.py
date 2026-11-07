import os

SECRET_KEY = os.environ["SECRET_KEY"]

try:
    SQLALCHEMY_DATABASE_URI = os.environ["SQLALCHEMY_DATABASE_URI"]
except KeyError:
    SQLALCHEMY_DATABASE_URI = "sqlite:///project.db"

SESSION_COOKIE_NAME = "__session"
SESSION_COOKIE_SECURE = "K_SERVICE" in os.environ