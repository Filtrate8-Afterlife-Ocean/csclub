from flask import Flask

from . import activities, announcements, auth, leaderboard, main
from .extensions import database, login_manager, migrate


def create_app():
    
    app = Flask(__name__)
    app.config.from_pyfile('config.py')

    database.init_app(app)
    migrate.init_app(app, database)
    login_manager.init_app(app)

    app.register_blueprint(activities.blueprint)
    app.register_blueprint(announcements.blueprint)
    app.register_blueprint(auth.blueprint)
    app.register_blueprint(leaderboard.blueprint)
    app.register_blueprint(main.blueprint)

    return app