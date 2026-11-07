from flask import Blueprint, render_template
from flask_login import login_required

blueprint = Blueprint("main", __name__, url_prefix="/")

# Landing page
@blueprint.get("/")
def landing():
    return render_template("landing.html")

# Home page
@blueprint.get("/user")
@login_required
def home():
    return render_template('home.html')