"""Lecturer repository for database operations."""

from src.models.lecturer import (
    Lecturer,
    LecturerExpertise,
    LecturerQualification,
    LecturerResearchInterest,
    Publication,
)
from src.repositories.base import BaseRepository


class LecturerRepository(BaseRepository[Lecturer]):
    """Repository for Lecturer entity operations."""

    @property
    def table_name(self) -> str:
        return "lecturer"

    @property
    def model_class(self) -> type[Lecturer]:
        return Lecturer

    @property
    def primary_key(self) -> str:
        return "lecturer_id"

    def get_by_expertise(self, area: str) -> list[Lecturer]:
        """Get lecturers with expertise in a specific area."""
        query = """
            SELECT DISTINCT l.*
            FROM lecturer l
            INNER JOIN lecturer_expertise le ON l.lecturer_id = le.lecturer_id
            WHERE LOWER(le.area) LIKE LOWER(?)
            ORDER BY l.name
        """
        return self._execute_query(query, (f"%{area}%",))

    def get_by_department(self, dept_id: int) -> list[Lecturer]:
        """Get all lecturers in a department."""
        query = """
            SELECT * FROM lecturer
            WHERE dept_id = ?
            ORDER BY name
        """
        return self._execute_query(query, (dept_id,))

    def get_qualifications(self, lecturer_id: int) -> list[LecturerQualification]:
        """Get all qualifications for a lecturer."""
        query = """
            SELECT * FROM lecturer_qualification
            WHERE lecturer_id = ?
            ORDER BY year_awarded DESC
        """
        rows = self._connection.execute(query, (lecturer_id,))
        return [LecturerQualification.from_row(row) for row in rows]

    def get_expertise(self, lecturer_id: int) -> list[LecturerExpertise]:
        """Get all expertise areas for a lecturer."""
        query = """
            SELECT * FROM lecturer_expertise
            WHERE lecturer_id = ?
            ORDER BY area
        """
        rows = self._connection.execute(query, (lecturer_id,))
        return [LecturerExpertise.from_row(row) for row in rows]

    def get_publications(self, lecturer_id: int) -> list[Publication]:
        """Get all publications by a lecturer."""
        query = """
            SELECT * FROM publication
            WHERE lecturer_id = ?
            ORDER BY publication_date DESC
        """
        rows = self._connection.execute(query, (lecturer_id,))
        return [Publication.from_row(row) for row in rows]

    def get_research_interests(
        self,
        lecturer_id: int,
    ) -> list[LecturerResearchInterest]:
        """Get all research interests for a lecturer."""
        query = """
            SELECT * FROM lecturer_research_interest
            WHERE lecturer_id = ?
            ORDER BY interest
        """
        rows = self._connection.execute(query, (lecturer_id,))
        return [LecturerResearchInterest.from_row(row) for row in rows]

