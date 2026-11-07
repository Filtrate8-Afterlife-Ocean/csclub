from flask import Flask, render_template, url_for, request, session, flash, redirect, Blueprint
from sqlalchemy.exc import IntegrityError
from flask_login import login_user
from . import db, main, forms


bp = Blueprint("auth", __name__, url_prefix="/auth")

# Load user in
@db.login_manager.user_loader
def load_user(id: str):
    return db.db.session.execute(db.db.select(db.User).where(db.User.id == id)).scalar()

# Register page
@bp.route("/register", methods=["GET", "POST"])
def register():
    form = forms.RegisterForm()
    if request.method == "POST":
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
    if request.method == "POST":
        username = form.username.data
        password = form.password.data

        user = db.db.session.execute(db.db.select(db.User).where(db.User.username == username)).scalar()
        if user is None or not user.validate_password(password):  
            flash("Incorrect username or password.")
        else:
            login_user(user)
            return redirect(url_for('main.home', name=username))

    return render_template('auth/login.html', form=form)