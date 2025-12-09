"""Model classes representing database entities."""

from src.models.course import Course, CourseMaterial
from src.models.department import Department, ResearchArea
from src.models.lecturer import (
    Lecturer,
    LecturerExpertise,
    LecturerQualification,
    Publication,
)
from src.models.programme import Programme
from src.models.research import ProjectFunding, ProjectOutcome, ResearchProject
from src.models.staff import NonAcademicStaff
from src.models.student import DisciplinaryRecord, Student, StudentGrade

__all__ = [
    "Course",
    "CourseMaterial",
    "Department",
    "DisciplinaryRecord",
    "Lecturer",
    "LecturerExpertise",
    "LecturerQualification",
    "NonAcademicStaff",
    "Programme",
    "ProjectFunding",
    "ProjectOutcome",
    "Publication",
    "ResearchArea",
    "ResearchProject",
    "Student",
    "StudentGrade",
]
