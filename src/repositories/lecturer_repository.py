"""Lecturer repository for database operations."""

from src.exceptions import DatabaseError
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

    # Read

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

    def search(self, name: str) -> list[Lecturer]:
        """Search lecturers by name."""
        query = """
            SELECT * FROM lecturer
            WHERE LOWER(name) LIKE LOWER(?)
            ORDER BY name
        """
        return self._execute_query(query, (f"%{name}%",))

    # Create / Update / Delete

    def assign_to_course(self, lecturer_id: int, course_id: int) -> bool:
        """Assign a lecturer to teach a course."""
        query = "INSERT INTO lecturer_course (lecturer_id, course_id) VALUES (?, ?)"
        self._connection.execute_write(query, (lecturer_id, course_id))
        return True

    def unassign_from_course(self, lecturer_id: int, course_id: int) -> bool:
        """Remove a lecturer from a course."""
        query = (
            "DELETE FROM lecturer_course "
            "WHERE lecturer_id = ? AND course_id = ?"
        )
        rows_affected = self._connection.execute_delete(
            query, (lecturer_id, course_id)
        )
        return rows_affected > 0

    def add_qualification(
        self,
        lecturer_id: int,
        qualification_name: str,
        institution: str | None = None,
        year_awarded: int | None = None,
    ) -> LecturerQualification:
        """Add a qualification for a lecturer."""
        query = """
            INSERT INTO lecturer_qualification
                (lecturer_id, qualification_name, institution, year_awarded)
            VALUES (?, ?, ?, ?)
        """
        new_id = self._connection.execute_write(
            query, (lecturer_id, qualification_name, institution, year_awarded)
        )
        row = self._connection.execute_one(
            "SELECT * FROM lecturer_qualification WHERE qualification_id = ?",
            (new_id,),
        )
        if row is None:
            raise DatabaseError("Failed to retrieve created qualification")
        return LecturerQualification.from_row(row)

    def add_expertise(self, lecturer_id: int, area: str) -> LecturerExpertise:
        """Add an expertise area for a lecturer."""
        query = "INSERT INTO lecturer_expertise (lecturer_id, area) VALUES (?, ?)"
        new_id = self._connection.execute_write(query, (lecturer_id, area))
        row = self._connection.execute_one(
            "SELECT * FROM lecturer_expertise WHERE expertise_id = ?", (new_id,)
        )
        if row is None:
            raise DatabaseError("Failed to retrieve created expertise")
        return LecturerExpertise.from_row(row)

    def add_publication(
        self,
        lecturer_id: int,
        title: str,
        journal: str | None = None,
        publication_date: str | None = None,
    ) -> Publication:
        """Add a publication for a lecturer."""
        query = """
            INSERT INTO publication (lecturer_id, title, journal, publication_date)
            VALUES (?, ?, ?, ?)
        """
        new_id = self._connection.execute_write(
            query, (lecturer_id, title, journal, publication_date)
        )
        row = self._connection.execute_one(
            "SELECT * FROM publication WHERE publication_id = ?", (new_id,)
        )
        if row is None:
            raise DatabaseError("Failed to retrieve created publication")
        return Publication.from_row(row)

    def add_research_interest(
        self,
        lecturer_id: int,
        interest: str,
    ) -> LecturerResearchInterest:
        """Add a research interest for a lecturer."""
        query = """
            INSERT INTO lecturer_research_interest (lecturer_id, interest)
            VALUES (?, ?)
        """
        new_id = self._connection.execute_write(query, (lecturer_id, interest))
        row = self._connection.execute_one(
            "SELECT * FROM lecturer_research_interest WHERE interest_id = ?",
            (new_id,),
        )
        if row is None:
            raise DatabaseError("Failed to retrieve created research interest")
        return LecturerResearchInterest.from_row(row)
