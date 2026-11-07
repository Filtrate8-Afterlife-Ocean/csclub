from flask import Flask, render_template, url_for, request, session, flash, redirect, Blueprint, abort
from sqlalchemy.exc import IntegrityError
from flask_login import login_user, logout_user, login_required, current_user
from functools import wraps
from . import db, main, forms
import click

bp = Blueprint("auth", __name__, url_prefix="/auth")

# Load user in
@db.login_manager.user_loader
def load_user(id: str):
    return db.db.session.get(db.User, int(id)) # db.db.session.execute(db.db.select(db.User).where(db.User.id == id)).scalar()

# Register page
@bp.route("/register", methods=["GET", "POST"])
def register():
    form = forms.RegisterForm()
    if form.validate_on_submit():
        name = form.name.data
        username = form.username.data
        email = form.email.data
        password = form.password.data

        try:
            user = db.User(name=name, username=username, email=email, password_hash=db.User.hash_password(password))
            db.db.session.add(user)
            db.db.session.commit()
        except IntegrityError:
            db.db.session.rollback()
            flash("Username or email is already registered.")
        else:
            return redirect(url_for("auth.login"))

    return render_template('auth/register.html', form=form) 

# Login page
@bp.route("/login", methods=["GET", "POST"])
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = db.db.session.execute(db.db.select(db.User).where(db.User.username == username)).scalar()
        if user is None or not user.validate_password(password):  
            flash("Incorrect username or password.")
        else:
            login_user(user)
            return redirect(url_for('main.home', name=username))

    return render_template('auth/login.html', form=form)

# Logout
@bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.landing"))

# Executive is required
def exec_required(function):
    @wraps(function)
    def decorated_function(*args, **kwargs):
        if not current_user.is_exec:
            abort(403, description="User is not an executive.")
        return function(*args, **kwargs)
    return decorated_function

# Create executive (terminal only)
@bp.cli.command("declare-exec")
@click.argument("username")
def declare_exec(username):
    user = db.db.session.execute(db.db.select(db.User).where(db.User.username == username)).scalar()
    if user is None:
        click.echo("No user found!")
    user.is_exec = True
    db.db.session.commit()
    click.echo(f"{username} successfully declared as an exec!")