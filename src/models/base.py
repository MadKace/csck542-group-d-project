"""SQLAlchemy declarative base."""

from typing import Any

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Base class for all ORM models."""

    @property
    def as_dict(self) -> dict[str, Any]:
        """Return model attributes as a dictionary."""
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
