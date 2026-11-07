from functools import wraps

from click import argument, secho
from flask import Blueprint, abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_required, login_user, logout_user
from sqlalchemy.exc import IntegrityError

from .extensions import database, login_manager
from .forms import LoginForm, RegisterForm
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
        email = form.email.data
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
            return redirect(url_for('main.home', name=username))

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

