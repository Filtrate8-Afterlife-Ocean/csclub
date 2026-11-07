from typing import Optional

from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import login_required

from .auth import exec_required
from .extensions import database
from .forms import AnnouncementForm
from .models import Announcement

blueprint = Blueprint("announcements", __name__, url_prefix="/announcements")

# Submit announcements
def submit_announcements(title: str, message: str, url: Optional[str] = None) -> None:
    announcement = Announcement(title=title, message=message, url=url)
    database.session.add(announcement)
    database.session.commit()

# Get announcements
def get_announcements():
    return database.session.execute(database.select(Announcement).order_by(Announcement.id.desc())).scalars()

# View announcements page
@blueprint.get("/view")
@login_required
def announcements():
    return render_template("announcements/view.html", messages=get_announcements())

# Submit announcement page
@blueprint.route("/create", methods=['GET', 'POST'])
@login_required
@exec_required
def announce():
    form = AnnouncementForm()
    if form.validate_on_submit():
        title = form.title.data
        message = form.message.data
        url = form.url.data
        submit_announcements(title, message, url)
        feedback = "Announcement sent successfully!"
        flash("Message Successfully Sent!")
        return redirect(url_for('announcements.announcements'))
    return render_template("announcements/create.html", form=form)