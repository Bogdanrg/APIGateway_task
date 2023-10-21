from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import expression

from core.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(30), unique=True)
    password: Mapped[str]
    email: Mapped[str] = mapped_column(String(60), unique=True)
    is_admin: Mapped[bool] = mapped_column(server_default=expression.false())
    is_active: Mapped[bool] = mapped_column(server_default=expression.true())

    def __repr__(self) -> str:
        return f"User: [{self.id}, {self.username}]"
