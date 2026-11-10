from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required

from .auth import exec_required
from .extensions import database
from .forms import ButtonForm
from .models import User
from .settings import get_setting

blueprint = Blueprint("leaderboard", __name__, url_prefix="/leaderboard")

# Leaderboard page
@blueprint.get("/")
@login_required
def leaderboard():
    form = ButtonForm()
    users = database.session.execute(database.select(User).order_by(User.points.desc(), User.name.asc())).scalars()
    return render_template('leaderboard.html', users=users, form=form, activities_shown=get_setting().activities_shown)

# Reset points
@blueprint.post("/reset")
@exec_required
def reset_points():
    form = ButtonForm()
    if form.validate_on_submit():
        database.session.execute(database.update(User).values(points=0))
        database.session.commit()
    return redirect(url_for("leaderboard.leaderboard"))

# Toggle activities shown
@blueprint.post("/toggle-activity")
@exec_required
def toggle_activities():
    form = ButtonForm()
    if form.validate_on_submit():
        setting = get_setting()
        setting.activities_shown = not setting.activities_shown
        database.session.commit()
    return redirect(url_for("leaderboard.leaderboard"))