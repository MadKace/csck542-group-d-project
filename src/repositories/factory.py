"""Repository factory for creating repository instances."""

from src.repositories.base import BaseRepository
from src.repositories.course_repository import CourseRepository
from src.repositories.department_repository import DepartmentRepository
from src.repositories.lecturer_repository import LecturerRepository
from src.repositories.programme_repository import ProgrammeRepository
from src.repositories.staff_repository import StaffRepository
from src.repositories.student_repository import StudentRepository


class RepositoryFactory:
    """Factory for creating and caching repository instances."""

    _instances: dict[type, BaseRepository] = {}

    @classmethod
    def get_student_repository(cls) -> StudentRepository:
        """Get or create a StudentRepository instance."""
        if StudentRepository not in cls._instances:
            cls._instances[StudentRepository] = StudentRepository()
        return cls._instances[StudentRepository]

    @classmethod
    def get_lecturer_repository(cls) -> LecturerRepository:
        """Get or create a LecturerRepository instance."""
        if LecturerRepository not in cls._instances:
            cls._instances[LecturerRepository] = LecturerRepository()
        return cls._instances[LecturerRepository]

    @classmethod
    def get_course_repository(cls) -> CourseRepository:
        """Get or create a CourseRepository instance."""
        if CourseRepository not in cls._instances:
            cls._instances[CourseRepository] = CourseRepository()
        return cls._instances[CourseRepository]

    @classmethod
    def get_department_repository(cls) -> DepartmentRepository:
        """Get or create a DepartmentRepository instance."""
        if DepartmentRepository not in cls._instances:
            cls._instances[DepartmentRepository] = DepartmentRepository()
        return cls._instances[DepartmentRepository]

    @classmethod
    def get_programme_repository(cls) -> ProgrammeRepository:
        """Get or create a ProgrammeRepository instance."""
        if ProgrammeRepository not in cls._instances:
            cls._instances[ProgrammeRepository] = ProgrammeRepository()
        return cls._instances[ProgrammeRepository]

    @classmethod
    def get_staff_repository(cls) -> StaffRepository:
        """Get or create a StaffRepository instance."""
        if StaffRepository not in cls._instances:
            cls._instances[StaffRepository] = StaffRepository()
        return cls._instances[StaffRepository]
