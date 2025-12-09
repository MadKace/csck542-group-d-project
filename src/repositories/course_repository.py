"""Course repository for database operations."""

from src.models.course import Course, CourseMaterial
from src.repositories.base import BaseRepository


class CourseRepository(BaseRepository[Course]):
    """Repository for Course entity operations."""

    @property
    def table_name(self) -> str:
        return "course"

    @property
    def model_class(self) -> type[Course]:
        return Course

    @property
    def primary_key(self) -> str:
        return "course_id"

    def get_by_department(self, dept_id: int) -> list[Course]:
        """Get all courses offered by a department."""
        query = """
            SELECT * FROM course
            WHERE dept_id = ?
            ORDER BY course_code
        """
        return self._execute_query(query, (dept_id,))

    def get_by_department_lecturers(self, dept_id: int) -> list[Course]:
        """Get courses taught by lecturers in a department."""
        query = """
            SELECT DISTINCT c.*
            FROM course c
            INNER JOIN lecturer_course lc ON c.course_id = lc.course_id
            INNER JOIN lecturer l ON lc.lecturer_id = l.lecturer_id
            WHERE l.dept_id = ?
            ORDER BY c.course_code
        """
        return self._execute_query(query, (dept_id,))

    def get_by_lecturer(self, lecturer_id: int) -> list[Course]:
        """Get all courses taught by a lecturer."""
        query = """
            SELECT c.*
            FROM course c
            INNER JOIN lecturer_course lc ON c.course_id = lc.course_id
            WHERE lc.lecturer_id = ?
            ORDER BY c.course_code
        """
        return self._execute_query(query, (lecturer_id,))

    def get_materials(self, course_id: int) -> list[CourseMaterial]:
        """Get all materials for a course."""
        query = """
            SELECT * FROM course_material
            WHERE course_id = ?
            ORDER BY title
        """
        rows = self._connection.execute(query, (course_id,))
        return [CourseMaterial.from_row(row) for row in rows]

    def get_prerequisites(self, course_id: int) -> list[Course]:
        """Get all prerequisite courses for a course."""
        query = """
            SELECT c.*
            FROM course c
            INNER JOIN course_prerequisite cp
                ON c.course_id = cp.prerequisite_id
            WHERE cp.course_id = ?
            ORDER BY c.course_code
        """
        return self._execute_query(query, (course_id,))

    def get_by_level(self, level: str) -> list[Course]:
        """Get all courses at a specific level."""
        query = """
            SELECT * FROM course
            WHERE level = ?
            ORDER BY course_code
        """
        return self._execute_query(query, (level,))
    
    # Maybe include get_by_department_level > all courses in a department of a given level

    def get_by_code(self, course_code: str) -> Course | None:
        """Get a course by its course code."""
        query = "SELECT * FROM course WHERE course_code = ?"
        return self._execute_query_one(query, (course_code,))
