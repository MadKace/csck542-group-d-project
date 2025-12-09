"""Staff repository for database operations."""

from src.models.staff import NonAcademicStaff
from src.repositories.base import BaseRepository


class StaffRepository(BaseRepository[NonAcademicStaff]):
    """Repository for NonAcademicStaff entity operations."""

    @property
    def table_name(self) -> str:
        return "non_academic_staff"

    @property
    def model_class(self) -> type[NonAcademicStaff]:
        return NonAcademicStaff

    @property
    def primary_key(self) -> str:
        return "staff_id"

    def get_by_department(self, dept_id: int) -> list[NonAcademicStaff]:
        """Get all staff members in a department."""
        query = """
            SELECT * FROM non_academic_staff
            WHERE dept_id = ?
            ORDER BY name
        """
        return self._execute_query(query, (dept_id,))

    def get_by_job_title(self, job_title: str) -> list[NonAcademicStaff]:
        """Get all staff members with a specific job title."""
        query = """
            SELECT * FROM non_academic_staff
            WHERE LOWER(job_title) LIKE LOWER(?)
            ORDER BY name
        """
        return self._execute_query(query, (f"%{job_title}%",))

    def get_by_employment_type(
        self,
        employment_type: str,
    ) -> list[NonAcademicStaff]:
        """Get all staff members with a specific employment type."""
        query = """
            SELECT * FROM non_academic_staff
            WHERE employment_type = ?
            ORDER BY name
        """
        return self._execute_query(query, (employment_type,))
