from flask import Flask, config

from . import announcements, auth, main
from .extensions import database, login_manager, migrate


def create_app():
    
    app = Flask(__name__)
    app.config.from_pyfile('config.py')

    database.init_app(app)
    migrate.init_app(app, database)
    login_manager.init_app(app)
    
    app.register_blueprint(main.blueprint)
    app.register_blueprint(auth.blueprint)
    app.register_blueprint(announcements.blueprint)
    return app