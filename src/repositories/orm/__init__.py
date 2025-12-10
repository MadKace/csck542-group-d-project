"""SQLAlchemy ORM repositories."""

from src.repositories.orm.course_repository import CourseRepository
from src.repositories.orm.department_repository import DepartmentRepository
from src.repositories.orm.factory import ORMRepositoryFactory
from src.repositories.orm.lecturer_repository import LecturerRepository
from src.repositories.orm.programme_repository import ProgrammeRepository
from src.repositories.orm.research_repository import ResearchProjectRepository
from src.repositories.orm.staff_repository import StaffRepository
from src.repositories.orm.student_repository import StudentRepository

__all__ = [
    "CourseRepository",
    "DepartmentRepository",
    "LecturerRepository",
    "ORMRepositoryFactory",
    "ProgrammeRepository",
    "ResearchProjectRepository",
    "StaffRepository",
    "StudentRepository",
]
