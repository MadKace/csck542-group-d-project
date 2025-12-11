"""Repository layer for database access."""

from src.repositories.base import BaseRepository
from src.repositories.course_repository import CourseRepository
from src.repositories.department_repository import DepartmentRepository
from src.repositories.factory import RepositoryFactory
from src.repositories.lecturer_repository import LecturerRepository
from src.repositories.programme_repository import ProgrammeRepository
from src.repositories.research_repository import ResearchProjectRepository
from src.repositories.staff_repository import StaffRepository
from src.repositories.student_repository import StudentRepository

__all__ = [
    "BaseRepository",
    "CourseRepository",
    "DepartmentRepository",
    "LecturerRepository",
    "ProgrammeRepository",
    "RepositoryFactory",
    "ResearchProjectRepository",
    "StaffRepository",
    "StudentRepository",
]
