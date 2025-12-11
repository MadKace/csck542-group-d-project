"""Research project repository using SQLAlchemy ORM."""

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from src.models.research import ProjectFunding, ProjectOutcome, ResearchProject
from src.models.tables import research_project_member
from src.repositories.base import BaseRepository


class ResearchProjectRepository(BaseRepository[ResearchProject]):
    """Repository for ResearchProject entity operations."""

    def __init__(self, session: Session | None = None) -> None:
        super().__init__(session)

    @property
    def model_class(self) -> type[ResearchProject]:
        return ResearchProject

    def get_by_department(self, dept_id: int) -> list[ResearchProject]:
        """Get all research projects in a department."""
        stmt = (
            select(ResearchProject)
            .where(ResearchProject.dept_id == dept_id)
            .order_by(ResearchProject.title)
        )
        return list(self._session.scalars(stmt).all())

    def get_by_head_lecturer(self, lecturer_id: int) -> ResearchProject | None:
        """Get the research project headed by a lecturer."""
        stmt = select(ResearchProject).where(
            ResearchProject.head_lecturer_id == lecturer_id
        )
        return self._session.scalar(stmt)

    def get_funding(self, project_id: int) -> list[ProjectFunding]:
        """Get all funding sources for a project."""
        stmt = (
            select(ProjectFunding)
            .where(ProjectFunding.project_id == project_id)
            .order_by(ProjectFunding.source_name)
        )
        return list(self._session.scalars(stmt).all())

    def get_outcomes(self, project_id: int) -> list[ProjectOutcome]:
        """Get all outcomes for a project."""
        stmt = (
            select(ProjectOutcome)
            .where(ProjectOutcome.project_id == project_id)
            .order_by(ProjectOutcome.outcome_date.desc())
        )
        return list(self._session.scalars(stmt).all())

    def search(self, title: str) -> list[ResearchProject]:
        """Search projects by title."""
        stmt = (
            select(ResearchProject)
            .where(func.lower(ResearchProject.title).like(func.lower(f"%{title}%")))
            .order_by(ResearchProject.title)
        )
        return list(self._session.scalars(stmt).all())

    def add_member(self, project_id: int, student_id: int) -> bool:
        """Add a student member to a research project."""
        stmt = research_project_member.insert().values(
            project_id=project_id, student_id=student_id
        )
        self._session.execute(stmt)
        self._session.flush()
        return True

    def remove_member(self, project_id: int, student_id: int) -> bool:
        """Remove a student member from a research project."""
        stmt = research_project_member.delete().where(
            (research_project_member.c.project_id == project_id)
            & (research_project_member.c.student_id == student_id)
        )
        result = self._session.execute(stmt)
        self._session.flush()
        return result.rowcount > 0

    def add_funding(
        self,
        project_id: int,
        source_name: str,
        amount: float | None = None,
    ) -> ProjectFunding:
        """Add a funding source to a project."""
        funding = ProjectFunding(
            project_id=project_id,
            source_name=source_name,
            amount=amount,
        )
        self._session.add(funding)
        self._session.flush()
        self._session.refresh(funding)
        return funding

    def add_outcome(
        self,
        project_id: int,
        description: str,
        outcome_date: str | None = None,
    ) -> ProjectOutcome:
        """Add an outcome to a project."""
        outcome = ProjectOutcome(
            project_id=project_id,
            description=description,
            outcome_date=outcome_date,
        )
        self._session.add(outcome)
        self._session.flush()
        self._session.refresh(outcome)
        return outcome
