from flask import Flask, render_template

app = Flask(__name__)

# Home page
@app.route("/")
@app.route("/<name>")
def home(name=None):
    return render_template('home.html.jinja', person=name)

# About page
# @app.route("/about")
# def about():
#     return render_template("hi")