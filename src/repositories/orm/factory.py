"""Repository factory for creating ORM repository instances."""

from sqlalchemy.orm import Session

from src.database import get_session
from src.repositories.orm.course_repository import CourseRepository
from src.repositories.orm.department_repository import DepartmentRepository
from src.repositories.orm.lecturer_repository import LecturerRepository
from src.repositories.orm.programme_repository import ProgrammeRepository
from src.repositories.orm.research_repository import ResearchProjectRepository
from src.repositories.orm.staff_repository import StaffRepository
from src.repositories.orm.student_repository import StudentRepository


class ORMRepositoryFactory:
    """Factory for creating ORM repository instances with shared sessions."""

    def __init__(self, session: Session | None = None) -> None:
        """Initialise factory with optional session."""
        self._session = session or get_session()
        self._instances: dict[type, object] = {}

    @property
    def session(self) -> Session:
        """Get the current session."""
        return self._session

    def get_student_repository(self) -> StudentRepository:
        """Get or create a StudentRepository instance."""
        if StudentRepository not in self._instances:
            self._instances[StudentRepository] = StudentRepository(self._session)
        return self._instances[StudentRepository]

    def get_lecturer_repository(self) -> LecturerRepository:
        """Get or create a LecturerRepository instance."""
        if LecturerRepository not in self._instances:
            self._instances[LecturerRepository] = LecturerRepository(self._session)
        return self._instances[LecturerRepository]

    def get_course_repository(self) -> CourseRepository:
        """Get or create a CourseRepository instance."""
        if CourseRepository not in self._instances:
            self._instances[CourseRepository] = CourseRepository(self._session)
        return self._instances[CourseRepository]

    def get_department_repository(self) -> DepartmentRepository:
        """Get or create a DepartmentRepository instance."""
        if DepartmentRepository not in self._instances:
            self._instances[DepartmentRepository] = DepartmentRepository(self._session)
        return self._instances[DepartmentRepository]

    def get_programme_repository(self) -> ProgrammeRepository:
        """Get or create a ProgrammeRepository instance."""
        if ProgrammeRepository not in self._instances:
            self._instances[ProgrammeRepository] = ProgrammeRepository(self._session)
        return self._instances[ProgrammeRepository]

    def get_staff_repository(self) -> StaffRepository:
        """Get or create a StaffRepository instance."""
        if StaffRepository not in self._instances:
            self._instances[StaffRepository] = StaffRepository(self._session)
        return self._instances[StaffRepository]

    def get_research_project_repository(self) -> ResearchProjectRepository:
        """Get or create a ResearchProjectRepository instance."""
        if ResearchProjectRepository not in self._instances:
            self._instances[ResearchProjectRepository] = ResearchProjectRepository(
                self._session
            )
        return self._instances[ResearchProjectRepository]

    def commit(self) -> None:
        """Commit the current transaction."""
        self._session.commit()

    def rollback(self) -> None:
        """Rollback the current transaction."""
        self._session.rollback()

    def close(self) -> None:
        """Close the session."""
        self._session.close()
