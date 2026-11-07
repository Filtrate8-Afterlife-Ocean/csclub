from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String, Boolean, MetaData
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from flask_migrate import Migrate
from datetime import datetime, timezone
from flask_login import LoginManager, UserMixin    
from werkzeug.security import check_password_hash, generate_password_hash

class Base(DeclarativeBase):
    metadata = MetaData(naming_convention={
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    })

db = SQLAlchemy(model_class=Base)
migrate = Migrate()

login_manager = LoginManager()
login_manager.login_view = "auth.login"

class User(UserMixin, db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    password_hash: Mapped[str] = mapped_column()
    is_exec: Mapped[bool] = mapped_column(default=False)
    
    def hash_password(password: str) -> str:
        return generate_password_hash(password)

    def validate_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

class Announcement(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column()
    message: Mapped[str] = mapped_column()
    date: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))
    url: Mapped[str | None] = mapped_column()
