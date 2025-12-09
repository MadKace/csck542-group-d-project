"""Programme repository for database operations."""

from src.models.course import Course
from src.models.programme import Programme
from src.repositories.base import BaseRepository


class ProgrammeRepository(BaseRepository[Programme]):
    """Repository for Programme entity operations."""

    @property
    def table_name(self) -> str:
        return "programme"

    @property
    def model_class(self) -> type[Programme]:
        return Programme

    @property
    def primary_key(self) -> str:
        return "programme_id"

    def get_by_name(self, name: str) -> Programme | None:
        """Get a programme by its name."""
        query = "SELECT * FROM programme WHERE name = ?"
        return self._execute_query_one(query, (name,))

    def get_by_degree(self, degree_awarded: str) -> list[Programme]:
        """Get all programmes awarding a specific degree."""
        query = """
            SELECT * FROM programme
            WHERE degree_awarded = ?
            ORDER BY name
        """
        return self._execute_query(query, (degree_awarded,))

    def get_programme_courses(
        self,
        programme_id: int,
        required_only: bool = False,
    ) -> list[Course]:
        """Get all courses in a programme."""
        if required_only:
            query = """
                SELECT c.*
                FROM course c
                INNER JOIN programme_course pc ON c.course_id = pc.course_id
                WHERE pc.programme_id = ?
                  AND pc.is_required = 1
                ORDER BY c.course_code
            """
        else:
            query = """
                SELECT c.*
                FROM course c
                INNER JOIN programme_course pc ON c.course_id = pc.course_id
                WHERE pc.programme_id = ?
                ORDER BY c.course_code
            """

        rows = self._connection.execute(query, (programme_id,))
        return [Course.from_row(row) for row in rows]
