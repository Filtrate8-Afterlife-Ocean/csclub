from flask import Flask, render_template, url_for, request, session
import os

app = Flask(__name__)

app.secret_key = os.environ["SECRET_KEY"]

# Home page
@app.route("/")
@app.route("/<name>")
def home(name=None):
    return render_template('home.html', person=name)

# About page
@app.route("/about")
def about():
    return render_template("about.html")

# See announcements
messages = ["hi", "there"]
@app.route("/announcement", methods=['GET', 'POST'])
def announcements():
    # if request.method == 'GET':
    return render_template("announcements.html")
    # else:
    #     title = request.form['title']
    #     message = request.form['msg']

# Submit announcement
@app.route("/announce")
def announce():
    return render_template("announce.html")