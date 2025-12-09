"""Query service providing the main API for database queries."""

from src.repositories import (
    CourseRepository,
    DepartmentRepository,
    LecturerRepository,
    ProgrammeRepository,
    RepositoryFactory,
    StaffRepository,
    StudentRepository,
)


class QueryService:
    """Primary interface for database queries.

    Example:
        service = QueryService()
        students = service.get_students_by_advisor(lecturer_id=1)
    """

    def __init__(self) -> None:
        """Initialise the query service with repositories."""
        self._student_repo: StudentRepository = (
            RepositoryFactory.get_student_repository()
        )
        self._lecturer_repo: LecturerRepository = (
            RepositoryFactory.get_lecturer_repository()
        )
        self._course_repo: CourseRepository = (
            RepositoryFactory.get_course_repository()
        )
        self._department_repo: DepartmentRepository = (
            RepositoryFactory.get_department_repository()
        )
        self._programme_repo: ProgrammeRepository = (
            RepositoryFactory.get_programme_repository()
        )
        self._staff_repo: StaffRepository = (
            RepositoryFactory.get_staff_repository()
        )

    # TODO: Implement query methods
