"""Student ORM models."""

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import Base

if TYPE_CHECKING:
    from src.models.course import Course
    from src.models.lecturer import Lecturer
    from src.models.programme import Programme
    from src.models.research import ResearchProject


class Student(Base):
    """Represents a university student."""

    __tablename__ = "student"

    student_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    date_of_birth: Mapped[str | None] = mapped_column(String(10))
    contact_info: Mapped[str | None] = mapped_column(String(200))
    programme_id: Mapped[int | None] = mapped_column(ForeignKey("programme.programme_id"))
    year_of_study: Mapped[int | None]
    graduation_status: Mapped[str | None] = mapped_column(String(20))
    advisor_id: Mapped[int | None] = mapped_column(ForeignKey("lecturer.lecturer_id"))

    # Relationships
    programme: Mapped["Programme | None"] = relationship(back_populates="students")
    advisor: Mapped["Lecturer | None"] = relationship(back_populates="advisees")
    grades: Mapped[list["StudentGrade"]] = relationship(
        back_populates="student", passive_deletes=True
    )
    disciplinary_records: Mapped[list["DisciplinaryRecord"]] = relationship(
        back_populates="student", passive_deletes=True
    )
    courses: Mapped[list["Course"]] = relationship(
        secondary="student_course", back_populates="students", passive_deletes=True
    )
    research_projects: Mapped[list["ResearchProject"]] = relationship(
        secondary="research_project_member",
        back_populates="student_members",
        passive_deletes=True,
    )


class StudentGrade(Base):
    """Represents a grade record for a student."""

    __tablename__ = "student_grade"

    grade_id: Mapped[int] = mapped_column(primary_key=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("student.student_id"))
    course_id: Mapped[int] = mapped_column(ForeignKey("course.course_id"))
    assessment_type: Mapped[str | None] = mapped_column(String(50))
    grade: Mapped[int | None]
    date_recorded: Mapped[str | None] = mapped_column(String(10))

    # Relationships
    student: Mapped["Student"] = relationship(back_populates="grades")
    course: Mapped["Course"] = relationship(back_populates="grades")


class DisciplinaryRecord(Base):
    """Represents a disciplinary record for a student."""

    __tablename__ = "disciplinary_record"

    record_id: Mapped[int] = mapped_column(primary_key=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("student.student_id"))
    incident_date: Mapped[str | None] = mapped_column(String(10))
    description: Mapped[str | None] = mapped_column(String(500))
    action_taken: Mapped[str | None] = mapped_column(String(200))

    # Relationships
    student: Mapped["Student"] = relationship(back_populates="disciplinary_records")
