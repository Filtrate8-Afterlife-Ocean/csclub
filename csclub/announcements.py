from flask import Flask, render_template, url_for, request, session, flash, redirect, Blueprint
from flask_login import login_required
from . import db

bp = Blueprint("announcements", __name__, url_prefix="/announcements")

# Submit announcements
def submit_announcements(title: str, message: str) -> None:
    announcement = db.Announcement(title=title, message=message)
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
def announce():
    feedback = None
    if request.method == 'POST':
        title = request.form['title']
        message = request.form['msg']
        if not title or not message:
            feedback = "One or more fields are not filled out!"
        else:
            submit_announcements(title, message)
            feedback = "Announcement sent successfully!"
            flash("Message Successfully Sent!")
            return redirect(url_for('announcements.announcements'))
    return render_template("announcements/create.html", feedback=feedback)