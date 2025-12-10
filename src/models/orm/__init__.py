"""SQLAlchemy ORM models."""

from src.models.orm.base import Base
from src.models.orm.course import Course, CourseMaterial
from src.models.orm.department import Department, ResearchArea
from src.models.orm.lecturer import (
    Lecturer,
    LecturerExpertise,
    LecturerQualification,
    LecturerResearchInterest,
    Publication,
)
from src.models.orm.programme import Programme
from src.models.orm.research import (
    ProjectFunding,
    ProjectOutcome,
    ProjectPublication,
    ResearchProject,
)
from src.models.orm.staff import NonAcademicStaff
from src.models.orm.student import DisciplinaryRecord, Student, StudentGrade
from src.models.orm.tables import (
    course_prerequisite,
    lecturer_course,
    programme_course,
    research_project_member,
    student_course,
)

__all__ = [
    "Base",
    "Course",
    "CourseMaterial",
    "Department",
    "DisciplinaryRecord",
    "Lecturer",
    "LecturerExpertise",
    "LecturerQualification",
    "LecturerResearchInterest",
    "NonAcademicStaff",
    "Programme",
    "ProjectFunding",
    "ProjectOutcome",
    "ProjectPublication",
    "Publication",
    "ResearchArea",
    "ResearchProject",
    "Student",
    "StudentGrade",
    "course_prerequisite",
    "lecturer_course",
    "programme_course",
    "research_project_member",
    "student_course",
]
