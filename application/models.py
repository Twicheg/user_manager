from typing import List, Dict, Optional

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import String, Float, create_engine
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey


class Base(DeclarativeBase):
    pass


class Users(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[Optional[str]] = mapped_column(String(50))
    country: Mapped[Optional[List["Countries"]]] = relationship(backref="countries", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"User(id={self.id}, name={self.name}, fullname={self.country})"


class Countries(Base):
    __tablename__ = "countries"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    country_id: Mapped[str] = mapped_column(String(2))
    probability: Mapped[float] = mapped_column(Float())
