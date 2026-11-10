from pathlib import Path

from flask import abort, Blueprint, render_template
from flask_login import current_user, login_required

from . import sliding_window, two_pointers
from .extensions import database
from .forms import ButtonForm
from .settings import get_setting

blueprint = Blueprint("activities", __name__, url_prefix="/activities")
blueprint.register_blueprint(two_pointers.blueprint)
blueprint.register_blueprint(sliding_window.blueprint)

# Description files in csclub/static
STATIC_DIR = Path(__file__).parent / "static"

class ActivityDescription:
    def __init__(self, title: str, endpoint: str, filename: str, leetcode_url: str = None) -> None:
        self.title = title
        self.endpoint = endpoint
        with open(STATIC_DIR / filename, "r", encoding="utf-8") as file:
            self.description = file.read()
        self.leetcode_url = leetcode_url

descriptions = [
    ActivityDescription("Two Pointers", "activities.two_pointers.two_pointers", "two_pointers.txt", "https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/description/"),
    ActivityDescription("Sliding Window", "activities.sliding_window.sliding_window", "sliding_window.txt", "https://leetcode.com/problems/longest-substring-without-repeating-characters/description/"),
]

# Activities page
@blueprint.get("/")
@login_required
def activities():
    return render_template("activities/index.html", descriptions=descriptions, activities_shown=get_setting().activities_shown)

# Give points
@blueprint.post("/give-points")
@login_required
def give_points():
    form = ButtonForm()
    if form.validate_on_submit():
        current_user.points += 10
        database.session.commit()
        return "", 204
    abort(400)