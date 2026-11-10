from functools import wraps

from flask import abort
from flask_login import current_user

from .models import Setting
from .extensions import database


# Retrieve settings
def get_setting() -> Setting:
    setting = database.session.get(Setting, 1)
    if setting is None:
        setting = Setting(id=1)
        database.session.add(setting)
        database.session.commit()
    return setting

# Requires activity to toggle on
def activity_toggle_required(function):
    @wraps(function)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for("main.landing"))
        elif not get_setting().activities_shown:
            abort(403, description="Activity not toggled yet.")
        return function(*args, **kwargs)
    return decorated_function