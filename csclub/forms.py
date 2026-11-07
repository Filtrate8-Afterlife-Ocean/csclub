from wtforms import Form, StringField, validators

class RegisterForm(Form):
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
        validators.Length(min=6, max=35, message="Email must be between 6 and 35 characters long."),
        validators.Email(message="Email must be valid")
    ])
    password = StringField("Password", [
        validators.InputRequired(message=_("Password is required.")),
        validators.Length(min=8, max=64, message="Password must be between 8 and 64 characters long.")
    ])
    verify_password = StringField("Verify Password", [
        validators.EqualTo("password", message="Passwords must match.")
    ])

class Login(Form):
    username = StringField("Username", [
        validators.InputRequired(message="Username is required."),
        validators.Length(min=4, max=25, message="Username must be between 4 and 25 characters long.")
    ])
    password = StringField("Password", [
        validators.InputRequired(message="Password is required."),
        validators.Length(min=8, max=64, message="Password must be between 8 and 64 characters long.")
    ])

class Anouncement(Form):
    title = StringField("Title", [
        validators.InputRequired(message="Title is required"),
    ])
    message = StringField("Message", [
        validators.InputRequired(message="Message is required."),
    ])