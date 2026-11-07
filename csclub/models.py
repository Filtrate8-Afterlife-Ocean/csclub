from datetime import datetime, timezone

from flask_login import UserMixin
from sqlalchemy import Boolean, Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from werkzeug.security import check_password_hash, generate_password_hash

from .extensions import database


# Users can be regular members or executives
class User(UserMixin, database.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    password_hash: Mapped[str] = mapped_column()
    is_exec: Mapped[bool] = mapped_column(default=False)
    # attendance_count: Mapped[int] = mapped_column(default=0)
    
    def hash_password(password: str) -> str:
        return generate_password_hash(password)

    def validate_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

# Announcements with optional Google Slides link
class Announcement(database.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column()
    message: Mapped[str] = mapped_column()
    date: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))
    url: Mapped[str | None] = mapped_column()
