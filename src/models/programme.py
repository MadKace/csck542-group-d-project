"""Programme ORM models."""

from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import Base

if TYPE_CHECKING:
    from src.models.course import Course
    from src.models.student import Student


class Programme(Base):
    """Represents an academic programme."""

    __tablename__ = "programme"

    programme_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    degree_awarded: Mapped[str | None] = mapped_column(String(50))
    duration_years: Mapped[int | None]
    enrolment_details: Mapped[str | None] = mapped_column(String(500))

    # Relationships
    students: Mapped[list["Student"]] = relationship(
        back_populates="programme", passive_deletes=True
    )
    courses: Mapped[list["Course"]] = relationship(
        secondary="programme_course", back_populates="programmes", passive_deletes=True
    )
