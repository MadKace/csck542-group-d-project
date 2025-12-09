"""Student repository for database operations."""

from src.models.student import (
    DisciplinaryRecord,
    Student,
    StudentGrade,
)
from src.repositories.base import BaseRepository


class StudentRepository(BaseRepository[Student]):
    """Repository for Student entity operations."""

    @property
    def table_name(self) -> str:
        return "student"

    @property
    def model_class(self) -> type[Student]:
        return Student

    @property
    def primary_key(self) -> str:
        return "student_id"

    def get_by_advisor(self, lecturer_id: int) -> list[Student]:
        """Get all students advised by a lecturer."""
        query = """
            SELECT * FROM student
            WHERE advisor_id = ?
            ORDER BY name
        """
        return self._execute_query(query, (lecturer_id,))

    def get_in_course_by_lecturer(
        self,
        course_id: int,
        lecturer_id: int,
    ) -> list[Student]:
        """Get students enrolled in a course taught by a specific lecturer."""
        query = """
            SELECT DISTINCT s.*
            FROM student s
            INNER JOIN student_course sc ON s.student_id = sc.student_id
            INNER JOIN lecturer_course lc ON sc.course_id = lc.course_id
            WHERE sc.course_id = ?
              AND lc.lecturer_id = ?
            ORDER BY s.name
        """
        return self._execute_query(query, (course_id, lecturer_id))

    def get_grades(self, student_id: int) -> list[StudentGrade]:
        """Get all grades for a student."""
        query = """
            SELECT * FROM student_grade
            WHERE student_id = ?
            ORDER BY date_recorded DESC
        """
        rows = self._connection.execute(query, (student_id,))
        return [StudentGrade.from_row(row) for row in rows]

    def get_disciplinary_records(self, student_id: int) -> list[DisciplinaryRecord]:
        """Get all disciplinary records for a student."""
        query = """
            SELECT * FROM disciplinary_record
            WHERE student_id = ?
            ORDER BY incident_date DESC
        """
        rows = self._connection.execute(query, (student_id,))
        return [DisciplinaryRecord.from_row(row) for row in rows]

    def get_by_programme(self, programme_id: int) -> list[Student]:
        """Get all students enrolled in a programme."""
        query = """
            SELECT * FROM student
            WHERE programme_id = ?
            ORDER BY year_of_study, name
        """
        return self._execute_query(query, (programme_id,))

    def get_by_course(self, course_id: int) -> list[Student]:
        """Get all students enrolled in a course."""
        query = """
            SELECT s.*
            FROM student s
            INNER JOIN student_course sc ON s.student_id = sc.student_id
            WHERE sc.course_id = ?
            ORDER BY s.name
        """
        return self._execute_query(query, (course_id,))

    def search(self, name: str) -> list[Student]:
        """Search students by name."""
        query = """
            SELECT * FROM student
            WHERE LOWER(name) LIKE LOWER(?)
            ORDER BY name
        """
        return self._execute_query(query, (f"%{name}%",))

    def get_by_research_project(self, project_id: int) -> list[Student]:
        """Get all student members of a research project."""
        query = """
            SELECT s.*
            FROM student s
            INNER JOIN research_project_member rpm
                ON s.student_id = rpm.student_id
            WHERE rpm.project_id = ?
            ORDER BY s.name
        """
        return self._execute_query(query, (project_id,))
