from flask_wtf import FlaskForm
from wtforms import (PasswordField, StringField, TextAreaField, URLField,
                     validators)


# Registration form for new user
class RegisterForm(FlaskForm):
    name = StringField("Name", [
        validators.InputRequired(message="Name is required"),
        validators.Length(min=1, max=25, message="Name must be between 1 and 25 characters long.")
    ])
    username = StringField("Username", [
        validators.InputRequired(message="Username is required."),
        validators.Length(min=4, max=25, message="Username must be between 4 and 25 characters long.")
    ])
    email = StringField('Email Address', [
        validators.InputRequired(message="Email is required."),
        validators.Length(min=6, max=254, message="Email must be between 6 and 254 characters long."),
        validators.Email(message="Email must be valid")
    ])
    password = PasswordField("Password", [
        validators.InputRequired(message="Password is required."),
        validators.Length(min=8, max=64, message="Password must be between 8 and 64 characters long.")
    ])
    verify_password = PasswordField("Verify Password", [
        validators.EqualTo("password", message="Passwords must match.")
    ])

# Login form for pre-existing users
class LoginForm(FlaskForm):
    username = StringField("Username", [
        validators.InputRequired(message="Username is required."),
        validators.Length(min=4, max=25, message="Username must be between 4 and 25 characters long.")
    ])
    password = PasswordField("Password", [
        validators.InputRequired(message="Password is required."),
        validators.Length(min=8, max=64, message="Password must be between 8 and 64 characters long.")
    ])

# Announcement form with optional URL for Google Slides
class AnnouncementForm(FlaskForm):
    title = StringField("Title", [
        validators.InputRequired(message="Title is required"),
    ])
    message = TextAreaField("Message", [
        validators.InputRequired(message="Message is required."),
    ])
    url = URLField("URL", [
        validators.Optional(),
        validators.URL(message="Input must be a valid URL.")
    ])