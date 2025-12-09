"""API service providing the main interface for database access."""

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

    Example:
        api = APIService()
        students = api.student_repo.get_by_advisor(lecturer_id=1)
        courses = api.course_repo.get_by_department(dept_id=1)
    """

    _instance: "APIService | None" = None

    def __new__(cls) -> "APIService":
        """Return the singleton instance, creating it if necessary."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialise()
        return cls._instance

    def _initialise(self) -> None:
        """Initialise the service with repository instances."""
        self._student_repo = RepositoryFactory.get_student_repository()
        self._lecturer_repo = RepositoryFactory.get_lecturer_repository()
        self._course_repo = RepositoryFactory.get_course_repository()
        self._department_repo = RepositoryFactory.get_department_repository()
        self._programme_repo = RepositoryFactory.get_programme_repository()
        self._staff_repo = RepositoryFactory.get_staff_repository()
        self._research_project_repo = (
            RepositoryFactory.get_research_project_repository()
        )

    @property
    def student_repo(self) -> StudentRepository:
        """Access student data operations."""
        return self._student_repo

    @property
    def lecturer_repo(self) -> LecturerRepository:
        """Access lecturer data operations."""
        return self._lecturer_repo

    @property
    def course_repo(self) -> CourseRepository:
        """Access course data operations."""
        return self._course_repo

    @property
    def department_repo(self) -> DepartmentRepository:
        """Access department data operations."""
        return self._department_repo

    @property
    def programme_repo(self) -> ProgrammeRepository:
        """Access programme data operations."""
        return self._programme_repo

    @property
    def staff_repo(self) -> StaffRepository:
        """Access staff data operations."""
        return self._staff_repo

    @property
    def research_project_repo(self) -> ResearchProjectRepository:
        """Access research project data operations."""
        return self._research_project_repo
