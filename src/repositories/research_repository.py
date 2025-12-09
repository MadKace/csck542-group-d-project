"""Research project repository for database operations."""

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

    # TODO: Check if "LIKE" is the best operator here
    def search(self, title: str) -> list[ResearchProject]:
        """Search projects by title."""
        query = """
            SELECT * FROM research_project
            WHERE LOWER(title) LIKE LOWER(?)
            ORDER BY title
        """
        return self._execute_query(query, (f"%{title}%",))
