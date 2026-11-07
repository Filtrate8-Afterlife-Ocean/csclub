from flask import Flask, render_template, url_for, request, session, flash, redirect, config
from . import announcements, db

def create_app():
    
    app = Flask(__name__)
    app.config.from_object('config.py')

    db.db.init_app(app)
    with app.app_context():
        db.db.create_all()
    


    # Landing page
    @app.route("/")
    def landing():
        return render_template("landing.html")

    # Home page
    @app.route("/user")
    @app.route("/user/<name>")
    def home(name=None):
        return render_template('home.html', person=name)

    # About page
    @app.route("/about")
    def about():
        return render_template("about.html")

    app.register_blueprint(announcements.bp)
    return app