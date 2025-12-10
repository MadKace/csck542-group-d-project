"""Research project repository for database operations."""

from src.exceptions import DatabaseError
from src.models.research import ProjectFunding, ProjectOutcome, ResearchProject
from src.repositories.base import BaseRepository


class ResearchProjectRepository(BaseRepository[ResearchProject]):
    """Repository for ResearchProject entity operations."""

    @property
    def table_name(self) -> str:
        return "research_project"

    @property
    def model_class(self) -> type[ResearchProject]:
        return ResearchProject

    @property
    def primary_key(self) -> str:
        return "project_id"

    # Read

    def get_by_department(self, dept_id: int) -> list[ResearchProject]:
        """Get all research projects in a department."""
        query = """
            SELECT * FROM research_project
            WHERE dept_id = ?
            ORDER BY title
        """
        return self._execute_query(query, (dept_id,))

    def get_by_head_lecturer(self, lecturer_id: int) -> ResearchProject | None:
        """Get the research project headed by a lecturer."""
        query = "SELECT * FROM research_project WHERE head_lecturer_id = ?"
        return self._execute_query_one(query, (lecturer_id,))

    def get_funding(self, project_id: int) -> list[ProjectFunding]:
        """Get all funding sources for a project."""
        query = """
            SELECT * FROM project_funding
            WHERE project_id = ?
            ORDER BY source_name
        """
        rows = self._connection.execute(query, (project_id,))
        return [ProjectFunding.from_row(row) for row in rows]

    def get_outcomes(self, project_id: int) -> list[ProjectOutcome]:
        """Get all outcomes for a project."""
        query = """
            SELECT * FROM project_outcome
            WHERE project_id = ?
            ORDER BY outcome_date DESC
        """
        rows = self._connection.execute(query, (project_id,))
        return [ProjectOutcome.from_row(row) for row in rows]

    def search(self, title: str) -> list[ResearchProject]:
        """Search projects by title."""
        query = """
            SELECT * FROM research_project
            WHERE LOWER(title) LIKE LOWER(?)
            ORDER BY title
        """
        return self._execute_query(query, (f"%{title}%",))

    # Create / Update / Delete

    def add_member(self, project_id: int, student_id: int) -> bool:
        """Add a student member to a research project."""
        query = """
            INSERT INTO research_project_member (project_id, student_id)
            VALUES (?, ?)
        """
        self._connection.execute_write(query, (project_id, student_id))
        return True

    def remove_member(self, project_id: int, student_id: int) -> bool:
        """Remove a student member from a research project."""
        query = """
            DELETE FROM research_project_member
            WHERE project_id = ? AND student_id = ?
        """
        rows_affected = self._connection.execute_delete(
            query, (project_id, student_id)
        )
        return rows_affected > 0

    def add_funding(
        self,
        project_id: int,
        source_name: str,
        amount: float | None = None,
    ) -> ProjectFunding:
        """Add a funding source to a project."""
        query = """
            INSERT INTO project_funding (project_id, source_name, amount)
            VALUES (?, ?, ?)
        """
        new_id = self._connection.execute_write(
            query, (project_id, source_name, amount)
        )
        row = self._connection.execute_one(
            "SELECT * FROM project_funding WHERE funding_id = ?", (new_id,)
        )
        if row is None:
            raise DatabaseError("Failed to retrieve created funding record")
        return ProjectFunding.from_row(row)

    def add_outcome(
        self,
        project_id: int,
        description: str,
        outcome_date: str | None = None,
    ) -> ProjectOutcome:
        """Add an outcome to a project."""
        query = """
            INSERT INTO project_outcome (project_id, description, outcome_date)
            VALUES (?, ?, ?)
        """
        new_id = self._connection.execute_write(
            query, (project_id, description, outcome_date)
        )
        row = self._connection.execute_one(
            "SELECT * FROM project_outcome WHERE outcome_id = ?", (new_id,)
        )
        if row is None:
            raise DatabaseError("Failed to retrieve created outcome record")
        return ProjectOutcome.from_row(row)
