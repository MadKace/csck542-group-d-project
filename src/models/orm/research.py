"""Research project ORM models."""

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.orm.base import Base

if TYPE_CHECKING:
    from src.models.orm.department import Department
    from src.models.orm.lecturer import Lecturer
    from src.models.orm.student import Student


class ResearchProject(Base):
    """Represents a research project."""

    __tablename__ = "research_project"

    project_id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    head_lecturer_id: Mapped[int] = mapped_column(
        ForeignKey("lecturer.lecturer_id"), unique=True
    )
    dept_id: Mapped[int | None] = mapped_column(ForeignKey("department.dept_id"))
    start_date: Mapped[str | None] = mapped_column(String(10))
    end_date: Mapped[str | None] = mapped_column(String(10))

    # Relationships
    head_lecturer: Mapped["Lecturer"] = relationship(back_populates="research_project")
    department: Mapped["Department | None"] = relationship(
        back_populates="research_projects"
    )
    funding_sources: Mapped[list["ProjectFunding"]] = relationship(
        back_populates="project"
    )
    outcomes: Mapped[list["ProjectOutcome"]] = relationship(back_populates="project")
    student_members: Mapped[list["Student"]] = relationship(
        secondary="research_project_member", back_populates="research_projects"
    )


class ProjectFunding(Base):
    """Represents a funding source for a research project."""

    __tablename__ = "project_funding"

    funding_id: Mapped[int] = mapped_column(primary_key=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("research_project.project_id"))
    source_name: Mapped[str] = mapped_column(String(100))
    amount: Mapped[float | None] = mapped_column(Numeric(12, 2))

    # Relationships
    project: Mapped["ResearchProject"] = relationship(back_populates="funding_sources")


class ProjectOutcome(Base):
    """Represents an outcome from a research project."""

    __tablename__ = "project_outcome"

    outcome_id: Mapped[int] = mapped_column(primary_key=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("research_project.project_id"))
    description: Mapped[str] = mapped_column(String(500))
    outcome_date: Mapped[str | None] = mapped_column(String(10))

    # Relationships
    project: Mapped["ResearchProject"] = relationship(back_populates="outcomes")
