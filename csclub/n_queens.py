from flask import Blueprint, render_template
from flask_login import login_required

from .forms import ButtonForm
from .settings import activity_toggle_required

blueprint = Blueprint("n_queens", __name__, url_prefix="/n-queens")

# Activities page
@blueprint.get("/")
@activity_toggle_required
def n_queens():
    form = ButtonForm()
    return render_template("activities/n_queens.html", form=form)

