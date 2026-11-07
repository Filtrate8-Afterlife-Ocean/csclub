from flask import Flask, render_template, url_for, request, session, flash, redirect, config
from . import main, announcements, db

def create_app():
    
    app = Flask(__name__)
    app.config.from_pyfile('config.py')

    db.db.init_app(app)
    db.migrate.init_app(app, db.db)
    
    app.register_blueprint(main.bp)
    app.register_blueprint(announcements.bp)
    return app