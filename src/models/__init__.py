"""SQLAlchemy ORM models."""

from src.models.base import Base
from src.models.course import Course, CourseMaterial
from src.models.department import Department, ResearchArea
from src.models.lecturer import (
    Lecturer,
    LecturerExpertise,
    LecturerQualification,
    LecturerResearchInterest,
    Publication,
)
from src.models.programme import Programme
from src.models.research import (
    ProjectFunding,
    ProjectOutcome,
    ProjectPublication,
    ResearchProject,
)
from src.models.staff import NonAcademicStaff
from src.models.student import DisciplinaryRecord, Student, StudentGrade
from src.models.tables import (
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
