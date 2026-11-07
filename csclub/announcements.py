from flask import Flask, render_template, url_for, request, session, flash, redirect, Blueprint
from flask_login import login_required
from typing import Optional
from . import db, forms, auth

bp = Blueprint("announcements", __name__, url_prefix="/announcements")

# Submit announcements
def submit_announcements(title: str, message: str, url: Optional[str] = None) -> None:
    announcement = db.Announcement(title=title, message=message, url=url)
    db.db.session.add(announcement)
    db.db.session.commit()

# Get announcements
def get_announcements():
    return db.db.session.execute(db.db.select(db.Announcement).order_by(db.Announcement.id.desc())).scalars()

# View announcements page
@bp.route("/view")
@login_required
def announcements():
    return render_template("announcements/view.html", messages=get_announcements())

# Submit announcement page
@bp.route("/create", methods=['GET', 'POST'])
@login_required
@auth.exec_required
def announce():
    form = forms.AnouncementForm()
    if form.validate_on_submit():
        title = form.title.data
        message = form.message.data
        url = form.url.data
        submit_announcements(title, message, url)
        feedback = "Announcement sent successfully!"
        flash("Message Successfully Sent!")
        return redirect(url_for('announcements.announcements'))
    return render_template("announcements/create.html", form=form)