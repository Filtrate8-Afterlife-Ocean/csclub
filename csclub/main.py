from flask import Flask, render_template, Blueprint
from flask_login import login_required

bp = Blueprint("main", __name__, url_prefix="/")

# Landing page
@bp.route("/")
def landing():
    return render_template("landing.html")

# Home page
@bp.route("/user/<name>")
@login_required
def home(name):
    return render_template('home.html', name=name)