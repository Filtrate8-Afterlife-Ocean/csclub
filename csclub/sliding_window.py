from flask import Blueprint, render_template
from flask_login import login_required

from .forms import ButtonForm
from .settings import activity_toggle_required


blueprint = Blueprint("sliding_window", __name__, url_prefix="/sliding-window")

# Activities page
@blueprint.get("/")
@activity_toggle_required
def sliding_window():
    form = ButtonForm()
    return render_template("activities/sliding_window.html", form=form)
