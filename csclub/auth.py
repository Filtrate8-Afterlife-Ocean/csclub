from flask import Flask, render_template, url_for, request, session, flash, redirect, Blueprint
from . import db, main

bp = Blueprint("auth", __name__, url_prefix="/auth")

# Load user in
def load_user(id: str):
    return db.db.session.execute(db.db.select(db.User).where(db.User.id == id)).scalar()

# Locate error for register form submission
def locate_register_error(name: str, username: str, email: str, password: str) -> str:
    if not name:
        return "Name is required."
    elif not username:
        return "Username is required."
    elif not email:
        return "Email is required."
    elif not password:
        return "Password is required."
    return None

# Register page
@bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        username = request.form["username"]
        email = request.form["email"]
        password = request.form['password']
        feedback = locate_error(username, password)

        if feedback is None:
            try:
                password_hash = generate_password_hash(password)
                user = db.User(name=name, username=username, email=email, password_hash=password_hash)
                db.db.session.add(user)
                db.db.session.commit()
            except db.IntegrityError:
                feedback = f"Username or email is already registered."
            else:
                return redirect(url_for("auth.login"))

        flash(feedback)

    return render_template('auth/register.html') 

# Locate error for login form submission
def locate_login_error(username: str, password: str) -> str:
    if not name:
        return "Name is required."
    else:
        return "Password is required."
    return None

# Login page
@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        feedback = locate_error(username, password)
        if feedback is None:
            user = db.db.session.execute(db.db.select(db.User).where(db.User.username == username)).scalar()
            if user is None or not check_password_hash(user['password_hash'], password):
                feedback = "Incorrect username or password."

            if feedback is None:
                session.clear()
                session['user_id'] = user['id']
                return redirect(url_for('main.user', name=username))

            flash(feedback)

    return render_template('auth/login.html')