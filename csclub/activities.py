from flask import Blueprint, render_template
from flask_login import login_required

from . import two_pointers

blueprint = Blueprint("activities", __name__, url_prefix="/activities")

# Activities page
@blueprint.get("/")
@login_required
def activities():
    return render_template("activities/index.html")

blueprint.register_blueprint(two_pointers.blueprint)