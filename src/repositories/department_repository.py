"""Department repository for database operations."""

from src.models.department import Department, ResearchArea
from src.repositories.base import BaseRepository


class DepartmentRepository(BaseRepository[Department]):
    """Repository for Department entity operations."""

    @property
    def table_name(self) -> str:
        return "department"

    @property
    def model_class(self) -> type[Department]:
        return Department

    @property
    def primary_key(self) -> str:
        return "dept_id"

    def get_by_name(self, name: str) -> Department | None:
        """Get a department by its name."""
        query = "SELECT * FROM department WHERE name = ?"
        return self._execute_query_one(query, (name,))

    def get_by_faculty(self, faculty: str) -> list[Department]:
        """Get all departments in a faculty."""
        query = """
            SELECT * FROM department
            WHERE faculty = ?
            ORDER BY name
        """
        return self._execute_query(query, (faculty,))

    def get_research_areas(self, dept_id: int) -> list[ResearchArea]:
        """Get all research areas for a department."""
        query = """
            SELECT * FROM department_research_area
            WHERE dept_id = ?
            ORDER BY area
        """
        rows = self._connection.execute(query, (dept_id,))
        return [ResearchArea.from_row(row) for row in rows]

    def get_departments_with_research_area(self, area: str) -> list[Department]:
        """Get departments with a matching research area."""
        query = """
            SELECT DISTINCT d.*
            FROM department d
            INNER JOIN department_research_area dra ON d.dept_id = dra.dept_id
            WHERE LOWER(dra.area) LIKE LOWER(?)
            ORDER BY d.name
        """
        return self._execute_query(query, (f"%{area}%",))

    def search(self, name: str) -> list[Department]:
        """Search departments by name."""
        query = """
            SELECT * FROM department
            WHERE LOWER(name) LIKE LOWER(?)
            ORDER BY name
        """
        return self._execute_query(query, (f"%{name}%",))
