"""Junction tables for many-to-many relationships."""

from sqlalchemy import Column, ForeignKey, Integer, String, Table

from src.models.base import Base

# Student <-> Course (M:N)
student_course = Table(
    "student_course",
    Base.metadata,
    Column("student_id", Integer, ForeignKey("student.student_id"), primary_key=True),
    Column("course_id", Integer, ForeignKey("course.course_id"), primary_key=True),
    Column("semester", String(20)),
    Column("enrolment_date", String(10)),
)

# Lecturer <-> Course (M:N)
lecturer_course = Table(
    "lecturer_course",
    Base.metadata,
    Column(
        "lecturer_id", Integer, ForeignKey("lecturer.lecturer_id"), primary_key=True
    ),
    Column("course_id", Integer, ForeignKey("course.course_id"), primary_key=True),
)

# Course <-> Course prerequisites (self-referential M:N)
course_prerequisite = Table(
    "course_prerequisite",
    Base.metadata,
    Column("course_id", Integer, ForeignKey("course.course_id"), primary_key=True),
    Column(
        "prerequisite_id", Integer, ForeignKey("course.course_id"), primary_key=True
    ),
)

# Programme <-> Course (M:N)
programme_course = Table(
    "programme_course",
    Base.metadata,
    Column(
        "programme_id", Integer, ForeignKey("programme.programme_id"), primary_key=True
    ),
    Column("course_id", Integer, ForeignKey("course.course_id"), primary_key=True),
    Column("is_required", Integer, default=0),
)

# ResearchProject <-> Student members (M:N)
research_project_member = Table(
    "research_project_member",
    Base.metadata,
    Column(
        "project_id",
        Integer,
        ForeignKey("research_project.project_id"),
        primary_key=True,
    ),
    Column("student_id", Integer, ForeignKey("student.student_id"), primary_key=True),
)
