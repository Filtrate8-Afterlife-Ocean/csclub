from flask import Flask, render_template, url_for, request, session, flash, redirect
from classes import Announcement
import os

app = Flask(__name__)

app.secret_key = os.environ["SECRET_KEY"]

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
messages = []
@app.route("/announcements")
def announcements():
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
            messages.append(Announcement(title, message))
            feedback = "Announcement sent successfully!"
            flash("Message Successfully Sent!")
            return redirect(url_for('announcements'))
    return render_template("announce.html", feedback=feedback)