"""Department ORM models."""

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.orm.base import Base

if TYPE_CHECKING:
    from src.models.orm.course import Course
    from src.models.orm.lecturer import Lecturer
    from src.models.orm.research import ResearchProject
    from src.models.orm.staff import NonAcademicStaff


class Department(Base):
    """Represents a university department."""

    __tablename__ = "department"

    dept_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    faculty: Mapped[str | None] = mapped_column(String(100))

    # Relationships
    research_areas: Mapped[list["ResearchArea"]] = relationship(
        back_populates="department"
    )
    lecturers: Mapped[list["Lecturer"]] = relationship(back_populates="department")
    courses: Mapped[list["Course"]] = relationship(back_populates="department")
    staff: Mapped[list["NonAcademicStaff"]] = relationship(
        back_populates="department"
    )
    research_projects: Mapped[list["ResearchProject"]] = relationship(
        back_populates="department"
    )


class ResearchArea(Base):
    """Represents a research area within a department."""

    __tablename__ = "department_research_area"

    area_id: Mapped[int] = mapped_column(primary_key=True)
    dept_id: Mapped[int] = mapped_column(ForeignKey("department.dept_id"))
    area: Mapped[str] = mapped_column(String(100))

    # Relationships
    department: Mapped["Department"] = relationship(back_populates="research_areas")
