from flask import Blueprint, render_template
from flask_login import login_required

blueprint = Blueprint("sliding_window", __name__, url_prefix="/sliding-window")

# Activities page
@blueprint.get("/")
@login_required
def sliding_window():
    return render_template("activities/sliding_window.html")

