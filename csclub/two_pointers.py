from flask import Blueprint, render_template
from flask_login import login_required

blueprint = Blueprint("two_pointers", __name__, url_prefix="/two-pointers")

# Activities page
@blueprint.get("/")
@login_required
def two_pointers():
    return render_template("activities/two_pointers.html")

