from flask import Flask, render_template, Blueprint
from flask_login import login_required

bp = Blueprint("main", __name__, url_prefix="/")

# Landing page
@bp.route("/")
def landing():
    return render_template("landing.html")

# Home page
@bp.route("/user")
@bp.route("/user/<name>")
@login_required
def home(name=None):
    return render_template('home.html', person=name)

# About page
@bp.route("/about")
def about():
    return render_template("about.html")