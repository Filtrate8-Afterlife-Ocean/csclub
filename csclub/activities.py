from pathlib import Path

from flask import Blueprint, render_template
from flask_login import login_required

from . import sliding_window, two_pointers

blueprint = Blueprint("activities", __name__, url_prefix="/activities")
blueprint.register_blueprint(two_pointers.blueprint)
blueprint.register_blueprint(sliding_window.blueprint)

# Description files in csclub/static
STATIC_DIR = Path(__file__).parent / "static"

class ActivityDescription:
    def __init__(self, title: str, endpoint: str, filename: str) -> None:
        self.title = title
        self.endpoint = endpoint
        with open(STATIC_DIR / filename, "r", encoding="utf-8") as file:
            self.description = file.read()

descriptions = [
    ActivityDescription("Two Pointers", "activities.two_pointers.two_pointers", "two_pointers.txt"),
    ActivityDescription("Sliding Window", "activities.sliding_window.sliding_window", "sliding_window.txt"),
]

# Activities page
@blueprint.get("/")
@login_required
def activities():
    return render_template("activities/index.html", descriptions=descriptions)