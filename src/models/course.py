"""Course ORM models."""

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import Base

if TYPE_CHECKING:
    from src.models.department import Department
    from src.models.lecturer import Lecturer
    from src.models.programme import Programme
    from src.models.student import Student, StudentGrade


class Course(Base):
    """Represents a university course."""

    __tablename__ = "course"

    course_id: Mapped[int] = mapped_column(primary_key=True)
    course_code: Mapped[str] = mapped_column(String(20))
    name: Mapped[str] = mapped_column(String(100))
    description: Mapped[str | None] = mapped_column(String(500))
    dept_id: Mapped[int | None] = mapped_column(ForeignKey("department.dept_id"))
    level: Mapped[str | None] = mapped_column(String(20))
    credits: Mapped[int | None]
    schedule: Mapped[str | None] = mapped_column(String(100))

    # Relationships
    department: Mapped["Department | None"] = relationship(back_populates="courses")
    materials: Mapped[list["CourseMaterial"]] = relationship(back_populates="course")
    grades: Mapped[list["StudentGrade"]] = relationship(back_populates="course")
    students: Mapped[list["Student"]] = relationship(
        secondary="student_course", back_populates="courses"
    )
    lecturers: Mapped[list["Lecturer"]] = relationship(
        secondary="lecturer_course", back_populates="courses"
    )
    programmes: Mapped[list["Programme"]] = relationship(
        secondary="programme_course", back_populates="courses"
    )
    prerequisites: Mapped[list["Course"]] = relationship(
        secondary="course_prerequisite",
        primaryjoin="Course.course_id == course_prerequisite.c.course_id",
        secondaryjoin="Course.course_id == course_prerequisite.c.prerequisite_id",
        backref="required_for",
    )


class CourseMaterial(Base):
    """Represents a material associated with a course."""

    __tablename__ = "course_material"

    material_id: Mapped[int] = mapped_column(primary_key=True)
    course_id: Mapped[int] = mapped_column(ForeignKey("course.course_id"))
    title: Mapped[str] = mapped_column(String(200))
    material_type: Mapped[str | None] = mapped_column(String(50))
    url: Mapped[str | None] = mapped_column(String(500))

    # Relationships
    course: Mapped["Course"] = relationship(back_populates="materials")
