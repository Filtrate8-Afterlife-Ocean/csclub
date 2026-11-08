from flask import url_for

class ActivityDescription:
    def __init__(self, title: str, url: str, description_path: str) -> None:
        self.title = title
        self.url = url
        with open(description_path, "r", encoding="utf-8") as file:
            self.description = file.read()

two_pointers_description = ActivityDescription("Two Pointers", url_for('activities.two_pointers.two_pointers'))