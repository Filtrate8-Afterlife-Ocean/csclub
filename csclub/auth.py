from functools import wraps

from click import argument, secho
from flask import Blueprint, abort, flash, redirect, render_template, url_for, request
from flask_login import current_user, login_required, login_user, logout_user
from sqlalchemy.exc import IntegrityError

from .extensions import database, login_manager
from .forms import ButtonForm, LoginForm, RegisterForm
from .models import User

blueprint = Blueprint("auth", __name__, url_prefix="/auth")

# Load user in
@login_manager.user_loader
def load_user(id: str):
    return database.session.get(User, int(id)) 

# Register page
@blueprint.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        name = form.name.data
        username = form.username.data
        email = form.email.data.lower()
        password = form.password.data

        try:
            user = User(name=name, username=username, email=email)
            user.set_password(password)
            database.session.add(user)
            database.session.commit()
        except IntegrityError:
            database.session.rollback()
            flash("Username or email is already registered.")
        else:
            return redirect(url_for("auth.login"))

    return render_template('auth/register.html', form=form) 

# Login page
@blueprint.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = database.session.execute(database.select(User).where(User.username == username)).scalar()
        if user is None or not user.validate_password(password):  
            flash("Incorrect username or password.")
        else:
            login_user(user)
            next_url = request.args.get('next')
            if next_url is None or not next_url.startswith("/") or next_url.startswith("//"):
                next_url = url_for("main.home")
            return redirect(next_url)

    return render_template('auth/login.html', form=form)

# Logout
@blueprint.get("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.landing"))

# Executive is required
def exec_required(function):
    @wraps(function)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for("main.landing"))
        elif not current_user.is_exec:
            abort(403, description="User is not an executive.")
        return function(*args, **kwargs)
    return decorated_function

# Create executive (terminal only)
@blueprint.cli.command("declare-exec")
@argument("username")
def declare_exec(username):
    user = database.session.execute(database.select(User).where(User.username == username)).scalar()
    if user is None:
        secho("No user found!", fg="red", bold=True)
        return
    user.is_exec = True
    database.session.commit()
    secho(f"{username} successfully declared as an exec!", fg="green", bold=True)

# Promote user to executive
@blueprint.post("/promote/<user_id>")
@exec_required
def promote(user_id: int):
    form = ButtonForm()
    if form.validate_on_submit():
        user = database.session.execute(database.select(User).where(User.id == user_id)).scalar()
        user.is_exec = True
        database.session.commit()
    return redirect(url_for("leaderboard.leaderboard"))

# Demote executive to user
@blueprint.post("/demote/<user_id>")
@exec_required
def demote(user_id: int):
    form = ButtonForm()
    if form.validate_on_submit():
        user = database.session.execute(database.select(User).where(User.id == user_id)).scalar()
        user.is_exec = False
        database.session.commit()
    return redirect(url_for("leaderboard.leaderboard"))

# Remove user
@blueprint.post("/remove/<user_id>")
@exec_required
def remove(user_id: int):
    form = ButtonForm()
    if form.validate_on_submit():
        user = database.session.execute(database.select(User).where(User.id == user_id)).scalar()
        database.session.delete(user)
        database.session.commit()
    return redirect(url_for("leaderboard.leaderboard"))