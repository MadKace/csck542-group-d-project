"""API service providing the main interface for database access."""

from src.database import get_session
from src.repositories import (
    CourseRepository,
    DepartmentRepository,
    LecturerRepository,
    ProgrammeRepository,
    RepositoryFactory,
    ResearchProjectRepository,
    StaffRepository,
    StudentRepository,
)


class APIService:
    """Facade providing a single entry point for all data access.

    Singleton that exposes repositories as properties for GUI consumption.
    Uses a shared session for transaction consistency.

    Example:
        api = APIService()
        students = api.student_repo.get_by_advisor(lecturer_id=1)
        api.commit()  # Commit changes
    """

    _instance: "APIService | None" = None

    def __new__(cls) -> "APIService":
        """Return the singleton instance, creating it if necessary."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialise()
        return cls._instance

    def _initialise(self) -> None:
        """Initialise the service with a factory instance."""
        self._factory = RepositoryFactory(get_session())

    @property
    def student_repo(self) -> StudentRepository:
        """Access student data operations."""
        return self._factory.get_student_repository()

    @property
    def lecturer_repo(self) -> LecturerRepository:
        """Access lecturer data operations."""
        return self._factory.get_lecturer_repository()

    @property
    def course_repo(self) -> CourseRepository:
        """Access course data operations."""
        return self._factory.get_course_repository()

    @property
    def department_repo(self) -> DepartmentRepository:
        """Access department data operations."""
        return self._factory.get_department_repository()

    @property
    def programme_repo(self) -> ProgrammeRepository:
        """Access programme data operations."""
        return self._factory.get_programme_repository()

    @property
    def staff_repo(self) -> StaffRepository:
        """Access staff data operations."""
        return self._factory.get_staff_repository()

    @property
    def research_project_repo(self) -> ResearchProjectRepository:
        """Access research project data operations."""
        return self._factory.get_research_project_repository()

    def commit(self) -> None:
        """Commit the current transaction."""
        self._factory.commit()

    def rollback(self) -> None:
        """Rollback the current transaction."""
        self._factory.rollback()

    def close(self) -> None:
        """Close the session and reset the singleton."""
        self._factory.close()
        APIService._instance = None
