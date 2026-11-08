from flask import Blueprint, render_template
from flask_login import login_required

from .auth import exec_required
from .extensions import database
from .forms import ButtonForm
from .models import User

blueprint = Blueprint("leaderboard", __name__, url_prefix="/leaderboard")

# Landing page
@blueprint.get("/")
@login_required
def leaderboard():
    form = ButtonForm()
    users = database.session.execute(database.select(User).order_by(User.name.asc())).scalars()
    return render_template('leaderboard.html', users=users, form=form)