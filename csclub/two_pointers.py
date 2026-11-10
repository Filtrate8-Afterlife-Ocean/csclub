from flask import Blueprint, render_template
from flask_login import login_required

from .forms import ButtonForm
from .settings import activity_toggle_required


blueprint = Blueprint("two_pointers", __name__, url_prefix="/two-pointers")

# Activities page
@blueprint.get("/")
@activity_toggle_required
def two_pointers():
    form = ButtonForm()
    return render_template("activities/two_pointers.html", form=form)

