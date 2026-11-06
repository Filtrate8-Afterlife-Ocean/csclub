from flask import Flask, render_template, url_for, request, session, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
import os

class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ["SECRET_KEY"]
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
db.init_app(app)

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column()

class Announcement(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column()
    message: Mapped[str] = mapped_column()

with app.app_context():
    db.create_all()

# Landing page
@app.route("/")
def landing():
    return render_template("landing.html")

# Home page
@app.route("/user")
@app.route("/user/<name>")
def home(name=None):
    return render_template('home.html', person=name)

# About page
@app.route("/about")
def about():
    return render_template("about.html")

# See announcements
@app.route("/announcements")
def announcements():
    messages = db.session.execute(db.select(Announcement).order_by(Announcement.id.desc())).scalars()
    return render_template("announcements.html", messages=messages)

# Submit announcement
@app.route("/announce", methods=['GET', 'POST'])
def announce():
    feedback = None
    if request.method == 'POST':
        title = request.form['title']
        message = request.form['msg']
        if not title or not message:
            feedback = "One or more fields are not filled out!"
        else:
            announcement = Announcement(title=title, message=message)
            db.session.add(announcement)
            db.session.commit()
            feedback = "Announcement sent successfully!"
            flash("Message Successfully Sent!")
            return redirect(url_for('announcements'))
    return render_template("announce.html", feedback=feedback)