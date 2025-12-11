"""Lecturer ORM models."""

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import Base

if TYPE_CHECKING:
    from src.models.course import Course
    from src.models.department import Department
    from src.models.research import ResearchProject
    from src.models.student import Student


class Lecturer(Base):
    """Represents a university lecturer."""

    __tablename__ = "lecturer"

    lecturer_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    dept_id: Mapped[int | None] = mapped_column(ForeignKey("department.dept_id"))
    course_load: Mapped[int | None]

    # Relationships
    department: Mapped["Department | None"] = relationship(back_populates="lecturers")
    qualifications: Mapped[list["LecturerQualification"]] = relationship(
        back_populates="lecturer"
    )
    expertise_areas: Mapped[list["LecturerExpertise"]] = relationship(
        back_populates="lecturer"
    )
    research_interests: Mapped[list["LecturerResearchInterest"]] = relationship(
        back_populates="lecturer"
    )
    publications: Mapped[list["Publication"]] = relationship(back_populates="lecturer")
    advisees: Mapped[list["Student"]] = relationship(back_populates="advisor")
    courses: Mapped[list["Course"]] = relationship(
        secondary="lecturer_course", back_populates="lecturers"
    )
    research_project: Mapped["ResearchProject | None"] = relationship(
        back_populates="head_lecturer"
    )


class LecturerQualification(Base):
    """Represents an academic qualification of a lecturer."""

    __tablename__ = "lecturer_qualification"

    qualification_id: Mapped[int] = mapped_column(primary_key=True)
    lecturer_id: Mapped[int] = mapped_column(ForeignKey("lecturer.lecturer_id"))
    qualification_name: Mapped[str] = mapped_column(String(100))
    institution: Mapped[str | None] = mapped_column(String(100))
    year_awarded: Mapped[int | None]

    # Relationships
    lecturer: Mapped["Lecturer"] = relationship(back_populates="qualifications")


class LecturerExpertise(Base):
    """Represents an area of expertise for a lecturer."""

    __tablename__ = "lecturer_expertise"

    expertise_id: Mapped[int] = mapped_column(primary_key=True)
    lecturer_id: Mapped[int] = mapped_column(ForeignKey("lecturer.lecturer_id"))
    area: Mapped[str] = mapped_column(String(100))

    # Relationships
    lecturer: Mapped["Lecturer"] = relationship(back_populates="expertise_areas")


class LecturerResearchInterest(Base):
    """Represents a research interest for a lecturer."""

    __tablename__ = "lecturer_research_interest"

    interest_id: Mapped[int] = mapped_column(primary_key=True)
    lecturer_id: Mapped[int] = mapped_column(ForeignKey("lecturer.lecturer_id"))
    interest: Mapped[str] = mapped_column(String(100))

    # Relationships
    lecturer: Mapped["Lecturer"] = relationship(back_populates="research_interests")


class Publication(Base):
    """Represents a publication by a lecturer."""

    __tablename__ = "publication"

    publication_id: Mapped[int] = mapped_column(primary_key=True)
    lecturer_id: Mapped[int] = mapped_column(ForeignKey("lecturer.lecturer_id"))
    title: Mapped[str] = mapped_column(String(200))
    journal: Mapped[str | None] = mapped_column(String(100))
    publication_date: Mapped[str | None] = mapped_column(String(10))

    # Relationships
    lecturer: Mapped["Lecturer"] = relationship(back_populates="publications")
